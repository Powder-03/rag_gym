@echo off
setlocal enabledelayedexpansion

echo 🏋️  GymPro RAG Chatbot - Complete Setup
echo =======================================

REM Check if .env file exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from .env.example...
    copy .env.example .env
    echo 📝 Please edit .env file and add your Google API key before running again.
    echo    Required: GOOGLE_API_KEY=your_actual_api_key_here
    pause
    exit /b 1
)

REM Check if Google API key is set
findstr /C:"your_google_api_key_here" .env >nul
if !errorlevel! equ 0 (
    echo ⚠️  Please set your Google API key in .env file before running.
    echo    Required: GOOGLE_API_KEY=your_actual_api_key_here
    pause
    exit /b 1
)

echo Choose deployment method:
echo 1) Docker Compose (Recommended - Full Stack)
echo 2) Local Development (Separate windows)
echo 3) Backend Only (FastAPI)
echo 4) Frontend Only (Streamlit)
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🐳 Starting with Docker Compose...
    if not exist logs mkdir logs
    docker-compose up --build
) else if "%choice%"=="2" (
    echo 💻 Local Development Mode
    echo This will start both services in separate windows
    echo Make sure you have activated your virtual environment
    
    echo 🚀 Starting FastAPI backend...
    start "GymPro Backend" cmd /c "python main.py"
    
    timeout /t 5 /nobreak >nul
    
    echo 🎨 Starting Streamlit frontend...
    start "GymPro Frontend" cmd /c "streamlit run streamlit_app.py"
    
    echo ✅ Both services started!
    echo 📱 Frontend: http://localhost:8501
    echo 🔗 Backend: http://localhost:8001
    echo.
    echo Close the respective windows to stop the services
    
) else if "%choice%"=="3" (
    echo 🔧 Starting FastAPI Backend Only...
    python main.py
) else if "%choice%"=="4" (
    echo 🎨 Starting Streamlit Frontend Only...
    echo ⚠️  Make sure FastAPI backend is running on http://localhost:8001
    streamlit run streamlit_app.py
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)

pause
