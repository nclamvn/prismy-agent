import pytest
import os
import tempfile
from exporters.docx_exporter import DOCXExporter
from exporters.pdf_exporter import PDFExporter
import pandas as pd

@pytest.fixture
def complex_data():
    return {
        'title': 'Complex Test Document',
        'text': {
            'content': 'This is a complex text content',
            'metadata': {'type': 'paragraph'}
        },
        'translation': {
            'translated_text': 'This is translated content',
            'metadata': {'confidence': 0.95}
        },
        'tables': {
            'tables': [
                pd.DataFrame({
                    'Col1': ['A1', 'A2'],
                    'Col2': ['B1', 'B2']
                })
            ]
        }
    }

def test_docx_complex_content(complex_data):
    exporter = DOCXExporter()
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        try:
            result = exporter.export_content(
                content=complex_data,
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_pdf_complex_content(complex_data):
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            result = exporter.export_content(
                content=complex_data,
                output_path=tmp_file.name
            )
            assert result is True
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_docx_error_handling():
    exporter = DOCXExporter()
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        try:
            # Test invalid table data
            result = exporter.export_content(
                content={
                    'title': 'Error Test',
                    'tables': {'tables': [None]}  # Invalid table data
                },
                output_path=tmp_file.name
            )
            assert result is True  # Should handle error gracefully
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
            
            # Test invalid file path
            result = exporter.export_content(
                content={'title': 'Error Test'},
                output_path='/nonexistent/path/file.docx'
            )
            assert result is False
        finally:
            os.unlink(tmp_file.name)

def test_pdf_error_handling():
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            # Test invalid table data
            result = exporter.export_content(
                content={
                    'title': 'Error Test',
                    'tables': {'tables': [None]}  # Invalid table data
                },
                output_path=tmp_file.name
            )
            assert result is True  # Should handle error gracefully
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
            
            # Test invalid file path
            result = exporter.export_content(
                content={'title': 'Error Test'},
                output_path='/nonexistent/path/file.pdf'
            )
            assert result is False
        finally:
            os.unlink(tmp_file.name)

def test_docx_style_customization():
    exporter = DOCXExporter()
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as tmp_file:
        try:
            # Test custom paragraph alignment
            exporter.add_paragraph('Left aligned', alignment='LEFT')
            exporter.add_paragraph('Center aligned', alignment='CENTER')
            exporter.add_paragraph('Right aligned', alignment='RIGHT')
            
            # Test different heading levels
            exporter.add_heading('Level 1 Heading', level=1)
            exporter.add_heading('Level 2 Heading', level=2)
            exporter.add_heading('Level 3 Heading', level=3)
            
            exporter.document.save(tmp_file.name)
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)

def test_pdf_style_customization():
    exporter = PDFExporter()
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_file:
        try:
            # Test different heading levels
            exporter.add_heading('Level 1 Heading', level=1)
            exporter.add_heading('Level 2 Heading', level=2)
            exporter.add_heading('Level 3 Heading', level=3)
            
            # Test paragraph content
            exporter.add_paragraph('Test paragraph content')
            
            # Build the PDF
            doc = exporter.export_content(
                content={'title': 'Style Test'},
                output_path=tmp_file.name
            )
            assert os.path.exists(tmp_file.name)
            assert os.path.getsize(tmp_file.name) > 0
        finally:
            os.unlink(tmp_file.name)
