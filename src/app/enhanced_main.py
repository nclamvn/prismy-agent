# src/app/enhanced_main.py
import streamlit as st
import time
import io
from datetime import datetime
import sys
import os

# Comprehensive path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = current_dir
src_dir = os.path.join(current_dir, '..')
root_dir = os.path.join(current_dir, '..', '..')

# Add all necessary paths
for path in [root_dir, src_dir, app_dir, os.path.join(root_dir, 'src')]:
    if path not in sys.path:
        sys.path.insert(0, path)

# Debug path info
print(f"🔧 Paths added: {len(sys.path)} total paths")
print(f"📁 Root dir: {root_dir}")
print(f"📁 Src dir: {src_dir}")

# Page config
st.set_page_config(
    page_title="🚀 AI Translation Hub - Enterprise",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .success-alert {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def render_header():
    """Render header"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI Translation Hub - Enterprise Edition</h1>
        <p>Phase 3B Complete: PDF Processing • OCR • Formula Detection • Export System</p>
    </div>
    """, unsafe_allow_html=True)

def test_all_components():
    """Test all Phase 3B components"""
    st.markdown("### 🧪 Component Status Test")
    
    tests = []
    
    # Test 1: Chunking
    try:
        # Test chunking với interface hiện tại
        from src.core.interfaces.chunking import ChunkerInterface, TextChunk
        from src.infrastructure.chunking.smart_chunker import SmartTextChunker
        chunker = SmartTextChunker()
        # Test chunking functionality
        test_text = "This is a test text for chunking."
        chunks = chunker.chunk_text(test_text, max_chunk_size=100)
        tests.append(("✅ Smart Chunking", f"Working - Created {len(chunks)} chunks"))
    except Exception as e:
        tests.append(("❌ Smart Chunking", f"Error: {str(e)[:50]}..."))
    
    # Test 2: PDF Processing
    try:
        # Test PDF processor với better error handling
        import sys
        import os
        
        # Ensure proper path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, '..', '..')
        sys.path.insert(0, root_dir)
        
        from src.infrastructure.processors.pdf_processor import PDFProcessor
        processor = PDFProcessor()
        formats = processor.get_supported_formats()
        tests.append(("✅ PDF Processing", f"Supports: {formats}"))
    except Exception as e:
        tests.append(("❌ PDF Processing", f"Error: {str(e)[:50]}..."))
    
    # Test 3: OCR Engine
    try:
        from src.infrastructure.ocr.ocr_engine import OCREngineFactory
        factory = OCREngineFactory()
        engines = factory.get_available_engines()
        tests.append(("✅ OCR Engine", f"Available: {engines}"))
    except Exception as e:
        tests.append(("❌ OCR Engine", f"Error: {str(e)[:50]}..."))
    
    # Test 4: Formula Processor
    try:
        from src.infrastructure.formula.formula_processor import FormulaProcessorFactory
        factory = FormulaProcessorFactory()
        processor = factory.create_processor("stem")
        formulas = processor.detect_formulas("Test E=mc² formula")
        tests.append(("✅ Formula Detection", f"Detected {len(formulas)} formulas"))
    except Exception as e:
        tests.append(("❌ Formula Detection", f"Error: {str(e)[:50]}..."))
    
    # Test 5: Export System
    try:
        from src.infrastructure.export.export_system import ExportManager
        manager = ExportManager()
        formats = manager.get_available_formats()
        tests.append(("✅ Export System", f"Formats: {formats}"))
    except Exception as e:
        tests.append(("❌ Export System", f"Error: {str(e)[:50]}..."))
    
    # Display results
    for test_name, result in tests:
        st.write(f"{test_name}: {result}")
    
    # Count successes
    passed = sum(1 for test_name, _ in tests if "✅" in test_name)
    total = len(tests)
    
    if passed == total:
        st.markdown("""
        <div class="success-alert">
            🎉 ALL COMPONENTS WORKING! Phase 3B Complete!
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ {passed}/{total} components working. Some features may be limited.")
    
    return passed, total

def render_demo_translation():
    """Demo translation interface"""
    st.markdown("### 📝 Demo Translation")
    
    input_text = st.text_area(
        "Enter text to test:",
        value="Hello world! Einstein discovered E=mc² which is a famous formula.",
        height=100
    )
    
    if st.button("🚀 Test Translation", type="primary"):
        with st.spinner("Processing..."):
            # Simulate processing
            time.sleep(1)
            
            # Simple demo translation
            demo_result = f"[DEMO TRANSLATION] {input_text}"
            
            st.success("✅ Demo translation completed!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original:**")
                st.text_area("", input_text, height=150, disabled=True, key="orig")
            
            with col2:
                st.markdown("**Demo Translation:**")
                st.text_area("", demo_result, height=150, disabled=True, key="trans")

def main():
    """Main app function"""
    render_header()
    
    # Sidebar info
    with st.sidebar:
        st.markdown("### 📊 Enterprise Features")
        st.markdown("""
        ✅ Smart Text Chunking  
        ✅ PDF Document Processing  
        ✅ OCR Engine (Tesseract)  
        ✅ Formula Detection  
        ✅ Export System  
        ✅ Translation Cache  
        """)
        
        st.markdown("### 🎯 Phase 3B Status")
        if st.button("🧪 Test Components"):
            st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🧪 Component Test", "📝 Demo Translation", "📋 Documentation"])
    
    with tab1:
        passed, total = test_all_components()
        
        if passed == total:
            st.balloons()
    
    with tab2:
        render_demo_translation()
    
    with tab3:
        st.markdown("""
        ### 📚 Phase 3B Documentation
        
        **🎯 Completed Features:**
        - **Smart Chunking**: Intelligent text segmentation with context preservation
        - **PDF Processing**: Extract text from PDF documents with table support
        - **OCR Engine**: Image-to-text conversion using Tesseract
        - **Formula Detection**: LaTeX and mathematical formula recognition
        - **Export System**: JSON and CSV export capabilities
        
        **🏗️ Architecture:**
        - **Clean Architecture**: Separation of concerns with interfaces
        - **Modular Design**: Each component can be used independently
        - **Enterprise Ready**: Error handling, logging, and validation
        
        **🚀 Next Steps:**
        - Integrate real Google Translate API
        - Add user authentication
        - Deploy to production
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        🚀 <strong>AI Translation Hub - Enterprise Edition</strong><br>
        Phase 3B Complete: All Advanced Features Successfully Integrated
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
