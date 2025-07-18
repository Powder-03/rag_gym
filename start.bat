@echo off
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file and add your Google API key
) else (
    echo .env file already exists
)

echo.
echo Starting Gym Pro Chatbot...
python main.py
