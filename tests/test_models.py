import pytest
from pydantic import ValidationError
from app.core.models import QuizQuestionModel, ActiveQuizSession, UserAnswer


def test_valid_quiz_question():
    """Valid question with 4 unique options and correct index must succeed."""
    q = QuizQuestionModel(
        question="O'zbekiston poytaxti qaysi shahar?",
        options=["Toshkent", "Samarqand", "Buxoro", "Xiva"],
        correct_index=0,
        explanation="Toshkent O'zbekiston Respublikasining poytaxti hisoblanadi.",
    )
    assert q.question == "O'zbekiston poytaxti qaysi shahar?"
    assert len(q.options) == 4
    assert q.correct_index == 0


def test_invalid_options_count():
    """Question with != 4 options must raise ValidationError."""
    with pytest.raises(ValidationError):
        QuizQuestionModel(
            question="Savol matni?",
            options=["A", "B", "C"],  # Only 3 options
            correct_index=0,
            explanation="Izoh",
        )

    with pytest.raises(ValidationError):
        QuizQuestionModel(
            question="Savol matni?",
            options=["A", "B", "C", "D", "E"],  # 5 options
            correct_index=0,
            explanation="Izoh",
        )


def test_duplicate_options():
    """Options containing duplicates must raise ValidationError."""
    with pytest.raises(ValidationError):
        QuizQuestionModel(
            question="Savol matni?",
            options=["Variant", "Variant", "Boshqa 1", "Boshqa 2"],
            correct_index=0,
            explanation="Izoh",
        )


def test_invalid_correct_index():
    """Index outside 0..3 must raise ValidationError."""
    with pytest.raises(ValidationError):
        QuizQuestionModel(
            question="Savol matni?",
            options=["A", "B", "C", "D"],
            correct_index=4,  # Out of bounds
            explanation="Izoh",
        )

    with pytest.raises(ValidationError):
        QuizQuestionModel(
            question="Savol matni?",
            options=["A", "B", "C", "D"],
            correct_index=-1,
            explanation="Izoh",
        )


def test_session_score_and_percentage_calculation():
    """Calculations for score, percentages, and completion status."""
    q1 = QuizQuestionModel(
        question="1-savol?",
        options=["A", "B", "C", "D"],
        correct_index=0,
        explanation="Izoh 1",
    )
    q2 = QuizQuestionModel(
        question="2-savol?",
        options=["A", "B", "C", "D"],
        correct_index=1,
        explanation="Izoh 2",
    )

    session = ActiveQuizSession(
        user_id=123,
        test_type="ai",
        topic="Matematika",
        questions=[q1, q2],
    )

    assert session.total_questions == 2
    assert session.correct_count == 0
    assert session.percentage == 0.0
    assert not session.is_completed

    # Answer 1 correctly
    session.answers.append(UserAnswer(question_index=0, selected_index=0, is_correct=True))
    session.current_index = 1
    assert session.correct_count == 1
    assert session.percentage == 50.0

    # Answer 2 incorrectly
    session.answers.append(UserAnswer(question_index=1, selected_index=0, is_correct=False))
    session.current_index = 2
    assert session.correct_count == 1
    assert session.incorrect_count == 1
    assert session.percentage == 50.0
    assert session.is_completed
