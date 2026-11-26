from datetime import datetime, timezone
from fastapi import APIRouter

from app.config import settings
from app.database.db import get_connection
from app.schemas import HealthResponse
from app.services import is_ai_configured

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    db_ok = False
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1").fetchone()
            db_ok = True
    except Exception:
        db_ok = False

    return HealthResponse(
        status="ok" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        database_connected=db_ok,
        ai_configured=is_ai_configured(),
        ai_provider=settings.AI_PROVIDER,
        ai_model=settings.AI_MODEL,
        aqi_provider=settings.AQI_PROVIDER,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
