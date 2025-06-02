"""Core business entities for translation domain."""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class TranslationRequest:
    """Represents a translation request."""
    text: str
    source_language: Optional[str]
    target_language: str
    preserve_formatting: bool = True
    quality_tier: str = "standard"
    
    def __post_init__(self):
        if not self.text.strip():
            raise ValueError("Text cannot be empty")
        if not self.target_language:
            raise ValueError("Target language is required")


@dataclass
class TranslationResult:
    """Represents the result of a translation operation."""
    translated_text: str
    source_language: str
    target_language: str
    confidence: float
    processing_time: float
    chunks_processed: int = 1
    tokens_used: int = 0
    model_used: str = "unknown"
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.created_at is None:
            self.created_at = datetime.now()
    
    @property
    def success(self) -> bool:
        """Returns True if translation was successful."""
        return bool(self.translated_text and self.confidence > 0)


@dataclass
class ChunkResult:
    """Represents a single chunk processing result."""
    chunk_id: int
    original_content: str
    translated_content: str
    processing_time: float
    tokens_used: int
    confidence: float
    has_context: bool = False
    error: Optional[str] = None


@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    target_lang: str
    ai_model: str = "gpt-3.5-turbo"
    quality_tier: str = "standard"
    chunk_size: int = 3000
    overlap_size: int = 200
    preserve_formatting: bool = True
    quality_check: bool = True
    enable_caching: bool = True
    max_retries: int = 3
    timeout_seconds: int = 120
    openai_key: Optional[str] = None
    claude_key: Optional[str] = None
