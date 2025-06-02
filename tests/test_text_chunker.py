import pytest
import asyncio
from chunking.text_chunker import SmartTextChunkerEnhanced, ChunkResult, ChunkMetadata

@pytest.fixture
def chunker():
    """Create a chunker instance for testing."""
    return SmartTextChunkerEnhanced(max_chunk_size=100, overlap_size=20)

@pytest.fixture
def sample_text():
    """Create a sample text for testing."""
    return """
    First paragraph with some content.
    This is part of the first paragraph.

    Second paragraph starts here.
    It continues with more text.

    Third paragraph has numbers 1, 2, 3.
    And some special chars: !?.,
    """ * 3

def test_init_validation():
    """Test initialization parameter validation."""
    # Valid initialization
    chunker = SmartTextChunkerEnhanced(max_chunk_size=100, overlap_size=20)
    assert chunker.max_chunk_size == 100
    assert chunker.overlap_size == 20

    # Invalid max_chunk_size
    with pytest.raises(ValueError):
        SmartTextChunkerEnhanced(max_chunk_size=0)
    
    with pytest.raises(ValueError):
        SmartTextChunkerEnhanced(max_chunk_size=-1)

    # Invalid overlap_size
    with pytest.raises(ValueError):
        SmartTextChunkerEnhanced(max_chunk_size=100, overlap_size=-1)
    
    with pytest.raises(ValueError):
        SmartTextChunkerEnhanced(max_chunk_size=100, overlap_size=100)

def test_empty_text(chunker):
    """Test handling of empty text."""
    with pytest.raises(ValueError):
        chunker.chunk_text("")

@pytest.mark.asyncio
async def test_empty_text_async(chunker):
    """Test handling of empty text in async mode."""
    with pytest.raises(ValueError):
        await chunker.chunk_text_async("")

def test_short_text(chunker):
    """Test handling of text shorter than max_chunk_size."""
    text = "Short text for testing."
    chunks = chunker.chunk_text(text)
    
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].main_content == text
    assert chunks[0].context is None
    assert chunks[0].metadata.chunk_id == 0
    assert chunks[0].metadata.has_context is False

@pytest.mark.asyncio
async def test_short_text_async(chunker):
    """Test handling of short text in async mode."""
    text = "Short text for testing."
    chunks = await chunker.chunk_text_async(text)
    
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].main_content == text
    assert chunks[0].context is None
    assert chunks[0].metadata.chunk_id == 0
    assert chunks[0].metadata.has_context is False

def test_chunking_with_overlap(chunker, sample_text):
    """Test text chunking with overlap."""
    chunks = chunker.chunk_text(sample_text)
    
    assert len(chunks) > 1
    
    # Check first chunk
    assert chunks[0].metadata.chunk_id == 0
    assert chunks[0].metadata.has_context is False
    assert chunks[0].context is None
    
    # Check middle chunks
    for chunk in chunks[1:]:
        assert chunk.metadata.has_context is True
        assert chunk.context is not None
        assert len(chunk.context) <= chunker.overlap_size
        
    # Check metadata
    for i, chunk in enumerate(chunks):
        assert chunk.metadata.chunk_id == i
        assert chunk.metadata.char_count == len(chunk.main_content)
        assert chunk.metadata.word_count == len(chunk.main_content.split())

@pytest.mark.asyncio
async def test_chunking_with_overlap_async(chunker, sample_text):
    """Test text chunking with overlap in async mode."""
    chunks = await chunker.chunk_text_async(sample_text)
    
    assert len(chunks) > 1
    
    # Check first chunk
    assert chunks[0].metadata.chunk_id == 0
    assert chunks[0].metadata.has_context is False
    assert chunks[0].context is None
    
    # Check middle chunks
    for chunk in chunks[1:]:
        assert chunk.metadata.has_context is True
        assert chunk.context is not None
        assert len(chunk.context) <= chunker.overlap_size

