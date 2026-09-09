import os
import pytest
import pytest_asyncio
import tempfile
import aiosqlite
from unittest.mock import patch

from app.config import Settings
from app.core.database import Database


@pytest.fixture
def mock_settings(monkeypatch):
    """Provides isolated settings for testing."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
    monkeypatch.setenv("GEMINI_API_KEY", "test_gemini_key_12345")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    monkeypatch.setenv("ADMIN_IDS", "[111222333, 999888777]")
    monkeypatch.setenv("AI_DAILY_LIMIT", "5")
    return Settings(
        TELEGRAM_BOT_TOKEN="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
        GEMINI_API_KEY="test_gemini_key_12345",
        GEMINI_MODEL="gemini-2.5-flash",
        ADMIN_IDS=[111222333, 999888777],
        AI_DAILY_LIMIT=5,
    )


@pytest_asyncio.fixture
async def temp_db():
    """Creates a fresh, isolated temporary SQLite database for each test."""
    temp_dir = tempfile.mkdtemp()
    db_file = os.path.join(temp_dir, "test_fika.db")
    test_db = Database(db_path=db_file)
    await test_db.init_db()
    yield test_db
    try:
        if os.path.exists(db_file):
            os.remove(db_file)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    except Exception:
        pass
