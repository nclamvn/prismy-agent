# sdip_integration.py
"""
SDIP Integration Wrapper
Connects SDIP system with existing Streamlit app
"""

import asyncio
import streamlit as st
from engines.semantic_chunking import SemanticChunkingEngine
from translators.professional_translator import ProfessionalTranslator
from core.base_classes import DocumentType

class SDIPSystem:
    """Main SDIP system interface"""
    
    def __init__(self):
        self.chunking_engine = None
        self.professional_translator = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize SDIP components"""
        try:
            self.chunking_engine = SemanticChunkingEngine()
            self.professional_translator = ProfessionalTranslator()
            st.success("🚀 SDIP System initialized successfully!")
        except Exception as e:
            st.error(f"❌ SDIP initialization error: {e}")
    
    async def translate_document_async(self, content: str, target_language: str, 
                                     source_language: str = "auto") -> dict:
        """
        Translate document using SDIP system
        
        Returns:
            dict: Translation result with metadata
        """
        try:
            # Step 1: Semantic Chunking
            with st.spinner("🔍 Performing semantic chunking..."):
                chunks = self.chunking_engine.chunk_document(
                    content, 
                    DocumentType.TXT  # Default to TXT for now
                )
            
            st.info(f"📊 Created {len(chunks)} semantic chunks")
            
            # Step 2: Professional Translation
            with st.spinner("🏆 Performing professional translation..."):
                translation_result = await self.professional_translator.translate_document(
                    chunks,
                    target_language=target_language,
                    source_language=source_language
                )
            
            return {
                "success": True,
                "translated_text": translation_result.translated_text,
                "quality_score": translation_result.quality_score,
                "processing_time": translation_result.processing_time,
                "chunk_count": len(chunks),
                "translation_tier": "Professional",
                "metadata": translation_result.metadata
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "translated_text": "Translation failed",
                "quality_score": 0,
                "processing_time": 0
            }
    
    async def smart_translate_document(self, content: str, target_language: str, 
                                     source_language: str = "auto") -> dict:
        """
        Smart translate method - wrapper for translate_document_async
        Compatible with app_analytics_dashboard.py
        """
        return await self.translate_document_async(content, target_language, source_language)
    
    def translate_document(self, content: str, target_language: str, 
                          source_language: str = "auto") -> dict:
        """
        Synchronous wrapper for async translation
        """
        return asyncio.run(self.translate_document_async(
            content, target_language, source_language
        ))

# Global SDIP instance
@st.cache_resource
def get_sdip_system():
    """Get cached SDIP system instance"""
    return SDIPSystem()
