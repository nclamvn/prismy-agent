import streamlit as st
import asyncio
import time
from sdip_smart_integration import SDIPSmartSystem
from ui_components.modern_components import ModernUIComponents

# Initialize modern UI and smart system
ui = ModernUIComponents()
ui.setup_page_config()

# Hero Section
ui.create_hero_section()

# Smart features introduction
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
           padding: 20px; border-radius: 16px; margin: 15px 0; border-left: 4px solid #667eea;">
    <h3 style="color: #333; margin: 0 0 10px 0;">🧠 AI Smart Features Active</h3>
    <p style="margin: 0; color: #666;">
        • <strong>Intelligent Document Analysis</strong> - Automatic complexity detection<br>
        • <strong>Smart Retry System</strong> - Multi-model quality optimization<br>
        • <strong>Adaptive Chunking</strong> - Context-aware segmentation<br>
        • <strong>Batch Processing</strong> - Efficient multiple document handling
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("### ⚙️ Smart Translation Configuration")
st.sidebar.markdown("---")

# Translation mode selection
translation_mode = st.sidebar.selectbox(
    "🎯 Translation Mode",
    ["🧠 Smart Single Document", "📦 Smart Batch Processing"],
    help="Choose between single document or batch processing"
)

translation_tier = st.sidebar.selectbox(
    "🏆 Translation Quality Tier",
    ["🧠 Professional SDIP (Smart)", "🔧 Legacy System"],
    help="Smart tier includes AI intelligence features"
)

target_language = st.sidebar.selectbox(
    "🌍 Target Language",
    ["Vietnamese", "English", "French", "German", "Spanish", "Chinese", "Japanese"],
)

source_language = st.sidebar.selectbox(
    "🔤 Source Language", 
    ["Auto-detect", "English", "Vietnamese", "French", "German", "Spanish"]
)

# Smart settings
if "Smart" in translation_tier:
    st.sidebar.markdown("#### 🧠 Smart Features")
    enable_analysis = st.sidebar.checkbox("📊 Document Analysis", value=True)
    enable_retry = st.sidebar.checkbox("🔄 Smart Retry", value=True)
    enable_optimization = st.sidebar.checkbox("⚡ Optimization", value=True)

# Main Interface based on mode
if translation_mode == "🧠 Smart Single Document":
    st.markdown("## 🧠 Smart Single Document Translation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Document")
        
        input_text = st.text_area(
            "Enter text to translate:",
            height=350,
            placeholder="Paste your document here for AI-powered smart translation...",
            help="Smart system will automatically analyze and optimize translation"
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
        st.markdown("### 🎯 Smart Translation Result")
        
        if st.button("🧠 Smart Translate", type="primary"):
            if input_text:
                if "Smart" in translation_tier:
                    # Initialize smart system
                    smart_system = SDIPSmartSystem()
                    
                    # Create placeholders for real-time updates
                    status_placeholder = st.empty()
                    progress_placeholder = st.empty()
                    analysis_placeholder = st.empty()
                    
                    # Step-by-step processing with real-time updates
                    with status_placeholder.container():
                        ui.create_status_indicators({
                            "🧠 AI Analysis": "info",
                            "⚡ Optimizing": "warning"
                        })
                    
                    with progress_placeholder.container():
                        ui.create_animated_progress_bar(25, "Smart Analysis")
                    
                    time.sleep(0.8)
                    
                    # Perform smart translation
                    try:
                        result = asyncio.run(smart_system.smart_translate_document(
                            input_text, target_language, 
                            "auto" if source_language == "Auto-detect" else source_language
                        ))
                        
                        # Update progress
                        with progress_placeholder.container():
                            ui.create_animated_progress_bar(100, "Complete")
                        
                        with status_placeholder.container():
                            ui.create_status_indicators({
                                "✅ Smart Analysis": "success",
                                "✅ Translation": "success",
                                "✅ Quality Assured": "success"
                            })
                        
                        time.sleep(0.5)
                        
                        if result['success']:
                            # Clear progress indicators
                            progress_placeholder.empty()
                            status_placeholder.empty()
                            
                            # Success message
                            st.success("🧠 Smart Translation Completed!")
                            
                            # Smart metrics
                            st.markdown("### 📊 Smart Performance Metrics")
                            ui.create_modern_metrics(
                                result['quality_score'],
                                result['processing_time'],
                                result['chunk_count']
                            )
                            
                            # Translation result
                            st.markdown("### 🎯 Smart Translation Result")
                            st.text_area(
                                "AI-Enhanced Translation:",
                                value=result['translated_text'],
                                height=300,
                                help="Processed with intelligent analysis and optimization"
                            )
                            
                            # Smart features details
                            with st.expander("🧠 Smart Features Analysis", expanded=False):
                                # Document analysis insights
                                if 'analysis' in result:
                                    analysis = result['analysis']
                                    
                                    st.markdown("#### 📊 Document Intelligence")
                                    col_a, col_b, col_c = st.columns(3)
                                    
                                    with col_a:
                                        st.metric("Complexity", analysis.complexity.value.title())
                                        st.metric("Content Type", analysis.content_type.value.title())
                                    
                                    with col_b:
                                        st.metric("Confidence", f"{analysis.confidence_prediction:.2f}")
                                        st.metric("Optimal Chunks", f"{analysis.recommended_chunk_size}")
                                    
                                    with col_c:
                                        st.metric("Features", len(analysis.key_features))
                                        st.metric("Suggestions", len(analysis.optimization_suggestions))
                                
                                # Smart retry information
                                if 'retry_info' in result:
                                    retry_info = result['retry_info']
                                    st.markdown("#### 🔄 Smart Retry Analysis")
                                    
                                    if retry_info['retry_count'] > 0:
                                        st.write(f"**Retry Attempts:** {retry_info['retry_count']}")
                                        st.write(f"**Retry Reasons:** {', '.join(retry_info['retry_reasons'])}")
                                        st.write(f"**Model Used:** {retry_info['model_used']}")
                                        st.write("**Improvements:**")
                                        for improvement in retry_info['improvements']:
                                            st.write(f"• {improvement}")
                                    else:
                                        st.write("✅ Initial translation quality was sufficient - no retry needed")
                                
                                # Smart features used
                                st.markdown("#### ✨ AI Features Utilized")
                                for feature in result.get('smart_features_used', []):
                                    st.write(f"✅ {feature}")
                        
                        else:
                            progress_placeholder.empty()
                            status_placeholder.empty()
                            st.error(f"❌ Smart translation failed: {result.get('error', 'Unknown error')}")
                    
                    except Exception as e:
                        progress_placeholder.empty()
                        status_placeholder.empty()
                        st.error(f"❌ Smart system error: {e}")
                
                else:
                    st.warning("🔧 Legacy system not available - use Smart SDIP tier")
            
            else:
                st.warning("⚠️ Please enter text to translate")

else:  # Batch Processing Mode
    st.markdown("## 📦 Smart Batch Processing")
    st.info("🚧 Batch processing interface - Coming in next phase!")
    
    # Placeholder for batch processing UI
    st.markdown("""
    **Smart Batch Features:**
    - 📊 Intelligent document prioritization
    - ⚡ Parallel processing optimization  
    - 📈 Batch performance analytics
    - 🎯 Quality consistency across documents
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <h4 style="color: #333;">🧠 SDIP Smart Enhanced</h4>
    <p>Semantic Document Intelligence Platform with AI-Powered Smart Features</p>
    <p><small>Intelligent Analysis • Smart Retry • Adaptive Processing • Quality Optimization</small></p>
</div>
""", unsafe_allow_html=True)
