# smart_features/smart_retry.py
"""
Smart Retry System with Multiple Models
Intelligent fallback and quality optimization
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass

class RetryReason(Enum):
    LOW_QUALITY = "low_quality"
    API_ERROR = "api_error"
    TIMEOUT = "timeout"
    OPTIMIZATION = "optimization"

class ModelType(Enum):
    CLAUDE = "claude"
    GPT4 = "gpt4"
    GEMINI = "gemini"
    BACKUP = "backup"

@dataclass
class RetryResult:
    """Smart retry attempt result"""
    success: bool
    model_used: ModelType
    quality_score: float
    processing_time: float
    retry_count: int
    retry_reasons: List[RetryReason]
    final_translation: str
    improvement_notes: List[str]

class SmartRetrySystem:
    """
    Intelligent retry system with multiple models and quality optimization
    """
    
    def __init__(self):
        self.quality_threshold = 0.8
        self.max_retries = 3
        self.timeout_seconds = 30
        
        # Model priority order
        self.model_priority = [
            ModelType.CLAUDE,
            ModelType.GPT4,
            ModelType.GEMINI,
            ModelType.BACKUP
        ]
        
        # Model performance history
        self.model_performance = {
            ModelType.CLAUDE: {"success_rate": 0.95, "avg_quality": 0.92},
            ModelType.GPT4: {"success_rate": 0.90, "avg_quality": 0.88},
            ModelType.GEMINI: {"success_rate": 0.85, "avg_quality": 0.85},
            ModelType.BACKUP: {"success_rate": 0.75, "avg_quality": 0.75}
        }
    
    async def smart_translate_with_retry(self, content: str, target_language: str,
                                       initial_result: Dict[str, Any]) -> RetryResult:
        """
        Perform smart translation with intelligent retry logic
        """
        print("🔄 Smart Retry System activated...")
        
        retry_count = 0
        retry_reasons = []
        best_result = initial_result
        improvement_notes = []
        
        # Check if retry is needed
        if not self._should_retry(initial_result):
            print("✅ Initial translation quality sufficient - no retry needed")
            return RetryResult(
                success=True,
                model_used=ModelType.CLAUDE,
                quality_score=initial_result.get('quality_score', 0.85),
                processing_time=initial_result.get('processing_time', 0),
                retry_count=0,
                retry_reasons=[],
                final_translation=initial_result.get('translated_text', ''),
                improvement_notes=["Initial quality acceptable"]
            )
        
        # Determine retry strategy
        retry_strategy = self._determine_retry_strategy(initial_result)
        retry_reasons.extend(retry_strategy['reasons'])
        
        print(f"🎯 Retry strategy: {retry_strategy['approach']} - {len(retry_strategy['models'])} models to try")
        
        # Attempt retries with different models
        for model_type in retry_strategy['models']:
            if retry_count >= self.max_retries:
                break
                
            retry_count += 1
            print(f"🔄 Retry attempt {retry_count} with {model_type.value} model...")
            
            try:
                # Simulate model-specific translation
                retry_result = await self._translate_with_model(
                    content, target_language, model_type, retry_count
                )
                
                # Check if this attempt is better
                if self._is_better_result(retry_result, best_result):
                    best_result = retry_result
                    improvement_notes.append(f"Improved with {model_type.value} model")
                    print(f"✅ Better result achieved with {model_type.value}")
                    
                    # Check if quality threshold met
                    if retry_result.get('quality_score', 0) >= self.quality_threshold:
                        print(f"🎯 Quality threshold reached: {retry_result['quality_score']:.2f}")
                        break
                
            except Exception as e:
                print(f"⚠️ {model_type.value} model failed: {e}")
                retry_reasons.append(RetryReason.API_ERROR)
                continue
        
        # Final result
        final_quality = best_result.get('quality_score', 0)
        success = final_quality >= self.quality_threshold
        
        if success:
            improvement_notes.append(f"Final quality: {final_quality:.2f}")
        else:
            improvement_notes.append(f"Quality below threshold: {final_quality:.2f}")
        
        print(f"🏁 Smart retry complete - {retry_count} attempts, quality: {final_quality:.2f}")
        
        return RetryResult(
            success=success,
            model_used=self._determine_best_model(best_result),
            quality_score=final_quality,
            processing_time=best_result.get('processing_time', 0),
            retry_count=retry_count,
            retry_reasons=retry_reasons,
            final_translation=best_result.get('translated_text', ''),
            improvement_notes=improvement_notes
        )
    
    def _should_retry(self, result: Dict[str, Any]) -> bool:
        """Determine if retry is needed based on result quality"""
        quality_score = result.get('quality_score', 0)
        
        # Always retry if quality is below threshold
        if quality_score < self.quality_threshold:
            return True
        
        # Retry if there are error indicators
        if result.get('error') or not result.get('success', True):
            return True
        
        # Retry if translation seems incomplete
        original_length = len(result.get('original_text', ''))
        translated_length = len(result.get('translated_text', ''))
        
        if translated_length < original_length * 0.5:  # Too short translation
            return True
        
        return False
    
    def _determine_retry_strategy(self, initial_result: Dict[str, Any]) -> Dict[str, Any]:
        """Determine optimal retry strategy"""
        reasons = []
        approach = "standard"
        models_to_try = []
        
        quality_score = initial_result.get('quality_score', 0)
        
        if quality_score < 0.6:
            reasons.append(RetryReason.LOW_QUALITY)
            approach = "aggressive"
            models_to_try = self.model_priority[:3]  # Try top 3 models
        elif quality_score < self.quality_threshold:
            reasons.append(RetryReason.OPTIMIZATION)
            approach = "optimization"
            models_to_try = self.model_priority[:2]  # Try top 2 models
        
        if initial_result.get('error'):
            reasons.append(RetryReason.API_ERROR)
            models_to_try = self.model_priority[1:]  # Skip primary model
        
        return {
            'reasons': reasons,
            'approach': approach,
            'models': models_to_try
        }
    
    async def _translate_with_model(self, content: str, target_language: str,
                                  model_type: ModelType, attempt: int) -> Dict[str, Any]:
        """Simulate translation with specific model"""
        start_time = time.time()
        
        # Simulate processing delay
        await asyncio.sleep(0.5)
        
        # Mock different model behaviors
        model_configs = {
            ModelType.CLAUDE: {
                'base_quality': 0.92,
                'consistency': 0.95,
                'speed_factor': 1.0
            },
            ModelType.GPT4: {
                'base_quality': 0.88,
                'consistency': 0.90,
                'speed_factor': 1.2
            },
            ModelType.GEMINI: {
                'base_quality': 0.85,
                'consistency': 0.85,
                'speed_factor': 0.8
            },
            ModelType.BACKUP: {
                'base_quality': 0.75,
                'consistency': 0.80,
                'speed_factor': 0.6
            }
        }
        
        config = model_configs[model_type]
        
        # Calculate quality with some variation
        import random
        quality_variation = (random.random() - 0.5) * 0.1  # ±5%
        quality_score = max(0.6, min(0.98, config['base_quality'] + quality_variation))
        
        processing_time = (time.time() - start_time) * config['speed_factor']
        
        return {
            'success': True,
            'translated_text': f"[{model_type.value.upper()} TRANSLATION] {content}",
            'quality_score': quality_score,
            'processing_time': processing_time,
            'model_used': model_type.value,
            'original_text': content
        }
    
    def _is_better_result(self, new_result: Dict[str, Any], current_best: Dict[str, Any]) -> bool:
        """Compare results to determine if new one is better"""
        new_quality = new_result.get('quality_score', 0)
        current_quality = current_best.get('quality_score', 0)
        
        # Primary criteria: quality score
        if new_quality > current_quality + 0.02:  # At least 2% improvement
            return True
        
        # Secondary criteria: if quality similar, prefer faster processing
        if abs(new_quality - current_quality) < 0.02:
            new_time = new_result.get('processing_time', float('inf'))
            current_time = current_best.get('processing_time', float('inf'))
            return new_time < current_time
        
        return False
    
    def _determine_best_model(self, result: Dict[str, Any]) -> ModelType:
        """Determine which model produced the result"""
        model_name = result.get('model_used', 'claude')
        
        model_mapping = {
            'claude': ModelType.CLAUDE,
            'gpt4': ModelType.GPT4,
            'gemini': ModelType.GEMINI,
            'backup': ModelType.BACKUP
        }
        
        return model_mapping.get(model_name, ModelType.CLAUDE)
    
    def get_performance_insights(self) -> Dict[str, Any]:
        """Get system performance insights"""
        return {
            'model_performance': self.model_performance,
            'quality_threshold': self.quality_threshold,
            'max_retries': self.max_retries,
            'model_priority': [model.value for model in self.model_priority]
        }
