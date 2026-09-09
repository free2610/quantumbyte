import os
import json
import logging
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import aiosqlite

from app.config import settings
from app.core.models import QuizQuestionModel
from app.services.preloaded_data import PRELOADED_QUESTIONS

logger = logging.getLogger(__name__)


class Database:
    """Asynchronous SQLite database manager."""

    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.DATABASE_PATH
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensures the parent directory for the SQLite database file exists."""
        dir_name = os.path.dirname(self.db_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[aiosqlite.Connection, None]:
        """Context manager that yields an active SQLite connection with WAL mode enabled."""
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            await conn.execute("PRAGMA foreign_keys = ON;")
            await conn.execute("PRAGMA journal_mode = WAL;")
            yield conn

    async def init_db(self) -> None:
        """Initializes database tables and seeds initial preloaded questions."""
        self._ensure_dir()
        async with self.get_connection() as conn:
            # Users table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT NOT NULL,
                    language TEXT NOT NULL DEFAULT 'uz',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Preloaded & Admin questions table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS premade_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    lang TEXT NOT NULL,
                    question TEXT NOT NULL,
                    options_json TEXT NOT NULL,
                    correct_index INTEGER NOT NULL,
                    explanation TEXT NOT NULL,
                    created_by INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Quiz results table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS quiz_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    test_type TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    total_questions INTEGER NOT NULL,
                    percentage REAL NOT NULL,
                    time_spent_seconds INTEGER NOT NULL,
                    answers_json TEXT NOT NULL,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
            """)

            # Daily AI usage tracking table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS ai_daily_usage (
                    user_id INTEGER NOT NULL,
                    usage_date TEXT NOT NULL,
                    request_count INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, usage_date),
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                );
            """)

            # Create indices for fast querying
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_premade_cat_lang ON premade_questions(category, lang);")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_results_user_type ON quiz_results(user_id, test_type);")

            await conn.commit()

            # Seed questions if table is empty
            await self._seed_questions_if_empty(conn)

    async def _seed_questions_if_empty(self, conn: aiosqlite.Connection) -> None:
        """Seeds curated initial questions if none exist in the database."""
        async with conn.execute("SELECT COUNT(*) FROM premade_questions;") as cursor:
            row = await cursor.fetchone()
            count = row[0] if row else 0

        if count == 0:
            logger.info("Dastlabki tayyor savollar bazaga yuklanmoqda (%d ta)...", len(PRELOADED_QUESTIONS))
            for item in PRELOADED_QUESTIONS:
                await conn.execute(
                    """
                    INSERT INTO premade_questions (category, lang, question, options_json, correct_index, explanation, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, 0);
                    """,
                    (
                        item["category"],
                        item["lang"],
                        item["question"],
                        json.dumps(item["options"], ensure_ascii=False),
                        item["correct_index"],
                        item["explanation"],
                    ),
                )
            await conn.commit()
            logger.info("Dastlabki savollar muvaffaqiyatli saqlandi.")

    async def get_or_create_user(
        self, user_id: int, username: str | None, full_name: str, default_lang: str = "uz"
    ) -> dict:
        """Fetches existing user or inserts a new user record."""
        async with self.get_connection() as conn:
            async with conn.execute("SELECT * FROM users WHERE user_id = ?;", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    # Update username/fullname if changed
                    await conn.execute(
                        "UPDATE users SET username = ?, full_name = ? WHERE user_id = ?;",
                        (username, full_name, user_id),
                    )
                    await conn.commit()
                    return dict(row)

            # Insert new user
            await conn.execute(
                "INSERT INTO users (user_id, username, full_name, language) VALUES (?, ?, ?, ?);",
                (user_id, username, full_name, default_lang),
            )
            await conn.commit()
            return {
                "user_id": user_id,
                "username": username,
                "full_name": full_name,
                "language": default_lang,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

    async def get_user_language(self, user_id: int) -> str:
        """Returns the chosen language of a user, defaulting to settings.DEFAULT_LANGUAGE."""
        async with self.get_connection() as conn:
            async with conn.execute("SELECT language FROM users WHERE user_id = ?;", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row and row["language"]:
                    return row["language"]
        return settings.DEFAULT_LANGUAGE

    async def set_user_language(self, user_id: int, lang: str) -> None:
        """Updates user's preferred language."""
        if lang not in ("uz", "ru"):
            lang = "uz"
        async with self.get_connection() as conn:
            await conn.execute("UPDATE users SET language = ? WHERE user_id = ?;", (lang, user_id))
            await conn.commit()

    async def get_ai_daily_usage(self, user_id: int, date_str: str) -> int:
        """Returns the number of AI requests made by user on a given date (YYYY-MM-DD)."""
        async with self.get_connection() as conn:
            async with conn.execute(
                "SELECT request_count FROM ai_daily_usage WHERE user_id = ? AND usage_date = ?;",
                (user_id, date_str),
            ) as cursor:
                row = await cursor.fetchone()
                return row["request_count"] if row else 0

    async def increment_ai_daily_usage(self, user_id: int, date_str: str) -> int:
        """Increments AI daily usage counter and returns the updated count."""
        async with self.get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO ai_daily_usage (user_id, usage_date, request_count)
                VALUES (?, ?, 1)
                ON CONFLICT(user_id, usage_date) DO UPDATE SET request_count = request_count + 1;
                """,
                (user_id, date_str),
            )
            await conn.commit()
            async with conn.execute(
                "SELECT request_count FROM ai_daily_usage WHERE user_id = ? AND usage_date = ?;",
                (user_id, date_str),
            ) as cursor:
                row = await cursor.fetchone()
                return row["request_count"] if row else 1

    async def save_quiz_result(
        self,
        user_id: int,
        test_type: str,
        topic: str,
        score: int,
        total_questions: int,
        percentage: float,
        time_spent_seconds: int,
        answers: list[dict],
    ) -> int:
        """Saves a finished quiz session result to the database."""
        async with self.get_connection() as conn:
            cursor = await conn.execute(
                """
                INSERT INTO quiz_results (
                    user_id, test_type, topic, score, total_questions, 
                    percentage, time_spent_seconds, answers_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """,
                (
                    user_id,
                    test_type,
                    topic,
                    score,
                    total_questions,
                    percentage,
                    time_spent_seconds,
                    json.dumps(answers, ensure_ascii=False),
                ),
            )
            await conn.commit()
            return cursor.lastrowid or 0

    async def get_user_stats(self, user_id: int) -> dict:
        """Aggregates user stats for tests taken."""
        async with self.get_connection() as conn:
            # Total quizzes
            async with conn.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id = ?;", (user_id,)) as cur:
                total_quizzes = (await cur.fetchone())[0]

            # AI quizzes
            async with conn.execute(
                "SELECT COUNT(*) FROM quiz_results WHERE user_id = ? AND test_type = 'ai';", (user_id,)
            ) as cur:
                ai_quizzes = (await cur.fetchone())[0]

            # Premade quizzes
            async with conn.execute(
                "SELECT COUNT(*) FROM quiz_results WHERE user_id = ? AND test_type = 'premade';", (user_id,)
            ) as cur:
                premade_quizzes = (await cur.fetchone())[0]

            # Average score
            async with conn.execute(
                "SELECT AVG(percentage) FROM quiz_results WHERE user_id = ?;", (user_id,)
            ) as cur:
                row = await cur.fetchone()
                avg_score = round(row[0], 1) if row and row[0] is not None else 0.0

            # Best score in premade
            async with conn.execute(
                "SELECT MAX(score) FROM quiz_results WHERE user_id = ? AND test_type = 'premade';", (user_id,)
            ) as cur:
                row = await cur.fetchone()
                best_score = row[0] if row and row[0] is not None else 0

            return {
                "total_quizzes": total_quizzes,
                "ai_quizzes": ai_quizzes,
                "premade_quizzes": premade_quizzes,
                "avg_score": avg_score,
                "best_score": best_score,
            }

    async def get_top_leaderboard(self, limit: int = 10) -> list[dict]:
        """Returns TOP-10 leaderboard for premade quizzes.
        
        Rule: Takes the best result per user (highest score, tie-breaker: lowest time_spent_seconds).
        """
        async with self.get_connection() as conn:
            query = """
                WITH RankedResults AS (
                    SELECT 
                        r.user_id,
                        u.full_name,
                        u.username,
                        r.score,
                        r.total_questions,
                        r.percentage,
                        r.time_spent_seconds,
                        r.completed_at,
                        ROW_NUMBER() OVER (
                            PARTITION BY r.user_id 
                            ORDER BY r.score DESC, r.time_spent_seconds ASC, r.completed_at ASC
                        ) as rank
                    FROM quiz_results r
                    JOIN users u ON r.user_id = u.user_id
                    WHERE r.test_type = 'premade'
                )
                SELECT user_id, full_name, username, score, total_questions, percentage, time_spent_seconds, completed_at
                FROM RankedResults
                WHERE rank = 1
                ORDER BY score DESC, time_spent_seconds ASC
                LIMIT ?;
            """
            async with conn.execute(query, (limit,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def get_premade_questions(self, category: str, lang: str, limit: int = 10) -> list[QuizQuestionModel]:
        """Fetches up to `limit` premade questions for a given category and language."""
        async with self.get_connection() as conn:
            query = """
                SELECT question, options_json, correct_index, explanation 
                FROM premade_questions 
                WHERE category = ? AND lang = ? 
                ORDER BY id ASC 
                LIMIT ?;
            """
            async with conn.execute(query, (category, lang, limit)) as cursor:
                rows = await cursor.fetchall()
                questions = []
                for row in rows:
                    options = json.loads(row["options_json"])
                    questions.append(
                        QuizQuestionModel(
                            question=row["question"],
                            options=options,
                            correct_index=row["correct_index"],
                            explanation=row["explanation"],
                        )
                    )
                return questions

    async def add_premade_question(
        self,
        category: str,
        lang: str,
        question: str,
        options: list[str],
        correct_index: int,
        explanation: str,
        created_by: int = 0,
    ) -> int:
        """Inserts an admin-created question into premade_questions table."""
        async with self.get_connection() as conn:
            cursor = await conn.execute(
                """
                INSERT INTO premade_questions (category, lang, question, options_json, correct_index, explanation, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?);
                """,
                (category, lang, question, json.dumps(options, ensure_ascii=False), correct_index, explanation, created_by),
            )
            await conn.commit()
            return cursor.lastrowid or 0

    async def get_admin_stats(self) -> dict:
        """Fetches system-wide statistics for the admin dashboard."""
        async with self.get_connection() as conn:
            async with conn.execute("SELECT COUNT(*) FROM users;") as cur:
                users_count = (await cur.fetchone())[0]

            async with conn.execute("SELECT COUNT(*) FROM quiz_results;") as cur:
                quizzes_count = (await cur.fetchone())[0]

            async with conn.execute("SELECT COUNT(*) FROM quiz_results WHERE test_type = 'ai';") as cur:
                ai_count = (await cur.fetchone())[0]

            async with conn.execute("SELECT COUNT(*) FROM premade_questions;") as cur:
                premade_count = (await cur.fetchone())[0]

            return {
                "users_count": users_count,
                "quizzes_count": quizzes_count,
                "ai_count": ai_count,
                "premade_count": premade_count,
            }


# Global database instance
db = Database()
