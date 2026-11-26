import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Generator

from app.config import settings


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Initialize SQLite tables for preferences, chat history, reports, and sustainable activities."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                preferred_language TEXT NOT NULL DEFAULT 'en',
                age_group TEXT NOT NULL DEFAULT 'adult',
                lifestyle TEXT NOT NULL DEFAULT 'balanced',
                family_categories TEXT NOT NULL DEFAULT '[]',
                transportation_type TEXT NOT NULL DEFAULT 'public_transit',
                outdoor_preferences TEXT NOT NULL DEFAULT '[]',
                updated_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                language TEXT NOT NULL DEFAULT 'en',
                aqi_context TEXT,
                model_used TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS community_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporter_name TEXT NOT NULL,
                location TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                category TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                upvotes INTEGER NOT NULL DEFAULT 0,
                is_sample INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sustainable_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL DEFAULT 'default',
                activity_type TEXT NOT NULL,
                description TEXT NOT NULL,
                co2_saved_kg REAL NOT NULL DEFAULT 0.0,
                points INTEGER NOT NULL DEFAULT 10,
                created_at TEXT NOT NULL
            )
            """
        )

        # Ensure a default preference profile exists
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM user_preferences WHERE session_id = ?",
            ("default",),
        )
        if cursor.fetchone()["cnt"] == 0:
            cursor.execute(
                """
                INSERT INTO user_preferences (
                    session_id, location, latitude, longitude, preferred_language,
                    age_group, lifestyle, family_categories, transportation_type,
                    outdoor_preferences, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "default",
                    settings.DEFAULT_CITY,
                    settings.DEFAULT_LAT,
                    settings.DEFAULT_LON,
                    "en",
                    "adult",
                    "active",
                    json.dumps(["general"]),
                    "public_transit",
                    json.dumps(["morning_walk", "cycling"]),
                    utc_now_iso(),
                ),
            )
