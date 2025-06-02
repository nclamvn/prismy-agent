"""
Anthropic Translation Provider with Claude 4 models
"""
import os
from anthropic import Anthropic
from src.config.logging_config import get_logger

logger = get_logger(__name__)

class AnthropicProvider:
    def __init__(self):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("Anthropic API key not found")
        self.client = Anthropic(api_key=api_key)
        
    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate using Claude 4 models"""
        lang_map = {
            "en": "English", "vi": "Vietnamese", "zh": "Chinese",
            "ja": "Japanese", "ko": "Korean", "es": "Spanish",
            "fr": "French", "de": "German"
        }
        
        prompt = f"""Translate the following text from {lang_map.get(source_lang, source_lang)} to {lang_map.get(target_lang, target_lang)}.
Only return the translated text, nothing else.

Text: {text}"""
        
        # Claude 4 models (May 2025 release)
        models = [
            "claude-opus-4-20250514",       # Claude Opus 4 (most powerful)
            "claude-sonnet-4-20250514",     # Claude Sonnet 4 (balanced)
            "claude-3-5-sonnet-20241022",   # Claude 3.5 Sonnet (fallback)
            "claude-3-haiku-20240307",      # Claude 3 Haiku (fastest/cheapest)
        ]
        
        for model in models:
            try:
                logger.info(f"Trying Anthropic model: {model}")
                
                response = self.client.messages.create(
                    model=model,
                    max_tokens=2000,
                    temperature=0.3,
                    system="You are a professional translator. Provide accurate and natural translations that sound native in the target language.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                logger.info(f"Success with model: {model}")
                return response.content[0].text.strip()
                
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}")
                if "not_found_error" not in str(e):
                    raise
                continue
        
        raise Exception("No available Anthropic models could complete the translation")
