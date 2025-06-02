"""
Translation endpoints
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional
from src.application.services.translation_service import TranslationService
from src.core.exceptions import TranslationError, ValidationError
from src.config.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize service
translation_service = TranslationService()

class TranslateRequest(BaseModel):
    """Translation request model"""
    text: str = Field(..., min_length=1, max_length=50000)
    source_lang: str = Field(..., pattern="^[a-z]{2}$")
    target_lang: str = Field(..., pattern="^[a-z]{2}$")
    style: Optional[str] = Field(None, pattern="^(formal|casual|technical)$")

class TranslateResponse(BaseModel):
    """Translation response model"""
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float
    processing_time: float

@router.post("/", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """Translate text"""
    try:
        logger.info(f"Translation request: {request.source_lang} -> {request.target_lang}")
        
        # Check if service is configured
        if not translation_service.is_configured():
            raise HTTPException(
                status_code=503,
                detail="Translation service not configured. API key required."
            )
        
        # Translate
        result = await translation_service.translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang,
            style=request.style
        )
        
        return TranslateResponse(
            translated_text=result.translated_text,
            source_lang=result.source_lang,
            target_lang=result.target_lang,
            confidence=result.confidence,
            processing_time=result.processing_time
        )
        
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TranslationError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail="Translation failed")

@router.get("/languages")
async def get_supported_languages():
    """Get supported languages"""
    return {
        "languages": [
            {"code": "en", "name": "English"},
            {"code": "vi", "name": "Vietnamese"},
            {"code": "zh", "name": "Chinese"},
            {"code": "ja", "name": "Japanese"},
            {"code": "ko", "name": "Korean"},
            {"code": "es", "name": "Spanish"},
            {"code": "fr", "name": "French"},
            {"code": "de", "name": "German"}
        ]
    }
