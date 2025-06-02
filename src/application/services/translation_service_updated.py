"""Application service for translation operations with advanced chunking and caching."""

from typing import Optional, List, Dict, Any
import asyncio
import time
import logging

from src.core.use_cases.translate_text import TranslateTextUseCase
from src.core.entities.translation import TranslationRequest, TranslationResult, ProcessingConfig
from src.infrastructure.ai_clients.openai_translator import OpenAITranslator
from src.infrastructure.repositories.memory_cache import SmartCache
from src.infrastructure.chunking.smart_chunker import SmartTextChunker
from src.infrastructure.chunking.chunk_combiner import SmartChunkCombiner

logger = get_logger(__name__)


class TranslationService:
    """High-level service for translation operations with advanced chunking and caching."""
    
    def __init__(self, openai_api_key: Optional[str] = None, enable_cache: bool = True):
        self.openai_api_key = openai_api_key
        self.enable_cache = enable_cache
        self._translator = None
        self._cache = None
        self._use_case = None
        self._chunker = None
        self._combiner = None
        
        # Initialize cache if enabled
        if self.enable_cache:
            self._cache = SmartCache(default_ttl=3600)  # 1 hour TTL
        
        # Initialize chunking system
        self._chunker = SmartTextChunker(
            max_chunk_size=2800,  # Optimized for GPT models
            overlap_size=200,
            preserve_formulas=True,
            preserve_code=True
        )
        self._combiner = SmartChunkCombiner()
    
    def _get_translator(self) -> OpenAITranslator:
        """Lazy initialization of translator."""
        if not self._translator:
            if not self.openai_api_key:
                raise ValueError("OpenAI API key is required")
            self._translator = OpenAITranslator(self.openai_api_key)
        return self._translator
    
    def _get_use_case(self) -> TranslateTextUseCase:
        """Lazy initialization of use case with cache."""
        if not self._use_case:
            translator = self._get_translator()
            # Pass cache to use case if available
            self._use_case = TranslateTextUseCase(
                translator=translator,
                cache=self._cache
            )
        return self._use_case
    
    async def translate_text(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None,
        preserve_formatting: bool = True,
        quality_tier: str = "standard"
    ) -> TranslationResult:
        """Translate text using smart chunking, caching, and AI."""
        
        start_time = time.time()
        
        # Check if text needs chunking
        needs_chunking = len(text) > 2500
        
        if not needs_chunking:
            # Use simple translation for short text
            return await self._translate_simple(
                text, target_language, source_language, 
                preserve_formatting, quality_tier, start_time
            )
        
        # Use advanced chunking for long text
        return await self._translate_with_chunking(
            text, target_language, source_language,
            preserve_formatting, quality_tier, start_time
        )
    
    async def _translate_simple(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str],
        preserve_formatting: bool,
        quality_tier: str,
        start_time: float
    ) -> TranslationResult:
        """Simple translation for short text with caching."""
        
        # Check cache first if enabled
        if self._cache:
            cache_key = self._cache.generate_key(
                text=text,
                target_lang=target_language,
                preserve_formatting=preserve_formatting,
                quality_tier=quality_tier
            )
            
            cached_result = await self._cache.get(cache_key)
            if cached_result:
                # Update processing time for cache hit
                cache_retrieval_time = time.time() - start_time
                cached_result.processing_time = cache_retrieval_time
                cached_result.metadata = cached_result.metadata or {}
                cached_result.metadata['from_cache'] = True
                cached_result.metadata['cache_hit'] = True
                cached_result.metadata['chunked'] = False
                return cached_result
        
        # Create translation request
        request = TranslationRequest(
            text=text,
            source_language=source_language,
            target_language=target_language,
            preserve_formatting=preserve_formatting,
            quality_tier=quality_tier
        )
        
        # Execute translation
        use_case = self._get_use_case()
        result = await use_case.execute(request)
        
        # Cache result if successful and cache enabled
        if self._cache and result.success:
            await self._cache.set(cache_key, result)
            
            # Add cache metadata
            result.metadata = result.metadata or {}
            result.metadata['cached'] = True
            result.metadata['chunked'] = False
        
        return result
    
    async def _translate_with_chunking(
        self,
        text: str,
        target_language: str, 
        source_language: Optional[str],
        preserve_formatting: bool,
        quality_tier: str,
        start_time: float
    ) -> TranslationResult:
        """Advanced translation with smart chunking."""
        
        logger.info(f"Using chunking for text of {len(text)} characters")
        
        try:
            # Step 1: Smart chunking
            chunks = self._chunker.chunk_text(text)
            total_chunks = len(chunks)
            
            logger.info(f"Created {total_chunks} chunks")
            
            # Step 2: Translate each chunk
            translated_chunks = []
            successful_chunks = 0
            chunk_times = []
            
            for i, chunk in enumerate(chunks):
                chunk_start_time = time.time()
                
                try:
                    # Check cache for individual chunk
                    chunk_cache_key = None
                    if self._cache:
                        chunk_cache_key = self._cache.generate_key(
                            text=chunk.main_content,
                            target_lang=target_language,
                            preserve_formatting=preserve_formatting,
                            quality_tier=quality_tier
                        )
                        
                        cached_chunk = await self._cache.get(chunk_cache_key)
                        if cached_chunk:
                            chunk_time = time.time() - chunk_start_time
                            translated_chunks.append({
                                'chunk_id': chunk.chunk_id,
                                'translated': cached_chunk.translated_text,
                                'original_content': chunk.main_content,
                                'processing_time': chunk_time,
                                'from_cache': True,
                                'metadata': chunk.metadata.__dict__ if chunk.metadata else {}
                            })
                            successful_chunks += 1
                            chunk_times.append({'chunk_id': chunk.chunk_id, 'time': chunk_time})
                            continue
                    
                    # Create request for chunk
                    chunk_request = TranslationRequest(
                        text=chunk.main_content,
                        source_language=source_language,
                        target_language=target_language,
                        preserve_formatting=preserve_formatting,
                        quality_tier=quality_tier
                    )
                    
                    # Add context if available
                    if chunk.context:
                        chunk_request.context = chunk.context
                    
                    # Translate chunk
                    use_case = self._get_use_case()
                    chunk_result = await use_case.execute(chunk_request)
                    
                    chunk_time = time.time() - chunk_start_time
                    
                    if chunk_result.success:
                        # Cache individual chunk result
                        if self._cache and chunk_cache_key:
                            await self._cache.set(chunk_cache_key, chunk_result)
                        
                        translated_chunks.append({
                            'chunk_id': chunk.chunk_id,
                            'translated': chunk_result.translated_text,
                            'original_content': chunk.main_content,
                            'processing_time': chunk_time,
                            'from_cache': False,
                            'confidence': chunk_result.confidence,
                            'metadata': chunk.metadata.__dict__ if chunk.metadata else {}
                        })
                        successful_chunks += 1
                    else:
                        # Handle failed chunk
                        translated_chunks.append({
                            'chunk_id': chunk.chunk_id,
                            'translated': f"[TRANSLATION ERROR]: {chunk.main_content[:200]}...",
                            'original_content': chunk.main_content,
                            'processing_time': chunk_time,
                            'error': True
                        })
                    
                    chunk_times.append({'chunk_id': chunk.chunk_id, 'time': chunk_time})
                    
                    # Add small delay between chunks
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Error translating chunk {i}: {str(e)}")
                    chunk_time = time.time() - chunk_start_time
                    translated_chunks.append({
                        'chunk_id': chunk.chunk_id,
                        'translated': f"[CHUNK ERROR]: {str(e)}",
                        'original_content': chunk.main_content,
                        'processing_time': chunk_time,
                        'error': True
                    })
                    chunk_times.append({'chunk_id': chunk.chunk_id, 'time': chunk_time})
            
            # Step 3: Combine chunks intelligently
            combined_text = self._combiner.combine_chunks(translated_chunks)
            
            # Calculate final metrics
            total_time = time.time() - start_time
            avg_chunk_time = sum(ct['time'] for ct in chunk_times) / len(chunk_times) if chunk_times else 0
            success_rate = successful_chunks / total_chunks if total_chunks > 0 else 0
            
            # Create final result
            result = TranslationResult(
                translated_text=combined_text,
                source_language=source_language or "auto-detected",
                target_language=target_language,
                success=success_rate > 0.5,  # Success if >50% chunks successful
                confidence=success_rate,
                processing_time=total_time,
                chunks_processed=total_chunks,
                tokens_used=sum(len(chunk.main_content.split()) for chunk in chunks),
                model_used="gpt-3.5-turbo",
                metadata={
                    'chunked': True,
                    'total_chunks': total_chunks,
                    'successful_chunks': successful_chunks,
                    'failed_chunks': total_chunks - successful_chunks,
                    'success_rate': success_rate,
                    'avg_chunk_time': avg_chunk_time,
                    'chunk_times': chunk_times,
                    'chunking_strategy': 'smart_chunker',
                    'preserve_formatting': preserve_formatting,
                    'quality_tier': quality_tier
                }
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Chunking translation failed: {str(e)}")
            return TranslationResult(
                translated_text=f"Translation failed: {str(e)}",
                source_language=source_language or "unknown",
                target_language=target_language,
                success=False,
                confidence=0.0,
                processing_time=time.time() - start_time,
                model_used="error"
            )
    
    def translate_text_sync(
        self, 
        text: str, 
        target_language: str,
        source_language: Optional[str] = None,
        preserve_formatting: bool = True,
        quality_tier: str = "standard"
    ) -> TranslationResult:
        """Synchronous wrapper for translation with smart chunking and caching."""
        return asyncio.run(
            self.translate_text(
                text, 
                target_language, 
                source_language, 
                preserve_formatting,
                quality_tier
            )
        )
    
    def update_api_key(self, api_key: str) -> None:
        """Update API key and reset translator."""
        self.openai_api_key = api_key
        self._translator = None
        self._use_case = None
    
    def is_configured(self) -> bool:
        """Check if service is properly configured."""
        return bool(self.openai_api_key)
    
    def get_cache_stats(self) -> Optional[dict]:
        """Get cache performance statistics."""
        if not self._cache:
            return None
        
        return self._cache.get_performance_stats()
    
    def get_chunking_stats(self, text: str) -> Dict[str, Any]:
        """Get chunking statistics for given text."""
        if not self._chunker:
            return {}
        
        return {
            'text_length': len(text),
            'estimated_chunks': self._chunker.estimate_chunks(text),
            'optimal_chunk_size': self._chunker.get_optimal_chunk_size(text),
            'needs_chunking': len(text) > 2500,
            'chunking_strategy': 'smart_chunker'
        }
    
    async def clear_cache(self) -> None:
        """Clear translation cache."""
        if self._cache:
            await self._cache.clear()
    
    async def invalidate_cache_pattern(self, pattern: str) -> None:
        """Invalidate cache entries matching pattern."""
        if self._cache:
            await self._cache.invalidate(pattern)
    
    def toggle_cache(self, enable: bool) -> None:
        """Enable or disable caching."""
        self.enable_cache = enable
        if enable and not self._cache:
            self._cache = SmartCache(default_ttl=3600)
        elif not enable:
            self._cache = None
            # Reset use case to remove cache
            self._use_case = None
    
    def get_service_info(self) -> dict:
        """Get comprehensive service information."""
        cache_stats = self.get_cache_stats()
        
        return {
            'configured': self.is_configured(),
            'cache_enabled': self.enable_cache,
            'cache_stats': cache_stats,
            'chunking_enabled': True,
            'chunker_type': 'SmartTextChunker',
            'combiner_type': 'SmartChunkCombiner',
            'translator_type': 'OpenAI' if self._translator else 'Not initialized',
            'api_key_set': bool(self.openai_api_key),
            'performance': {
                'cache_hit_rate': cache_stats.get('hit_rate_percent', 0) if cache_stats else 0,
                'total_requests': cache_stats.get('total_requests', 0) if cache_stats else 0,
                'memory_usage_mb': cache_stats.get('memory_usage_mb', 0) if cache_stats else 0
            },
            'features': [
                'Smart Chunking',
                'Context Preservation', 
                'Formula Handling',
                'Cache System',
                'Overlap Detection'
            ]
        }
