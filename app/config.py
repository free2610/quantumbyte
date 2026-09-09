import json
import logging
from typing import Any
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    ADMIN_IDS: list[int] = []
    DATABASE_PATH: str = "./data/fika_quiz.db"
    DEFAULT_LANGUAGE: str = "uz"
    AI_DAILY_LIMIT: int = 10
    GEMINI_TIMEOUT_SECONDS: int = 60
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any) -> list[int]:
        if isinstance(v, list):
            return [int(x) for x in v]
        if isinstance(v, (int, float)):
            return [int(v)]
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("[") and v.endswith("]"):
                try:
                    data = json.loads(v)
                    return [int(x) for x in data]
                except Exception:
                    pass
            # Comma-separated fallback
            items = []
            for part in v.replace("[", "").replace("]", "").split(","):
                part = part.strip()
                if part and part.isdigit():
                    items.append(int(part))
            return items
        return []

    @field_validator("DEFAULT_LANGUAGE")
    @classmethod
    def validate_language(cls, v: str) -> str:
        lang = v.lower().strip()
        return lang if lang in ("uz", "ru") else "uz"

    @property
    def has_gemini(self) -> bool:
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY.strip())

    def validate_bot_token(self) -> None:
        if not self.TELEGRAM_BOT_TOKEN or not self.TELEGRAM_BOT_TOKEN.strip():
            raise ValueError(
                "TELEGRAM_BOT_TOKEN sozlanmagan! Iltimos, .env fayliga haqiqiy bot tokeningizni kiriting."
            )


# Global settings instance
settings = Settings()


def setup_logging() -> None:
    level_name = settings.LOG_LEVEL.upper()
    level = getattr(logging, level_name, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
