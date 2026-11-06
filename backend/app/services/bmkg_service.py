"""BMKG (Badan Meteorologi, Klimatologi, dan Geofisika) data integration.

Fetches XML forecast data from BMKG's public endpoint, parses it, and stores
weather forecasts in the database.
"""
from __future__ import annotations

import logging
import xml.etree.ElementTree as ET
from datetime import datetime, date, timezone
from typing import Any

import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.forecast import WeatherForecast
from app.models.location import Location

logger = logging.getLogger(__name__)
settings = get_settings()

# ── BMKG weather code → human-readable mapping ──────────────────────────────
BMKG_WEATHER_CODES: dict[int, tuple[str, str]] = {
    0:  ("Cerah", "clear"),
    1:  ("Cerah Berawan", "mostly_clear"),
    2:  ("Cerah Berawan", "partly_cloudy"),
    3:  ("Berawan", "cloudy"),
    4:  ("Berawan Tebal", "overcast"),
    5:  ("Udara Kabur", "haze"),
    10: ("Asap", "smoke"),
    45: ("Kabut", "fog"),
    60: ("Hujan Ringan", "light_rain"),
    61: ("Hujan Sedang", "rain"),
    63: ("Hujan Lebat", "heavy_rain"),
    80: ("Hujan Lokal", "isolated_shower"),
    95: ("Hujan Petir", "thunderstorm"),
    97: ("Hujan Petir", "thunderstorm"),
}

# Province name → BMKG XML province code
PROVINCE_TO_BMKG: dict[str, str] = {
    "Jawa Timur": "JawaTimur",
    "DKI Jakarta": "DKIJakarta",
    "Jawa Barat": "JawaBarat",
    "DI Yogyakarta": "DIYogyakarta",
    "Jawa Tengah": "JawaTengah",
    "Sumatera Utara": "SumateraUtara",
    "Sulawesi Selatan": "SulawesiSelatan",
    "Sumatera Selatan": "SumateraSelatan",
    "Bali": "Bali",
    "Kalimantan Timur": "KalimantanTimur",
    "Sulawesi Utara": "SulawesiUtara",
    "Sumatera Barat": "SumateraBarat",
    "Kalimantan Barat": "KalimantanBarat",
    "Kalimantan Selatan": "KalimantanSelatan",
    "Kepulauan Riau": "KepulauanRiau",
    "Riau": "Riau",
    "Lampung": "Lampung",
    "Nusa Tenggara Barat": "NusaTenggaraBarat",
    "Nusa Tenggara Timur": "NusaTenggaraTimur",
    "Maluku": "Maluku",
    "Papua": "Papua",
}

# In-memory cache for raw XML data, keyed by province code
_xml_cache: dict[str, tuple[datetime, str]] = {}
_CACHE_TTL_SECONDS = 3600  # 1 hour


