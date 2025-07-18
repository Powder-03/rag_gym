@echo off
setlocal enabledelayedexpansion

echo 🏋️  GymPro RAG Chatbot - Docker Deployment
echo ==========================================

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

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

echo 🔧 Building Docker image...
docker-compose build

echo 🚀 Starting GymPro RAG Chatbot...
docker-compose up -d

echo ⏳ Waiting for application to start...
timeout /t 10 /nobreak >nul

REM Check if application is healthy
curl -f http://localhost:8001/health >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ GymPro RAG Chatbot is running successfully!
    echo.
    echo 🌐 Access points:
    echo    • Streamlit Frontend: http://localhost:8501
    echo    • FastAPI Backend: http://localhost:8001
    echo    • API Docs: http://localhost:8001/docs
    echo    • Health Check: http://localhost:8001/health
    echo.
    echo 📋 Useful commands:
    echo    • View logs: docker-compose logs -f
    echo    • Stop app: docker-compose down
    echo    • Restart: docker-compose restart
) else (
    echo ❌ Application failed to start. Check logs:
    docker-compose logs
    pause
    exit /b 1
)

pause
