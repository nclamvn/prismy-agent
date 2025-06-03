# src/core/models/document.py

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ProcessingStatus(Enum):
    """Document processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class Document:
    """Main document model for processing."""
    
    id: str
    content: str
    title: Optional[str] = None
    source_language: str = "auto"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    word_count: Optional[int] = None
    
    def __post_init__(self):
        """Calculate word count if not provided."""
        if self.word_count is None:
            self.word_count = len(self.content.split())
            
    def estimate_tokens(self) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: 1 token ≈ 0.75 words
        return int(self.word_count * 1.33)
    
    def estimate_processing_time(self) -> float:
        """Estimate processing time in minutes."""
        # Rough estimate: 1000 words per minute
        return self.word_count / 1000


@dataclass 
class DocumentChunk:
    """Chunk of a document for processing."""
    
    content: str
    start_position: int
    end_position: int
    metadata: Dict[str, Any] = field(default_factory=dict)
    chunk_id: Optional[str] = None
    parent_doc_id: Optional[str] = None
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    
    def __post_init__(self):
        """Generate chunk ID if not provided."""
        if self.chunk_id is None:
            import hashlib
            content_hash = hashlib.md5(self.content.encode()).hexdigest()[:8]
            self.chunk_id = f"chunk_{self.start_position}_{content_hash}"
            
    @property
    def word_count(self) -> int:
        """Get word count of chunk."""
        return len(self.content.split())
    
    @property
    def char_count(self) -> int:
        """Get character count of chunk."""
        return len(self.content)


@dataclass
class ProcessedDocument:
    """Result of document processing."""
    
    original_document: Document
    chunks: List[DocumentChunk]
    output_format: str
    processed_content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: float = 0.0
    total_cost: float = 0.0
    model_usage: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics."""
        return {
            "original_word_count": self.original_document.word_count,
            "chunk_count": len(self.chunks),
            "output_format": self.output_format,
            "processing_time_minutes": round(self.processing_time / 60, 2),
            "total_cost_usd": round(self.total_cost, 2),
            "models_used": list(self.model_usage.keys()),
            "average_chunk_size": sum(c.word_count for c in self.chunks) / len(self.chunks) if self.chunks else 0
        }


@dataclass
class ChunkProcessingResult:
    """Result of processing a single chunk."""
    
    chunk: DocumentChunk
    processed_content: str
    model_used: str
    tokens_used: int
    processing_time: float
    cost: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    
    @property
    def success(self) -> bool:
        """Check if processing was successful."""
        return self.error is None
