@echo off
echo 🏋️  Starting GymPro Streamlit Frontend
echo =====================================

REM Check if virtual environment is activated
if "%VIRTUAL_ENV%"=="" (
    echo ⚠️  Virtual environment not detected. Activating...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        echo ❌ Virtual environment not found. Please run setup first.
        pause
        exit /b 1
    )
)

REM Install streamlit if not already installed
pip install streamlit >nul 2>&1

echo 🚀 Starting Streamlit app...
echo 📱 Frontend will be available at: http://localhost:8501
echo 🔗 Make sure the FastAPI backend is running on: http://localhost:8001
echo.

REM Run Streamlit
streamlit run streamlit_app.py

pause
