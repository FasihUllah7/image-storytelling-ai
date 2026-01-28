@echo off
REM Setup script for Multimodal Image Understanding & Storytelling AI
REM Windows version

echo ========================================
echo Multimodal AI System - Setup
echo ========================================
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)
python --version
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Check if .env exists
echo [2/5] Checking environment configuration...
if exist .env (
    echo .env file found
) else (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your GEMINI_API_KEY
    echo Get your free API key from: https://makersuite.google.com/app/apikey
    echo.
)
echo.

REM Install dependencies
echo [3/5] Installing Python dependencies...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Check if API key is set
echo [4/5] Verifying API key configuration...
findstr /C:"GEMINI_API_KEY=your_api_key_here" .env >nul
if not errorlevel 1 (
    echo.
    echo ========================================
    echo WARNING: API key not configured!
    echo ========================================
    echo.
    echo Please follow these steps:
    echo 1. Get your API key from: https://makersuite.google.com/app/apikey
    echo 2. Open backend\.env in a text editor
    echo 3. Replace 'your_api_key_here' with your actual API key
    echo 4. Save the file
    echo.
    echo Then run: start_server.bat
    echo.
    pause
    exit /b 0
)
echo API key configured
echo.

REM All done
echo [5/5] Setup complete!
echo.
echo ========================================
echo Next Steps:
echo ========================================
echo 1. Start the backend server:
echo    cd backend
echo    python app.py
echo.
echo 2. Open the frontend:
echo    Open frontend\index.html in your browser
echo    OR run: cd frontend ^&^& python -m http.server 8000
echo.
echo For detailed instructions, see README.md
echo ========================================
echo.
pause
