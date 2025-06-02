"""
Test custom exceptions
"""
import pytest
from src.core.exceptions import (
    BaseAppException,
    LLMAPIKeyError,
    TranslationTimeoutError,
    ValidationError
)

class TestCustomExceptions:
    """Test exception functionality"""
    
    def test_base_exception(self):
        """Test base exception"""
        exc = BaseAppException(
            message="Test error",
            error_code="TEST_ERROR",
            details={"key": "value"}
        )
        
        assert exc.message == "Test error"
        assert exc.error_code == "TEST_ERROR"
        assert exc.details == {"key": "value"}
        
        # Test to_dict
        result = exc.to_dict()
        assert result["error"] == "TEST_ERROR"
        assert result["message"] == "Test error"
        assert result["details"] == {"key": "value"}
    
    def test_llm_api_key_error(self):
        """Test LLM API key error"""
        exc = LLMAPIKeyError(
            "API key missing",
            details={"provider": "openai"}
        )
        
        assert exc.error_code == "LLMAPIKeyError"
        assert exc.details["provider"] == "openai"
    
    def test_translation_timeout_error(self):
        """Test translation timeout error"""
        exc = TranslationTimeoutError(
            "Request timed out",
            details={"timeout": 30, "text_length": 5000}
        )
        
        result = exc.to_dict()
        assert result["error"] == "TranslationTimeoutError"
        assert result["details"]["timeout"] == 30
        assert result["details"]["text_length"] == 5000
