"""
LLM Service with fixed OpenAI client
"""
import os
import openai
from typing import Optional

class LLMService:
    def __init__(self):
        openai_key = os.getenv("OPENAI_API_KEY", "")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY", "")
        provider = os.getenv("LLM_PROVIDER", "openai")
        
        # Fix: Initialize OpenAI client properly
        if openai_key:
            self.openai_client = openai.OpenAI(
                api_key=openai_key,
                # Remove proxies parameter
            )
        else:
            self.openai_client = None
            
        # Rest of initialization...

def get_llm_service():
    return LLMService()
