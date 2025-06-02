"""
Enhanced Semantic Chunking Engine
Provides structure-aware document segmentation with table and formula detection
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re
import nltk
from engines.semantic_chunking import SemanticChunker

@dataclass
class EnhancedChunk:
    """Enhanced chunk with metadata"""
    content: str
    chunk_id: str
    chunk_type: str = "text"  # text, table, formula, structure
    confidence: float = 1.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class EnhancedSemanticChunking:
    """Enhanced semantic chunking with structure awareness"""
    
    def __init__(self):
        """Initialize enhanced chunking system"""
        try:
            # Try to use the original semantic chunker
            self.base_chunker = SemanticChunker()
        except:
            # Fallback if base chunker not available
            self.base_chunker = None
        
        # Enhanced patterns
        self.table_patterns = [
            r'\|.*\|.*\|',  # Markdown tables
            r'\t.*\t.*\t',  # Tab-separated
            r'(\w+\s+){3,}\n',  # Space-separated columns
        ]
        
        self.formula_patterns = [
            r'[A-Z]+\d+:\w+',  # Excel cell references
            r'=\w+\(',  # Excel formulas
            r'\$[A-Z]+\$\d+',  # Absolute references
            r'SUM|AVERAGE|COUNT|MAX|MIN|IF',  # Function names
        ]
        
        self.structure_patterns = [
            r'^#{1,6}\s+',  # Headers
            r'^\*\s+|^\-\s+|^\d+\.\s+',  # Lists
            r'```.*```',  # Code blocks
        ]
    
    def chunk_document(self, text: str, preserve_tables: bool = True, 
                      preserve_formulas: bool = True) -> List[EnhancedChunk]:
        """
        Enhanced document chunking with structure preservation
        
        Args:
            text: Input text to chunk
            preserve_tables: Whether to detect and preserve tables
            preserve_formulas: Whether to detect and preserve formulas
            
        Returns:
            List of enhanced chunks with metadata
        """
        try:
            chunks = []
            
            # If we have base chunker, use it first
            if self.base_chunker:
                try:
                    base_chunks = self.base_chunker.chunk_text(text)
                    # Convert base chunks to enhanced chunks
                    for i, chunk in enumerate(base_chunks):
                        enhanced_chunk = EnhancedChunk(
                            content=chunk,
                            chunk_id=f"base_{i}",
                            chunk_type="text",
                            confidence=0.8
                        )
                        chunks.append(enhanced_chunk)
                except:
                    # Fallback to simple chunking
                    chunks = self._simple_chunk(text)
            else:
                # Use simple chunking as fallback
                chunks = self._simple_chunk(text)
            
            # Enhanced processing
            enhanced_chunks = []
            
            for chunk in chunks:
                # Detect special content types
                chunk_type = self._detect_chunk_type(
                    chunk.content, preserve_tables, preserve_formulas
                )
                
                # Update chunk with enhanced metadata
                enhanced_chunk = EnhancedChunk(
                    content=chunk.content,
                    chunk_id=chunk.chunk_id,
                    chunk_type=chunk_type,
                    confidence=self._calculate_confidence(chunk.content, chunk_type),
                    metadata={
                        'word_count': len(chunk.content.split()),
                        'has_tables': preserve_tables and self._has_tables(chunk.content),
                        'has_formulas': preserve_formulas and self._has_formulas(chunk.content),
                        'structure_elements': self._detect_structure_elements(chunk.content)
                    }
                )
                
                enhanced_chunks.append(enhanced_chunk)
            
            return enhanced_chunks
            
        except Exception as e:
            # Ultimate fallback - simple text chunking
            return [EnhancedChunk(
                content=text,
                chunk_id="fallback_0",
                chunk_type="text",
                confidence=0.5,
                metadata={'error': str(e)}
            )]
    
    def _simple_chunk(self, text: str) -> List[EnhancedChunk]:
        """Simple text chunking fallback"""
        # Split by paragraphs
        paragraphs = text.split('\n\n')
        chunks = []
        
        for i, para in enumerate(paragraphs):
            if para.strip():
                chunk = EnhancedChunk(
                    content=para.strip(),
                    chunk_id=f"simple_{i}",
                    chunk_type="text",
                    confidence=0.7
                )
                chunks.append(chunk)
        
        return chunks if chunks else [EnhancedChunk(
            content=text,
            chunk_id="simple_0",
            chunk_type="text",
            confidence=0.6
        )]
    
    def _detect_chunk_type(self, content: str, preserve_tables: bool, 
                          preserve_formulas: bool) -> str:
        """Detect the type of content in a chunk"""
        if preserve_tables and self._has_tables(content):
            return "table"
        elif preserve_formulas and self._has_formulas(content):
            return "formula"
        elif self._has_structure_elements(content):
            return "structure"
        else:
            return "text"
    
    def _has_tables(self, content: str) -> bool:
        """Check if content contains table structures"""
        for pattern in self.table_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return True
        return False
    
    def _has_formulas(self, content: str) -> bool:
        """Check if content contains formulas"""
        for pattern in self.formula_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return False
    
    def _has_structure_elements(self, content: str) -> bool:
        """Check if content has structural elements"""
        for pattern in self.structure_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return True
        return False
    
    def _detect_structure_elements(self, content: str) -> List[str]:
        """Detect specific structure elements"""
        elements = []
        
        if re.search(r'^#{1,6}\s+', content, re.MULTILINE):
            elements.append("headers")
        if re.search(r'^\*\s+|^\-\s+|^\d+\.\s+', content, re.MULTILINE):
            elements.append("lists")
        if re.search(r'```.*```', content, re.DOTALL):
            elements.append("code_blocks")
        
        return elements
    
    def _calculate_confidence(self, content: str, chunk_type: str) -> float:
        """Calculate confidence score for chunk classification"""
        base_confidence = 0.8
        
        # Adjust based on chunk type detection accuracy
        if chunk_type == "table" and self._has_tables(content):
            return min(0.95, base_confidence + 0.1)
        elif chunk_type == "formula" and self._has_formulas(content):
            return min(0.95, base_confidence + 0.1)
        elif chunk_type == "structure" and self._has_structure_elements(content):
            return min(0.9, base_confidence + 0.05)
        
        # Standard text confidence
        return base_confidence
