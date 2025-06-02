"""
Translation Quality Scorer
Multi-dimensional quality assessment for translation results
"""

import re
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .providers.base_provider import TranslationRequest, TranslationResponse


class QualityMetric(Enum):
    """Quality assessment metrics"""
    CONFIDENCE = "confidence"
    LENGTH_RATIO = "length_ratio"
    CHARACTER_PRESERVATION = "character_preservation"
    FORMATTING_PRESERVATION = "formatting_preservation"
    RESPONSE_TIME = "response_time"
    COST_EFFICIENCY = "cost_efficiency"


@dataclass
class QualityScore:
    """Comprehensive quality score"""
    overall_score: float  # 0.0 to 1.0
    confidence_score: float
    length_ratio_score: float
    formatting_score: float
    speed_score: float
    cost_score: float
    metadata: Dict[str, Any]


class QualityScorer:
    """
    Evaluates translation quality using multiple metrics
    """
    
    def __init__(self):
        self.scoring_weights = {
            QualityMetric.CONFIDENCE: 0.35,
            QualityMetric.LENGTH_RATIO: 0.15,
            QualityMetric.CHARACTER_PRESERVATION: 0.15,
            QualityMetric.FORMATTING_PRESERVATION: 0.10,
            QualityMetric.RESPONSE_TIME: 0.15,
            QualityMetric.COST_EFFICIENCY: 0.10
        }
    
    def score_translation(self, request: TranslationRequest, 
                         response: TranslationResponse) -> QualityScore:
        """
        Calculate comprehensive quality score for a translation
        """
        scores = {}
        
        # 1. Provider confidence score
        scores[QualityMetric.CONFIDENCE] = self._score_confidence(response)
        
        # 2. Length ratio score (detect over/under translation)
        scores[QualityMetric.LENGTH_RATIO] = self._score_length_ratio(
            request.text, response.translated_text
        )
        
        # 3. Character preservation (numbers, URLs, etc.)
        scores[QualityMetric.CHARACTER_PRESERVATION] = self._score_character_preservation(
            request.text, response.translated_text
        )
        
        # 4. Formatting preservation (markdown, punctuation)
        scores[QualityMetric.FORMATTING_PRESERVATION] = self._score_formatting_preservation(
            request.text, response.translated_text
        )
        
        # 5. Response time score
        scores[QualityMetric.RESPONSE_TIME] = self._score_response_time(response.processing_time)
        
        # 6. Cost efficiency score
        scores[QualityMetric.COST_EFFICIENCY] = self._score_cost_efficiency(
            request.text, response.cost_estimate
        )
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[metric] * self.scoring_weights[metric]
            for metric in scores
        )
        
        return QualityScore(
            overall_score=overall_score,
            confidence_score=scores[QualityMetric.CONFIDENCE],
            length_ratio_score=scores[QualityMetric.LENGTH_RATIO],
            formatting_score=scores[QualityMetric.FORMATTING_PRESERVATION],
            speed_score=scores[QualityMetric.RESPONSE_TIME],
            cost_score=scores[QualityMetric.COST_EFFICIENCY],
            metadata={
                "provider": response.provider,
                "source_length": len(request.text),
                "target_length": len(response.translated_text),
                "processing_time": response.processing_time,
                "cost_estimate": response.cost_estimate,
                "individual_scores": scores
            }
        )
    
    def _score_confidence(self, response: TranslationResponse) -> float:
        """Score based on provider's confidence"""
        return response.confidence_score
    
    def _score_length_ratio(self, source_text: str, translated_text: str) -> float:
        """Score based on length ratio between source and translation"""
        if not source_text or not translated_text:
            return 0.0
        
        ratio = len(translated_text) / len(source_text)
        
        # Ideal ratio ranges (language-dependent, using general ranges)
        if 0.7 <= ratio <= 1.5:  # Good range
            return 1.0
        elif 0.5 <= ratio < 0.7 or 1.5 < ratio <= 2.0:  # Acceptable range
            return 0.8
        elif 0.3 <= ratio < 0.5 or 2.0 < ratio <= 3.0:  # Poor range
            return 0.5
        else:  # Very poor
            return 0.2
    
    def _score_character_preservation(self, source_text: str, translated_text: str) -> float:
        """Score based on preservation of special characters (numbers, URLs, emails)"""
        # Extract special elements
        numbers_source = re.findall(r'\d+', source_text)
        numbers_target = re.findall(r'\d+', translated_text)
        
        urls_source = re.findall(r'https?://\S+', source_text)
        urls_target = re.findall(r'https?://\S+', translated_text)
        
        emails_source = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', source_text)
        emails_target = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', translated_text)
        
        # Calculate preservation rates
        scores = []
        
        if numbers_source:
            numbers_preserved = len(set(numbers_source) & set(numbers_target)) / len(set(numbers_source))
            scores.append(numbers_preserved)
        
        if urls_source:
            urls_preserved = len(set(urls_source) & set(urls_target)) / len(set(urls_source))
            scores.append(urls_preserved)
        
        if emails_source:
            emails_preserved = len(set(emails_source) & set(emails_target)) / len(set(emails_source))
            scores.append(emails_preserved)
        
        return sum(scores) / len(scores) if scores else 1.0
    
    def _score_formatting_preservation(self, source_text: str, translated_text: str) -> float:
        """Score based on preservation of formatting elements"""
        formatting_elements = [
            r'\*\*.*?\*\*',  # Bold markdown
            r'\*.*?\*',      # Italic markdown
            r'`.*?`',        # Code markdown
            r'\[.*?\]\(.*?\)',  # Links markdown
            r'\n',           # Line breaks
            r'[.!?]+',       # Punctuation
        ]
        
        scores = []
        
        for pattern in formatting_elements:
            source_matches = len(re.findall(pattern, source_text))
            target_matches = len(re.findall(pattern, translated_text))
            
            if source_matches > 0:
                preservation = min(target_matches / source_matches, 1.0)
                scores.append(preservation)
        
        return sum(scores) / len(scores) if scores else 1.0
    
    def _score_response_time(self, processing_time: float) -> float:
        """Score based on response time (faster is better)"""
        # Score mapping: < 0.5s = 1.0, 0.5-2s = 0.8, 2-5s = 0.6, 5-10s = 0.4, >10s = 0.2
        if processing_time < 0.5:
            return 1.0
        elif processing_time < 2.0:
            return 0.8
        elif processing_time < 5.0:
            return 0.6
        elif processing_time < 10.0:
            return 0.4
        else:
            return 0.2
    
    def _score_cost_efficiency(self, source_text: str, cost_estimate: float) -> float:
        """Score based on cost efficiency (lower cost per character is better)"""
        if cost_estimate == 0.0:  # Free service
            return 1.0
        
        if not source_text:
            return 0.0
        
        cost_per_char = cost_estimate / len(source_text)
        
        # Score mapping based on cost per character (in USD)
        if cost_per_char < 0.00001:  # Very cheap
            return 1.0
        elif cost_per_char < 0.0001:  # Cheap
            return 0.8
        elif cost_per_char < 0.001:   # Moderate
            return 0.6
        elif cost_per_char < 0.01:    # Expensive
            return 0.4
        else:  # Very expensive
            return 0.2
    
    def compare_translations(self, request: TranslationRequest, 
                           responses: List[TranslationResponse]) -> List[QualityScore]:
        """Compare multiple translation responses and rank them"""
        scores = []
        
        for response in responses:
            score = self.score_translation(request, response)
            scores.append(score)
        
        # Sort by overall score (highest first)
        scores.sort(key=lambda x: x.overall_score, reverse=True)
        
        return scores
    
    def get_best_translation(self, request: TranslationRequest, 
                           responses: List[TranslationResponse]) -> TranslationResponse:
        """Get the best translation from multiple responses"""
        if not responses:
            raise ValueError("No responses to evaluate")
        
        if len(responses) == 1:
            return responses[0]
        
        scores = self.compare_translations(request, responses)
        best_score = scores[0]
        
        # Find the response that matches the best score
        for response in responses:
            if response.provider == best_score.metadata["provider"]:
                return response
        
        # Fallback to first response
        return responses[0]
