# ==================================================
# INTEGRATION HELPER - KẾT NỐI VỚI FILE CHÍNH CŨ
# ==================================================

# 1. IMPORTS CẦN THÊM VÀO FILE CHÍNH CỦA BẠN
"""
Thêm các import này vào đầu file chính:

from processors.pdf_processor import PDFProcessor
from processors.table_extractor import TableExtractor  
from processors.ocr_engine import OCREngine
from engines.translation_engine import TranslationEngine
from engines.api_manager import APIManager
"""

# 2. KHỞI TẠO CÁC COMPONENTS
def initialize_advanced_components():
    """
    Hàm khởi tạo tất cả components mới
    Gọi hàm này trong file chính của bạn
    """
    # Khởi tạo processors
    pdf_processor = PDFProcessor()
    table_extractor = TableExtractor()
    ocr_engine = OCREngine()
    
    # Khởi tạo API manager
    api_manager = APIManager()
    
    # Khởi tạo translation engine (nếu có API keys)
    translation_engine = None
    openai_key = api_manager.get_api_key('openai')
    anthropic_key = api_manager.get_api_key('anthropic')
    
    if openai_key or anthropic_key:
        translation_engine = TranslationEngine(
            openai_api_key=openai_key,
            anthropic_api_key=anthropic_key
        )
    
    return {
        'pdf_processor': pdf_processor,
        'table_extractor': table_extractor,
        'ocr_engine': ocr_engine,
        'api_manager': api_manager,
        'translation_engine': translation_engine
    }

# 3. HÀM XỬ LÝ PDF NÂNG CAP 
def process_pdf_advanced(pdf_path, components):
    """
    Hàm xử lý PDF với tất cả tính năng nâng cao
    Thay thế hàm xử lý PDF cũ của bạn bằng hàm này
    
    Args:
        pdf_path: Đường dẫn file PDF
        components: Dict các components từ initialize_advanced_components()
    
    Returns:
        Kết quả xử lý chi tiết
    """
    import streamlit as st
    
    results = {
        'analysis': None,
        'content': None,
        'tables': None,
        'translation': None,
        'processing_stats': {}
    }
    
    # Bước 1: Phân tích PDF
    st.write("🔍 **Analyzing PDF structure...**")
    progress = st.progress(0)
    
    try:
        analysis = components['pdf_processor'].analyze_pdf(pdf_path)
        results['analysis'] = analysis
        progress.progress(0.25)
        
        # Hiển thị thống kê phân tích
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📄 Pages", analysis['page_count'])
        with col2:
            st.metric("📊 Tables", "✅" if analysis['has_tables'] else "❌")
        with col3:
            st.metric("🧮 Formulas", "✅" if analysis['has_formulas'] else "❌")
        with col4:
            st.metric("🖼️ Scanned", "✅" if analysis['is_scanned'] else "❌")
            
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        return results
    
    # Bước 2: Trích xuất nội dung
    st.write("📄 **Extracting content...**")
    
    try:
        if analysis['is_scanned'] or not analysis['has_text']:
            # Dùng OCR cho file scan
            content = components['ocr_engine'].process_pdf_ocr(pdf_path)
            extraction_method = "OCR"
        else:
            # Dùng text extraction cho file có text
            content = components['pdf_processor'].extract_text_content(pdf_path)
            extraction_method = "Text Extraction"
        
        results['content'] = content
        progress.progress(0.5)
        
        # Hiển thị thống kê content
        if extraction_method == "OCR":
            total_chars = sum(p.get('character_count', 0) for p in content.get('pages', []))
            avg_confidence = content.get('total_confidence', 0) * 100
        else:
            total_chars = len(content.get('full_text', ''))
            avg_confidence = content.get('confidence', 0) * 100
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📝 Characters", f"{total_chars:,}")
        with col2:
            st.metric("🎯 Confidence", f"{avg_confidence:.1f}%")
        
        st.info(f"✅ Content extracted using **{extraction_method}**")
        
    except Exception as e:
        st.error(f"Content extraction failed: {e}")
        return results
    
    # Bước 3: Trích xuất bảng (nếu có)
    if analysis.get('has_tables', False):
        st.write("📊 **Extracting tables...**")
        
        try:
            tables = components['table_extractor'].process_all_tables(pdf_path)
            results['tables'] = tables
            progress.progress(0.75)
            
            # Hiển thị thống kê bảng
            tables_count = tables.get('tables_extracted', 0)
            total_rows = sum(t.get('rows_count', 0) for t in tables.get('tables', []))
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("📊 Tables Found", tables_count)
            with col2:
                st.metric("📋 Total Rows", total_rows)
            
            if tables_count > 0:
                st.success(f"✅ Successfully extracted {tables_count} tables")
                
        except Exception as e:
            st.warning(f"Table extraction failed: {e}")
    
    # Bước 4: Dịch thuật (nếu có API)
    if components['translation_engine']:
        st.write("🌐 **AI Translation...**")
        
        try:
            # Lấy text để dịch
            if extraction_method == "OCR":
                text_to_translate = content.get('full_text', '')
            else:
                text_to_translate = content.get('full_text', '')
            
            if text_to_translate.strip():
                # Xác định loại document
                if analysis.get('has_formulas'):
                    doc_type = 'formula'
                elif analysis.get('has_tables'):
                    doc_type = 'technical'
                else:
                    doc_type = 'general'
                
                # Thực hiện dịch
                import asyncio
                translation = asyncio.run(
                    components['translation_engine'].translate_document(
                        text=text_to_translate,
                        target_lang='vi',  # Vietnamese
                        document_type=doc_type
                    )
                )
                
                results['translation'] = translation
                
                # Hiển thị thống kê dịch
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("🌍 Source", translation.get('source_lang', '').upper())
                with col2:
                    st.metric("✨ Quality", f"{translation.get('average_confidence', 0)*100:.1f}%")
                
                st.success("✅ Translation completed!")
                
        except Exception as e:
            st.warning(f"Translation failed: {e}")
    
    progress.progress(1.0)
    return results

