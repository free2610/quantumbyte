import logging
from datetime import datetime, timezone
from aiogram import Router, F
from aiogram.types import Message

from app.config import settings
from app.core.database import db
from app.core.i18n import t, format_seconds
from app.core.security import escape_html

logger = logging.getLogger(__name__)

router = Router(name="results")


@router.message(F.text.in_([t("btn_my_results", "uz"), t("btn_my_results", "ru"), "📊 Mening natijalarim", "📊 Мои результаты"]))
async def show_my_results(message: Message) -> None:
    """Displays individual performance statistics for the user."""
    user = message.from_user
    if not user:
        return

    lang = await db.get_user_language(user.id)
    stats = await db.get_user_stats(user.id)

    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ai_used = await db.get_ai_daily_usage(user.id, today_str)

    text = t(
        "my_results_title",
        lang,
        name=escape_html(user.full_name or "Foydalanuvchi"),
        total_quizzes=stats["total_quizzes"],
        ai_quizzes=stats["ai_quizzes"],
        premade_quizzes=stats["premade_quizzes"],
        avg_score=stats["avg_score"],
        best_score=stats["best_score"],
        ai_used=ai_used,
        ai_limit=settings.AI_DAILY_LIMIT,
    )

    await message.answer(text, parse_mode="HTML")


@router.message(F.text.in_([t("btn_leaderboard", "uz"), t("btn_leaderboard", "ru"), "🏆 TOP-10", "🏆 ТОП-10"]))
async def show_leaderboard(message: Message) -> None:
    """Displays TOP-10 leaderboard strictly based on premade quizzes."""
    user = message.from_user
    lang = await db.get_user_language(user.id) if user else "uz"

    leaderboard = await db.get_top_leaderboard(limit=10)

    if not leaderboard:
        await message.answer(
            t("leaderboard_title", lang) + t("leaderboard_empty", lang),
            parse_mode="HTML",
        )
        return

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    lines = []

    for i, entry in enumerate(leaderboard):
        medal = medals[i] if i < len(medals) else f"<b>{i+1}.</b>"
        user_name = escape_html(entry.get("full_name") or "Anonim")
        score = entry.get("score", 0)
        total = entry.get("total_questions", 10)
        percent = entry.get("percentage", 0.0)
        time_sec = entry.get("time_spent_seconds", 0)
        time_str = format_seconds(time_sec, lang)

        line = f"{medal} <b>{user_name}</b> — <b>{score}/{total}</b> ({percent}%) | ⏱ {time_str}"
        lines.append(line)

    full_text = t("leaderboard_title", lang) + "\n".join(lines)
    await message.answer(full_text, parse_mode="HTML")
