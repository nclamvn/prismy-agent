# sdip_advanced_integration.py
"""
SDIP Advanced Integration
Enhanced system with advanced document processing capabilities
"""

import asyncio
import streamlit as st
from typing import List, Dict, Any, Optional

# Import enhanced components
from engines.semantic_chunking_enhanced import EnhancedSemanticChunkingEngine
from translators.professional_translator import ProfessionalTranslator
from processors.advanced_document_processor import AdvancedDocumentProcessor
from core.base_classes import DocumentType

# Import smart features
from smart_features.document_analyzer import IntelligentDocumentAnalyzer
from smart_features.smart_retry import SmartRetrySystem
from smart_features.batch_processor import SmartBatchProcessor, BatchDocument, Priority

class SDIPAdvancedSystem:
    """
    Advanced SDIP system with enhanced document processing:
    - PDF table extraction
    - DOCX complex structures
    - Excel formula processing
    - Mathematical expression handling
    """
    
    def __init__(self):
        # Enhanced core components
        self.chunking_engine = EnhancedSemanticChunkingEngine()
        self.professional_translator = ProfessionalTranslator()
        self.advanced_processor = AdvancedDocumentProcessor()
        
        # Smart features
        self.document_analyzer = IntelligentDocumentAnalyzer()
        self.smart_retry = SmartRetrySystem()
        self.batch_processor = SmartBatchProcessor()
        
        st.success("🚀 SDIP Advanced System with Document Processing initialized!")
    
    async def smart_translate_document(self, content: str, target_language: str, 
                                     source_language: str = "auto") -> Dict[str, Any]:
        """
        Smart translation with enhanced document processing
        """
        try:
            # Step 1: Smart Document Analysis
            with st.spinner("🧠 Performing intelligent document analysis..."):
                analysis = self.document_analyzer.analyze_document(content)
            
            # Display analysis insights
            self._display_analysis_insights(analysis)
            
            # Step 2: Enhanced Semantic Chunking
            with st.spinner("🔍 Enhanced semantic chunking with advanced features..."):
                chunks = self.chunking_engine.chunk_document(content, DocumentType.TXT)
            
            st.info(f"📊 Created {len(chunks)} enhanced semantic chunks")
            
            # Display advanced chunk info
            self._display_chunk_insights(chunks)
            
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
                'advanced_features': self._get_advanced_features_summary(chunks),
                'retry_info': {
                    'retry_count': retry_result.retry_count,
                    'retry_reasons': [r.value for r in retry_result.retry_reasons],
                    'improvements': retry_result.improvement_notes,
                    'model_used': retry_result.model_used.value
                },
                'smart_features_used': [
                    'Enhanced Document Processing',
                    'Advanced Table Detection',
                    'Formula Preservation',
                    'Intelligent Document Analysis',
                    'Enhanced Semantic Chunking', 
                    'Smart Retry System',
                    'Quality Optimization'
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'translated_text': 'Advanced translation failed',
                'quality_score': 0,
                'processing_time': 0
            }
    
    async def smart_translate_file(self, file_content: bytes, filename: str, 
                                 target_language: str, source_language: str = "auto") -> Dict[str, Any]:
        """
        NEW: Smart translation directly from file with advanced processing
        """
        try:
            # Step 1: Advanced Document Processing
            with st.spinner(f"📄 Processing {filename} with advanced features..."):
                processing_result = self.advanced_processor.process_document(file_content, filename)
            
            if not processing_result.success:
                st.error(f"❌ Advanced processing failed: {processing_result.error}")
                return {
                    'success': False,
                    'error': f"Document processing failed: {processing_result.error}",
                    'translated_text': '',
                    'quality_score': 0,
                    'processing_time': 0
                }
            
            # Display processing results
            self._display_processing_results(processing_result)
            
            # Step 2: Enhanced Chunking from processed content
            with st.spinner("🔍 Enhanced chunking from processed document..."):
                chunks = self.chunking_engine.chunk_document_from_file(file_content, filename)
            
            st.info(f"📊 Created {len(chunks)} enhanced chunks from file")
            
            # Step 3: Translation
            with st.spinner("🎯 Translating advanced document..."):
                initial_result = await self.professional_translator.translate_document(
                    chunks, target_language, source_language
                )
                
                # Apply smart retry
                initial_result_dict = {
                    'success': True,
                    'translated_text': initial_result.translated_text,
                    'quality_score': initial_result.quality_score,
                    'processing_time': initial_result.processing_time,
                    'original_text': processing_result.content
                }
                
                retry_result = await self.smart_retry.smart_translate_with_retry(
                    processing_result.content, target_language, initial_result_dict
                )
            
            return {
                'success': True,
                'translated_text': retry_result.final_translation,
                'quality_score': retry_result.quality_score,
                'processing_time': retry_result.processing_time,
                'chunk_count': len(chunks),
                'file_processing': {
                    'tables_found': len(processing_result.tables),
                    'images_found': len(processing_result.images),
                    'formulas_found': len(processing_result.formulas),
                    'format': getattr(processing_result.metadata, 'format', 'Unknown')
                },
                'advanced_features': self._get_advanced_features_summary(chunks),
                'smart_features_used': [
                    'Advanced File Processing',
                    'PDF Table Extraction',
                    'DOCX Structure Analysis',
                    'Excel Formula Processing',
                    'Enhanced Semantic Chunking',
                    'Smart Retry System'
                ]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),  
                'translated_text': 'File processing failed',
                'quality_score': 0,
                'processing_time': 0
            }
    
    def _display_analysis_insights(self, analysis):
        """Display smart analysis insights"""
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
    
    def _display_chunk_insights(self, chunks):
        """Display enhanced chunk insights"""
        table_chunks = sum(1 for c in chunks if c.metadata.get('has_tables'))
        formula_chunks = sum(1 for c in chunks if c.metadata.get('has_formulas'))
        
        if table_chunks > 0 or formula_chunks > 0:
            with st.expander("📊 Advanced Content Detection", expanded=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Table Chunks", table_chunks)
                with col2:
                    st.metric("Formula Chunks", formula_chunks)
                with col3:
                    avg_confidence = sum(c.confidence_score for c in chunks) / len(chunks)
                    st.metric("Avg Confidence", f"{avg_confidence:.2f}")
    
    def _display_processing_results(self, result):
        """Display advanced processing results"""
        with st.expander("📄 Advanced Document Processing Results", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Tables Found", len(result.tables))
            with col2:
                st.metric("Images Found", len(result.images))
            with col3:
                st.metric("Formulas Found", len(result.formulas))
            with col4:
                st.metric("Format", getattr(result.metadata, 'format', 'Unknown'))
            
            if result.formulas:
                st.write("**🧮 Detected Formulas:**")
                for formula in result.formulas[:5]:  # Show first 5
                    st.code(formula)
    
    def _get_advanced_features_summary(self, chunks):
        """Get summary of advanced features used"""
        return {
            'total_chunks': len(chunks),
            'table_chunks': sum(1 for c in chunks if c.metadata.get('has_tables')),
            'formula_chunks': sum(1 for c in chunks if c.metadata.get('has_formulas')),
            'advanced_contexts': list(set(c.semantic_context for c in chunks)),
            'average_confidence': sum(c.confidence_score for c in chunks) / len(chunks) if chunks else 0
        }

# Global advanced SDIP instance
@st.cache_resource
def get_advanced_sdip_system():
    """Get cached advanced SDIP system instance"""
    return SDIPAdvancedSystem()