def test_pattern_matching(chunker):
    """Test pattern matching for chunk boundaries."""
    text = "First sentence. Second sentence! Third sentence? Fourth sentence."
    chunks = chunker.chunk_text(text)
    
    # Verify chunks are split at sentence boundaries
    for chunk in chunks:
        assert chunk.main_content.strip().endswith(('.', '!', '?'))

def test_chinese_text(chunker):
    """Test handling of Chinese text."""
    text = "第一句话。第二句话，带有逗号。第三句话！第四句话？"
    chunks = chunker.chunk_text(text)
    
    # Verify chunks are split at Chinese punctuation
    for chunk in chunks:
        assert any(chunk.main_content.strip().endswith(char) 
                  for char in ('。', '，', '！', '？'))

def test_performance_large_text():
    """Test performance with large text."""
    # Create large text
    large_text = "Sample sentence. " * 1000
    
    # Create chunker with larger chunk size for performance test
    chunker = SmartTextChunkerEnhanced(max_chunk_size=1000, overlap_size=100)
    
    # Measure execution time
    import time
    start_time = time.time()
    chunks = chunker.chunk_text(large_text)
    execution_time = time.time() - start_time
    
    # Verify reasonable performance (adjust threshold as needed)
    assert execution_time < 2.0
    assert len(chunks) > 0

@pytest.mark.asyncio
async def test_performance_large_text_async():
    """Test async performance with large text."""
    # Create large text
    large_text = "Sample sentence. " * 1000
    
    # Create chunker with larger chunk size for performance test
    chunker = SmartTextChunkerEnhanced(max_chunk_size=1000, overlap_size=100)
    
    # Measure execution time
    import time
    start_time = time.time()
    chunks = await chunker.chunk_text_async(large_text)
    execution_time = time.time() - start_time
    
    # Verify reasonable performance (adjust threshold as needed)
    assert execution_time < 2.0
    assert len(chunks) > 0

def test_chunk_consistency(chunker, sample_text):
    """Test consistency of chunking results."""
    # Get chunks multiple times
    chunks1 = chunker.chunk_text(sample_text)
    chunks2 = chunker.chunk_text(sample_text)
    
    # Verify results are consistent
    assert len(chunks1) == len(chunks2)
    for c1, c2 in zip(chunks1, chunks2):
        assert c1.text == c2.text
        assert c1.main_content == c2.main_content
        assert c1.context == c2.context
        assert c1.metadata.chunk_id == c2.metadata.chunk_id

@pytest.mark.asyncio
async def test_chunk_consistency_async(chunker, sample_text):
    """Test consistency of async chunking results."""
    # Get chunks multiple times
    chunks1 = await chunker.chunk_text_async(sample_text)
    chunks2 = await chunker.chunk_text_async(sample_text)
    
    # Verify results are consistent
    assert len(chunks1) == len(chunks2)
    for c1, c2 in zip(chunks1, chunks2):
        assert c1.text == c2.text
        assert c1.main_content == c2.main_content
        assert c1.context == c2.context
        assert c1.metadata.chunk_id == c2.metadata.chunk_id

def test_metadata_accuracy(chunker):
    """Test accuracy of chunk metadata."""
    text = "First chunk content.\n\nSecond chunk content."
    chunks = chunker.chunk_text(text)
    
    for chunk in chunks:
        # Verify position tracking
        content_length = len(chunk.main_content)
        assert chunk.metadata.end_pos - chunk.metadata.start_pos == content_length
        
        # Verify word count
        expected_word_count = len(chunk.main_content.split())
        assert chunk.metadata.word_count == expected_word_count
        
        # Verify character count
        assert chunk.metadata.char_count == content_length

def test_pattern_cache(chunker):
    """Test pattern matching cache functionality."""
    text = "Test text. " * 100
    
    # First run to populate cache
    chunks1 = chunker.chunk_text(text)
    
    # Second run should use cache
    import time
    start_time = time.time()
    chunks2 = chunker.chunk_text(text)
    cached_execution_time = time.time() - start_time
    
    # Verify cache improves performance
    assert cached_execution_time < 0.1  # Adjust threshold as needed
    assert len(chunks1) == len(chunks2)

if __name__ == '__main__':
    pytest.main([__file__])
