from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.core.i18n import t


def get_language_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard to select language."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
            ]
        ]
    )


def get_ai_mode_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to choose AI quiz generation mode (topic vs text)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_by_topic", lang), callback_data="ai_mode:topic"),
                InlineKeyboardButton(text=t("btn_by_text", lang), callback_data="ai_mode:text"),
            ],
            [
                InlineKeyboardButton(text="❌ " + ("Bekor qilish" if lang == "uz" else "Отмена"), callback_data="cancel_action"),
            ],
        ]
    )


def get_difficulty_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to select quiz difficulty level."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("diff_easy", lang), callback_data="diff:easy"),
                InlineKeyboardButton(text=t("diff_medium", lang), callback_data="diff:medium"),
                InlineKeyboardButton(text=t("diff_hard", lang), callback_data="diff:hard"),
            ],
            [
                InlineKeyboardButton(text="❌ " + ("Bekor qilish" if lang == "uz" else "Отмена"), callback_data="cancel_action"),
            ],
        ]
    )


def get_question_count_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard to select question count (5, 10, 15)."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="5", callback_data="count:5"),
                InlineKeyboardButton(text="10", callback_data="count:10"),
                InlineKeyboardButton(text="15", callback_data="count:15"),
            ],
            [
                InlineKeyboardButton(text="❌ " + ("Bekor qilish" if lang == "uz" else "Отмена"), callback_data="cancel_action"),
            ],
        ]
    )


def get_quiz_question_keyboard(session_id: str, q_index: int, options: list[str]) -> InlineKeyboardMarkup:
    """Builds inline buttons for 4 options (A, B, C, D).
    
    Each button displays 'A) ...' or A/B/C/D if options are shown in message text.
    To ensure clean UX on mobile screens, we show letters A, B, C, D in a 2x2 grid.
    """
    letters = ["A", "B", "C", "D"]
    rows = []
    
    # Grid: [A, B], [C, D]
    row1 = [
        InlineKeyboardButton(
            text=f"🔘 {letters[0]}",
            callback_data=f"ans:{session_id}:{q_index}:0",
        ),
        InlineKeyboardButton(
            text=f"🔘 {letters[1]}",
            callback_data=f"ans:{session_id}:{q_index}:1",
        ),
    ]
    row2 = [
        InlineKeyboardButton(
            text=f"🔘 {letters[2]}",
            callback_data=f"ans:{session_id}:{q_index}:2",
        ),
        InlineKeyboardButton(
            text=f"🔘 {letters[3]}",
            callback_data=f"ans:{session_id}:{q_index}:3",
        ),
    ]
    rows.append(row1)
    rows.append(row2)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def get_next_question_keyboard(session_id: str, is_last: bool, lang: str = "uz") -> InlineKeyboardMarkup:
    """Button to proceed to the next question or view final results."""
    btn_text = t("btn_finish_quiz" if is_last else "btn_next_question", lang)
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=btn_text, callback_data=f"next:{session_id}"),
            ]
        ]
    )


def get_quiz_finish_keyboard(session_id: str, has_mistakes: bool, lang: str = "uz") -> InlineKeyboardMarkup:
    """Buttons displayed after quiz completion."""
    buttons = []
    if has_mistakes:
        buttons.append([
            InlineKeyboardButton(text=t("btn_view_errors", lang), callback_data=f"review:{session_id}")
        ])
    buttons.append([
        InlineKeyboardButton(text=t("btn_new_quiz", lang), callback_data="new_quiz_prompt"),
        InlineKeyboardButton(text=t("btn_home", lang), callback_data="go_home"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_premade_categories_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Inline keyboard for selecting premade quiz category."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("cat_physics", lang), callback_data="cat:physics"),
            ],
            [
                InlineKeyboardButton(text=t("cat_english", lang), callback_data="cat:english"),
            ],
            [
                InlineKeyboardButton(text=t("cat_it", lang), callback_data="cat:it"),
            ],
            [
                InlineKeyboardButton(text="❌ " + ("Bekor qilish" if lang == "uz" else "Отмена"), callback_data="go_home"),
            ],
        ]
    )


def get_admin_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Admin panel main actions."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_admin_add_question", lang), callback_data="admin:add_q"),
            ],
            [
                InlineKeyboardButton(text=t("btn_admin_refresh", lang), callback_data="admin:refresh"),
                InlineKeyboardButton(text="🏠 " + ("Menyu" if lang == "uz" else "Меню"), callback_data="go_home"),
            ],
        ]
    )


def get_admin_confirm_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Confirm or cancel saving newly drafted admin question."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ " + ("Saqlash" if lang == "uz" else "Сохранить"),
                    callback_data="admin:confirm_save",
                ),
                InlineKeyboardButton(
                    text="❌ " + ("Bekor qilish" if lang == "uz" else "Отмена"),
                    callback_data="admin:cancel_save",
                ),
            ]
        ]
    )
