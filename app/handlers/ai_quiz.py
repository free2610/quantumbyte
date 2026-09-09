import logging
import json
from datetime import datetime, timezone
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.config import settings
from app.core.database import db
from app.core.i18n import t, format_seconds
from app.core.security import escape_html, sanitize_topic, sanitize_custom_text
from app.core.models import ActiveQuizSession
from app.states.quiz_states import AIQuizStates
from app.keyboards.inline import (
    get_ai_mode_keyboard,
    get_difficulty_keyboard,
    get_question_count_keyboard,
    get_quiz_question_keyboard,
    get_next_question_keyboard,
    get_quiz_finish_keyboard,
)
from app.keyboards.reply import get_main_menu_keyboard
from app.services.gemini import (
    gemini_service,
    GeminiNotConfiguredError,
    GeminiQuotaExceededError,
    GeminiConcurrencyError,
    GeminiServiceError,
)
from app.services.quiz_manager import (
    quiz_manager,
    InvalidSessionError,
    AlreadyAnsweredError,
)

logger = logging.getLogger(__name__)

router = Router(name="ai_quiz")


async def render_question_message(
    session: ActiveQuizSession,
    lang: str,
) -> tuple[str, any]:
    """Prepares formatted HTML text and inline keyboard for the current question."""
    q_index = session.current_index
    q = session.questions[q_index]
    letters = ["A", "B", "C", "D"]

    header = t(
        "question_progress",
        lang,
        current=q_index + 1,
        total=session.total_questions,
        topic=escape_html(session.topic),
    )

    options_formatted = "\n".join(
        f"<b>{letters[i]})</b> {escape_html(opt)}" for i, opt in enumerate(q.options)
    )

    text = f"{header}\n\n<b>{escape_html(q.question)}</b>\n\n{options_formatted}"
    keyboard = get_quiz_question_keyboard(session.session_id, q_index, q.options)
    return text, keyboard


