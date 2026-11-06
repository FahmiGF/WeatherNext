"""WeatherNext AI — Application configuration."""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────
    APP_NAME: str = "WeatherNext AI"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ── Server ───────────────────────────────────────────────────────────
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite+aiosqlite:///./weathernext.db"

    # ── BMKG ─────────────────────────────────────────────────────────────
    BMKG_BASE_URL: str = (
        "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast"
    )

    # ── AI Model Placeholders ────────────────────────────────────────────
    WEATHERNEXT3_API_KEY: str = ""
    WEATHERNEXT3_ENDPOINT: str = ""
    TIMESFM3_API_KEY: str = ""
    TIMESFM3_ENDPOINT: str = ""

    # ── Chatbot ──────────────────────────────────────────────────────────
    LLM_API_KEY: str = ""
    LLM_MODEL: str = ""

    # ── Defaults ─────────────────────────────────────────────────────────
    DEFAULT_CITY: str = "Surabaya"
    DEFAULT_PROVINCE: str = "JawaTimur"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
