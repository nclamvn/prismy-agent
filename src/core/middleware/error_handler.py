"""
Global error handler middleware
"""
import logging
from typing import Callable, Any
from src.core.exceptions import BaseAppException

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Global error handler"""
    
    @staticmethod
    def handle_error(error: Exception) -> dict:
        """
        Handle different types of errors
        
        Returns:
            Dictionary with error details
        """
        if isinstance(error, BaseAppException):
            # Our custom exceptions
            logger.error(f"{error.error_code}: {error.message}", extra=error.details)
            return error.to_dict()
        
        # Unknown errors
        logger.exception("Unhandled exception occurred")
        return {
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
            "details": {}
        }
    
    @staticmethod
    def wrap_handler(func: Callable) -> Callable:
        """Wrap a handler function with error handling"""
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                return ErrorHandler.handle_error(e)
        
        return wrapper
