"""WeatherNext AI API routers package."""
from app.api.weather import router as weather_router
from app.api.chat import router as chat_router
from app.api.admin import router as admin_router

__all__ = ["weather_router", "chat_router", "admin_router"]
