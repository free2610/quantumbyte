import pytest
import pytest_asyncio
from app.core.database import Database


@pytest.mark.asyncio
async def test_user_creation_and_language(temp_db: Database):
    user = await temp_db.get_or_create_user(
        user_id=12345,
        username="testuser",
        full_name="Test User",
        default_lang="uz",
    )
    assert user["user_id"] == 12345
    assert user["language"] == "uz"

    # Update language
    await temp_db.set_user_language(12345, "ru")
    current_lang = await temp_db.get_user_language(12345)
    assert current_lang == "ru"


@pytest.mark.asyncio
async def test_premade_questions_seeded(temp_db: Database):
    # Physics Uzbek
    physics_uz = await temp_db.get_premade_questions("physics", "uz", limit=10)
    assert len(physics_uz) == 10

    # Physics Russian
    physics_ru = await temp_db.get_premade_questions("physics", "ru", limit=10)
    assert len(physics_ru) == 10

    # English Uzbek
    english_uz = await temp_db.get_premade_questions("english", "uz", limit=10)
    assert len(english_uz) == 10

    # IT Uzbek
    it_uz = await temp_db.get_premade_questions("it", "uz", limit=10)
    assert len(it_uz) == 10


@pytest.mark.asyncio
async def test_ai_daily_limit_tracking(temp_db: Database):
    date_str = "2026-09-09"
    # Ensure user exists for foreign key constraint
    await temp_db.get_or_create_user(555, "user555", "User 555")
    # Initial usage
    usage = await temp_db.get_ai_daily_usage(555, date_str)
    assert usage == 0

    # First increment
    u1 = await temp_db.increment_ai_daily_usage(555, date_str)
    assert u1 == 1

    # Second increment
    u2 = await temp_db.increment_ai_daily_usage(555, date_str)
    assert u2 == 2

    # Different date
    other_day = await temp_db.get_ai_daily_usage(555, "2026-09-10")
    assert other_day == 0


@pytest.mark.asyncio
async def test_top_leaderboard_logic(temp_db: Database):
    # Create two users
    await temp_db.get_or_create_user(1, "alice", "Alice")
    await temp_db.get_or_create_user(2, "bob", "Bob")
    await temp_db.get_or_create_user(3, "charlie", "Charlie")

    # Alice takes premade: score 8, 45 seconds
    await temp_db.save_quiz_result(1, "premade", "Fizika", 8, 10, 80.0, 45, [])
    # Alice takes another premade: score 10, 60 seconds (better score!)
    await temp_db.save_quiz_result(1, "premade", "Fizika", 10, 10, 100.0, 60, [])

    # Bob takes premade: score 10, 40 seconds (same score as Alice, but lower time!)
    await temp_db.save_quiz_result(2, "premade", "IT", 10, 10, 100.0, 40, [])

    # Charlie takes AI quiz: score 10, 20 seconds. BUT AI quiz MUST NOT enter TOP-10!
    await temp_db.save_quiz_result(3, "ai", "Tarix", 10, 10, 100.0, 20, [])

    leaderboard = await temp_db.get_top_leaderboard(limit=10)

    # Only Alice and Bob should be in leaderboard
    assert len(leaderboard) == 2

    # Bob must be #1 because time (40s) < Alice (60s)
    assert leaderboard[0]["user_id"] == 2
    assert leaderboard[0]["score"] == 10
    assert leaderboard[0]["time_spent_seconds"] == 40

    # Alice must be #2
    assert leaderboard[1]["user_id"] == 1
    assert leaderboard[1]["score"] == 10
    assert leaderboard[1]["time_spent_seconds"] == 60
