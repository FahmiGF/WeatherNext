@echo off
title WeatherNext AI - Backend Server
echo ============================================
echo   WeatherNext AI - Backend Server
echo ============================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting WeatherNext AI Backend Server...
echo API Docs: http://localhost:8000/docs
echo Health:   http://localhost:8000/api/health
echo.
python run.py
pause
