import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
import tempfile

logger = logging.getLogger(__name__)

class OCREngine:
    """Advanced OCR processing for scanned documents and images"""

    def __init__(self):
        self.supported_languages = {
            'eng': 'English',
            'vie': 'Vietnamese',
            'chi_sim': 'Chinese Simplified',
            'chi_tra': 'Chinese Traditional',
            'jpn': 'Japanese',
            'kor': 'Korean',
            'fra': 'French',
            'deu': 'German',
            'spa': 'Spanish',
            'ita': 'Italian',
            'por': 'Portuguese'
        }
        
        # OCR configurations for different scenarios
        self.configs = {
            'default': '--oem 3 --psm 6',
            'table': '--oem 3 --psm 6 -c preserve_interword_spaces=1',
            'formula': '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.+-*/(){}[]',
            'columns': '--oem 3 --psm 1'  # Automatic page segmentation with OSD
        }
        
        self._initialize_preprocessing()
    
    def _initialize_preprocessing(self):
        """Initialize image preprocessing parameters"""
        self.preprocessing_steps = {
            'basic': [
                ('resize', {'width': 3000}),
                ('denoise', {'strength': 10}),
                ('threshold', {'method': 'adaptive'})
            ],
            'complex': [
                ('resize', {'width': 3000}),
                ('denoise', {'strength': 15}),
                ('deskew', {}),
                ('threshold', {'method': 'otsu'})
            ]
        }
    
    def preprocess_image(self, image: np.ndarray, pipeline: str = 'basic') -> np.ndarray:
        """Apply preprocessing pipeline to improve OCR accuracy"""
        steps = self.preprocessing_steps.get(pipeline, self.preprocessing_steps['basic'])
        img = image.copy()
        
        for step, params in steps:
            try:
                if step == 'resize':
                    height = int(img.shape[0] * (params['width'] / img.shape[1]))
                    img = cv2.resize(img, (params['width'], height))
                
                elif step == 'denoise':
                    img = cv2.fastNlMeansDenoisingColored(img, None, params['strength'], 10, 7, 21)
                
                elif step == 'deskew':
                    coords = np.column_stack(np.where(img > 0))
                    angle = cv2.minAreaRect(coords)[-1]
                    if angle < -45:
                        angle = 90 + angle
                    (h, w) = img.shape[:2]
                    center = (w // 2, h // 2)
                    M = cv2.getRotationMatrix2D(center, angle, 1.0)
                    img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
                
                elif step == 'threshold':
                    if params['method'] == 'adaptive':
                        img = cv2.adaptiveThreshold(
                            cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                            255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
                        )
                    else:  # otsu
                        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                        img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                
            except Exception as e:
                logger.warning(f"Preprocessing step {step} failed: {e}")
                continue
        
        return img
    
    def process_pdf_ocr(self, pdf_path: str, lang: str = 'eng', mode: str = 'default') -> Dict[str, Any]:
        """Process PDF with OCR, supporting multiple languages and modes"""
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path, dpi=300)
            results = []
            total_confidence = 0
            
            for i, image in enumerate(images):
                # Convert PIL image to OpenCV format
                img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Preprocess image
                preprocessed = self.preprocess_image(img_cv, 'complex')
                
                # Get OCR data with confidence
                ocr_data = pytesseract.image_to_data(
                    preprocessed,
                    lang=lang,
                    config=self.configs[mode],
                    output_type=pytesseract.Output.DICT
                )
                
                # Extract text and confidence
                text_parts = []
                conf_sum = 0
                conf_count = 0
                
                for j, conf in enumerate(ocr_data['conf']):
                    if conf > 0:  # Valid confidence score
                        text = ocr_data['text'][j]
                        if text.strip():
                            text_parts.append(text)
                            conf_sum += conf
                            conf_count += 1
                
                # Calculate page confidence
                page_confidence = conf_sum / conf_count if conf_count > 0 else 0
                total_confidence += page_confidence
                
                # Store page results
                results.append({
                    'page_number': i + 1,
                    'text': ' '.join(text_parts),
                    'confidence': page_confidence / 100,  # Convert to 0-1 scale
                    'word_count': len(text_parts),
                    'character_count': sum(len(t) for t in text_parts)
                })
            
            # Combine results
            full_text = '\n\n'.join(page['text'] for page in results)
            avg_confidence = (total_confidence / len(images)) / 100
            
            return {
                'pages': results,
                'full_text': full_text,
                'total_confidence': avg_confidence,
                'language': self.supported_languages.get(lang, 'Unknown'),
                'processing_mode': mode,
                'total_pages': len(images)
            }
            
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            raise
    
    def detect_language(self, image: np.ndarray) -> str:
        """Detect the primary language in an image"""
        try:
            # Use tesseract's language detection
            osd = pytesseract.image_to_osd(image)
            script_confidence = float(osd.split('Script confidence: ')[1].split('\n')[0])
            
            if script_confidence > 50:
                # If script is detected with high confidence, try language detection
                sample_text = pytesseract.image_to_string(image, lang='eng+vie+chi_sim+jpn')
                # Implement language detection logic based on character sets
                if any('\u4e00' <= char <= '\u9fff' for char in sample_text):
                    return 'chi_sim'
                elif any('\u3040' <= char <= '\u309f' or '\u30a0' <= char <= '\u30ff' for char in sample_text):
                    return 'jpn'
                elif any('ă' in sample_text or 'đ' in sample_text or 'ơ' in sample_text):
                    return 'vie'
                else:
                    return 'eng'
            else:
                return 'eng'  # Default to English if unsure
                
        except Exception as e:
            logger.warning(f"Language detection failed: {e}")
            return 'eng'  # Default to English on error
    
    def enhance_text_recognition(self, image: np.ndarray, lang: str = 'eng') -> Dict[str, Any]:
        """Enhanced text recognition with multiple preprocessing attempts"""
        best_result = {'text': '', 'confidence': 0}
        
        # Try different preprocessing pipelines
        for pipeline in ['basic', 'complex']:
            try:
                processed = self.preprocess_image(image, pipeline)
                ocr_data = pytesseract.image_to_data(
                    processed,
                    lang=lang,
                    config=self.configs['default'],
                    output_type=pytesseract.Output.DICT
                )
                
                # Calculate confidence and extract text
                valid_conf = [c for c in ocr_data['conf'] if c > 0]
                if valid_conf:
                    confidence = sum(valid_conf) / len(valid_conf)
                    text = ' '.join(
                        word for i, word in enumerate(ocr_data['text'])
                        if word.strip() and ocr_data['conf'][i] > 0
                    )
                    
                    if confidence > best_result['confidence']:
                        best_result = {
                            'text': text,
                            'confidence': confidence / 100,
                            'pipeline': pipeline,
                            'word_count': len(text.split()),
                            'character_count': len(text)
                        }
            
            except Exception as e:
                logger.warning(f"Enhancement pipeline {pipeline} failed: {e}")
                continue
        
        return best_result
