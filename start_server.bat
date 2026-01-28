@echo off
REM Quick start script for the backend server

cd /d "%~dp0backend"

echo ========================================
echo Starting Multimodal AI Backend Server
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Check if API key is configured
findstr /C:"GEMINI_API_KEY=your_api_key_here" .env >nul
if not errorlevel 1 (
    echo ERROR: API key not configured!
    echo.
    echo Please edit backend\.env and add your GEMINI_API_KEY
    echo Get your free API key from: https://makersuite.google.com/app/apikey
    echo.
    pause
    exit /b 1
)

echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
