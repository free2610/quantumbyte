import html
from aiogram.filters import Filter
from aiogram.types import TelegramObject, User
from app.config import settings


def escape_html(text: str | None) -> str:
    """Escapes HTML special characters to prevent Telegram parse mode errors."""
    if not text:
        return ""
    return html.escape(str(text), quote=False)


def sanitize_topic(text: str, max_length: int = 200) -> str:
    """Validates and sanitizes user quiz topic."""
    cleaned = text.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned


def sanitize_custom_text(text: str, max_length: int = 3000) -> str:
    """Validates and sanitizes custom text input for AI quiz."""
    cleaned = text.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    return cleaned


def is_admin(user_id: int) -> bool:
    """Checks if a Telegram user ID is present in ADMIN_IDS."""
    return user_id in settings.ADMIN_IDS


class IsAdminFilter(Filter):
    """Aiogram filter for handlers requiring admin permissions."""
    async def __call__(self, obj: TelegramObject) -> bool:
        user: User | None = getattr(obj, "from_user", None)
        if not user:
            return False
        return is_admin(user.id)
