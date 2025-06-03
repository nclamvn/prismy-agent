# src/infrastructure/document_processing/document_processor.py

import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import json

from src.core.models.document import (
    Document, DocumentChunk, ProcessedDocument, 
    ChunkProcessingResult, ProcessingStatus
)
from src.core.utils.logger import Logger
from src.core.exceptions import ProcessingError

from src.infrastructure.document_processing.chunkers.intelligent_chunker import IntelligentChunker
from src.infrastructure.document_processing.orchestrators.model_orchestrator import ModelOrchestrator
from src.infrastructure.document_processing.orchestrators.cost_calculator import CostCalculator
from src.infrastructure.document_processing.optimizers.hybrid_processor import HybridProcessor
from src.infrastructure.document_processing.cache.cache_manager import CacheManager

logger = Logger(__name__)


class DocumentProcessor:
    """
    Main document processing system that coordinates all components.
    
    Features:
    - Intelligent chunking
    - Multi-model orchestration
    - Hybrid NLP/LLM processing
    - Smart caching
    - Cost optimization
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize components
        self.chunker = IntelligentChunker()
        self.orchestrator = ModelOrchestrator()
        self.cost_calculator = CostCalculator()
        self.hybrid_processor = HybridProcessor()
        self.cache_manager = CacheManager(
            max_size_mb=self.config.get("cache_size_mb", 500),
            ttl_hours=self.config.get("cache_ttl_hours", 24)
        )
        
        # Processing stats
        self.stats = {
            "documents_processed": 0,
            "total_chunks": 0,
            "cache_hits": 0,
            "total_cost": 0.0,
            "total_time": 0.0
        }
        
    async def process_document(
        self,
        document: Document,
        output_format: str,
        options: Optional[Dict[str, Any]] = None
    ) -> ProcessedDocument:
        """
        Process a document end-to-end.
        
        Args:
            document: Document to process
            output_format: Target format (podcast, course, video, translation)
            options: Processing options including:
                - target_language: For translation
                - quality_level: high/medium/low
                - budget_limit: Maximum cost in USD
                - use_cache: Whether to use caching
                - parallel_chunks: Number of chunks to process in parallel
                
        Returns:
            ProcessedDocument with results
        """
        start_time = time.time()
        options = options or {}
        
        try:
            # Update document status
            document.processing_status = ProcessingStatus.PROCESSING
            
            # Step 1: Preprocess document with hybrid processor
            logger.info(f"Preprocessing document: {document.id}")
            preprocessed = await self.hybrid_processor.preprocess_document(
                document,
                output_format
            )
            
            # Step 2: Intelligent chunking
            logger.info(f"Chunking document for {output_format} format")
            chunks, context_map = self.chunker.chunk_document(
                document,
                output_format
            )
            logger.info(f"Created {len(chunks)} chunks")
            
            # Step 3: Check cache and filter chunks
            chunks_to_process = []
            cached_results = []
            
            if options.get("use_cache", True):
                for chunk in chunks:
                    cached_result = self.cache_manager.get_chunk_result(chunk)
                    if cached_result:
                        cached_results.append(cached_result)
                        self.stats["cache_hits"] += 1
                    else:
                        chunks_to_process.append(chunk)
            else:
                chunks_to_process = chunks
                
            logger.info(f"Cache hits: {len(cached_results)}, chunks to process: {len(chunks_to_process)}")
            
            # Step 4: Process remaining chunks with orchestrator
            processing_results = []
            
            if chunks_to_process:
                logger.info(f"Processing {len(chunks_to_process)} chunks with orchestrator")
                
                # Preprocess chunks for token reduction
                preprocessed_chunks = []
                for chunk in chunks_to_process:
                    # Create a copy to avoid modifying original
                    chunk_copy = DocumentChunk(
                        content=chunk.content,
                        start_position=chunk.start_position,
                        end_position=chunk.end_position,
                        metadata=chunk.metadata.copy()
                    )
                    
                    chunk_data = await self.hybrid_processor.preprocess_chunk(
                        chunk_copy,
                        preprocessed
                    )
                    
                    # Create compressed version
                    compressed_content = self.hybrid_processor.compress_for_llm(
                        chunk_copy.content,
                        max_tokens=2000
                    )
                    
                    # Store original content and compressed version in metadata
                    chunk_copy.metadata["original_content"] = chunk.content
                    chunk_copy.metadata["preprocessing"] = chunk_data
                    chunk_copy.metadata["compressed_content"] = compressed_content
                    
                    # Use compressed content for processing
                    chunk_copy.content = compressed_content
                    
                    preprocessed_chunks.append(chunk_copy)
                
                # Process with orchestrator
                results = await self.orchestrator.process_document(
                    document,
                    preprocessed_chunks,
                    output_format,
                    budget_limit=options.get("budget_limit")
                )
                
                # Cache successful results with ORIGINAL content
                if options.get("use_cache", True):
                    for original_chunk, result in zip(chunks_to_process, results):
                        if result.success:
                            # Cache with original chunk (unmodified content)
                            self.cache_manager.cache_chunk_result(original_chunk, result)
                            
                processing_results.extend(results)
                
            # Combine cached and new results
            all_results = cached_results + processing_results
            
            # Step 5: Merge results based on output format
            final_content = await self._merge_results(
                all_results,
                output_format,
                context_map,
                options
            )
            
            # Step 6: Post-process based on format
            final_content = await self._post_process(
                final_content,
                output_format,
                options
            )
            
            # Calculate metrics
            processing_time = time.time() - start_time
            total_cost = sum(r.cost for r in processing_results)
            
            # Update stats
            self.stats["documents_processed"] += 1
            self.stats["total_chunks"] += len(chunks)
            self.stats["total_cost"] += total_cost
            self.stats["total_time"] += processing_time
            
            # Create processed document
            processed_doc = ProcessedDocument(
                original_document=document,
                chunks=chunks,
                output_format=output_format,
                processed_content=final_content,
                metadata={
                    "preprocessing": preprocessed.metadata,
                    "context_map": context_map,
                    "cache_hits": len(cached_results),
                    "quality_level": options.get("quality_level", "medium"),
                    "models_used": self._get_models_used(all_results)
                },
                processing_time=processing_time,
                total_cost=total_cost,
                model_usage=self._calculate_model_usage(all_results)
            )
            
            # Update document status
            document.processing_status = ProcessingStatus.COMPLETED
            
            logger.info(f"Document processed successfully in {processing_time:.2f}s, cost: ${total_cost:.4f}")
            
            return processed_doc
            
        except Exception as e:
            document.processing_status = ProcessingStatus.FAILED
            logger.error(f"Document processing failed: {str(e)}")
            raise ProcessingError(f"Failed to process document: {str(e)}")
    
    async def process_batch(
        self,
        documents: List[Document],
        output_format: str,
        options: Optional[Dict[str, Any]] = None
    ) -> List[ProcessedDocument]:
        """Process multiple documents in batch."""
        options = options or {}
        batch_size = options.get("batch_size", 5)
        
        results = []
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Process batch in parallel
            tasks = [
                self.process_document(doc, output_format, options)
                for doc in batch
            ]
            
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for doc, result in zip(batch, batch_results):
                if isinstance(result, Exception):
                    logger.error(f"Failed to process document {doc.id}: {str(result)}")
                    # Create error result
                    error_result = ProcessedDocument(
                        original_document=doc,
                        chunks=[],
                        output_format=output_format,
                        processed_content="",
                        metadata={"error": str(result)},
                        processing_time=0.0,
                        total_cost=0.0
                    )
                    results.append(error_result)
                else:
                    results.append(result)
                    
        return results
    
    async def _merge_results(
        self,
        results: List[ChunkProcessingResult],
        output_format: str,
        context_map: Dict[str, Any],
        options: Dict[str, Any]
    ) -> str:
        """Merge chunk results based on output format."""
        # Sort results by chunk index
        results.sort(key=lambda r: r.chunk.metadata.get("index", 0))
        
        if output_format == "translation":
            # Simple concatenation for translations
            return "\n\n".join([r.processed_content for r in results if r.success])
            
        elif output_format == "podcast":
            return self._merge_podcast_results(results, context_map)
            
        elif output_format == "course":
            return self._merge_course_results(results, context_map)
            
        elif output_format == "video":
            return self._merge_video_results(results, context_map)
            
        else:
            # Default merging
            return "\n\n---\n\n".join([r.processed_content for r in results if r.success])
    
    def _merge_podcast_results(
        self,
        results: List[ChunkProcessingResult],
        context_map: Dict[str, Any]
    ) -> str:
        """Merge results into podcast format."""
        episodes = []
        current_episode = []
        current_duration = 0
        max_duration = 20 * 60  # 20 minutes per episode
        
        for result in results:
            if not result.success:
                continue
                
            chunk_duration = result.chunk.metadata.get("duration_minutes", 5) * 60
            
            if current_duration + chunk_duration > max_duration and current_episode:
                # Create episode
                episode_content = self._format_podcast_episode(
                    current_episode,
                    len(episodes) + 1
                )
                episodes.append(episode_content)
                
                current_episode = [result]
                current_duration = chunk_duration
            else:
                current_episode.append(result)
                current_duration += chunk_duration
                
        # Add final episode
        if current_episode:
            episode_content = self._format_podcast_episode(
                current_episode,
                len(episodes) + 1
            )
            episodes.append(episode_content)
            
        # Create series overview
        overview = self._create_podcast_overview(episodes, context_map)
        
        return overview + "\n\n" + "\n\n".join(episodes)
    
    def _merge_course_results(
        self,
        results: List[ChunkProcessingResult],
        context_map: Dict[str, Any]
    ) -> str:
        """Merge results into course format."""
        modules = {}
        
        for result in results:
            if not result.success:
                continue
                
            lesson_type = result.chunk.metadata.get("lesson_type", "general")
            module_name = result.chunk.metadata.get("section", "General")
            
            if module_name not in modules:
                modules[module_name] = []
                
            lesson = self._format_course_lesson(
                result,
                len(modules[module_name]) + 1
            )
            modules[module_name].append(lesson)
            
        # Create course structure
        course_content = self._create_course_structure(modules, context_map)
        
        return course_content
    
    def _merge_video_results(
        self,
        results: List[ChunkProcessingResult],
        context_map: Dict[str, Any]
    ) -> str:
        """Merge results into video script format."""
        scenes = []
        
        for result in results:
            if not result.success:
                continue
                
            scene = self._format_video_scene(
                result,
                len(scenes) + 1
            )
            scenes.append(scene)
            
        # Create video script
        script = self._create_video_script(scenes, context_map)
        
        return script
    
    def _format_podcast_episode(
        self,
        results: List[ChunkProcessingResult],
        episode_num: int
    ) -> str:
        """Format results as podcast episode."""
        segments = []
        
        for result in results:
            segments.append(f"""
