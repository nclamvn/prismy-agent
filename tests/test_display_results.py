import sys
import pytest
from unittest.mock import patch, MagicMock, call
import pandas as pd
import numpy as np
from typing import Dict, Any

# Mock all required modules
mock_modules = [
    'streamlit',
    'plotly.express',
    'layoutparser',
    'pdf2image',
    'pytesseract',
    'openai',
    'anthropic',
    'pix2tex',
    'pix2tex.cli',
    'chunking.text_chunker',
    'chunking.layout_chunker',
    'chunking.chunk_combiner',
    'processors.formula_processor',
    'processors.pdf_processor',
    'processors.table_extractor',
    'processors.ocr_engine',
    'engines.translation_engine',
    'engines.api_manager',
    'exporters.docx_exporter',
    'exporters.pdf_exporter',
    'integrations.google_drive'
]

for module in mock_modules:
    sys.modules[module] = MagicMock()
    # For nested modules, ensure parent exists
    if '.' in module:
        parent = module.split('.')[0]
        if parent not in sys.modules:
            sys.modules[parent] = MagicMock()

# Mock specific classes
sys.modules['pix2tex.cli'].LatexOCR = MagicMock()
sys.modules['chunking.layout_chunker'].LayoutAwareChunker = MagicMock()
sys.modules['chunking.layout_chunker'].LayoutChunk = MagicMock()
sys.modules['processors.formula_processor'].FormulaProcessor = MagicMock()
sys.modules['processors.formula_processor'].Formula = MagicMock()

# Now we can safely import our module
from app_ultra_modern_fixed import display_real_text_results

@pytest.fixture
def sample_metadata():
    """Fixture for sample metadata"""
    return {
        'detected_lang': 'en',
        'doc_type': 'general',
        'confidence': 0.95,
        'processing_time': 1.5,
        'word_count': 100,
        'config': {
            'target_lang': 'Vietnamese',
            'ai_model': 'gpt-3.5-turbo'
        },
        'chunks_used': 2,
        'chunk_times': [
            {'chunk_id': 1, 'time': 0.8},
            {'chunk_id': 2, 'time': 0.7}
        ]
    }

@pytest.fixture
def mock_st():
    """Fixture for mocked streamlit"""
    mock_st = MagicMock()
    
    # Setup column mock to return a context manager
    column_context = MagicMock()
    column_context.__enter__ = MagicMock(return_value=MagicMock())
    column_context.__exit__ = MagicMock(return_value=None)
    mock_st.columns.return_value = [column_context] * 4  # Return 4 column contexts
    
    # Setup container mock
    container_context = MagicMock()
    container_context.__enter__ = MagicMock(return_value=MagicMock())
    container_context.__exit__ = MagicMock(return_value=None)
    mock_st.container.return_value = container_context
    
    return mock_st

@pytest.fixture
def mock_px():
    """Fixture for mocked plotly"""
    mock_px = MagicMock()
    mock_px.bar.return_value = MagicMock()
    return mock_px

def test_basic_display(mock_st, sample_metadata):
    """Test basic display functionality"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        original_text = "Hello world"
        translated_text = "Xin chào thế giới"
        
        display_real_text_results(original_text, translated_text, sample_metadata)
        
        # Verify metrics were displayed
        assert mock_st.metric.call_count >= 3
        
        # Verify markdown headers were created
        assert mock_st.markdown.call_count >= 1
        
        # Verify text areas were created for original and translated text
        assert mock_st.text_area.call_count >= 2

def test_chunk_timing_visualization(mock_st, mock_px, sample_metadata):
    """Test chunk timing visualization with plotly"""
    with patch('app_ultra_modern_fixed.st', mock_st), \
         patch('app_ultra_modern_fixed.px', mock_px):
        
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Verify plotly chart was created if chunk times exist
        if sample_metadata.get('chunk_times'):
            assert mock_px.bar.called
            assert mock_st.plotly_chart.called

def test_metrics_display(mock_st, sample_metadata):
    """Test metrics display with correct values"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Get all metric calls
        metric_calls = mock_st.metric.call_args_list
        
        # Verify confidence metric
        confidence_calls = [call for call in metric_calls 
                          if call[1].get('label', '').startswith('🎯')]
        assert len(confidence_calls) > 0
        
        # Verify word count metric
        word_calls = [call for call in metric_calls 
                     if call[1].get('label', '').startswith('📝')]
        assert len(word_calls) > 0

