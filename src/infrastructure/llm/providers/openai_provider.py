"""
OpenAI Translation Provider
"""
import os
from openai import OpenAI
from src.config.logging_config import get_logger

logger = get_logger(__name__)

class OpenAIProvider:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key not found")
        self.client = OpenAI(api_key=api_key)
        
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate using OpenAI GPT"""
        lang_map = {
            "en": "English", "vi": "Vietnamese", "zh": "Chinese",
            "ja": "Japanese", "ko": "Korean", "es": "Spanish",
            "fr": "French", "de": "German"
        }
        
        prompt = f"""Translate the following text from {lang_map.get(source_lang, source_lang)} to {lang_map.get(target_lang, target_lang)}.
Only return the translated text, nothing else.

Text: {text}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional translator. Provide accurate and natural translations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI translation failed: {e}")
            raise
