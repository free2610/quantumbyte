"""Handlers package registering all modular routers."""
from app.handlers.common import router as common_router
from app.handlers.ai_quiz import router as ai_quiz_router
from app.handlers.premade_quiz import router as premade_quiz_router
from app.handlers.results import router as results_router
from app.handlers.admin import router as admin_router

all_routers = [
    admin_router,
    common_router,
    ai_quiz_router,
    premade_quiz_router,
    results_router,
]

__all__ = ["all_routers"]
