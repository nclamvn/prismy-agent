"""Chunking interfaces for clean architecture."""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum


class ChunkType(Enum):
    """Types of chunks."""
    TEXT = "text"
    FORMULA = "formula"
    TABLE = "table"
    CODE = "code"
    HEADER = "header"


@dataclass
class ChunkMetadata:
    """Metadata for a chunk."""
    chunk_type: ChunkType = ChunkType.TEXT
    has_context: bool = False
    is_formula_heavy: bool = False
    is_code_block: bool = False
    confidence: float = 1.0
    language: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None


@dataclass  
class TextChunk:
    """Represents a text chunk with metadata."""
    chunk_id: str
    main_content: str
    context: Optional[str] = None
    metadata: Optional[ChunkMetadata] = None
    start_position: Optional[int] = None
    end_position: Optional[int] = None


class ChunkerInterface(ABC):
    """Interface for text chunking strategies."""
    
    @abstractmethod
    def chunk_text(self, text: str, **kwargs) -> List[TextChunk]:
        """Split text into chunks with metadata."""
        pass
    
    @abstractmethod
    def get_optimal_chunk_size(self, text: str) -> int:
        """Calculate optimal chunk size for given text."""
        pass
    
    @abstractmethod
    def estimate_chunks(self, text: str) -> int:
        """Estimate number of chunks for given text."""
        pass


class ChunkCombinerInterface(ABC):
    """Interface for combining translated chunks."""
    
    @abstractmethod
    def combine_chunks(self, chunks: List[Dict[str, Any]]) -> str:
        """Combine translated chunks into final text."""
        pass
    
    @abstractmethod
    def handle_overlaps(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle overlapping content between chunks."""
        pass


class LayoutChunkerInterface(ABC):
    """Interface for layout-aware chunking."""
    
    @abstractmethod
    def chunk_with_layout(self, content: str, layout_info: Dict[str, Any]) -> List[TextChunk]:
        """Chunk text preserving layout information."""
        pass
    
    @abstractmethod
    def detect_layout_elements(self, content: str) -> Dict[str, Any]:
        """Detect layout elements in content."""
        pass
