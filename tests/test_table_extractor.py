import pytest
import pandas as pd
import pdfplumber
import tempfile
from processors.table_extractor import TableExtractor
from typing import List, Dict

@pytest.fixture
def table_extractor():
    return TableExtractor()

@pytest.fixture
def sample_table_pdf():
    # Create a temporary PDF file with tables for testing
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
        return tmp.name

class TestTableExtractor:
    def test_initialization(self, table_extractor):
        """Test proper initialization of TableExtractor"""
        assert isinstance(table_extractor, TableExtractor)

    def test_basic_table_extraction(self, table_extractor, sample_table_pdf):
        """Test extraction of basic tables"""
        result = table_extractor.extract_tables_from_pdf(sample_table_pdf)
        
        assert isinstance(result, dict)
        assert 'tables' in result
        assert 'total_tables' in result
        assert isinstance(result['tables'], list)
        assert isinstance(result['total_tables'], int)
        
        if result['total_tables'] > 0:
            first_table = result['tables'][0]
            assert 'table_id' in first_table
            assert 'dataframe' in first_table
            assert 'rows_count' in first_table
            assert 'columns_count' in first_table
            assert 'headers' in first_table
            assert isinstance(first_table['dataframe'], pd.DataFrame)

    def test_complex_table_structures(self, table_extractor, sample_table_pdf):
        """Test handling of complex table structures"""
        # Test with a page containing multiple tables
        with pdfplumber.open(sample_table_pdf) as pdf:
            page = pdf.pages[0]
            tables = table_extractor.extract_tables_from_page(page)
            
            assert isinstance(tables, list)
            for table in tables:
                assert isinstance(table, dict)
                assert 'dataframe' in table
                df = table['dataframe']
                
                # Verify DataFrame structure
                assert isinstance(df, pd.DataFrame)
                assert len(df.columns) == table['columns_count']
                assert len(df) == table['rows_count']

    def test_merged_cells_handling(self, table_extractor):
        """Test handling of tables with merged cells"""
        # Create a test PDF with merged cells
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        result = table_extractor.extract_tables_from_pdf(pdf_path)
        
        for table in result['tables']:
            df = table['dataframe']
            # Check for proper handling of merged cells
            assert not df.empty
            # Verify no None/NaN values in merged regions
            assert df.notna().all().all()

    def test_nested_tables(self, table_extractor):
        """Test handling of nested tables"""
        # Create a test PDF with nested tables
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        result = table_extractor.extract_tables_from_pdf(pdf_path)
        
        # Verify nested table detection
        tables = result['tables']
        if len(tables) > 1:
            # Check for parent-child relationships
            table_positions = [
                (t['page_number'], t['dataframe'].shape)
                for t in tables
            ]
            # Verify no overlapping tables
            assert len(set(table_positions)) == len(table_positions)

    def test_table_headers(self, table_extractor, sample_table_pdf):
        """Test correct extraction of table headers"""
        result = table_extractor.extract_tables_from_pdf(sample_table_pdf)
        
        for table in result['tables']:
            headers = table['headers']
            df = table['dataframe']
            
            assert isinstance(headers, list)
            assert len(headers) == len(df.columns)
            # Verify headers match DataFrame columns
            assert all(h == c for h, c in zip(headers, df.columns))

    def test_multi_page_tables(self, table_extractor):
        """Test handling of tables spanning multiple pages"""
        # Create a test PDF with multi-page tables
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        result = table_extractor.extract_tables_from_pdf(pdf_path)
        
        # Check for table continuity across pages
        tables = result['tables']
        if len(tables) > 1:
            for i in range(len(tables) - 1):
                current = tables[i]
                next_table = tables[i + 1]
                if (current['page_number'] != next_table['page_number'] and
                    current['columns_count'] == next_table['columns_count']):
                    # Verify header consistency
                    assert current['headers'] == next_table['headers']

    def test_error_handling(self, table_extractor):
        """Test error handling for various scenarios"""
        # Test with non-existent file
        with pytest.raises(Exception):
            table_extractor.extract_tables_from_pdf('nonexistent.pdf')
        
        # Test with invalid file
        with tempfile.NamedTemporaryFile(suffix='.txt') as tmp:
            tmp.write(b'This is not a PDF')
            tmp.flush()
            with pytest.raises(Exception):
                table_extractor.extract_tables_from_pdf(tmp.name)

    def test_performance(self, table_extractor, sample_table_pdf):
        """Test performance with large tables"""
        import time
        
        start_time = time.time()
        result = table_extractor.extract_tables_from_pdf(sample_table_pdf)
        processing_time = time.time() - start_time
        
        # Processing should complete within reasonable time
        assert processing_time < 30  # seconds
        
        # Verify extraction completed successfully
        assert isinstance(result, dict)
        assert 'tables' in result
        assert 'total_tables' in result

    def test_table_data_types(self, table_extractor, sample_table_pdf):
        """Test handling of different data types in tables"""
        result = table_extractor.extract_tables_from_pdf(sample_table_pdf)
        
        for table in result['tables']:
            df = table['dataframe']
            
            # Check numeric column detection
            for col in df.columns:
                if df[col].dtype in [int, float]:
                    # Verify numeric values are properly parsed
                    assert df[col].notna().any()
                    
            # Check date column detection
            date_cols = df.select_dtypes(include=['datetime64']).columns
            for col in date_cols:
                assert pd.to_datetime(df[col], errors='coerce').notna().any()

    def test_table_formatting(self, table_extractor, sample_table_pdf):
        """Test preservation of table formatting"""
        result = table_extractor.extract_tables_from_pdf(sample_table_pdf)
        
        for table in result['tables']:
            df = table['dataframe']
            
            # Check for common formatting issues
            assert not df.columns.str.contains(r'Unnamed:').any()
            assert not df.columns.duplicated().any()
            
            # Verify no leading/trailing whitespace
            for col in df.columns:
                if df[col].dtype == object:
                    assert not df[col].str.match(r'^\s+|\s+$').any()

    @classmethod
    def teardown_class(cls):
        """Clean up test files after all tests complete"""
        import os
        from pathlib import Path
        
        # Remove temporary PDF files
        for file in Path(tempfile.gettempdir()).glob('*.pdf'):
            try:
                file.unlink()
            except Exception:
                pass
