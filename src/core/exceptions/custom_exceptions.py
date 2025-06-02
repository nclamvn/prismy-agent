"""
Custom exceptions for the application
"""
from typing import Optional, Dict, Any

class BaseAppException(Exception):
    """Base exception for all app exceptions"""
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses"""
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details
        }

# Translation Errors
class TranslationError(BaseAppException):
    """Base translation error"""
    pass

class TranslationAPIError(TranslationError):
    """API call failed"""
    pass

class TranslationTimeoutError(TranslationError):
    """Translation timeout"""
    pass

# LLM Errors
class LLMError(BaseAppException):
    """Base LLM error"""
    pass

class LLMAPIKeyError(LLMError):
    """Invalid or missing API key"""
    pass

class LLMRateLimitError(LLMError):
    """Rate limit exceeded"""
    pass

class LLMTimeoutError(LLMError):
    """LLM request timeout"""
    pass

# Configuration Errors
class ConfigurationError(BaseAppException):
    """Configuration related errors"""
    pass

class MissingConfigError(ConfigurationError):
    """Required config missing"""
    pass

# Validation Errors
class ValidationError(BaseAppException):
    """Input validation errors"""
    pass

class InvalidInputError(ValidationError):
    """Invalid input data"""
    pass

# Content Transformation Errors
class TransformationError(BaseAppException):
    """Content transformation errors"""
    pass

class UnsupportedFormatError(TransformationError):
    """Unsupported content format"""
    pass
