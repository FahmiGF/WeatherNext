"""Weather & forecast Pydantic schemas."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


# ── Current / Observation ────────────────────────────────────────────────────

class WeatherObservationOut(BaseModel):
    id: int
    location_id: int
    observed_at: datetime
    temperature: float
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    humidity: float
    wind_speed: float
    wind_direction: float
    precipitation: float
    cloud_cover: float
    pressure: Optional[float] = None
    uv_index: Optional[float] = None
    condition: str
    condition_code: str
    source: str

    model_config = {"from_attributes": True}


class CurrentWeatherOut(BaseModel):
    """Enriched response for current weather."""
    location: "LocationSummary"
    observation: WeatherObservationOut
    feels_like: Optional[float] = None


# ── Forecasts ────────────────────────────────────────────────────────────────

class ForecastDayOut(BaseModel):
    forecast_date: date
    model_name: str
    model_version: Optional[str] = None
    forecast_horizon_days: int
    temperature_min: float
    temperature_max: float
    rain_probability: float = Field(ge=0, le=100)
    precipitation_estimate: float
    humidity: float
    wind_speed: float
    wind_direction: float
    cloud_cover: float
    uv_index: Optional[float] = None
    condition: str
    condition_code: str
    confidence_score: Optional[float] = None
    uncertainty_low: Optional[float] = None
    uncertainty_high: Optional[float] = None

    model_config = {"from_attributes": True}


class WeeklyForecastOut(BaseModel):
    location: "LocationSummary"
    forecasts: list[ForecastDayOut]
    generated_at: datetime


class MonthlyOutlookOut(BaseModel):
    location: "LocationSummary"
    forecasts: list[ForecastDayOut]
    summary: "MonthlySummary"
    generated_at: datetime


class MonthlySummary(BaseModel):
    avg_temp_min: float
    avg_temp_max: float
    total_precipitation: float
    avg_rain_probability: float
    dominant_condition: str


# ── History & Comparison ─────────────────────────────────────────────────────

class HistoryOut(BaseModel):
    location: "LocationSummary"
    observations: list[WeatherObservationOut]
    period_start: date
    period_end: date


class PeriodStats(BaseModel):
    period: str
    avg_temperature: float
    avg_humidity: float
    total_precipitation: float
    rain_days: int


class ComparisonOut(BaseModel):
    location: "LocationSummary"
    period_a: PeriodStats
    period_b: PeriodStats
    delta_temperature: float
    delta_precipitation: float


# ── Alerts ───────────────────────────────────────────────────────────────────

class WeatherAlertOut(BaseModel):
    id: int
    location_id: Optional[int] = None
    alert_type: str
    severity: str
    title: str
    description: str
    source: str
    issued_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool

    model_config = {"from_attributes": True}


# ── Helpers ──────────────────────────────────────────────────────────────────

class LocationSummary(BaseModel):
    id: int
    city: str
    province: str
    latitude: float
    longitude: float

    model_config = {"from_attributes": True}


# Rebuild forward references
CurrentWeatherOut.model_rebuild()
WeeklyForecastOut.model_rebuild()
MonthlyOutlookOut.model_rebuild()
HistoryOut.model_rebuild()
ComparisonOut.model_rebuild()
