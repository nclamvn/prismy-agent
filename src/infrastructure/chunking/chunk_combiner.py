"""Chunk combination with overlap handling and intelligent merging."""

import re
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher

from src.core.interfaces.chunking import ChunkCombinerInterface


class SmartChunkCombiner(ChunkCombinerInterface):
    """Smart chunk combiner with overlap detection and handling."""
    
    def __init__(self, overlap_threshold: float = 0.8, min_similarity: float = 0.3):
        self.overlap_threshold = overlap_threshold
        self.min_similarity = min_similarity
    
    def combine_chunks(self, chunks: List[Dict[str, Any]]) -> str:
        """Combine translated chunks into final text with smart overlap handling."""
        if not chunks:
            return ""
        
        if len(chunks) == 1:
            return chunks[0].get('translated', chunks[0].get('content', ''))
        
        # Sort chunks by ID to ensure correct order
        sorted_chunks = sorted(chunks, key=lambda x: x.get('chunk_id', x.get('id', '')))
        
        # Handle overlaps first
        processed_chunks = self.handle_overlaps(sorted_chunks)
        
        # Combine processed chunks
        result_parts = []
        for chunk in processed_chunks:
            translated_text = chunk.get('translated', chunk.get('content', '')).strip()
            if translated_text:
                result_parts.append(translated_text)
        
        # Join with appropriate spacing
        return self._join_with_smart_spacing(result_parts)
    
    def handle_overlaps(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Handle overlapping content between chunks."""
        if len(chunks) <= 1:
            return chunks
        
        processed_chunks = [chunks[0]]  # First chunk always included
        
        for i in range(1, len(chunks)):
            current_chunk = chunks[i]
            previous_chunk = processed_chunks[-1]
            
            # Check for overlap between consecutive chunks
            overlap_info = self._detect_overlap(previous_chunk, current_chunk)
            
            if overlap_info['has_overlap']:
                # Remove overlap from current chunk
                current_chunk = self._remove_overlap(current_chunk, overlap_info)
            
            processed_chunks.append(current_chunk)
        
        return processed_chunks
    
    def _detect_overlap(self, chunk1: Dict[str, Any], chunk2: Dict[str, Any]) -> Dict[str, Any]:
        """Detect overlap between two consecutive chunks."""
        text1 = chunk1.get('translated', chunk1.get('content', ''))
        text2 = chunk2.get('translated', chunk2.get('content', ''))
        
        # Get last part of first chunk and first part of second chunk
        words1 = text1.split()
        words2 = text2.split()
        
        if not words1 or not words2:
            return {'has_overlap': False}
        
        # Check for word-level overlap
        max_overlap_length = min(len(words1), len(words2), 50)  # Check up to 50 words
        
        best_overlap = {'length': 0, 'similarity': 0, 'position1': 0, 'position2': 0}
        
        for overlap_len in range(max_overlap_length, 2, -1):  # Start from longest possible
            tail1 = " ".join(words1[-overlap_len:])
            head2 = " ".join(words2[:overlap_len])
            
            similarity = SequenceMatcher(None, tail1.lower(), head2.lower()).ratio()
            
            if similarity > self.overlap_threshold:
                best_overlap = {
                    'length': overlap_len,
                    'similarity': similarity,
                    'position1': len(words1) - overlap_len,
                    'position2': 0,
                    'text1': tail1,
                    'text2': head2
                }
                break
        
        return {
            'has_overlap': best_overlap['length'] > 0,
            'overlap_data': best_overlap if best_overlap['length'] > 0 else None
        }
    
    def _remove_overlap(self, chunk: Dict[str, Any], overlap_info: Dict[str, Any]) -> Dict[str, Any]:
        """Remove overlap from chunk based on overlap information."""
        if not overlap_info['has_overlap']:
            return chunk
        
        text = chunk.get('translated', chunk.get('content', ''))
        words = text.split()
        
        overlap_data = overlap_info['overlap_data']
        overlap_length = overlap_data['length']
        
        # Remove overlapping words from the beginning of the chunk
        remaining_words = words[overlap_length:]
        cleaned_text = " ".join(remaining_words)
        
        # Update chunk with cleaned text
        updated_chunk = chunk.copy()
        if 'translated' in updated_chunk:
            updated_chunk['translated'] = cleaned_text
        else:
            updated_chunk['content'] = cleaned_text
        
        return updated_chunk
    
    def _join_with_smart_spacing(self, text_parts: List[str]) -> str:
        """Join text parts with intelligent spacing."""
        if not text_parts:
            return ""
        
        if len(text_parts) == 1:
            return text_parts[0]
        
        result = text_parts[0]
        
        for i in range(1, len(text_parts)):
            current_part = text_parts[i]
            
            if not current_part.strip():
                continue
            
            # Determine appropriate spacing
            spacing = self._determine_spacing(result, current_part)
            result += spacing + current_part
        
        return result.strip()
    
    def _determine_spacing(self, prev_text: str, next_text: str) -> str:
        """Determine appropriate spacing between text parts."""
        if not prev_text or not next_text:
            return ""
        
        prev_text = prev_text.strip()
        next_text = next_text.strip()
        
        # Check if previous text ends with sentence ending
        if re.search(r'[.!?]\s*$', prev_text):
            # Check if next text starts with paragraph indicator
            if re.match(r'^[A-Z\d]', next_text) or next_text.startswith('•'):
                return "\n\n"  # Paragraph break
            else:
                return " "  # Single space
        
        # Check if we're connecting list items or bullet points
        if (prev_text.endswith(':') or 
            re.search(r'[0-9]\.\s*$', prev_text) or 
            prev_text.endswith('•')):
            return "\n"  # Line break for lists
        
        # Check if next text starts like a new paragraph
        if re.match(r'^[A-Z].*[.!?]', next_text):
            return "\n\n"  # Paragraph break
        
        # Default spacing
        return " "


def combine_chunks_safely(translated_chunks: List[Dict[str, Any]], total_chunks: int) -> str:
    """Legacy function for backward compatibility with old app."""
    combiner = SmartChunkCombiner()
    return combiner.combine_chunks(translated_chunks)
