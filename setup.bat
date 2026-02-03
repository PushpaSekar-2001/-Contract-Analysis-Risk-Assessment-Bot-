@echo off
REM GenAI Contract Analysis Bot - Windows Setup Script

echo.
echo ===================================================
echo   GenAI Contract Analysis & Risk Assessment Bot
echo   Setup Script for Windows
echo ===================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo ✓ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✓ pip upgraded
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ All dependencies installed
echo.

REM Check for .env file
if not exist .env (
    echo.
    echo ⚠️  IMPORTANT: Create a .env file in the project root
    echo.
    echo Steps:
    echo 1. Go to https://console.anthropic.com/api_keys
    echo 2. Create an API key
    echo 3. Create a file named .env in the project folder
    echo 4. Add: ANTHROPIC_API_KEY=your-key-here
    echo.
    echo You can use .env.example as a template
    echo.
)

echo.
echo ===================================================
echo   Setup Complete! ✓
echo ===================================================
echo.
echo To start the application:
echo   streamlit run app.py
echo.
echo The app will open at: http://localhost:8501
echo.

pause
