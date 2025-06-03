# src/infrastructure/document_processing/orchestrators/model_orchestrator.py

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import time

from src.core.models.document import Document, DocumentChunk, ChunkProcessingResult
from src.core.utils.logger import Logger
from src.infrastructure.llm.llm_factory import LLMFactory
from src.infrastructure.document_processing.orchestrators.cost_calculator import CostCalculator

logger = Logger(__name__)


class ModelCapability(Enum):
    """Model capabilities for task assignment."""
    SUMMARY = "summary"
    TRANSLATION = "translation"
    CREATIVE = "creative"
    REASONING = "reasoning"
    EXTRACTION = "extraction"
    SIMPLE = "simple"


@dataclass
class ModelProfile:
    """Profile of an AI model with capabilities and costs."""
    name: str
    provider: str
    capabilities: List[ModelCapability]
    cost_per_1k_tokens: float
    max_tokens: int
    speed_rating: int  # 1-10, 10 being fastest
    quality_rating: int  # 1-10, 10 being best
    
    @property
    def efficiency_score(self) -> float:
        """Calculate efficiency score (quality/cost ratio)."""
        return (self.quality_rating * self.speed_rating) / self.cost_per_1k_tokens


class ModelOrchestrator:
    """Orchestrate multiple AI models for optimal processing."""
    
    def __init__(self):
        self.llm_factory = LLMFactory()
        self.cost_calculator = CostCalculator()
        self.model_profiles = self._initialize_model_profiles()
        self.processing_stats = {
            "total_chunks": 0,
            "successful_chunks": 0,
            "failed_chunks": 0,
            "total_cost": 0.0,
            "total_tokens": 0
        }
        
    def _initialize_model_profiles(self) -> Dict[str, ModelProfile]:
        """Initialize model profiles with capabilities and costs."""
        return {
            "gpt-3.5-turbo": ModelProfile(
                name="gpt-3.5-turbo",
                provider="openai",
                capabilities=[ModelCapability.SUMMARY, ModelCapability.SIMPLE, 
                             ModelCapability.EXTRACTION],
                cost_per_1k_tokens=0.0005,  # $0.0005 per 1K tokens
                max_tokens=16385,
                speed_rating=9,
                quality_rating=7
            ),
            "gpt-4-turbo": ModelProfile(
                name="gpt-4-turbo-preview",
                provider="openai",
                capabilities=[ModelCapability.REASONING, ModelCapability.CREATIVE,
                             ModelCapability.TRANSLATION],
                cost_per_1k_tokens=0.01,  # $0.01 per 1K tokens
                max_tokens=128000,
                speed_rating=7,
                quality_rating=10
            ),
            "claude-3-sonnet": ModelProfile(
                name="claude-3-sonnet-20240229",
                provider="anthropic",
                capabilities=[ModelCapability.CREATIVE, ModelCapability.REASONING,
                             ModelCapability.SUMMARY],
                cost_per_1k_tokens=0.003,  # $0.003 per 1K tokens
                max_tokens=200000,
                speed_rating=8,
                quality_rating=9
            ),
            "claude-3-opus": ModelProfile(
                name="claude-3-opus-20240229",
                provider="anthropic",
                capabilities=[ModelCapability.CREATIVE, ModelCapability.REASONING,
                             ModelCapability.TRANSLATION],
                cost_per_1k_tokens=0.015,  # $0.015 per 1K tokens
                max_tokens=200000,
                speed_rating=6,
                quality_rating=10
            ),
            "gemini-1.5-flash": ModelProfile(
                name="gemini-1.5-flash",
                provider="google",
                capabilities=[ModelCapability.SUMMARY, ModelCapability.TRANSLATION,
                             ModelCapability.SIMPLE],
                cost_per_1k_tokens=0.00035,  # $0.00035 per 1K tokens
                max_tokens=1000000,
                speed_rating=10,
                quality_rating=8
            )
        }
    
    async def process_document(
        self,
        document: Document,
        chunks: List[DocumentChunk],
        output_format: str,
        budget_limit: Optional[float] = None
    ) -> List[ChunkProcessingResult]:
        """
        Process document chunks with optimal model selection.
        
        Args:
            document: Original document
            chunks: Document chunks to process
            output_format: Target output format
            budget_limit: Optional budget constraint
            
        Returns:
            List of chunk processing results
        """
        # Create processing plan
        processing_plan = await self._create_processing_plan(
            chunks, 
            output_format,
            budget_limit
        )
        
        # Log plan
        logger.info(f"Processing plan created: {len(processing_plan)} tasks")
        
        # Process chunks in parallel batches
        results = await self._process_chunks_parallel(processing_plan)
        
        # Update stats
        self._update_processing_stats(results)
        
        return results
    
    async def _create_processing_plan(
        self,
        chunks: List[DocumentChunk],
        output_format: str,
        budget_limit: Optional[float] = None
    ) -> List[Tuple[DocumentChunk, str, Dict[str, Any]]]:
        """Create optimal processing plan for chunks."""
        plan = []
        estimated_cost = 0.0
        
        for chunk in chunks:
            # Determine required capability
            capability = self._determine_capability(chunk, output_format)
            
            # Select optimal model
            model_name = self._select_optimal_model(
                capability,
                chunk,
                budget_limit - estimated_cost if budget_limit else None
            )
            
            # Create task config
            task_config = self._create_task_config(chunk, output_format, capability)
            
            # Estimate cost
            chunk_cost = self._estimate_chunk_cost(chunk, model_name)
            estimated_cost += chunk_cost
            
            plan.append((chunk, model_name, task_config))
            
            # Check budget
            if budget_limit and estimated_cost > budget_limit:
                logger.warning(f"Budget limit reached. Planned {len(plan)} of {len(chunks)} chunks")
                break
                
        return plan
    
    def _determine_capability(
        self,
        chunk: DocumentChunk,
        output_format: str
    ) -> ModelCapability:
        """Determine required capability based on chunk and output format."""
        chunk_type = chunk.metadata.get("type", "general")
        
        # Format-specific capability mapping
        format_capability_map = {
            "podcast": {
                "chapter": ModelCapability.CREATIVE,
                "scene": ModelCapability.CREATIVE,
                "dialogue": ModelCapability.CREATIVE,
                "general": ModelCapability.SUMMARY
            },
            "course": {
                "theoretical": ModelCapability.REASONING,
                "practical": ModelCapability.EXTRACTION,
                "exercise": ModelCapability.CREATIVE,
                "general": ModelCapability.SUMMARY
            },
            "video": {
                "narrative": ModelCapability.CREATIVE,
                "technical": ModelCapability.EXTRACTION,
                "general": ModelCapability.SUMMARY
            },
            "translation": {
                "all": ModelCapability.TRANSLATION
            }
        }
        
        # Get capability for format and chunk type
        if output_format in format_capability_map:
            format_map = format_capability_map[output_format]
            if chunk_type in format_map:
                return format_map[chunk_type]
            elif "all" in format_map:
                return format_map["all"]
                
        # Default capability based on content analysis
        if self._is_complex_content(chunk.content):
            return ModelCapability.REASONING
        elif self._is_creative_content(chunk.content):
            return ModelCapability.CREATIVE
        else:
            return ModelCapability.SIMPLE
    
    def _select_optimal_model(
        self,
        capability: ModelCapability,
        chunk: DocumentChunk,
        remaining_budget: Optional[float] = None
    ) -> str:
        """Select optimal model based on capability and constraints."""
        # Filter models by capability
        capable_models = [
            (name, profile) for name, profile in self.model_profiles.items()
            if capability in profile.capabilities
        ]
        
        if not capable_models:
            # Fallback to GPT-3.5
            return "gpt-3.5-turbo"
        
        # Sort by efficiency score
        capable_models.sort(key=lambda x: x[1].efficiency_score, reverse=True)
        
        # Check budget constraints
        if remaining_budget is not None:
            for name, profile in capable_models:
                estimated_cost = self._estimate_chunk_cost(chunk, name)
                if estimated_cost <= remaining_budget:
                    return name
            # If all exceed budget, use cheapest
            return min(capable_models, key=lambda x: x[1].cost_per_1k_tokens)[0]
        
        # Return most efficient model
        return capable_models[0][0]
    
    def _create_task_config(
        self,
        chunk: DocumentChunk,
        output_format: str,
        capability: ModelCapability
    ) -> Dict[str, Any]:
        """Create task-specific configuration."""
        base_config = {
            "temperature": 0.7,
            "max_tokens": 2000,
            "chunk_context": {
                "type": chunk.metadata.get("type", "general"),
                "index": chunk.metadata.get("index", 0),
                "total_chunks": chunk.metadata.get("total_chunks", 1)
            }
        }
        
        # Format-specific configs
        format_configs = {
            "podcast": {
                "style": "conversational",
                "tone": "engaging",
                "structure": "episode_segment"
            },
            "course": {
                "style": "educational",
                "tone": "clear",
                "structure": "lesson"
            },
            "video": {
                "style": "visual",
                "tone": "dynamic",
                "structure": "scene"
            }
        }
        
        if output_format in format_configs:
            base_config.update(format_configs[output_format])
            
        # Capability-specific adjustments
        if capability == ModelCapability.CREATIVE:
            base_config["temperature"] = 0.8
        elif capability == ModelCapability.REASONING:
            base_config["temperature"] = 0.3
        elif capability == ModelCapability.SUMMARY:
            base_config["max_tokens"] = 500
            
        return base_config
    
    def _estimate_chunk_cost(self, chunk: DocumentChunk, model_name: str) -> float:
        """Estimate processing cost for a chunk."""
        if model_name not in self.model_profiles:
            return 0.0
            
        profile = self.model_profiles[model_name]
        
        # Estimate tokens (input + output)
        input_tokens = int(chunk.word_count * 1.33)  # Rough estimate
        output_tokens = 500  # Average output
        total_tokens = input_tokens + output_tokens
        
        # Calculate cost
        cost = (total_tokens / 1000) * profile.cost_per_1k_tokens
        
        return cost
    
    async def _process_chunks_parallel(
        self,
        processing_plan: List[Tuple[DocumentChunk, str, Dict[str, Any]]]
    ) -> List[ChunkProcessingResult]:
        """Process chunks in parallel batches."""
        results = []
        batch_size = 5  # Process 5 chunks at a time
        
        for i in range(0, len(processing_plan), batch_size):
            batch = processing_plan[i:i + batch_size]
            
            # Create tasks for batch
            tasks = []
            for chunk, model_name, config in batch:
                task = self._process_single_chunk(chunk, model_name, config)
                tasks.append(task)
            
            # Process batch
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Handle results
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Chunk processing failed: {str(result)}")
                    # Create error result
                    error_result = ChunkProcessingResult(
                        chunk=batch[0][0],  # Get chunk from batch
                        processed_content="",
                        model_used="error",
                        tokens_used=0,
                        processing_time=0.0,
                        cost=0.0,
                        error=str(result)
                    )
                    results.append(error_result)
                else:
                    results.append(result)
            
            # Brief pause between batches
            await asyncio.sleep(0.1)
            
        return results
    
    async def _process_single_chunk(
        self,
        chunk: DocumentChunk,
        model_name: str,
        config: Dict[str, Any]
    ) -> ChunkProcessingResult:
        """Process a single chunk with specified model."""
        start_time = time.time()
        
        try:
            # Get model provider
            provider = self.model_profiles[model_name].provider
            
            # Create prompt based on output format
            prompt = self._create_chunk_prompt(chunk, config)
            
            # Process with appropriate provider
            if provider == "openai":
                from src.infrastructure.llm.providers.openai_provider import OpenAIProvider
                llm = OpenAIProvider()
                response = await llm.translate(  # Using translate as generic process method
                    prompt,
                    target_language="",  # Not used for general processing
                    model=model_name,
                    temperature=config.get("temperature", 0.7),
                    max_tokens=config.get("max_tokens", 2000)
                )
            elif provider == "anthropic":
                from src.infrastructure.llm.providers.anthropic_provider import AnthropicProvider
                llm = AnthropicProvider()
                response = await llm.translate(
                    prompt,
                    target_language="",
                    model=model_name,
                    temperature=config.get("temperature", 0.7),
                    max_tokens=config.get("max_tokens", 2000)
                )
            else:
                # Fallback to simple processing
                response = await self._simple_process(chunk, config)
            
            # Calculate metrics
            processing_time = time.time() - start_time
            tokens_used = self._estimate_tokens_used(chunk, response)
            cost = self._calculate_actual_cost(model_name, tokens_used)
            
            return ChunkProcessingResult(
                chunk=chunk,
                processed_content=response,
                model_used=model_name,
                tokens_used=tokens_used,
                processing_time=processing_time,
                cost=cost,
                metadata={
                    "config": config,
                    "provider": provider
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing chunk: {str(e)}")
            return ChunkProcessingResult(
                chunk=chunk,
                processed_content="",
                model_used=model_name,
                tokens_used=0,
                processing_time=time.time() - start_time,
                cost=0.0,
                error=str(e)
            )
    
    def _create_chunk_prompt(self, chunk: DocumentChunk, config: Dict[str, Any]) -> str:
        """Create processing prompt for chunk."""
        output_format = config.get("structure", "general")
        
        prompts = {
            "episode_segment": f"""
Transform this content into a podcast episode segment. Make it conversational and engaging.
Include natural transitions and speaking cues.

Content:
{chunk.content}
""",
            "lesson": f"""
Transform this content into an educational lesson segment.
Make it clear and structured with learning objectives.

Content:
{chunk.content}
""",
            "scene": f"""
Transform this content into a video script scene.
Include visual descriptions and pacing notes.

Content:
{chunk.content}
""",
            "general": f"""
Process and optimize this content maintaining its key information.

Content:
{chunk.content}
"""
        }
        
        return prompts.get(output_format, prompts["general"])
    
    async def _simple_process(self, chunk: DocumentChunk, config: Dict[str, Any]) -> str:
        """Simple processing fallback."""
        # Basic transformation without LLM
        content = chunk.content
        
        # Apply basic formatting based on config
        if config.get("style") == "conversational":
            # Add conversational markers
            content = f"Let's talk about this: {content}"
        elif config.get("style") == "educational":
            # Add educational structure
            content = f"Learning Point: {content}"
        elif config.get("style") == "visual":
            # Add visual cues
            content = f"[SCENE]: {content}"
            
        return content
    
    def _estimate_tokens_used(self, chunk: DocumentChunk, response: str) -> int:
        """Estimate tokens used in processing."""
        input_tokens = int(chunk.word_count * 1.33)
        output_tokens = int(len(response.split()) * 1.33)
        return input_tokens + output_tokens
    
    def _calculate_actual_cost(self, model_name: str, tokens_used: int) -> float:
        """Calculate actual cost based on tokens used."""
        if model_name not in self.model_profiles:
            return 0.0
            
        profile = self.model_profiles[model_name]
        return (tokens_used / 1000) * profile.cost_per_1k_tokens
    
    def _is_complex_content(self, content: str) -> bool:
        """Check if content requires complex reasoning."""
        indicators = [
            "analyze", "compare", "evaluate", "synthesize",
            "therefore", "however", "consequently", "thus"
        ]
        content_lower = content.lower()
        return sum(1 for ind in indicators if ind in content_lower) >= 2
    
    def _is_creative_content(self, content: str) -> bool:
        """Check if content requires creative processing."""
        indicators = [
            "story", "narrative", "character", "dialogue",
            "imagine", "describe", "scene", "emotion"
        ]
        content_lower = content.lower()
        return sum(1 for ind in indicators if ind in content_lower) >= 2
    
    def _update_processing_stats(self, results: List[ChunkProcessingResult]):
        """Update processing statistics."""
        self.processing_stats["total_chunks"] += len(results)
        
        for result in results:
            if result.success:
                self.processing_stats["successful_chunks"] += 1
            else:
                self.processing_stats["failed_chunks"] += 1
                
            self.processing_stats["total_cost"] += result.cost
            self.processing_stats["total_tokens"] += result.tokens_used
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get current processing statistics."""
        return {
            **self.processing_stats,
            "success_rate": (
                self.processing_stats["successful_chunks"] / 
                self.processing_stats["total_chunks"] * 100
                if self.processing_stats["total_chunks"] > 0 else 0
            ),
            "average_cost_per_chunk": (
                self.processing_stats["total_cost"] / 
                self.processing_stats["total_chunks"]
                if self.processing_stats["total_chunks"] > 0 else 0
            )
        }
