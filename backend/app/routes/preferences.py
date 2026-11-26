from fastapi import APIRouter, Query

from app.database.repository import get_preferences, upsert_preferences
from app.schemas import PreferencesIn, PreferencesOut

router = APIRouter(prefix="/api", tags=["preferences"])


@router.get("/preferences", response_model=PreferencesOut)
def read_preferences(
    session_id: str = Query(default="default", min_length=1, max_length=64),
) -> PreferencesOut:
    record = get_preferences(session_id)
    return PreferencesOut(
        session_id=record.session_id,
        location=record.location,
        latitude=record.latitude,
        longitude=record.longitude,
        preferred_language=record.preferred_language,
        age_group=record.age_group,
        lifestyle=record.lifestyle,
        family_categories=record.family_categories,
        transportation_type=record.transportation_type,
        outdoor_preferences=record.outdoor_preferences,
        updated_at=record.updated_at,
    )


@router.post("/preferences", response_model=PreferencesOut)
def save_preferences(payload: PreferencesIn) -> PreferencesOut:
    record = upsert_preferences(payload)
    return PreferencesOut(
        session_id=record.session_id,
        location=record.location,
        latitude=record.latitude,
        longitude=record.longitude,
        preferred_language=record.preferred_language,
        age_group=record.age_group,
        lifestyle=record.lifestyle,
        family_categories=record.family_categories,
        transportation_type=record.transportation_type,
        outdoor_preferences=record.outdoor_preferences,
        updated_at=record.updated_at,
    )
