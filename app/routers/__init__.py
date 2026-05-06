from .auth_router import router as auth_router
from .user_router import router as user_router
from .task_router import router as task_router

__all__ = ["auth_router", "user_router","task_router"]