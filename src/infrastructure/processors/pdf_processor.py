# src/infrastructure/processors/pdf_processor.py
import io
import time
from typing import Union, BinaryIO, List
import logging

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PyPDF2 = None
    PYPDF2_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None
    PDFPLUMBER_AVAILABLE = False

from src.core.interfaces.document_processing import DocumentProcessor, ProcessingResult

logger = logging.getLogger(__name__)

class PDFProcessor(DocumentProcessor):
    """PDF processor with multiple extraction methods"""
    
    def __init__(self, method: str = "auto"):
        """Initialize PDF processor"""
        self.method = method
        self.supported_formats = ['.pdf']
        
        # Check available methods
        if method == "pypdf2" and not PYPDF2_AVAILABLE:
            logger.warning("PyPDF2 not available, falling back to basic extraction")
        elif method == "pdfplumber" and not PDFPLUMBER_AVAILABLE:
            logger.warning("pdfplumber not available, falling back to PyPDF2")
    
    def process(self, file_content: Union[bytes, BinaryIO], filename: str) -> ProcessingResult:
        """Process PDF file and extract text"""
        start_time = time.time()
        
        try:
            # Convert to bytes if needed
            if hasattr(file_content, 'read'):
                pdf_bytes = file_content.read()
            else:
                pdf_bytes = file_content
            
            # Validate file
            if not self.validate_file(pdf_bytes, filename):
                return ProcessingResult(
                    success=False,
                    text="",
                    metadata={},
                    error_message="Invalid PDF file"
                )
            
            # Try different extraction methods
            result = self._extract_text_auto(pdf_bytes)
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                success=True,
                text=result['text'],
                metadata={
                    'method': result['method'],
                    'page_count': result['page_count'],
                    'filename': filename,
                    'has_images': result.get('has_images', False),
                    'has_tables': result.get('has_tables', False)
                },
                processing_time=processing_time,
                page_count=result['page_count'],
                file_size=len(pdf_bytes)
            )
            
        except Exception as e:
            logger.error(f"Error processing PDF {filename}: {str(e)}")
            return ProcessingResult(
                success=False,
                text="",
                metadata={'filename': filename},
                error_message=f"PDF processing failed: {str(e)}",
                processing_time=time.time() - start_time
            )
    
    def _extract_text_auto(self, pdf_bytes: bytes) -> dict:
        """Auto-select best extraction method"""
        
        # Try pdfplumber first (more accurate)
        if PDFPLUMBER_AVAILABLE:
            try:
                result = self._extract_with_pdfplumber(pdf_bytes)
                result['method'] = 'pdfplumber'
                return result
            except Exception as e:
                logger.warning(f"pdfplumber failed: {e}, trying PyPDF2...")
        
        # Fall back to PyPDF2
        if PYPDF2_AVAILABLE:
            try:
                result = self._extract_with_pypdf2(pdf_bytes)
                result['method'] = 'pypdf2'
                return result
            except Exception as e:
                logger.warning(f"PyPDF2 failed: {e}, using basic extraction...")
        
        # Basic extraction as last resort
        return self._extract_basic(pdf_bytes)
    
    def _extract_with_pdfplumber(self, pdf_bytes: bytes) -> dict:
        """Extract text using pdfplumber"""
        text_parts = []
        page_count = 0
        has_tables = False
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            page_count = len(pdf.pages)
            
            for page in pdf.pages:
                # Extract text
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
                
                # Check for tables
                tables = page.extract_tables()
                if tables:
                    has_tables = True
                    for table in tables:
                        table_text = self._process_table(table)
                        text_parts.append(table_text)
        
        return {
            'text': '\n\n'.join(text_parts),
            'page_count': page_count,
            'has_tables': has_tables,
            'has_images': False
        }
    
    def _extract_with_pypdf2(self, pdf_bytes: bytes) -> dict:
        """Extract text using PyPDF2"""
        text_parts = []
        
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        page_count = len(pdf_reader.pages)
        
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text.strip():
                text_parts.append(text)
        
        return {
            'text': '\n\n'.join(text_parts),
            'page_count': page_count,
            'has_tables': False,
            'has_images': False
        }
    
    def _extract_basic(self, pdf_bytes: bytes) -> dict:
        """Basic extraction fallback"""
        return {
            'text': f"PDF file detected ({len(pdf_bytes)} bytes) but no extraction library available. Please install PyPDF2 or pdfplumber.",
            'page_count': 1,
            'has_tables': False,
            'has_images': False,
            'method': 'basic_fallback'
        }
    
    def _process_table(self, table: List[List]) -> str:
        """Convert table data to readable text"""
        if not table:
            return ""
        
        processed_rows = []
        for row in table:
            if row:
                processed_row = [str(cell) if cell is not None else "" for cell in row]
                processed_rows.append(" | ".join(processed_row))
        
        return "\n".join(processed_rows)
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        return self.supported_formats
    
    def validate_file(self, file_content: Union[bytes, BinaryIO], filename: str) -> bool:
        """Validate if file is a valid PDF"""
        try:
            # Check file extension
            if not filename.lower().endswith('.pdf'):
                return False
            
            # Convert to bytes if needed
            if hasattr(file_content, 'read'):
                pdf_bytes = file_content.read()
                file_content.seek(0)  # Reset position
            else:
                pdf_bytes = file_content
            
            # Check PDF header
            if not pdf_bytes.startswith(b'%PDF'):
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"PDF validation error: {str(e)}")
            return False
