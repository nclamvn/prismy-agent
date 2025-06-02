"""
LLM Service - Fixed for Railway
"""
import os
import openai
from anthropic import Anthropic
from typing import Optional

class LLMService:
    def __init__(self):
        # Get API keys
        openai_key = os.getenv("OPENAI_API_KEY", "")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        
        # Initialize clients WITHOUT proxies parameter
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
        else:
            self.openai_client = None
            
        if anthropic_key:
            self.anthropic_client = Anthropic(api_key=anthropic_key)
        else:
            self.anthropic_client = None
        
        self.provider = os.getenv("LLM_PROVIDER", "openai")
    
    def get_completion(self, prompt: str, **kwargs):
        """Get completion from LLM"""
        if self.provider == "openai" and self.openai_client:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        elif self.provider == "anthropic" and self.anthropic_client:
            response = self.anthropic_client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                **kwargs
            )
            return response.content[0].text
        else:
            return "LLM service not configured"

# Singleton instance
_llm_service_instance = None

def get_llm_service():
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance
