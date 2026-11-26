from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.routes import (
    chat_router,
    dashboard_router,
    health_router,
    preferences_router,
    reports_router,
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_TAGLINE,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(dashboard_router)
app.include_router(chat_router)
app.include_router(preferences_router)
app.include_router(reports_router)


@app.get("/")
def root() -> dict:
    return {
        "name": settings.APP_NAME,
        "tagline": settings.APP_TAGLINE,
        "docs": "/docs",
        "health": "/api/health",
    }
