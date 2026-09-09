import pytest
from app.services.gemini import GeminiService, GeminiValidationError


def test_clean_json_markdown():
    """Service cleanly removes ```json markdown code fences."""
    service = GeminiService()
    raw = "```json\n{\"questions\": []}\n```"
    cleaned = service._clean_json_text(raw)
    assert cleaned == "{\"questions\": []}"


def test_parse_valid_quiz_json():
    """Service successfully parses and validates standard JSON quiz payload."""
    service = GeminiService()
    payload = """
    {
        "questions": [
            {
                "question": "Python yaratuvchisi kim?",
                "options": ["Guido van Rossum", "James Gosling", "Dennis Ritchie", "Bjarne Stroustrup"],
                "correct_index": 0,
                "explanation": "Guido van Rossum 1991-yilda Python tilini yaratgan."
            },
            {
                "question": "Git nima?",
                "options": ["Versiyalarni boshqarish tizimi", "Ma'lumotlar bazasi", "Operatsion tizim", "Kompilyator"],
                "correct_index": 0,
                "explanation": "Git tarqatilgan versiyalarni boshqarish tizimidir."
            }
        ]
    }
    """
    questions = service._parse_and_validate(payload, expected_count=2)
    assert len(questions) == 2
    assert questions[0].question == "Python yaratuvchisi kim?"
    assert questions[1].correct_index == 0


def test_parse_insufficient_questions_raises_error():
    """Service raises GeminiValidationError when fewer questions than expected are returned."""
    service = GeminiService()
    payload = """
    {
        "questions": [
            {
                "question": "Bitta savol?",
                "options": ["A", "B", "C", "D"],
                "correct_index": 1,
                "explanation": "Izoh"
            }
        ]
    }
    """
    with pytest.raises(GeminiValidationError):
        service._parse_and_validate(payload, expected_count=5)


def test_parse_malformed_json_raises_error():
    """Service raises error when JSON syntax is corrupted."""
    service = GeminiService()
    payload = "{ malformed json: not valid ... }"
    with pytest.raises(Exception):
        service._parse_and_validate(payload, expected_count=1)
