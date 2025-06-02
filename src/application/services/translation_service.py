"""
Translation service with multiple providers
"""
import os
import time
from typing import Optional
from src.config.logging_config import get_logger
from src.core.exceptions import TranslationError

logger = get_logger(__name__)

class TranslationResult:
    def __init__(self, translated_text: str, source_lang: str, target_lang: str, 
                 confidence: float = 0.95, processing_time: float = 0.0):
        self.translated_text = translated_text
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.confidence = confidence
        self.processing_time = processing_time

class TranslationService:
    def __init__(self, enable_cache: bool = True):
        self.enable_cache = enable_cache
        self.provider = os.getenv("LLM_PROVIDER", "google")
        self.openai_key = os.getenv("OPENAI_API_KEY", "")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        logger.info(f"TranslationService initialized with provider: {self.provider}")
        
    def is_configured(self) -> bool:
        """Check if service is properly configured"""
        if self.provider == "google":
            return True
        elif self.provider == "openai":
            return bool(self.openai_key)
        elif self.provider == "anthropic":
            return bool(self.anthropic_key)
        return False
    
    async def translate_text(self, text: str, source_lang: str, target_lang: str, 
                           style: Optional[str] = None) -> TranslationResult:
        """Translate text using configured provider"""
        start_time = time.time()
        
        try:
            logger.info(f"Translating with {self.provider}: {text[:50]}...")
            
            translated_text = ""
            
            # Use configured provider
            if self.provider == "openai" and self.openai_key:
                from src.infrastructure.llm.providers.openai_provider import OpenAIProvider
                provider = OpenAIProvider()
                translated_text = await provider.translate(text, source_lang, target_lang)
                confidence = 0.95
                
            elif self.provider == "anthropic" and self.anthropic_key:
                from src.infrastructure.llm.providers.anthropic_provider import AnthropicProvider
                provider = AnthropicProvider()
                translated_text = await provider.translate(text, source_lang, target_lang)
                confidence = 0.95
                
            else:
                # Default to Google Translate
                from deep_translator import GoogleTranslator
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                translated_text = translator.translate(text)
                confidence = 0.9
            
            processing_time = time.time() - start_time
            
            logger.info(f"Translation successful: {translated_text[:50]}...")
            
            return TranslationResult(
                translated_text=translated_text,
                source_lang=source_lang,
                target_lang=target_lang,
                confidence=confidence,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            raise TranslationError(f"Translation failed: {str(e)}")
