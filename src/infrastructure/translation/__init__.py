"""
Translation Infrastructure Package
Complete multi-provider translation system with quality scoring and smart routing
"""

from .providers.base_provider import (
    BaseTranslationProvider, 
    ProviderType, 
    TranslationRequest, 
    TranslationResponse,
    ProviderConfig
)
from .providers.mock_provider import MockTranslationProvider
from .providers.openai_provider import OpenAITranslationProvider
from .providers.google_provider import GoogleTranslationProvider
from .providers.anthropic_provider import AnthropicTranslationProvider
from .provider_manager import ProviderManager, RoutingStrategy
from .quality_scorer import QualityScorer

__all__ = [
    'BaseTranslationProvider', 
    'ProviderType', 
    'TranslationRequest', 
    'TranslationResponse',
    'ProviderConfig',
    'MockTranslationProvider',
    'OpenAITranslationProvider',
    'GoogleTranslationProvider', 
    'AnthropicTranslationProvider',
    'ProviderManager',
    'RoutingStrategy',
    'QualityScorer'
]
