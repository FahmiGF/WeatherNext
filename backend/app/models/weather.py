"""Weather observation model — actual / recorded weather data."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    String, Float, Integer, DateTime, ForeignKey, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class WeatherObservation(Base):
    __tablename__ = "weather_observations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=False
    )
    observed_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    temperature_min: Mapped[float | None] = mapped_column(Float, nullable=True)
    temperature_max: Mapped[float | None] = mapped_column(Float, nullable=True)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)
    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)
    wind_direction: Mapped[float] = mapped_column(Float, nullable=False)
    precipitation: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cloud_cover: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pressure: Mapped[float | None] = mapped_column(Float, nullable=True)
    uv_index: Mapped[float | None] = mapped_column(Float, nullable=True)
    condition: Mapped[str] = mapped_column(String(50), nullable=False)
    condition_code: Mapped[str] = mapped_column(String(30), nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="observation")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Relationships
    location = relationship("Location", back_populates="observations")

    def __repr__(self) -> str:
        return (
            f"<WeatherObservation(id={self.id}, location_id={self.location_id}, "
            f"observed_at={self.observed_at}, temp={self.temperature}°C)>"
        )
