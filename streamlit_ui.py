"""
Simple Streamlit UI for Translate Export Agent
"""
import streamlit as st
import requests
import json

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

st.set_page_config(
    page_title="Translate Export Agent",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Translate Export Agent")
st.markdown("AI-powered translation and content transformation")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # API Health Check
    try:
        response = requests.get(f"{API_BASE_URL}/health/")
        health_data = response.json()
        
        if health_data["status"] == "healthy":
            st.success("✅ System Healthy")
        else:
            st.warning(f"⚠️ System {health_data['status']}")
            
        # Show components
        with st.expander("System Components"):
            for component in health_data["components"]:
                icon = "✅" if component["status"] == "healthy" else "⚠️"
                st.write(f"{icon} {component['name']}: {component['message']}")
    except:
        st.error("❌ Cannot connect to API")

# Main content
tab1, tab2, tab3 = st.tabs(["🌐 Translation", "📝 Content Transformation", "📊 About"])

# Translation Tab
with tab1:
    st.header("Translation Service")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Get languages
        try:
            response = requests.get(f"{API_BASE_URL}/translate/languages")
            languages = response.json()["languages"]
            lang_options = {lang["name"]: lang["code"] for lang in languages}
        except:
            lang_options = {"English": "en", "Vietnamese": "vi"}
        
        source_lang = st.selectbox(
            "Source Language",
            options=list(lang_options.keys()),
            index=0
        )
        
        source_text = st.text_area(
            "Text to translate",
            height=200,
            placeholder="Enter text here..."
        )
    
    with col2:
        target_lang = st.selectbox(
            "Target Language",
            options=list(lang_options.keys()),
            index=1
        )
        
        if st.button("🌐 Translate", type="primary"):
            if source_text:
                with st.spinner("Translating..."):
                    try:
                        payload = {
                            "text": source_text,
                            "source_lang": lang_options[source_lang],
                            "target_lang": lang_options[target_lang]
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/translate/",
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.text_area(
                                "Translation Result",
                                value=result["translated_text"],
                                height=200
                            )
                            st.caption(f"Confidence: {result['confidence']:.2%}")
                        else:
                            error = response.json()
                            st.error(f"Translation failed: {error.get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter text to translate")

# Content Transformation Tab
with tab2:
    st.header("Content Transformation")
    
    # Get transformation types
    try:
        response = requests.get(f"{API_BASE_URL}/content/types")
        types = response.json()["types"]
    except:
        types = [
            {"id": "podcast", "name": "Podcast Script"},
            {"id": "education", "name": "Education Module"},
            {"id": "video", "name": "Video Script"}
        ]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        content = st.text_area(
            "Content to transform",
            height=300,
            placeholder="Enter your content here..."
        )
    
    with col2:
        transform_type = st.selectbox(
            "Transformation Type",
            options=[t["name"] for t in types],
            format_func=lambda x: x
        )
        
        audience = st.selectbox(
            "Target Audience",
            options=["children", "teenagers", "adults", "professionals"]
        )
        
        difficulty = st.selectbox(
            "Difficulty Level",
            options=["beginner", "intermediate", "advanced"]
        )
        
        if st.button("🎯 Transform", type="primary"):
            if content:
                with st.spinner("Transforming content..."):
                    try:
                        # Find type id
                        type_id = next(t["id"] for t in types if t["name"] == transform_type)
                        
                        payload = {
                            "content": content,
                            "transformation_type": type_id,
                            "target_audience": audience,
                            "difficulty": difficulty
                        }
                        
                        response = requests.post(
                            f"{API_BASE_URL}/content/transform",
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            st.success("✅ Transformation Complete!")
                            
                            st.text_area(
                                "Transformed Content",
                                value=result["transformed_content"],
                                height=400
                            )
                            
                            # Show metadata
                            with st.expander("📊 Metadata"):
                                st.json(result["metadata"])
                                st.metric("Quality Score", f"{result['quality_score']:.2f}")
                                st.metric("Processing Time", f"{result['processing_time']:.2f}s")
                        else:
                            error = response.json()
                            st.error(f"Transformation failed: {error.get('detail', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter content to transform")

# About Tab
with tab3:
    st.header("About Translate Export Agent")
    
    st.markdown("""
    ### Features
    
    - 🌐 **Multi-language Translation**: Support for 8+ languages
    - 🎙️ **Podcast Generation**: Convert content to engaging podcast scripts
    - 📚 **Education Modules**: Create structured learning materials
    - 🎬 **Video Scripts**: Generate screenplays and AI prompts
    - 🤖 **AI-Powered**: LLM enhancement with fallback mechanisms
    
    ### API Documentation
    
    Access the interactive API documentation at:
    - [Swagger UI](http://localhost:8000/docs)
    - [ReDoc](http://localhost:8000/redoc)
    
    ### System Architecture
    
    - Clean architecture with separation of concerns
    - Error handling and retry mechanisms
    - Performance monitoring and health checks
    - Extensible plugin system
    """)
    
    # Show current configuration
    with st.expander("🔧 Current Configuration"):
        st.code("""
# API Endpoints
- POST /api/v1/translate/
- GET  /api/v1/translate/languages
- POST /api/v1/content/transform
- GET  /api/v1/content/types
- GET  /api/v1/health/
        """)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and FastAPI")