class BMKGService:
    """Service for fetching and parsing BMKG weather forecast data."""

    def __init__(self) -> None:
        self.base_url = settings.BMKG_BASE_URL

    # ── Public API ───────────────────────────────────────────────────────

    async def refresh_bmkg_data(
        self, session: AsyncSession, province: str | None = None
    ) -> dict[str, Any]:
        """Fetch fresh BMKG data for one or all provinces, parse & store.

        Returns a summary dict with counts.
        """
        provinces = [province] if province else list(PROVINCE_TO_BMKG.values())
        total_stored = 0
        errors: list[str] = []

        for prov_code in provinces:
            try:
                xml_text = await self._fetch_xml(prov_code)
                if xml_text:
                    count = await self._parse_and_store(session, xml_text, prov_code)
                    total_stored += count
            except Exception as exc:
                msg = f"Error processing {prov_code}: {exc}"
                logger.error(msg)
                errors.append(msg)

        await session.commit()
        return {
            "provinces_processed": len(provinces),
            "forecasts_stored": total_stored,
            "errors": errors,
        }

    async def fetch_province_forecast(
        self, province_code: str
    ) -> list[dict[str, Any]]:
        """Fetch & parse BMKG data for a single province (no DB write)."""
        xml_text = await self._fetch_xml(province_code)
        if not xml_text:
            return []
        return self._parse_xml(xml_text)

    # ── Private helpers ──────────────────────────────────────────────────

    async def _fetch_xml(self, province_code: str) -> str | None:
        """Download XML from BMKG, with caching and error handling."""
        # Check cache
        now = datetime.now(timezone.utc)
        if province_code in _xml_cache:
            cached_at, cached_text = _xml_cache[province_code]
            age = (now - cached_at).total_seconds()
            if age < _CACHE_TTL_SECONDS:
                logger.debug("Using cached BMKG data for %s (age %ds).", province_code, int(age))
                return cached_text

        url = f"{self.base_url}/DigitalForecast-{province_code}.xml"
        logger.info("Fetching BMKG data: %s", url)

        try:
            async with aiohttp.ClientSession() as http:
                async with http.get(url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                    if resp.status != 200:
                        logger.warning(
                            "BMKG returned HTTP %d for %s", resp.status, province_code
                        )
                        # Fall back to cache even if expired
                        if province_code in _xml_cache:
                            logger.info("Falling back to expired cache for %s.", province_code)
                            return _xml_cache[province_code][1]
                        return None
                    text = await resp.text()
                    _xml_cache[province_code] = (now, text)
                    return text
        except Exception as exc:
            logger.error("Network error fetching BMKG %s: %s", province_code, exc)
            # Fallback to stale cache
            if province_code in _xml_cache:
                logger.info("Falling back to stale cache for %s.", province_code)
                return _xml_cache[province_code][1]
            return None

    def _parse_xml(self, xml_text: str) -> list[dict[str, Any]]:
        """Parse BMKG XML into a list of forecast dicts."""
        results: list[dict[str, Any]] = []
        try:
            root = ET.fromstring(xml_text)
        except ET.ParseError as exc:
            logger.error("Failed to parse BMKG XML: %s", exc)
            return results

        forecast_el = root.find("forecast")
        if forecast_el is None:
            # Try alternative structure
            forecast_el = root

        for area in forecast_el.findall(".//area"):
            area_id = area.get("id", "")
            area_name = ""
            for name_el in area.findall("name"):
                if name_el.get("xml:lang") == "en" or name_el.get("lang") == "en":
                    area_name = name_el.text or ""
                elif not area_name:
                    area_name = name_el.text or ""

            lat = area.get("latitude", "0")
            lon = area.get("longitude", "0")

            # Collect parameters by type
            params: dict[str, dict[str, Any]] = {}
            for param in area.findall("parameter"):
                param_id = param.get("id", "")
                for timerange in param.findall("timerange"):
                    dt_str = timerange.get("datetime", "")
                    tr_type = timerange.get("type", "")
                    value_el = timerange.find("value")
                    value = value_el.text if value_el is not None else None

                    key = f"{dt_str}_{tr_type}"
                    if key not in params:
                        params[key] = {"datetime": dt_str, "type": tr_type}
                    params[key][param_id] = value

            for key, p in params.items():
                # Build a forecast record
                weather_code = int(p.get("weather", "0") or "0")
                condition, condition_code = BMKG_WEATHER_CODES.get(
                    weather_code, ("Tidak Diketahui", "unknown")
                )

                record: dict[str, Any] = {
                    "area_id": area_id,
                    "area_name": area_name,
                    "latitude": float(lat) if lat else 0.0,
                    "longitude": float(lon) if lon else 0.0,
                    "datetime": p.get("datetime", ""),
                    "temperature": self._safe_float(p.get("t")),
                    "temperature_min": self._safe_float(p.get("tmin")),
                    "temperature_max": self._safe_float(p.get("tmax")),
                    "humidity": self._safe_float(p.get("hu")),
                    "wind_speed": self._safe_float(p.get("ws")),
                    "wind_direction": self._safe_float(p.get("wd")),
                    "weather_code": weather_code,
                    "condition": condition,
                    "condition_code": condition_code,
                    "cloud_cover": self._safe_float(p.get("cc"), 0.0),
                }
                results.append(record)

        return results

    async def _parse_and_store(
        self, session: AsyncSession, xml_text: str, province_code: str
    ) -> int:
        """Parse XML and persist forecasts linked to known locations."""
        records = self._parse_xml(xml_text)
        if not records:
            return 0

        # Load locations for this province
        province_name = next(
            (k for k, v in PROVINCE_TO_BMKG.items() if v == province_code),
            None,
        )
        if not province_name:
            return 0

        result = await session.execute(
            select(Location).where(Location.province == province_name)
        )
        locations = {loc.city.lower(): loc for loc in result.scalars().all()}

        if not locations:
            return 0

        today = date.today()
        stored = 0

        for rec in records:
            # Try to match area_name to a known city
            area_lower = rec["area_name"].lower()
            loc = locations.get(area_lower)
            if loc is None:
                # Try partial match
                for city_lower, city_loc in locations.items():
                    if city_lower in area_lower or area_lower in city_lower:
                        loc = city_loc
                        break
            if loc is None:
                continue

            # Parse the datetime string (format: 202611060000)
            dt_str = rec.get("datetime", "")
            try:
                forecast_dt = datetime.strptime(dt_str[:8], "%Y%m%d").date()
            except (ValueError, IndexError):
                forecast_dt = today

            horizon = (forecast_dt - today).days
            if horizon < 0:
                continue

            temp = rec.get("temperature") or 28.0
            temp_min = rec.get("temperature_min") or temp - 3
            temp_max = rec.get("temperature_max") or temp + 3
            humidity = rec.get("humidity") or 75.0
            rain_prob = 70.0 if "hujan" in rec["condition"].lower() else 20.0

            fc = WeatherForecast(
                location_id=loc.id,
                forecast_date=forecast_dt,
                model_name="bmkg",
                model_version="digital-forecast",
                forecast_horizon_days=max(horizon, 1),
                temperature_min=temp_min,
                temperature_max=temp_max,
                rain_probability=rain_prob,
                precipitation_estimate=0.0,
                humidity=humidity,
                wind_speed=rec.get("wind_speed") or 10.0,
                wind_direction=rec.get("wind_direction") or 0.0,
                cloud_cover=rec.get("cloud_cover") or 50.0,
                uv_index=None,
                condition=rec["condition"],
                condition_code=rec["condition_code"],
                confidence_score=0.85,
                raw_data=rec,
            )
            session.add(fc)
            stored += 1

        await session.flush()
        logger.info("Stored %d BMKG forecasts for %s.", stored, province_code)
        return stored

    @staticmethod
    def _safe_float(val: Any, default: float | None = None) -> float | None:
        """Convert a value to float, returning *default* on failure."""
        if val is None:
            return default
        try:
            return float(val)
        except (ValueError, TypeError):
            return default
