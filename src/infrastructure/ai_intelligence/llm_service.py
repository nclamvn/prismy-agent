"""
Production LLM Service for PRISM Platform
Supports OpenAI and Anthropic APIs
"""

import os
from typing import Dict, List, Any, Optional, Union
from enum import Enum
import openai
import anthropic
from dotenv import load_dotenv
import json
import logging

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMService:
    """
    Unified LLM Service for content enhancement
    """
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        
        # Initialize clients
        self.openai_client = None
        self.anthropic_client = None
        
        # Setup OpenAI
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            self.openai_client = openai.OpenAI(api_key=openai_key)
            logger.info("OpenAI client initialized")
        
        # Setup Anthropic
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        if anthropic_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            logger.info("Anthropic client initialized")
    
    def enhance_podcast_content(
        self,
        content: str,
        section_type: str,
        target_audience: str,
        tone: str = "conversational",
        **kwargs
    ) -> str:
        """
        Enhance content for podcast format
        
        Args:
            content: Raw content to transform
            section_type: intro, main, transition, outro
            target_audience: children, teenagers, adults, professionals
            tone: conversational, professional, educational, entertaining
            
        Returns:
            Enhanced podcast script
        """
        
        prompt = f"""Transform this content into a natural podcast script.

Content: {content}

Requirements:
- Section type: {section_type}
- Target audience: {target_audience}
- Tone: {tone}
- Make it sound natural and conversational
- Add appropriate transitions and hooks
- Include engagement elements (questions, pauses, emphasis)

Output the podcast script directly without any meta-commentary."""

        return self._call_llm(prompt, max_tokens=500)
    
    def enhance_education_content(
        self,
        content: str,
        module_type: str,
        difficulty_level: str,
        learning_style: str = "interactive",
        **kwargs
    ) -> str:
        """
        Enhance content for educational format
        
        Args:
            content: Raw content to transform
            module_type: objective, lesson, exercise, assessment
            difficulty_level: beginner, intermediate, advanced
            learning_style: interactive, visual, practical
            
        Returns:
            Enhanced educational content
        """
        
        prompt = f"""Transform this content into engaging educational material.

Content: {content}

Requirements:
- Module type: {module_type}
- Difficulty level: {difficulty_level}
- Learning style: {learning_style}
- Make it clear and easy to understand
- Add examples and practical applications
- Include engagement elements

Output the educational content directly without any meta-commentary."""

        return self._call_llm(prompt, max_tokens=600)
    
    def _call_llm(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> str:
        """
        Call the appropriate LLM API
        """
        try:
            if self.provider == 'openai' and self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a professional content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content
                
            elif self.provider == 'anthropic' and self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-4-sonnet-20250514",
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.content[0].text
                
            else:
                logger.warning(f"No LLM client available for provider: {self.provider}")
                return self._fallback_enhancement(prompt)
                
        except Exception as e:
            logger.error(f"LLM API error: {e}")
            return self._fallback_enhancement(prompt)
    
    def _fallback_enhancement(self, prompt: str) -> str:
        """
        Fallback when API fails
        """
        # Extract content from prompt
        if "Content:" in prompt:
            content = prompt.split("Content:")[1].split("\n\n")[0].strip()
            return f"[Enhanced] {content}"
        return "[Error: Could not enhance content]"
    
    def batch_enhance(
        self,
        contents: List[str],
        enhancement_type: str,
        **kwargs
    ) -> List[str]:
        """
        Enhance multiple contents
        """
        enhanced = []
        for content in contents:
            if enhancement_type == 'podcast':
                enhanced.append(self.enhance_podcast_content(content, **kwargs))
            elif enhancement_type == 'education':
                enhanced.append(self.enhance_education_content(content, **kwargs))
            else:
                enhanced.append(content)
        return enhanced


# Singleton instance
_llm_service_instance = None

def get_llm_service() -> LLMService:
    """Get singleton LLM service"""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance


# Test function
if __name__ == "__main__":
    service = get_llm_service()
    
    # Test podcast enhancement
    test_content = "AI is transforming how we work and live."
    enhanced = service.enhance_podcast_content(
        test_content,
        section_type="intro",
        target_audience="adults",
        tone="conversational"
    )
    print("Podcast Enhancement:")
    print(enhanced)
    print("\n" + "="*50 + "\n")
    
    # Test education enhancement
    enhanced = service.enhance_education_content(
        test_content,
        module_type="lesson",
        difficulty_level="intermediate",
        learning_style="interactive"
    )
    print("Education Enhancement:")
    print(enhanced)
