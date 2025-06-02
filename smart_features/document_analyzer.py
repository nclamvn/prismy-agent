# smart_features/document_analyzer.py
"""
Intelligent Document Analyzer
Smart features for automatic document optimization and analysis
"""

import re
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class DocumentComplexity(Enum):
    SIMPLE = "simple"
    MODERATE = "moderate" 
    COMPLEX = "complex"
    TECHNICAL = "technical"

class ContentType(Enum):
    GENERAL = "general"
    TECHNICAL = "technical"
    ACADEMIC = "academic"
    BUSINESS = "business"
    CREATIVE = "creative"
    LEGAL = "legal"

@dataclass
class DocumentAnalysis:
    """Smart document analysis results"""
    complexity: DocumentComplexity
    content_type: ContentType
    estimated_time: float
    confidence_prediction: float
    recommended_chunk_size: int
    language_hints: List[str]
    key_features: List[str]
    optimization_suggestions: List[str]

class IntelligentDocumentAnalyzer:
    """
    Smart document analyzer with AI-powered insights
    Automatically optimizes translation parameters
    """
    
    def __init__(self):
        # Technical indicators
        self.technical_patterns = [
            r'\b(?:API|SDK|HTTP|JSON|XML|SQL|CPU|GPU|RAM)\b',
            r'\b(?:algorithm|function|variable|parameter|database)\b',
            r'\b(?:configure|implement|execute|compile|debug)\b',
            r'[a-zA-Z]+\([^)]*\)',  # Function calls
            r'[{}\[\]<>]',           # Code brackets
        ]
        
        # Business indicators
        self.business_patterns = [
            r'\b(?:revenue|profit|ROI|KPI|metrics|performance)\b',
            r'\b(?:strategy|market|customer|client|stakeholder)\b',
            r'\b(?:budget|investment|cost|pricing|sales)\b',
            r'\b(?:meeting|presentation|proposal|contract)\b',
        ]
        
        # Academic indicators  
        self.academic_patterns = [
            r'\b(?:research|study|analysis|hypothesis|methodology)\b',
            r'\b(?:conclusion|findings|results|data|statistics)\b',
            r'\b(?:literature|references|bibliography|citation)\b',
            r'Figure \d+|Table \d+|Section \d+',
        ]
        
        # Legal indicators
        self.legal_patterns = [
            r'\b(?:contract|agreement|terms|conditions|clause)\b',
            r'\b(?:liability|warranty|intellectual property|copyright)\b',
            r'\b(?:shall|hereby|whereas|therefore|pursuant)\b',
            r'Article \d+|Section \d+\.\d+',
        ]
        
        # Creative indicators
        self.creative_patterns = [
            r'\b(?:story|character|plot|narrative|dialogue)\b',
            r'\b(?:metaphor|imagery|symbolism|theme|tone)\b',
            r'\b(?:creative|artistic|inspiration|imagination)\b',
        ]
    
    def analyze_document(self, content: str) -> DocumentAnalysis:
        """
        Perform comprehensive smart analysis of document
        """
        print("🧠 Smart Document Analysis in progress...")
        
        # Basic metrics
        word_count = len(content.split())
        sentence_count = len(re.findall(r'[.!?]+', content))
        char_count = len(content)
        
        # Complexity analysis
        complexity = self._analyze_complexity(content, word_count, sentence_count)
        
        # Content type detection
        content_type = self._detect_content_type(content)
        
        # Time estimation (based on complexity and length)
        estimated_time = self._estimate_processing_time(word_count, complexity)
        
        # Confidence prediction
        confidence_prediction = self._predict_translation_confidence(content, complexity, content_type)
        
        # Smart chunk size recommendation
        recommended_chunk_size = self._recommend_chunk_size(content, complexity, content_type)
        
        # Language hints detection
        language_hints = self._detect_language_hints(content)
        
        # Key features extraction
        key_features = self._extract_key_features(content, complexity, content_type)
        
        # Optimization suggestions
        optimization_suggestions = self._generate_optimization_suggestions(
            content, complexity, content_type, word_count
        )
        
        print(f"✅ Smart analysis complete - {complexity.value} {content_type.value} document")
        
        return DocumentAnalysis(
            complexity=complexity,
            content_type=content_type,
            estimated_time=estimated_time,
            confidence_prediction=confidence_prediction,
            recommended_chunk_size=recommended_chunk_size,
            language_hints=language_hints,
            key_features=key_features,
            optimization_suggestions=optimization_suggestions
        )
    
    def _analyze_complexity(self, content: str, word_count: int, sentence_count: int) -> DocumentComplexity:
        """Analyze document complexity using multiple factors"""
        complexity_score = 0
        
        # Length factor
        if word_count < 100:
            complexity_score += 1
        elif word_count < 500:
            complexity_score += 2
        elif word_count < 1000:
            complexity_score += 3
        else:
            complexity_score += 4
        
        # Sentence complexity
        avg_words_per_sentence = word_count / max(sentence_count, 1)
        if avg_words_per_sentence > 20:
            complexity_score += 2
        elif avg_words_per_sentence > 15:
            complexity_score += 1
        
        # Technical complexity indicators
        technical_matches = sum(1 for pattern in self.technical_patterns 
                              if re.search(pattern, content, re.IGNORECASE))
        if technical_matches > 5:
            complexity_score += 3
        elif technical_matches > 2:
            complexity_score += 2
        
        # Special characters and formatting
        special_chars = len(re.findall(r'[{}()\[\]<>]', content))
        if special_chars > word_count * 0.1:
            complexity_score += 2
        
        # Map score to complexity level
        if complexity_score <= 3:
            return DocumentComplexity.SIMPLE
        elif complexity_score <= 6:
            return DocumentComplexity.MODERATE
        elif complexity_score <= 9:
            return DocumentComplexity.COMPLEX
        else:
            return DocumentComplexity.TECHNICAL
    
    def _detect_content_type(self, content: str) -> ContentType:
        """Smart content type detection"""
        scores = {
            ContentType.TECHNICAL: sum(1 for pattern in self.technical_patterns 
                                     if re.search(pattern, content, re.IGNORECASE)),
            ContentType.BUSINESS: sum(1 for pattern in self.business_patterns 
                                    if re.search(pattern, content, re.IGNORECASE)),
            ContentType.ACADEMIC: sum(1 for pattern in self.academic_patterns 
                                    if re.search(pattern, content, re.IGNORECASE)),
            ContentType.LEGAL: sum(1 for pattern in self.legal_patterns 
                                 if re.search(pattern, content, re.IGNORECASE)),
            ContentType.CREATIVE: sum(1 for pattern in self.creative_patterns 
                                    if re.search(pattern, content, re.IGNORECASE))
        }
        
        # Find highest scoring type
        max_score = max(scores.values())
        if max_score < 2:
            return ContentType.GENERAL
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _estimate_processing_time(self, word_count: int, complexity: DocumentComplexity) -> float:
        """Smart processing time estimation"""
        base_time = word_count * 0.01  # Base: 0.01s per word
        
        complexity_multipliers = {
            DocumentComplexity.SIMPLE: 1.0,
            DocumentComplexity.MODERATE: 1.5,
            DocumentComplexity.COMPLEX: 2.0,
            DocumentComplexity.TECHNICAL: 2.5
        }
        
        return base_time * complexity_multipliers[complexity]
    
    def _predict_translation_confidence(self, content: str, complexity: DocumentComplexity, 
                                      content_type: ContentType) -> float:
        """Predict translation confidence score"""
        base_confidence = 0.85
        
        # Complexity adjustments
        complexity_adjustments = {
            DocumentComplexity.SIMPLE: 0.1,
            DocumentComplexity.MODERATE: 0.0,
            DocumentComplexity.COMPLEX: -0.05,
            DocumentComplexity.TECHNICAL: -0.1
        }
        
        # Content type adjustments
        content_adjustments = {
            ContentType.GENERAL: 0.05,
            ContentType.BUSINESS: 0.0,
            ContentType.TECHNICAL: -0.05,
            ContentType.ACADEMIC: -0.02,
            ContentType.CREATIVE: -0.03,
            ContentType.LEGAL: -0.1
        }
        
        confidence = base_confidence + complexity_adjustments[complexity] + content_adjustments[content_type]
        return max(0.6, min(0.95, confidence))
    
    def _recommend_chunk_size(self, content: str, complexity: DocumentComplexity, 
                            content_type: ContentType) -> int:
        """Smart chunk size recommendation"""
        base_size = 2000
        
        # Adjust based on complexity
        if complexity == DocumentComplexity.SIMPLE:
            base_size = 2500
        elif complexity == DocumentComplexity.TECHNICAL:
            base_size = 1500
        
        # Adjust based on content type
        if content_type == ContentType.TECHNICAL:
            base_size = int(base_size * 0.8)
        elif content_type == ContentType.CREATIVE:
            base_size = int(base_size * 1.2)
        
        return base_size
    
    def _detect_language_hints(self, content: str) -> List[str]:
        """Detect language hints in document"""
        hints = []
        
        # Common non-English patterns
        if re.search(r'[àáâãäåèéêëìíîïòóôõöùúûüý]', content):
            hints.append("Contains accented characters")
        
        if re.search(r'[αβγδεζηθικλμνξοπρστυφχψω]', content):
            hints.append("Contains Greek characters")
        
        if re.search(r'[ñç]', content):
            hints.append("Possible Spanish/Portuguese content")
        
        if re.search(r'[äöüß]', content):
            hints.append("Possible German content")
        
        return hints
    
    def _extract_key_features(self, content: str, complexity: DocumentComplexity, 
                            content_type: ContentType) -> List[str]:
        """Extract key document features"""
        features = []
        
        # Structure features
        if re.search(r'^#{1,6}\s', content, re.MULTILINE):
            features.append("Contains markdown headers")
        
        if re.search(r'^\s*[-*+]\s', content, re.MULTILINE):
            features.append("Contains bullet lists")
        
        if re.search(r'^\s*\d+\.\s', content, re.MULTILINE):
            features.append("Contains numbered lists")
        
        # Content features
        if re.search(r'https?://', content):
            features.append("Contains URLs")
        
        if re.search(r'\b[A-Z]{2,}\b', content):
            features.append("Contains acronyms")
        
        # Complexity features
        features.append(f"Complexity: {complexity.value}")
        features.append(f"Type: {content_type.value}")
        
        return features
    
    def _generate_optimization_suggestions(self, content: str, complexity: DocumentComplexity,
                                         content_type: ContentType, word_count: int) -> List[str]:
        """Generate smart optimization suggestions"""
        suggestions = []
        
        # Length-based suggestions
        if word_count > 2000:
            suggestions.append("Consider breaking into smaller sections for better processing")
        
        if word_count < 50:
            suggestions.append("Document is quite short - consider batch processing multiple documents")
        
        # Complexity-based suggestions
        if complexity == DocumentComplexity.TECHNICAL:
            suggestions.append("Technical content detected - recommend Professional tier for accuracy")
            suggestions.append("Consider smaller chunk sizes for better context preservation")
        
        # Content type suggestions
        if content_type == ContentType.CREATIVE:
            suggestions.append("Creative content - focus on preserving tone and style")
        elif content_type == ContentType.LEGAL:
            suggestions.append("Legal content - use highest quality tier for precision")
        elif content_type == ContentType.BUSINESS:
            suggestions.append("Business content - maintain professional terminology")
        
        # Structure suggestions
        if re.search(r'^#{1,6}\s', content, re.MULTILINE):
            suggestions.append("Document structure detected - formatting will be preserved")
        
        return suggestions
