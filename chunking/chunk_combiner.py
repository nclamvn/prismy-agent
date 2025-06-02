"""Enhanced chunk combination system with safe text handling."""

from typing import List, Dict, Any
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def combine_chunks_safely(translated_chunks: List[Dict], total_expected: int) -> str:
    """Combine translated chunks safely while preserving formatting and handling overlaps.
    
    Args:
        translated_chunks: List of dictionaries containing translated chunks
        total_expected: Expected total number of chunks
        
    Returns:
        Combined text with proper formatting
        
    Features:
    - Maintains chunk order using chunk_id
    - Handles overlapping content intelligently
    - Preserves formatting and structure
    - Provides detailed logging
    - Handles errors gracefully
    """
    
    if not translated_chunks:
        logger.warning("No chunks to combine")
        return "[ERROR: No chunks to combine]"
    
    try:
        # Sort chunks by chunk_id
        sorted_chunks = sorted(translated_chunks, key=lambda x: x['chunk_id'])
        logger.info(f"Combining {len(sorted_chunks)} chunks in order")
        
        # Validate chunk count
        if len(sorted_chunks) != total_expected:
            logger.warning(
                f"Chunk count mismatch: got {len(sorted_chunks)}, "
                f"expected {total_expected}"
            )
        
        # Combine chunks with intelligent overlap handling
        combined_parts = []
        last_content = ""
        
        for i, chunk in enumerate(sorted_chunks):
            translated_text = chunk['translated'].strip()
            
            if not translated_text:
                logger.warning(f"Empty chunk {i+1}, skipping")
                continue
                
            # Handle error markers
            if translated_text.startswith('[TRANSLATION ERROR'):
                logger.warning(f"Error in chunk {i+1}, using original content")
                combined_parts.append(
                    f"\n[Chunk {i+1} - Translation Error]\n"
                    f"{chunk.get('original_content', '')[:1000]}\n"
                )
                continue
            
            # Intelligent overlap handling
            if last_content and len(last_content) > 100:
                # Look for overlapping content in the last 100 chars
                last_100 = last_content[-100:].strip()
                first_100 = translated_text[:100].strip()
                
                # Find and remove overlaps
                for overlap_size in range(50, 0, -1):
                    if last_100[-overlap_size:] in first_100:
                        overlap_pos = first_100.find(last_100[-overlap_size:])
                        if overlap_pos >= 0:
                            translated_text = translated_text[overlap_pos + overlap_size:].strip()
                            logger.debug(f"Removed {overlap_size} chars overlap in chunk {i+1}")
                            break
            
            # Add to combined parts
            combined_parts.append(translated_text)
            last_content = translated_text
            logger.debug(f"Added chunk {i+1}: {len(translated_text)} chars")
        
        # Join with appropriate separator
        if len(combined_parts) > 1:
            final_result = "\n\n".join(combined_parts)
        else:
            final_result = combined_parts[0] if combined_parts else "[ERROR: No content to combine]"
        
        # Clean up formatting
        final_result = clean_combined_text(final_result)
        
        logger.info(f"Successfully combined {len(sorted_chunks)} chunks: {len(final_result)} chars")
        return final_result
        
    except Exception as e:
        logger.error(f"Error combining chunks: {str(e)}")
        return f"[ERROR: Chunk combination failed - {str(e)}]"

def clean_combined_text(text: str) -> str:
    """Clean up combined text by removing excessive whitespace while preserving formatting.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text with normalized whitespace
    """
    # Remove excessive newlines (more than 3)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    
    # Normalize multiple spaces
    text = re.sub(r' {3,}', '  ', text)
    
    # Replace tabs with double space
    text = re.sub(r'\t+', '  ', text)
    
    # Clean up spacing around punctuation
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Normalize spacing after punctuation
    text = re.sub(r'([.,!?;:])\s*', r'\1 ', text)
    
    # Remove leading/trailing whitespace
    return text.strip()
