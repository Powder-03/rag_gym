"""
Chat API endpoints
"""
import logging
from fastapi import APIRouter, HTTPException

from app.models.schemas import ChatRequest, ChatResponse
from app.services.rag_service import rag_service
from app.utils.content_filter import content_filter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for gym-related questions"""
    try:
        # Validate and filter content
        validation = content_filter.validate_message(request.message)
        
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail=validation["error"])
        
        message = validation["message"]
        gym_related = validation["gym_related"]
        
        # If not gym-related, return polite rejection
        if not gym_related:
            return ChatResponse(
                response=content_filter.get_fallback_response(message),
                is_gym_related=False,
                sources=[]
            )
        
        # Use RAG system if available
        if rag_service.is_rag_ready():
            try:
                result = rag_service.query(message)
                
                if result["success"]:
                    return ChatResponse(
                        response=result["response"],
                        is_gym_related=True,
                        sources=result["sources"]
                    )
                else:
                    # RAG failed, use fallback
                    logger.warning(f"RAG query failed: {result.get('error', 'Unknown error')}")
                    fallback_response = content_filter.get_fallback_response(message)
                    return ChatResponse(
                        response=fallback_response,
                        is_gym_related=True,
                        sources=[]
                    )
                    
            except Exception as e:
                logger.error(f"RAG query error: {e}")
                # Fall back to basic response
                fallback_response = content_filter.get_fallback_response(message)
                return ChatResponse(
                    response=fallback_response,
                    is_gym_related=True,
                    sources=[]
                )
        else:
            # RAG system not available, use fallback
            fallback_response = content_filter.get_fallback_response(message)
            return ChatResponse(
                response=fallback_response,
                is_gym_related=True,
                sources=[]
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
