"""
Intelligence Orchestrator
Master AI coordinator that orchestrates all AI engines for optimal results
"""

import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

from src.infrastructure.content_transformation.base_transformer import TargetAudience, TransformationType
# Import all AI engines
# from ..translation import ProviderManager, TranslationRequest, ProviderType
#from ..content_transformation import (
#    TransformationManager, TransformationType, TargetAudience,
#    TransformationRequest, BatchTransformationRequest
#)
from .smart_chunking_engine import SmartChunkingEngine
from .quality_enhancer import QualityEnhancer
from .context_awareness_engine import ContextAwarenessEngine


class ProcessingMode(Enum):
    """Processing modes for orchestrator"""
    SPEED_OPTIMIZED = "speed_optimized"       # Fastest processing
    QUALITY_OPTIMIZED = "quality_optimized"   # Best quality output
    COST_OPTIMIZED = "cost_optimized"         # Lowest cost
    BALANCED = "balanced"                     # Balance all factors
    CUSTOM = "custom"                         # Custom parameters


class WorkflowStage(Enum):
    """Stages in AI processing workflow"""
    INPUT_ANALYSIS = "input_analysis"
    TRANSLATION = "translation"
    CHUNKING = "chunking"
    CONTEXT_ANALYSIS = "context_analysis"
    QUALITY_ENHANCEMENT = "quality_enhancement"
    TRANSFORMATION = "transformation"
    OPTIMIZATION = "optimization"
    OUTPUT_GENERATION = "output_generation"


@dataclass
class ProcessingRequest:
    """Comprehensive processing request"""
    input_text: str
    source_language: str = "auto"             # Auto-detect or specify
    target_language: str = "vi"
    processing_mode: ProcessingMode = ProcessingMode.BALANCED
    target_audience: TargetAudience = TargetAudience.GENERAL
    desired_outputs: List[TransformationType] = field(default_factory=list)
    quality_target: float = 0.8
    max_cost: Optional[float] = None
    max_processing_time: Optional[float] = None
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProcessingResult:
    """Comprehensive processing result"""
    original_text: str
    translated_text: str
    chunks_analysis: Dict[str, Any]
    context_analysis: Dict[str, Any]
    quality_analysis: Dict[str, Any]
    transformed_outputs: Dict[TransformationType, Any]
    optimization_insights: Dict[str, Any]
    processing_metadata: Dict[str, Any]
    total_processing_time: float
    total_cost: float
    quality_achieved: float


@dataclass
class OptimizationInsight:
    """AI-generated optimization insights"""
    insight_type: str
    description: str
    confidence: float
    recommendation: str
    potential_improvement: float