@router.message(F.text.in_([t("btn_ai_quiz", "uz"), t("btn_ai_quiz", "ru"), "🧠 AI test yaratish", "🧠 Создать тест с ИИ"]))
async def start_ai_quiz_flow(message: Message, state: FSMContext) -> None:
    """Initiates AI quiz generation wizard."""
    user = message.from_user
    if not user:
        return

    lang = await db.get_user_language(user.id)

    # 1. Check if user already has an active quiz
    if quiz_manager.has_active_session(user.id):
        await message.answer(t("active_quiz_exists", lang))
        return

    # 2. Check if Gemini API is configured
    if not settings.has_gemini:
        await message.answer(t("ai_unavailable", lang), parse_mode="HTML")
        return

    # 3. Check daily AI limit
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    used_today = await db.get_ai_daily_usage(user.id, today_str)
    if used_today >= settings.AI_DAILY_LIMIT:
        await message.answer(
            t("ai_limit_reached", lang, limit=settings.AI_DAILY_LIMIT),
            parse_mode="HTML",
        )
        return

    # Start FSM: choose mode
    await state.set_state(AIQuizStates.choose_mode)
    await message.answer(
        t("ai_mode_select", lang),
        reply_markup=get_ai_mode_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(AIQuizStates.choose_mode, F.data.startswith("ai_mode:"))
async def cb_choose_mode(callback: CallbackQuery, state: FSMContext) -> None:
    """Handles selection between topic-based and text-based quiz."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    mode = callback.data.split(":")[1]

    if mode == "topic":
        await state.set_state(AIQuizStates.waiting_topic)
        await callback.message.edit_text(
            t("prompt_enter_topic", lang),
            parse_mode="HTML",
        )
    else:
        await state.set_state(AIQuizStates.waiting_text)
        await callback.message.edit_text(
            t("prompt_enter_text", lang),
            parse_mode="HTML",
        )
    await callback.answer()


@router.message(AIQuizStates.waiting_topic, F.text)
async def process_topic_input(message: Message, state: FSMContext) -> None:
    """Validates and stores user topic, then prompts for difficulty."""
    user = message.from_user
    lang = await db.get_user_language(user.id) if user else "uz"
    raw_topic = message.text.strip()

    if len(raw_topic) > 200:
        await message.answer(t("topic_too_long", lang))
        return

    cleaned_topic = sanitize_topic(raw_topic)
    await state.update_data(prompt_type="topic", user_input=cleaned_topic)
    await state.set_state(AIQuizStates.waiting_difficulty)

    await message.answer(
        t("select_difficulty", lang),
        reply_markup=get_difficulty_keyboard(lang),
    )


@router.message(AIQuizStates.waiting_text, F.text)
async def process_text_input(message: Message, state: FSMContext) -> None:
    """Validates and stores user custom text, then prompts for difficulty."""
    user = message.from_user
    lang = await db.get_user_language(user.id) if user else "uz"
    raw_text = message.text.strip()

    if len(raw_text) > 3000:
        await message.answer(t("text_too_long", lang, length=len(raw_text)))
        return

    if len(raw_text) < 50:
        msg = (
            "⚠️ Matn juda qisqa. Test tuzish uchun kamida 50 ta belgi yuboring:"
            if lang == "uz"
            else "⚠️ Текст слишком короткий. Для составления теста отправьте минимум 50 символов:"
        )
        await message.answer(msg)
        return

    cleaned_text = sanitize_custom_text(raw_text)
    # Generate short topic summary for display
    display_topic = raw_text[:40] + "..." if len(raw_text) > 40 else raw_text
    await state.update_data(
        prompt_type="text",
        user_input=cleaned_text,
        display_topic=display_topic,
    )
    await state.set_state(AIQuizStates.waiting_difficulty)

    await message.answer(
        t("select_difficulty", lang),
        reply_markup=get_difficulty_keyboard(lang),
    )


@router.callback_query(AIQuizStates.waiting_difficulty, F.data.startswith("diff:"))
async def cb_select_difficulty(callback: CallbackQuery, state: FSMContext) -> None:
    """Stores difficulty and asks for question count."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    diff_val = callback.data.split(":")[1]

    diff_map = {
        "easy": "oson" if lang == "uz" else "легкий",
        "medium": "o'rtacha" if lang == "uz" else "средний",
        "hard": "qiyin" if lang == "uz" else "сложный",
    }
    difficulty = diff_map.get(diff_val, "o'rtacha")
    await state.update_data(difficulty=difficulty)
    await state.set_state(AIQuizStates.waiting_count)

    await callback.message.edit_text(
        t("select_count", lang),
        reply_markup=get_question_count_keyboard(lang),
    )
    await callback.answer()


@router.callback_query(AIQuizStates.waiting_count, F.data.startswith("count:"))
async def cb_select_count(callback: CallbackQuery, state: FSMContext) -> None:
    """Generates quiz via Gemini AI and starts the quiz session."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    count = int(callback.data.split(":")[1])

    data = await state.get_data()
    prompt_type = data.get("prompt_type", "topic")
    user_input = data.get("user_input", "")
    difficulty = data.get("difficulty", "o'rtacha")
    display_topic = data.get("display_topic") or user_input

    # Clear state now that inputs are gathered
    await state.clear()

    # Show loading message
    loading_msg = await callback.message.edit_text(
        t("ai_generating", lang),
        parse_mode="HTML",
    )
    await callback.answer()

    try:
        questions = await gemini_service.generate_quiz(
            user_id=user.id,
            prompt_type=prompt_type,
            user_input=user_input,
            difficulty=difficulty,
            count=count,
            lang=lang,
        )

        # Register usage count
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        await db.increment_ai_daily_usage(user.id, today_str)

        # Start session
        session = quiz_manager.start_session(
            user_id=user.id,
            test_type="ai",
            topic=display_topic,
            difficulty=difficulty,
            questions=questions,
        )

        # Render and send first question
        text, keyboard = await render_question_message(session, lang)
        await loading_msg.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

    except GeminiQuotaExceededError:
        await loading_msg.edit_text(
            t("ai_limit_reached", lang, limit=settings.AI_DAILY_LIMIT),
            parse_mode="HTML",
        )
    except GeminiConcurrencyError:
        await loading_msg.edit_text(
            t("ai_concurrent_request", lang),
            parse_mode="HTML",
        )
    except (GeminiServiceError, Exception) as e:
        logger.error("AI quiz yaratishda kutilmagan xato: %s", str(e), exc_info=True)
        await loading_msg.edit_text(
            t("ai_generation_failed", lang),
            parse_mode="HTML",
        )


@router.callback_query(F.data.startswith("ans:"))
async def cb_answer_question(callback: CallbackQuery) -> None:
    """Processes option selection for the current question."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    parts = callback.data.split(":")
    if len(parts) != 4:
        await callback.answer()
        return

    _, session_id, q_idx_str, opt_idx_str = parts
    q_index = int(q_idx_str)
    selected_index = int(opt_idx_str)

    # Check session
    session = quiz_manager.get_session(user.id)
    if not session or session.session_id != session_id:
        await callback.answer(
            "⚠️ Ushbu test sessiyasi eskirgan yoki boshqa foydalanuvchiga tegishli."
            if lang == "uz"
            else "⚠️ Эта сессия теста устарела или принадлежит другому пользователю.",
            show_alert=True,
        )
        return

    try:
        is_correct, explanation, q = quiz_manager.answer_question(
            user_id=user.id,
            session_id=session_id,
            question_index=q_index,
            selected_index=selected_index,
        )
    except AlreadyAnsweredError:
        await callback.answer(t("already_answered", lang), show_alert=True)
        return
    except InvalidSessionError:
        await callback.answer(
            "⚠️ Sessiya eskirgan." if lang == "uz" else "⚠️ Сессия устарела.",
            show_alert=True,
        )
        return

    await callback.answer("✅ To'g'ri!" if is_correct else "❌ Noto'g'ri!")

    letters = ["A", "B", "C", "D"]
    corr_letter = letters[q.correct_index]
    corr_text = f"{corr_letter}) {q.options[q.correct_index]}"

    if is_correct:
        feedback = t("answer_correct", lang, explanation=escape_html(explanation))
    else:
        feedback = t(
            "answer_incorrect",
            lang,
            correct_opt=escape_html(corr_text),
            explanation=escape_html(explanation),
        )

    # Build updated text with question and result
    header = t(
        "question_progress",
        lang,
        current=q_index + 1,
        total=session.total_questions,
        topic=escape_html(session.topic),
    )
    options_formatted = "\n".join(
        f"{'👉 ' if i == selected_index else '   '}<b>{letters[i]})</b> {escape_html(opt)}"
        for i, opt in enumerate(q.options)
    )

    updated_text = (
        f"{header}\n\n"
        f"<b>{escape_html(q.question)}</b>\n\n"
        f"{options_formatted}\n\n"
        f"{feedback}"
    )

    is_last = q_index + 1 >= session.total_questions
    keyboard = get_next_question_keyboard(session_id, is_last=is_last, lang=lang)

    await callback.message.edit_text(updated_text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("next:"))
async def cb_next_question(callback: CallbackQuery) -> None:
    """Loads the next question or completes the quiz."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    session_id = callback.data.split(":")[1]

    session = quiz_manager.get_session(user.id)
    if not session or session.session_id != session_id:
        await callback.answer("⚠️ Sessiya eskirgan.", show_alert=True)
        return

    next_q, is_finished = quiz_manager.next_question(user.id, session_id)
    await callback.answer()

    if is_finished:
        # Finalize and persist
        finished_session, result_id = await quiz_manager.finish_and_save(user.id)
        time_str = format_seconds(finished_session.time_spent_seconds, lang)

        summary = t(
            "quiz_results_summary",
            lang,
            topic=escape_html(finished_session.topic),
            correct=finished_session.correct_count,
            incorrect=finished_session.incorrect_count,
            percent=finished_session.percentage,
            time_str=time_str,
        )

        has_mistakes = finished_session.incorrect_count > 0
        keyboard = get_quiz_finish_keyboard(
            session_id=str(result_id),
            has_mistakes=has_mistakes,
            lang=lang,
        )

        await callback.message.edit_text(summary, reply_markup=keyboard, parse_mode="HTML")
    else:
        text, keyboard = await render_question_message(session, lang)
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")


@router.callback_query(F.data.startswith("review:"))
async def cb_review_errors(callback: CallbackQuery) -> None:
    """Fetches and displays questions that the user answered incorrectly."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    result_id_str = callback.data.split(":")[1]

    if not result_id_str.isdigit():
        await callback.answer()
        return

    result_id = int(result_id_str)
    await callback.answer()

    # Fetch result from DB
    async with db.get_connection() as conn:
        async with conn.execute(
            "SELECT answers_json FROM quiz_results WHERE id = ? AND user_id = ?;",
            (result_id, user.id),
        ) as cur:
            row = await cur.fetchone()

    if not row:
        await callback.message.answer(t("no_errors_to_show", lang))
        return

    answers = json.loads(row["answers_json"])
    mistakes = [a for a in answers if not a.get("is_correct")]

    if not mistakes:
        await callback.message.answer(t("no_errors_to_show", lang))
        return

    letters = ["A", "B", "C", "D"]
    title = (
        "❌ <b>Siz yo'l qo'ygan xatolar va to'g'ri javoblar:</b>\n\n"
        if lang == "uz"
        else "❌ <b>Ваши ошибки и правильные ответы:</b>\n\n"
    )

    items = []
    for item in mistakes:
        q_text = escape_html(item.get("question", ""))
        options = item.get("options", [])
        sel_idx = item.get("selected_index", 0)
        corr_idx = item.get("correct_index", 0)
        expl = escape_html(item.get("explanation", ""))

        user_ans = escape_html(options[sel_idx]) if 0 <= sel_idx < len(options) else "?"
        corr_ans = escape_html(options[corr_idx]) if 0 <= corr_idx < len(options) else "?"

        item_str = t(
            "error_review_item",
            lang,
            num=item.get("question_index", 0) + 1,
            question=q_text,
            user_ans=user_ans,
            correct_ans=corr_ans,
            explanation=expl,
        )
        items.append(item_str)

    full_text = title + "\n-------------------\n".join(items)

    # Telegram limit guard: max 4000 chars per message
    if len(full_text) > 4000:
        chunks = [full_text[i:i + 3800] for i in range(0, len(full_text), 3800)]
        for chunk in chunks:
            await callback.message.answer(chunk, parse_mode="HTML")
    else:
        await callback.message.answer(full_text, parse_mode="HTML")


@router.callback_query(F.data == "new_quiz_prompt")
async def cb_new_quiz_prompt(callback: CallbackQuery) -> None:
    """Prompts user to start a new quiz."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    await callback.answer()
    await callback.message.answer(
        t("main_menu_title", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )
