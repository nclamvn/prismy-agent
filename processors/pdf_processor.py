import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import layoutparser as lp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PDFAnalysis:
    page_count: int
    has_text: bool
    has_tables: bool
    has_images: bool
    has_formulas: bool
    is_scanned: bool
    layout_score: float
    complexity_score: float
    metadata: Dict[str, Any]

@dataclass
class PDFPage:
    page_number: int
    text_content: str
    tables: List[Dict]
    images: List[Dict]
    layout: Dict[str, Any]
    confidence: float

class PDFProcessor:
    def __init__(self):
        try:
            self.layout_model = lp.AutoLayoutModel('lp://PubLayNet')
            logger.info("Layout detection model loaded successfully")
            self.ocr_config = '--oem 3 --psm 6'
            self.supported_langs = {
                'eng': 'English',
                'vie': 'Vietnamese',
                'chi_sim': 'Chinese Simplified',
                'chi_tra': 'Chinese Traditional',
                'jpn': 'Japanese',
                'kor': 'Korean'
            }
            self.initialized = True
            logger.info("PDF Processor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize PDF Processor: {e}")
            self.initialized = False

    def analyze_pdf(self, pdf_path: str) -> PDFAnalysis:
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            has_text = any(page.extract_text() and page.extract_text().strip() for page in pdf.pages)
            has_tables = any(len(page.extract_tables()) > 0 for page in pdf.pages)
            has_images = any(page.images for page in pdf.pages)
            is_scanned = self._check_if_scanned(pdf)
            layout_score = self._analyze_layout_complexity(pdf)
            complexity_score = self._calculate_complexity_score(page_count, has_tables, has_images, layout_score)
            metadata = pdf.metadata or {}
            return PDFAnalysis(
                page_count=page_count,
                has_text=has_text,
                has_tables=has_tables,
                has_images=has_images,
                has_formulas=False,
                is_scanned=is_scanned,
                layout_score=layout_score,
                complexity_score=complexity_score,
                metadata=metadata
            )

    def _check_if_scanned(self, pdf) -> bool:
        # Heuristic: if pages have no extractable text but have images, likely scanned
        for page in pdf.pages:
            text = page.extract_text()
            if text and text.strip():
                return False
        return True

    def _analyze_layout_complexity(self, pdf) -> float:
        # Use layoutparser to analyze complexity of first page as proxy
        first_page = pdf.pages[0]
        image = first_page.to_image(resolution=150).original
        layout = self.layout_model.detect(image)
        # Complexity score based on number of layout elements
        score = len(layout) / 50.0  # Normalize by 50 elements
        return min(score, 1.0)

    def _calculate_complexity_score(self, page_count, has_tables, has_images, layout_score) -> float:
        score = 0.1 * min(page_count / 10, 1.0)
        score += 0.3 if has_tables else 0.0
        score += 0.2 if has_images else 0.0
        score += 0.4 * layout_score
        return min(score, 1.0)

    def extract_text_content(self, pdf_path: str) -> Dict[str, Any]:
        pages = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                tables = page.extract_tables()
                images = page.images
                layout = self.layout_model.detect(page.to_image(resolution=150).original)
                confidence = 0.9  # Placeholder for confidence
                pages.append({
                    'page_number': i + 1,
                    'text': text,
                    'tables': tables,
                    'images': images,
                    'layout': layout,
                    'confidence': confidence
                })
        full_text = "\n\n".join(p['text'] for p in pages)
        return {
            'pages': pages,
            'full_text': full_text,
            'confidence': 0.9
        }

    def process_pdf_ocr(self, pdf_path: str, lang: str = 'eng') -> Dict[str, Any]:
        images = convert_from_path(pdf_path, dpi=300)
        full_text = ""
        pages = []
        for i, image in enumerate(images):
            img_np = np.array(image)
            text = pytesseract.image_to_string(img_np, lang=lang, config=self.ocr_config)
            confidence = 0.85  # Placeholder
            pages.append({
                'page_number': i + 1,
                'text': text,
                'confidence': confidence
            })
            full_text += text + "\n\n"
        return {
            'pages': pages,
            'full_text': full_text,
            'confidence': 0.85
        }
