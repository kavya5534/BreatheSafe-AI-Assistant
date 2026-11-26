from .chat import router as chat_router
from .dashboard import router as dashboard_router
from .health import router as health_router
from .preferences import router as preferences_router
from .reports import router as reports_router

__all__ = [
    "health_router",
    "dashboard_router",
    "chat_router",
    "preferences_router",
    "reports_router",
]
