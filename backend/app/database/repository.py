import json
from typing import Optional

from app.config import settings
from app.database.db import get_connection, utc_now_iso
from app.models import (
    ChatMessageRecord,
    CommunityReportRecord,
    SustainableActivityRecord,
    UserPreferencesRecord,
)
from app.schemas import CommunityReportCreate, PreferencesIn, SustainableActivityCreate


def _row_to_prefs(row) -> UserPreferencesRecord:
    return UserPreferencesRecord(
        id=row["id"],
        session_id=row["session_id"],
        location=row["location"],
        latitude=row["latitude"],
        longitude=row["longitude"],
        preferred_language=row["preferred_language"],
        age_group=row["age_group"],
        lifestyle=row["lifestyle"],
        family_categories=json.loads(row["family_categories"] or '["general"]'),
        transportation_type=row["transportation_type"],
        outdoor_preferences=json.loads(row["outdoor_preferences"] or '["morning_walk"]'),
        updated_at=row["updated_at"],
    )


def get_preferences(session_id: str = "default") -> UserPreferencesRecord:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM user_preferences WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if row:
            return _row_to_prefs(row)

        now = utc_now_iso()
        conn.execute(
            """
            INSERT INTO user_preferences (
                session_id, location, latitude, longitude, preferred_language,
                age_group, lifestyle, family_categories, transportation_type,
                outdoor_preferences, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                settings.DEFAULT_CITY,
                settings.DEFAULT_LAT,
                settings.DEFAULT_LON,
                "en",
                "adult",
                "balanced",
                json.dumps(["general"]),
                "public_transit",
                json.dumps(["morning_walk"]),
                now,
            ),
        )
        created = conn.execute(
            "SELECT * FROM user_preferences WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        return _row_to_prefs(created)


def upsert_preferences(payload: PreferencesIn) -> UserPreferencesRecord:
    now = utc_now_iso()
    with get_connection() as conn:
        existing = conn.execute(
            "SELECT id FROM user_preferences WHERE session_id = ?",
            (payload.session_id,),
        ).fetchone()

        if existing:
            conn.execute(
                """
                UPDATE user_preferences
                SET location = ?, latitude = ?, longitude = ?, preferred_language = ?,
                    age_group = ?, lifestyle = ?, family_categories = ?,
                    transportation_type = ?, outdoor_preferences = ?, updated_at = ?
                WHERE session_id = ?
                """,
                (
                    payload.location,
                    payload.latitude,
                    payload.longitude,
                    payload.preferred_language,
                    payload.age_group,
                    payload.lifestyle,
                    json.dumps(payload.family_categories),
                    payload.transportation_type,
                    json.dumps(payload.outdoor_preferences),
                    now,
                    payload.session_id,
                ),
            )
        else:
            conn.execute(
                """
                INSERT INTO user_preferences (
                    session_id, location, latitude, longitude, preferred_language,
                    age_group, lifestyle, family_categories, transportation_type,
                    outdoor_preferences, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.session_id,
                    payload.location,
                    payload.latitude,
                    payload.longitude,
                    payload.preferred_language,
                    payload.age_group,
                    payload.lifestyle,
                    json.dumps(payload.family_categories),
                    payload.transportation_type,
                    json.dumps(payload.outdoor_preferences),
                    now,
                ),
            )

        row = conn.execute(
            "SELECT * FROM user_preferences WHERE session_id = ?",
            (payload.session_id,),
        ).fetchone()
        return _row_to_prefs(row)


def save_chat_message(
    session_id: str,
    role: str,
    content: str,
    language: str,
    aqi_context: Optional[dict] = None,
    model_used: Optional[str] = None,
) -> ChatMessageRecord:
    now = utc_now_iso()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO chat_history (session_id, role, content, language, aqi_context, model_used, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                role,
                content,
                language,
                json.dumps(aqi_context) if aqi_context else None,
                model_used,
                now,
            ),
        )
        return ChatMessageRecord(
            id=cursor.lastrowid,
            session_id=session_id,
            role=role,
            content=content,
            language=language,
            aqi_context=aqi_context,
            model_used=model_used,
            created_at=now,
        )


