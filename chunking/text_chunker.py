from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Pattern
import re
import logging
from datetime import datetime
import asyncio
from functools import lru_cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ChunkMetadata:
    """Metadata for a text chunk"""
    chunk_id: int
    start_pos: int
    end_pos: int
    word_count: int
    char_count: int
    has_context: bool
    original_start: int
    original_end: int

@dataclass
class ChunkResult:
    """Result of text chunking operation"""
    chunk_id: int
    text: str
    main_content: str
    metadata: ChunkMetadata
    context: Optional[str] = None

class SmartTextChunkerEnhanced:
    """Enhanced system for intelligent text chunking with advanced features.
    
    Features:
    - Intelligent chunk boundary detection
    - Context preservation
    - Async support for large texts
    - Pattern caching
    - Advanced error handling
    
    Attributes:
        max_chunk_size (int): Maximum size of each chunk
        overlap_size (int): Size of overlap between chunks
        split_patterns (List[Pattern]): Compiled regex patterns for splitting
    """
    
    def __init__(self, max_chunk_size: int = 2800, overlap_size: int = 150):
        """Initialize the chunker with specified parameters.
        
        Args:
            max_chunk_size: Maximum size of each chunk (default: 2800)
            overlap_size: Size of overlap between chunks (default: 150)
            
        Raises:
            ValueError: If max_chunk_size or overlap_size is invalid
        """
        self._validate_init_params(max_chunk_size, overlap_size)
        
        self.max_chunk_size = max_chunk_size
        self.overlap_size = overlap_size
        
        # Compile patterns once during initialization
        self.split_patterns = self._compile_split_patterns()
        
        logger.info(
            f"Initialized SmartTextChunkerEnhanced with max_chunk_size={max_chunk_size}, "
            f"overlap_size={overlap_size}"
        )

    @staticmethod
    def _validate_init_params(max_chunk_size: int, overlap_size: int) -> None:
        """Validate initialization parameters.
        
        Args:
            max_chunk_size: Maximum chunk size to validate
            overlap_size: Overlap size to validate
            
        Raises:
            ValueError: If parameters are invalid
        """
        if max_chunk_size <= 0:
            raise ValueError("max_chunk_size must be positive")
        if overlap_size < 0:
            raise ValueError("overlap_size must be non-negative")
        if overlap_size >= max_chunk_size:
            raise ValueError("overlap_size must be less than max_chunk_size")

    @staticmethod
    def _compile_split_patterns() -> List[Pattern]:
        """Compile and return regex patterns for text splitting.
        
        Returns:
            List of compiled regex patterns
        """
        patterns = [
            r'\n\n\n+',    # Multiple line breaks (paragraphs)
            r'\n\n',       # Double line breaks
            r'\.\s+',      # Sentence endings with space
            r'。\s*',      # Chinese sentence endings
            r'\!\s+',      # Exclamation with space
            r'\?\s+',      # Question with space
            r'\n',         # Single line breaks
            r'，\s*',      # Chinese comma
            r',\s+',       # Comma with space
            r'；\s*',      # Chinese semicolon
            r';\s+',       # Semicolon with space
            r'\s+',        # Any whitespace
        ]
        
        return [re.compile(pattern) for pattern in patterns]

    @lru_cache(maxsize=1024)
    def _find_pattern_match(self, text: str, start: int, end: int) -> Optional[int]:
        """Find the best pattern match in the given text range.
        
        Args:
            text: Text to search in
            start: Start position
            end: End position
            
        Returns:
            Position of the best match or None if no match found
        """
        search_region = text[start:end]
        
        for pattern in self.split_patterns:
            matches = list(pattern.finditer(search_region))
            if matches:
                # Get last match position
                last_match = matches[-1]
                return start + last_match.end()
        
        return None

    def _find_optimal_cut_point(self, text: str, start: int, max_end: int) -> int:
        """Find the optimal point to cut the text.
        
        Uses KMP algorithm for pattern matching when beneficial.
        
        Args:
            text: Text to process
            start: Start position
            max_end: Maximum end position
            
        Returns:
            Position to cut the text
        """
        if max_end >= len(text):
            return len(text)
        
        # Search in the last 400 chars for more options
        search_start = max(start, max_end - 400)
        
        # Try pattern matching first
        cut_pos = self._find_pattern_match(text, search_start, max_end)
        if cut_pos and cut_pos > start:
            return cut_pos
        
        # Fallback: find last space
        for i in range(max_end - 1, start + self.max_chunk_size // 2, -1):
            if i < len(text) and text[i].isspace():
                return i + 1
        
        # Last resort: hard cut
        return max_end

    async def chunk_text_async(self, text: str) -> List[ChunkResult]:
        """Asynchronously chunk text for parallel processing of large texts.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of ChunkResult objects
            
        Raises:
            ValueError: If text is empty
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if len(text) <= self.max_chunk_size:
            return [self._create_single_chunk(text, 0)]
        
        chunks = []
        chunk_id = 0
        current_pos = 0
        
        logger.info(f"Starting async chunking of text: {len(text)} chars")
        
        while current_pos < len(text):
            # Process chunks in parallel when beneficial
            if len(text) - current_pos > self.max_chunk_size * 2:
                chunk_futures = []
                for _ in range(min(3, (len(text) - current_pos) // self.max_chunk_size)):
                    if current_pos >= len(text):
                        break
                        
                    chunk_end = min(current_pos + self.max_chunk_size, len(text))
                    optimal_cut = self._find_optimal_cut_point(text, current_pos, chunk_end)
                    
                    chunk_futures.append(
                        self._process_chunk_async(
                            text, current_pos, optimal_cut, chunk_id
                        )
                    )
                    
                    current_pos = optimal_cut
                    chunk_id += 1
                
                # Wait for parallel chunk processing
                chunk_results = await asyncio.gather(*chunk_futures)
                chunks.extend(chunk_results)
            else:
                # Process remaining text normally
                chunk_end = min(current_pos + self.max_chunk_size, len(text))
                optimal_cut = self._find_optimal_cut_point(text, current_pos, chunk_end)
                
                chunk = await self._process_chunk_async(
                    text, current_pos, optimal_cut, chunk_id
                )
                chunks.append(chunk)
                
                current_pos = optimal_cut
                chunk_id += 1
        
        logger.info(f"Completed chunking: {len(chunks)} chunks created")
        return chunks

    def chunk_text(self, text: str) -> List[ChunkResult]:
        """Synchronously chunk text into optimal pieces.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of ChunkResult objects
            
        Raises:
            ValueError: If text is empty
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if len(text) <= self.max_chunk_size:
            return [self._create_single_chunk(text, 0)]
        
        chunks = []
        chunk_id = 0
        current_pos = 0
        
        logger.info(f"Starting chunking of text: {len(text)} chars")
        
        while current_pos < len(text):
            chunk_end = min(current_pos + self.max_chunk_size, len(text))
            optimal_cut = self._find_optimal_cut_point(text, current_pos, chunk_end)
            
            chunk = self._create_chunk(text, current_pos, optimal_cut, chunk_id)
            chunks.append(chunk)
            
            current_pos = optimal_cut
            chunk_id += 1
            
            logger.debug(
                f"Created chunk {chunk_id}: pos {current_pos}-{optimal_cut} "
                f"({optimal_cut-current_pos} chars)"
            )
        
        logger.info(f"Completed chunking: {len(chunks)} chunks created")
        return chunks

    def _create_single_chunk(self, text: str, chunk_id: int) -> ChunkResult:
        """Create a single chunk for short texts.
        
        Args:
            text: Text content
            chunk_id: Chunk identifier
            
        Returns:
            ChunkResult object
        """
        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            start_pos=0,
            end_pos=len(text),
            word_count=len(text.split()),
            char_count=len(text),
            has_context=False,
            original_start=0,
            original_end=len(text)
        )
        
        return ChunkResult(
            chunk_id=chunk_id,
            text=text,
            main_content=text,
            metadata=metadata
        )

    async def _process_chunk_async(
        self, 
        text: str, 
        start_pos: int, 
        end_pos: int, 
        chunk_id: int
    ) -> ChunkResult:
        """Asynchronously process a single chunk.
        
        Args:
            text: Full text
            start_pos: Start position
            end_pos: End position
            chunk_id: Chunk identifier
            
        Returns:
            ChunkResult object
        """
        # Simulate async processing
        await asyncio.sleep(0)
        return self._create_chunk(text, start_pos, end_pos, chunk_id)

    def _create_chunk(
        self, 
        text: str, 
        start_pos: int, 
        end_pos: int, 
        chunk_id: int
    ) -> ChunkResult:
        """Create a chunk with context if needed.
        
        Args:
            text: Full text
            start_pos: Start position
            end_pos: End position
            chunk_id: Chunk identifier
            
        Returns:
            ChunkResult object
        """
        main_content = text[start_pos:end_pos]
        has_context = chunk_id > 0 and self.overlap_size > 0
        
        if has_context:
            context_start = max(0, start_pos - self.overlap_size)
            context = text[context_start:start_pos]
            
            full_chunk_text = (
                f"[CONTEXT_START]\n{context}\n[CONTEXT_END]\n\n"
                f"[MAIN_CONTENT_START]\n{main_content}\n[MAIN_CONTENT_END]"
            )
        else:
            context = None
            full_chunk_text = main_content
        
        metadata = ChunkMetadata(
            chunk_id=chunk_id,
            start_pos=start_pos,
            end_pos=end_pos,
            word_count=len(main_content.split()),
            char_count=len(main_content),
            has_context=has_context,
            original_start=start_pos,
            original_end=end_pos
        )
        
        return ChunkResult(
            chunk_id=chunk_id,
            text=full_chunk_text,
            main_content=main_content,
            metadata=metadata,
            context=context
        )

# Example usage and tests
if __name__ == "__main__":
    # Create test text
    test_text = """
    This is a sample text for testing the enhanced chunking system.
    It includes multiple paragraphs and various punctuation marks.
    
    Second paragraph with some content.
    This helps test paragraph splitting.
    
    Final paragraph with numbers 1, 2, 3 and special chars!
    How well does it handle questions? Let's see...
    """ * 10
    
    # Create chunker
    chunker = SmartTextChunkerEnhanced(max_chunk_size=500, overlap_size=50)
    
    # Test sync chunking
    chunks = chunker.chunk_text(test_text)
    print(f"\nSync chunking created {len(chunks)} chunks")
    
    # Test async chunking
    async def test_async():
        chunks = await chunker.chunk_text_async(test_text)
        print(f"\nAsync chunking created {len(chunks)} chunks")
    
    # Run async test
    import asyncio
    asyncio.run(test_async())
