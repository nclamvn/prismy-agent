"""Modern theme management for Streamlit application."""

import streamlit as st
from typing import Dict, Any


class ThemeManager:
    """Manages application themes and styling."""
    
    def __init__(self):
        self.current_theme = "modern"
        self._styles_injected = False
    
    def inject_modern_styles(self):
        """Inject modern CSS styling."""
        if self._styles_injected:
            return
            
        modern_css = """
        <style>
        /* Modern Color Palette */
        :root {
            --primary-color: #2563eb;
            --secondary-color: #64748b;
            --success-color: #059669;
            --warning-color: #d97706;
            --background-color: #f8fafc;
            --card-background: #ffffff;
            --border-color: #e2e8f0;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
        }
        
        /* Main Container */
        .main .block-container {
            background: var(--background-color);
            padding: 2rem 1rem;
            max-width: 1200px;
        }
        
        /* Sidebar Styling */
        .css-1d391kg {
            background: var(--card-background);
            border-right: 1px solid var(--border-color);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        /* Cards */
        .element-container {
            background: var(--card-background);
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            border: 1px solid var(--border-color);
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        /* Buttons */
        .stButton > button {
            background: var(--primary-color);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        }
        
        .stButton > button:hover {
            background: #1d4ed8;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(37, 99, 235, 0.3);
        }
        
        /* Text Areas */
        .stTextArea > div > div > textarea {
            border: 2px solid var(--border-color);
            border-radius: 8px;
            font-family: 'Inter', sans-serif;
            transition: border-color 0.2s ease;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
        }
        
        /* Select Boxes */
        .stSelectbox > div > div {
            border: 2px solid var(--border-color);
            border-radius: 8px;
            transition: border-color 0.2s ease;
        }
        
        /* Success/Warning/Error Messages */
        .stSuccess {
            background: rgba(5, 150, 105, 0.1);
            border: 1px solid var(--success-color);
            border-radius: 8px;
            color: #065f46;
        }
        
        .stWarning {
            background: rgba(217, 119, 6, 0.1);
            border: 1px solid var(--warning-color);
            border-radius: 8px;
            color: #92400e;
        }
        
        .stError {
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid #ef4444;
            border-radius: 8px;
            color: #dc2626;
        }
        
        /* Metrics */
        .metric-container {
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            transition: transform 0.2s ease;
        }
        
        .metric-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        /* Typography */
        h1, h2, h3 {
            color: var(--text-primary);
            font-weight: 700;
        }
        
        p, span, div {
            color: var(--text-secondary);
            line-height: 1.6;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.3s ease-out;
        }
        </style>
        """
        
        st.markdown(modern_css, unsafe_allow_html=True)
        self._styles_injected = True
    
    def create_metric_card(self, title: str, value: str, delta: str = None):
        """Create a styled metric card."""
        delta_html = f"<p style='color: var(--success-color); margin: 0;'>{delta}</p>" if delta else ""
        
        card_html = f"""
        <div class="metric-container fade-in">
            <h3 style="margin: 0 0 0.5rem 0; color: var(--text-primary);">{value}</h3>
            <p style="margin: 0; color: var(--text-secondary); font-weight: 500;">{title}</p>
            {delta_html}
        </div>
        """
        
        st.markdown(card_html, unsafe_allow_html=True)
    
    def create_status_indicator(self, status: str, message: str):
        """Create a status indicator with appropriate styling."""
        status_colors = {
            "success": "var(--success-color)",
            "warning": "var(--warning-color)", 
            "error": "#ef4444",
            "info": "var(--primary-color)"
        }
        
        color = status_colors.get(status, "var(--text-secondary)")
        
        indicator_html = f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.75rem 1rem;
            border-radius: 8px;
            border-left: 4px solid {color};
            background: rgba(37, 99, 235, 0.05);
            margin: 0.5rem 0;
        ">
            <div style="
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: {color};
                margin-right: 0.75rem;
            "></div>
            <span style="color: var(--text-primary); font-weight: 500;">{message}</span>
        </div>
        """
        
        st.markdown(indicator_html, unsafe_allow_html=True)
