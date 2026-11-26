from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator


SupportedLanguage = Literal["en", "kn", "hi"]


class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    database_connected: bool
    ai_configured: bool
    ai_provider: str
    ai_model: str
    aqi_provider: str
    timestamp: str


class PollutantMetrics(BaseModel):
    aqi: int
    aqi_scale: str = "US EPA (0-500)"
    pm25: float
    pm10: float
    co: float
    no2: float
    so2: float
    o3: float


class WeatherMetrics(BaseModel):
    temperature_c: float
    humidity_pct: float
    wind_speed_kmh: float
    condition: str
    apparent_temp_c: Optional[float] = None


class HourlyPoint(BaseModel):
    time: str
    aqi: int
    pm25: float
    pm10: float
    o3: float


class SeverityInfo(BaseModel):
    level: Literal["good", "moderate", "sensitive", "unhealthy", "very_unhealthy", "hazardous"]
    label: str
    color_hex: str
    summary: str


class PrecautionItem(BaseModel):
    title: str
    detail: str
    reason: str
    audience: str


class DailyUpdateItem(BaseModel):
    title: str
    detail: str
    category: str


class DashboardResponse(BaseModel):
    location: str
    latitude: float
    longitude: float
    language: SupportedLanguage
    is_live: bool
    data_source: str
    last_updated: str
    notice: Optional[str] = None
    pollutants: PollutantMetrics
    weather: WeatherMetrics
    severity: SeverityInfo
    hourly_trend: list[HourlyPoint]
    precautions: list[PrecautionItem]
    daily_updates: list[DailyUpdateItem]
    personalized_routine: list[DailyUpdateItem]


class PreferencesIn(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=64)
    location: str = Field(..., min_length=2, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    preferred_language: SupportedLanguage = "en"
    age_group: Literal["child", "teen", "adult", "senior"] = "adult"
    lifestyle: Literal["sedentary", "balanced", "active", "outdoor_worker"] = "balanced"
    family_categories: list[
        Literal["general", "children", "elderly", "pregnant", "respiratory_sensitive"]
    ] = Field(default_factory=lambda: ["general"])
    transportation_type: Literal[
        "walking", "cycling", "public_transit", "two_wheeler", "car", "ev"
    ] = "public_transit"
    outdoor_preferences: list[
        Literal["morning_walk", "evening_jog", "cycling", "gardening", "sports", "mostly_indoor"]
    ] = Field(default_factory=lambda: ["morning_walk"])

    @field_validator("location")
    @classmethod
    def clean_location(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError("Location must be at least 2 characters.")
        return cleaned


class PreferencesOut(PreferencesIn):
    updated_at: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: SupportedLanguage = "en"
    session_id: str = Field(default="default", min_length=1, max_length=64)
    city: Optional[str] = Field(default=None, max_length=120)
    include_aqi_context: bool = True

    @field_validator("message")
    @classmethod
    def clean_message(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty.")
        return cleaned


class SetupGuide(BaseModel):
    title: str
    explanation: str
    steps: list[str]
    env_example: str


class ChatResponse(BaseModel):
    configured: bool
    language: SupportedLanguage
    reply: Optional[str] = None
    model_used: Optional[str] = None
    provider: str
    aqi_context_used: Optional[dict] = None
    error: Optional[str] = None
    setup_guide: Optional[SetupGuide] = None
    created_at: str


class ChatMessageOut(BaseModel):
    id: int
    session_id: str
    role: Literal["user", "assistant"]
    content: str
    language: SupportedLanguage
    model_used: Optional[str] = None
    created_at: str


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: list[ChatMessageOut]


class CommunityReportCreate(BaseModel):
    reporter_name: str = Field(..., min_length=2, max_length=60)
    location: str = Field(..., min_length=2, max_length=120)
    latitude: Optional[float] = Field(default=None, ge=-90, le=90)
    longitude: Optional[float] = Field(default=None, ge=-180, le=180)
    category: Literal[
        "smoke",
        "dust",
        "vehicle_emissions",
        "industrial_odor",
        "burning_waste",
        "clean_zone",
    ]
    severity: Literal["low", "moderate", "high", "critical"]
    description: str = Field(..., min_length=8, max_length=600)

    @field_validator("reporter_name", "location", "description")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()


class CommunityReportOut(CommunityReportCreate):
    id: int
    upvotes: int
    is_sample: bool = False
    created_at: str


class SustainableActivityCreate(BaseModel):
    session_id: str = Field(default="default", min_length=1, max_length=64)
    activity_type: Literal[
        "public_transit",
        "cycling",
        "walking",
        "carpool",
        "indoor_plants",
        "energy_saving",
        "no_burn",
    ]
    description: str = Field(..., min_length=4, max_length=300)

    @field_validator("description")
    @classmethod
    def strip_desc(cls, value: str) -> str:
        return value.strip()


class SustainableActivityOut(SustainableActivityCreate):
    id: int
    co2_saved_kg: float
    points: int
    created_at: str
