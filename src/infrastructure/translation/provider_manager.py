"""
Provider Manager
Smart routing, load balancing, and fallback management for translation providers
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from .providers.base_provider import (
    BaseTranslationProvider, 
    ProviderType, 
    ProviderConfig,
    TranslationRequest, 
    TranslationResponse,
    ProviderError,
    RateLimitError
)
from .providers.mock_provider import MockTranslationProvider


class RoutingStrategy(Enum):
    """Provider routing strategies"""
    ROUND_ROBIN = "round_robin"
    COST_OPTIMIZED = "cost_optimized"
    QUALITY_FIRST = "quality_first"
    FASTEST_FIRST = "fastest_first"
    FALLBACK_CHAIN = "fallback_chain"


@dataclass
class ProviderStats:
    """Provider performance statistics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    avg_confidence: float = 0.0
    total_cost: float = 0.0
    last_used: Optional[float] = None
    health_status: bool = True


class ProviderManager:
    """
    Manages multiple translation providers with smart routing and fallback
    """
    
    def __init__(self, routing_strategy: RoutingStrategy = RoutingStrategy.FALLBACK_CHAIN):
        self.routing_strategy = routing_strategy
        self.providers: Dict[ProviderType, BaseTranslationProvider] = {}
        self.provider_stats: Dict[ProviderType, ProviderStats] = {}
        self.provider_priority: List[ProviderType] = []
        
        # Initialize with mock provider
        self._register_mock_provider()
    
    def _register_mock_provider(self):
        """Register mock provider for testing"""
        mock_config = ProviderConfig(enabled=True)
        mock_provider = MockTranslationProvider(mock_config)
        self.register_provider(mock_provider)
        self.provider_priority = [ProviderType.MOCK]
    
    def register_provider(self, provider: BaseTranslationProvider):
        """Register a new translation provider"""
        provider_type = provider.provider_type
        self.providers[provider_type] = provider
        self.provider_stats[provider_type] = ProviderStats()
        
        print(f"✅ Registered provider: {provider_type.value}")
    
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text using the best available provider
        """
        if not self.providers:
            raise ProviderError("No providers registered", "manager")
        
        # Use first available provider for now (simplified)
        for provider_type in self.provider_priority:
            provider = self.providers.get(provider_type)
            if provider and provider.config.enabled:
                try:
                    response = await provider.translate(request)
                    self._update_provider_stats(provider_type, response, success=True)
                    return response
                except Exception as e:
                    self._update_provider_stats(provider_type, None, success=False)
                    continue
        
        raise ProviderError("All providers failed", "manager")
    
    def _update_provider_stats(self, provider_type: ProviderType, 
                             response: Optional[TranslationResponse], 
                             success: bool):
        """Update provider performance statistics"""
        stats = self.provider_stats[provider_type]
        stats.total_requests += 1
        stats.last_used = time.time()
        
        if success and response:
            stats.successful_requests += 1
            stats.avg_response_time = response.processing_time
            stats.avg_confidence = response.confidence_score
            stats.total_cost += response.cost_estimate
        else:
            stats.failed_requests += 1
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get comprehensive provider statistics"""
        stats = {}
        for provider_type, provider_stats in self.provider_stats.items():
            stats[provider_type.value] = {
                "total_requests": provider_stats.total_requests,
                "successful_requests": provider_stats.successful_requests,
                "avg_response_time": provider_stats.avg_response_time,
                "avg_confidence": provider_stats.avg_confidence,
            }
        return stats
    
    def get_available_providers(self) -> List[str]:
        """Get list of available provider types"""
        return [p.value for p in self.providers.keys() if self.providers[p].config.enabled]
