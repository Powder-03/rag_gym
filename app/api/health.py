"""
Health check and system status API endpoints
"""
import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import HealthResponse, SystemStatus, ResetResponse
from app.services.rag_service import rag_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    try:
        system_status = rag_service.get_system_status()
        all_systems_ready = all(system_status.values())
        
        return HealthResponse(
            status="healthy" if all_systems_ready else "degraded",
            message="GymPro RAG Chatbot is running",
            rag_enabled=rag_service.is_rag_ready()
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            message=f"Health check failed: {str(e)}",
            rag_enabled=False
        )

@router.get("/health", response_model=HealthResponse)
async def detailed_health():
    """Detailed health check with system status"""
    try:
        system_status = rag_service.get_system_status()
        all_systems_ready = all(system_status.values())
        
        # Try to reinitialize if not ready
        if not rag_service.is_rag_ready():
            logger.info("Attempting to reinitialize RAG system...")
            rag_service.initialize_rag_system()
        
        return HealthResponse(
            status="healthy" if all_systems_ready else "degraded",
            message=f"System Status: {system_status}",
            rag_enabled=rag_service.is_rag_ready()
        )
        
    except Exception as e:
        logger.error(f"Detailed health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            message=f"Error: {str(e)}",
            rag_enabled=False
        )

@router.post("/reset", response_model=ResetResponse)
async def reset_system():
    """Reset and reinitialize the RAG system"""
    try:
        success = rag_service.reset_system()
        
        if success:
            return ResetResponse(
                status="success",
                message="RAG system reset and reinitialized successfully"
            )
        else:
            return ResetResponse(
                status="error",
                message="Failed to reinitialize RAG system"
            )
            
    except Exception as e:
        logger.error(f"Reset error: {e}")
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")
