"""In-memory caching implementation."""

import hashlib
import time
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

from src.core.interfaces.translation import CacheInterface
from src.core.entities.translation import TranslationResult


class MemoryCache(CacheInterface):
    """In-memory cache implementation for translations."""
    
    def __init__(self, default_ttl: int = 3600):
        self.default_ttl = default_ttl
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_times: Dict[str, datetime] = {}
        self._max_size = 1000  # Maximum cache entries
    
    async def get(self, key: str) -> Optional[TranslationResult]:
        """Get cached translation result."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if self._is_expired(entry):
            await self._remove(key)
            return None
        
        # Update access time
        self._access_times[key] = datetime.now()
        
        # Reconstruct TranslationResult from cached data
        return TranslationResult(**entry['data'])
    
    async def set(self, key: str, result: TranslationResult, ttl: int = None) -> None:
        """Cache translation result."""
        if ttl is None:
            ttl = self.default_ttl
        
        # Clean up if cache is too large
        if len(self._cache) >= self._max_size:
            await self._cleanup_old_entries()
        
        # Store result
        self._cache[key] = {
            'data': {
                'translated_text': result.translated_text,
                'source_language': result.source_language,
                'target_language': result.target_language,
                'confidence': result.confidence,
                'processing_time': result.processing_time,
                'chunks_processed': result.chunks_processed,
                'tokens_used': result.tokens_used,
                'model_used': result.model_used,
                'metadata': result.metadata,
                'created_at': result.created_at
            },
            'expires_at': datetime.now() + timedelta(seconds=ttl),
            'created_at': datetime.now()
        }
        
        self._access_times[key] = datetime.now()
    
    async def invalidate(self, pattern: str) -> None:
        """Invalidate cache entries matching pattern."""
        keys_to_remove = []
        
        for key in self._cache.keys():
            if pattern in key:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            await self._remove(key)
    
    async def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._access_times.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_entries = len(self._cache)
        expired_entries = sum(1 for entry in self._cache.values() if self._is_expired(entry))
        
        return {
            'total_entries': total_entries,
            'active_entries': total_entries - expired_entries,
            'expired_entries': expired_entries,
            'max_size': self._max_size,
            'hit_rate': getattr(self, '_hits', 0) / max(getattr(self, '_requests', 1), 1),
            'memory_usage_mb': self._estimate_memory_usage()
        }
    
    def _is_expired(self, entry: Dict[str, Any]) -> bool:
        """Check if cache entry is expired."""
        return datetime.now() > entry['expires_at']
    
    async def _remove(self, key: str) -> None:
        """Remove entry from cache."""
        if key in self._cache:
            del self._cache[key]
        if key in self._access_times:
            del self._access_times[key]
    
    async def _cleanup_old_entries(self) -> None:
        """Remove old or expired entries."""
        current_time = datetime.now()
        
        # Remove expired entries first
        expired_keys = [
            key for key, entry in self._cache.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            await self._remove(key)
        
        # If still too large, remove least recently accessed
        if len(self._cache) >= self._max_size:
            # Sort by access time, remove oldest
            sorted_keys = sorted(
                self._access_times.keys(),
                key=lambda k: self._access_times[k]
            )
            
            # Remove oldest 20% of entries
            num_to_remove = max(1, len(sorted_keys) // 5)
            for key in sorted_keys[:num_to_remove]:
                await self._remove(key)
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage in MB."""
        total_chars = 0
        for entry in self._cache.values():
            data = entry['data']
            total_chars += len(str(data.get('translated_text', '')))
            total_chars += len(str(data.get('metadata', {})))
        
        # Rough estimate: 1 char ≈ 1 byte, plus overhead
        return (total_chars * 2) / (1024 * 1024)  # Convert to MB


class SmartCache(MemoryCache):
    """Enhanced cache with smart features."""
    
    def __init__(self, default_ttl: int = 3600):
        super().__init__(default_ttl)
        self._hits = 0
        self._misses = 0
        self._requests = 0
    
    async def get(self, key: str) -> Optional[TranslationResult]:
        """Get with hit/miss tracking."""
        self._requests += 1
        result = await super().get(key)
        
        if result:
            self._hits += 1
        else:
            self._misses += 1
        
        return result
    
    def generate_key(self, text: str, target_lang: str, **kwargs) -> str:
        """Generate optimized cache key."""
        # Include important parameters that affect translation
        key_parts = [
            text,
            target_lang,
            str(kwargs.get('preserve_formatting', True)),
            str(kwargs.get('quality_tier', 'standard'))
        ]
        
        content = ":".join(key_parts)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get detailed performance statistics."""
        base_stats = self.get_stats()
        
        return {
            **base_stats,
            'total_requests': self._requests,
            'cache_hits': self._hits,
            'cache_misses': self._misses,
            'hit_rate_percent': (self._hits / max(self._requests, 1)) * 100
        }
