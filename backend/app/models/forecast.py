"""Forecast models — predictions, runs, and accuracy tracking."""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    String, Float, Integer, DateTime, Date, ForeignKey, JSON, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    model_version: Mapped[str | None] = mapped_column(String(30), nullable=True)
    forecast_horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)

    # Weather parameters
    temperature_min: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_max: Mapped[float] = mapped_column(Float, nullable=False)
    rain_probability: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation_estimate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    wind_direction: Mapped[float] = mapped_column(Float, nullable=False)
    cloud_cover: Mapped[float] = mapped_column(Float, nullable=False)
    uv_index: Mapped[float | None] = mapped_column(Float, nullable=True)
    condition: Mapped[str] = mapped_column(String(50), nullable=False)
    condition_code: Mapped[str] = mapped_column(String(30), nullable=False)

    # Model confidence
    confidence_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    uncertainty_low: Mapped[float | None] = mapped_column(Float, nullable=True)
    uncertainty_high: Mapped[float | None] = mapped_column(Float, nullable=True)
    ensemble_members: Mapped[int | None] = mapped_column(Integer, nullable=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    location = relationship("Location", back_populates="forecasts")
    accuracy_records = relationship("ForecastAccuracy", back_populates="forecast", lazy="selectin")

    def __repr__(self) -> str:
        return (
            f"<WeatherForecast(id={self.id}, location_id={self.location_id}, "
            f"date={self.forecast_date}, model={self.model_name})>"
        )


class ForecastRun(Base):
    __tablename__ = "forecast_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)
    model_version: Mapped[str] = mapped_column(String(30), nullable=False)
    run_started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    run_completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="running"
    )
    locations_processed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    error_message: Mapped[str | None] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return (
            f"<ForecastRun(id={self.id}, model={self.model_name}, "
            f"status={self.status!r})>"
        )


class ForecastAccuracy(Base):
    __tablename__ = "forecast_accuracy"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    forecast_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("weather_forecasts.id"), nullable=False
    )
    observation_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("weather_observations.id"), nullable=True
    )
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    forecast_date: Mapped[date] = mapped_column(Date, nullable=False)
    horizon_days: Mapped[int] = mapped_column(Integer, nullable=False)
    model_name: Mapped[str] = mapped_column(String(50), nullable=False)

    # Accuracy metrics
    mae_temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    rmse_temperature: Mapped[float | None] = mapped_column(Float, nullable=True)
    brier_score_rain: Mapped[float | None] = mapped_column(Float, nullable=True)
    precipitation_error: Mapped[float | None] = mapped_column(Float, nullable=True)
    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    forecast = relationship("WeatherForecast", back_populates="accuracy_records")
    location = relationship("Location", back_populates="accuracy_records")

    def __repr__(self) -> str:
        return (
            f"<ForecastAccuracy(id={self.id}, model={self.model_name}, "
            f"mae={self.mae_temperature})>"
        )
