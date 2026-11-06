"""Mock WeatherNext3 AI forecast service.

Generates realistic-looking short-range (1-15 day) weather forecasts
for Indonesian cities. Will be replaced with real model inference in Phase 2.
"""
from __future__ import annotations

import math
import random
from datetime import date, datetime, timedelta, timezone
from typing import Any

from app.seed import CONDITIONS


class MockWeatherNextService:
    """Simulates WeatherNext3 short-range weather predictions (1-15 days)."""

    MODEL_NAME = "weathernext3"
    MODEL_VERSION = "1.0.0-mock"

    def generate_forecast(
        self,
        latitude: float,
        longitude: float,
        city: str,
        days: int = 15,
        base_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """Generate mock forecast data for *days* ahead.

        Parameters
        ----------
        latitude, longitude : float
            Location coordinates.
        city : str
            City name (used for slight regional variation).
        days : int
            Number of forecast days (1–15).
        base_date : date | None
            Starting date; defaults to today.

        Returns
        -------
        list[dict]
            One dict per forecast day.
        """
        base = base_date or date.today()
        forecasts: list[dict[str, Any]] = []
        days = min(days, 15)

        # Regional base temperature adjustment
        base_temp = self._base_temp_for_location(latitude)

        for horizon in range(1, days + 1):
            forecast_dt = base + timedelta(days=horizon)
            rain_prob = self._seasonal_rain_probability(forecast_dt)

            temp_min, temp_max = self._generate_temperatures(
                forecast_dt, base_temp, horizon
            )
            condition, condition_code = self._pick_condition(rain_prob)
            confidence = self._confidence_score(horizon)

            forecasts.append({
                "forecast_date": forecast_dt.isoformat(),
                "model_name": self.MODEL_NAME,
                "model_version": self.MODEL_VERSION,
                "forecast_horizon_days": horizon,
                "temperature_min": temp_min,
                "temperature_max": temp_max,
                "rain_probability": round(rain_prob, 1),
                "precipitation_estimate": self._estimate_precipitation(rain_prob),
                "humidity": round(random.uniform(60, 92), 1),
                "wind_speed": round(random.uniform(5, 30), 1),
                "wind_direction": round(random.uniform(0, 360), 0),
                "cloud_cover": round(random.uniform(15, 90), 1),
                "uv_index": round(random.uniform(4, 11), 1),
                "condition": condition,
                "condition_code": condition_code,
                "confidence_score": confidence,
                "uncertainty_low": round(temp_min - horizon * 0.25, 1),
                "uncertainty_high": round(temp_max + horizon * 0.25, 1),
                "ensemble_members": 10,
            })

        return forecasts

    # ── Helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _base_temp_for_location(latitude: float) -> float:
        """Higher-altitude / higher-latitude cities are slightly cooler."""
        # Near equator → warmer; Java/Bali (−7 to −8) → typical 29°C
        abs_lat = abs(latitude)
        if abs_lat > 8:
            return 27.5
        elif abs_lat > 5:
            return 28.5
        else:
            return 29.5

    @staticmethod
    def _seasonal_rain_probability(dt: date) -> float:
        """Indonesian monsoon-based rain probability."""
        month = dt.month
        if month in (12, 1, 2):
            return random.uniform(60, 90)
        elif month in (11, 3):
            return random.uniform(50, 75)
        elif month in (4, 10):
            return random.uniform(35, 60)
        elif month in (5, 9):
            return random.uniform(20, 45)
        else:
            return random.uniform(10, 35)

    @staticmethod
    def _generate_temperatures(
        dt: date, base: float, horizon: int
    ) -> tuple[float, float]:
        seasonal = 1.2 * math.sin(2 * math.pi * (dt.month - 1) / 12)
        noise = random.gauss(0, 0.8 + horizon * 0.1)
        mid = base + seasonal + noise
        spread = random.uniform(3, 6)
        return round(mid - spread / 2, 1), round(mid + spread / 2, 1)

    @staticmethod
    def _pick_condition(rain_prob: float) -> tuple[str, str]:
        if rain_prob < 20:
            return random.choice(CONDITIONS[:2])
        elif rain_prob < 50:
            return random.choice(CONDITIONS[1:4])
        elif rain_prob < 75:
            return random.choice(CONDITIONS[4:6])
        else:
            return random.choice(CONDITIONS[5:])

    @staticmethod
    def _estimate_precipitation(rain_prob: float) -> float:
        if rain_prob < 20:
            return round(random.uniform(0, 1), 1)
        elif rain_prob < 50:
            return round(random.uniform(0, 5), 1)
        elif rain_prob < 75:
            return round(random.uniform(2, 15), 1)
        else:
            return round(random.uniform(8, 40), 1)

    @staticmethod
    def _confidence_score(horizon: int) -> float:
        """Confidence decreases with forecast horizon."""
        base = 0.95 - horizon * 0.035
        return round(max(0.35, base + random.gauss(0, 0.02)), 2)
