"""
FastAPI application factory and configuration
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.services.rag_service import rag_service
from app.api import chat, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting GymPro RAG Chatbot...")
    success = rag_service.initialize_rag_system()
    if success:
        logger.info("✅ RAG system initialized successfully")
    else:
        logger.warning("⚠️ RAG system initialization failed - using fallback mode")
    
    yield
    
    # Shutdown
    logger.info("Shutting down GymPro RAG Chatbot...")

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        description="A comprehensive gym information chatbot using RAG (Retrieval-Augmented Generation)",
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(health.router)
    app.include_router(chat.router)
    
    # Mount static files (for serving the chat UI)
    try:
        static_path = settings.PROJECT_ROOT / "static"
        if static_path.exists():
            app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    except Exception as e:
        logger.warning(f"Could not mount static files: {e}")
    
    return app

# Create the app instance
app = create_app()