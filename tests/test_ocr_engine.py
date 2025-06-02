import pytest
import numpy as np
import cv2
from pathlib import Path
import tempfile
from processors.ocr_engine import OCREngine
import pytesseract
from pdf2image import convert_from_path

@pytest.fixture
def ocr_engine():
    return OCREngine()

@pytest.fixture
def sample_image():
    # Create a sample image with text for testing
    img = np.ones((300, 800), dtype=np.uint8) * 255
    cv2.putText(
        img, 'Sample Text', (50, 150),
        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2
    )
    return img

@pytest.fixture
def multilingual_image():
    # Create an image with text in multiple languages
    img = np.ones((600, 800), dtype=np.uint8) * 255
    # English text
    cv2.putText(
        img, 'Hello World', (50, 100),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
    )
    # Add other language text (simulated)
    return img

class TestOCREngine:
    def test_initialization(self, ocr_engine):
        """Test proper initialization of OCR Engine"""
        assert isinstance(ocr_engine, OCREngine)
        assert hasattr(ocr_engine, 'supported_languages')
        assert 'eng' in ocr_engine.supported_languages
        assert 'vie' in ocr_engine.supported_languages
        
        # Verify OCR configurations
        assert all(key in ocr_engine.configs for key in [
            'default', 'table', 'formula', 'columns'
        ])

    def test_image_preprocessing(self, ocr_engine, sample_image):
        """Test image preprocessing pipeline"""
        # Test basic preprocessing
        processed = ocr_engine.preprocess_image(sample_image, 'basic')
        assert isinstance(processed, np.ndarray)
        assert processed.shape[0] > 0 and processed.shape[1] > 0
        
        # Test complex preprocessing
        processed = ocr_engine.preprocess_image(sample_image, 'complex')
        assert isinstance(processed, np.ndarray)
        assert processed.shape[0] > 0 and processed.shape[1] > 0
        
        # Verify preprocessing improves image quality
        assert cv2.Laplacian(processed, cv2.CV_64F).var() >= \
               cv2.Laplacian(sample_image, cv2.CV_64F).var() * 0.8

    def test_language_detection(self, ocr_engine, multilingual_image):
        """Test language detection capabilities"""
        detected_lang = ocr_engine.detect_language(multilingual_image)
        assert detected_lang in ocr_engine.supported_languages
        
        # Test with different scripts
        for script_lang in ['eng', 'vie', 'chi_sim']:
            if script_lang in ocr_engine.supported_languages:
                # Create image with specific script
                img = np.ones((300, 800), dtype=np.uint8) * 255
                cv2.putText(
                    img, 'Text in ' + script_lang, (50, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2
                )
                detected = ocr_engine.detect_language(img)
                assert detected in ocr_engine.supported_languages

    def test_pdf_ocr_processing(self, ocr_engine):
        """Test PDF OCR processing"""
        # Create a test PDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            pdf_path = tmp.name
        
        result = ocr_engine.process_pdf_ocr(pdf_path, lang='eng')
        
        assert isinstance(result, dict)
        assert 'pages' in result
        assert 'full_text' in result
        assert 'total_confidence' in result
        
        # Test with different languages
        for lang in ['eng', 'vie']:
            if lang in ocr_engine.supported_languages:
                result = ocr_engine.process_pdf_ocr(pdf_path, lang=lang)
                assert result['language'] == ocr_engine.supported_languages[lang]

    def test_enhanced_text_recognition(self, ocr_engine, sample_image):
        """Test enhanced text recognition with multiple preprocessing attempts"""
        result = ocr_engine.enhance_text_recognition(sample_image)
        
        assert isinstance(result, dict)
        assert 'text' in result
        assert 'confidence' in result
        assert 'pipeline' in result
        assert 0 <= result['confidence'] <= 1
        
        # Test with different preprocessing pipelines
        for pipeline in ['basic', 'complex']:
            result = ocr_engine.enhance_text_recognition(
                sample_image, lang='eng'
            )
            assert result['pipeline'] in ['basic', 'complex']

    def test_error_handling(self, ocr_engine):
        """Test error handling for various scenarios"""
        # Test with invalid image
        with pytest.raises(Exception):
            ocr_engine.preprocess_image(None)
        
        # Test with invalid language
        with pytest.raises(Exception):
            ocr_engine.process_pdf_ocr('test.pdf', lang='invalid')
        
        # Test with corrupted image
        corrupt_image = np.zeros((10, 10), dtype=np.uint8)
        result = ocr_engine.enhance_text_recognition(corrupt_image)
        assert result['confidence'] < 0.5

    def test_performance(self, ocr_engine, sample_image):
        """Test performance and processing time"""
        import time
        
        # Test preprocessing performance
        start_time = time.time()
        processed = ocr_engine.preprocess_image(sample_image, 'complex')
        preprocessing_time = time.time() - start_time
        assert preprocessing_time < 5  # seconds
        
        # Test OCR performance
        start_time = time.time()
        result = ocr_engine.enhance_text_recognition(processed)
        ocr_time = time.time() - start_time
        assert ocr_time < 10  # seconds

    def test_multi_language_support(self, ocr_engine, multilingual_image):
        """Test handling of multiple languages in the same document"""
        # Test with multiple language configurations
        langs = '+'.join(['eng', 'vie'])
        result = ocr_engine.enhance_text_recognition(
            multilingual_image, lang=langs
        )
        
        assert isinstance(result, dict)
        assert result['confidence'] > 0
        assert len(result['text']) > 0

    def test_image_quality_metrics(self, ocr_engine, sample_image):
        """Test image quality assessment and enhancement"""
        # Test different preprocessing combinations
        quality_scores = []
        
        for pipeline in ['basic', 'complex']:
            processed = ocr_engine.preprocess_image(sample_image, pipeline)
            
            # Calculate quality metrics
            blur_score = cv2.Laplacian(processed, cv2.CV_64F).var()
            contrast = processed.std()
            
            quality_scores.append({
                'pipeline': pipeline,
                'blur_score': blur_score,
                'contrast': contrast
            })
        
        # Verify quality improvements
        assert quality_scores[1]['blur_score'] >= quality_scores[0]['blur_score']

    def test_ocr_confidence_scoring(self, ocr_engine, sample_image):
        """Test OCR confidence scoring mechanism"""
        result = ocr_engine.enhance_text_recognition(sample_image)
        
        assert 'confidence' in result
        assert 0 <= result['confidence'] <= 1
        
        # Test confidence correlation with image quality
        noisy_image = sample_image.copy()
        noise = np.random.normal(0, 50, noisy_image.shape).astype(np.uint8)
        noisy_image = cv2.add(noisy_image, noise)
        
        noisy_result = ocr_engine.enhance_text_recognition(noisy_image)
        assert noisy_result['confidence'] <= result['confidence']

    @classmethod
    def teardown_class(cls):
        """Clean up test files after all tests complete"""
        # Remove temporary files
        for file in Path(tempfile.gettempdir()).glob('ocr_test_*'):
            try:
                file.unlink()
            except Exception:
                pass
