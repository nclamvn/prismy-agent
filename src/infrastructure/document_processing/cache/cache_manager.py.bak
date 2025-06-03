# src/infrastructure/document_processing/cache/cache_manager.py

import hashlib
import json
import time
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import numpy as np
from collections import OrderedDict

from src.core.models.document import DocumentChunk, ChunkProcessingResult
from src.core.utils.logger import Logger

logger = Logger(__name__)


@dataclass
class CacheEntry:
    """Single cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    last_accessed: float
    access_count: int
    size_bytes: int
    metadata: Dict[str, Any]
    
    def update_access(self):
        """Update access timestamp and count."""
        self.last_accessed = time.time()
        self.access_count += 1


class CacheManager:
    """
    Advanced caching system for document processing.
    Features:
    - LRU eviction
    - Similarity-based lookup
    - Compression
    - TTL support
    """
    
    def __init__(
        self,
        max_size_mb: int = 500,
        ttl_hours: int = 24,
        similarity_threshold: float = 0.85
    ):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.ttl_seconds = ttl_hours * 3600
        self.similarity_threshold = similarity_threshold
        
        # Different cache stores
        self.chunk_cache = OrderedDict()  # LRU cache for chunks
        self.embedding_cache = {}  # Embeddings for similarity
        self.translation_memory = {}  # Translation pairs
        self.template_cache = {}  # Reusable templates
        
        # Stats
        self.stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0,
            "current_size_bytes": 0
        }
        
    def cache_chunk_result(
        self,
        chunk: DocumentChunk,
        result: ChunkProcessingResult,
        embedding: Optional[np.ndarray] = None
    ) -> str:
        """Cache a processed chunk result."""
        # Generate cache key
        cache_key = self._generate_chunk_key(chunk)
        
        # Prepare cache value
        cache_value = {
            "chunk_content": chunk.content,
            "processed_content": result.processed_content,
            "model_used": result.model_used,
            "metadata": {
                **chunk.metadata,
                **result.metadata
            }
        }
        
        # Calculate size
        size_bytes = len(json.dumps(cache_value).encode())
        
        # Check if we need to evict
        self._evict_if_needed(size_bytes)
        
        # Create cache entry
        entry = CacheEntry(
            key=cache_key,
            value=cache_value,
            created_at=time.time(),
            last_accessed=time.time(),
            access_count=0,
            size_bytes=size_bytes,
            metadata={
                "chunk_type": chunk.metadata.get("type", "general"),
                "output_format": result.metadata.get("output_format", "general")
            }
        )
        
        # Store in cache
        self.chunk_cache[cache_key] = entry
        self.chunk_cache.move_to_end(cache_key)  # Move to end (most recent)
        
        # Store embedding if provided
        if embedding is not None:
            self.embedding_cache[cache_key] = embedding
            
        # Update stats
        self.stats["current_size_bytes"] += size_bytes
        
        logger.debug(f"Cached chunk: {cache_key[:16]}...")
        
        return cache_key
    
    def get_chunk_result(
        self,
        chunk: DocumentChunk,
        check_similar: bool = True
    ) -> Optional[ChunkProcessingResult]:
        """Retrieve cached chunk result."""
        # Try exact match first
        cache_key = self._generate_chunk_key(chunk)
        
        if cache_key in self.chunk_cache:
            entry = self.chunk_cache[cache_key]
            
            # Check TTL
            if self._is_expired(entry):
                self._remove_entry(cache_key)
                return None
                
            # Update access
            entry.update_access()
            self.chunk_cache.move_to_end(cache_key)
            self.stats["hits"] += 1
            
            # Reconstruct result
            return self._reconstruct_result(chunk, entry.value)
        
        # Try similarity-based lookup if enabled
        if check_similar and self.embedding_cache:
            similar_key = self._find_similar_chunk(chunk)
            if similar_key:
                entry = self.chunk_cache[similar_key]
                
                # Check if similar enough
                if self._calculate_similarity(chunk.content, entry.value["chunk_content"]) > self.similarity_threshold:
                    entry.update_access()
                    self.chunk_cache.move_to_end(similar_key)
                    self.stats["hits"] += 1
                    
                    logger.debug(f"Found similar chunk: {similar_key[:16]}...")
                    return self._reconstruct_result(chunk, entry.value)
        
        self.stats["misses"] += 1
        return None
    
    def cache_translation(
        self,
        source_text: str,
        target_text: str,
        source_lang: str,
        target_lang: str,
        model: str
    ):
        """Cache translation pair for reuse."""
        # Create translation key
        trans_key = self._generate_translation_key(source_text, source_lang, target_lang)
        
        # Store translation
        self.translation_memory[trans_key] = {
            "target_text": target_text,
            "model": model,
            "timestamp": time.time()
        }
        
        # Limit translation memory size
        if len(self.translation_memory) > 10000:
            # Remove oldest entries
            sorted_keys = sorted(
                self.translation_memory.keys(),
                key=lambda k: self.translation_memory[k]["timestamp"]
            )
            for key in sorted_keys[:1000]:
                del self.translation_memory[key]
    
    def get_translation(
        self,
        source_text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """Get cached translation if available."""
        trans_key = self._generate_translation_key(source_text, source_lang, target_lang)
        
        if trans_key in self.translation_memory:
            entry = self.translation_memory[trans_key]
            
            # Check age (translations don't expire as quickly)
            if time.time() - entry["timestamp"] < self.ttl_seconds * 7:  # 7x longer TTL
                return entry["target_text"]
                
        return None
    
    def cache_template(
        self,
        template_type: str,
        template_config: Dict[str, Any],
        template_content: str
    ):
        """Cache reusable template."""
        template_key = f"{template_type}_{hashlib.md5(json.dumps(template_config, sort_keys=True).encode()).hexdigest()[:8]}"
        
        self.template_cache[template_key] = {
            "content": template_content,
            "config": template_config,
            "usage_count": 0,
            "created_at": time.time()
        }
    
    def get_template(
        self,
        template_type: str,
        template_config: Dict[str, Any]
    ) -> Optional[str]:
        """Get cached template."""
        template_key = f"{template_type}_{hashlib.md5(json.dumps(template_config, sort_keys=True).encode()).hexdigest()[:8]}"
        
        if template_key in self.template_cache:
            template = self.template_cache[template_key]
            template["usage_count"] += 1
            return template["content"]
            
        return None
    
    def _generate_chunk_key(self, chunk: DocumentChunk) -> str:
        """Generate unique key for chunk."""
        # Include content hash and metadata
        content_hash = hashlib.md5(chunk.content.encode()).hexdigest()
        metadata_str = json.dumps(chunk.metadata, sort_keys=True)
        metadata_hash = hashlib.md5(metadata_str.encode()).hexdigest()[:8]
        
        return f"chunk_{content_hash}_{metadata_hash}"
    
    def _generate_translation_key(
        self,
        source_text: str,
        source_lang: str,
        target_lang: str
    ) -> str:
        """Generate key for translation cache."""
        text_hash = hashlib.md5(source_text.encode()).hexdigest()
        return f"trans_{source_lang}_{target_lang}_{text_hash}"
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        return (time.time() - entry.created_at) > self.ttl_seconds
    
    def _evict_if_needed(self, required_bytes: int):
        """Evict cache entries if needed to make space."""
        while self.stats["current_size_bytes"] + required_bytes > self.max_size_bytes:
            if not self.chunk_cache:
                break
                
            # Remove least recently used
            oldest_key = next(iter(self.chunk_cache))
            self._remove_entry(oldest_key)
            self.stats["evictions"] += 1
    
    def _remove_entry(self, cache_key: str):
        """Remove entry from cache."""
        if cache_key in self.chunk_cache:
            entry = self.chunk_cache[cache_key]
            self.stats["current_size_bytes"] -= entry.size_bytes
            del self.chunk_cache[cache_key]
            
            # Remove from other caches
            if cache_key in self.embedding_cache:
                del self.embedding_cache[cache_key]
    
    def _find_similar_chunk(self, chunk: DocumentChunk) -> Optional[str]:
        """Find similar chunk using embeddings."""
        # This is a placeholder - in real implementation, would use
        # actual embeddings and vector similarity
        
        # For now, use simple text similarity
        chunk_text = chunk.content[:200]  # Compare first 200 chars
        
        best_match = None
        best_similarity = 0.0
        
        for cache_key, entry in self.chunk_cache.items():
            cached_text = entry.value["chunk_content"][:200]
            similarity = self._calculate_similarity(chunk_text, cached_text)
            
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = cache_key
                
        return best_match if best_similarity > self.similarity_threshold else None
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (simplified)."""
        # Simple Jaccard similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
            
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def _reconstruct_result(
        self,
        chunk: DocumentChunk,
        cached_value: Dict[str, Any]
    ) -> ChunkProcessingResult:
        """Reconstruct processing result from cache."""
        return ChunkProcessingResult(
            chunk=chunk,
            processed_content=cached_value["processed_content"],
            model_used=cached_value["model_used"],
            tokens_used=0,  # Not stored in cache
            processing_time=0.0,  # Not relevant for cached
            cost=0.0,  # Already paid
            metadata={
                **cached_value.get("metadata", {}),
                "from_cache": True
            }
        )
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total_requests = self.stats["hits"] + self.stats["misses"]
        
        return {
            **self.stats,
            "hit_rate": (
                self.stats["hits"] / total_requests * 100
                if total_requests > 0 else 0
            ),
            "size_mb": round(self.stats["current_size_bytes"] / (1024 * 1024), 2),
            "chunk_count": len(self.chunk_cache),
            "translation_count": len(self.translation_memory),
            "template_count": len(self.template_cache)
        }
    
    def clear_expired(self):
        """Clear all expired entries."""
        expired_keys = []
        
        for key, entry in self.chunk_cache.items():
            if self._is_expired(entry):
                expired_keys.append(key)
                
        for key in expired_keys:
            self._remove_entry(key)
            
        logger.info(f"Cleared {len(expired_keys)} expired entries")
    
    def optimize_cache(self):
        """Optimize cache by removing low-value entries."""
        # Calculate value score for each entry
        entries_with_scores = []
        
        for key, entry in self.chunk_cache.items():
            # Value score based on access count and recency
            age_hours = (time.time() - entry.last_accessed) / 3600
            score = entry.access_count / (age_hours + 1)
            entries_with_scores.append((key, score))
        
        # Sort by score
        entries_with_scores.sort(key=lambda x: x[1])
        
        # Remove bottom 20% if cache is over 80% full
        if self.stats["current_size_bytes"] > self.max_size_bytes * 0.8:
            remove_count = int(len(entries_with_scores) * 0.2)
            for key, _ in entries_with_scores[:remove_count]:
                self._remove_entry(key)
                self.stats["evictions"] += 1
                
        logger.info(f"Cache optimized, current size: {self.get_cache_stats()['size_mb']} MB")
