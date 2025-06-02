import pytest
from chunking.layout_chunker import LayoutAwareChunker, LayoutChunk, LayoutElement
from typing import List

@pytest.fixture
def layout_chunker():
    return LayoutAwareChunker(max_chunk_size=500, overlap_size=50)

@pytest.fixture
def complex_document():
    return """# Main Heading

## Section 1
This is a paragraph with some content.
It continues on multiple lines.

### Subsection 1.1
* List item 1
* List item 2
  * Nested item 2.1
  * Nested item 2.2

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| More 1   | More 2   | More 3   |

## Section 2
Another paragraph with different content.
This helps test the chunking behavior.

| Table 2  | Header 2 |
|----------|----------|
| Value 1  | Value 2  |

* Final list item 1
* Final list item 2
"""

def test_structure_detection(layout_chunker, complex_document):
    """Test if the chunker correctly detects document structure elements"""
    chunks = layout_chunker.chunk_text(complex_document)
    assert len(chunks) > 0
    
    # Verify all chunks are LayoutChunk instances
    assert all(isinstance(chunk, LayoutChunk) for chunk in chunks)
    
    # Check for heading detection
    headings_found = False
    for chunk in chunks:
        for element in chunk.layout_elements:
            if element.element_type == 'heading':
                headings_found = True
                assert element.metadata.get('level') in [1, 2, 3]
    assert headings_found, "No headings were detected"
    
    # Check for table detection
    tables_found = False
    for chunk in chunks:
        for element in chunk.layout_elements:
            if element.element_type == 'table':
                tables_found = True
                assert element.metadata.get('rows') >= 2
                assert element.metadata.get('columns') >= 2
    assert tables_found, "No tables were detected"
    
    # Check for list detection
    lists_found = False
    for chunk in chunks:
        for element in chunk.layout_elements:
            if element.element_type == 'list':
                lists_found = True
                assert element.metadata.get('items') >= 1
    assert lists_found, "No lists were detected"

def test_chunk_boundaries(layout_chunker, complex_document):
    """Test if chunk boundaries respect structural elements"""
    chunks = layout_chunker.chunk_text(complex_document)
    
    # Verify no headings are split across chunks
    heading_texts = []
    for chunk in chunks:
        chunk_headings = [
            elem.content for elem in chunk.layout_elements
            if elem.element_type == 'heading'
        ]
        heading_texts.extend(chunk_headings)
    
    # Check if headings are complete
    for heading in heading_texts:
        assert heading.strip().startswith('#'), f"Incomplete heading: {heading}"
        assert len(heading.split('\n')) == 1, f"Split heading detected: {heading}"

def test_table_preservation(layout_chunker):
    """Test if tables are kept intact within chunks"""
    test_doc = """Some text before the table.

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| More 1   | More 2   | More 3   |

Some text after the table."""

    chunks = layout_chunker.chunk_text(test_doc)
    
    # Find chunk containing table
    table_chunk = None
    for chunk in chunks:
        for element in chunk.layout_elements:
            if element.element_type == 'table':
                table_chunk = chunk
                break
        if table_chunk:
            break
    
    assert table_chunk is not None, "Table not found in any chunk"
    
    # Verify table structure
    table_elements = [
        elem for elem in table_chunk.layout_elements
        if elem.element_type == 'table'
    ]
    assert len(table_elements) == 1, "Table was split or duplicated"
    
    table = table_elements[0]
    assert table.metadata['rows'] == 4  # Header + separator + 2 data rows
    assert table.metadata['columns'] == 3

