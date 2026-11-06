"""Seed data — Indonesian cities, mock observations, and mock forecasts."""
from __future__ import annotations

import logging
import math
import random
from datetime import datetime, timedelta, date, timezone

from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.location import Location
from app.models.weather import WeatherObservation
from app.models.forecast import WeatherForecast

logger = logging.getLogger(__name__)

# ── BMKG Province Codes ──────────────────────────────────────────────────────
CITIES: list[dict] = [
    {"city": "Surabaya",     "province": "Jawa Timur",         "lat": -7.2575,  "lon": 112.7521, "tz": "Asia/Jakarta",    "bmkg": "501492"},
    {"city": "Jakarta",      "province": "DKI Jakarta",        "lat": -6.2088,  "lon": 106.8456, "tz": "Asia/Jakarta",    "bmkg": "501162"},
    {"city": "Bandung",      "province": "Jawa Barat",         "lat": -6.9175,  "lon": 107.6191, "tz": "Asia/Jakarta",    "bmkg": "501119"},
    {"city": "Yogyakarta",   "province": "DI Yogyakarta",      "lat": -7.7956,  "lon": 110.3695, "tz": "Asia/Jakarta",    "bmkg": "501340"},
    {"city": "Semarang",     "province": "Jawa Tengah",        "lat": -6.9667,  "lon": 110.4196, "tz": "Asia/Jakarta",    "bmkg": "501300"},
    {"city": "Medan",        "province": "Sumatera Utara",     "lat":  3.5952,  "lon":  98.6722, "tz": "Asia/Jakarta",    "bmkg": "501002"},
    {"city": "Makassar",     "province": "Sulawesi Selatan",   "lat": -5.1477,  "lon": 119.4327, "tz": "Asia/Makassar",   "bmkg": "501562"},
    {"city": "Palembang",    "province": "Sumatera Selatan",   "lat": -2.9761,  "lon": 104.7754, "tz": "Asia/Jakarta",    "bmkg": "501070"},
    {"city": "Denpasar",     "province": "Bali",               "lat": -8.6500,  "lon": 115.2167, "tz": "Asia/Makassar",   "bmkg": "501510"},
    {"city": "Malang",       "province": "Jawa Timur",         "lat": -7.9786,  "lon": 112.6304, "tz": "Asia/Jakarta",    "bmkg": "501487"},
    {"city": "Solo",         "province": "Jawa Tengah",        "lat": -7.5755,  "lon": 110.8243, "tz": "Asia/Jakarta",    "bmkg": "501313"},
    {"city": "Balikpapan",   "province": "Kalimantan Timur",   "lat": -1.2654,  "lon": 116.8311, "tz": "Asia/Makassar",   "bmkg": "501590"},
    {"city": "Manado",       "province": "Sulawesi Utara",     "lat":  1.4748,  "lon": 124.8421, "tz": "Asia/Makassar",   "bmkg": "501530"},
    {"city": "Padang",       "province": "Sumatera Barat",     "lat": -0.9471,  "lon": 100.4172, "tz": "Asia/Jakarta",    "bmkg": "501030"},
    {"city": "Pontianak",    "province": "Kalimantan Barat",   "lat": -0.0263,  "lon": 109.3425, "tz": "Asia/Jakarta",    "bmkg": "501570"},
    {"city": "Banjarmasin",  "province": "Kalimantan Selatan", "lat": -3.3186,  "lon": 114.5944, "tz": "Asia/Makassar",   "bmkg": "501580"},
    {"city": "Batam",        "province": "Kepulauan Riau",     "lat":  1.0456,  "lon": 104.0305, "tz": "Asia/Jakarta",    "bmkg": "501015"},
    {"city": "Pekanbaru",    "province": "Riau",               "lat":  0.5071,  "lon": 101.4478, "tz": "Asia/Jakarta",    "bmkg": "501020"},
    {"city": "Lampung",      "province": "Lampung",            "lat": -5.4500,  "lon": 105.2667, "tz": "Asia/Jakarta",    "bmkg": "501098"},
    {"city": "Mataram",      "province": "Nusa Tenggara Barat","lat": -8.5833,  "lon": 116.1167, "tz": "Asia/Makassar",   "bmkg": "501520"},
    {"city": "Kupang",       "province": "Nusa Tenggara Timur","lat": -10.1772, "lon": 123.6070, "tz": "Asia/Makassar",   "bmkg": "501525"},
    {"city": "Ambon",        "province": "Maluku",             "lat": -3.6954,  "lon": 128.1814, "tz": "Asia/Jayapura",   "bmkg": "501610"},
    {"city": "Jayapura",     "province": "Papua",              "lat": -2.5337,  "lon": 140.7181, "tz": "Asia/Jayapura",   "bmkg": "501640"},
]

