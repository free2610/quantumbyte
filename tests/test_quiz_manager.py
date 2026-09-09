import pytest
from app.core.models import QuizQuestionModel
from app.services.quiz_manager import QuizManager, AlreadyAnsweredError, InvalidSessionError


@pytest.fixture
def sample_questions():
    return [
        QuizQuestionModel(
            question="1-savol: O'zbekiston poytaxti?",
            options=["Toshkent", "Samarqand", "Buxoro", "Navoiy"],
            correct_index=0,
            explanation="Toshkent poytaxt.",
        ),
        QuizQuestionModel(
            question="2-savol: 2 + 2 nechaga teng?",
            options=["3", "4", "5", "6"],
            correct_index=1,
            explanation="2 + 2 = 4.",
        ),
    ]


def test_start_session(sample_questions):
    qm = QuizManager()
    session = qm.start_session(
        user_id=100,
        test_type="ai",
        topic="Umumiy bilim",
        difficulty="oson",
        questions=sample_questions,
    )

    assert qm.has_active_session(100)
    assert session.current_index == 0
    assert session.total_questions == 2
    assert not session.is_completed


def test_answer_and_anti_duplicate(sample_questions):
    qm = QuizManager()
    session = qm.start_session(
        user_id=100,
        test_type="ai",
        topic="Umumiy bilim",
        difficulty="oson",
        questions=sample_questions,
    )

    # First answer
    is_correct, expl, q = qm.answer_question(
        user_id=100,
        session_id=session.session_id,
        question_index=0,
        selected_index=0,
    )
    assert is_correct is True
    assert session.correct_count == 1

    # Second answer to the SAME question MUST raise AlreadyAnsweredError
    with pytest.raises(AlreadyAnsweredError):
        qm.answer_question(
            user_id=100,
            session_id=session.session_id,
            question_index=0,
            selected_index=1,
        )

    # Score must NOT be increased
    assert session.correct_count == 1


def test_invalid_session_guard(sample_questions):
    qm = QuizManager()
    session = qm.start_session(
        user_id=100,
        test_type="ai",
        topic="Umumiy bilim",
        difficulty="oson",
        questions=sample_questions,
    )

    with pytest.raises(InvalidSessionError):
        qm.answer_question(
            user_id=100,
            session_id="wrong_session_id",
            question_index=0,
            selected_index=0,
        )


def test_next_question_flow(sample_questions):
    qm = QuizManager()
    session = qm.start_session(
        user_id=100,
        test_type="ai",
        topic="Test",
        difficulty="oson",
        questions=sample_questions,
    )

    # Question 0 answered
    qm.answer_question(100, session.session_id, 0, 0)
    next_q, is_finished = qm.next_question(100, session.session_id)
    assert is_finished is False
    assert next_q is not None
    assert next_q.question == sample_questions[1].question

    # Question 1 answered
    qm.answer_question(100, session.session_id, 1, 1)
    next_q, is_finished = qm.next_question(100, session.session_id)
    assert is_finished is True
    assert next_q is None
    assert session.is_completed
    assert session.correct_count == 2
    assert session.percentage == 100.0
