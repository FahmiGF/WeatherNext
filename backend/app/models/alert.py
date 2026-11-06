"""Weather alert model."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    String, Integer, DateTime, ForeignKey, Boolean, Text, JSON, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class WeatherAlert(Base):
    __tablename__ = "weather_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    location_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("locations.id"), nullable=True
    )
    alert_type: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(30), nullable=False, default="system")
    issued_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    raw_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    location = relationship("Location", back_populates="alerts")

    def __repr__(self) -> str:
        return (
            f"<WeatherAlert(id={self.id}, type={self.alert_type!r}, "
            f"severity={self.severity!r})>"
        )
