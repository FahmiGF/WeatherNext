@echo off
title WeatherNow AI - Weather Prediction & Voice Assistant
color 0B
echo ===================================================================
echo             WEATHERNOW AI - WEATHER PREDICTION & VOICE
echo ===================================================================
echo.
echo [1/2] Menyiapkan server WeatherNow AI...
cd /d "%~dp0backend"
pip install -r requirements.txt >nul 2>&1
echo.
echo [2/2] Membuka WeatherNow AI Dashboard di browser...
start "" "http://localhost:8001"
echo.
echo ===================================================================
echo Dashboard & Voice Assistant: http://localhost:8001
echo Dokumentasi REST API:        http://localhost:8001/docs
echo ===================================================================
echo.
echo Server sedang berjalan... Tekan Ctrl+C untuk menutup.
python run.py
pause
