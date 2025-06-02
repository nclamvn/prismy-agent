import streamlit as st
import time
from sdip_integration import SDIPSystem
from ui_components.modern_components import ModernUIComponents

# Initialize modern UI
ui = ModernUIComponents()
ui.setup_page_config()

# Hero Section with modern design
ui.create_hero_section()

# Sidebar Configuration
st.sidebar.markdown("### ⚙️ Translation Configuration")
st.sidebar.markdown("---")

translation_tier = st.sidebar.selectbox(
    "🎯 Translation Quality Tier",
    ["🏆 Professional (SDIP) - Premium", "🔧 Legacy System - Basic"],
    help="Choose your translation quality level"
)

target_language = st.sidebar.selectbox(
    "🌍 Target Language",
    ["Vietnamese", "English", "French", "German", "Spanish", "Chinese", "Japanese"],
)

source_language = st.sidebar.selectbox(
    "🔤 Source Language", 
    ["Auto-detect", "English", "Vietnamese", "French", "German", "Spanish"]
)

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📝 Input Document")
    
    input_text = st.text_area(
        "Enter text to translate:",
        height=300,
        placeholder="Paste your document here for professional translation...",
        help="Supports documents up to 10,000 characters"
    )
    
    uploaded_file = st.file_uploader(
        "Or upload a document:",
        type=['txt', 'pdf', 'docx'],
        help="Supported formats: TXT, PDF, DOCX"
    )
    
    if uploaded_file and not input_text:
        if uploaded_file.type == "text/plain":
            input_text = str(uploaded_file.read(), "utf-8")
            st.success(f"✅ Loaded {len(input_text)} characters from file")

with col2:
    st.markdown("### 🎯 Translation Result")
    
    if st.button("🚀 Translate Document", type="primary"):
        if input_text:
            if "SDIP" in translation_tier:
                # Modern progress visualization
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                # Step 1: Initialization (20%)
                with progress_placeholder.container():
                    ui.create_animated_progress_bar(20, "Initializing SDIP")
                
                with status_placeholder.container():
                    ui.create_status_indicators({
                        "🚀 SDIP System": "success",
                        "🔄 Loading Models": "info"
                    })
                
                time.sleep(1)
                
                # Step 2: Initialize SDIP System (40%)
                try:
                    sdip_system = SDIPSystem()
                    
                    with progress_placeholder.container():
                        ui.create_animated_progress_bar(40, "Semantic Analysis")
                    
                    with status_placeholder.container():
                        ui.create_status_indicators({
                            "✅ System Ready": "success",
                            "🧠 Analyzing Document": "info"
                        })
                    
                    time.sleep(0.8)
                    
                    # Step 3: Processing (70%)
                    with progress_placeholder.container():
                        ui.create_animated_progress_bar(70, "AI Translation")
                    
                    with status_placeholder.container():
                        ui.create_status_indicators({
                            "✅ Analysis Complete": "success",
                            "🎯 Professional Translation": "warning"
                        })
                    
                    time.sleep(0.8)
                    
                    # Step 4: Perform actual translation
                    result = sdip_system.translate_document(
                        input_text, 
                        target_language,
                        "auto" if source_language == "Auto-detect" else source_language
                    )
                    
                    # Step 5: Completion (100%)
                    with progress_placeholder.container():
                        ui.create_animated_progress_bar(100, "Complete")
                    
                    with status_placeholder.container():
                        ui.create_status_indicators({
                            "✅ Translation Complete": "success",
                            "🎯 Quality Assured": "success",
                            "📊 Results Ready": "success"
                        })
                    
                    time.sleep(1)
                    
                    if result["success"]:
                        # Clear progress indicators
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        
                        # Show success message
                        st.success("✅ Professional Translation Completed!")
                        
                        # Display modern metrics
                        st.markdown("### 📊 Performance Metrics")
                        ui.create_modern_metrics(
                            result['quality_score'],
                            result['processing_time'], 
                            result['chunk_count']
                        )
                        
                        # Translation result
                        st.markdown("### 🎯 Professional Translation")
                        st.text_area(
                            "Translation Result:",
                            value=result['translated_text'],
                            height=250,
                            help="Professional quality translation with semantic understanding"
                        )
                        
                        # Advanced details
                        with st.expander("📊 Advanced Translation Details"):
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.json({
                                    "Translation Tier": "Professional",
                                    "Quality Score": result['quality_score'],
                                    "Processing Time": f"{result['processing_time']:.2f}s",
                                    "Semantic Chunks": result['chunk_count']
                                })
                            
                            with col_b:
                                st.json({
                                    "Source Language": source_language,
                                    "Target Language": target_language,
                                    "System": "SDIP Enhanced",
                                    "Model": "Professional Tier"
                                })
                    
                    else:
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        st.error(f"❌ Translation failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    progress_placeholder.empty()
                    status_placeholder.empty()
                    st.error(f"❌ SDIP system error: {e}")
            
            else:
                st.warning("🔧 Legacy system not implemented in this demo")
                st.info("Use SDIP Professional tier for actual translation")
        
        else:
            st.warning("⚠️ Please enter text to translate")

# Footer with modern styling
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <h4 style="color: #333;">🚀 SDIP Enhanced - Modern UI Demo</h4>
    <p>Semantic Document Intelligence Platform with Real-time Process Visualization</p>
    <p><small>Built with advanced UI components and glassmorphism design</small></p>
</div>
""", unsafe_allow_html=True)
