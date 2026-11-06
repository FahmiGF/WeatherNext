"""Hybrid forecast engine — combines WeatherNext3 (1-15 days) and TimesFM3 (16-30 days).

Applies simple ensemble weighting and produces a unified 30-day forecast.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timezone
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.forecast import WeatherForecast, ForecastRun
from app.models.location import Location
from app.services.weathernext_service import MockWeatherNextService
from app.services.timesfm_service import MockTimesFMService

logger = logging.getLogger(__name__)


class HybridForecastEngine:
    """Blends short-range and long-range forecasts into a unified 30-day view."""

    MODEL_NAME = "hybrid"
    MODEL_VERSION = "1.0.0"

    def __init__(self) -> None:
        self.weathernext = MockWeatherNextService()
        self.timesfm = MockTimesFMService()

    async def generate_full_forecast(
        self,
        location: Location,
        days: int = 30,
        base_date: date | None = None,
        session: AsyncSession | None = None,
    ) -> list[dict[str, Any]]:
        """Generate a combined 30-day forecast for a location.

        Days 1-15 → WeatherNext3
        Days 16-30 → TimesFM3
        Returns merged + weighted list.
        """
        base = base_date or date.today()

        short_days = min(days, 15)
        short_range = self.weathernext.generate_forecast(
            latitude=location.latitude,
            longitude=location.longitude,
            city=location.city,
            days=short_days,
            base_date=base,
        )

        long_range: list[dict[str, Any]] = []
        if days > 15:
            long_range = self.timesfm.generate_forecast(
                latitude=location.latitude,
                longitude=location.longitude,
                city=location.city,
                start_day=16,
                end_day=min(days, 30),
                base_date=base,
            )

        # Apply ensemble weighting
        combined = self._apply_weights(short_range, long_range)

        # Optionally persist
        if session is not None:
            await self._store_forecasts(session, location, combined)

        return combined

    async def run_batch_forecast(
        self,
        session: AsyncSession,
        locations: list[Location],
        days: int = 30,
    ) -> ForecastRun:
        """Run forecasts for multiple locations and record the run."""
        run = ForecastRun(
            model_name=self.MODEL_NAME,
            model_version=self.MODEL_VERSION,
            run_started_at=datetime.now(timezone.utc),
            status="running",
        )
        session.add(run)
        await session.flush()

        try:
            for loc in locations:
                await self.generate_full_forecast(
                    location=loc, days=days, session=session
                )
                run.locations_processed += 1

            run.status = "completed"
            run.run_completed_at = datetime.now(timezone.utc)
        except Exception as exc:
            run.status = "failed"
            run.error_message = str(exc)[:500]
            logger.error("Batch forecast failed: %s", exc)

        await session.flush()
        return run

    # ── Private helpers ──────────────────────────────────────────────────

    def _apply_weights(
        self,
        short_range: list[dict[str, Any]],
        long_range: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Merge and relabel both ranges under the hybrid model."""
        combined: list[dict[str, Any]] = []

        for fc in short_range:
            fc["model_name"] = self.MODEL_NAME
            fc["model_version"] = self.MODEL_VERSION
            fc["source_model"] = "weathernext3"
            combined.append(fc)

        for fc in long_range:
            fc["model_name"] = self.MODEL_NAME
            fc["model_version"] = self.MODEL_VERSION
            fc["source_model"] = "timesfm3"
            # Slightly reduce confidence for blended long-range
            if fc.get("confidence_score"):
                fc["confidence_score"] = round(fc["confidence_score"] * 0.92, 2)
            combined.append(fc)

        return combined

    async def _store_forecasts(
        self,
        session: AsyncSession,
        location: Location,
        forecasts: list[dict[str, Any]],
    ) -> int:
        """Persist forecast dicts to the database."""
        stored = 0
        for fc_data in forecasts:
            forecast_date = fc_data.get("forecast_date")
            if isinstance(forecast_date, str):
                forecast_date = date.fromisoformat(forecast_date)

            fc = WeatherForecast(
                location_id=location.id,
                forecast_date=forecast_date,
                model_name=fc_data["model_name"],
                model_version=fc_data.get("model_version"),
                forecast_horizon_days=fc_data["forecast_horizon_days"],
                temperature_min=fc_data["temperature_min"],
                temperature_max=fc_data["temperature_max"],
                rain_probability=fc_data["rain_probability"],
                precipitation_estimate=fc_data.get("precipitation_estimate", 0.0),
                humidity=fc_data["humidity"],
                wind_speed=fc_data["wind_speed"],
                wind_direction=fc_data["wind_direction"],
                cloud_cover=fc_data["cloud_cover"],
                uv_index=fc_data.get("uv_index"),
                condition=fc_data["condition"],
                condition_code=fc_data["condition_code"],
                confidence_score=fc_data.get("confidence_score"),
                uncertainty_low=fc_data.get("uncertainty_low"),
                uncertainty_high=fc_data.get("uncertainty_high"),
                ensemble_members=fc_data.get("ensemble_members"),
                raw_data=fc_data,
            )
            session.add(fc)
            stored += 1

        await session.flush()
        return stored
