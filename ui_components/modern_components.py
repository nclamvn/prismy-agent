# ui_components/modern_components.py
"""
Modern UI Components for SDIP - Basic Version
Essential UI elements with glassmorphism design
"""

import streamlit as st

class ModernUIComponents:
    """Modern UI components with glassmorphism styling"""
    
    @staticmethod
    def setup_page_config():
        """Setup page configuration with custom CSS"""
        st.set_page_config(
            page_title="SDIP - Enhanced",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Basic glassmorphism CSS
        st.markdown("""
        <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            font-family: 'Inter', sans-serif;
        }
        
        /* Premium gradient header */
        .premium-gradient {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 16px;
            color: white;
            margin: 15px 0;
            text-align: center;
        }
        
        /* Modern metric cards */
        .metric-card {
            background: linear-gradient(145deg, #f8f9fa, #ffffff);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
            margin: 10px 0;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.15);
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-top: 8px;
            font-weight: 500;
        }
        
        /* Animated progress bar */
        .progress-container {
            background: #f0f2f6;
            border-radius: 12px;
            padding: 4px;
            margin: 15px 0;
        }
        
        .progress-bar {
            height: 24px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 8px;
            transition: width 1s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
        }
        
        /* Status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 500;
            margin: 5px;
        }
        
        .status-success {
            background: rgba(40, 167, 69, 0.1);
            color: #28a745;
            border: 1px solid rgba(40, 167, 69, 0.3);
        }
        
        .status-info {
            background: rgba(23, 162, 184, 0.1);
            color: #17a2b8;
            border: 1px solid rgba(23, 162, 184, 0.3);
        }
        
        .status-warning {
            background: rgba(255, 193, 7, 0.1);
            color: #ffc107;
            border: 1px solid rgba(255, 193, 7, 0.3);
        }
        
        /* Enhanced buttons */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            padding: 12px 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_hero_section():
        """Create premium hero section"""
        st.markdown("""
        <div class="premium-gradient">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">
                🚀 SDIP Enhanced
            </h1>
            <p style="margin: 10px 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Semantic Document Intelligence Platform with Modern UI
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_modern_metrics(quality_score: float, processing_time: float, chunk_count: int):
        """Create modern metrics display"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{quality_score:.2f}</div>
                <div class="metric-label">Quality Score</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{processing_time:.2f}s</div>
                <div class="metric-label">Processing Time</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{chunk_count}</div>
                <div class="metric-label">Semantic Chunks</div>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def create_animated_progress_bar(progress: float, label: str = "Processing"):
        """Create animated progress bar"""
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress}%;">
                {label} {progress:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_status_indicators(status_data: dict):
        """Create status indicators"""
        status_html = ""
        for status, type_class in status_data.items():
            status_html += f'<span class="status-indicator status-{type_class}">{status}</span>'
        
        st.markdown(f'<div style="margin: 10px 0;">{status_html}</div>', unsafe_allow_html=True)
