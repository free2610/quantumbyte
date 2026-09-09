from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.core.i18n import t


def get_main_menu_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Constructs the main persistent reply keyboard with localized buttons."""
    keyboard = [
        [
            KeyboardButton(text=t("btn_ai_quiz", lang)),
            KeyboardButton(text=t("btn_premade_quiz", lang)),
        ],
        [
            KeyboardButton(text=t("btn_my_results", lang)),
            KeyboardButton(text=t("btn_leaderboard", lang)),
        ],
        [
            KeyboardButton(text=t("btn_change_lang", lang)),
            KeyboardButton(text=t("btn_help", lang)),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
