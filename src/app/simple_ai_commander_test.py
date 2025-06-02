"""Simple AI Commander Test App"""
import streamlit as st
import requests
import json

# Page config MUST be first
st.set_page_config(
    page_title="AI Commander Test",
    page_icon="🤖",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://localhost:8000"
AI_COMMANDER_ENDPOINT = f"{API_BASE_URL}/api/v1/ai-commander/chat"

def main():
    st.title("🤖 AI Commander - Quick Test")
    st.markdown("Test connection between Streamlit and FastAPI backend")
    
    # Create columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("📝 Your Request")
        user_input = st.text_area(
            "What would you like to create?",
            height=100,
            placeholder="Example: Create a video about AI trends for our Q3 meeting"
        )
        
        if st.button("🚀 Send to AI Commander", type="primary"):
            if user_input:
                with st.spinner("Processing with AI Commander..."):
                    try:
                        # Call API
                        response = requests.post(
                            AI_COMMANDER_ENDPOINT,
                            json={
                                "message": user_input,
                                "session_id": "streamlit-test-001"
                            }
                        )
                        
                        if response.status_code == 200:
                            data = response.json()
                            
                            # Display response
                            st.success("✅ AI Commander Response:")
                            st.write(data.get("response", "No response"))
                            
                            # Show details in sidebar
                            with col2:
                                st.subheader("🎯 Analysis Details")
                                st.metric("Detected Service", data.get("intent", "Unknown"))
                                st.metric("Confidence", f"{data.get('confidence', 0):.0%}")
                                
                                if data.get("suggestions"):
                                    st.write("**Follow-up Questions:**")
                                    for q in data["suggestions"]:
                                        st.write(f"• {q}")
                        else:
                            st.error(f"API Error: {response.status_code}")
                            
                    except Exception as e:
                        st.error(f"Connection Error: {str(e)}")
            else:
                st.warning("Please enter a request")
    
    with col2:
        st.subheader("ℹ️ API Status")
        if st.button("Check Connection"):
            try:
                health = requests.get(f"{API_BASE_URL}/health")
                if health.status_code == 200:
                    st.success("✅ API is running!")
                    st.json(health.json())
                else:
                    st.error("❌ API not responding")
            except:
                st.error("❌ Cannot connect to API")
        
        st.markdown("---")
        st.caption("Backend: http://localhost:8000")
        st.caption("Docs: http://localhost:8000/api/docs")

if __name__ == "__main__":
    main()
