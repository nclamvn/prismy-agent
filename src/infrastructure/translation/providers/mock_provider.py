"""
Mock Translation Provider
For testing and development purposes
"""

import asyncio
import time
from typing import List, Dict, Any
from .base_provider import (
    BaseTranslationProvider, 
    ProviderType, 
    ProviderConfig,
    TranslationRequest, 
    TranslationResponse
)


class MockTranslationProvider(BaseTranslationProvider):
    """Mock provider for testing - simulates real translation behavior"""
    
    # Mock translations for testing
    MOCK_TRANSLATIONS = {
        ("en", "vi"): {
            "Hello world": "Xin chào thế giới",
            "How are you?": "Bạn có khỏe không?",
            "Good morning": "Chào buổi sáng",
            "Thank you": "Cảm ơn bạn"
        },
        ("vi", "en"): {
            "Xin chào": "Hello",
            "Cảm ơn": "Thank you",
            "Tốt lành": "Good",
            "Dự án": "Project"
        },
        ("en", "fr"): {
            "Hello world": "Bonjour le monde",
            "How are you?": "Comment allez-vous?",
            "Good morning": "Bonjour",
            "Thank you": "Merci"
        }
    }
    
    def _get_provider_type(self) -> ProviderType:
        return ProviderType.MOCK
    
    def _validate_config(self) -> None:
        """Mock provider doesn't need validation"""
        pass
    
    async def translate(self, request: TranslationRequest) -> TranslationResponse:
        """
        Mock translation with simulated processing time
        """
        start_time = time.time()
        
        # Simulate API call delay
        await asyncio.sleep(0.1 + (len(request.text) * 0.001))
        
        # Get mock translation
        lang_pair = (request.source_language, request.target_language)
        translations = self.MOCK_TRANSLATIONS.get(lang_pair, {})
        
        # Find exact match or create mock translation
        if request.text in translations:
            translated_text = translations[request.text]
            confidence = 0.95
        else:
            # Generate mock translation
            translated_text = f"[MOCK-{request.target_language.upper()}] {request.text}"
            confidence = 0.85
        
        processing_time = time.time() - start_time
        
        return TranslationResponse(
            translated_text=translated_text,
            source_language=request.source_language,
            target_language=request.target_language,
            provider="mock",
            confidence_score=confidence,
            processing_time=processing_time,
            cost_estimate=0.0,  # Mock is free
            metadata={
                "mock_provider": True,
                "character_count": len(request.text),
                "processing_mode": "mock_simulation",
                "quality_level": request.quality_level
            }
        )
    
    def get_supported_languages(self) -> List[str]:
        """Return supported language codes"""
        return ["en", "vi", "fr", "es", "de", "ja", "ko", "zh"]
    
    def estimate_cost(self, text: str, source_lang: str, target_lang: str) -> float:
        """Mock provider is free"""
        return 0.0
    
    def health_check(self) -> bool:
        """Mock provider is always healthy"""
        return True
    
    def get_provider_info(self) -> Dict[str, Any]:
        """Get mock provider information"""
        info = super().get_provider_info()
        info.update({
            "description": "Mock provider for testing and development",
            "cost_per_char": 0.0,
            "max_text_length": 10000,
            "features": ["instant_translation", "free_usage", "testing_mode"]
        })
        return info