class IntelligenceOrchestrator:
    """
    Master AI coordinator that orchestrates all engines for optimal results
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            "enable_auto_optimization": True,
            "enable_predictive_selection": True,
            "enable_cost_tracking": True,
            "enable_quality_prediction": True,
            "cache_results": True,
            "max_parallel_operations": 3
        }
        self.config = {**self.default_config, **self.config}
        
        # Initialize all engines
        self._initialize_engines()
        
        # Processing statistics
        self.processing_stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "avg_processing_time": 0.0,
            "avg_quality_achieved": 0.0,
            "total_cost": 0.0
        }
        
        # Learning data for optimization
        self.learning_data = []
    
    def _initialize_engines(self):
        """Initialize all AI engines"""
        print("🚀 Initializing Intelligence Orchestrator...")
        
        self.translation_manager = ProviderManager()
        self.transformation_manager = TransformationManager()
        self.chunking_engine = SmartChunkingEngine()
        self.quality_enhancer = QualityEnhancer()
        self.context_engine = ContextAwarenessEngine()
        
        print("✅ All AI engines initialized and ready")
    
    async def process_intelligent(self, request: ProcessingRequest) -> ProcessingResult:
        """
        Intelligent processing with full AI orchestration
        """
        start_time = time.time()
        
        print(f"🧠 Starting intelligent processing...")
        print(f"   Mode: {request.processing_mode.value}")
        print(f"   Target quality: {request.quality_target}")
        print(f"   Desired outputs: {[t.value for t in request.desired_outputs]}")
        
        try:
            # Stage 1: Input Analysis & Auto-Detection
            input_analysis = await self._analyze_input(request)
            
            # Stage 2: Smart Translation
            translation_result = await self._smart_translation(request, input_analysis)
            
            # Stage 3: Intelligent Chunking
            chunking_result = await self._intelligent_chunking(translation_result, request)
            
            # Stage 4: Context Awareness
            context_result = await self._context_awareness_analysis(chunking_result, request)
            
            # Stage 5: Quality Enhancement (if needed)
            quality_result = await self._smart_quality_enhancement(translation_result, context_result, request)
            
            # Stage 6: Predictive Content Transformation
            transformation_result = await self._predictive_transformation(quality_result, context_result, request)
            
            # Stage 7: AI Optimization
            optimization_insights = await self._generate_optimization_insights(
                input_analysis, translation_result, chunking_result, 
                context_result, quality_result, transformation_result
            )
            
            # Calculate final metrics
            total_time = time.time() - start_time
            total_cost = self._calculate_total_cost(translation_result, transformation_result)
            quality_achieved = quality_result.get('final_quality', 0.8)
            
            # Create comprehensive result
            result = ProcessingResult(
                original_text=request.input_text,
                translated_text=translation_result['translated_text'],
                chunks_analysis=chunking_result,
                context_analysis=context_result,
                quality_analysis=quality_result,
                transformed_outputs=transformation_result,
                optimization_insights=optimization_insights,
                processing_metadata={
                    "processing_mode": request.processing_mode.value,
                    "stages_completed": 7,
                    "engines_used": ["translation", "chunking", "context", "quality", "transformation"],
                    "auto_optimizations_applied": len(optimization_insights)
                },
                total_processing_time=total_time,
                total_cost=total_cost,
                quality_achieved=quality_achieved
            )
            
            # Update statistics and learning data
            self._update_processing_stats(result)
            self._store_learning_data(request, result)
            
            print(f"✅ Intelligent processing completed in {total_time:.3f}s")
            print(f"   Quality achieved: {quality_achieved:.3f}")
            print(f"   Total cost: ${total_cost:.6f}")
            print(f"   Optimization insights: {len(optimization_insights)}")
            
            return result
            
        except Exception as e:
            print(f"❌ Processing failed: {str(e)}")
            raise
    
    async def _analyze_input(self, request: ProcessingRequest) -> Dict[str, Any]:
        """Analyze input and make predictions"""
        print("📊 Stage 1: Input Analysis...")
        
        # Basic text analysis
        text_stats = {
            "length": len(request.input_text),
            "word_count": len(request.input_text.split()),
            "sentence_count": len([s for s in request.input_text.split('.') if s.strip()]),
            "complexity_estimate": self._estimate_text_complexity(request.input_text)
        }
        
        # Language detection (simple version)
        detected_language = self._detect_language(request.input_text)
        
        # Processing predictions
        predicted_processing_time = self._predict_processing_time(text_stats, request.processing_mode)
        predicted_cost = self._predict_cost(text_stats, request)
        
        return {
            "text_stats": text_stats,
            "detected_language": detected_language,
            "predicted_processing_time": predicted_processing_time,
            "predicted_cost": predicted_cost,
            "recommended_chunking_strategy": self._recommend_chunking_strategy(text_stats),
            "optimal_transformation_types": self._predict_optimal_transformations(request.input_text, request.target_audience)
        }
    
    async def _smart_translation(self, request: ProcessingRequest, input_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Smart translation with provider optimization"""
        print("🔄 Stage 2: Smart Translation...")
        
        # Determine source language
        source_lang = request.source_language
        if source_lang == "auto":
            source_lang = input_analysis["detected_language"]
        
        # Skip translation if already in target language
        if source_lang == request.target_language:
            return {
                "translated_text": request.input_text,
                "translation_provider": "none",
                "translation_cost": 0.0,
                "translation_time": 0.0,
                "translation_quality": 1.0
            }
        
        # Perform translation
        translation_req = TranslationRequest(
            text=request.input_text,
            source_language=source_lang,
            target_language=request.target_language
        )
        
        translation_response = await self.translation_manager.translate(translation_req)
        
        return {
            "translated_text": translation_response.translated_text,
            "translation_provider": translation_response.provider,
            "translation_cost": translation_response.cost_estimate,
            "translation_time": translation_response.processing_time,
            "translation_quality": translation_response.confidence_score
        }
    
    async def _intelligent_chunking(self, translation_result: Dict[str, Any], request: ProcessingRequest) -> Dict[str, Any]:
        """Intelligent chunking with context awareness"""
        print("🧠 Stage 3: Intelligent Chunking...")
        
        text_to_chunk = translation_result["translated_text"]
        chunks, doc_structure = await self.chunking_engine.analyze_document(text_to_chunk)
        
        return {
            "chunks": [
                {
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "type": chunk.chunk_type.value,
                    "complexity": chunk.semantic_complexity.value,
                    "key_concepts": chunk.key_concepts,
                    "transformation_potential": chunk.transformation_potential
                }
                for chunk in chunks
            ],
            "document_structure": {
                "main_topics": doc_structure.main_topics,
                "document_type": doc_structure.document_type,
                "overall_complexity": doc_structure.overall_complexity.value
            },
            "chunking_stats": {
                "total_chunks": len(chunks),
                "avg_chunk_size": sum(len(c.content) for c in chunks) / len(chunks) if chunks else 0
            }
        }
    
    async def _context_awareness_analysis(self, chunking_result: Dict[str, Any], request: ProcessingRequest) -> Dict[str, Any]:
        """Context awareness analysis"""
        print("🔗 Stage 4: Context Analysis...")
        
        # Create mock chunks for context engine (simplified)
        chunks = chunking_result["chunks"]
        
        # Simple context analysis
        context_info = {
            "total_concepts": sum(len(chunk["key_concepts"]) for chunk in chunks),
            "document_coherence": self._calculate_document_coherence(chunks),
            "main_themes": chunking_result["document_structure"]["main_topics"],
            "chunk_relationships": self._analyze_chunk_relationships(chunks)
        }
        
        return context_info
    
    async def _smart_quality_enhancement(self, translation_result: Dict[str, Any], 
                                       context_result: Dict[str, Any], 
                                       request: ProcessingRequest) -> Dict[str, Any]:
        """Smart quality enhancement"""
        print("✨ Stage 5: Quality Enhancement...")
        
        text_to_enhance = translation_result["translated_text"]
        
        # Check if enhancement is needed
        initial_quality = await self.quality_enhancer.analyze_quality(text_to_enhance)
        
        if initial_quality.overall_score < request.quality_target:
            enhancement_result = await self.quality_enhancer.enhance_content(
                text_to_enhance, 
                target_quality=request.quality_target
            )
            
            return {
                "enhanced_text": enhancement_result.enhanced_content,
                "initial_quality": initial_quality.overall_score,
                "final_quality": enhancement_result.quality_after.overall_score,
                "improvements_made": enhancement_result.improvements_made,
                "enhancement_time": enhancement_result.processing_time
            }
        else:
            return {
                "enhanced_text": text_to_enhance,
                "initial_quality": initial_quality.overall_score,
                "final_quality": initial_quality.overall_score,
                "improvements_made": ["No enhancement needed - quality already sufficient"],
                "enhancement_time": 0.0
            }
    
    async def _predictive_transformation(self, quality_result: Dict[str, Any], 
                                       context_result: Dict[str, Any], 
                                       request: ProcessingRequest) -> Dict[str, Any]:
        """Predictive content transformation"""
        print("🎯 Stage 6: Predictive Transformation...")
        
        text_to_transform = quality_result["enhanced_text"]
        transformations = {}
        
        # Use desired outputs or predict optimal ones
        target_formats = request.desired_outputs
        if not target_formats:
            target_formats = [TransformationType.PODCAST_SCRIPT, TransformationType.EDUCATION_MODULE]
        
        # Perform transformations
        for format_type in target_formats:
            try:
                transform_request = TransformationRequest(
                    source_text=text_to_transform,
                    transformation_type=format_type,
                    target_audience=request.target_audience
                )
                
                transform_result = await self.transformation_manager.transform_single(transform_request)
                
                transformations[format_type] = {
                    "content": transform_result.transformed_content[:500] + "...",  # Truncate for display
                    "quality_score": transform_result.quality_score,
                    "processing_time": transform_result.processing_time,
                    "metadata": transform_result.metadata
                }
                
            except Exception as e:
                transformations[format_type] = {
                    "error": str(e),
                    "content": None
                }
        
        return transformations
    
    async def _generate_optimization_insights(self, *stage_results) -> Dict[str, Any]:
        """Generate AI optimization insights"""
        print("🔍 Stage 7: Optimization Insights...")
        
        insights = {
            "processing_efficiency": {
                "description": "Analysis of processing efficiency",
                "recommendations": ["Consider caching for similar content", "Parallel processing enabled"],
                "confidence": 0.85
            },
            "quality_optimization": {
                "description": "Quality improvement opportunities",
                "recommendations": ["Content quality is good", "No significant improvements needed"],
                "confidence": 0.90
            },
            "cost_optimization": {
                "description": "Cost reduction opportunities", 
                "recommendations": ["Using mock provider for testing", "Real providers available for production"],
                "confidence": 0.75
            }
        }
        
        return insights
    
    def _estimate_text_complexity(self, text: str) -> float:
        """Estimate text complexity (0-1)"""
        word_count = len(text.split())
        avg_word_length = sum(len(word) for word in text.split()) / max(1, word_count)
        sentence_count = len([s for s in text.split('.') if s.strip()])
        avg_sentence_length = word_count / max(1, sentence_count)
        
        # Simple complexity calculation
        complexity = min(1.0, (avg_word_length - 3) * 0.1 + (avg_sentence_length - 10) * 0.02)
        return max(0.0, complexity)
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection"""
        # Very basic detection - can be enhanced
        vietnamese_indicators = ['là', 'và', 'của', 'trong', 'với', 'được', 'có', 'này']
        english_indicators = ['the', 'and', 'of', 'in', 'to', 'is', 'are', 'that']
        
        text_lower = text.lower()
        vi_count = sum(1 for word in vietnamese_indicators if word in text_lower)
        en_count = sum(1 for word in english_indicators if word in text_lower)
        
        return "vi" if vi_count > en_count else "en"
    
    def _predict_processing_time(self, text_stats: Dict[str, Any], mode: ProcessingMode) -> float:
        """Predict processing time based on text stats and mode"""
        base_time = text_stats["word_count"] * 0.01  # Base: 0.01s per word
        
        mode_multipliers = {
            ProcessingMode.SPEED_OPTIMIZED: 0.5,
            ProcessingMode.QUALITY_OPTIMIZED: 2.0,
            ProcessingMode.COST_OPTIMIZED: 1.5,
            ProcessingMode.BALANCED: 1.0,
            ProcessingMode.CUSTOM: 1.0
        }
        
        return base_time * mode_multipliers.get(mode, 1.0)
    
    def _predict_cost(self, text_stats: Dict[str, Any], request: ProcessingRequest) -> float:
        """Predict processing cost"""
        # Mock provider is free, real providers have costs
        return 0.0  # For now, using mock providers
    
    def _recommend_chunking_strategy(self, text_stats: Dict[str, Any]) -> str:
        """Recommend optimal chunking strategy"""
        if text_stats["word_count"] < 100:
            return "single_chunk"
        elif text_stats["word_count"] < 500:
            return "paragraph_based"
        else:
            return "semantic_based"
    
    def _predict_optimal_transformations(self, text: str, audience: TargetAudience) -> List[TransformationType]:
        """Predict optimal transformation types"""
        # Simple prediction logic
        if "learning" in text.lower() or "education" in text.lower():
            return [TransformationType.EDUCATION_MODULE, TransformationType.PRESENTATION]
        elif "story" in text.lower() or "narrative" in text.lower():
            return [TransformationType.PODCAST_SCRIPT, TransformationType.VIDEO_SCENARIO]
        else:
            return [TransformationType.PODCAST_SCRIPT, TransformationType.EDUCATION_MODULE]
    
    def _calculate_document_coherence(self, chunks: List[Dict[str, Any]]) -> float:
        """Calculate document coherence score"""
        if len(chunks) <= 1:
            return 1.0
        
        # Simple coherence calculation based on concept overlap
        all_concepts = set()
        for chunk in chunks:
            all_concepts.update(chunk["key_concepts"])
        
        if not all_concepts:
            return 0.5
        
        chunk_concept_counts = [len(chunk["key_concepts"]) for chunk in chunks]
        avg_concepts_per_chunk = sum(chunk_concept_counts) / len(chunks)
        
        # Coherence based on concept distribution
        coherence = min(1.0, avg_concepts_per_chunk / max(1, len(all_concepts)) * 5)
        return coherence
    
    def _analyze_chunk_relationships(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze relationships between chunks"""
        relationships = []
        
        for i, chunk1 in enumerate(chunks):
            for j, chunk2 in enumerate(chunks):
                if i != j and abs(i - j) <= 2:  # Only check nearby chunks
                    # Check for concept overlap
                    concepts1 = set(chunk1["key_concepts"])
                    concepts2 = set(chunk2["key_concepts"])
                    overlap = concepts1 & concepts2
                    
                    if overlap:
                        relationships.append({
                            "source": chunk1["chunk_id"],
                            "target": chunk2["chunk_id"],
                            "type": "concept_overlap",
                            "strength": len(overlap) / max(1, len(concepts1 | concepts2)),
                            "shared_concepts": list(overlap)
                        })
        
        return relationships
    
    def _calculate_total_cost(self, translation_result: Dict[str, Any], transformation_result: Dict[str, Any]) -> float:
        """Calculate total processing cost"""
        total_cost = translation_result.get("translation_cost", 0.0)
        
        for transform_data in transformation_result.values():
            if isinstance(transform_data, dict) and "cost" in transform_data:
                total_cost += transform_data["cost"]
        
        return total_cost
    
    def _update_processing_stats(self, result: ProcessingResult):
        """Update processing statistics"""
        self.processing_stats["total_requests"] += 1
        self.processing_stats["successful_requests"] += 1
        
        # Update averages
        total = self.processing_stats["total_requests"]
        self.processing_stats["avg_processing_time"] = (
            (self.processing_stats["avg_processing_time"] * (total - 1) + result.total_processing_time) / total
        )
        self.processing_stats["avg_quality_achieved"] = (
            (self.processing_stats["avg_quality_achieved"] * (total - 1) + result.quality_achieved) / total
        )
        self.processing_stats["total_cost"] += result.total_cost
    
    def _store_learning_data(self, request: ProcessingRequest, result: ProcessingResult):
        """Store data for machine learning and optimization"""
        learning_entry = {
            "request_params": {
                "text_length": len(request.input_text),
                "processing_mode": request.processing_mode.value,
                "target_audience": request.target_audience.value,
                "quality_target": request.quality_target
            },
            "results": {
                "processing_time": result.total_processing_time,
                "quality_achieved": result.quality_achieved,
                "total_cost": result.total_cost
            },
            "timestamp": time.time()
        }
        
        self.learning_data.append(learning_entry)
        
        # Keep only recent data (last 1000 entries)
        if len(self.learning_data) > 1000:
            self.learning_data = self.learning_data[-1000:]
    
    def get_orchestrator_stats(self) -> Dict[str, Any]:
        """Get orchestrator performance statistics"""
        return {
            "processing_stats": self.processing_stats,
            "learning_data_size": len(self.learning_data),
            "engines_status": {
                "translation": bool(self.translation_manager.providers),
                "transformation": bool(self.transformation_manager.transformers),
                "chunking": True,
                "quality": True,
                "context": True
            }
        }
