import pytest
import os
import tempfile
from exporters.docx_exporter import DOCXExporter
from exporters.pdf_exporter import PDFExporter
import pandas as pd

@pytest.fixture
def sample_data():
    return {
        'original_text': 'Hello World',
        'translated_text': 'Bonjour le Monde',
        'metadata': {
            'detected_lang': 'en',
            'config': {'target_lang': 'fr'},
            'processing_time': 1.23,
            'confidence': 0.95
        }
    }

@pytest.fixture
def sample_pdf_data():
    return {
        'title': 'Test Document',
        'text': 'Sample text content',
        'translation': {'translated_text': 'Texte exemple'},
        'tables': {
            'tables': [
                pd.DataFrame({
                    'Column1': ['A', 'B'],
                    'Column2': [1, 2]
                })
            ]
        }
    }

def test_docx_export_translation(sample_data):
    exporter = DOCXExporter()
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        try:
            result = exporter.export_translation_result(
                original_text=sample_data['original_text'],
                translated_text=sample_data['translated_text'],
                metadata=sample_data['metadata'],
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_pdf_export_translation(sample_data):
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            result = exporter.export_translation_result(
                original_text=sample_data['original_text'],
                translated_text=sample_data['translated_text'],
                metadata=sample_data['metadata'],
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_docx_export_content(sample_pdf_data):
    exporter = DOCXExporter()
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        try:
            result = exporter.export_content(
                content=sample_pdf_data,
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_pdf_export_content(sample_pdf_data):
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            result = exporter.export_content(
                content=sample_pdf_data,
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_pdf_story_reset():
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            # First export
            exporter.add_heading('Test 1')
            exporter.export_content(
                content={'title': 'Test 1', 'text': 'Content 1'},
                output_path=tmp_file.name
            )
            initial_size = os.path.getsize(tmp_file.name)
            
            # Reset story and second export
            exporter.story = []
            exporter.add_heading('Test 2')
            exporter.export_content(
                content={'title': 'Test 2', 'text': 'Content 2'},
                output_path=tmp_file.name
            )
            second_size = os.path.getsize(tmp_file.name)
            
            # Sizes should be similar (within 10% difference)
            size_ratio = second_size / initial_size
            assert 0.9 <= size_ratio <= 1.1
        finally:
            os.unlink(tmp_file.name)

def test_safe_metadata_handling(sample_data):
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            # Test with missing metadata fields
            incomplete_metadata = {
                'detected_lang': 'en'
                # missing config, processing_time, and confidence
            }
            result = exporter.export_translation_result(
                original_text=sample_data['original_text'],
                translated_text=sample_data['translated_text'],
                metadata=incomplete_metadata,
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)
