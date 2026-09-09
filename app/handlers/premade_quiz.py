import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.core.database import db
from app.core.i18n import t
from app.keyboards.inline import get_premade_categories_keyboard
from app.handlers.ai_quiz import render_question_message
from app.services.quiz_manager import quiz_manager

logger = logging.getLogger(__name__)

router = Router(name="premade_quiz")


@router.message(F.text.in_([t("btn_premade_quiz", "uz"), t("btn_premade_quiz", "ru"), "📚 Tayyor testlar", "📚 Готовые тесты"]))
async def select_premade_quiz(message: Message) -> None:
    """Displays subject categories for pre-made tests."""
    user = message.from_user
    if not user:
        return

    lang = await db.get_user_language(user.id)

    # Check if user already has an active quiz
    if quiz_manager.has_active_session(user.id):
        await message.answer(t("active_quiz_exists", lang))
        return

    await message.answer(
        t("premade_select_category", lang),
        reply_markup=get_premade_categories_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("cat:"))
async def cb_start_premade_category(callback: CallbackQuery) -> None:
    """Fetches questions for the chosen subject and starts a pre-made quiz session."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    category = callback.data.split(":")[1]

    if quiz_manager.has_active_session(user.id):
        await callback.answer(t("active_quiz_exists", lang), show_alert=True)
        return

    questions = await db.get_premade_questions(category=category, lang=lang, limit=10)
    if not questions:
        # Fallback to 'uz' if 'ru' questions are somehow absent
        questions = await db.get_premade_questions(category=category, lang="uz", limit=10)

    if not questions:
        await callback.answer(t("premade_no_questions", lang), show_alert=True)
        return

    cat_titles = {
        "physics": "Fizika" if lang == "uz" else "Физика",
        "english": "Ingliz tili" if lang == "uz" else "Английский язык",
        "it": "IT va Dasturlash" if lang == "uz" else "IT и Программирование",
    }
    topic_title = cat_titles.get(category, category.title())

    # Start session
    session = quiz_manager.start_session(
        user_id=user.id,
        test_type="premade",
        topic=topic_title,
        difficulty="o'rtacha",
        questions=questions,
    )

    await callback.answer()
    text, keyboard = await render_question_message(session, lang)
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
