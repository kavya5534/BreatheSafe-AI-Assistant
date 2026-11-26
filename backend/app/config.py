import os
from pathlib import Path
from dotenv import dotenv_values, load_dotenv

# Load .env from BreatheSafe_AI root or backend directory
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BASE_DIR.parent

for env_path in (PROJECT_ROOT / ".env", BASE_DIR / ".env"):
    if env_path.exists():
        load_dotenv(env_path)
        break


class Settings:
    """Application settings loaded from environment variables."""

    APP_NAME: str = "BreatheSafe AI"
    APP_TAGLINE: str = "Breathe Better. Live Better. Protect Everyone."
    APP_VERSION: str = "1.0.0"

    BACKEND_HOST: str = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))

    _raw_db_path: str = os.getenv("SQLITE_DB_PATH", "breathesafe.db")
    SQLITE_DB_PATH: str = (
        _raw_db_path
        if os.path.isabs(_raw_db_path)
        else str(BASE_DIR / _raw_db_path)
    )

    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        ).split(",")
        if origin.strip()
    ]

    # AI Provider Abstraction
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "openai_compatible").strip().lower()
    AI_API_KEY: str = os.getenv("AI_API_KEY", "").strip()
    AI_MODEL: str = os.getenv("AI_MODEL", "gpt-4o-mini").strip()
    AI_BASE_URL: str = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").strip().rstrip("/")
    AI_TIMEOUT_SECONDS: float = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))

    # Air Quality & Weather Provider
    AQI_PROVIDER: str = os.getenv("AQI_PROVIDER", "open_meteo").strip().lower()
    WAQI_API_TOKEN: str = os.getenv("WAQI_API_TOKEN", "").strip()
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "").strip()
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "Bengaluru").strip()
    DEFAULT_LAT: float = float(os.getenv("DEFAULT_LAT", "12.9716"))
    DEFAULT_LON: float = float(os.getenv("DEFAULT_LON", "77.5946"))

    def refresh_ai_settings(self) -> None:
        """Reload AI provider values from .env if updated on disk."""
        for env_path in (PROJECT_ROOT / ".env", BASE_DIR / ".env"):
            if env_path.exists():
                values = dotenv_values(env_path)
                if values.get("AI_PROVIDER"):
                    self.AI_PROVIDER = str(values["AI_PROVIDER"]).strip().lower()
                if values.get("AI_API_KEY") is not None:
                    key_val = str(values["AI_API_KEY"]).strip()
                    if key_val:
                        self.AI_API_KEY = key_val
                if values.get("AI_MODEL"):
                    self.AI_MODEL = str(values["AI_MODEL"]).strip()
                if values.get("AI_BASE_URL"):
                    self.AI_BASE_URL = str(values["AI_BASE_URL"]).strip().rstrip("/")
                break


settings = Settings()
