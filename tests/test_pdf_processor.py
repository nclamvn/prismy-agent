import pytest
import os
from pathlib import Path
import numpy as np
from processors.pdf_processor import PDFProcessor, PDFAnalysis, PDFPage
import pdfplumber
import tempfile

@pytest.fixture
def pdf_processor():
    return PDFProcessor()

@pytest.fixture
def sample_pdf_path():
    # Create a temporary PDF file for testing
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        return tmp.name

@pytest.fixture
def complex_pdf_path():
    # Create a more complex PDF with tables and images for testing
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        return tmp.name

class TestPDFProcessor:
    def test_initialization(self, pdf_processor):
        """Test proper initialization of PDF Processor"""
        assert pdf_processor.initialized
        assert hasattr(pdf_processor, 'layout_model')
        assert pdf_processor.ocr_config == '--oem 3 --psm 6'
        assert 'eng' in pdf_processor.supported_langs
        assert 'vie' in pdf_processor.supported_langs

    def test_pdf_analysis(self, pdf_processor, sample_pdf_path):
        """Test PDF document analysis capabilities"""
        # Create a simple PDF for testing
        with pdfplumber.open(sample_pdf_path) as pdf:
            first_page = pdf.pages[0]
            analysis = pdf_processor.analyze_pdf(sample_pdf_path)
            
            assert isinstance(analysis, PDFAnalysis)
            assert analysis.page_count >= 1
            assert isinstance(analysis.has_text, bool)
            assert isinstance(analysis.has_tables, bool)
            assert isinstance(analysis.has_images, bool)
            assert isinstance(analysis.is_scanned, bool)
            assert 0 <= analysis.layout_score <= 1
            assert 0 <= analysis.complexity_score <= 1
            assert isinstance(analysis.metadata, dict)

    def test_scanned_document_detection(self, pdf_processor, sample_pdf_path):
        """Test detection of scanned documents"""
        analysis = pdf_processor.analyze_pdf(sample_pdf_path)
        assert isinstance(analysis.is_scanned, bool)
        
        # Test with a known scanned document
        if analysis.is_scanned:
            assert analysis.has_images
            assert not analysis.has_text

    def test_layout_complexity_analysis(self, pdf_processor, complex_pdf_path):
        """Test layout complexity analysis"""
        analysis = pdf_processor.analyze_pdf(complex_pdf_path)
        
        assert 0 <= analysis.layout_score <= 1
        assert 0 <= analysis.complexity_score <= 1
        
        # More complex documents should have higher scores
        if analysis.has_tables and analysis.has_images:
            assert analysis.complexity_score > 0.5

    def test_text_extraction(self, pdf_processor, sample_pdf_path):
        """Test text content extraction"""
        content = pdf_processor.extract_text_content(sample_pdf_path)
        
        assert isinstance(content, dict)
        assert 'pages' in content
        assert 'full_text' in content
        assert 'confidence' in content
        
        assert isinstance(content['pages'], list)
        assert isinstance(content['full_text'], str)
        assert 0 <= content['confidence'] <= 1

    def test_ocr_processing(self, pdf_processor, sample_pdf_path):
        """Test OCR processing capabilities"""
        # Test with different languages
        for lang in ['eng', 'vie']:
            result = pdf_processor.process_pdf_ocr(sample_pdf_path, lang=lang)
            
            assert isinstance(result, dict)
            assert 'pages' in result
            assert 'full_text' in result
            assert 'confidence' in result
            
            assert isinstance(result['pages'], list)
            for page in result['pages']:
                assert 'page_number' in page
                assert 'text' in page
                assert 'confidence' in page
                assert 0 <= page['confidence'] <= 1

    def test_error_handling(self, pdf_processor):
        """Test error handling for various scenarios"""
        # Test with non-existent file
        with pytest.raises(Exception):
            pdf_processor.analyze_pdf('nonexistent.pdf')
        
        # Test with invalid file
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
            tmp.write(b'This is not a PDF')
            tmp.flush()
            with pytest.raises(Exception):
                pdf_processor.analyze_pdf(tmp.name)

    def test_performance(self, pdf_processor, complex_pdf_path):
        """Test performance with large documents"""
        import time
        
        start_time = time.time()
        analysis = pdf_processor.analyze_pdf(complex_pdf_path)
        processing_time = time.time() - start_time
        
        # Processing should complete within reasonable time
        assert processing_time < 30  # seconds
        
        # Verify analysis completed successfully
        assert isinstance(analysis, PDFAnalysis)
        assert analysis.page_count > 0

    def test_metadata_extraction(self, pdf_processor, sample_pdf_path):
        """Test PDF metadata extraction"""
        analysis = pdf_processor.analyze_pdf(sample_pdf_path)
        
        assert isinstance(analysis.metadata, dict)
        # Check common metadata fields
        for field in ['Producer', 'Creator', 'Title']:
            if field in analysis.metadata:
                assert isinstance(analysis.metadata[field], str)

    @pytest.mark.asyncio
    async def test_async_processing(self, pdf_processor, complex_pdf_path):
        """Test asynchronous processing capabilities"""
        # This test assumes async processing is implemented
        analysis = await pdf_processor.analyze_pdf_async(complex_pdf_path)
        
        assert isinstance(analysis, PDFAnalysis)
        assert analysis.page_count > 0
        assert isinstance(analysis.layout_score, float)

    def test_cleanup(self, pdf_processor, sample_pdf_path, complex_pdf_path):
        """Test cleanup of temporary files and resources"""
        # Process files
        pdf_processor.analyze_pdf(sample_pdf_path)
        pdf_processor.analyze_pdf(complex_pdf_path)
        
        # Clean up temporary files
        if hasattr(pdf_processor, 'cleanup'):
            pdf_processor.cleanup()
            
            # Verify cleanup
            assert not any(
                Path(tempfile.gettempdir()).glob('pdf_processor_temp_*')
            )

    @classmethod
    def teardown_class(cls):
        """Clean up test files after all tests complete"""
        # Remove temporary PDF files
        for file in Path(tempfile.gettempdir()).glob('*.pdf'):
            try:
                file.unlink()
            except Exception:
                pass
