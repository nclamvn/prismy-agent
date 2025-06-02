"""Core interfaces for translation domain."""

from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.entities.translation import (
    TranslationRequest, 
    TranslationResult, 
    ChunkResult,
    ProcessingConfig
)


class TranslatorInterface(ABC):
    """Interface for translation services."""
    
    @abstractmethod
    async def translate(self, request: TranslationRequest) -> TranslationResult:
        """Translate text according to the request."""
        pass


class ChunkerInterface(ABC):
    """Interface for text chunking services."""
    
    @abstractmethod
    def chunk_text(self, text: str, max_size: int = 3000, overlap: int = 200) -> List[str]:
        """Split text into manageable chunks."""
        pass


class CacheInterface(ABC):
    """Interface for caching services."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[TranslationResult]:
        """Get cached translation result."""
        pass
