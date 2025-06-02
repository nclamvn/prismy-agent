"""
Input validation utilities
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from src.core.exceptions import ValidationError, InvalidInputError

class TextValidation(BaseModel):
    """Text input validation"""
    text: str = Field(..., min_length=1, max_length=50000)
    language: str = Field(..., pattern="^[a-z]{2}$")
    
    @field_validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise InvalidInputError("Text cannot be empty or whitespace only")
        return v.strip()

class TranslationRequestValidation(BaseModel):
    """Translation request validation"""
    source_text: str = Field(..., min_length=1, max_length=50000)
    source_lang: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")
    target_lang: str = Field(..., pattern="^[a-z]{2}(-[A-Z]{2})?$")
    
    @field_validator('source_lang', 'target_lang')
    def validate_languages(cls, v, info):
        valid_langs = ['en', 'vi', 'zh', 'ja', 'ko', 'es', 'fr', 'de']
        if v.split('-')[0] not in valid_langs:
            raise InvalidInputError(
                f"Unsupported language: {v}",
                details={"field": info.field_name, "valid_languages": valid_langs}
            )
        return v

def validate_api_key(key: str, provider: str) -> bool:
    """Validate API key format"""
    if not key:
        raise InvalidInputError(f"API key for {provider} is empty")
    
    # Basic format validation
    if provider == 'openai' and not key.startswith('sk-'):
        raise InvalidInputError(
            f"Invalid OpenAI API key format",
            details={"expected_prefix": "sk-"}
        )
    
    return True

class ConfigValidation(BaseModel):
    """Configuration validation"""
    openai_api_key: Optional[str] = Field(None, min_length=10)
    anthropic_api_key: Optional[str] = Field(None, min_length=10)
    llm_provider: str = Field("openai", pattern="^(openai|anthropic)$")
    llm_temperature: float = Field(0.7, ge=0.0, le=2.0)
    llm_max_tokens: int = Field(2000, ge=1, le=32000)
    log_level: str = Field("INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    @field_validator('openai_api_key')
    def validate_openai_key(cls, v):
        if v and not v.startswith('sk-'):
            raise ValueError("OpenAI API key must start with 'sk-'")
        return v
