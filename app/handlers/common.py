import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.core.database import db
from app.core.i18n import t
from app.core.security import escape_html
from app.keyboards.reply import get_main_menu_keyboard
from app.keyboards.inline import get_language_keyboard
from app.services.quiz_manager import quiz_manager

logger = logging.getLogger(__name__)

router = Router(name="common")


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """Handles /start command.
    
    If user is new, prompts for language choice.
    If returning user, shows main menu.
    """
    await state.clear()
    user = message.from_user
    if not user:
        return

    # Check if user already exists
    existing_lang = await db.get_user_language(user.id)
    # Check in DB if user is saved
    user_record = await db.get_or_create_user(
        user_id=user.id,
        username=user.username,
        full_name=user.full_name or "Foydalanuvchi",
        default_lang="uz",
    )

    # If first time, offer language choice
    if not user_record.get("language") or message.text and "/start lang" in message.text:
        await message.answer(
            t("welcome_new", "uz"),
            reply_markup=get_language_keyboard(),
            parse_mode="HTML",
        )
        return

    lang = user_record.get("language", "uz")
    await message.answer(
        t("welcome_back", lang, name=escape_html(user.first_name or "Do'st")),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML",
    )


@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_language(callback: CallbackQuery, state: FSMContext) -> None:
    """Updates user's preferred language."""
    await state.clear()
    user = callback.from_user
    data = callback.data or ""
    new_lang = data.split(":")[1] if ":" in data else "uz"

    await db.set_user_language(user.id, new_lang)
    await callback.answer(t("lang_changed", new_lang))

    await callback.message.delete() if callback.message else None

    # Send welcome / main menu
    await callback.message.answer(
        t("welcome_back", new_lang, name=escape_html(user.first_name or "Do'st")),
        reply_markup=get_main_menu_keyboard(new_lang),
        parse_mode="HTML",
    )


@router.message(Command("cancel"))
@router.message(F.text.in_(["/cancel", "❌ Bekor qilish", "❌ Отмена"]))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """Cancels any ongoing FSM state or active quiz session."""
    user = message.from_user
    if not user:
        return

    lang = await db.get_user_language(user.id)
    current_state = await state.get_state()
    had_active_quiz = quiz_manager.has_active_session(user.id)

    await state.clear()
    if had_active_quiz:
        quiz_manager.cancel_session(user.id)

    await message.answer(
        t("cancel_done", lang),
        reply_markup=get_main_menu_keyboard(lang),
    )


@router.callback_query(F.data == "cancel_action")
async def cb_cancel_action(callback: CallbackQuery, state: FSMContext) -> None:
    """Cancels inline prompt and returns to main menu."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)

    await state.clear()
    quiz_manager.cancel_session(user.id)

    await callback.answer(t("cancel_done", lang))
    if callback.message:
        await callback.message.delete()
        await callback.message.answer(
            t("main_menu_title", lang),
            reply_markup=get_main_menu_keyboard(lang),
        )


@router.callback_query(F.data == "go_home")
async def cb_go_home(callback: CallbackQuery, state: FSMContext) -> None:
    """Navigates back to main menu."""
    user = callback.from_user
    lang = await db.get_user_language(user.id)
    await state.clear()

    await callback.answer()
    if callback.message:
        await callback.message.answer(
            t("main_menu_title", lang),
            reply_markup=get_main_menu_keyboard(lang),
        )


@router.message(F.text.in_([t("btn_change_lang", "uz"), t("btn_change_lang", "ru"), "🌐 Tilni o'zgartirish", "🌐 Сменить язык"]))
async def menu_change_language(message: Message) -> None:
    """Offers language selection keyboard."""
    user = message.from_user
    lang = await db.get_user_language(user.id) if user else "uz"
    await message.answer(
        t("select_lang_prompt", lang),
        reply_markup=get_language_keyboard(),
    )


@router.message(Command("help"))
@router.message(F.text.in_([t("btn_help", "uz"), t("btn_help", "ru"), "ℹ️ Yordam", "ℹ️ Помощь"]))
async def menu_help(message: Message) -> None:
    """Displays help text and usage guidelines."""
    user = message.from_user
    lang = await db.get_user_language(user.id) if user else "uz"
    await message.answer(
        t("help_text", lang),
        reply_markup=get_main_menu_keyboard(lang),
        parse_mode="HTML",
    )