def test_list_structure(layout_chunker):
    """Test if list structure is preserved"""
    test_doc = """Some text before the list.

* Item 1
* Item 2
  * Nested 2.1
  * Nested 2.2
* Item 3

Some text after the list."""

    chunks = layout_chunker.chunk_text(test_doc)
    
    # Find chunk containing list
    list_chunk = None
    for chunk in chunks:
        for element in chunk.layout_elements:
            if element.element_type == 'list':
                list_chunk = chunk
                break
        if list_chunk:
            break
    
    assert list_chunk is not None, "List not found in any chunk"
    
    # Verify list structure
    list_elements = [
        elem for elem in list_chunk.layout_elements
        if elem.element_type == 'list'
    ]
    assert len(list_elements) >= 1, "List structure not preserved"
    
    # Check if nested items are kept together
    list_content = list_elements[0].content
    assert "* Item 2" in list_content
    assert "  * Nested 2.1" in list_content
    assert "  * Nested 2.2" in list_content

def test_chunk_metadata(layout_chunker, complex_document):
    """Test if chunks contain correct metadata"""
    chunks = layout_chunker.chunk_text(complex_document)
    
    for chunk in chunks:
        # Check basic metadata
        assert hasattr(chunk, 'chunk_id')
        assert hasattr(chunk, 'metadata')
        assert hasattr(chunk, 'layout_metadata')
        
        # Verify layout metadata
        assert 'element_counts' in chunk.layout_metadata
        assert 'layout_confidence' in chunk.layout_metadata
        assert 0 <= chunk.layout_metadata['layout_confidence'] <= 1
        
        # Check structure type
        assert hasattr(chunk, 'structure_type')
        assert chunk.structure_type in ['heading', 'paragraph', 'table', 'list']

def test_json_serialization(layout_chunker, complex_document):
    """Test if chunks can be properly serialized to JSON"""
    chunks = layout_chunker.chunk_text(complex_document)
    
    for chunk in chunks:
        json_str = layout_chunker.to_json(chunk)
        
        # Verify JSON structure
        assert '"chunk_id":' in json_str
        assert '"text":' in json_str
        assert '"main_content":' in json_str
        assert '"metadata":' in json_str
        assert '"layout_elements":' in json_str
        assert '"structure_type":' in json_str
        assert '"layout_metadata":' in json_str

def test_empty_document(layout_chunker):
    """Test handling of empty documents"""
    with pytest.raises(ValueError):
        layout_chunker.chunk_text("")

def test_single_line_document(layout_chunker):
    """Test handling of single-line documents"""
    text = "Just a single line of text."
    chunks = layout_chunker.chunk_text(text)
    
    assert len(chunks) == 1
    assert chunks[0].text == text
    assert not chunks[0].layout_elements  # No special structure expected

def test_overlap_handling(layout_chunker):
    """Test if overlap is handled correctly with layout elements"""
    # Create a document that will require multiple chunks
    long_doc = "# Heading\n\n" + ("This is a test paragraph.\n" * 20)
    
    chunks = layout_chunker.chunk_text(long_doc)
    
    assert len(chunks) > 1, "Document should be split into multiple chunks"
    
    # Check if context is preserved
    for i, chunk in enumerate(chunks):
        if i > 0:  # Not the first chunk
            assert chunk.context is not None, "Missing context in non-first chunk"
            assert chunk.metadata.has_context

def test_configuration_options():
    """Test different configuration options"""
    # Test with tables disabled
    chunker_no_tables = LayoutAwareChunker(
        max_chunk_size=500,
        overlap_size=50,
        preserve_tables=False
    )
    
    test_doc = """# Heading

| Col 1 | Col 2 |
|-------|--------|
| Data  | Data   |"""

    chunks = chunker_no_tables.chunk_text(test_doc)
    
    # Verify no table elements are detected
    for chunk in chunks:
        assert not any(
            elem.element_type == 'table'
            for elem in chunk.layout_elements
        )
    
    # Test with headings disabled
    chunker_no_headings = LayoutAwareChunker(
        max_chunk_size=500,
        overlap_size=50,
        respect_headings=False
    )
    
    chunks = chunker_no_headings.chunk_text(test_doc)
    
    # Verify no heading elements are detected
    for chunk in chunks:
        assert not any(
            elem.element_type == 'heading'
            for elem in chunk.layout_elements
        )
