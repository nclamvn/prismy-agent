"""
Enhanced AI Commander with PRISM Video DNA Integration
SUPERIOR TO SORA - Perfect visual continuity for AI video generation
"""

import streamlit as st
import sys
import os
import json
import time
from datetime import datetime

# Add paths for imports
current_dir = os.path.dirname(__file__)
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)

# Import existing AI Commander components
try:
    from src.ai_commander.enhanced_commander.hotel_concierge_claude import EnhancedProductionCommander as ClaudeCommander
    from src.infrastructure.content_transformation.unified_video_processor import UnifiedVideoProcessor, VideoOutputFormat
    VIDEO_DNA_AVAILABLE = True
except ImportError as e:
    VIDEO_DNA_AVAILABLE = False
    st.error(f"Import error: {e}")

def main():
    st.set_page_config(
        page_title="🚀 AI Commander + Video DNA",
        page_icon="🧬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced header with Video DNA
    st.markdown("""
    # 🚀 AI Commander + 🧬 PRISM Video DNA
    ## Enterprise AI Platform - SUPERIOR TO SORA
    """)
    
    # Sidebar with enhanced options
    with st.sidebar:
        st.markdown("## 🎛️ Control Panel")
        
        # User info
        user_name = st.text_input("👤 Tên của bạn:", value="Lâm Nguyễn")
        expertise_level = st.selectbox(
            "🎯 Expertise Level:",
            ["Beginner", "Intermediate", "Advanced", "Expert"]
        )
        
        # Feature selection
        st.markdown("### 🛠️ AI Features")
        feature_mode = st.radio(
            "Select AI Mode:",
            [
                "🤖 AI Commander (Conversation)",
                "🎬 Video DNA Generation", 
                "📄 Document Processing",
                "🎙️ Podcast Creation",
                "📚 Education Module"
            ]
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Settings")
        
        if feature_mode == "🎬 Video DNA Generation":
            video_duration = st.slider("🎬 Target Duration (seconds):", 5, 15, 8)
            export_platform = st.selectbox(
                "🚀 Export Platform:",
                ["all", "runway", "pika", "stable_video", "sora"]
            )

    # Main content area
    if feature_mode == "🎬 Video DNA Generation":
        render_video_dna_interface(user_name, video_duration, export_platform)
    elif feature_mode == "🤖 AI Commander (Conversation)":
        render_ai_commander_interface(user_name, expertise_level)
    else:
        st.info(f"🚧 {feature_mode} - Coming soon in enhanced AI Commander!")

def render_video_dna_interface(user_name: str, duration: int, platform: str):
    """Render Video DNA generation interface"""
    
    st.markdown("## 🧬 PRISM Video DNA Generation")
    st.markdown("**Perfect visual continuity for AI video generation - SUPERIOR TO SORA**")
    
    if not VIDEO_DNA_AVAILABLE:
        st.error("❌ Video DNA Engine not available. Please check installation.")
        return
    
    # Input methods
    input_method = st.radio(
        "📥 Input Method:",
        ["✍️ Text Input", "📁 File Upload"]
    )
    
    script_content = ""
    
    if input_method == "✍️ Text Input":
        script_content = st.text_area(
            "🎬 Enter your movie script or video content:",
            height=200,
            placeholder="""Example:
FADE IN:

EXT. MODERN OFFICE - DAY

ALEX (30, entrepreneur) types on laptop.

ALEX
Today we change everything.

SARAH (28, AI engineer) joins him.

SARAH
The future starts now.

FADE OUT."""
        )
    
    else:  # File Upload
        uploaded_file = st.file_uploader(
            "📁 Upload script file:",
            type=['txt', 'pdf', 'docx'],
            help="Supported formats: TXT, PDF, DOCX"
        )
        
        if uploaded_file:
            if uploaded_file.type == "text/plain":
                script_content = str(uploaded_file.read(), "utf-8")
                st.success(f"✅ File uploaded: {uploaded_file.name}")
            else:
                st.warning("📄 PDF/DOCX processing coming soon. Please use TXT files.")
    
    # Generation controls
    col1, col2 = st.columns([2, 1])
    
    with col1:
        generate_button = st.button(
            "🚀 Generate Video DNA",
            type="primary",
            disabled=not script_content.strip()
        )
    
    with col2:
        if st.button("📋 Load Demo Script"):
            st.session_state.demo_script = """
FADE IN:

EXT. FUTURISTIC STARTUP - DAY

MINH (35, Vietnamese tech CEO) walks through glass corridors.

MINH
Chúng ta đã sẵn sàng cho cuộc cách mạng AI.

LAN (30, AI researcher) shows holographic data.

LAN  
PRISM engine đã vượt qua Sora.

They smile as holographic videos play around them.

FADE OUT.
"""
            st.rerun()
    
    # Use demo script if loaded
    if hasattr(st.session_state, 'demo_script') and not script_content.strip():
        script_content = st.session_state.demo_script
        st.info("📋 Demo script loaded. Click 'Generate Video DNA' to process.")
    
    # Processing and results
    if generate_button and script_content.strip():
        with st.spinner("🧬 Processing with PRISM Video DNA Engine..."):
            
            # Progress indicators
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate processing steps
            steps = [
                "🔍 Analyzing script structure...",
                "👥 Extracting characters with AI intelligence...", 
                "🎬 Enhanced scene analysis...",
                "🧬 Generating DNA fingerprints...",
                "⚡ Creating ultra-compact DNA chain...",
                "🚀 Preparing export formats..."
            ]
            
            for i, step in enumerate(steps):
                status_text.text(step)
                progress_bar.progress((i + 1) / len(steps))
                time.sleep(0.3)
            
            # Generate with Unified Video Processor
            processor = UnifiedVideoProcessor()
            
            # Create transformation request
            from src.infrastructure.content_transformation import (
                TransformationRequest, 
                TransformationType,
                TargetAudience,
                ContentDifficulty
            )
            
            request = TransformationRequest(
                source_text=script_content,
                transformation_type=TransformationType.VIDEO_SCENARIO,
                target_audience=TargetAudience.ADULTS,
                difficulty_level=ContentDifficulty.INTERMEDIATE,
                language="en",
                duration_target=duration
            )
            
            # Generate AI prompts for the selected platform
            response = processor.transform_content(
                request,
                output_format=VideoOutputFormat.AI_PROMPTS,
                target_platform=platform.lower() if platform else "sora"
            )
            
            # Convert response to expected format
            result = {
                "success": bool(response.transformed_content),
                "error": response.metadata.get("error") if not response.transformed_content else None
            }
            
            if response.transformed_content:
                output_data = json.loads(response.transformed_content)
                result.update(output_data)
            
            # Clear progress
            progress_bar.empty()
            status_text.empty()
            
            # Display results
            if result["success"]:
                display_video_dna_results(result, user_name, platform)
            else:
                st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")

def display_video_dna_results(result: dict, user_name: str, platform: str):
    """Display Video DNA generation results"""
    
    # Success header
    st.success("✅ Video DNA Generation Complete!")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🎯 Quality Grade",
            result["quality"]["grade"],
            f"{result['quality']['overall_score']:.3f}"
        )
    
    with col2:
        st.metric(
            "🎬 Video Chunks", 
            result["video_data"]["total_chunks"],
            f"{result['video_data']['total_duration']:.1f}s total"
        )
    
    with col3:
        st.metric(
            "👥 Characters",
            len(result["video_data"]["characters"]),
            f"{result['quality']['character_accuracy']:.1%} accuracy"
        )
    
    with col4:
        st.metric(
            "⚡ Processing",
            f"{result['processing_time']:.3f}s",
            result["prism_info"]["processing_speed"]
        )
    
    # Detailed results
    tab1, tab2, tab3, tab4 = st.tabs(["🧬 DNA Chain", "🎬 Video Chunks", "📊 Analytics", "🚀 Export"])
    
    with tab1:
        st.markdown("### 🧬 Ultra-Compact DNA Chain")
        st.markdown("**Perfect visual continuity across all chunks:**")
        
        for i, dna_hash in enumerate(result["dna_chain"]):
            st.code(f"Chunk {i+1}: DNA Hash {dna_hash}", language="text")
        
        st.info("🔗 Each DNA hash ensures perfect character and visual continuity between video chunks.")
    
    with tab2:
        st.markdown("### 🎬 Generated Video Chunks")
        
        for chunk in result["chunks"]:
            with st.expander(f"🎥 Chunk {chunk['id']}: {chunk['scene_type'].title()} ({chunk['duration']}s)"):
                
                # Chunk metadata
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"**Content:** {chunk['content']}")
                    st.markdown(f"**Characters:** {', '.join(chunk['characters']) if chunk['characters'] else 'None'}")
                    st.markdown(f"**DNA Hash:** `{chunk['dna_hash']}`")
                
                with col2:
                    st.markdown(f"**Emotional Tone:** {chunk['emotional_tone']}")
                    st.markdown(f"**Visual Complexity:** {chunk['visual_complexity']}")
                    st.markdown(f"**AI Ready:** {'✅' if chunk['ai_generation_ready'] else '❌'}")
                
                # AI Prompt
                st.markdown("**🚀 AI Generation Prompt:**")
                st.code(chunk["ai_prompt"], language="text")
    
    with tab3:
        st.markdown("### 📊 Quality Analytics")
        
        # Quality breakdown
        quality_data = result["quality"]
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Quality Scores:**")
            st.progress(quality_data["character_accuracy"], text=f"Character Accuracy: {quality_data['character_accuracy']:.1%}")
            st.progress(quality_data["scene_intelligence"], text=f"Scene Intelligence: {quality_data['scene_intelligence']:.1%}")
            st.progress(quality_data["visual_continuity"], text=f"Visual Continuity: {quality_data['visual_continuity']:.1%}")
        
        with col2:
            st.markdown("**Characters Detected:**")
            for char in result["video_data"]["characters"]:
                st.markdown(f"• {char}")
            
            st.markdown(f"**Language:** {result['video_data']['language']}")
            st.markdown(f"**Session ID:** `{result['session_id']}`")
    
    with tab4:
        st.markdown("### 🚀 Export Formats")
        
        export_data = result["exports"]
        
        # Platform selection
        if platform != "all":
            st.info(f"🎯 Optimized for: **{platform.title()}**")
        
        # Export buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download JSON"):
                st.download_button(
                    "💾 Download Video DNA",
                    json.dumps(result, indent=2),
                    file_name=f"prism_video_dna_{result['session_id']}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🎬 Runway ML Export"):
                st.info("🚀 Runway ML prompts ready for generation!")
        
        with col3:
            if st.button("🎨 Pika Labs Export"):
                st.info("🚀 Pika Labs prompts ready for generation!")
        
        # Superiority statement
        st.markdown("---")
        st.markdown(f"### 🏆 {result['prism_info']['superiority']}")
        st.markdown(f"**Engine:** {result['prism_info']['engine']}")
        st.markdown(f"**Generated:** {result['prism_info']['timestamp']}")

