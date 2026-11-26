from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.database.repository import (
    clear_chat_history,
    get_preferences,
    list_chat_history,
    save_chat_message,
)
from app.schemas import (
    ChatHistoryResponse,
    ChatMessageOut,
    ChatRequest,
    ChatResponse,
)
from app.services import chat_with_assistant, fetch_air_quality_and_weather, is_ai_configured

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def post_chat(payload: ChatRequest) -> ChatResponse:
    prefs = get_preferences(payload.session_id)

    aqi_context = None
    if payload.include_aqi_context:
        target_city = payload.city.strip() if payload.city and payload.city.strip() else prefs.location
        env_data = await fetch_air_quality_and_weather(
            city=target_city,
            lat=prefs.latitude if not payload.city else None,
            lon=prefs.longitude if not payload.city else None,
            lang=payload.language,
        )
        aqi_context = {
            "location": env_data["location"],
            "is_live": env_data["is_live"],
            "data_source": env_data["data_source"],
            "last_updated": env_data["last_updated"],
            "pollutants": env_data["pollutants"].model_dump(),
            "weather": env_data["weather"].model_dump(),
        }

    # If AI key is missing, return setup instructions immediately without faking AI output
    if not is_ai_configured():
        return await chat_with_assistant(
            user_message=payload.message,
            language=payload.language,
            prefs=prefs,
            history=[],
            aqi_context=aqi_context,
        )

    prior_records = list_chat_history(payload.session_id, limit=20)
    history = [{"role": rec.role, "content": rec.content} for rec in prior_records]

    # Persist user message in SQLite
    save_chat_message(
        session_id=payload.session_id,
        role="user",
        content=payload.message,
        language=payload.language,
        aqi_context=aqi_context,
    )

    try:
        response = await chat_with_assistant(
            user_message=payload.message,
            language=payload.language,
            prefs=prefs,
            history=history,
            aqi_context=aqi_context,
        )
    except Exception as exc:
        return ChatResponse(
            configured=True,
            language=payload.language,
            reply=None,
            model_used=settings.AI_MODEL,
            provider=settings.AI_PROVIDER,
            aqi_context_used=aqi_context,
            error=str(exc),
            setup_guide=None,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

    if response.reply:
        save_chat_message(
            session_id=payload.session_id,
            role="assistant",
            content=response.reply,
            language=payload.language,
            aqi_context=aqi_context,
            model_used=response.model_used,
        )

    return response


@router.get("/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str = Query(default="default", min_length=1, max_length=64),
) -> ChatHistoryResponse:
    records = list_chat_history(session_id)
    return ChatHistoryResponse(
        session_id=session_id,
        messages=[
            ChatMessageOut(
                id=rec.id or 0,
                session_id=rec.session_id,
                role=rec.role,
                content=rec.content,
                language=rec.language,
                model_used=rec.model_used,
                created_at=rec.created_at,
            )
            for rec in records
        ],
    )


@router.delete("/chat/history")
def delete_chat_history(
    session_id: str = Query(default="default", min_length=1, max_length=64),
) -> dict:
    deleted_count = clear_chat_history(session_id)
    return {"status": "cleared", "deleted_messages": deleted_count}
