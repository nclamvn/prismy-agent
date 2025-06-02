import streamlit as st
import asyncio
from sdip_integration import SDIPSystem

# Page config
st.set_page_config(
    page_title="AI Translator Agent - SDIP Enhanced",
    page_icon="🚀",
    layout="wide"
)

# Header
st.title("🚀 AI Translator Agent - SDIP Enhanced")
st.markdown("**Semantic Document Intelligence Platform** - Professional Translation System")

# Sidebar for configuration
st.sidebar.header("⚙️ Translation Configuration")

# Translation tier selection
translation_tier = st.sidebar.selectbox(
    "🎯 Translation Quality Tier",
    ["Professional (SDIP) - Premium", "Legacy System - Basic"],
    help="Choose translation quality level"
)

# Language selection
target_language = st.sidebar.selectbox(
    "🌍 Target Language",
    ["Vietnamese", "English", "French", "German", "Spanish", "Chinese", "Japanese"],
)

source_language = st.sidebar.selectbox(
    "🔤 Source Language", 
    ["Auto-detect", "English", "Vietnamese", "French", "German", "Spanish"]
)

# Main interface
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📝 Input Document")
    
    # Text input
    input_text = st.text_area(
        "Enter text to translate:",
        height=300,
        placeholder="Paste your document here..."
    )
    
    # File upload option
    uploaded_file = st.file_uploader(
        "Or upload a document:",
        type=['txt', 'pdf', 'docx'],
        help="Supported formats: TXT, PDF, DOCX"
    )
    
    if uploaded_file and not input_text:
        # Simple file processing for demo
        if uploaded_file.type == "text/plain":
            input_text = str(uploaded_file.read(), "utf-8")
            st.success(f"✅ Loaded {len(input_text)} characters from file")

with col2:
    st.header("🎯 Translation Result")
    
    if st.button("🚀 Translate Document", type="primary"):
        if input_text:
            if "SDIP" in translation_tier:
                # Use SDIP system
                st.info("🚀 Using SDIP - Semantic Document Intelligence Platform")
                
                try:
                    # Initialize SDIP system
                    sdip_system = SDIPSystem()
                    
                    # Perform translation
                    with st.spinner("🔄 Processing with SDIP..."):
                        result = sdip_system.translate_document(
                            input_text, 
                            target_language,
                            "auto" if source_language == "Auto-detect" else source_language
                        )
                    
                    if result["success"]:
                        # Display results
                        st.success("✅ Professional Translation Completed!")
                        
                        # Metrics
                        metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                        with metrics_col1:
                            st.metric("Quality Score", f"{result['quality_score']:.2f}")
                        with metrics_col2:
                            st.metric("Processing Time", f"{result['processing_time']:.2f}s")
                        with metrics_col3:
                            st.metric("Semantic Chunks", result['chunk_count'])
                        
                        # Translation result
                        st.text_area(
                            "🎯 Professional Translation:",
                            value=result['translated_text'],
                            height=300
                        )
                        
                        # Advanced info
                        with st.expander("📊 Advanced Translation Details"):
                            st.json({
                                "Translation Tier": result.get('translation_tier', 'Professional'),
                                "Quality Score": result['quality_score'],
                                "Processing Time": f"{result['processing_time']:.2f} seconds",
                                "Semantic Chunks": result['chunk_count'],
                                "Source Language": source_language,
                                "Target Language": target_language,
                                "System": "SDIP - Semantic Document Intelligence Platform"
                            })
                    
                    else:
                        st.error(f"❌ Translation failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    st.error(f"❌ SDIP system error: {e}")
            
            else:
                # Legacy system placeholder
                st.warning("🔧 Legacy system not implemented in this demo")
                st.info("Use SDIP Professional tier for actual translation")
        
        else:
            st.warning("⚠️ Please enter text to translate")

# Footer info
st.markdown("---")
st.markdown("""
### 🚀 About SDIP (Semantic Document Intelligence Platform)

**Core Innovations:**
- **Semantic Chunking Engine™**: Advanced document segmentation with context awareness
- **Professional Translator**: Multi-model orchestration with quality assurance
- **Document Blueprint Reconstruction™**: Preserves formatting and structure

**Translation Tiers:**
- 🏆 **Professional**: Premium quality with multi-model validation
- 🔧 **Standard**: Balanced quality and speed (coming soon)
- ⚡ **Basic**: Fast translation for simple content (coming soon)

*Currently running in demo mode with mock translations*
""")

# System status
with st.expander("🔧 System Status"):
    st.success("✅ SDIP Core Systems Operational")
    st.info("ℹ️ Running in demo mode - API keys not configured")
    st.warning("⚠️ For production use, configure Claude and OpenAI API keys")
