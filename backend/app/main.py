"""WeatherNext AI — FastAPI Main Application."""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import admin_router, chat_router, weather_router
from app.config import get_settings
from app.database import async_session_factory, init_db
from app.seed import run_all_seeds

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("weathernext-ai")

settings = get_settings()
STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler: initializes tables and seeds mock/baseline data."""
    logger.info("Initializing WeatherNext AI Database...")
    await init_db()

    async with async_session_factory() as session:
        try:
            logger.info("Running initial seed data...")
            await run_all_seeds(session)
            await session.commit()
            logger.info("Database initialized and seeded successfully.")
        except Exception as exc:
            logger.exception("Failed to run seed data: %s", exc)
            await session.rollback()

    yield

    logger.info("Shutting down WeatherNext AI backend...")


app = FastAPI(
    title="WeatherNext AI API",
    description=(
        "Platform prediksi cuaca cerdas berbasis AI yang menggabungkan "
        "WeatherNext 3, TimesFM-3, data pengamatan BMKG, serta asisten AI interaktif."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(weather_router)
app.include_router(chat_router)
app.include_router(admin_router)


# Serve static files if directory exists
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def root():
    """Serve WeatherNext AI Web Dashboard."""
    index_file = STATIC_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return RedirectResponse(url="/docs")


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Service health check."""
    return {
        "status": "healthy",
        "service": "WeatherNext AI Backend",
        "version": "1.0.0",
        "env": settings.ENVIRONMENT,
    }
