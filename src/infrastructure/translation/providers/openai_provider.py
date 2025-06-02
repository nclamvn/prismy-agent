"""
OpenAI Translation Provider
GPT-4 and GPT-3.5 powered translation with context awareness
"""

import asyncio
import time
import json
from typing import List, Dict, Any, Optional

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


class OpenAITranslationProvider(BaseTranslationProvider):
    """OpenAI GPT-powered translation provider"""
    
    # Supported models
    SUPPORTED_MODELS = {
        "gpt-4": {
            "cost_per_token": 0.00003,  # $0.03 per 1K tokens
            "max_tokens": 8192,
            "quality": "premium"
        },
        "gpt-3.5-turbo": {
            "cost_per_token": 0.000002,  # $0.002 per 1K tokens
            "max_tokens": 4096,
            "quality": "standard"
        }
    }
    
    # Language code mapping (OpenAI uses full language names)
    LANGUAGE_MAPPING = {
        "en": "English",
        "vi": "Vietnamese", 
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese",
        "ru": "Russian",
        "it": "Italian",
        "pt": "Portuguese",
        "ar": "Arabic",
        "hi": "Hindi",
        "th": "Thai"
    }
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.session = None
    
    def _get_provider_type(self) -> ProviderType:
        return ProviderType.OPENAI
    
    def _validate_config(self) -> None:
        """Validate OpenAI configuration"""
        # Only validate API key if provider is enabled
        if self.config.enabled and not self.config.api_key:
            raise AuthenticationError("OpenAI API key is required when provider is enabled", "openai")
        
        if self.config.model and self.config.model not in self.SUPPORTED_MODELS:
            raise ProviderError(
                f"Unsupported model: {self.config.model}. Supported: {list(self.SUPPORTED_MODELS.keys())}", 
                "openai"
            )
        
        # Set default model if not specified
        if not self.config.model:
            self.config.model = "gpt-3.5-turbo"
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not AIOHTTP_AVAILABLE:
            raise ProviderError("aiohttp is required for OpenAI provider", "openai")
            
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                headers={
                    "Authorization": f"Bearer {self.config.api_key}",
                    "Content-Type": "application/json"
                }
            )
        return self.session
    
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using OpenAI GPT models"""
        if not self.config.enabled:
            raise ProviderError("OpenAI provider is disabled", "openai")
            
        if not self.config.api_key:
            raise AuthenticationError("OpenAI API key is required for translation", "openai")
        
        start_time = time.time()
        
        try:
            # Build prompt
            prompt = self._build_translation_prompt(request)
            
            # Make API call
            session = await self._get_session()
            
            payload = {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": "You are a professional translator."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": min(self.config.max_tokens, 1000),
                "temperature": 0.1,  # Low temperature for consistent translations
                "top_p": 1.0
            }
            
            async with session.post(self.api_url, json=payload) as response:
                if response.status == 401:
                    raise AuthenticationError("Invalid OpenAI API key", "openai")
                elif response.status == 429:
                    raise RateLimitError("OpenAI rate limit exceeded", "openai")
                elif response.status != 200:
                    error_text = await response.text()
                    raise ProviderError(f"OpenAI API error {response.status}: {error_text}", "openai")
                
                result = await response.json()
                
                if "error" in result:
                    raise ProviderError(f"OpenAI API error: {result['error']['message']}", "openai")
                
                # Extract translation
                translated_text = result["choices"][0]["message"]["content"].strip()
                
                # Calculate costs
                usage = result.get("usage", {})
                total_tokens = usage.get("total_tokens", 0)
                cost_estimate = total_tokens * self.SUPPORTED_MODELS[self.config.model]["cost_per_token"]
                
                processing_time = time.time() - start_time
                
                return TranslationResponse(
                    translated_text=translated_text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    provider="openai",
                    confidence_score=0.9,  # GPT models are generally high confidence
                    processing_time=processing_time,
                    cost_estimate=cost_estimate,
                    metadata={
                        "model": self.config.model,
                        "tokens_used": total_tokens,
                        "prompt_tokens": usage.get("prompt_tokens", 0),
                        "completion_tokens": usage.get("completion_tokens", 0),
                        "quality_level": request.quality_level,
                        "context_provided": bool(request.context)
                    }
                )
                
        except (AuthenticationError, RateLimitError, ProviderError):
            raise
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", "openai")
    
    def _build_translation_prompt(self, request: TranslationRequest) -> str:
        """Build optimized translation prompt for GPT"""
        source_lang = self.LANGUAGE_MAPPING.get(request.source_language, request.source_language)
        target_lang = self.LANGUAGE_MAPPING.get(request.target_language, request.target_language)
        
        prompt = f"Translate the following text from {source_lang} to {target_lang}."
        
        # Add quality level instructions
        if request.quality_level == "premium":
            prompt += " Focus on nuanced meaning, cultural context, and natural flow."
        elif request.quality_level == "high":
            prompt += " Ensure accuracy and natural expression."
        
        # Add domain context
        if request.domain:
            prompt += f" This is {request.domain} content, so use appropriate terminology."
        
        # Add additional context
        if request.context:
            prompt += f" Context: {request.context}"
        
        prompt += f"\n\nText to translate:\n{request.text}\n\nTranslation:"
        
        return prompt
    
    def get_supported_languages(self) -> List[str]:
        """Return supported language codes"""
        return list(self.LANGUAGE_MAPPING.keys())
    
    def estimate_cost(self, text: str, source_lang: str, target_lang: str) -> float:
        """Estimate translation cost based on text length"""
        # Rough estimation: 1 char ≈ 0.25 tokens for English, varies for other languages
        estimated_tokens = len(text) * 0.3  # Conservative estimate
        
        # Add prompt overhead (approximately 50-100 tokens)
        estimated_tokens += 75
        
        return estimated_tokens * self.SUPPORTED_MODELS[self.config.model]["cost_per_token"]
    
    def health_check(self) -> bool:
        """Check OpenAI API health"""
        try:
            # Return False if disabled or no API key
            if not self.config.enabled or not self.config.api_key:
                return False
            return True
        except:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get OpenAI provider information"""
        info = super().get_provider_info()
        info.update({
            "description": "OpenAI GPT-powered translation with context awareness",
            "models": list(self.SUPPORTED_MODELS.keys()),
            "current_model": self.config.model,
            "cost_per_token": self.SUPPORTED_MODELS.get(self.config.model, {}).get("cost_per_token", 0),
            "max_text_length": self.SUPPORTED_MODELS.get(self.config.model, {}).get("max_tokens", 4096),
            "features": ["context_aware", "domain_specific", "quality_levels", "cost_estimation"],
            "api_key_configured": bool(self.config.api_key)
        })
        return info
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - close session"""
        if hasattr(self, 'session') and self.session and not self.session.closed:
            await self.session.close()