# 4. HÀM TẠO UI SETTINGS
def create_advanced_settings_sidebar(api_manager):
    """
    Tạo sidebar settings cho API keys
    Thêm vào sidebar của file chính
    """
    import streamlit as st
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("⚙️ Advanced Settings")
        
        # API Configuration
        if st.checkbox("🔐 Configure API Keys"):
            api_manager.create_api_settings_ui()
        
        # Processing Options
        st.subheader("🛠️ Processing Options")
        
        # OCR Settings
        ocr_quality = st.selectbox(
            "OCR Quality",
            ["Standard", "High Quality", "Maximum"],
            help="Higher quality takes longer but more accurate"
        )
        
        # Translation Settings
        target_lang = st.selectbox(
            "Target Language",
            ["Vietnamese", "English", "Chinese", "Japanese"],
            help="Language to translate to"
        )
        
        ai_model = st.selectbox(
            "AI Model Preference", 
            ["OpenAI (GPT)", "Anthropic (Claude)"],
            help="Preferred AI model for translation"
        )
        
        # Save settings to session state
        st.session_state.ocr_quality = ocr_quality
        st.session_state.target_language = target_lang.lower()[:2]  # vi, en, zh, ja
        st.session_state.ai_model_preference = 'openai' if 'OpenAI' in ai_model else 'anthropic'

