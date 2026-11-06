@echo off
title WeatherNext AI - Launcher
color 0B
echo ========================================================
echo       WEATHERNEXT AI - WEATHER INTELLIGENCE & VOICE
echo ========================================================
echo.
echo [1/2] Memeriksa dependensi backend...
cd /d "%~dp0backend"
pip install -r requirements.txt >nul 2>&1
echo.
echo [2/2] Membuka WeatherNext AI Web Dashboard...
start "" "http://localhost:8001"
echo.
echo ========================================================
echo Server berjalan di: http://localhost:8001
echo API Documentation:  http://localhost:8001/docs
echo ========================================================
echo.
echo Tekan Ctrl+C untuk menghentikan server kapan saja.
python run.py
pause
