# src/application/services/enhanced_translation_service.py
import time
import logging
from typing import Dict, List, Optional, Union, BinaryIO
from dataclasses import dataclass

# Simple path setup
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from src.infrastructure.chunking.smart_chunker import SmartTextChunker
from src.infrastructure.chunking.chunk_combiner import SmartChunkCombiner
from src.infrastructure.processors.pdf_processor import PDFProcessor
from src.infrastructure.ocr.ocr_engine import OCREngineFactory
from src.infrastructure.formula.formula_processor import FormulaProcessorFactory
from src.infrastructure.export.export_system import ExportManager

logger = logging.getLogger(__name__)

@dataclass
class ProcessingOptions:
    """Options for document processing"""
    enable_chunking: bool = True
    enable_ocr: bool = False
    enable_formula_detection: bool = True
    enable_export: bool = False
    chunk_size: int = 2500
    chunk_overlap: int = 200
    ocr_engine: str = "tesseract"
    formula_processor: str = "stem"
    export_format: str = "json"

@dataclass
class ProcessingResult:
    """Comprehensive processing result"""
    success: bool
    translated_text: str
    original_text: str
    processing_time: float
    metadata: Dict
    error_message: Optional[str] = None
    chunks_processed: int = 0
    formulas_detected: int = 0
    export_data: Optional[bytes] = None
    export_filename: Optional[str] = None

