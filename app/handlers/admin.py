import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from app.core.database import db
from app.core.i18n import t
from app.core.security import is_admin, escape_html
from app.core.models import QuizQuestionModel
from app.states.quiz_states import AdminAddQuestionStates
from app.keyboards.inline import get_admin_keyboard, get_admin_confirm_keyboard

logger = logging.getLogger(__name__)

router = Router(name="admin")


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    """Entry point for /admin command. Checks admin privileges."""
    user = message.from_user
    if not user:
        return

    lang = await db.get_user_language(user.id)

    # Check admin privileges explicitly
    if not is_admin(user.id):
        await message.answer(t("admin_access_denied", lang))
        return

    await state.clear()
    stats = await db.get_admin_stats()
    text = t(
        "admin_panel_title",
        lang,
        users_count=stats["users_count"],
        quizzes_count=stats["quizzes_count"],
        ai_count=stats["ai_count"],
        premade_count=stats["premade_count"],
    )

    await message.answer(text, reply_markup=get_admin_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data == "admin:refresh")
async def cb_admin_refresh(callback: CallbackQuery, state: FSMContext) -> None:
    """Refreshes admin panel statistics."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    lang = await db.get_user_language(user.id)
    stats = await db.get_admin_stats()
    text = t(
        "admin_panel_title",
        lang,
        users_count=stats["users_count"],
        quizzes_count=stats["quizzes_count"],
        ai_count=stats["ai_count"],
        premade_count=stats["premade_count"],
    )

    await callback.answer("Yangilandi!")
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(lang), parse_mode="HTML")


# ------------------- ADMIN ADD QUESTION FSM -------------------

@router.callback_query(F.data == "admin:add_q")
async def cb_admin_add_question_start(callback: CallbackQuery, state: FSMContext) -> None:
    """Starts the step-by-step FSM wizard to add a new pre-made question."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    lang = await db.get_user_language(user.id)
    await state.set_state(AdminAddQuestionStates.choose_lang)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="adm_lang:uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="adm_lang:ru"),
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel_save"),
            ],
        ]
    )

    await callback.message.edit_text(
        "<b>1-bosqich:</b> Savol qaysi tilda tuzilayotganini tanlang:",
        reply_markup=kb,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(AdminAddQuestionStates.choose_lang, F.data.startswith("adm_lang:"))
async def cb_admin_lang_selected(callback: CallbackQuery, state: FSMContext) -> None:
    """Stores language and prompts for subject category."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    target_lang = callback.data.split(":")[1]
    await state.update_data(target_lang=target_lang)
    await state.set_state(AdminAddQuestionStates.choose_category)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧲 Fizika", callback_data="adm_cat:physics"),
            ],
            [
                InlineKeyboardButton(text="🇬🇧 Ingliz tili", callback_data="adm_cat:english"),
            ],
            [
                InlineKeyboardButton(text="💻 IT va Dasturlash", callback_data="adm_cat:it"),
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="admin:cancel_save"),
            ],
        ]
    )

    await callback.message.edit_text(
        "<b>2-bosqich:</b> Fanni (kategoriyani) tanlang:",
        reply_markup=kb,
        parse_mode="HTML",
    )
    await callback.answer()


@router.callback_query(AdminAddQuestionStates.choose_category, F.data.startswith("adm_cat:"))
async def cb_admin_cat_selected(callback: CallbackQuery, state: FSMContext) -> None:
    """Stores category and prompts for question text."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    category = callback.data.split(":")[1]
    await state.update_data(category=category)
    await state.set_state(AdminAddQuestionStates.enter_question)

    await callback.message.edit_text(
        "<b>3-bosqich:</b> Savol matnini kiriting:\n\n<i>(Bekor qilish uchun /cancel)</i>",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AdminAddQuestionStates.enter_question, F.text)
async def process_admin_question_text(message: Message, state: FSMContext) -> None:
    """Stores question text and prompts for Option A."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    q_text = message.text.strip()
    if len(q_text) < 5 or len(q_text) > 1000:
        await message.answer("⚠️ Savol matni 5 dan 1000 belgiga bo'lishi kerak. Qaytadan kiriting:")
        return

    await state.update_data(question_text=q_text)
    await state.set_state(AdminAddQuestionStates.enter_option_1)
    await message.answer("<b>4-bosqich (1/4):</b> <b>A</b> varianti matnini kiriting:", parse_mode="HTML")


@router.message(AdminAddQuestionStates.enter_option_1, F.text)
async def process_admin_opt_1(message: Message, state: FSMContext) -> None:
    """Stores Option A and prompts for Option B."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    opt = message.text.strip()
    if not opt or len(opt) > 120:
        await message.answer("⚠️ Variant matni 120 belgidan oshmasligi kerak. Qaytadan kiriting:")
        return

    await state.update_data(opt_1=opt)
    await state.set_state(AdminAddQuestionStates.enter_option_2)
    await message.answer("<b>4-bosqich (2/4):</b> <b>B</b> varianti matnini kiriting:", parse_mode="HTML")


@router.message(AdminAddQuestionStates.enter_option_2, F.text)
async def process_admin_opt_2(message: Message, state: FSMContext) -> None:
    """Stores Option B and prompts for Option C."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    opt = message.text.strip()
    if not opt or len(opt) > 120:
        await message.answer("⚠️ Variant matni 120 belgidan oshmasligi kerak. Qaytadan kiriting:")
        return

    await state.update_data(opt_2=opt)
    await state.set_state(AdminAddQuestionStates.enter_option_3)
    await message.answer("<b>4-bosqich (3/4):</b> <b>C</b> varianti matnini kiriting:", parse_mode="HTML")


@router.message(AdminAddQuestionStates.enter_option_3, F.text)
async def process_admin_opt_3(message: Message, state: FSMContext) -> None:
    """Stores Option C and prompts for Option D."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    opt = message.text.strip()
    if not opt or len(opt) > 120:
        await message.answer("⚠️ Variant matni 120 belgidan oshmasligi kerak. Qaytadan kiriting:")
        return

    await state.update_data(opt_3=opt)
    await state.set_state(AdminAddQuestionStates.enter_option_4)
    await message.answer("<b>4-bosqich (4/4):</b> <b>D</b> varianti matnini kiriting:", parse_mode="HTML")


@router.message(AdminAddQuestionStates.enter_option_4, F.text)
async def process_admin_opt_4(message: Message, state: FSMContext) -> None:
    """Stores Option D and prompts for the correct answer index."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    opt = message.text.strip()
    if not opt or len(opt) > 120:
        await message.answer("⚠️ Variant matni 120 belgidan oshmasligi kerak. Qaytadan kiriting:")
        return

    await state.update_data(opt_4=opt)
    await state.set_state(AdminAddQuestionStates.enter_correct_index)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A", callback_data="adm_corr:0"),
                InlineKeyboardButton(text="B", callback_data="adm_corr:1"),
                InlineKeyboardButton(text="C", callback_data="adm_corr:2"),
                InlineKeyboardButton(text="D", callback_data="adm_corr:3"),
            ]
        ]
    )

    await message.answer(
        "<b>5-bosqich:</b> To'g'ri javob variantini tanlang (A, B, C yoki D):",
        reply_markup=kb,
        parse_mode="HTML",
    )


@router.callback_query(AdminAddQuestionStates.enter_correct_index, F.data.startswith("adm_corr:"))
async def cb_admin_correct_selected(callback: CallbackQuery, state: FSMContext) -> None:
    """Stores correct index and prompts for explanation."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    corr_idx = int(callback.data.split(":")[1])
    await state.update_data(correct_index=corr_idx)
    await state.set_state(AdminAddQuestionStates.enter_explanation)

    await callback.message.edit_text(
        "<b>6-bosqich:</b> Savol uchun qisqa tushuntirish (izoh) matnini kiriting:",
        parse_mode="HTML",
    )
    await callback.answer()


@router.message(AdminAddQuestionStates.enter_explanation, F.text)
async def process_admin_explanation(message: Message, state: FSMContext) -> None:
    """Validates full question model and presents a preview for final confirmation."""
    user = message.from_user
    if not user or not is_admin(user.id):
        return

    explanation = message.text.strip()
    if len(explanation) < 3 or len(explanation) > 1000:
        await message.answer("⚠️ Izoh 3 dan 1000 belgiga bo'lishi kerak. Qaytadan kiriting:")
        return

    data = await state.get_data()
    q_text = data["question_text"]
    options = [data["opt_1"], data["opt_2"], data["opt_3"], data["opt_4"]]
    corr_idx = data["correct_index"]
    target_lang = data["target_lang"]
    category = data["category"]

    # Validate through Pydantic
    try:
        model = QuizQuestionModel(
            question=q_text,
            options=options,
            correct_index=corr_idx,
            explanation=explanation,
        )
    except Exception as e:
        await message.answer(f"⚠️ Validatsiya xatoligi: {str(e)}\nIltimos, /cancel qilib qaytadan urinib ko'ring.")
        return

    await state.update_data(explanation=explanation)
    await state.set_state(AdminAddQuestionStates.confirm_save)

    letters = ["A", "B", "C", "D"]
    opts_display = "\n".join(
        f"{'✅ ' if i == corr_idx else '⚪️ '}<b>{letters[i]})</b> {escape_html(opt)}"
        for i, opt in enumerate(options)
    )

    preview_text = (
        "🔍 <b>Yangi savol tekshiruvi (Prevyu):</b>\n\n"
        f"🌐 <b>Til:</b> {target_lang.upper()}\n"
        f"📚 <b>Fan:</b> {category.title()}\n\n"
        f"❓ <b>Savol:</b> {escape_html(q_text)}\n\n"
        f"📋 <b>Variantlar:</b>\n{opts_display}\n\n"
        f"💡 <b>Izoh:</b> {escape_html(explanation)}\n\n"
        "Savolni bazaga saqlaysizmi?"
    )

    lang = await db.get_user_language(user.id)
    await message.answer(
        preview_text,
        reply_markup=get_admin_confirm_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(AdminAddQuestionStates.confirm_save, F.data == "admin:confirm_save")
async def cb_admin_save_confirmed(callback: CallbackQuery, state: FSMContext) -> None:
    """Persists validated question into SQLite database."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    data = await state.get_data()
    category = data["category"]
    target_lang = data["target_lang"]
    q_text = data["question_text"]
    options = [data["opt_1"], data["opt_2"], data["opt_3"], data["opt_4"]]
    corr_idx = data["correct_index"]
    explanation = data["explanation"]

    await db.add_premade_question(
        category=category,
        lang=target_lang,
        question=q_text,
        options=options,
        correct_index=corr_idx,
        explanation=explanation,
        created_by=user.id,
    )

    await state.clear()
    await callback.answer("✅ Savol muvaffaqiyatli saqlandi!", show_alert=True)

    lang = await db.get_user_language(user.id)
    stats = await db.get_admin_stats()
    text = (
        "✅ <b>Savol bazaga qo'shildi!</b>\n\n"
        + t(
            "admin_panel_title",
            lang,
            users_count=stats["users_count"],
            quizzes_count=stats["quizzes_count"],
            ai_count=stats["ai_count"],
            premade_count=stats["premade_count"],
        )
    )
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(lang), parse_mode="HTML")


@router.callback_query(F.data == "admin:cancel_save")
async def cb_admin_cancel_save(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancels question creation wizard and returns to admin dashboard."""
    user = callback.from_user
    if not is_admin(user.id):
        await callback.answer("Ruxsat yo'q!", show_alert=True)
        return

    await state.clear()
    await callback.answer("Bekor qilindi.")

    lang = await db.get_user_language(user.id)
    stats = await db.get_admin_stats()
    text = t(
        "admin_panel_title",
        lang,
        users_count=stats["users_count"],
        quizzes_count=stats["quizzes_count"],
        ai_count=stats["ai_count"],
        premade_count=stats["premade_count"],
    )
    await callback.message.edit_text(text, reply_markup=get_admin_keyboard(lang), parse_mode="HTML")
