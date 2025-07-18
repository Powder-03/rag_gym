"""
GymPro RAG Chatbot - Main entry point
"""
import uvicorn
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=8001,  # Use different port to avoid conflicts
        reload=settings.DEBUG,
        log_level="info"
    )
