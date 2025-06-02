# ui_components/modern_ui_system.py
"""
Modern UI System - Step 1: Ultra-Modern Interface
Based on Modern Minimalism with sophisticated color blocks and charts
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any

class ModernUISystem:
    """
    Modern UI System with sophisticated design principles:
    - Modern Minimalism
    - Harmonious color blocks
    - Subtle micro-interactions
    - Breathing space and rhythm
    """
    
    @staticmethod
    def setup_modern_theme():
        """Setup modern theme with sophisticated design"""
        st.set_page_config(
            page_title="SDIP Ultra - AI Document Intelligence",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Modern Minimalism CSS with sophisticated aesthetics
        st.markdown("""
        <style>
        /* Import premium fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@100;200;300;400;500;600;700&display=swap');
        
        /* CSS Variables for consistent theming */
        :root {
            /* Base Colors - Muted and Natural */
            --bg-primary: #FAFBFC;
            --bg-secondary: #F5F7FA;
            --bg-accent: #E8F4F8;
            
            /* Sophisticated Color Blocks */
            --block-overview: #E6F4F1;
            --block-analysis: #FAF4EB;
            --block-action: #F0F8FF;
            --block-progress: #FFF5F5;
            
            /* Harmonious Palette */
            --mint-soft: #E6F4F1;
            --mint-medium: #B8E6D3;
            --mint-deep: #4A9B8E;
            
            --beige-soft: #FAF4EB;
            --beige-medium: #F5E6D3;
            --beige-deep: #B8860B;
            
            --blue-soft: #F0F8FF;
            --blue-medium: #E1F2FF;
            --blue-deep: #4A90E2;
            
            /* Text Colors - Never Pure Black */
            --text-primary: #2E2E2E;
            --text-secondary: #333333;
            --text-muted: #6B7280;
            --text-light: #9CA3AF;
            
            /* Sophisticated Shadows */
            --shadow-soft: 0 2px 8px rgba(0, 0, 0, 0.06);
            --shadow-medium: 0 4px 16px rgba(0, 0, 0, 0.08);
            --shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.12);
            
            /* Glassmorphism Effects */
            --glass-bg: rgba(255, 255, 255, 0.7);
            --glass-border: rgba(255, 255, 255, 0.3);
            --glass-blur: blur(12px);
        }
        
        /* Global Styling */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
            color: var(--text-primary);
        }
        
        .main .block-container {
            padding: 2rem 3rem 4rem 3rem;
            max-width: 100%;
        }
        
        /* Modern Hero Section */
        .modern-hero {
            background: var(--glass-bg);
            backdrop-filter: var(--glass-blur);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            padding: 3rem 2.5rem;
            margin: 1.5rem 0 3rem 0;
            text-align: center;
            box-shadow: var(--shadow-medium);
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .modern-hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, var(--mint-deep), var(--blue-deep), var(--beige-deep));
            opacity: 0.6;
        }
        
        .modern-hero:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-hover);
        }
        
        .modern-hero h1 {
            font-size: 3rem;
            font-weight: 700;
            margin: 0 0 1rem 0;
            color: var(--text-primary);
            line-height: 1.2;
        }
        
        .modern-hero .subtitle {
            font-size: 1.2rem;
            color: var(--text-muted);
            font-weight: 400;
            margin: 0 0 1.5rem 0;
            line-height: 1.5;
        }
        
        .modern-hero .status-badge {
            display: inline-flex;
            align-items: center;
            background: var(--mint-soft);
            color: var(--mint-deep);
            padding: 0.75rem 1.5rem;
            border-radius: 50px;
            font-weight: 500;
            font-size: 0.9rem;
            border: 1px solid var(--mint-medium);
            transition: all 0.2s ease;
        }
        
        .modern-hero .status-badge:hover {
            background: var(--mint-medium);
            transform: scale(1.02);
        }
        
        /* Sophisticated Color Blocks */
        .color-block {
            border-radius: 20px;
            padding: 2rem;
            margin: 1.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.5);
            box-shadow: var(--shadow-soft);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        .color-block::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
        }
        
        .color-block:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-hover);
        }
        
        .block-overview {
            background: var(--block-overview);
            border-left: 4px solid var(--mint-deep);
        }
        
        .block-analysis {
            background: var(--block-analysis);
            border-left: 4px solid var(--beige-deep);
        }
        
        .block-action {
            background: var(--block-action);
            border-left: 4px solid var(--blue-deep);
        }
        
        .block-progress {
            background: var(--block-progress);
            border-left: 4px solid #E53E3E;
        }
        
        /* Modern Cards with Breathing Space */
        .modern-card {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: var(--shadow-soft);
            border: 1px solid #F1F5F9;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        
        .modern-card:hover {
            box-shadow: var(--shadow-medium);
            transform: translateY(-1px);
            border-color: #E2E8F0;
        }
        
        .modern-card h3 {
            color: var(--text-primary);
            font-weight: 600;
            font-size: 1.25rem;
            margin: 0 0 1rem 0;
            line-height: 1.4;
        }
        
        .modern-card p {
            color: var(--text-muted);
            line-height: 1.6;
            margin: 0;
        }
        
        /* Sophisticated Metrics */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .metric-card {
            background: white;
            border-radius: 16px;
            padding: 1.5rem;
            text-align: center;
            box-shadow: var(--shadow-soft);
            border: 1px solid #F8FAFC;
            transition: all 0.15s ease;
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--mint-deep), var(--blue-deep));
            opacity: 0;
            transition: opacity 0.2s ease;
        }
        
        .metric-card:hover::after {
            opacity: 1;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-medium);
            border-color: #E2E8F0;
        }
        
        .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0 0 0.5rem 0;
            line-height: 1;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        /* Modern Progress with Breathing Animation */
        .modern-progress {
            background: #F8FAFC;
            border-radius: 12px;
            padding: 6px;
            margin: 1.5rem 0;
            box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.06);
        }
        
        .progress-bar {
            height: 28px;
            background: linear-gradient(90deg, var(--mint-deep), var(--blue-deep));
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            animation: breathe 2s ease-in-out infinite;
        }
        
        @keyframes breathe {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.01); }
        }
        
        .progress-bar::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* Modern Buttons with Micro-interactions */
        .stButton > button {
            background: linear-gradient(135deg, var(--mint-deep), var(--blue-deep));
            border: none;
            border-radius: 12px;
            color: white;
            font-weight: 600;
            padding: 0.875rem 2rem;
            font-size: 0.95rem;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-soft);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: var(--shadow-hover);
        }
        
        .stButton > button:active {
            transform: translateY(0) scale(0.98);
        }
        
        /* Sophisticated Status Indicators */
        .status-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
            margin: 1rem 0;
            justify-content: center;
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 500;
            font-size: 0.85rem;
            transition: all 0.15s ease;
            border: 1px solid transparent;
        }
        
        .status-indicator:hover {
            transform: scale(1.05);
        }
        
        .status-success {
            background: #F0FDF4;
            color: #15803D;
            border-color: #BBF7D0;
        }
        
        .status-info {
            background: #F0F9FF;
            color: #0369A1;
            border-color: #BAE6FD;
        }
        
        .status-warning {
            background: #FFFBEB;
            color: #D97706;
            border-color: #FED7AA;
        }
        
        .status-processing {
            background: var(--block-progress);
            color: #DC2626;
            border-color: #FECACA;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.8; }
        }
        
        /* Modern Inputs with Sophisticated Feel */
        .stTextArea textarea, 
        .stTextInput input, 
        .stSelectbox select {
            border: 1px solid #E2E8F0 !important;
            border-radius: 8px !important;
            background: white !important;
            color: var(--text-primary) !important;
            transition: all 0.2s ease !important;
            padding: 0.75rem !important;
        }
        
        .stTextArea textarea:focus, 
        .stTextInput input:focus, 
        .stSelectbox select:focus {
            border-color: var(--mint-deep) !important;
            box-shadow: 0 0 0 3px rgba(74, 155, 142, 0.1) !important;
            outline: none !important;
        }
        
        /* File Uploader Modern Style */
        .stFileUploader > div {
            border: 2px dashed #CBD5E1;
            border-radius: 12px;
            background: #FAFBFC;
            transition: all 0.2s ease;
            padding: 2rem;
        }
        
        .stFileUploader > div:hover {
            border-color: var(--mint-deep);
            background: var(--mint-soft);
        }
        
        /* Hide Streamlit Elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* Modern Sidebar */
        .css-1d391kg {
            background: white;
            border-right: 1px solid #F1F5F9;
        }
        
        /* Typography Improvements */
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-primary);
            font-weight: 600;
            line-height: 1.3;
        }
        
        p {
            color: var(--text-muted);
            line-height: 1.6;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem 1.5rem 2rem 1.5rem;
            }
            
            .modern-hero {
                padding: 2rem 1.5rem;
            }
            
            .modern-hero h1 {
                font-size: 2rem;
            }
            
            .metric-grid {
                grid-template-columns: 1fr;
                gap: 1rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_modern_hero():
        """Create sophisticated hero section"""
        st.markdown("""
        <div class="modern-hero">
            <h1>🚀 SDIP Ultra</h1>
            <p class="subtitle">AI-Powered Document Intelligence Platform<br>
            <em>Modern • Sophisticated • Intelligent</em></p>
            <div class="status-badge">
                ✨ Production Ready • Real-Time Processing
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_color_block(title: str, content: str, block_type: str = "overview", icon: str = "📊"):
        """Create sophisticated color block"""
        st.markdown(f"""
        <div class="color-block block-{block_type}">
            <h3 style="margin: 0 0 1rem 0; color: var(--text-primary); font-weight: 600;">
                {icon} {title}
            </h3>
            <div style="color: var(--text-muted); line-height: 1.6;">
                {content}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_modern_metrics(metrics: List[Dict[str, Any]]):
        """Create sophisticated metrics grid"""
        cols = st.columns(len(metrics))
        
        for i, metric in enumerate(metrics):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{metric['value']}</div>
                    <div class="metric-label">{metric['label']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    @staticmethod
    def create_modern_progress(progress: float, label: str = "Processing"):
        """Create sophisticated progress with breathing animation"""
        st.markdown(f"""
        <div class="modern-progress">
            <div class="progress-bar" style="width: {progress}%;">
                {label} • {progress:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def create_status_indicators(statuses: Dict[str, str]):
        """Create sophisticated status indicators"""
        status_html = '<div class="status-grid">'
        
        for status, status_type in statuses.items():
            icon = {
                'success': '✅',
                'info': 'ℹ️',
                'warning': '⚠️',
                'processing': '🔄'
            }.get(status_type, '•')
            
            status_html += f'''
            <div class="status-indicator status-{status_type}">
                <span>{icon}</span>
                <span>{status}</span>
            </div>
            '''
        
        status_html += '</div>'
        st.markdown(status_html, unsafe_allow_html=True)
    
    @staticmethod
    def create_modern_card(title: str, content: str, icon: str = "📄"):
        """Create modern card with subtle interactions"""
        st.markdown(f"""
        <div class="modern-card">
            <h3>{icon} {title}</h3>
            <p>{content}</p>
        </div>
        """, unsafe_allow_html=True)
