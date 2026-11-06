"""Open-Meteo Weather API Integration Service.

Provides real-time observations, 7-day daily forecasts, and 16-day extended
forecasts without requiring any API keys.
"""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta, timezone
from typing import Any

import aiohttp

logger = logging.getLogger(__name__)

# WMO Weather interpretation codes (WW)
WMO_CODE_MAP: dict[int, tuple[str, str]] = {
    0: ("Cerah", "clear"),
    1: ("Sebagian Besar Cerah", "mostly_clear"),
    2: ("Cerah Berawan", "partly_cloudy"),
    3: ("Berawan", "cloudy"),
    45: ("Berkabut", "fog"),
    48: ("Kabut Embun", "fog"),
    51: ("Gerimis Ringan", "drizzle"),
    53: ("Gerimis Sedang", "drizzle"),
    55: ("Gerimis Lebat", "drizzle"),
    61: ("Hujan Ringan", "light_rain"),
    63: ("Hujan Sedang", "rain"),
    65: ("Hujan Lebat", "heavy_rain"),
    80: ("Hujan Rintik Lokal", "showers"),
    81: ("Hujan Sedang Lokal", "showers"),
    82: ("Hujan Deras Lokal", "heavy_showers"),
    95: ("Hujan Petir", "thunderstorm"),
    96: ("Hujan Petir & Es Ringan", "thunderstorm"),
    99: ("Hujan Petir & Es Lebat", "severe_thunderstorm"),
}


class OpenMeteoService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout: int = 8) -> None:
        self.timeout = timeout

    def _map_wmo(self, code: int | None) -> tuple[str, str]:
        if code is None:
            return ("Cerah Berawan", "partly_cloudy")
        return WMO_CODE_MAP.get(code, ("Berawan", "cloudy"))

    async def fetch_weather_and_forecast(
        self,
        latitude: float,
        longitude: float,
        days: int = 14,
    ) -> dict[str, Any] | None:
        """Fetch current weather and daily forecasts from Open-Meteo."""
        forecast_days = min(max(days, 7), 16)
        params = {
            "latitude": str(latitude),
            "longitude": str(longitude),
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,cloud_cover,surface_pressure",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,precipitation_sum,wind_speed_10m_max,wind_direction_10m_dominant,uv_index_max",
            "timezone": "auto",
            "forecast_days": str(forecast_days),
        }

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(self.BASE_URL, params=params) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    logger.warning("Open-Meteo returned status %d", resp.status)
                    return None
        except Exception as exc:
            logger.warning("Failed to reach Open-Meteo: %s", exc)
            return None

    def parse_current(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Convert Open-Meteo current object into observation dictionary."""
        cur = raw_data.get("current", {})
        code = cur.get("weather_code")
        cond, cond_code = self._map_wmo(code)

        return {
            "temperature": float(cur.get("temperature_2m", 30.0)),
            "feels_like": float(cur.get("apparent_temperature", cur.get("temperature_2m", 30.0))),
            "humidity": float(cur.get("relative_humidity_2m", 70.0)),
            "precipitation": float(cur.get("precipitation", 0.0)),
            "wind_speed": float(cur.get("wind_speed_10m", 10.0)),
            "wind_direction": float(cur.get("wind_direction_10m", 0.0)),
            "cloud_cover": float(cur.get("cloud_cover", 40.0)),
            "pressure": float(cur.get("surface_pressure", 1010.0)),
            "condition": cond,
            "condition_code": cond_code,
            "observed_at": datetime.now(timezone.utc),
            "source": "open-meteo",
        }

    def parse_forecast(self, raw_data: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse daily forecasts into our standard schema list."""
        daily = raw_data.get("daily", {})
        times = daily.get("time", [])
        codes = daily.get("weather_code", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        rain_probs = daily.get("precipitation_probability_max", [])
        precips = daily.get("precipitation_sum", [])
        wind_speeds = daily.get("wind_speed_10m_max", [])
        wind_dirs = daily.get("wind_direction_10m_dominant", [])
        uvs = daily.get("uv_index_max", [])

        forecasts = []
        for i in range(len(times)):
            d_str = times[i]
            d = date.fromisoformat(d_str)
            cond, cond_code = self._map_wmo(codes[i] if i < len(codes) else None)
            horizon = (d - date.today()).days

            forecasts.append({
                "forecast_date": d,
                "forecast_horizon_days": max(horizon, 1),
                "model_name": "Open-Meteo Forecast",
                "model_version": "v1.0",
                "temperature_min": float(min_temps[i]) if i < len(min_temps) else 24.0,
                "temperature_max": float(max_temps[i]) if i < len(max_temps) else 32.0,
                "rain_probability": float(rain_probs[i]) if i < len(rain_probs) and rain_probs[i] is not None else 30.0,
                "precipitation_estimate": float(precips[i]) if i < len(precips) and precips[i] is not None else 1.0,
                "humidity": 75.0,
                "wind_speed": float(wind_speeds[i]) if i < len(wind_speeds) and wind_speeds[i] is not None else 12.0,
                "wind_direction": float(wind_dirs[i]) if i < len(wind_dirs) and wind_dirs[i] is not None else 120.0,
                "cloud_cover": 50.0,
                "uv_index": float(uvs[i]) if i < len(uvs) and uvs[i] is not None else 7.5,
                "condition": cond,
                "condition_code": cond_code,
                "confidence_score": round(max(0.4, 0.95 - (horizon * 0.04)), 2),
                "uncertainty_low": round(min_temps[i] - 1.0, 1) if i < len(min_temps) else 23.0,
                "uncertainty_high": round(max_temps[i] + 1.0, 1) if i < len(max_temps) else 33.0,
            })

        return forecasts