# Province name → BMKG XML code mapping
PROVINCE_BMKG_CODES: dict[str, str] = {
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

# Condition helpers
CONDITIONS = [
    ("Cerah", "clear"),
    ("Cerah Berawan", "mostly_clear"),
    ("Berawan", "cloudy"),
    ("Berawan Tebal", "overcast"),
    ("Hujan Ringan", "light_rain"),
    ("Hujan Sedang", "rain"),
    ("Hujan Lebat", "heavy_rain"),
    ("Hujan Petir", "thunderstorm"),
]


def _random_condition(rain_prob: float) -> tuple[str, str]:
    """Pick a weather condition weighted by rain probability."""
    if rain_prob < 20:
        return random.choice(CONDITIONS[:2])
    elif rain_prob < 50:
        return random.choice(CONDITIONS[1:4])
    elif rain_prob < 75:
        return random.choice(CONDITIONS[4:6])
    else:
        return random.choice(CONDITIONS[5:])


def _seasonal_rain_prob(dt: datetime) -> float:
    """Return a base rain probability for Indonesian monsoon seasons.

    Nov–Mar → wet season (60-90%), Apr–Oct → dry season (20-50%).
    """
    month = dt.month
    if month in (11, 12, 1, 2, 3):
        return random.uniform(55, 90)
    elif month in (4, 10):
        return random.uniform(35, 65)
    else:
        return random.uniform(15, 45)


def _generate_temp(dt: datetime, base: float = 29.0) -> tuple[float, float, float]:
    """Generate realistic tropical temperatures with diurnal variation."""
    # Slight seasonal variation
    seasonal = 1.0 * math.sin(2 * math.pi * (dt.month - 1) / 12)
    daily_noise = random.gauss(0, 1.5)
    temp = base + seasonal + daily_noise
    temp_min = temp - random.uniform(3, 6)
    temp_max = temp + random.uniform(2, 5)
    return round(temp, 1), round(temp_min, 1), round(temp_max, 1)


async def seed_locations(session: AsyncSession) -> list[Location]:
    """Insert seed cities if the table is empty. Returns all locations."""
    count = (await session.execute(
        select(sa_func.count()).select_from(Location)
    )).scalar_one()

    if count > 0:
        result = await session.execute(select(Location))
        logger.info("Locations already seeded (%d rows).", count)
        return list(result.scalars().all())

    locations: list[Location] = []
    for c in CITIES:
        loc = Location(
            city=c["city"],
            province=c["province"],
            country="Indonesia",
            latitude=c["lat"],
            longitude=c["lon"],
            timezone=c["tz"],
            bmkg_code=c["bmkg"],
        )
        session.add(loc)
        locations.append(loc)

    await session.flush()
    logger.info("Seeded %d Indonesian cities.", len(locations))
    return locations


async def seed_observations(
    session: AsyncSession,
    location: Location,
    days: int = 30,
) -> None:
    """Generate mock historical observations for the given location."""
    count = (await session.execute(
        select(sa_func.count())
        .select_from(WeatherObservation)
        .where(WeatherObservation.location_id == location.id)
    )).scalar_one()

    if count > 0:
        logger.info("Observations already seeded for %s.", location.city)
        return

    now = datetime.now(timezone.utc)

    for day_offset in range(days, 0, -1):
        dt = now - timedelta(days=day_offset)
        rain_prob = _seasonal_rain_prob(dt)
        temp, temp_min, temp_max = _generate_temp(dt)
        condition, condition_code = _random_condition(rain_prob)
        precip = round(random.uniform(0, 15), 1) if rain_prob > 40 else round(random.uniform(0, 2), 1)

        obs = WeatherObservation(
            location_id=location.id,
            observed_at=dt.replace(hour=12, minute=0, second=0, microsecond=0),
            temperature=temp,
            temperature_min=temp_min,
            temperature_max=temp_max,
            humidity=round(random.uniform(60, 92), 1),
            wind_speed=round(random.uniform(5, 25), 1),
            wind_direction=round(random.uniform(0, 360), 0),
            precipitation=precip,
            cloud_cover=round(random.uniform(20, 90), 1),
            pressure=round(random.uniform(1005, 1015), 1),
            uv_index=round(random.uniform(4, 11), 1),
            condition=condition,
            condition_code=condition_code,
            source="observation",
        )
        session.add(obs)

    await session.flush()
    logger.info("Seeded %d days of observations for %s.", days, location.city)


async def seed_forecasts(
    session: AsyncSession,
    location: Location,
    days: int = 7,
) -> None:
    """Generate mock forecasts for the next *days* for the given location."""
    count = (await session.execute(
        select(sa_func.count())
        .select_from(WeatherForecast)
        .where(WeatherForecast.location_id == location.id)
    )).scalar_one()

    if count > 0:
        logger.info("Forecasts already seeded for %s.", location.city)
        return

    today = date.today()
    now = datetime.now(timezone.utc)

    for horizon in range(1, days + 1):
        forecast_dt = today + timedelta(days=horizon)
        rain_prob = _seasonal_rain_prob(datetime.combine(forecast_dt, datetime.min.time()))
        temp, temp_min, temp_max = _generate_temp(
            datetime.combine(forecast_dt, datetime.min.time())
        )
        condition, condition_code = _random_condition(rain_prob)
        confidence = round(max(0.3, 1.0 - (horizon * 0.08) + random.gauss(0, 0.03)), 2)

        fc = WeatherForecast(
            location_id=location.id,
            forecast_date=forecast_dt,
            created_at=now,
            model_name="hybrid",
            model_version="1.0.0-mock",
            forecast_horizon_days=horizon,
            temperature_min=temp_min,
            temperature_max=temp_max,
            rain_probability=round(rain_prob, 1),
            precipitation_estimate=round(random.uniform(0, 20), 1) if rain_prob > 40 else round(random.uniform(0, 3), 1),
            humidity=round(random.uniform(60, 92), 1),
            wind_speed=round(random.uniform(5, 25), 1),
            wind_direction=round(random.uniform(0, 360), 0),
            cloud_cover=round(random.uniform(20, 90), 1),
            uv_index=round(random.uniform(4, 11), 1),
            condition=condition,
            condition_code=condition_code,
            confidence_score=confidence,
            uncertainty_low=round(temp_min - horizon * 0.3, 1),
            uncertainty_high=round(temp_max + horizon * 0.3, 1),
            ensemble_members=10,
        )
        session.add(fc)

    await session.flush()
    logger.info("Seeded %d days of forecasts for %s.", days, location.city)


async def run_all_seeds(session: AsyncSession) -> None:
    """Master seed runner — locations, then observations & forecasts for Surabaya."""
    locations = await seed_locations(session)

    # Find Surabaya (primary city)
    surabaya = next((loc for loc in locations if loc.city == "Surabaya"), None)
    if surabaya:
        await seed_observations(session, surabaya, days=30)
        await seed_forecasts(session, surabaya, days=7)

    await session.commit()
    logger.info("All seed data populated.")
