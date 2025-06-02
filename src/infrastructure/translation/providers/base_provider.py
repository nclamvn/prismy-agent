"""
Base Translation Provider Interface
Abstract base class for all translation providers
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class ProviderType(Enum):
    """Supported provider types"""
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"
    MOCK = "mock"
    AZURE = "azure"  # Future
    DEEPL = "deepl"  # Future
    AWS = "aws"      # Future


@dataclass
class TranslationRequest:
    """Translation request data structure"""
    text: str
    source_language: str
    target_language: str
    context: Optional[str] = None
    domain: Optional[str] = None  # technical, medical, legal, etc.
    quality_level: str = "standard"  # standard, high, premium


@dataclass
class TranslationResponse:
    """Translation response data structure"""
    translated_text: str
    source_language: str
    target_language: str
    provider: str
    confidence_score: float
    processing_time: float
    cost_estimate: float
    metadata: Dict[str, Any]


@dataclass
class ProviderConfig:
    """Provider configuration"""
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    model: Optional[str] = None
    max_tokens: int = 4000
    timeout: int = 30
    rate_limit: int = 100  # requests per minute
    enabled: bool = True


class BaseTranslationProvider(ABC):
    """
    Abstract base class for all translation providers
    All providers must implement these methods
    """
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.provider_type = self._get_provider_type()
        self._validate_config()
    
    @abstractmethod
    def _get_provider_type(self) -> ProviderType:
        """Return the provider type"""
        pass
    
    @abstractmethod
    def _validate_config(self) -> None:
        """Validate provider configuration"""
        pass
    
    @abstractmethod
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Translate text using this provider
        
        Args:
            request: Translation request with text and parameters
            
        Returns:
            TranslationResponse with translated text and metadata
            
        Raises:
            ProviderError: If translation fails
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Return list of supported language codes"""
        pass
    
    @abstractmethod
    def estimate_cost(self, text: str, source_lang: str, target_lang: str) -> float:
        """Estimate cost for translation in USD"""
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        """Check if provider is healthy and responsive"""
        pass
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get provider information and capabilities"""
        return {
            "type": self.provider_type.value,
            "enabled": self.config.enabled,
            "supported_languages": self.get_supported_languages(),
            "rate_limit": self.config.rate_limit,
            "model": self.config.model
        }


class ProviderError(Exception):
    """Base exception for provider errors"""
    
    def __init__(self, message: str, provider: str, error_code: Optional[str] = None):
        self.message = message
        self.provider = provider
        self.error_code = error_code
        super().__init__(f"[{provider}] {message}")


class RateLimitError(ProviderError):
    """Raised when provider rate limit is exceeded"""
    pass


class AuthenticationError(ProviderError):
    """Raised when provider authentication fails"""
    pass


class UnsupportedLanguageError(ProviderError):
    """Raised when language pair is not supported"""
    pass
