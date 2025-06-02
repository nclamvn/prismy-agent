# core/base_classes.py
"""
SDIP Core Base Classes
Defines abstract interfaces and base functionality for all components
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum
import time

class TranslationTier(Enum):
    """Translation quality tiers"""
    BASIC = "basic"           # Tier 1: Fast, simple translation
    STANDARD = "standard"     # Tier 2: Balanced quality/speed
    PROFESSIONAL = "professional"  # Tier 3: Premium quality

class DocumentType(Enum):
    """Supported document types"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "md"

@dataclass
class SemanticChunk:
    """
    Represents a semantically coherent piece of content
    Core unit for the Semantic Chunking Engine™
    """
    content: str                    # The actual text content
    chunk_id: str                  # Unique identifier
    semantic_context: str          # Context type (header, paragraph, list, etc.)
    position: int                  # Position in original document
    relationships: List[str]       # Related chunk IDs
    metadata: Dict[str, Any]       # Additional chunk metadata
    confidence_score: float        # Semantic coherence confidence (0-1)
    
    def __post_init__(self):
        """Validate chunk data after initialization"""
        if not self.content.strip():
            raise ValueError("Chunk content cannot be empty")
        if self.confidence_score < 0 or self.confidence_score > 1:
            raise ValueError("Confidence score must be between 0 and 1")

@dataclass
class TranslationResult:
    """
    Contains translation results and metadata
    """
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    translation_tier: TranslationTier
    quality_score: float           # Quality assessment (0-1)
    processing_time: float         # Time taken in seconds
    chunk_results: List[Dict]      # Individual chunk translation results
    metadata: Dict[str, Any]       # Additional metadata

class BaseSemanticChunker(ABC):
    """
    Abstract base class for semantic chunking engines
    Defines the interface for Semantic Chunking Engine™
    """
    
    @abstractmethod
    def chunk_document(self, content: str, doc_type: DocumentType) -> List[SemanticChunk]:
        """Break document into semantically coherent chunks"""
        pass
    
    @abstractmethod
    def analyze_semantic_relationships(self, chunks: List[SemanticChunk]) -> Dict[str, List[str]]:
        """Analyze relationships between chunks"""
        pass

class BaseTranslator(ABC):
    """
    Abstract base class for all translator implementations
    Defines common interface for all translation tiers
    """
    
    def __init__(self, tier: TranslationTier):
        self.tier = tier
        self.translation_count = 0
        self.total_processing_time = 0.0
    
    @abstractmethod
    async def translate_chunk(self, chunk: SemanticChunk, target_language: str, 
                            source_language: str = "auto") -> Dict[str, Any]:
        """Translate a single semantic chunk"""
        pass
    
    @abstractmethod
    async def translate_document(self, chunks: List[SemanticChunk], 
                               target_language: str, source_language: str = "auto") -> TranslationResult:
        """Translate entire document using semantic chunks"""
        pass
