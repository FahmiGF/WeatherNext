"""Admin / monitoring Pydantic schemas."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ModelStatus(BaseModel):
    name: str
    version: str
    status: str  # "online", "mock", "offline"
    description: str
    forecast_range: str


class AccuracyMetrics(BaseModel):
    model_name: str
    horizon_days: int
    mae_temperature: Optional[float] = None
    rmse_temperature: Optional[float] = None
    brier_score_rain: Optional[float] = None
    sample_count: int = 0


class ForecastRunOut(BaseModel):
    id: int
    model_name: str
    model_version: str
    run_started_at: datetime
    run_completed_at: Optional[datetime] = None
    status: str
    locations_processed: int
    error_message: Optional[str] = None

    model_config = {"from_attributes": True}


class SystemStats(BaseModel):
    total_locations: int
    total_observations: int
    total_forecasts: int
    total_alerts: int
    total_chat_sessions: int
    total_chat_messages: int
    database_size_mb: Optional[float] = None
