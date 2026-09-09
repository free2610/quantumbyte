from aiogram.fsm.state import State, StatesGroup


class AIQuizStates(StatesGroup):
    """FSM states for creating a quiz with Gemini AI."""
    choose_mode = State()        # by topic or by text
    waiting_topic = State()      # waiting for topic text
    waiting_text = State()       # waiting for custom text
    waiting_difficulty = State()# easy, medium, hard
    waiting_count = State()      # 5, 10, 15


class AdminAddQuestionStates(StatesGroup):
    """FSM states for Admin adding a new pre-made question."""
    choose_lang = State()
    choose_category = State()
    enter_question = State()
    enter_option_1 = State()
    enter_option_2 = State()
    enter_option_3 = State()
    enter_option_4 = State()
    enter_correct_index = State()
    enter_explanation = State()
    confirm_save = State()
