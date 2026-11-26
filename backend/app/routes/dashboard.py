from typing import Optional
from fastapi import APIRouter, Query

from app.database.repository import get_preferences
from app.schemas import DashboardResponse, SupportedLanguage
from app.services import (
    build_daily_updates,
    build_personalized_routine,
    build_precautions,
    classify_severity,
    fetch_air_quality_and_weather,
)

router = APIRouter(prefix="/api", tags=["dashboard"])


@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    city: Optional[str] = Query(default=None, max_length=120),
    lat: Optional[float] = Query(default=None, ge=-90, le=90),
    lon: Optional[float] = Query(default=None, ge=-180, le=180),
    lang: SupportedLanguage = Query(default="en"),
    session_id: str = Query(default="default", min_length=1, max_length=64),
) -> DashboardResponse:
    prefs = get_preferences(session_id)
    target_city = city if city and city.strip() else prefs.location
    target_lat = lat if lat is not None else (prefs.latitude if not city else None)
    target_lon = lon if lon is not None else (prefs.longitude if not city else None)

    env_data = await fetch_air_quality_and_weather(
        city=target_city,
        lat=target_lat,
        lon=target_lon,
        lang=lang,
    )

    pollutants = env_data["pollutants"]
    severity = classify_severity(pollutants.aqi, lang)
    precautions = build_precautions(pollutants, prefs, lang)
    daily_updates = build_daily_updates(pollutants, lang)
    personalized_routine = build_personalized_routine(pollutants, prefs, lang)

    return DashboardResponse(
        location=env_data["location"],
        latitude=env_data["latitude"],
        longitude=env_data["longitude"],
        language=lang,
        is_live=env_data["is_live"],
        data_source=env_data["data_source"],
        last_updated=env_data["last_updated"],
        notice=env_data["notice"],
        pollutants=pollutants,
        weather=env_data["weather"],
        severity=severity,
        hourly_trend=env_data["hourly_trend"],
        precautions=precautions,
        daily_updates=daily_updates,
        personalized_routine=personalized_routine,
    )
