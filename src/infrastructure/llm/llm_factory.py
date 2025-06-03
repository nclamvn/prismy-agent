# src/infrastructure/llm/llm_factory.py
from typing import Dict, Optional, Any

class LLMFactory:
    """Factory for creating LLM providers."""
    
    def __init__(self):
        self.providers = {}
        
    def get_provider(self, provider_name: str):
        """Get LLM provider by name."""
        # For now, return a mock provider
        return MockProvider()
        
class MockProvider:
    """Mock provider for testing."""
    
    async def translate(self, text: str, target_language: str, **kwargs):
        """Mock translate method."""
        return f"Translated: {text[:50]}..."
        
    async def generate(self, prompt: str, **kwargs):
        """Mock generate method."""
        return f"Generated response for: {prompt[:50]}..."