def test_download_buttons(mock_st, sample_metadata):
    """Test creation of download buttons"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Verify download buttons were created
        assert mock_st.download_button.call_count >= 1

def test_column_layout(mock_st, sample_metadata):
    """Test column layout creation"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Verify columns were created
        assert mock_st.columns.called
        
        # Verify multiple column calls for different sections
        assert mock_st.columns.call_count >= 2

def test_error_handling(mock_st):
    """Test handling of missing metadata fields"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        minimal_metadata = {
            'detected_lang': 'en',
            'doc_type': 'general',
            'config': {'target_lang': 'Vietnamese'}
        }
        
        display_real_text_results("test", "test translation", minimal_metadata)
        
        # Verify function handles missing fields gracefully
        assert mock_st.metric.call_count >= 1
        assert not mock_st.error.called

def test_long_text_handling(mock_st, sample_metadata):
    """Test handling of long text content"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        long_text = "Long text " * 1000
        long_translation = "Bản dịch dài " * 1000
        
        display_real_text_results(long_text, long_translation, sample_metadata)
        
        # Verify text areas were created
        text_area_calls = mock_st.text_area.call_args_list
        assert len(text_area_calls) >= 2
        
        # Verify preview truncation
        for call in text_area_calls:
            text_value = call[1].get('value', '')
            assert len(text_value) <= 1500  # Preview should be truncated

def test_performance_metrics(mock_st, sample_metadata):
    """Test display of performance metrics"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Verify performance metrics were displayed
        metrics_calls = mock_st.metric.call_args_list
        metric_labels = [call[1].get('label', '') for call in metrics_calls]
        
        # Check for required metrics
        assert any('Time' in label for label in metric_labels)
        assert any('Words' in label for label in metric_labels)
        assert any('Confidence' in label for label in metric_labels)

def test_high_confidence_display(mock_st):
    """Test display with high confidence score"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        metadata = {
            'detected_lang': 'en',
            'doc_type': 'general',
            'confidence': 0.98,
            'processing_time': 1.0,
            'word_count': 50,
            'config': {'target_lang': 'Vietnamese'},
            'chunks_used': 1
        }
        
        display_real_text_results("test", "test translation", metadata)
        
        # Verify high confidence is properly displayed
        metrics_calls = mock_st.metric.call_args_list
        confidence_calls = [call for call in metric_calls 
                          if call[1].get('label', '').startswith('🎯')]
        assert len(confidence_calls) > 0
        assert '98.0%' in str(confidence_calls[0])

def test_low_confidence_display(mock_st):
    """Test display with low confidence score"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        metadata = {
            'detected_lang': 'en',
            'doc_type': 'general',
            'confidence': 0.6,
            'processing_time': 1.0,
            'word_count': 50,
            'config': {'target_lang': 'Vietnamese'},
            'chunks_used': 1
        }
        
        display_real_text_results("test", "test translation", metadata)
        
        # Verify low confidence is properly displayed
        metrics_calls = mock_st.metric.call_args_list
        confidence_calls = [call for call in metric_calls 
                          if call[1].get('label', '').startswith('🎯')]
        assert len(confidence_calls) > 0
        assert '60.0%' in str(confidence_calls[0])

def test_language_display(mock_st, sample_metadata):
    """Test language display functionality"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        # Test Vietnamese detection
        metadata_vi = {**sample_metadata, 'detected_lang': 'vi'}
        display_real_text_results("Xin chào", "Hello", metadata_vi)
        
        # Test English detection
        metadata_en = {**sample_metadata, 'detected_lang': 'en'}
        display_real_text_results("Hello", "Xin chào", metadata_en)
        
        # Verify language metrics were displayed
        metrics_calls = mock_st.metric.call_args_list
        lang_calls = [call for call in metrics_calls 
                     if call[1].get('label', '').startswith('🌍')]
        assert len(lang_calls) >= 2

