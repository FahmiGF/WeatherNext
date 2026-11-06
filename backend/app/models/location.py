"""Location model — Indonesian cities and weather stations."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Float, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    province: Mapped[str] = mapped_column(String(100), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False, default="Indonesia")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False, default="Asia/Jakarta")
    bmkg_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    observations = relationship("WeatherObservation", back_populates="location", lazy="selectin")
    forecasts = relationship("WeatherForecast", back_populates="location", lazy="selectin")
    alerts = relationship("WeatherAlert", back_populates="location", lazy="selectin")
    accuracy_records = relationship("ForecastAccuracy", back_populates="location", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Location(id={self.id}, city={self.city!r}, province={self.province!r})>"
