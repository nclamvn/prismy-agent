"""Main application entry point with persistent cache."""

import streamlit as st
import os
from typing import Optional

from src.application.services.translation_service import TranslationService
from src.core.entities.translation import TranslationRequest
from presentation.streamlit_app.components.theme_manager import ThemeManager


class TranslationApp:
    """Main application class with persistent cache."""
    
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.setup_page_config()
        self.apply_theme()
    
    def setup_page_config(self):
        """Configure Streamlit page."""
        st.set_page_config(
            page_title="🚀 Translation Agent v2.0",
            page_icon="🚀",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def apply_theme(self):
        """Apply modern theme styling."""
        self.theme_manager.inject_modern_styles()
    
    def get_translation_service(self) -> TranslationService:
        """Get or create persistent translation service."""
        # Use session state to persist service
        if 'translation_service' not in st.session_state:
            api_key = st.session_state.get('openai_api_key', '')
            st.session_state.translation_service = TranslationService(
                api_key if api_key else None, 
                enable_cache=True
            )
        
        # Update API key if changed
        current_key = st.session_state.get('openai_api_key', '')
        if current_key != st.session_state.translation_service.openai_api_key:
            st.session_state.translation_service.update_api_key(current_key)
        
        return st.session_state.translation_service
    
    def render_header(self):
        """Render application header with modern styling."""
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0; margin-bottom: 2rem;">
            <h1 style="color: var(--text-primary); margin-bottom: 0.5rem;">
                🚀 Translation Agent v2.0
            </h1>
            <p style="color: var(--text-secondary); font-size: 1.1rem; margin: 0;">
                Clean Architecture • Modern UI • High Performance Cache
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render application sidebar with modern styling."""
        with st.sidebar:
            st.markdown("### 🔑 API Configuration")
            
            # API Key input with modern styling
            api_key = st.text_input(
                "OpenAI API Key",
                type="password",
                value=st.session_state.get('openai_api_key', ''),
                help="Enter your OpenAI API key for translation services"
            )
            
            if api_key:
                st.session_state['openai_api_key'] = api_key
            
            # Language selection with modern styling
            st.markdown("### 🌍 Language Settings")
            target_lang = st.selectbox(
                "Target Language",
                ["vi", "en", "zh", "ja", "fr", "de", "es", "ko"],
                format_func=lambda x: {
                    "vi": "🇻🇳 Vietnamese", "en": "🇺🇸 English", "zh": "🇨🇳 Chinese",
                    "ja": "🇯🇵 Japanese", "fr": "🇫🇷 French", "de": "🇩🇪 German", 
                    "es": "🇪🇸 Spanish", "ko": "🇰🇷 Korean"
                }[x]
            )
            
            st.session_state['target_lang'] = target_lang
            
            # Status with theme manager
            service = self.get_translation_service()
            if service.is_configured():
                self.theme_manager.create_status_indicator("success", "Ready to translate")
            else:
                self.theme_manager.create_status_indicator("warning", "Please add API key")
            
            # Cache control
            st.markdown("### ⚡ Cache Control")
            if st.button("🗑️ Clear Cache", help="Clear translation cache"):
                if 'translation_service' in st.session_state:
                    import asyncio
                    asyncio.run(st.session_state.translation_service.clear_cache())
                    st.success("Cache cleared!")
                    st.rerun()
            
            # Advanced Settings
            with st.expander("⚙️ Advanced Settings"):
                preserve_formatting = st.checkbox("Preserve Formatting", value=True)
                quality_tier = st.selectbox("Quality Tier", ["standard", "high", "premium"])
                
                st.session_state['preserve_formatting'] = preserve_formatting
                st.session_state['quality_tier'] = quality_tier
    
    def render_main_content(self):
        """Render main translation interface with modern theme."""
        self.render_header()
        
        # Translation interface with modern layout
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("### 📝 Input Text")
            input_text = st.text_area(
                "Enter text to translate:",
                height=400,
                placeholder="Enter your text here for professional translation...",
                key="input_text",
                help="Supports text up to 50,000 characters with automatic chunking"
            )
            
            # Input statistics
            if input_text:
                word_count = len(input_text.split())
                char_count = len(input_text)
                
                stats_col1, stats_col2, stats_col3 = st.columns(3)
                with stats_col1:
                    self.theme_manager.create_metric_card("Words", f"{word_count:,}")
                with stats_col2:
                    self.theme_manager.create_metric_card("Characters", f"{char_count:,}")
                with stats_col3:
                    chunking_needed = "Yes" if char_count > 3000 else "No"
                    self.theme_manager.create_metric_card("Chunking", chunking_needed)
        
        with col2:
            st.markdown("### 🌐 Translation Result")
            translation_container = st.empty()
            metrics_container = st.empty()
        
        # Translation button with modern styling
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            translate_button = st.button(
                "🚀 Translate Now",
                type="primary",
                use_container_width=True,
                help="Click to start professional translation"
            )
        
        # Translation logic
        if translate_button:
            if not input_text.strip():
                st.error("Please enter some text to translate")
                return
            
            service = self.get_translation_service()
            if not service.is_configured():
                st.error("Please configure your API key in the sidebar")
                return
            
            target_lang = st.session_state.get('target_lang', 'vi')
            preserve_formatting = st.session_state.get('preserve_formatting', True)
            
            with st.spinner("🔄 Translating with AI..."):
                try:
                    result = service.translate_text_sync(
                        text=input_text,
                        target_language=target_lang,
                        preserve_formatting=preserve_formatting
                    )
                    
                    with translation_container.container():
                        if result.success:
                            st.text_area(
                                "Translation Result:",
                                value=result.translated_text,
                                height=400,
                                disabled=True,
                                help="Professional AI translation result"
                            )
                            
                            # Show cache info if available
                            if result.metadata and result.metadata.get('from_cache'):
                                st.success("⚡ Retrieved from cache (instant!)")
                            elif result.metadata and result.metadata.get('cached'):
                                st.info("💾 Result cached for future use")
                            
                            # Show metrics with theme manager
                            with metrics_container.container():
                                metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
                                
                                with metrics_col1:
                                    confidence_pct = f"{result.confidence:.1%}"
                                    self.theme_manager.create_metric_card("Confidence", confidence_pct)
                                
                                with metrics_col2:
                                    time_str = f"{result.processing_time:.1f}s"
                                    self.theme_manager.create_metric_card("Time", time_str)
                                
                                with metrics_col3:
                                    tokens_str = f"{result.tokens_used:,}"
                                    self.theme_manager.create_metric_card("Tokens", tokens_str)
                                
                                with metrics_col4:
                                    chunks_str = f"{result.chunks_processed}"
                                    self.theme_manager.create_metric_card("Chunks", chunks_str)
                            
                            # Success indicator
                            cache_info = " (from cache)" if result.metadata and result.metadata.get('from_cache') else ""
                            self.theme_manager.create_status_indicator(
                                "success", 
                                f"Translation completed successfully using {result.model_used}{cache_info}"
                            )
                            

                        else:
                            st.error(f"Translation failed: {result.translated_text}")
                            self.theme_manager.create_status_indicator(
                                "error",
                                "Translation failed - please check your input and try again"
                            )
                
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
                    self.theme_manager.create_status_indicator(
                        "error",
                        f"System error: {str(e)}"
                    )
    
    def render_performance_section(self):
        """Render performance and cache statistics."""
        service = self.get_translation_service()
        service_info = service.get_service_info()
        
        if service_info['cache_enabled']:
            st.markdown("### 📊 Performance Statistics")
            
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
            
            with perf_col1:
                hit_rate = service_info['performance']['cache_hit_rate']
                self.theme_manager.create_metric_card("Cache Hit Rate", f"{hit_rate:.1f}%")
            
            with perf_col2:
                total_requests = service_info['performance']['total_requests']
                self.theme_manager.create_metric_card("Total Requests", f"{total_requests}")
            
            with perf_col3:
                memory_usage = service_info['performance']['memory_usage_mb']
                self.theme_manager.create_metric_card("Cache Memory", f"{memory_usage:.1f}MB")
            
            with perf_col4:
                cache_status = "Active" if service_info['cache_enabled'] else "Disabled"
                self.theme_manager.create_metric_card("Cache Status", cache_status)
    
    def run(self):
        """Run the application with modern theme."""
        self.render_sidebar()
        self.render_main_content()
        
        # Performance stats
        service = self.get_translation_service()
        if service.enable_cache:
            self.render_performance_section()


def main():
    """Main entry point with modern theme."""
    app = TranslationApp()
    app.run()


if __name__ == "__main__":
    main()
