"""Use case for translating text with caching support."""

import time
import hashlib
from typing import Optional

from src.core.entities.translation import TranslationRequest, TranslationResult
from src.core.interfaces.translation import TranslatorInterface, CacheInterface


class TranslateTextUseCase:
    """Use case for text translation with caching."""
    
    def __init__(self, translator: TranslatorInterface, cache: Optional[CacheInterface] = None):
        self.translator = translator
        self.cache = cache
    
    async def execute(self, request: TranslationRequest) -> TranslationResult:
        """Execute translation with caching support."""
        start_time = time.time()
        
        # Try cache first if available
        if self.cache:
            cache_key = self._generate_cache_key(request)
            cached_result = await self.cache.get(cache_key)
            
            if cached_result:
                # Update metadata to indicate cache hit
                cached_result.metadata = cached_result.metadata or {}
                cached_result.metadata['from_cache'] = True
                cached_result.metadata['cache_hit'] = True
                cached_result.metadata['cache_retrieval_time'] = time.time() - start_time
                return cached_result
        
        # No cache hit, perform actual translation
        try:
            result = await self.translator.translate(request)
            
            # Cache successful result
            if self.cache and result.success:
                cache_key = self._generate_cache_key(request)
                await self.cache.set(cache_key, result)
                
                # Add cache metadata
                result.metadata = result.metadata or {}
                result.metadata['cached'] = True
                result.metadata['cache_miss'] = True
                result.metadata['cache_key'] = cache_key[:16] + "..."
            
            return result
            
        except Exception as e:
            return TranslationResult(
                translated_text=f"Translation failed: {str(e)}",
                source_language=request.source_language or "unknown",
                target_language=request.target_language,
                success=False,
                confidence=0.0,
                processing_time=time.time() - start_time,
                model_used="error"
            )
    
    def _generate_cache_key(self, request: TranslationRequest) -> str:
        """Generate cache key from request."""
        key_parts = [
            request.text,
            request.target_language,
            str(request.preserve_formatting),
            request.quality_tier or "standard"
        ]
        
        content = ":".join(key_parts)
        return hashlib.sha256(content.encode()).hexdigest()