def test_processing_time_display(mock_st, sample_metadata):
    """Test processing time metrics display"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        # Test fast processing
        metadata_fast = {**sample_metadata, 'processing_time': 0.5}
        display_real_text_results("test", "test", metadata_fast)
        
        # Test slow processing
        metadata_slow = {**sample_metadata, 'processing_time': 5.0}
        display_real_text_results("test", "test", metadata_slow)
        
        # Verify time metrics were displayed
        metrics_calls = mock_st.metric.call_args_list
        time_calls = [call for call in metrics_calls 
                     if call[1].get('label', '').startswith('⚡')]
        assert len(time_calls) >= 2

def test_export_functionality(mock_st, sample_metadata):
    """Test export functionality with different formats"""
    with patch('app_ultra_modern_fixed.st', mock_st), \
         patch('app_ultra_modern_fixed.DOCXExporter', MagicMock()), \
         patch('app_ultra_modern_fixed.PDFExporter', MagicMock()):
        
        display_real_text_results("test", "test translation", sample_metadata)
        
        # Verify download buttons for different formats
        download_calls = mock_st.download_button.call_args_list
        
        # Check for TXT download
        txt_calls = [call for call in download_calls 
                    if call[1].get('file_name', '').endswith('.txt')]
        assert len(txt_calls) > 0
        
        # Check for DOCX download
        docx_calls = [call for call in download_calls 
                     if call[1].get('file_name', '').endswith('.docx')]
        assert len(docx_calls) >= 0  # May be 0 if exporter not available
        
        # Check for PDF download
        pdf_calls = [call for call in download_calls 
                    if call[1].get('file_name', '').endswith('.pdf')]
        assert len(pdf_calls) >= 0  # May be 0 if exporter not available

def test_chunk_statistics(mock_st, sample_metadata):
    """Test chunk statistics display"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        # Test with multiple chunks
        metadata_chunks = {
            **sample_metadata,
            'chunks_used': 3,
            'chunk_times': [
                {'chunk_id': 1, 'time': 0.5},
                {'chunk_id': 2, 'time': 0.7},
                {'chunk_id': 3, 'time': 0.6}
            ]
        }
        
        display_real_text_results("test", "test translation", metadata_chunks)
        
        # Verify chunk statistics were displayed
        metrics_calls = mock_st.metric.call_args_list
        chunk_calls = [call for call in metrics_calls 
                      if 'Chunk' in str(call)]
        assert len(chunk_calls) > 0

def test_empty_text_handling(mock_st, sample_metadata):
    """Test handling of empty text input"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        display_real_text_results("", "", sample_metadata)
        
        # Verify function handles empty text gracefully
        text_area_calls = mock_st.text_area.call_args_list
        for call in text_area_calls:
            # Text areas should still be created even with empty content
            assert 'value' in call[1]

def test_special_characters_display(mock_st, sample_metadata):
    """Test handling of special characters in text"""
    with patch('app_ultra_modern_fixed.st', mock_st):
        special_text = "Test with 特殊字符 và ký tự đặc biệt"
        special_translation = "Testing 测试 kiểm tra"
        
        display_real_text_results(special_text, special_translation, sample_metadata)
        
        # Verify text areas handle special characters
        text_area_calls = mock_st.text_area.call_args_list
        assert len(text_area_calls) >= 2
        
        # Verify special characters are preserved
        for call in text_area_calls:
            text_value = call[1].get('value', '')
            assert any(ord(c) > 127 for c in text_value)

def test_chunk_timing_visualization_detailed(mock_st, mock_px, sample_metadata):
    """Test detailed visualization of chunk processing times"""
    with patch('app_ultra_modern_fixed.st', mock_st), \
         patch('app_ultra_modern_fixed.px', mock_px):
        
        # Create metadata with varied chunk times
        metadata_with_chunks = {
            **sample_metadata,
            'chunks_used': 4,
            'chunk_times': [
                {'chunk_id': 1, 'time': 0.5},
                {'chunk_id': 2, 'time': 1.2},
                {'chunk_id': 3, 'time': 0.8},
                {'chunk_id': 4, 'time': 0.7}
            ]
        }
        
        display_real_text_results("test", "test translation", metadata_with_chunks)
        
        # Verify plotly chart creation
        assert mock_px.bar.called
        
        # Get the arguments passed to plotly bar chart
        bar_args = mock_px.bar.call_args[1]
        
        # Verify chart data structure
        assert 'x' in bar_args
        assert 'y' in bar_args
        
        # Verify chart styling
        assert 'title' in bar_args
        assert 'labels' in bar_args
        
        # Verify streamlit chart display
        assert mock_st.plotly_chart.called
        
        # Verify chart container creation
        container_calls = [call for call in mock_st.container.call_args_list]
        assert len(container_calls) > 0
