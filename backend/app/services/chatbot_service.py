"""Weather-focused chatbot — intent detection and response generation.

Uses keyword matching (no LLM) to detect weather intents and produces
natural-language responses in Bahasa Indonesia.
"""
from __future__ import annotations

import logging
import re
import uuid
from datetime import datetime, date, timedelta, timezone
from typing import Any

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat import ChatSession, ChatMessage
from app.models.location import Location
from app.models.weather import WeatherObservation
from app.models.forecast import WeatherForecast
from app.models.alert import WeatherAlert

logger = logging.getLogger(__name__)

# ── Intent definitions ───────────────────────────────────────────────────────
INTENT_PATTERNS: dict[str, list[str]] = {
    "current_weather": [
        r"cuaca\s+sekarang", r"cuaca\s+hari\s+ini", r"cuaca\s+saat\s+ini",
        r"current\s+weather", r"weather\s+now", r"hari\s+ini",
        r"suhu\s+sekarang", r"temperature\s+now",
    ],
    "tomorrow_forecast": [
        r"cuaca\s+besok", r"besok", r"tomorrow",
        r"prakiraan\s+besok", r"forecast\s+tomorrow",
    ],
    "weekly_forecast": [
        r"cuaca\s+7\s+hari", r"cuaca\s+minggu\s+ini", r"mingguan",
        r"7\s*day", r"weekly", r"seminggu",
        r"prakiraan\s+minggu",
    ],
    "monthly_outlook": [
        r"cuaca\s+30\s+hari", r"cuaca\s+bulanan", r"tren\s+cuaca",
        r"30\s*day", r"monthly", r"sebulan", r"outlook",
        r"prakiraan\s+bulan",
    ],
    "rain_check": [
        r"hujan", r"apakah\s+hujan", r"rain", r"will\s+it\s+rain",
        r"kemungkinan\s+hujan", r"probabilitas\s+hujan",
    ],
    "alerts": [
        r"peringatan", r"alert", r"warning", r"bahaya",
        r"cuaca\s+buruk", r"bencana", r"siaga",
    ],
    "historical": [
        r"sejarah", r"histori", r"history", r"data\s+lalu",
        r"kemarin", r"minggu\s+lalu", r"bulan\s+lalu",
    ],
    "comparison": [
        r"bandingkan", r"compare", r"perbandingan", r"versus", r"vs",
    ],
    "greeting": [
        r"^(halo|hai|hi|hello|hey|selamat\s+pagi|selamat\s+siang|"
        r"selamat\s+sore|selamat\s+malam)",
    ],
    "help": [
        r"^(help|bantuan|bantu|bisa\s+apa|fitur|menu)",
    ],
}

# City detection pattern — populated from database on first use
_city_cache: dict[str, int] = {}


