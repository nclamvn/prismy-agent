# run_enhanced_app.py
"""
🚀 Enhanced Translation App Launcher - Phase 3B COMPLETE
"""

import streamlit as st
import sys
import os
import traceback

def setup_paths():
    """Thiết lập đường dẫn Python paths"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    print(f"✅ Đã thiết lập Python path: {src_dir}")
    return src_dir

def check_dependencies():
    """Kiểm tra dependencies cần thiết"""
    required_packages = ['streamlit', 'time', 'datetime', 'io', 'logging']
    optional_packages = [
        ('PyPDF2', 'PDF processing'),
        ('pdfplumber', 'Advanced PDF extraction'),
        ('pytesseract', 'Tesseract OCR'),
        ('easyocr', 'EasyOCR engine'),
        ('PIL', 'Image processing'),
        ('reportlab', 'PDF export'),
        ('docx', 'DOCX export')
    ]
    
    print("🔍 Kiểm tra dependencies...")
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - THIẾU (cần thiết)")
            return False
    
    available_features = []
    for package, feature in optional_packages:
        try:
            __import__(package)
            print(f"✅ {package} - {feature}")
            available_features.append(feature)
        except ImportError:
            print(f"⚠️  {package} - {feature} (tùy chọn)")
    
    print(f"\n🎯 Tính năng khả dụng: {', '.join(available_features)}")
    return True

def create_init_files():
    """Tạo các file __init__.py cần thiết"""
    print("📁 Tạo __init__.py files...")
    
    init_dirs = [
        'src', 'src/core', 'src/core/interfaces', 'src/infrastructure',
        'src/infrastructure/chunking', 'src/infrastructure/processors',
        'src/infrastructure/ocr', 'src/infrastructure/formula',
        'src/infrastructure/export', 'src/application',
        'src/application/services', 'src/app'
    ]
    
    for dir_path in init_dirs:
        if os.path.exists(dir_path):
            init_file = os.path.join(dir_path, '__init__.py')
            if not os.path.exists(init_file):
                with open(init_file, 'w') as f:
                    f.write('')
                print(f"✅ Tạo {init_file}")
            else:
                print(f"✅ {init_file} đã tồn tại")
        else:
            print(f"⚠️  Thư mục {dir_path} không tồn tại")

def test_chunking_system():
    """Test chunking system"""
    try:
        print("📦 Testing chunking system...")
        
        from core.interfaces.chunking import ChunkerInterface, ChunkCombinerInterface, TextChunk
        print("✅ Core chunking interfaces")
        
        from infrastructure.chunking.smart_chunker import SmartTextChunker
        from infrastructure.chunking.chunk_combiner import SmartChunkCombiner
        print("✅ Chunking implementations")
        
        chunker = SmartTextChunker()
        combiner = SmartChunkCombiner()
        print("✅ Chunking components initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Chunking system failed: {e}")
        return False

def test_pdf_processor():
    """Test PDF processor"""
    try:
        print("📄 Testing PDF processor...")
        from infrastructure.processors.pdf_processor import PDFProcessor
        
        processor = PDFProcessor()
        print(f"✅ PDF Processor (supports: {processor.get_supported_formats()})")
        return True
        
    except Exception as e:
        print(f"❌ PDF processor failed: {e}")
        return False

def test_ocr_engine():
    """Test OCR engine"""
    try:
        print("🔍 Testing OCR engine...")
        from infrastructure.ocr.ocr_engine import OCREngineFactory
        
        factory = OCREngineFactory()
        engines = factory.get_available_engines()
        print(f"✅ OCR engines available: {engines}")
        return True
        
    except Exception as e:
        print(f"❌ OCR engine failed: {e}")
        return False

def test_formula_processor():
    """Test formula processor"""
    try:
        print("🔢 Testing formula processor...")
        from infrastructure.formula.formula_processor import FormulaProcessorFactory
        
        factory = FormulaProcessorFactory()
        processor = factory.create_processor('stem')
        formulas = processor.detect_formulas('Test equation: E=mc² and F=ma')
        print(f"✅ Formula processor: {len(formulas)} formulas detected")
        return True
        
    except Exception as e:
        print(f"❌ Formula processor failed: {e}")
        return False

def test_export_system():
    """Test export system"""
    try:
        print("📤 Testing export system...")
        from infrastructure.export.export_system import ExportManager
        
        manager = ExportManager()
        formats = manager.get_available_formats()
        print(f"✅ Export system: {formats} formats available")
        return True
        
    except Exception as e:
        print(f"❌ Export system failed: {e}")
        return False

def run_comprehensive_test():
    """Run comprehensive test of all systems"""
    tests = [
        ("Chunking System", test_chunking_system),
        ("PDF Processor", test_pdf_processor),
        ("OCR Engine", test_ocr_engine),
        ("Formula Processor", test_formula_processor),
        ("Export System", test_export_system)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            failed += 1
    
    print(f"\n📊 TEST RESULTS: {passed} passed, {failed} failed")
    return failed == 0

def main():
    """Main launcher function"""
    print("🚀 ENHANCED TRANSLATION APP LAUNCHER")
    print("=" * 50)
    
    # Setup
    setup_paths()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Vui lòng cài đặt dependencies thiếu")
        return
    
    # Create init files
    create_init_files()
    
    # Run tests
    if run_comprehensive_test():
        print("\n🎉 ALL PHASE 3B COMPONENTS WORKING!")
        print("🚀 READY FOR ENHANCED STREAMLIT APP!")
        print("\n📋 Available features:")
        print("  ✅ Smart chunking system")
        print("  ✅ PDF processing")
        print("  ✅ OCR engine (Tesseract)")
        print("  ✅ Formula detection")
        print("  ✅ Export system (JSON, CSV)")
        print("\n🔧 Next: Create enhanced Streamlit app")
    else:
        print("\n⚠️  Some components need attention, but basic functionality available")
        print("🔄 You can still use Phase 3A app: streamlit run run_new_app.py --server.port 8510")

if __name__ == "__main__":
    main()
