"""Mock TimesFM3 time-series forecast service.

Generates long-range (16-30 day) probabilistic weather outlooks with
quantile predictions, simulating seasonal patterns for Indonesian climate.
"""
from __future__ import annotations

import math
import random
from datetime import date, timedelta
from typing import Any

from app.seed import CONDITIONS


class MockTimesFMService:
    """Simulates TimesFM3 extended-range time-series predictions (16-30 days)."""

    MODEL_NAME = "timesfm3"
    MODEL_VERSION = "1.0.0-mock"

    def generate_forecast(
        self,
        latitude: float,
        longitude: float,
        city: str,
        start_day: int = 16,
        end_day: int = 30,
        base_date: date | None = None,
    ) -> list[dict[str, Any]]:
        """Generate probabilistic long-range forecast.

        Parameters
        ----------
        latitude, longitude : float
            Location coordinates.
        city : str
            City name.
        start_day, end_day : int
            Horizon range (defaults 16-30).
        base_date : date | None
            Starting date; defaults to today.

        Returns
        -------
        list[dict]
            One dict per day with quantile data.
        """
        base = base_date or date.today()
        forecasts: list[dict[str, Any]] = []
        base_temp = self._base_temp(latitude)

        for horizon in range(start_day, end_day + 1):
            forecast_dt = base + timedelta(days=horizon)
            rain_prob = self._seasonal_rain_probability(forecast_dt)
            temp_mid = self._mid_temperature(forecast_dt, base_temp, horizon)

            quantiles = self._generate_quantiles(temp_mid, horizon)
            condition, condition_code = self._pick_condition(rain_prob)
            confidence = round(max(0.15, 0.6 - (horizon - 16) * 0.025 + random.gauss(0, 0.02)), 2)

            forecasts.append({
                "forecast_date": forecast_dt.isoformat(),
                "model_name": self.MODEL_NAME,
                "model_version": self.MODEL_VERSION,
                "forecast_horizon_days": horizon,
                "temperature_min": quantiles["p25"],
                "temperature_max": quantiles["p75"],
                "rain_probability": round(rain_prob, 1),
                "precipitation_estimate": self._estimate_precipitation(rain_prob),
                "humidity": round(random.uniform(60, 92), 1),
                "wind_speed": round(random.uniform(5, 25), 1),
                "wind_direction": round(random.uniform(0, 360), 0),
                "cloud_cover": round(random.uniform(20, 85), 1),
                "uv_index": round(random.uniform(4, 10), 1),
                "condition": condition,
                "condition_code": condition_code,
                "confidence_score": confidence,
                "uncertainty_low": quantiles["p10"],
                "uncertainty_high": quantiles["p90"],
                "ensemble_members": 50,
                "quantiles": quantiles,
            })

        return forecasts

    # ── Helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _base_temp(latitude: float) -> float:
        abs_lat = abs(latitude)
        if abs_lat > 8:
            return 27.0
        elif abs_lat > 5:
            return 28.0
        else:
            return 29.0

    @staticmethod
    def _seasonal_rain_probability(dt: date) -> float:
        month = dt.month
        if month in (12, 1, 2):
            return random.uniform(55, 85)
        elif month in (11, 3):
            return random.uniform(45, 70)
        elif month in (4, 10):
            return random.uniform(30, 55)
        else:
            return random.uniform(15, 40)

    @staticmethod
    def _mid_temperature(dt: date, base: float, horizon: int) -> float:
        seasonal = 1.5 * math.sin(2 * math.pi * (dt.month - 1) / 12)
        noise = random.gauss(0, 1.0 + horizon * 0.05)
        return round(base + seasonal + noise, 1)

    @staticmethod
    def _generate_quantiles(mid: float, horizon: int) -> dict[str, float]:
        """Generate percentile-based temperature spread."""
        spread_factor = 1.0 + (horizon - 16) * 0.15
        return {
            "p10": round(mid - 4.0 * spread_factor, 1),
            "p25": round(mid - 2.5 * spread_factor, 1),
            "p50": round(mid, 1),
            "p75": round(mid + 2.5 * spread_factor, 1),
            "p90": round(mid + 4.0 * spread_factor, 1),
        }

    @staticmethod
    def _pick_condition(rain_prob: float) -> tuple[str, str]:
        if rain_prob < 25:
            return random.choice(CONDITIONS[:2])
        elif rain_prob < 55:
            return random.choice(CONDITIONS[1:4])
        elif rain_prob < 75:
            return random.choice(CONDITIONS[4:6])
        else:
            return random.choice(CONDITIONS[5:])

    @staticmethod
    def _estimate_precipitation(rain_prob: float) -> float:
        if rain_prob < 25:
            return round(random.uniform(0, 2), 1)
        elif rain_prob < 55:
            return round(random.uniform(1, 8), 1)
        elif rain_prob < 75:
            return round(random.uniform(5, 20), 1)
        else:
            return round(random.uniform(10, 45), 1)