class ChatbotService:
    """Keyword-based weather chatbot with Bahasa Indonesia responses."""

    async def handle_message(
        self,
        session: AsyncSession,
        session_id: str,
        message: str,
        location_hint: str | None = None,
    ) -> dict[str, Any]:
        """Process a user message and produce a structured response.

        Returns
        -------
        dict with keys: session_id, reply, intent, weather_data, suggestions
        """
        # 1. Ensure chat session exists
        chat_session = await self._get_or_create_session(session, session_id)

        # 2. Store user message
        await self._store_message(session, chat_session, "user", message)

        # 3. Detect intent
        intent = self._detect_intent(message)

        # 4. Detect location from message or hint
        location = await self._detect_location(session, message, location_hint)
        if location:
            chat_session.location_context = location.city

        # 5. Dispatch to handler
        reply, weather_data = await self._dispatch(
            session, intent, location, message
        )

        # 6. Build suggestions
        suggestions = self._build_suggestions(intent, location)

        # 7. Store assistant reply
        function_calls = {"intent": intent, "location": location.city if location else None}
        await self._store_message(
            session, chat_session, "assistant", reply, function_calls
        )

        await session.commit()

        return {
            "session_id": session_id,
            "reply": reply,
            "intent": intent,
            "weather_data": weather_data,
            "suggestions": suggestions,
        }

    # ── Intent detection ─────────────────────────────────────────────────

    def _detect_intent(self, message: str) -> str:
        """Match message against keyword patterns."""
        text = message.lower().strip()
        for intent, patterns in INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return intent
        return "general"

    # ── Location detection ───────────────────────────────────────────────

    async def _detect_location(
        self,
        session: AsyncSession,
        message: str,
        hint: str | None,
    ) -> Location | None:
        """Try to find a city name in the message or hint."""
        # Build city cache if empty
        if not _city_cache:
            result = await session.execute(select(Location))
            for loc in result.scalars().all():
                _city_cache[loc.city.lower()] = loc.id

        text = message.lower()
        # Check hint first
        if hint:
            hint_lower = hint.lower()
            if hint_lower in _city_cache:
                loc_id = _city_cache[hint_lower]
                return await session.get(Location, loc_id)

        # Scan message for city names
        for city_name, loc_id in _city_cache.items():
            if city_name in text:
                return await session.get(Location, loc_id)

        # Default to Surabaya
        if "surabaya" in _city_cache:
            return await session.get(Location, _city_cache["surabaya"])
        return None

    # ── Dispatch to intent handlers ──────────────────────────────────────

    async def _dispatch(
        self,
        session: AsyncSession,
        intent: str,
        location: Location | None,
        message: str,
    ) -> tuple[str, dict[str, Any] | None]:
        """Route to the correct handler based on intent."""
        handlers = {
            "current_weather": self._handle_current,
            "tomorrow_forecast": self._handle_tomorrow,
            "weekly_forecast": self._handle_weekly,
            "monthly_outlook": self._handle_monthly,
            "rain_check": self._handle_rain,
            "alerts": self._handle_alerts,
            "historical": self._handle_historical,
            "comparison": self._handle_comparison,
            "greeting": self._handle_greeting,
            "help": self._handle_help,
        }

        handler = handlers.get(intent, self._handle_general)
        return await handler(session, location, message)

    # ── Intent Handlers ──────────────────────────────────────────────────

    async def _handle_current(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Maaf, kota tidak ditemukan. Coba sebutkan nama kota, misalnya 'cuaca Surabaya'.", None

        obs = await self._latest_observation(session, location.id)
        if not obs:
            return (
                f"Belum ada data cuaca terkini untuk {location.city}. "
                "Data sedang dimuat, coba lagi nanti ya.",
                None,
            )

        data = {
            "temperature": obs.temperature,
            "humidity": obs.humidity,
            "condition": obs.condition,
            "wind_speed": obs.wind_speed,
        }

        reply = (
            f"🌤️ **Cuaca {location.city} Saat Ini**\n\n"
            f"🌡️ Suhu: **{obs.temperature}°C** "
            f"(Min {obs.temperature_min}°C / Maks {obs.temperature_max}°C)\n"
            f"💧 Kelembapan: {obs.humidity}%\n"
            f"🌬️ Kecepatan Angin: {obs.wind_speed} km/h\n"
            f"🌧️ Curah Hujan: {obs.precipitation} mm\n"
            f"☁️ Tutupan Awan: {obs.cloud_cover}%\n"
            f"📊 Kondisi: **{obs.condition}**\n\n"
            f"_Sumber: {obs.source}_"
        )
        return reply, data

    async def _handle_tomorrow(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Kota tidak ditemukan. Sebutkan nama kota, contoh: 'cuaca besok Jakarta'.", None

        tomorrow = date.today() + timedelta(days=1)
        fc = await self._get_forecast(session, location.id, tomorrow)
        if not fc:
            return (
                f"Prakiraan besok untuk {location.city} belum tersedia. "
                "Coba lagi nanti.",
                None,
            )

        data = {
            "date": tomorrow.isoformat(),
            "temp_min": fc.temperature_min,
            "temp_max": fc.temperature_max,
            "rain_probability": fc.rain_probability,
            "condition": fc.condition,
        }

        rain_text = "kemungkinan hujan tinggi ☔" if fc.rain_probability > 60 else "kemungkinan hujan rendah ☀️"

        reply = (
            f"📅 **Prakiraan Cuaca {location.city} Besok** ({tomorrow.strftime('%d %B %Y')})\n\n"
            f"🌡️ Suhu: {fc.temperature_min}°C – {fc.temperature_max}°C\n"
            f"🌧️ Peluang Hujan: {fc.rain_probability}% ({rain_text})\n"
            f"💧 Kelembapan: {fc.humidity}%\n"
            f"🌬️ Angin: {fc.wind_speed} km/h\n"
            f"📊 Kondisi: **{fc.condition}**\n"
            f"🎯 Tingkat Keyakinan: {(fc.confidence_score or 0) * 100:.0f}%\n\n"
            f"_Model: {fc.model_name}_"
        )
        return reply, data

    async def _handle_weekly(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Sebutkan nama kota untuk prakiraan mingguan.", None

        today = date.today()
        forecasts = await self._get_forecasts_range(
            session, location.id, today + timedelta(days=1), today + timedelta(days=7)
        )
        if not forecasts:
            return f"Prakiraan mingguan untuk {location.city} belum tersedia.", None

        lines = [f"📅 **Prakiraan 7 Hari — {location.city}**\n"]
        data_list = []
        for fc in forecasts:
            emoji = "🌧️" if fc.rain_probability > 50 else "☀️"
            lines.append(
                f"  {emoji} **{fc.forecast_date.strftime('%a %d/%m')}** — "
                f"{fc.temperature_min}–{fc.temperature_max}°C, "
                f"{fc.condition} (Hujan {fc.rain_probability}%)"
            )
            data_list.append({
                "date": fc.forecast_date.isoformat(),
                "temp_min": fc.temperature_min,
                "temp_max": fc.temperature_max,
                "rain_probability": fc.rain_probability,
                "condition": fc.condition,
            })

        reply = "\n".join(lines) + f"\n\n_Model: hybrid | Keyakinan menurun seiring horizon_"
        return reply, {"forecasts": data_list}

    async def _handle_monthly(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Sebutkan nama kota untuk outlook bulanan.", None

        today = date.today()
        forecasts = await self._get_forecasts_range(
            session, location.id, today + timedelta(days=1), today + timedelta(days=30)
        )
        if not forecasts:
            return f"Outlook bulanan untuk {location.city} belum tersedia.", None

        temps_min = [f.temperature_min for f in forecasts]
        temps_max = [f.temperature_max for f in forecasts]
        rain_probs = [f.rain_probability for f in forecasts]

        avg_min = sum(temps_min) / len(temps_min)
        avg_max = sum(temps_max) / len(temps_max)
        avg_rain = sum(rain_probs) / len(rain_probs)

        reply = (
            f"📊 **Outlook 30 Hari — {location.city}**\n\n"
            f"🌡️ Rata-rata Suhu: {avg_min:.1f}°C – {avg_max:.1f}°C\n"
            f"🌧️ Rata-rata Peluang Hujan: {avg_rain:.0f}%\n"
            f"📅 Data tersedia: {len(forecasts)} hari\n\n"
            f"⚠️ _Outlook jangka panjang memiliki ketidakpastian lebih tinggi._"
        )
        data = {
            "avg_temp_min": round(avg_min, 1),
            "avg_temp_max": round(avg_max, 1),
            "avg_rain_probability": round(avg_rain, 1),
            "days_available": len(forecasts),
        }
        return reply, data

    async def _handle_rain(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Sebutkan kota untuk cek hujan, contoh: 'hujan Surabaya'.", None

        tomorrow = date.today() + timedelta(days=1)
        fc = await self._get_forecast(session, location.id, tomorrow)
        if not fc:
            obs = await self._latest_observation(session, location.id)
            if obs:
                if obs.precipitation > 0:
                    return f"🌧️ Saat ini sedang hujan di {location.city} ({obs.precipitation} mm).", {"raining": True}
                return f"☀️ Saat ini tidak hujan di {location.city}.", {"raining": False}
            return f"Data hujan untuk {location.city} belum tersedia.", None

        if fc.rain_probability > 70:
            text = f"🌧️ **Kemungkinan besar hujan** di {location.city} besok ({fc.rain_probability}%)."
        elif fc.rain_probability > 40:
            text = f"🌦️ **Ada kemungkinan hujan** di {location.city} besok ({fc.rain_probability}%). Siapkan payung!"
        else:
            text = f"☀️ **Kemungkinan hujan rendah** di {location.city} besok ({fc.rain_probability}%). Cerah!"

        return text, {"rain_probability": fc.rain_probability, "date": tomorrow.isoformat()}

    async def _handle_alerts(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Sebutkan kota untuk cek peringatan cuaca.", None

        result = await session.execute(
            select(WeatherAlert)
            .where(
                WeatherAlert.location_id == location.id,
                WeatherAlert.is_active == True,
            )
            .order_by(desc(WeatherAlert.issued_at))
            .limit(5)
        )
        alerts = list(result.scalars().all())

        if not alerts:
            return f"✅ Tidak ada peringatan cuaca aktif untuk {location.city}.", {"alerts": []}

        lines = [f"⚠️ **Peringatan Cuaca — {location.city}**\n"]
        alert_data = []
        for alert in alerts:
            severity_emoji = {"extreme": "🔴", "severe": "🟠", "moderate": "🟡", "minor": "🟢"}.get(alert.severity, "⚪")
            lines.append(f"  {severity_emoji} **{alert.title}** ({alert.severity})")
            lines.append(f"    {alert.description[:100]}")
            alert_data.append({"title": alert.title, "severity": alert.severity})

        return "\n".join(lines), {"alerts": alert_data}

    async def _handle_historical(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        if not location:
            return "Sebutkan kota untuk data historis.", None

        result = await session.execute(
            select(WeatherObservation)
            .where(WeatherObservation.location_id == location.id)
            .order_by(desc(WeatherObservation.observed_at))
            .limit(7)
        )
        observations = list(result.scalars().all())

        if not observations:
            return f"Belum ada data historis untuk {location.city}.", None

        lines = [f"📈 **Data Historis — {location.city}** (7 hari terakhir)\n"]
        for obs in observations:
            lines.append(
                f"  📅 {obs.observed_at.strftime('%d/%m')} — "
                f"{obs.temperature}°C, {obs.condition}, Hujan {obs.precipitation}mm"
            )
        return "\n".join(lines), {"count": len(observations)}

    async def _handle_comparison(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        return (
            "🔄 Fitur perbandingan cuaca sedang dalam pengembangan. "
            "Gunakan endpoint `/api/weather/compare` untuk perbandingan data.",
            None,
        )

    async def _handle_greeting(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        return (
            "👋 Halo! Saya **WeatherNext AI**, asisten prakiraan cuaca Indonesia.\n\n"
            "Saya bisa membantu Anda dengan:\n"
            "  🌤️ Cuaca saat ini — \"cuaca Surabaya\"\n"
            "  📅 Prakiraan besok — \"cuaca besok Jakarta\"\n"
            "  📊 Prakiraan mingguan — \"cuaca 7 hari Bandung\"\n"
            "  🌧️ Cek hujan — \"apakah hujan di Medan\"\n"
            "  ⚠️ Peringatan cuaca — \"peringatan cuaca Denpasar\"\n\n"
            "Silakan tanya apa saja tentang cuaca! 😊",
            None,
        )

    async def _handle_help(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        return await self._handle_greeting(session, location, msg)

    async def _handle_general(
        self, session: AsyncSession, location: Location | None, msg: str
    ) -> tuple[str, dict | None]:
        city_name = location.city if location else "Anda"
        return (
            f"Saya mengerti pertanyaan Anda. Untuk cuaca {city_name}, "
            "coba tanyakan:\n"
            "  • \"cuaca sekarang\"\n"
            "  • \"cuaca besok\"\n"
            "  • \"cuaca 7 hari\"\n"
            "  • \"apakah hujan\"\n\n"
            "Ketik **bantuan** untuk daftar lengkap fitur.",
            None,
        )

    # ── Suggestion builder ───────────────────────────────────────────────

    def _build_suggestions(
        self, intent: str, location: Location | None
    ) -> list[str]:
        city = location.city if location else "Surabaya"
        base = [
            f"Cuaca {city} besok",
            f"Cuaca 7 hari {city}",
            f"Apakah hujan di {city}?",
        ]
        if intent == "current_weather":
            return [f"Cuaca {city} besok", f"Cuaca 7 hari {city}", f"Peringatan cuaca {city}"]
        if intent == "tomorrow_forecast":
            return [f"Cuaca {city} minggu ini", f"Apakah hujan di {city}?", f"Outlook bulanan {city}"]
        return base

    # ── DB helpers ────────────────────────────────────────────────────────

    async def _latest_observation(
        self, session: AsyncSession, location_id: int
    ) -> WeatherObservation | None:
        result = await session.execute(
            select(WeatherObservation)
            .where(WeatherObservation.location_id == location_id)
            .order_by(desc(WeatherObservation.observed_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _get_forecast(
        self, session: AsyncSession, location_id: int, target_date: date
    ) -> WeatherForecast | None:
        result = await session.execute(
            select(WeatherForecast)
            .where(
                WeatherForecast.location_id == location_id,
                WeatherForecast.forecast_date == target_date,
            )
            .order_by(desc(WeatherForecast.created_at))
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def _get_forecasts_range(
        self,
        session: AsyncSession,
        location_id: int,
        start: date,
        end: date,
    ) -> list[WeatherForecast]:
        result = await session.execute(
            select(WeatherForecast)
            .where(
                WeatherForecast.location_id == location_id,
                WeatherForecast.forecast_date >= start,
                WeatherForecast.forecast_date <= end,
            )
            .order_by(WeatherForecast.forecast_date)
        )
        return list(result.scalars().all())

    # ── Session management ───────────────────────────────────────────────

    async def _get_or_create_session(
        self, session: AsyncSession, session_id: str
    ) -> ChatSession:
        result = await session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        chat_session = result.scalar_one_or_none()
        if chat_session is None:
            chat_session = ChatSession(
                session_id=session_id,
                message_count=0,
            )
            session.add(chat_session)
            await session.flush()
        return chat_session

    async def _store_message(
        self,
        session: AsyncSession,
        chat_session: ChatSession,
        role: str,
        content: str,
        function_calls: dict | None = None,
    ) -> None:
        msg = ChatMessage(
            session_id=chat_session.id,
            role=role,
            content=content,
            function_calls=function_calls,
        )
        session.add(msg)
        chat_session.message_count += 1
        chat_session.last_message_at = datetime.now(timezone.utc)
        await session.flush()
