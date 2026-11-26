from dataclasses import dataclass, field
from typing import Optional


@dataclass
class UserPreferencesRecord:
    session_id: str
    location: str
    latitude: Optional[float]
    longitude: Optional[float]
    preferred_language: str
    age_group: str
    lifestyle: str
    family_categories: list[str] = field(default_factory=list)
    transportation_type: str = "public_transit"
    outdoor_preferences: list[str] = field(default_factory=list)
    updated_at: str = ""
    id: Optional[int] = None


@dataclass
class ChatMessageRecord:
    session_id: str
    role: str
    content: str
    language: str
    created_at: str
    aqi_context: Optional[dict] = None
    model_used: Optional[str] = None
    id: Optional[int] = None


@dataclass
class CommunityReportRecord:
    reporter_name: str
    location: str
    category: str
    severity: str
    description: str
    created_at: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    upvotes: int = 0
    is_sample: bool = False
    id: Optional[int] = None


@dataclass
class SustainableActivityRecord:
    session_id: str
    activity_type: str
    description: str
    co2_saved_kg: float
    points: int
    created_at: str
    id: Optional[int] = None
