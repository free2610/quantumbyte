import time
import logging
from app.core.models import ActiveQuizSession, QuizQuestionModel, UserAnswer
from app.core.database import db

logger = logging.getLogger(__name__)


class QuizManagerError(Exception):
    """Base exception for quiz manager."""
    pass


class InvalidSessionError(QuizManagerError):
    """Raised when callback references an invalid or expired quiz session."""
    pass


class AlreadyAnsweredError(QuizManagerError):
    """Raised when user attempts to answer the same question multiple times."""
    pass


class QuizManager:
    """Manages active quiz sessions for users in memory."""

    def __init__(self):
        self._sessions: dict[int, ActiveQuizSession] = {}

    def get_session(self, user_id: int) -> ActiveQuizSession | None:
        """Retrieves active session for user if present."""
        return self._sessions.get(user_id)

    def has_active_session(self, user_id: int) -> bool:
        """Checks if user currently has an unfinished quiz session."""
        session = self._sessions.get(user_id)
        return session is not None and not session.is_completed

    def start_session(
        self,
        user_id: int,
        test_type: str,
        topic: str,
        difficulty: str,
        questions: list[QuizQuestionModel],
    ) -> ActiveQuizSession:
        """Initializes and registers a new active quiz session."""
        session = ActiveQuizSession(
            user_id=user_id,
            test_type=test_type,
            topic=topic,
            difficulty=difficulty,
            questions=questions,
            current_index=0,
            answers=[],
            start_time=time.time(),
            answered_current=False,
        )
        self._sessions[user_id] = session
        return session

    def cancel_session(self, user_id: int) -> bool:
        """Cancels and deletes an active session for the given user."""
        if user_id in self._sessions:
            del self._sessions[user_id]
            return True
        return False

    def answer_question(
        self,
        user_id: int,
        session_id: str,
        question_index: int,
        selected_index: int,
    ) -> tuple[bool, str, QuizQuestionModel]:
        """Processes user's answer for the current question."""
        session = self._sessions.get(user_id)
        if not session or session.session_id != session_id:
            raise InvalidSessionError("Ushbu test sessiyasi eskirgan yoki mavjud emas.")

        if session.current_index != question_index:
            raise InvalidSessionError("Savol tartibi mos kelmadi.")

        if session.answered_current:
            raise AlreadyAnsweredError("Bu savolga allaqachon javob bergansiz.")

        current_question = session.questions[session.current_index]
        is_correct = selected_index == current_question.correct_index

        session.answered_current = True
        session.answers.append(
            UserAnswer(
                question_index=question_index,
                selected_index=selected_index,
                is_correct=is_correct,
            )
        )

        return is_correct, current_question.explanation, current_question

    def next_question(
        self,
        user_id: int,
        session_id: str,
    ) -> tuple[QuizQuestionModel | None, bool]:
        """Advances session to the next question.
        
        Returns: (next_question or None, is_finished)
        """
        session = self._sessions.get(user_id)
        if not session or session.session_id != session_id:
            raise InvalidSessionError("Ushbu test sessiyasi eskirgan yoki mavjud emas.")

        session.current_index += 1
        session.answered_current = False

        if session.is_completed:
            session.end_time = time.time()
            return None, True

        return session.questions[session.current_index], False

    async def finish_and_save(self, user_id: int) -> tuple[ActiveQuizSession, int]:
        """Saves session results to SQLite database and removes from active sessions."""
        session = self._sessions.get(user_id)
        if not session:
            raise InvalidSessionError("Saqlash uchun faol sessiya topilmadi.")

        if session.end_time is None:
            session.end_time = time.time()

        answers_data = [
            {
                "question_index": a.question_index,
                "selected_index": a.selected_index,
                "is_correct": a.is_correct,
                "question": session.questions[a.question_index].question,
                "options": session.questions[a.question_index].options,
                "correct_index": session.questions[a.question_index].correct_index,
                "explanation": session.questions[a.question_index].explanation,
            }
            for a in session.answers
        ]

        result_id = await db.save_quiz_result(
            user_id=session.user_id,
            test_type=session.test_type,
            topic=session.topic,
            score=session.correct_count,
            total_questions=session.total_questions,
            percentage=session.percentage,
            time_spent_seconds=session.time_spent_seconds,
            answers=answers_data,
        )

        # Clear active session
        del self._sessions[user_id]
        return session, result_id

    def get_mistakes(self, session: ActiveQuizSession) -> list[dict]:
        """Extracts list of mistakes made during the session."""
        mistakes = []
        for a in session.answers:
            if not a.is_correct:
                q = session.questions[a.question_index]
                user_opt = q.options[a.selected_index] if 0 <= a.selected_index < len(q.options) else "?"
                corr_opt = q.options[q.correct_index] if 0 <= q.correct_index < len(q.options) else "?"
                mistakes.append({
                    "num": a.question_index + 1,
                    "question": q.question,
                    "user_ans": user_opt,
                    "correct_ans": corr_opt,
                    "explanation": q.explanation,
                })
        return mistakes


# Global quiz manager instance
quiz_manager = QuizManager()
