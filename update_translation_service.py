#!/usr/bin/env python3
"""
Add error handling and logging to TranslationService
"""

# Read current translation service
with open('src/application/services/translation_service.py', 'r') as f:
    content = f.read()

# Add imports at the beginning
new_imports = """
from src.config.logging_config import get_logger
from src.core.exceptions import (
    TranslationError, TranslationAPIError, TranslationTimeoutError,
    ValidationError, InvalidInputError
)
from src.core.utils.retry import retry
from src.core.utils.monitoring import monitor_performance

logger = get_logger(__name__)
"""

# Find where to insert (after existing imports)
import_end = content.find('logger = logging.getLogger(__name__)')
if import_end != -1:
    # Replace existing logger
    end_line = content.find('\n', import_end)
    content = content[:import_end] + 'logger = get_logger(__name__)' + content[end_line:]
else:
    # Add new imports after first imports block
    import_pos = content.find('from infrastructure.')
    if import_pos != -1:
        import_start = content.rfind('\n', 0, import_pos)
        content = content[:import_start] + '\n' + new_imports + content[import_start:]

# Save updated version
with open('src/application/services/translation_service_updated.py', 'w') as f:
    f.write(content)

print("✅ Created updated TranslationService")
print("📋 Review: src/application/services/translation_service_updated.py")

# Create example of how to update methods
example = '''
# Example method updates:

@monitor_performance()
@retry(max_attempts=3, exceptions=(TranslationAPIError, TranslationTimeoutError))
async def translate_text(
    self,
    text: str,
    source_lang: str,
    target_lang: str,
    ...
) -> TranslationResult:
    """Translate text với error handling và monitoring"""
    
    # Validation
    if not text or not text.strip():
        raise InvalidInputError("Text cannot be empty")
    
    if len(text) > 50000:
        raise InvalidInputError(
            "Text too long",
            details={"length": len(text), "max_length": 50000}
        )
    
    logger.info(
        f"Starting translation: {len(text)} chars, "
        f"{source_lang} -> {target_lang}"
    )
    
    try:
        # Existing translation logic
        result = await self._translate_with_provider(...)
        
        logger.info(f"Translation completed successfully")
        return result
        
    except asyncio.TimeoutError:
        logger.error(f"Translation timeout after {timeout}s")
        raise TranslationTimeoutError(
            f"Translation timed out after {timeout} seconds",
            details={
                "text_length": len(text),
                "timeout": timeout,
                "provider": self.provider
            }
        )
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise TranslationAPIError(
            f"Translation failed: {str(e)}",
            details={
                "provider": self.provider,
                "error_type": type(e).__name__
            }
        )
'''

print("\n📋 Example implementation:")
print(example)
