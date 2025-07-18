#!/bin/bash

# Run Streamlit frontend locally
echo "🏋️  Starting GymPro Streamlit Frontend"
echo "====================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    else
        echo "❌ Virtual environment not found. Please run setup first."
        exit 1
    fi
fi

# Install streamlit if not already installed
pip install streamlit > /dev/null 2>&1

echo "🚀 Starting Streamlit app..."
echo "📱 Frontend will be available at: http://localhost:8501"
echo "🔗 Make sure the FastAPI backend is running on: http://localhost:8001"
echo ""

# Run Streamlit
streamlit run streamlit_app.py
