#!/usr/bin/env python3
"""
Add logging to translation service
"""

content = '''
# At the top of the file, add:
from src.config.logging_config import get_logger
from src.core.exceptions import TranslationError, TranslationAPIError, TranslationTimeoutError

logger = get_logger(__name__)

# In translate_text method, add:
async def translate_text(self, ...):
    logger.info(f"Starting translation: {len(text)} chars, {source_lang} -> {target_lang}")
    try:
        # existing code
        logger.debug("Translation successful")
        return result
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise TranslationAPIError(
            "Translation failed",
            details={"error": str(e), "provider": self.provider}
        )
'''

print("📋 Add these logging statements to TranslationService:")
print(content)
print("\n✅ Logging example created")
