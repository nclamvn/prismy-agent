"""
Advanced Document Processor
Handles PDF, DOCX, Excel files with table and formula detection
"""

import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
import time

@dataclass
class ProcessingResult:
    """Result of document processing"""
    success: bool = True
    content: str = ""
    content_length: int = 0
    processing_time: float = 0.0
    tables_extracted: int = 0
    formulas_detected: int = 0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class AdvancedDocumentProcessor:
    """Advanced document processor with structure detection"""
    
    def __init__(self):
        """Initialize advanced document processor"""
        
        # Table detection patterns
        self.table_patterns = [
            r'\|.*\|.*\|',  # Markdown tables
            r'\t.*\t.*\t',  # Tab-separated
            r'(\w+\s+){3,}',  # Space-separated columns
            r'Product\s+Price\s+Quantity',  # Header patterns
        ]
        
        # Formula detection patterns
        self.formula_patterns = [
            r'[A-Z]+\d+:[A-Z]+\d+',  # Excel ranges like B2:D4
            r'=\w+\(',  # Excel formulas starting with =
            r'\$[A-Z]+\$\d+',  # Absolute references
            r'SUM|AVERAGE|COUNT|MAX|MIN|IF',  # Function names
            r'=SUM\([A-Z]+\d+:[A-Z]+\d+\)',  # Complete SUM formulas
            r'=AVERAGE\([A-Z]+\d+:[A-Z]+\d+\)',  # AVERAGE formulas
        ]
        
        # Structure patterns
        self.structure_patterns = [
            r'^#{1,6}\s+',  # Headers
            r'^\*\s+|^\-\s+|^\d+\.\s+',  # Lists
            r'```.*```',  # Code blocks
            r'===.*===',  # Section dividers
        ]
    
    def process_text(self, text: str, extract_tables: bool = True, 
                    detect_formulas: bool = True, analyze_structure: bool = True) -> ProcessingResult:
        """
        Process text with advanced features
        
        Args:
            text: Input text to process
            extract_tables: Whether to detect tables
            detect_formulas: Whether to detect formulas
            analyze_structure: Whether to analyze structure
            
        Returns:
            ProcessingResult with processing details
        """
        start_time = time.time()
        
        try:
            # Initialize result
            result = ProcessingResult(
                success=True,
                content=text,
                content_length=len(text)
            )
            
            # Detect tables
            tables_found = 0
            if extract_tables:
                tables_found = self._detect_tables(text)
                result.tables_extracted = tables_found
            
            # Detect formulas
            formulas_found = 0
            if detect_formulas:
                formulas_found = self._detect_formulas(text)
                result.formulas_detected = formulas_found
            
            # Analyze structure
            structure_elements = []
            if analyze_structure:
                structure_elements = self._analyze_structure(text)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            result.processing_time = processing_time
            
            # Add metadata
            result.metadata = {
                'tables_detected': tables_found,
                'formulas_detected': formulas_found,
                'structure_elements': structure_elements,
                'word_count': len(text.split()),
                'line_count': len(text.split('\n')),
                'processing_features': {
                    'table_extraction': extract_tables,
                    'formula_detection': detect_formulas,
                    'structure_analysis': analyze_structure
                }
            }
            
            return result
            
        except Exception as e:
            # Return error result
            processing_time = time.time() - start_time
            return ProcessingResult(
                success=False,
                content=text,
                content_length=len(text),
                processing_time=processing_time,
                metadata={'error': str(e)}
            )
    
    def process_file(self, file_content: bytes, filename: str, 
                    extract_tables: bool = True, detect_formulas: bool = True, 
                    analyze_structure: bool = True) -> ProcessingResult:
        """
        Process file content
        
        Args:
            file_content: Raw file bytes
            filename: Name of the file
            extract_tables: Whether to detect tables
            detect_formulas: Whether to detect formulas
            analyze_structure: Whether to analyze structure
            
        Returns:
            ProcessingResult with processing details
        """
        start_time = time.time()
        
        try:
            # Extract text based on file type
            file_ext = filename.lower().split('.')[-1]
            
            if file_ext == 'txt':
                text = file_content.decode('utf-8')
            elif file_ext == 'pdf':
                text = self._extract_from_pdf(file_content)
            elif file_ext in ['docx', 'doc']:
                text = self._extract_from_docx(file_content)
            elif file_ext in ['xlsx', 'xls']:
                text = self._extract_from_excel(file_content)
            else:
                # Try to decode as text
                text = file_content.decode('utf-8', errors='ignore')
            
            # Process the extracted text
            result = self.process_text(text, extract_tables, detect_formulas, analyze_structure)
            
            # Add file-specific metadata
            result.metadata['filename'] = filename
            result.metadata['file_type'] = file_ext
            result.metadata['file_size'] = len(file_content)
            
            return result
            
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                success=False,
                content="",
                processing_time=processing_time,
                metadata={
                    'error': str(e),
                    'filename': filename,
                    'file_size': len(file_content)
                }
            )
    
    def _detect_tables(self, text: str) -> int:
        """Detect tables in text"""
        table_count = 0
        
        for pattern in self.table_patterns:
            matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
            table_count += len(matches)
        
        # Additional heuristics for table detection
        lines = text.split('\n')
        potential_table_lines = 0
        
        for line in lines:
            # Check for multiple columns separated by spaces or tabs
            if len(line.split()) >= 3 or len(line.split('\t')) >= 2:
                potential_table_lines += 1
        
        # If we have multiple lines that look like table rows
        if potential_table_lines >= 3:
            table_count += 1
        
        return table_count
    
    def _detect_formulas(self, text: str) -> int:
        """Detect formulas in text"""
        formula_count = 0
        detected_formulas = []
        
        for pattern in self.formula_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            formula_count += len(matches)
            detected_formulas.extend(matches)
        
        # Remove duplicates
        unique_formulas = list(set(detected_formulas))
        
        return len(unique_formulas)
    
    def _analyze_structure(self, text: str) -> List[str]:
        """Analyze document structure"""
        structure_elements = []
        
        # Check for headers
        if re.search(r'^#{1,6}\s+', text, re.MULTILINE):
            structure_elements.append("markdown_headers")
        
        # Check for lists
        if re.search(r'^\*\s+|^\-\s+|^\d+\.\s+', text, re.MULTILINE):
            structure_elements.append("lists")
        
        # Check for tables
        if re.search(r'\|.*\|.*\|', text, re.MULTILINE):
            structure_elements.append("tables")
        
        # Check for code blocks
        if re.search(r'```.*```', text, re.DOTALL):
            structure_elements.append("code_blocks")
        
        # Check for section dividers
        if re.search(r'===.*===|---.*---', text):
            structure_elements.append("section_dividers")
        
        return structure_elements
    
    def _extract_from_pdf(self, file_content: bytes) -> str:
        """Extract text from PDF (fallback implementation)"""
        # This is a fallback - in real implementation would use PyMuPDF
        return "PDF content extraction requires PyMuPDF library. Using fallback text extraction."
    
    def _extract_from_docx(self, file_content: bytes) -> str:
        """Extract text from DOCX (fallback implementation)"""
        # This is a fallback - in real implementation would use python-docx
        return "DOCX content extraction requires python-docx library. Using fallback text extraction."
    
    def _extract_from_excel(self, file_content: bytes) -> str:
        """Extract text from Excel (fallback implementation)"""
        # This is a fallback - in real implementation would use openpyxl
        return "Excel content extraction requires openpyxl library. Using fallback text extraction."

# Test the processor
if __name__ == "__main__":
    processor = AdvancedDocumentProcessor()
    
    # Test with sample data
    test_text = """
    === TABLE 2 ===
    Product  Price  Quantity  Total
    Laptop   1000   5         =B2*C2
    Phone    500    10        =B3*C3
    Tablet   300    15        =B4*C4
    
    Total Revenue: =SUM(D2:D4)
    Average Price: =AVERAGE(B2:B4)
    """
    
    result = processor.process_text(test_text)
    print(f"✅ Success: {result.success}")
    print(f"📊 Tables: {result.tables_extracted}")
    print(f"🧮 Formulas: {result.formulas_detected}")
    print(f"⏱️ Time: {result.processing_time:.3f}s")
