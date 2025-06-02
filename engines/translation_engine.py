import openai
import anthropic
import tiktoken
import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Union
import logging
import time
import re
from dataclasses import dataclass
from langdetect import detect
import json

@dataclass
class TranslationRequest:
    """Data class for translation requests"""
    text: str
    source_lang: str = 'auto'
    target_lang: str = 'vi'
    context: str = ''
    document_type: str = 'general'
    preserve_formatting: bool = True

@dataclass
class TranslationResult:
    """Data class for translation results"""
    original_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    confidence: float
    model_used: str
    processing_time: float
    token_usage: Dict[str, int]
    context_preserved: bool = True

class TranslationEngine:
    """
    Advanced AI Translation Engine với OpenAI và Anthropic
    Xử lý: context-aware translation, technical documents, formulas, tables
    """
    
    def __init__(self, openai_api_key: Optional[str] = None, anthropic_api_key: Optional[str] = None):
        """
        Initialize Translation Engine
        
        Args:
            openai_api_key: OpenAI API key
            anthropic_api_key: Anthropic API key
        """
        self.logger = logging.getLogger(__name__)
        
        # Initialize API clients
        self.openai_client = None
        self.anthropic_client = None
        
        if openai_api_key:
            self.openai_client = openai.OpenAI(api_key=openai_api_key)
        
        if anthropic_api_key:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        
        # Initialize tokenizer for cost estimation
        try:
            self.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")
        except:
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
        # Translation statistics
        self.reset_stats()
        
        # Language mappings
        self.language_codes = {
            'vietnamese': 'vi',
            'english': 'en',
            'chinese': 'zh',
            'japanese': 'ja',
            'korean': 'ko',
            'french': 'fr',
            'german': 'de',
            'spanish': 'es'
        }
        
        # Specialized prompts for different document types
        self.translation_prompts = {
            'general': """Translate the following text to {target_lang}. Maintain the original meaning and style:

{text}""",
            
            'technical': """You are translating a technical document. Preserve technical terms, formulas, and formatting. 
Translate to {target_lang} while keeping:
- Technical terminology accurate
- Mathematical expressions unchanged
- Units and measurements
- Proper nouns when appropriate

Text to translate:
{text}""",
            
            'academic': """Translate this academic/scientific text to {target_lang}. Maintain:
- Academic tone and formality
- Technical terminology
- Citations and references format
- Mathematical formulas and equations

{text}""",
            
            'table': """Translate this table content to {target_lang}. Rules:
- Preserve table structure exactly
- Translate headers and data appropriately  
- Keep numerical values unchanged
- Maintain alignment and formatting

{text}""",
            
            'formula': """Translate text containing mathematical formulas to {target_lang}. Rules:
- Keep mathematical symbols and equations EXACTLY as they are
- Translate only the descriptive text
- Preserve variable names and notation
- Maintain mathematical formatting

{text}"""
        }
    
    def reset_stats(self):
        """Reset translation statistics"""
        self.stats = {
            'total_requests': 0,
            'successful_translations': 0,
            'failed_translations': 0,
            'total_tokens_used': 0,
            'total_cost_estimate': 0.0,
            'avg_processing_time': 0.0,
            'languages_processed': set(),
            'model_usage': {}
        }
    
    def detect_language(self, text: str) -> str:
        """
        Detect source language of text
        
        Args:
            text: Input text
            
        Returns:
            Detected language code
        """
        try:
            # Clean text for better detection
            clean_text = re.sub(r'[^\w\s]', ' ', text)
            clean_text = ' '.join(clean_text.split()[:100])  # Use first 100 words
            
            if len(clean_text.strip()) < 10:
                return 'unknown'
            
            detected = detect(clean_text)
            return detected
            
        except Exception as e:
            self.logger.warning(f"Language detection failed: {e}")
            return 'unknown'
    
    def estimate_cost(self, text: str, model: str = 'gpt-3.5-turbo') -> Dict[str, Any]:
        """
        Estimate translation cost
        
        Args:
            text: Input text
            model: Model to use for estimation
            
        Returns:
            Cost estimation details
        """
        try:
            # Count tokens
            input_tokens = len(self.tokenizer.encode(text))
            
            # Estimate output tokens (usually 1.2-1.5x input for translation)
            estimated_output_tokens = int(input_tokens * 1.3)
            
            # Pricing (per 1K tokens, as of 2024)
            pricing = {
                'gpt-3.5-turbo': {'input': 0.0005, 'output': 0.0015},
                'gpt-4': {'input': 0.03, 'output': 0.06},
                'gpt-4-turbo': {'input': 0.01, 'output': 0.03},
                'claude-3-haiku': {'input': 0.00025, 'output': 0.00125},
                'claude-3-sonnet': {'input': 0.003, 'output': 0.015},
                'claude-3-opus': {'input': 0.015, 'output': 0.075}
            }
            
            if model not in pricing:
                model = 'gpt-3.5-turbo'
            
            input_cost = (input_tokens / 1000) * pricing[model]['input']
            output_cost = (estimated_output_tokens / 1000) * pricing[model]['output']
            total_cost = input_cost + output_cost
            
            return {
                'model': model,
                'input_tokens': input_tokens,
                'estimated_output_tokens': estimated_output_tokens,
                'input_cost': input_cost,
                'output_cost': output_cost,
                'total_estimated_cost': total_cost
            }
            
        except Exception as e:
            self.logger.warning(f"Cost estimation failed: {e}")
            return {'total_estimated_cost': 0}
    
    def chunk_text(self, text: str, max_tokens: int = 3000) -> List[str]:
        """
        Split text into chunks for processing
        
        Args:
            text: Input text
            max_tokens: Maximum tokens per chunk
            
        Returns:
            List of text chunks
        """
        try:
            # Try to split by paragraphs first
            paragraphs = text.split('\n\n')
            chunks = []
            current_chunk = ""
            
            for paragraph in paragraphs:
                # Check if adding this paragraph exceeds limit
                test_chunk = current_chunk + '\n\n' + paragraph if current_chunk else paragraph
                token_count = len(self.tokenizer.encode(test_chunk))
                
                if token_count > max_tokens and current_chunk:
                    # Save current chunk and start new one
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                else:
                    current_chunk = test_chunk
            
            # Add remaining chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # If chunks are still too long, split by sentences
            final_chunks = []
            for chunk in chunks:
                if len(self.tokenizer.encode(chunk)) > max_tokens:
                    sentence_chunks = self._split_by_sentences(chunk, max_tokens)
                    final_chunks.extend(sentence_chunks)
                else:
                    final_chunks.append(chunk)
            
            return final_chunks
            
        except Exception as e:
            self.logger.error(f"Text chunking failed: {e}")
            return [text]  # Return original text as single chunk
    
    def _split_by_sentences(self, text: str, max_tokens: int) -> List[str]:
        """Split text by sentences when paragraph splitting isn't enough"""
        sentences = re.split(r'[.!?]+\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            test_chunk = current_chunk + '. ' + sentence if current_chunk else sentence
            if len(self.tokenizer.encode(test_chunk)) > max_tokens and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk = test_chunk
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks
    
    async def translate_with_openai(self, request: TranslationRequest, model: str = 'gpt-3.5-turbo') -> TranslationResult:
        """
        Translate using OpenAI API
        
        Args:
            request: Translation request
            model: OpenAI model to use
            
        Returns:
            Translation result
        """
        try:
            start_time = time.time()
            
            if not self.openai_client:
                raise ValueError("OpenAI client not initialized")
            
            # Select appropriate prompt
            prompt_template = self.translation_prompts.get(request.document_type, self.translation_prompts['general'])
            
            # Prepare system message
            system_message = f"You are a professional translator specializing in {request.document_type} documents. Translate accurately while preserving meaning, context, and formatting."
            
            # Add context if provided
            context_info = f"\nContext: {request.context}" if request.context else ""
            
            # Format prompt
            user_message = prompt_template.format(
                target_lang=request.target_lang,
                text=request.text
            ) + context_info
            
            # Make API call
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,  # Low temperature for consistent translations
                max_tokens=4000
            )
            
            translated_text = response.choices[0].message.content.strip()
            processing_time = time.time() - start_time
            
            # Calculate confidence based on response quality
            confidence = self._calculate_confidence(request.text, translated_text, model)
            
            return TranslationResult(
                original_text=request.text,
                translated_text=translated_text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                confidence=confidence,
                model_used=model,
                processing_time=processing_time,
                token_usage={
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(f"OpenAI translation failed: {e}")
            raise
    
    async def translate_with_claude(self, request: TranslationRequest, model: str = 'claude-3-haiku-20240307') -> TranslationResult:
        """
        Translate using Anthropic Claude API
        
        Args:
            request: Translation request
            model: Claude model to use
            
        Returns:
            Translation result
        """
        try:
            start_time = time.time()
            
            if not self.anthropic_client:
                raise ValueError("Anthropic client not initialized")
            
            # Select appropriate prompt
            prompt_template = self.translation_prompts.get(request.document_type, self.translation_prompts['general'])
            
            # Add context if provided
            context_info = f"\nAdditional context: {request.context}" if request.context else ""
            
            # Format prompt
            user_message = prompt_template.format(
                target_lang=request.target_lang,
                text=request.text
            ) + context_info
            
            # Make API call
            response = await asyncio.to_thread(
                self.anthropic_client.messages.create,
                model=model,
                max_tokens=4000,
                temperature=0.1,
                system=f"You are a professional translator specializing in {request.document_type} documents.",
                messages=[{"role": "user", "content": user_message}]
            )
            
            translated_text = response.content[0].text.strip()
            processing_time = time.time() - start_time
            
            # Calculate confidence
            confidence = self._calculate_confidence(request.text, translated_text, model)
            
            return TranslationResult(
                original_text=request.text,
                translated_text=translated_text,
                source_lang=request.source_lang,
                target_lang=request.target_lang,
                confidence=confidence,
                model_used=model,
                processing_time=processing_time,
                token_usage={
                    'input_tokens': response.usage.input_tokens,
                    'output_tokens': response.usage.output_tokens,
                    'total_tokens': response.usage.input_tokens + response.usage.output_tokens
                }
            )
            
        except Exception as e:
            self.logger.error(f"Claude translation failed: {e}")
            raise
    
    def _calculate_confidence(self, original: str, translated: str, model: str) -> float:
        """
        Calculate translation confidence score
        
        Args:
            original: Original text
            translated: Translated text
            model: Model used
            
        Returns:
            Confidence score (0-1)
        """
        try:
            base_confidence = 0.7  # Base confidence
            
            # Length ratio check
            len_ratio = len(translated) / len(original) if original else 0
            if 0.5 <= len_ratio <= 2.0:  # Reasonable length ratio
                base_confidence += 0.1
            
            # Model-based confidence adjustment
            model_confidence = {
                'gpt-4': 0.95,
                'gpt-3.5-turbo': 0.85,
                'claude-3-opus': 0.95,
                'claude-3-sonnet': 0.90,
                'claude-3-haiku': 0.80
            }
            
            return min(model_confidence.get(model, base_confidence), 1.0)
            
        except Exception:
            return 0.7
    
    async def translate_document(self, text: str, source_lang: str = 'auto', 
                               target_lang: str = 'vi', document_type: str = 'general',
                               model_preference: str = 'openai', context: str = '') -> Dict[str, Any]:
        """
        Complete document translation pipeline
        
        Args:
            text: Text to translate
            source_lang: Source language (auto-detect if 'auto')
            target_lang: Target language
            document_type: Type of document
            model_preference: Preferred AI model ('openai' or 'claude')
            context: Additional context for translation
            
        Returns:
            Complete translation results
        """
        try:
            start_time = time.time()
            self.stats['total_requests'] += 1
            
            # Auto-detect source language if needed
            if source_lang == 'auto':
                detected_lang = self.detect_language(text)
                source_lang = detected_lang if detected_lang != 'unknown' else 'en'
            
            # Skip translation if source and target are the same
            if source_lang == target_lang:
                return {
                    'original_text': text,
                    'translated_text': text,
                    'source_lang': source_lang,
                    'target_lang': target_lang,
                    'skipped': True,
                    'reason': 'Same source and target language'
                }
            
            # Split text into chunks if too long
            chunks = self.chunk_text(text)
            
            # Translate each chunk
            translated_chunks = []
            total_tokens = 0
            
            for i, chunk in enumerate(chunks):
                request = TranslationRequest(
                    text=chunk,
                    source_lang=source_lang,
                    target_lang=target_lang,
                    context=context,
                    document_type=document_type
                )
                
                # Choose model and translate
                try:
                    if model_preference == 'claude' and self.anthropic_client:
                        result = await self.translate_with_claude(request)
                    elif model_preference == 'openai' and self.openai_client:
                        result = await self.translate_with_openai(request)
                    else:
                        # Fallback to available client
                        if self.openai_client:
                            result = await self.translate_with_openai(request)
                        elif self.anthropic_client:
                            result = await self.translate_with_claude(request)
                        else:
                            raise ValueError("No AI client available")
                    
                    translated_chunks.append(result)
                    total_tokens += result.token_usage['total_tokens']
                    
                except Exception as e:
                    self.logger.error(f"Translation failed for chunk {i+1}: {e}")
                    self.stats['failed_translations'] += 1
                    raise
            
            # Combine translated chunks
            combined_translation = '\n\n'.join([chunk.translated_text for chunk in translated_chunks])
            
            # Calculate overall statistics
            avg_confidence = sum(chunk.confidence for chunk in translated_chunks) / len(translated_chunks)
            processing_time = time.time() - start_time
            
            # Update statistics
            self.stats['successful_translations'] += 1
            self.stats['total_tokens_used'] += total_tokens
            self.stats['languages_processed'].add(source_lang)
            self.stats['languages_processed'].add(target_lang)
            
            model_used = translated_chunks[0].model_used if translated_chunks else 'unknown'
            self.stats['model_usage'][model_used] = self.stats['model_usage'].get(model_used, 0) + 1
            
            return {
                'original_text': text,
                'translated_text': combined_translation,
                'source_lang': source_lang,
                'target_lang': target_lang,
                'document_type': document_type,
                'chunks_processed': len(chunks),
                'average_confidence': avg_confidence,
                'total_tokens': total_tokens,
                'processing_time': processing_time,
                'model_used': model_used,
                'chunk_results': translated_chunks
            }
            
        except Exception as e:
            self.logger.error(f"Document translation failed: {e}")
            self.stats['failed_translations'] += 1
            raise
    
    def translate_table_data(self, table_data: List[Dict[str, Any]], target_lang: str = 'vi') -> List[Dict[str, Any]]:
        """
        Translate table data while preserving structure
        
        Args:
            table_data: List of table dictionaries
            target_lang: Target language
            
        Returns:
            Translated table data
        """
        try:
            translated_tables = []
            
            for table in table_data:
                # Translate headers
                original_headers = table.get('headers', [])
                translated_headers = []
                
                for header in original_headers:
                    if header and header.strip():
                        # Use sync translation for headers (usually short)
                        header_result = asyncio.run(self.translate_document(
                            header, 
                            target_lang=target_lang,
                            document_type='table'
                        ))
                        translated_headers.append(header_result['translated_text'])
                    else:
                        translated_headers.append(header)
                
                # Translate data rows
                original_data = table.get('data', [])
                translated_data = []
                
                for row in original_data:
                    translated_row = []
                    for cell in row:
                        if cell and str(cell).strip() and not self._is_numeric(str(cell)):
                            # Translate text cells
                            cell_result = asyncio.run(self.translate_document(
                                str(cell),
                                target_lang=target_lang,
                                document_type='table'
                            ))
                            translated_row.append(cell_result['translated_text'])
                        else:
                            # Keep numeric values and empty cells as-is
                            translated_row.append(cell)
                    translated_data.append(translated_row)
                
                # Create translated table
                translated_table = table.copy()
                translated_table['headers'] = translated_headers
                translated_table['data'] = translated_data
                translated_table['translation_applied'] = True
                translated_table['target_language'] = target_lang
                
                translated_tables.append(translated_table)
            
            return translated_tables
            
        except Exception as e:
            self.logger.error(f"Table translation failed: {e}")
            return table_data  # Return original on failure
    
    def _is_numeric(self, text: str) -> bool:
        """Check if text is numeric (including formatted numbers)"""
        try:
            # Remove common formatting
            clean_text = re.sub(r'[,\s%$]', '', text)
            float(clean_text)
            return True
        except ValueError:
            return False
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get current processing statistics"""
        stats = self.stats.copy()
        stats['languages_processed'] = list(stats['languages_processed'])
        return stats
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported language mappings"""
        return self.language_codes.copy()
