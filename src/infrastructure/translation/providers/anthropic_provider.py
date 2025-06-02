"""
Anthropic Claude Translation Provider
Claude models powered translation with advanced reasoning
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


class AnthropicTranslationProvider(BaseTranslationProvider):
    """Anthropic Claude-powered translation provider"""
    
    # Supported Claude models
    SUPPORTED_MODELS = {
        "claude-3-opus-20240229": {
            "cost_per_token_input": 0.000015,   # $15 per 1M input tokens
            "cost_per_token_output": 0.000075,  # $75 per 1M output tokens  
            "max_tokens": 200000,
            "quality": "premium"
        },
        "claude-3-sonnet-20240229": {
            "cost_per_token_input": 0.000003,   # $3 per 1M input tokens
            "cost_per_token_output": 0.000015,  # $15 per 1M output tokens
            "max_tokens": 200000,
            "quality": "high"
        },
        "claude-3-haiku-20240307": {
            "cost_per_token_input": 0.00000025, # $0.25 per 1M input tokens
            "cost_per_token_output": 0.00000125,# $1.25 per 1M output tokens
            "max_tokens": 200000,
            "quality": "standard"
        }
    }
    
    # Language support (Claude supports many languages with high quality)
    LANGUAGE_MAPPING = {
        "en": "English",
        "vi": "Vietnamese", 
        "fr": "French",
        "es": "Spanish",
        "de": "German",
        "ja": "Japanese",
        "ko": "Korean",
        "zh": "Chinese (Simplified)",
        "zh-tw": "Chinese (Traditional)",
        "ru": "Russian",
        "it": "Italian",
        "pt": "Portuguese",
        "ar": "Arabic",
        "hi": "Hindi",
        "th": "Thai",
        "tr": "Turkish",
        "pl": "Polish",
        "nl": "Dutch",
        "sv": "Swedish",
        "da": "Danish",
        "no": "Norwegian",
        "fi": "Finnish"
    }
    
    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_url = "https://api.anthropic.com/v1/messages"
        self.session = None
    
    def _get_provider_type(self) -> ProviderType:
        return ProviderType.ANTHROPIC
    
    def _validate_config(self) -> None:
        """Validate Anthropic configuration"""
        # Only validate API key if provider is enabled
        if self.config.enabled and not self.config.api_key:
            raise AuthenticationError("Anthropic API key is required when provider is enabled", "anthropic")
        
        if self.config.model and self.config.model not in self.SUPPORTED_MODELS:
            raise ProviderError(
                f"Unsupported model: {self.config.model}. Supported: {list(self.SUPPORTED_MODELS.keys())}", 
                "anthropic"
            )
        
        # Set default model if not specified
        if not self.config.model:
            self.config.model = "claude-3-haiku-20240307"  # Default to most cost-effective
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not AIOHTTP_AVAILABLE:
            raise ProviderError("aiohttp is required for Anthropic provider", "anthropic")
            
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout),
                headers={
                    "x-api-key": self.config.api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                }
            )
        return self.session
    
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """Translate text using Anthropic Claude models"""
        if not self.config.enabled:
            raise ProviderError("Anthropic provider is disabled", "anthropic")
            
        if not self.config.api_key:
            raise AuthenticationError("Anthropic API key is required for translation", "anthropic")
        
        start_time = time.time()
        
        try:
            # Build prompt
            prompt = self._build_translation_prompt(request)
            
            # Make API call
            session = await self._get_session()
            
            payload = {
                "model": self.config.model,
                "max_tokens": min(self.config.max_tokens, 1000),
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1  # Low temperature for consistent translations
            }
            
            async with session.post(self.api_url, json=payload) as response:
                if response.status == 401:
                    raise AuthenticationError("Invalid Anthropic API key", "anthropic")
                elif response.status == 429:
                    raise RateLimitError("Anthropic rate limit exceeded", "anthropic")
                elif response.status != 200:
                    error_text = await response.text()
                    raise ProviderError(f"Anthropic API error {response.status}: {error_text}", "anthropic")
                
                result = await response.json()
                
                if "error" in result:
                    raise ProviderError(f"Anthropic API error: {result['error']['message']}", "anthropic")
                
                # Extract translation
                content = result["content"][0]["text"].strip()
                translated_text = content
                
                # Calculate costs
                usage = result.get("usage", {})
                input_tokens = usage.get("input_tokens", 0)
                output_tokens = usage.get("output_tokens", 0)
                
                model_pricing = self.SUPPORTED_MODELS[self.config.model]
                cost_estimate = (
                    input_tokens * model_pricing["cost_per_token_input"] +
                    output_tokens * model_pricing["cost_per_token_output"]
                )
                
                processing_time = time.time() - start_time
                
                return TranslationResponse(
                    translated_text=translated_text,
                    source_language=request.source_language,
                    target_language=request.target_language,
                    provider="anthropic",
                    confidence_score=0.93,  # Claude models are very high quality
                    processing_time=processing_time,
                    cost_estimate=cost_estimate,
                    metadata={
                        "model": self.config.model,
                        "input_tokens": input_tokens,
                        "output_tokens": output_tokens,
                        "total_tokens": input_tokens + output_tokens,
                        "quality_level": request.quality_level,
                        "context_provided": bool(request.context),
                        "reasoning_capable": True
                    }
                )
                
        except (AuthenticationError, RateLimitError, ProviderError):
            raise
        except Exception as e:
            raise ProviderError(f"Unexpected error: {str(e)}", "anthropic")
    
    def _build_translation_prompt(self, request: TranslationRequest) -> str:
        """Build optimized translation prompt for Claude"""
        source_lang = self.LANGUAGE_MAPPING.get(request.source_language, request.source_language)
        target_lang = self.LANGUAGE_MAPPING.get(request.target_language, request.target_language)
        
        prompt = f"Please translate the following text from {source_lang} to {target_lang}."
        
        # Add quality level instructions
        if request.quality_level == "premium":
            prompt += " Focus on preserving nuanced meaning, cultural context, idiomatic expressions, and ensuring the translation flows naturally in the target language."
        elif request.quality_level == "high":
            prompt += " Ensure accuracy, natural expression, and appropriate tone."
        
        # Add domain context
        if request.domain:
            prompt += f" This is {request.domain} content, so please use appropriate technical terminology and style conventions."
        
        # Add additional context
        if request.context:
            prompt += f" Additional context: {request.context}"
        
        prompt += f"\n\nText to translate:\n{request.text}\n\nPlease provide only the translation without any additional explanation or commentary."
        
        return prompt
    
    def get_supported_languages(self) -> List[str]:
        """Return supported language codes"""
        return list(self.LANGUAGE_MAPPING.keys())
    
    def estimate_cost(self, text: str, source_lang: str, target_lang: str) -> float:
        """Estimate translation cost based on text length"""
        # Rough estimation: 1 char ≈ 0.3 tokens for input, output usually similar length
        estimated_input_tokens = len(text) * 0.3 + 50  # Add prompt overhead
        estimated_output_tokens = len(text) * 0.3  # Assume similar length output
        
        model_pricing = self.SUPPORTED_MODELS[self.config.model]
        
        return (
            estimated_input_tokens * model_pricing["cost_per_token_input"] +
            estimated_output_tokens * model_pricing["cost_per_token_output"]
        )
    
    def health_check(self) -> bool:
        """Check Anthropic API health"""
        try:
            # Return False if disabled or no API key
            if not self.config.enabled or not self.config.api_key:
                return False
            return True
        except:
            return False
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get Anthropic provider information"""
        info = super().get_provider_info()
        info.update({
            "description": "Anthropic Claude-powered translation with advanced reasoning",
            "models": list(self.SUPPORTED_MODELS.keys()),
            "current_model": self.config.model,
            "cost_per_input_token": self.SUPPORTED_MODELS.get(self.config.model, {}).get("cost_per_token_input", 0),
            "cost_per_output_token": self.SUPPORTED_MODELS.get(self.config.model, {}).get("cost_per_token_output", 0),
            "max_text_length": self.SUPPORTED_MODELS.get(self.config.model, {}).get("max_tokens", 200000),
            "features": ["advanced_reasoning", "context_aware", "cultural_nuance", "domain_expertise", "high_quality"],
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
