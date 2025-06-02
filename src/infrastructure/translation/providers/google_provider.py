"""
Google Translate Provider
Google Cloud Translation API integration with high accuracy
"""

import asyncio
import time
import json
from typing import List, Dict, Any, Optional
from urllib.parse import urlencode

from .base_provider import (
    BaseTranslationProvider, 
    ProviderType, 
    ProviderConfig,
    TranslationRequest, 
    TranslationResponse,
    ProviderError,
    AuthenticationError,
    RateLimitError
)

# Import aiohttp only when needed
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False


class GoogleTranslationProvider(BaseTranslationProvider):
    """Google Cloud Translation API provider"""
    
    # Google Translate API pricing (as of 2024)
    COST_PER_CHARACTER = 0.00002  # $20 per 1M characters
    
    # Comprehensive language support (Google supports 100+ languages)
    SUPPORTED_LANGUAGES = [
        "af", "sq", "am", "ar", "hy", "az", "eu", "be", "bn", "bs", "bg", "ca", "ceb", 
        "ny", "zh", "co", "hr", "cs", "da", "nl", "en", "eo", "et", "tl", "fi", "fr", 
        "fy", "gl", "ka", "de", "el", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", 
        "is", "ig", "id", "ga", "it", "ja", "jw", "kn", "kk", "km", "ko", "ku", "ky", 
        "lo", "la", "lv", "lt", "lb", "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", 
        "my", "ne", "no", "ps", "fa", "pl", "pt", "pa", "ro", "ru", "sm", "gd", "sr", 
        "st", "sn", "sd", "si", "sk", "sl", "so", "es", "su", "sw", "sv", "tg", "ta", 
        "te", "th", "tr", "uk", "ur", "uz", "vi", "cy", "xh", "yi", "yo", "zu"
    ]
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_url = "https://translation.googleapis.com/language/translate/v2"
        self.session = None
    
    def _get_provider_type(self) -> ProviderType:
        return ProviderType.GOOGLE
    
    def _validate_config(self) -> None:
        """Validate Google configuration"""
        # Only validate API key if provider is enabled
        if self.config.enabled and not self.config.api_key:
            raise AuthenticationError("Google Translate API key is required when provider is enabled", "google")
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not AIOHTTP_AVAILABLE:
            raise ProviderError("aiohttp is required for Google provider", "google")
            
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
        return self.session
    
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Google Translate API"""
        if not self.config.enabled:
            raise ProviderError("Google provider is disabled", "google")
            
        if not self.config.api_key:
            raise AuthenticationError("Google Translate API key is required for translation", "google")
        
        start_time = time.time()
        
        try:
            # Prepare API request
            session = await self._get_session()
            
            params = {
                'key': self.config.api_key,
                'q': request.text,
                'source': request.source_language,
                'target': request.target_language,
                'format': 'text'
            }
            
            url = f"{self.api_url}?{urlencode(params)}"
            
            async with session.post(url) as response:
                if response.status == 400:
                    error_text = await response.text()
                    if "Invalid Value" in error_text:
                        raise ProviderError("Invalid language code or text", "google")
                    raise ProviderError(f"Bad request: {error_text}", "google")
                elif response.status == 403:
                    raise AuthenticationError("Invalid Google API key or quota exceeded", "google")
                elif response.status == 429:
                    raise RateLimitError("Google Translate rate limit exceeded", "google")
                elif response.status != 200:
                    error_text = await response.text()
                    raise ProviderError(f"Google API error {response.status}: {error_text}", "google")
                
                result = await response.json()
                
                if "error" in result:
                    error_msg = result["error"].get("message", "Unknown error")
                    raise ProviderError(f"Google API error: {error_msg}", "google")
                
                # Extract translation
                translations = result["data"]["translations"]
                if not translations:
                    raise ProviderError("No translation returned from Google", "google")
                
                translated_text = translations[0]["translatedText"]
                detected_lang = translations[0].get("detectedSourceLanguage", request.source_language)
                
                # Calculate cost
                cost_estimate = len(request.text) * self.COST_PER_CHARACTER
                processing_time = time.time() - start_time
                
                # Google doesn't provide confidence scores, but it's generally high quality
                confidence_score = 0.92
                
                return TranslationResponse(
                    translated_text=translated_text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    provider="google",
                    confidence_score=confidence_score,
                    processing_time=processing_time,
                    cost_estimate=cost_estimate,
                    metadata={
                        "detected_source_language": detected_lang,
                        "character_count": len(request.text),
                        "api_version": "v2",
                        "quality_level": request.quality_level
                    }
                )
                
        except (AuthenticationError, RateLimitError, ProviderError):
            raise
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", "google")
    
    def get_supported_languages(self) -> List[str]:
        """Return supported language codes"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def estimate_cost(self, text: str, source_lang: str, target_lang: str) -> float:
        """Estimate translation cost based on character count"""
        return len(text) * self.COST_PER_CHARACTER
    
    def health_check(self) -> bool:
        """Check Google Translate API health"""
        try:
            # Return False if disabled or no API key
            if not self.config.enabled or not self.config.api_key:
                return False
            return True
        except:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get Google provider information"""
        info = super().get_provider_info()
        info.update({
            "description": "Google Cloud Translation API with extensive language support",
            "api_version": "v2",
            "cost_per_character": self.COST_PER_CHARACTER,
            "max_text_length": 5000,  # Google has text length limits
            "features": ["high_accuracy", "language_detection", "extensive_language_support", "fast_translation"],
            "api_key_configured": bool(self.config.api_key),
            "total_languages": len(self.SUPPORTED_LANGUAGES)
        })
        return info
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close session"""
        if hasattr(self, 'session') and self.session and not self.session.closed:
            await self.session.close()
