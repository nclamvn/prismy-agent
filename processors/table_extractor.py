import pdfplumber
import pandas as pd
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class TableExtractor:
    """Extract tables from PDF pages and convert to structured data"""

    def extract_tables_from_page(self, page) -> List[Dict[str, Any]]:
        """Extract tables from a single pdfplumber page"""
        tables = []
        raw_tables = page.extract_tables()
        for i, raw_table in enumerate(raw_tables):
            try:
                df = pd.DataFrame(raw_table[1:], columns=raw_table[0])
                tables.append({
                    'table_id': i,
                    'dataframe': df,
                    'rows_count': df.shape[0],
                    'columns_count': df.shape[1],
                    'headers': list(df.columns)
                })
            except Exception as e:
                logger.warning(f"Failed to parse table {i} on page {page.page_number}: {e}")
        return tables

    def extract_tables_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract tables from all pages of a PDF"""
        tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_tables = self.extract_tables_from_page(page)
                for table in page_tables:
                    table['page_number'] = page.page_number
                tables.extend(page_tables)
        return {
            'tables': tables,
            'total_tables': len(tables)
        }