[SEGMENT {len(segments) + 1}]
{result.processed_content}

[TRANSITION]
""")
        
        episode = f"""
# EPISODE {episode_num}

## Episode Overview
- Duration: ~{sum(r.chunk.metadata.get('duration_minutes', 5) for r in results)} minutes
- Segments: {len(results)}

## Content
{"".join(segments)}

## Closing
[Episode wrap-up and preview of next episode]
"""
        return episode
    
    def _format_course_lesson(
        self,
        result: ChunkProcessingResult,
        lesson_num: int
    ) -> str:
        """Format result as course lesson."""
        lesson_type = result.chunk.metadata.get("lesson_type", "general")
        needs_exercises = result.chunk.metadata.get("exercises_needed", False)
        
        lesson = f"""
### Lesson {lesson_num}: {result.chunk.metadata.get('title', 'Untitled')}

**Type:** {lesson_type}
**Duration:** ~{result.chunk.metadata.get('duration_minutes', 10)} minutes

#### Content
{result.processed_content}
"""
        
        if needs_exercises:
            lesson += """
#### Exercises
1. [Exercise based on content]
2. [Practice activity]
3. [Assessment question]
"""
        
        return lesson
    
    def _format_video_scene(
        self,
        result: ChunkProcessingResult,
        scene_num: int
    ) -> str:
        """Format result as video scene."""
        duration = result.chunk.metadata.get("duration_seconds", 30)
        scene_count = result.chunk.metadata.get("scene_count", 1)
        
        scene = f"""
