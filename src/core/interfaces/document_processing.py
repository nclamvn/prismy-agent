# src/core/interfaces/document_processing.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, BinaryIO
from dataclasses import dataclass
from enum import Enum

class DocumentType(Enum):
    PDF = "pdf"
    IMAGE = "image"
    DOCX = "docx"

@dataclass
class ProcessingResult:
    """Result of document processing operation"""
    success: bool
    text: str
    metadata: Dict
    error_message: Optional[str] = None
    processing_time: float = 0.0
    page_count: Optional[int] = None
    file_size: Optional[int] = None

@dataclass
class OCRResult:
    """Result of OCR operation"""
    text: str
    confidence: float
    bounding_boxes: List[Dict]
    processing_time: float
    language: str = "en"

class DocumentProcessor(ABC):
    """Abstract base class for document processors"""
    
    @abstractmethod
    def process(self, file_content: Union[bytes, BinaryIO], filename: str) -> ProcessingResult:
        """Process document and extract text"""
        pass
    
    @abstractmethod
    def get_supported_formats(self) -> List[str]:
        """Get list of supported file formats"""
        pass
    
    @abstractmethod
    def validate_file(self, file_content: Union[bytes, BinaryIO], filename: str) -> bool:
        """Validate if file can be processed"""
        pass

class OCREngine(ABC):
    """Abstract base class for OCR engines"""
    
    @abstractmethod
    def extract_text(self, image_data: bytes, language: str = "en") -> OCRResult:
        """Extract text from image using OCR"""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        pass
    
    @abstractmethod
    def set_confidence_threshold(self, threshold: float) -> None:
        """Set minimum confidence threshold for text extraction"""
        pass

class FormulaProcessor(ABC):
    """Abstract base class for formula processors"""
    
    @abstractmethod
    def detect_formulas(self, text: str) -> List[Dict]:
        """Detect mathematical formulas in text"""
        pass
    
    @abstractmethod
    def process_latex(self, formula: str) -> str:
        """Process LaTeX formula"""
        pass
    
    @abstractmethod
    def process_mathml(self, formula: str) -> str:
        """Process MathML formula"""
        pass
