#!/usr/bin/env python3
"""
Add monitoring to podcast generator
"""

updates = '''
# Add to imports:
from src.config.logging_config import get_logger
from src.core.utils.monitoring import monitor_performance
from src.core.exceptions import TransformationError

logger = get_logger(__name__)

# Update transform method:
@monitor_performance()
async def transform(self, request: TransformationRequest) -> TransformationResponse:
    """Transform với monitoring"""
    logger.info(f"Starting podcast generation for {request.target_audience.value}")
    
    try:
        # Existing logic
        response = await self._original_transform(request)
        logger.info(f"Podcast generated: {response.metadata['section_count']} sections")
        return response
    except Exception as e:
        logger.error(f"Podcast generation failed: {e}")
        raise TransformationError(
            "Failed to generate podcast",
            details={"audience": request.target_audience.value}
        )
'''

print("📋 Add these enhancements to PodcastGenerator:")
print(updates)
print("\n✅ Enhancement guide created")
