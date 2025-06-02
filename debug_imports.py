#!/usr/bin/env python3
"""Debug imports for Phase 3B components"""

import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, current_dir)

print("🔍 IMPORT DEBUG TEST")
print("=" * 30)

# Test 1: Smart Chunking
print("1. Testing Smart Chunking...")
try:
    from src.core.interfaces.chunking import ChunkerInterface, TextChunk
    print("   ✅ Chunking interfaces imported")
    
    from src.infrastructure.chunking.smart_chunker import SmartTextChunker
    chunker = SmartTextChunker()
    print("   ✅ SmartTextChunker created")
    
    chunks = chunker.chunk_text("Test text", max_chunk_size=100)
    print(f"   ✅ Chunking test: {len(chunks)} chunks created")
    
except Exception as e:
    print(f"   ❌ Smart Chunking failed: {e}")

# Test 2: PDF Processing
print("\n2. Testing PDF Processing...")
try:
    from src.infrastructure.processors.pdf_processor import PDFProcessor
    processor = PDFProcessor()
    formats = processor.get_supported_formats()
    print(f"   ✅ PDF Processor created, supports: {formats}")
    
except Exception as e:
    print(f"   ❌ PDF Processing failed: {e}")

# Test 3: OCR
print("\n3. Testing OCR...")
try:
    from src.infrastructure.ocr.ocr_engine import OCREngineFactory
    factory = OCREngineFactory()
    engines = factory.get_available_engines()
    print(f"   ✅ OCR Factory, engines: {engines}")
    
except Exception as e:
    print(f"   ❌ OCR failed: {e}")

# Test 4: Formula
print("\n4. Testing Formula...")
try:
    from src.infrastructure.formula.formula_processor import FormulaProcessorFactory
    factory = FormulaProcessorFactory()
    processor = factory.create_processor("stem")
    formulas = processor.detect_formulas("E=mc²")
    print(f"   ✅ Formula Processor, detected: {len(formulas)} formulas")
    
except Exception as e:
    print(f"   ❌ Formula failed: {e}")

# Test 5: Export
print("\n5. Testing Export...")
try:
    from src.infrastructure.export.export_system import ExportManager
    manager = ExportManager()
    formats = manager.get_available_formats()
    print(f"   ✅ Export Manager, formats: {formats}")
    
except Exception as e:
    print(f"   ❌ Export failed: {e}")

print("\n🎯 Import debug complete!")
