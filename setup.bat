@echo off
echo ==========================================
echo Enterprise RAG Bot - One-Click Setup
echo ==========================================
echo.

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python from python.org
    pause
    exit /b
)

:: Create Virtual Environment
echo [1/3] Creating virtual environment (venv)...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b
)

:: Install Requirements
echo [2/3] Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b
)

:: Check for .env
if not exist .env (
    echo [3/3] Creating .env from template...
    copy .env.example .env
    echo [WARNING] .env created. Please add your GEMINI_API_KEY to the .env file.
) else (
    echo [3/3] .env already exists.
)

echo.
echo ==========================================
echo SETUP COMPLETE!
echo.
echo To start the bot, run: start_bot.bat
echo ==========================================
pause
