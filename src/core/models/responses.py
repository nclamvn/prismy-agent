# src/core/models/responses.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class ProcessingStatus(str, Enum):
    """Processing status enum."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    QUEUED = "queued"

class ProcessingResponse(BaseModel):
    """Response model for document processing."""
    job_id: str
    status: str
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = {}
    estimated_time: Optional[float] = None
    
class TranslationResponse(BaseModel):
    """Response model for translation."""
    translated_text: str
    source_language: str
    target_language: str
    confidence: Optional[float] = None
    
class ContentResponse(BaseModel):
    """Response model for content transformation."""
    transformed_content: str
    transformation_type: str
    metadata: Optional[Dict[str, Any]] = {}