def list_chat_history(session_id: str = "default", limit: int = 50) -> list[ChatMessageRecord]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM chat_history
            WHERE session_id = ?
            ORDER BY id ASC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
        return [
            ChatMessageRecord(
                id=row["id"],
                session_id=row["session_id"],
                role=row["role"],
                content=row["content"],
                language=row["language"],
                aqi_context=json.loads(row["aqi_context"]) if row["aqi_context"] else None,
                model_used=row["model_used"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


def clear_chat_history(session_id: str = "default") -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM chat_history WHERE session_id = ?",
            (session_id,),
        )
        return cursor.rowcount


def list_community_reports(limit: int = 50) -> list[CommunityReportRecord]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM community_reports
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        return [
            CommunityReportRecord(
                id=row["id"],
                reporter_name=row["reporter_name"],
                location=row["location"],
                latitude=row["latitude"],
                longitude=row["longitude"],
                category=row["category"],
                severity=row["severity"],
                description=row["description"],
                upvotes=row["upvotes"],
                is_sample=bool(row["is_sample"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]


def create_community_report(payload: CommunityReportCreate) -> CommunityReportRecord:
    now = utc_now_iso()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO community_reports (
                reporter_name, location, latitude, longitude, category,
                severity, description, upvotes, is_sample, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?)
            """,
            (
                payload.reporter_name,
                payload.location,
                payload.latitude,
                payload.longitude,
                payload.category,
                payload.severity,
                payload.description,
                now,
            ),
        )
        return CommunityReportRecord(
            id=cursor.lastrowid,
            reporter_name=payload.reporter_name,
            location=payload.location,
            latitude=payload.latitude,
            longitude=payload.longitude,
            category=payload.category,
            severity=payload.severity,
            description=payload.description,
            upvotes=0,
            is_sample=False,
            created_at=now,
        )


def upvote_community_report(report_id: int) -> Optional[CommunityReportRecord]:
    with get_connection() as conn:
        conn.execute(
            "UPDATE community_reports SET upvotes = upvotes + 1 WHERE id = ?",
            (report_id,),
        )
        row = conn.execute(
            "SELECT * FROM community_reports WHERE id = ?",
            (report_id,),
        ).fetchone()
        if not row:
            return None
        return CommunityReportRecord(
            id=row["id"],
            reporter_name=row["reporter_name"],
            location=row["location"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            category=row["category"],
            severity=row["severity"],
            description=row["description"],
            upvotes=row["upvotes"],
            is_sample=bool(row["is_sample"]),
            created_at=row["created_at"],
        )


ACTIVITY_IMPACT = {
    "public_transit": (2.4, 25),
    "cycling": (3.1, 35),
    "walking": (2.0, 30),
    "carpool": (1.8, 20),
    "indoor_plants": (0.4, 15),
    "energy_saving": (1.5, 20),
    "no_burn": (4.0, 40),
}


def list_sustainable_activities(session_id: str = "default", limit: int = 30) -> list[SustainableActivityRecord]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT * FROM sustainable_activities
            WHERE session_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (session_id, limit),
        ).fetchall()
        return [
            SustainableActivityRecord(
                id=row["id"],
                session_id=row["session_id"],
                activity_type=row["activity_type"],
                description=row["description"],
                co2_saved_kg=row["co2_saved_kg"],
                points=row["points"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


def create_sustainable_activity(payload: SustainableActivityCreate) -> SustainableActivityRecord:
    now = utc_now_iso()
    co2_saved, points = ACTIVITY_IMPACT.get(payload.activity_type, (1.0, 15))
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO sustainable_activities (
                session_id, activity_type, description, co2_saved_kg, points, created_at
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                payload.session_id,
                payload.activity_type,
                payload.description,
                co2_saved,
                points,
                now,
            ),
        )
        return SustainableActivityRecord(
            id=cursor.lastrowid,
            session_id=payload.session_id,
            activity_type=payload.activity_type,
            description=payload.description,
            co2_saved_kg=co2_saved,
            points=points,
            created_at=now,
        )