## SCENE {scene_num}
**Duration:** {duration} seconds
**Shots:** {scene_count}

{result.processed_content}

**Visual Notes:**
- [Camera angles and movements]
- [Transition to next scene]
"""
        return scene
    
    def _create_podcast_overview(
        self,
        episodes: List[str],
        context_map: Dict[str, Any]
    ) -> str:
        """Create podcast series overview."""
        total_duration = len(episodes) * 20  # Approximate
        
        overview = f"""
# PODCAST SERIES OVERVIEW

## Series Information
- Total Episodes: {len(episodes)}
- Total Duration: ~{total_duration} minutes
- Format: Educational/Conversational

## Episode Guide
"""
        
        for i in range(len(episodes)):
            overview += f"- Episode {i + 1}: [Main topic covered]\n"
            
        overview += """
## Series Description
[Comprehensive description of the podcast series, target audience, and key takeaways]
"""
        
        return overview
    
    def _create_course_structure(
        self,
        modules: Dict[str, List[str]],
        context_map: Dict[str, Any]
    ) -> str:
        """Create course structure."""
        total_lessons = sum(len(lessons) for lessons in modules.values())
        
        structure = f"""
# COURSE STRUCTURE

## Course Overview
- Total Modules: {len(modules)}
- Total Lessons: {total_lessons}
- Estimated Duration: {total_lessons * 15} minutes