# 5. HÀM HIỂN THỊ KẾT QUẢ NÂNG CAO
def display_advanced_results(results):
    """
    Hiển thị kết quả xử lý nâng cao
    Thay thế phần hiển thị kết quả cũ
    """
    import streamlit as st
    
    # Tab layout cho kết quả
    tabs = st.tabs(["📄 Content", "📊 Tables", "🌐 Translation", "📈 Statistics"])
    
    # Tab 1: Content
    with tabs[0]:
        if results.get('content'):
            content = results['content']
            
            if isinstance(content, dict) and 'full_text' in content:
                text_content = content['full_text']
            elif isinstance(content, dict) and 'pages' in content:
                # OCR result format
                text_content = content.get('full_text', '')
            else:
                text_content = str(content)
            
            st.subheader("📄 Extracted Content")
            
            # Show preview
            preview_length = st.slider("Preview Length", 100, 2000, 500)
            st.text_area(
                "Content Preview",
                text_content[:preview_length] + "..." if len(text_content) > preview_length else text_content,
                height=300
            )
            
            # Download button
            st.download_button(
                "📥 Download Full Content",
                text_content,
                file_name="extracted_content.txt",
                mime="text/plain"
            )
    
    # Tab 2: Tables
    with tabs[1]:
        if results.get('tables') and results['tables'].get('tables'):
            st.subheader("📊 Extracted Tables")
            
            for i, table in enumerate(results['tables']['tables']):
                st.write(f"**Table {i+1}** (Page {table.get('page_number', 'Unknown')})")
                
                if table.get('dataframe'):
                    # Display as DataFrame
                    import pandas as pd
                    df = pd.DataFrame(table['dataframe'])
                    st.dataframe(df)
                else:
                    # Display raw data
                    st.write("Headers:", table.get('headers', []))
                    st.write("Data Preview:", table.get('data', [])[:5])  # First 5 rows
                
                st.markdown("---")
        else:
            st.info("No tables found in the document")
    
    # Tab 3: Translation
    with tabs[2]:
        if results.get('translation'):
            translation = results['translation']
            st.subheader("🌐 AI Translation")
            
            # Show translation
            translated_text = translation.get('translated_text', '')
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write("**Original Text (Preview):**")
                original_preview = translation.get('original_text', '')[:500]
                st.text_area("Original", original_preview, height=200, key="orig")
            
            with col2:
                st.write("**Translated Text:**")
                st.text_area("Translation", translated_text[:500] + "..." if len(translated_text) > 500 else translated_text, height=200, key="trans")
            
            # Download translated content
            st.download_button(
                "📥 Download Translation",
                translated_text,
                file_name="translated_content.txt",
                mime="text/plain"
            )
        else:
            st.info("Translation not available - configure API keys in settings")
    
    # Tab 4: Statistics
    with tabs[3]:
        st.subheader("📈 Processing Statistics")
        
        # Analysis stats
        if results.get('analysis'):
            analysis = results['analysis']
            st.write("**Document Analysis:**")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pages", analysis.get('page_count', 0))
                st.metric("Complexity", f"{analysis.get('complexity_score', 0)}/100")
            with col2:
                st.metric("Has Text", "✅" if analysis.get('has_text') else "❌")
                st.metric("Has Images", "✅" if analysis.get('has_images') else "❌")
            with col3:
                st.metric("Has Tables", "✅" if analysis.get('has_tables') else "❌")
                st.metric("Has Formulas", "✅" if analysis.get('has_formulas') else "❌")
        
        # Processing stats
        st.markdown("---")
        st.write("**Processing Performance:**")
        
        processing_times = []
        if results.get('content') and isinstance(results['content'], dict):
            if 'processing_time' in results['content']:
                processing_times.append(("Content Extraction", results['content']['processing_time']))
        
        if results.get('tables') and isinstance(results['tables'], dict):
            if 'processing_stats' in results['tables']:
                # Add table processing time if available
                pass
        
        if results.get('translation') and isinstance(results['translation'], dict):
            if 'processing_time' in results['translation']:
                processing_times.append(("Translation", results['translation']['processing_time']))
        
        for stage, time_taken in processing_times:
            st.metric(f"{stage} Time", f"{time_taken:.2f}s")

# 6. CÁCH SỬ DỤNG TRONG FILE CHÍNH
"""
Trong file chính của bạn, thêm code này:

# Import integration helper
from integration_helper import (
    initialize_advanced_components,
    process_pdf_advanced, 
    create_advanced_settings_sidebar,
    display_advanced_results
)

# Khởi tạo components (thêm vào đầu file, sau các import)
if 'advanced_components' not in st.session_state:
    st.session_state.advanced_components = initialize_advanced_components()

# Tạo advanced settings trong sidebar
create_advanced_settings_sidebar(st.session_state.advanced_components['api_manager'])

# Thay thế hàm xử lý PDF cũ bằng:
if uploaded_file is not None:
    # Lưu file tạm
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name
    
    # Xử lý với components nâng cao
    results = process_pdf_advanced(tmp_file_path, st.session_state.advanced_components)
    
    # Hiển thị kết quả nâng cao
    display_advanced_results(results)
    
    # Cleanup
    os.unlink(tmp_file_path)
"""

print("✅ Integration helper ready! Follow the usage guide above to integrate with your main file.")
