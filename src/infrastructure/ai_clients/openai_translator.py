"""OpenAI-based translation service implementation."""

import openai
import time
import hashlib
from typing import List, Optional, Dict, Any
from datetime import datetime

from src.core.interfaces.translation import TranslatorInterface
from src.core.entities.translation import (
    TranslationRequest,
    TranslationResult, 
    ChunkResult,
    ProcessingConfig
)


class OpenAITranslator(TranslatorInterface):
    """OpenAI-based translator implementation."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        
    async def translate(self, request: TranslationRequest) -> TranslationResult:
        """Translate text using OpenAI API."""
        start_time = time.time()
        
        try:
            # Language mapping
            lang_names = {
                'vi': 'Vietnamese', 'en': 'English', 'zh': 'Chinese',
                'ja': 'Japanese', 'fr': 'French', 'de': 'German',
                'es': 'Spanish', 'ko': 'Korean'
            }
            
            target_language = lang_names.get(request.target_language, request.target_language)
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are a professional translator. Translate the following text to {target_language}. Preserve formatting, meaning, and style exactly."
                    },
                    {
                        "role": "user", 
                        "content": request.text
                    }
                ],
                max_tokens=4000,
                temperature=0.1
            )
            
            processing_time = time.time() - start_time
            
            return TranslationResult(
                translated_text=response.choices[0].message.content.strip(),
                source_language=request.source_language or 'auto-detected',
                target_language=target_language,
                confidence=0.95,
                processing_time=processing_time,
                tokens_used=response.usage.total_tokens,
                model_used=self.model
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return TranslationResult(
                translated_text=f"Translation error: {str(e)}",
                source_language=request.source_language or 'unknown',
                target_language=request.target_language,
                confidence=0.0,
                processing_time=processing_time,
                model_used=self.model,
                metadata={"error": str(e)}
            )
    
    async def translate_chunks(self, chunks: List[str], config: ProcessingConfig) -> List[ChunkResult]:
        """Translate multiple text chunks."""
        results = []
        
        for i, chunk in enumerate(chunks):
            start_time = time.time()
            
            try:
                request = TranslationRequest(
                    text=chunk,
                    source_language=None,
                    target_language=config.target_lang
                )
                
                result = await self.translate(request)
                
                chunk_result = ChunkResult(
                    chunk_id=i,
                    original_content=chunk,
                    translated_content=result.translated_text,
                    processing_time=result.processing_time,
                    tokens_used=result.tokens_used,
                    confidence=result.confidence
                )
                
                results.append(chunk_result)
                
                # Rate limiting
                time.sleep(0.5)
                
            except Exception as e:
                error_result = ChunkResult(
                    chunk_id=i,
                    original_content=chunk,
                    translated_content=f"Error: {str(e)}",
                    processing_time=time.time() - start_time,
                    tokens_used=0,
                    confidence=0.0,
                    error=str(e)
                )
                results.append(error_result)
        
        return results