## Learning Objectives
1. [Primary objective]
2. [Secondary objective]
3. [Additional objectives]

## Modules
"""
        
        for module_name, lessons in modules.items():
            structure += f"\n## Module: {module_name}\n"
            structure += f"**Lessons:** {len(lessons)}\n\n"
            structure += "\n".join(lessons)
            
        structure += """

## Assessment
- Quizzes after each module
- Final project/assessment
- Certificate of completion
"""
        
        return structure
    
    def _create_video_script(
        self,
        scenes: List[str],
        context_map: Dict[str, Any]
    ) -> str:
        """Create video script."""
        total_duration = sum(30 for _ in scenes)  # Default 30s per scene
        
        script = f"""
# VIDEO SCRIPT

## Video Information
- Total Scenes: {len(scenes)}
- Estimated Duration: {total_duration} seconds
- Format: Social Media (TikTok/Reels)
- Aspect Ratio: 9:16

## Pre-Production Notes
- Style: [Visual style guide]
- Music: [Background music suggestions]
- Effects: [Transition and effect notes]

## Script
"""
        
        script += "\n".join(scenes)
        
        script += """

## Post-Production Notes
- Color grading: [Suggestions]
- Sound design: [Requirements]
- Captions: [Style guide]
"""
        
        return script
    
    async def _post_process(
        self,
        content: str,
        output_format: str,
        options: Dict[str, Any]
    ) -> str:
        """Post-process content based on format."""
        # Add format-specific post-processing
        
        if output_format == "podcast":
            # Add intro/outro templates
            intro = options.get("podcast_intro", "[Standard podcast intro]")
            outro = options.get("podcast_outro", "[Standard podcast outro]")
            content = f"{intro}\n\n{content}\n\n{outro}"
            
        elif output_format == "course":
            # Add course metadata
            metadata = options.get("course_metadata", {})
            if metadata:
                header = f"""
# {metadata.get('title', 'Course Title')}
**Instructor:** {metadata.get('instructor', 'Unknown')}
**Level:** {metadata.get('level', 'Intermediate')}

---

"""
                content = header + content
                
        elif output_format == "video":
            # Add production metadata
            if options.get("add_production_notes", True):
                production_notes = """
## PRODUCTION CHECKLIST
- [ ] Review script for timing
- [ ] Prepare visual assets
- [ ] Record voiceover
- [ ] Edit video
- [ ] Add captions
- [ ] Color correction
- [ ] Export in correct format
"""
                content += "\n\n" + production_notes
                
        return content
    
    def _get_models_used(self, results: List[ChunkProcessingResult]) -> List[str]:
        """Get list of models used in processing."""
        models = set()
        for result in results:
            if result.success:
                models.add(result.model_used)
        return list(models)
    
    def _calculate_model_usage(
        self,
        results: List[ChunkProcessingResult]
    ) -> Dict[str, int]:
        """Calculate token usage by model."""
        usage = {}
        for result in results:
            if result.success:
                model = result.model_used
                if model not in usage:
                    usage[model] = 0
                usage[model] += result.tokens_used
        return usage
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        cache_stats = self.cache_manager.get_cache_stats()
        orchestrator_stats = self.orchestrator.get_processing_stats()
        
        return {
            "processor_stats": self.stats,
            "cache_stats": cache_stats,
            "orchestrator_stats": orchestrator_stats,
            "average_cost_per_document": (
                self.stats["total_cost"] / self.stats["documents_processed"]
                if self.stats["documents_processed"] > 0 else 0
            ),
            "average_processing_time": (
                self.stats["total_time"] / self.stats["documents_processed"]
                if self.stats["documents_processed"] > 0 else 0
            )
        }
    
    def optimize_cache(self):
        """Optimize cache by removing low-value entries."""
        self.cache_manager.optimize_cache()
        
    def clear_cache(self):
        """Clear all cache entries."""
        self.cache_manager.clear_expired()