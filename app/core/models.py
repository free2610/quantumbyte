import uuid
import time
from pydantic import BaseModel, Field, field_validator, model_validator


class QuizQuestionModel(BaseModel):
    """Pydantic model for validating each quiz question from Gemini or Admin."""
    question: str = Field(..., min_length=5, max_length=1000, description="Savol matni")
    options: list[str] = Field(..., min_length=4, max_length=4, description="4 ta javob varianti")
    correct_index: int = Field(..., ge=0, le=3, description="0 dan 3 gacha to'g'ri javob indeksi")
    explanation: str = Field(..., min_length=3, max_length=1000, description="Qisqa tushuntirish")

    @field_validator("options")
    @classmethod
    def validate_options(cls, v: list[str]) -> list[str]:
        cleaned = [opt.strip() for opt in v]
        if len(cleaned) != 4:
            raise ValueError("Javob variantlari soni aynan 4 ta bo'lishi shart.")
        if any(not opt for opt in cleaned):
            raise ValueError("Javob variantlari bo'sh bo'lishi mumkin emas.")
        # Check uniqueness case-insensitively
        lower_cleaned = [opt.lower() for opt in cleaned]
        if len(set(lower_cleaned)) != 4:
            raise ValueError("Javob variantlari bir-biridan farq qilishi shart, takrorlanmasin.")
        for opt in cleaned:
            if len(opt) > 120:
                raise ValueError("Javob varianti 120 belgidan oshmasligi kerak.")
        return cleaned

    @field_validator("question")
    @classmethod
    def clean_question(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Savol matni bo'sh bo'lishi mumkin emas.")
        return s

    @field_validator("explanation")
    @classmethod
    def clean_explanation(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("Izoh matni bo'sh bo'lishi mumkin emas.")
        return s


class QuizListResponse(BaseModel):
    """Container for a list of generated quiz questions."""
    questions: list[QuizQuestionModel] = Field(..., min_length=1)


class UserAnswer(BaseModel):
    """Record of a user's answer to a specific question."""
    question_index: int
    selected_index: int
    is_correct: bool


class ActiveQuizSession(BaseModel):
    """In-memory active quiz session for a user."""
    session_id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    user_id: int
    test_type: str  # "ai" or "premade"
    topic: str
    difficulty: str = "o'rtacha"
    questions: list[QuizQuestionModel]
    current_index: int = 0
    answers: list[UserAnswer] = Field(default_factory=list)
    start_time: float = Field(default_factory=time.time)
    end_time: float | None = None
    answered_current: bool = False

    @property
    def total_questions(self) -> int:
        return len(self.questions)

    @property
    def correct_count(self) -> int:
        return sum(1 for a in self.answers if a.is_correct)

    @property
    def incorrect_count(self) -> int:
        return len(self.answers) - self.correct_count

    @property
    def percentage(self) -> float:
        if not self.total_questions:
            return 0.0
        return round((self.correct_count / self.total_questions) * 100, 1)

    @property
    def time_spent_seconds(self) -> int:
        finish = self.end_time or time.time()
        return max(1, int(finish - self.start_time))

    @property
    def is_completed(self) -> bool:
        return self.current_index >= self.total_questions