def render_ai_commander_interface(user_name: str, expertise_level: str):
    """Render traditional AI Commander interface"""
    
    st.markdown("## 🤖 AI Commander Conversation")
    st.markdown("**Intelligent conversation with Claude AI**")
    
    # File upload for AI Commander
    uploaded_file = st.file_uploader(
        "📁 Upload document (optional):",
        type=['txt', 'pdf', 'docx'],
        help="Upload document for AI analysis"
    )
    
    # Conversation input
    user_request = st.text_area(
        "💬 Your request:",
        height=150,
        placeholder="Ask AI Commander anything..."
    )
    
    if st.button("🚀 Start AI Commander Conversation", type="primary"):
        if user_request.strip():
            with st.spinner("🤖 AI Commander processing..."):
                # Simulate AI Commander response
                time.sleep(1)
                
                st.success("✅ AI Commander Response:")
                st.markdown(f"""
                Hello **{user_name}**! 
                
                Based on your **{expertise_level}** level expertise, I understand you want to: 
                
                *{user_request}*
                
                I'm processing this with the AI Commander engine. This is a simulation response since we're focusing on Video DNA integration.
                
                For full AI Commander functionality, the conversation engine is ready and can be activated.
                """)
        else:
            st.warning("⚠️ Please enter your request.")

if __name__ == "__main__":
    main()
