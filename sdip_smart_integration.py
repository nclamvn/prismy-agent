# sdip_smart_integration.py
"""
SDIP Smart Integration
Enhanced system with intelligent document analysis, retry, and batch processing
"""

import asyncio
import streamlit as st
from typing import List, Dict, Any

# Import SDIP core components
from engines.semantic_chunking import SemanticChunkingEngine
from translators.professional_translator import ProfessionalTranslator
from core.base_classes import DocumentType

# Import smart features
from smart_features.document_analyzer import IntelligentDocumentAnalyzer
from smart_features.smart_retry import SmartRetrySystem
from smart_features.batch_processor import SmartBatchProcessor, BatchDocument, Priority

class SDIPSmartSystem:
    """Enhanced SDIP system with intelligent features"""
    
    def __init__(self):
        # Core components
        self.chunking_engine = SemanticChunkingEngine()
        self.professional_translator = ProfessionalTranslator()
        
        # Smart features
        self.document_analyzer = IntelligentDocumentAnalyzer()
        self.smart_retry = SmartRetrySystem()
        self.batch_processor = SmartBatchProcessor()
        
        st.success("🧠 SDIP Smart System initialized with AI intelligence!")
    
    async def smart_translate_document(self, content: str, target_language: str, 
                                     source_language: str = "auto") -> Dict[str, Any]:
        """
        Intelligent document translation with smart analysis and optimization
        """
        try:
            # Step 1: Smart Document Analysis
            with st.spinner("🧠 Performing intelligent document analysis..."):
                analysis = self.document_analyzer.analyze_document(content)
            
            # Display analysis insights
            self._display_analysis_insights(analysis)
            
            # Step 2: Optimized Semantic Chunking
            with st.spinner("🔍 Optimized semantic chunking..."):
                # Use recommended chunk size from analysis
                original_chunk_size = self.chunking_engine.config.max_chunk_size
                self.chunking_engine.config.max_chunk_size = analysis.recommended_chunk_size
                
                chunks = self.chunking_engine.chunk_document(content, DocumentType.TXT)
                
                # Restore original setting
                self.chunking_engine.config.max_chunk_size = original_chunk_size
            
            st.info(f"📊 Created {len(chunks)} optimized semantic chunks")
            
            # Step 3: Professional Translation with Smart Retry
            with st.spinner("🎯 Professional translation with smart retry..."):
                initial_result = await self.professional_translator.translate_document(
                    chunks, target_language, source_language
                )
                
                # Convert to format expected by smart retry
                initial_result_dict = {
                    'success': True,
                    'translated_text': initial_result.translated_text,
                    'quality_score': initial_result.quality_score,
                    'processing_time': initial_result.processing_time,
                    'original_text': content
                }
                
                # Apply smart retry if needed
                retry_result = await self.smart_retry.smart_translate_with_retry(
                    content, target_language, initial_result_dict
                )
            
            return {
                'success': True,
                'translated_text': retry_result.final_translation,
                'quality_score': retry_result.quality_score,
                'processing_time': retry_result.processing_time,
                'chunk_count': len(chunks),
                'analysis': analysis,
                'retry_info': {
                    'retry_count': retry_result.retry_count,
                    'retry_reasons': [r.value for r in retry_result.retry_reasons],
                    'improvements': retry_result.improvement_notes,
                    'model_used': retry_result.model_used.value
                },
                'smart_features_used': [
                    'Intelligent Document Analysis',
                    'Optimized Semantic Chunking', 
                    'Smart Retry System',
                    'Quality Optimization'
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'translated_text': 'Smart translation failed',
                'quality_score': 0,
                'processing_time': 0
            }
    
    def _display_analysis_insights(self, analysis):
        """Display smart analysis insights in Streamlit"""
        with st.expander("🧠 Smart Document Analysis", expanded=True):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Complexity", analysis.complexity.value.title())
                st.metric("Content Type", analysis.content_type.value.title())
            
            with col2:
                st.metric("Estimated Time", f"{analysis.estimated_time:.1f}s")
                st.metric("Confidence Prediction", f"{analysis.confidence_prediction:.2f}")
            
            with col3:
                st.metric("Optimal Chunk Size", f"{analysis.recommended_chunk_size}")
                st.metric("Key Features", len(analysis.key_features))
            
            # Key features
            if analysis.key_features:
                st.write("**🔍 Detected Features:**")
                for feature in analysis.key_features:
                    st.write(f"• {feature}")
            
            # Optimization suggestions
            if analysis.optimization_suggestions:
                st.write("**💡 Smart Recommendations:**")
                for suggestion in analysis.optimization_suggestions:
                    st.write(f"• {suggestion}")
    
    async def smart_batch_translate(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Smart batch processing for multiple documents
        """
        try:
            # Convert to BatchDocument objects
            batch_documents = []
            for i, doc in enumerate(documents):
                batch_doc = BatchDocument(
                    id=f"doc_{i+1}",
                    content=doc['content'],
                    target_language=doc['target_language'],
                    source_language=doc.get('source_language', 'auto'),
                    priority=Priority.NORMAL
                )
                batch_documents.append(batch_doc)
            
            # Process batch
            with st.spinner(f"📦 Smart batch processing {len(batch_documents)} documents..."):
                batch_result = await self.batch_processor.process_batch(batch_documents)
            
            return {
                'success': True,
                'batch_result': batch_result,
                'insights': batch_result.optimization_insights
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

# Global smart SDIP instance
@st.cache_resource
def get_smart_sdip_system():
    """Get cached smart SDIP system instance"""
    return SDIPSmartSystem()
