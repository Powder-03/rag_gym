#!/bin/bash

# GymPro RAG Chatbot - Docker Build and Run Script

set -e

echo "🏋️  GymPro RAG Chatbot - Docker Deployment"
echo "=========================================="

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

# Create logs directory if it doesn't exist
mkdir -p logs

echo "🔧 Building Docker image..."
docker-compose build

echo "🚀 Starting GymPro RAG Chatbot..."
docker-compose up -d

echo "⏳ Waiting for application to start..."
sleep 10

# Check if application is healthy
if curl -f http://localhost:8001/health >/dev/null 2>&1; then
    echo "✅ GymPro RAG Chatbot is running successfully!"
    echo ""
    echo "🌐 Access points:"
    echo "   • Streamlit Frontend: http://localhost:8501"
    echo "   • FastAPI Backend: http://localhost:8001"
    echo "   • API Docs: http://localhost:8001/docs"
    echo "   • Health Check: http://localhost:8001/health"
    echo ""
    echo "📋 Useful commands:"
    echo "   • View logs: docker-compose logs -f"
    echo "   • Stop app: docker-compose down"
    echo "   • Restart: docker-compose restart"
else
    echo "❌ Application failed to start. Check logs:"
    docker-compose logs
    exit 1
fi
