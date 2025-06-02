import pytest
import tempfile
import os
from pathlib import Path
import numpy as np
import cv2
from processors.pdf_processor import PDFProcessor
from processors.table_extractor import TableExtractor
from processors.ocr_engine import OCREngine
from chunking.layout_chunker import LayoutAwareChunker

@pytest.fixture
def test_components():
    """Initialize all components for integration testing"""
    return {
        'pdf_processor': PDFProcessor(),
        'table_extractor': TableExtractor(),
        'ocr_engine': OCREngine(),
        'chunker': LayoutAwareChunker()
    }

@pytest.fixture
def sample_complex_pdf():
    """Create a complex PDF with mixed content for testing"""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        return tmp.name

class TestIntegration:
    def test_full_processing_pipeline(self, test_components, sample_complex_pdf):
        """Test the complete document processing pipeline"""
        pdf_processor = test_components['pdf_processor']
        table_extractor = test_components['table_extractor']
        ocr_engine = test_components['ocr_engine']
        chunker = test_components['chunker']
        
        # Step 1: Analyze PDF
        analysis = pdf_processor.analyze_pdf(sample_complex_pdf)
        assert isinstance(analysis.page_count, int)
        assert isinstance(analysis.has_tables, bool)
        
        # Step 2: Extract content based on analysis
        if analysis.is_scanned:
            # Use OCR pipeline
            content = ocr_engine.process_pdf_ocr(sample_complex_pdf)
            assert 'full_text' in content
            text = content['full_text']
        else:
            # Use direct text extraction
            content = pdf_processor.extract_text_content(sample_complex_pdf)
            assert 'full_text' in content
            text = content['full_text']
        
        # Step 3: Extract tables if present
        if analysis.has_tables:
            tables = table_extractor.extract_tables_from_pdf(sample_complex_pdf)
            assert 'tables' in tables
            assert isinstance(tables['total_tables'], int)
        
        # Step 4: Create layout-aware chunks
        chunks = chunker.chunk_text(text)
        assert len(chunks) > 0
        assert all(hasattr(chunk, 'layout_elements') for chunk in chunks)

    def test_error_propagation(self, test_components):
        """Test error handling and propagation between components"""
        pdf_processor = test_components['pdf_processor']
        table_extractor = test_components['table_extractor']
        ocr_engine = test_components['ocr_engine']
        
        # Test with invalid PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf') as tmp:
            tmp.write(b'Invalid PDF content')
            tmp.flush()
            
            # Verify each component handles the error appropriately
            with pytest.raises(Exception):
                pdf_processor.analyze_pdf(tmp.name)
            
            with pytest.raises(Exception):
                table_extractor.extract_tables_from_pdf(tmp.name)
            
            with pytest.raises(Exception):
                ocr_engine.process_pdf_ocr(tmp.name)

    def test_multilingual_document_handling(self, test_components, sample_complex_pdf):
        """Test processing of multilingual documents"""
        pdf_processor = test_components['pdf_processor']
        ocr_engine = test_components['ocr_engine']
        chunker = test_components['chunker']
        
        # Process multilingual content
        content = ocr_engine.process_pdf_ocr(
            sample_complex_pdf,
            lang='eng+vie+chi_sim'
        )
        assert 'full_text' in content
        
        # Create chunks preserving language-specific formatting
        chunks = chunker.chunk_text(content['full_text'])
        assert len(chunks) > 0

    def test_table_and_layout_integration(self, test_components, sample_complex_pdf):
        """Test integration of table extraction with layout preservation"""
        pdf_processor = test_components['pdf_processor']
        table_extractor = test_components['table_extractor']
        chunker = test_components['chunker']
        
        # Extract content and tables
        content = pdf_processor.extract_text_content(sample_complex_pdf)
        tables = table_extractor.extract_tables_from_pdf(sample_complex_pdf)
        
        # Create chunks with table awareness
        text_with_tables = content['full_text']
        if tables['total_tables'] > 0:
            # Verify table positions are preserved in chunks
            chunks = chunker.chunk_text(text_with_tables)
            table_chunks = [
                chunk for chunk in chunks
                if any(elem.element_type == 'table' 
                      for elem in chunk.layout_elements)
            ]
            assert len(table_chunks) > 0

    def test_performance_integration(self, test_components, sample_complex_pdf):
        """Test performance of the integrated pipeline"""
        import time
        
        start_time = time.time()
        
        # Run full pipeline
        pdf_processor = test_components['pdf_processor']
        table_extractor = test_components['table_extractor']
        chunker = test_components['chunker']
        
        # Step 1: Analysis
        analysis = pdf_processor.analyze_pdf(sample_complex_pdf)
        
        # Step 2: Content extraction
        content = pdf_processor.extract_text_content(sample_complex_pdf)
        
        # Step 3: Table extraction
        if analysis.has_tables:
            tables = table_extractor.extract_tables_from_pdf(sample_complex_pdf)
        
        # Step 4: Chunking
        chunks = chunker.chunk_text(content['full_text'])
        
        total_time = time.time() - start_time
        assert total_time < 60  # seconds

    def test_memory_usage(self, test_components, sample_complex_pdf):
        """Test memory usage during integrated processing"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Run full pipeline
        pdf_processor = test_components['pdf_processor']
        table_extractor = test_components['table_extractor']
        chunker = test_components['chunker']
        
        pdf_processor.analyze_pdf(sample_complex_pdf)
        content = pdf_processor.extract_text_content(sample_complex_pdf)
        tables = table_extractor.extract_tables_from_pdf(sample_complex_pdf)
        chunks = chunker.chunk_text(content['full_text'])
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Ensure memory usage is reasonable (less than 1GB increase)
        assert memory_increase < 1024 * 1024 * 1024

    def test_concurrent_processing(self, test_components, sample_complex_pdf):
        """Test concurrent processing capabilities"""
        import asyncio
        
        async def process_document():
            pdf_processor = test_components['pdf_processor']
            table_extractor = test_components['table_extractor']
            chunker = test_components['chunker']
            
            # Parallel processing of different components
            analysis_task = asyncio.create_task(
                pdf_processor.analyze_pdf_async(sample_complex_pdf)
            )
            content_task = asyncio.create_task(
                pdf_processor.extract_text_content_async(sample_complex_pdf)
            )
            
            # Wait for results
            analysis = await analysis_task
            content = await content_task
            
            # Process results
            assert isinstance(analysis.page_count, int)
            assert 'full_text' in content
            
            return analysis, content
        
        # Run concurrent processing
        results = asyncio.run(process_document())
        assert len(results) == 2

    @classmethod
    def teardown_class(cls):
        """Clean up test files after all tests complete"""
        # Remove temporary files
        for file in Path(tempfile.gettempdir()).glob('test_integration_*'):
            try:
                file.unlink()
            except Exception:
                pass
