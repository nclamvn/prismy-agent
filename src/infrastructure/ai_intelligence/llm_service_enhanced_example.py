
"""
Enhanced LLM Service with error handling and monitoring
"""
import os
import asyncio
from typing import Optional, List
from enum import Enum

from src.config.logging_config import get_logger
from src.core.exceptions import (
    LLMError, LLMAPIKeyError, LLMRateLimitError, LLMTimeoutError
)
from src.core.utils.retry import retry
from src.core.utils.monitoring import monitor_performance

logger = get_logger(__name__)

class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"

class LLMService:
    """Enhanced LLM Service with error handling"""
    
    def __init__(self, provider: Optional[str] = None):
        self.provider = provider or os.getenv('LLM_PROVIDER', 'openai')
        logger.info(f"Initializing LLM service with provider: {self.provider}")
        
        # Validate API keys
        self._validate_api_keys()
        
        # Initialize clients
        self.openai_client = None
        self.anthropic_client = None
        self._initialize_clients()
    
    def _validate_api_keys(self):
        """Validate required API keys are present"""
        if self.provider == 'openai':
            if not os.getenv('OPENAI_API_KEY'):
                raise LLMAPIKeyError(
                    "OpenAI API key not found",
                    details={"env_var": "OPENAI_API_KEY"}
                )
        elif self.provider == 'anthropic':
            if not os.getenv('ANTHROPIC_API_KEY'):
                raise LLMAPIKeyError(
                    "Anthropic API key not found",
                    details={"env_var": "ANTHROPIC_API_KEY"}
                )
    
    @monitor_performance()
    @retry(max_attempts=3, exceptions=(LLMError, asyncio.TimeoutError))
    async def enhance_content(
        self,
        content: str,
        enhancement_type: str,
        **kwargs
    ) -> str:
        """Enhance content with LLM"""
        logger.debug(f"Enhancing content: type={enhancement_type}, length={len(content)}")
        
        try:
            # Set timeout
            timeout = kwargs.get('timeout', 30)
            
            async with asyncio.timeout(timeout):
                if self.provider == 'openai':
                    result = await self._call_openai(content, enhancement_type, **kwargs)
                elif self.provider == 'anthropic':
                    result = await self._call_anthropic(content, enhancement_type, **kwargs)
                else:
                    raise LLMError(f"Unknown provider: {self.provider}")
            
            logger.info(f"Content enhanced successfully")
            return result
            
        except asyncio.TimeoutError:
            raise LLMTimeoutError(
                f"LLM request timed out after {timeout}s",
                details={"provider": self.provider, "timeout": timeout}
            )
        except Exception as e:
            if "rate_limit" in str(e).lower():
                raise LLMRateLimitError(
                    "Rate limit exceeded",
                    details={"provider": self.provider}
                )
            raise LLMError(f"LLM enhancement failed: {str(e)}")
