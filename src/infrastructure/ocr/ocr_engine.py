# src/infrastructure/ocr/ocr_engine.py
import io
import time
from typing import List, Dict
import logging

# Simple path setup
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    import pytesseract
    from PIL import Image
    TESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    Image = None
    TESSERACT_AVAILABLE = False

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    easyocr = None
    EASYOCR_AVAILABLE = False

# Import or define OCR classes
try:
    from src.core.interfaces.document_processing import OCREngine, OCRResult
except ImportError:
    from dataclasses import dataclass
    from typing import List, Dict
    
    @dataclass
    class OCRResult:
        text: str
        confidence: float
        bounding_boxes: List[Dict]
        processing_time: float
        language: str = "en"
    
    class OCREngine:
        def extract_text(self, image_data, language="en"):
            pass
        def get_supported_languages(self):
            pass
        def set_confidence_threshold(self, threshold):
            pass

logger = logging.getLogger(__name__)

class TesseractOCREngine(OCREngine):
    """Simple Tesseract OCR engine"""
    
    def __init__(self, language: str = "eng"):
        self.default_language = language
        self.confidence_threshold = 0.0
        self.available = TESSERACT_AVAILABLE
    
    def extract_text(self, image_data: bytes, language: str = None) -> OCRResult:
        """Extract text from image using Tesseract OCR"""
        start_time = time.time()
        
        if not self.available:
            return OCRResult(
                text="Tesseract OCR not available. Please install: pip install pytesseract pillow",
                confidence=0.0,
                bounding_boxes=[],
                processing_time=time.time() - start_time,
                language=language or self.default_language
            )
        
        try:
            if language is None:
                language = self.default_language
            
            # Open image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text
            text = pytesseract.image_to_string(image, lang=language)
            
            processing_time = time.time() - start_time
            
            return OCRResult(
                text=text,
                confidence=85.0,  # Default confidence
                bounding_boxes=[],
                processing_time=processing_time,
                language=language
            )
            
        except Exception as e:
            return OCRResult(
                text=f"OCR extraction failed: {str(e)}",
                confidence=0.0,
                bounding_boxes=[],
                processing_time=time.time() - start_time,
                language=language or self.default_language
            )
    
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        if self.available:
            try:
                langs = pytesseract.get_languages(config='')
                return langs
            except:
                pass
        
        return ['eng', 'vie', 'fra', 'deu', 'spa']
    
    def set_confidence_threshold(self, threshold: float) -> None:
        """Set minimum confidence threshold"""
        self.confidence_threshold = threshold

class OCREngineFactory:
    """Factory for creating OCR engines"""
    
    @staticmethod
    def create_engine(engine_type: str = "tesseract", **kwargs):
        """Create OCR engine instance"""
        if engine_type.lower() == "tesseract":
            return TesseractOCREngine(**kwargs)
        else:
            raise ValueError(f"Unknown OCR engine type: {engine_type}")
    
    @staticmethod
    def get_available_engines() -> List[str]:
        """Get list of available OCR engines"""
        engines = []
        if TESSERACT_AVAILABLE:
            engines.append("tesseract")
        if EASYOCR_AVAILABLE:
            engines.append("easyocr")
        return engines
