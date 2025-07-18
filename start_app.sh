#!/bin/bash

# GymPro RAG Chatbot - Complete Startup Script
echo "🏋️  GymPro RAG Chatbot - Complete Setup"
echo "======================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your Google API key before running again."
    echo "   Required: GOOGLE_API_KEY=your_actual_api_key_here"
    exit 1
fi

# Check if Google API key is set
if grep -q "your_google_api_key_here" .env; then
    echo "⚠️  Please set your Google API key in .env file before running."
    echo "   Required: GOOGLE_API_KEY=your_actual_api_key_here"
    exit 1
fi

echo "Choose deployment method:"
echo "1) Docker Compose (Recommended - Full Stack)"
echo "2) Local Development (Separate terminals)"
echo "3) Backend Only (FastAPI)"
echo "4) Frontend Only (Streamlit)"

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo "🐳 Starting with Docker Compose..."
        mkdir -p logs
        docker-compose up --build
        ;;
    2)
        echo "💻 Local Development Mode"
        echo "This will start both services in separate terminal windows"
        echo "Make sure you have activated your virtual environment"
        
        # Start FastAPI backend in background
        echo "🚀 Starting FastAPI backend..."
        python main.py &
        BACKEND_PID=$!
        
        sleep 5
        
        # Start Streamlit frontend
        echo "🎨 Starting Streamlit frontend..."
        streamlit run streamlit_app.py &
        FRONTEND_PID=$!
        
        echo "✅ Both services started!"
        echo "📱 Frontend: http://localhost:8501"
        echo "🔗 Backend: http://localhost:8001"
        echo ""
        echo "Press Ctrl+C to stop both services"
        
        # Wait for interrupt
        trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
        wait
        ;;
    3)
        echo "🔧 Starting FastAPI Backend Only..."
        python main.py
        ;;
    4)
        echo "🎨 Starting Streamlit Frontend Only..."
        echo "⚠️  Make sure FastAPI backend is running on http://localhost:8001"
        streamlit run streamlit_app.py
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac
