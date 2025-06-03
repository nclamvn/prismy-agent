# src/core/models/requests.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class ProcessingRequest(BaseModel):
    """Request model for document processing."""
    content: str = Field(..., description="Document content to process")
    output_format: str = Field(..., description="Target output format")
    options: Optional[Dict[str, Any]] = Field(default={}, description="Processing options")
    
class TranslationRequest(BaseModel):
    """Request model for translation."""
    text: str
    target_language: str
    source_language: Optional[str] = "auto"
    
class ContentRequest(BaseModel):
    """Request model for content transformation."""
    content: str
    transformation_type: str
    options: Optional[Dict[str, Any]] = {}
