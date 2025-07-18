"""
Pydantic models for API request/response schemas
"""
from typing import List
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000, description="User's message to the chatbot")

class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="Chatbot's response")
    is_gym_related: bool = Field(..., description="Whether the query was gym/fitness related")
    sources: List[str] = Field(default=[], description="Source documents used for the response")

class HealthResponse(BaseModel):
    """Response model for health check endpoints"""
    status: str = Field(..., description="System status (healthy, degraded, unhealthy)")
    message: str = Field(..., description="Detailed status message")
    rag_enabled: bool = Field(..., description="Whether RAG system is operational")

class SystemStatus(BaseModel):
    """Model for detailed system status"""
    vectorstore_loaded: bool
    qa_chain_initialized: bool
    embeddings_ready: bool
    google_api_configured: bool

class ResetResponse(BaseModel):
    """Response model for system reset endpoint"""
    status: str = Field(..., description="Reset operation status")
    message: str = Field(..., description="Reset operation message")