class EnhancedTranslationService:
    """Enhanced translation service with all advanced features"""
    
    def __init__(self, api_key: str, enable_cache: bool = True):
        """Initialize enhanced translation service"""
        self.api_key = api_key
        self.enable_cache = enable_cache
        
        # Initialize components
        self.chunker = SmartTextChunker()
        self.combiner = SmartChunkCombiner()
        self.pdf_processor = PDFProcessor()
        self.ocr_factory = OCREngineFactory()
        self.formula_factory = FormulaProcessorFactory()
        self.export_manager = ExportManager()
        
        # Cache and stats
        self.translation_cache = {} if enable_cache else None
        self.stats = {
            'total_translations': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'total_chunks_processed': 0,
            'total_formulas_detected': 0,
            'processing_time_total': 0.0
        }
        
        logger.info("Enhanced Translation Service initialized")
    
    def translate_text(self, text: str, target_language: str, 
                      source_language: str = "auto", 
                      options: ProcessingOptions = None) -> ProcessingResult:
        """Translate text with advanced processing"""
        start_time = time.time()
        options = options or ProcessingOptions()
        
        try:
            # Formula processing
            formula_processor = None
            processed_text = text
            formula_map = {}
            formulas_detected = 0
            
            if options.enable_formula_detection:
                formula_processor = self.formula_factory.create_processor(options.formula_processor)
                processed_text, formula_map = formula_processor.preserve_formulas_in_text(text)
                formulas_detected = len(formula_map)
            
            # Check cache
            cache_key = self._generate_cache_key(processed_text, target_language, source_language)
            if self.translation_cache and cache_key in self.translation_cache:
                cached_result = self.translation_cache[cache_key]
                self.stats['cache_hits'] += 1
                
                final_translation = cached_result
                if formula_processor and formula_map:
                    final_translation = formula_processor.restore_formulas_in_text(cached_result, formula_map)
                
                return ProcessingResult(
                    success=True,
                    translated_text=final_translation,
                    original_text=text,
                    processing_time=time.time() - start_time,
                    metadata={'source': 'cache', 'formulas_detected': formulas_detected},
                    formulas_detected=formulas_detected
                )
            
            # Translation with chunking
            translated_text = ""
            chunks_processed = 0
            
            if options.enable_chunking and len(processed_text) > options.chunk_size:
                # Process with chunking
                chunks = self.chunker.chunk_text(processed_text, max_chunk_size=options.chunk_size)
                chunks_processed = len(chunks)
                
                translated_chunks = []
                for chunk in chunks:
                    # Simulate translation (replace with actual API call)
                    chunk_translation = self._simulate_translation(chunk.main_content, target_language, source_language)
                    translated_chunks.append(chunk_translation)
                
                translated_text = " ".join(translated_chunks)
            else:
                translated_text = self._simulate_translation(processed_text, target_language, source_language)
            
            # Restore formulas
            if formula_processor and formula_map:
                translated_text = formula_processor.restore_formulas_in_text(translated_text, formula_map)
            
            # Cache result
            if self.translation_cache:
                self.translation_cache[cache_key] = translated_text
                self.stats['cache_misses'] += 1
            
            # Update stats
            processing_time = time.time() - start_time
            self.stats['total_translations'] += 1
            self.stats['total_chunks_processed'] += chunks_processed
            self.stats['total_formulas_detected'] += formulas_detected
            self.stats['processing_time_total'] += processing_time
            
            # Export if requested
            export_data = None
            export_filename = None
            if options.enable_export:
                record = self.export_manager.create_translation_record(
                    text, translated_text, source_language, target_language,
                    processing_time, formulas_detected=formulas_detected
                )
                export_result = self.export_manager.export(record, options.export_format)
                if export_result.success:
                    export_data = export_result.file_data
                    export_filename = export_result.filename
            
            return ProcessingResult(
                success=True,
                translated_text=translated_text,
                original_text=text,
                processing_time=processing_time,
                metadata={
                    'source_language': source_language,
                    'target_language': target_language,
                    'chunks_processed': chunks_processed,
                    'formulas_detected': formulas_detected,
                    'chunking_enabled': options.enable_chunking,
                    'formula_detection_enabled': options.enable_formula_detection
                },
                chunks_processed=chunks_processed,
                formulas_detected=formulas_detected,
                export_data=export_data,
                export_filename=export_filename
            )
            
        except Exception as e:
            logger.error(f"Translation error: {str(e)}")
            return ProcessingResult(
                success=False,
                translated_text="",
                original_text=text,
                processing_time=time.time() - start_time,
                metadata={},
                error_message=f"Translation failed: {str(e)}"
            )
    
    def process_document(self, file_content: Union[bytes, BinaryIO], 
                        filename: str, target_language: str,
                        source_language: str = "auto",
                        options: ProcessingOptions = None) -> ProcessingResult:
        """Process uploaded document"""
        start_time = time.time()
        options = options or ProcessingOptions()
        
        try:
            extracted_text = ""
            file_type = filename.lower().split('.')[-1] if '.' in filename else ""
            
            # Process based on file type
            if file_type == "pdf":
                pdf_result = self.pdf_processor.process(file_content, filename)
                if pdf_result.success:
                    extracted_text = pdf_result.text
                else:
                    return ProcessingResult(
                        success=False,
                        translated_text="",
                        original_text="",
                        processing_time=time.time() - start_time,
                        metadata={},
                        error_message=f"PDF processing failed: {pdf_result.error_message}"
                    )
            
            elif file_type in ["jpg", "jpeg", "png", "bmp", "tiff"] and options.enable_ocr:
                try:
                    ocr_engine = self.ocr_factory.create_engine(options.ocr_engine)
                    
                    if hasattr(file_content, 'read'):
                        image_bytes = file_content.read()
                    else:
                        image_bytes = file_content
                    
                    ocr_result = ocr_engine.extract_text(image_bytes)
                    extracted_text = ocr_result.text
                    
                except Exception as e:
                    return ProcessingResult(
                        success=False,
                        translated_text="",
                        original_text="",
                        processing_time=time.time() - start_time,
                        metadata={},
                        error_message=f"OCR processing failed: {str(e)}"
                    )
            
            else:
                return ProcessingResult(
                    success=False,
                    translated_text="",
                    original_text="",
                    processing_time=time.time() - start_time,
                    metadata={},
                    error_message=f"Unsupported file type: {file_type}"
                )
            
            # Translate extracted text
            if extracted_text.strip():
                translation_result = self.translate_text(extracted_text, target_language, source_language, options)
                translation_result.metadata.update({
                    'document_type': file_type,
                    'filename': filename,
                    'extracted_text_length': len(extracted_text)
                })
                return translation_result
            else:
                return ProcessingResult(
                    success=False,
                    translated_text="",
                    original_text="",
                    processing_time=time.time() - start_time,
                    metadata={'filename': filename, 'document_type': file_type},
                    error_message="No text could be extracted from the document"
                )
                
        except Exception as e:
            return ProcessingResult(
                success=False,
                translated_text="",
                original_text="",
                processing_time=time.time() - start_time,
                metadata={'filename': filename},
                error_message=f"Document processing failed: {str(e)}"
            )
    
    def _simulate_translation(self, text: str, target_lang: str, source_lang: str) -> str:
        """Simulate translation (replace with actual API call)"""
        import time
        time.sleep(0.1)  # Simulate API delay
        return f"[TRANSLATED to {target_lang}] {text}"
    
    def _generate_cache_key(self, text: str, target_lang: str, source_lang: str) -> str:
        """Generate cache key"""
        import hashlib
        content = f"{text}|{source_lang}|{target_lang}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def get_service_info(self) -> Dict:
        """Get service information"""
        return {
            'service_name': 'Enhanced Translation Service',
            'version': '3.0.0',
            'features': [
                'Smart Chunking',
                'PDF Processing',
                'OCR Engine',
                'Formula Detection',
                'Export System',
                'Cache System'
            ],
            'chunking_enabled': True,
            'cache_enabled': self.enable_cache,
            'available_ocr_engines': self.ocr_factory.get_available_engines(),
            'available_formula_processors': self.formula_factory.get_available_processors(),
            'available_export_formats': self.export_manager.get_available_formats(),
            'statistics': self.stats.copy()
        }
    
    def get_processing_stats(self) -> Dict:
        """Get processing statistics"""
        return self.stats.copy()
    
    def clear_cache(self) -> bool:
        """Clear translation cache"""
        if self.translation_cache:
            self.translation_cache.clear()
            return True
        return False
