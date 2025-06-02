"""
Intent Analysis Engine - Phase 7 Week 1
Intelligently analyzes user input to understand what they want to achieve
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import re


class UserIntent(Enum):
    """Primary user intents"""
    TRANSLATE_ONLY = "translate_only"
    CREATE_PODCAST = "create_podcast"
    CREATE_VIDEO = "create_video"
    CREATE_EDUCATION = "create_education"
    BATCH_PROCESSING = "batch_processing"
    ANALYZE_CONTENT = "analyze_content"


class OutputFormat(Enum):
    """Desired output formats"""
    TEXT_TRANSLATION = "text_translation"
    PODCAST_SCRIPT = "podcast_script"
    VIDEO_SCENARIO = "video_scenario"
    EDUCATION_MODULE = "education_module"
    ANALYSIS_REPORT = "analysis_report"


class UserExpertise(Enum):
    """User expertise levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PROFESSIONAL = "professional"


@dataclass
class IntentAnalysisResult:
    """Complete intent analysis result"""
    primary_intent: UserIntent
    desired_output_format: OutputFormat
    user_expertise_level: UserExpertise
    confidence_score: float = 0.0
    key_requirements: Dict[str, Any] = field(default_factory=dict)
    suggested_questions: List[str] = field(default_factory=list)
    processing_recommendations: Dict[str, Any] = field(default_factory=dict)


class IntentAnalyzer:
    """AI-powered intent analysis engine"""
    
    def __init__(self):
        """Initialize intent analyzer"""
        print("🧠 Initializing Advanced Intent Analysis Engine...")
        self.intent_patterns = self._load_intent_patterns()
        self.expertise_indicators = self._load_expertise_indicators()
        print("✅ Advanced Intent Analysis Engine ready")
    
    def _load_intent_patterns(self) -> Dict[UserIntent, List[str]]:
        """Load intent detection patterns"""
        return {
            UserIntent.CREATE_PODCAST: [
                r"làm podcast|tạo podcast|podcast script|podcast từ",
                r"audio content|âm thanh|script âm thanh"
            ],
            UserIntent.CREATE_VIDEO: [
                r"làm video|tạo video|video script|video từ",
                r"scenario|kịch bản|storyboard"
            ],
            UserIntent.CREATE_EDUCATION: [
                r"học tập|giáo dục|education|module học|bài học",
                r"training|đào tạo|course|khóa học"
            ],
            UserIntent.TRANSLATE_ONLY: [
                r"^translate|^dịch|chỉ dịch|only translate",
                r"translation only|dịch thuần túy"
            ],
            UserIntent.ANALYZE_CONTENT: [
                r"phân tích|analyze|analysis|đánh giá",
                r"understand|hiểu|summary|tóm tắt"
            ]
        }
    
    def _load_expertise_indicators(self) -> Dict[UserExpertise, List[str]]:
        """Load user expertise detection patterns"""
        return {
            UserExpertise.BEGINNER: [
                r"không biết|don't know|help me|giúp tôi",
                r"new to|mới bắt đầu|beginner"
            ],
            UserExpertise.ADVANCED: [
                r"optimize|tối ưu|advanced|chuyên sâu",
                r"technical|kỹ thuật|professional"
            ],
            UserExpertise.PROFESSIONAL: [
                r"enterprise|doanh nghiệp|production|commercial"
            ]
        }
    
    def analyze_intent(self, user_input: str, content_info: Dict[str, Any] = None) -> IntentAnalysisResult:
        """
        Analyze user intent from input
        
        Args:
            user_input: User's request/command
            content_info: Optional info about uploaded content
            
        Returns:
            Complete intent analysis result
        """
        print(f"🧠 Analyzing intent: '{user_input[:50]}...'")
        
        # Detect primary intent
        primary_intent = self._detect_primary_intent(user_input)
        
        # Detect output format
        output_format = self._detect_output_format(user_input, primary_intent)
        
        # Assess user expertise
        expertise_level = self._assess_user_expertise(user_input)
        
        # Calculate confidence
        confidence = self._calculate_confidence(user_input, primary_intent)
        
        # Extract key requirements
        requirements = self._extract_requirements(user_input, primary_intent)
        
        # Generate smart questions
        questions = self._generate_smart_questions(primary_intent, expertise_level)
        
        # Create processing recommendations
        recommendations = self._create_processing_recommendations(
            primary_intent, output_format, expertise_level
        )
        
        result = IntentAnalysisResult(
            primary_intent=primary_intent,
            desired_output_format=output_format,
            user_expertise_level=expertise_level,
            confidence_score=confidence,
            key_requirements=requirements,
            suggested_questions=questions,
            processing_recommendations=recommendations
        )
        
        print(f"✅ Intent analyzed: {primary_intent.value} ({confidence:.1%} confidence)")
        return result
    
    def _detect_primary_intent(self, user_input: str) -> UserIntent:
        """Detect primary user intent"""
        user_input_lower = user_input.lower()
        
        # Score each intent
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    score += 1
            intent_scores[intent] = score
        
        # Return highest scoring intent or default
        if intent_scores and max(intent_scores.values()) > 0:
            return max(intent_scores, key=intent_scores.get)
        
        # Default fallback
        if "podcast" in user_input_lower:
            return UserIntent.CREATE_PODCAST
        elif "video" in user_input_lower:
            return UserIntent.CREATE_VIDEO
        elif any(word in user_input_lower for word in ["education", "học", "training"]):
            return UserIntent.CREATE_EDUCATION
        else:
            return UserIntent.TRANSLATE_ONLY
    
    def _detect_output_format(self, user_input: str, primary_intent: UserIntent) -> OutputFormat:
        """Detect desired output format"""
        # Map intent to format
        intent_to_format = {
            UserIntent.CREATE_PODCAST: OutputFormat.PODCAST_SCRIPT,
            UserIntent.CREATE_VIDEO: OutputFormat.VIDEO_SCENARIO,
            UserIntent.CREATE_EDUCATION: OutputFormat.EDUCATION_MODULE,
            UserIntent.TRANSLATE_ONLY: OutputFormat.TEXT_TRANSLATION,
            UserIntent.ANALYZE_CONTENT: OutputFormat.ANALYSIS_REPORT
        }
        
        return intent_to_format.get(primary_intent, OutputFormat.TEXT_TRANSLATION)
    
    def _assess_user_expertise(self, user_input: str) -> UserExpertise:
        """Assess user expertise level"""
        user_input_lower = user_input.lower()
        
        # Check expertise indicators
        for expertise, patterns in self.expertise_indicators.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return expertise
        
        # Default to intermediate
        return UserExpertise.INTERMEDIATE
    
    def _calculate_confidence(self, user_input: str, intent: UserIntent) -> float:
        """Calculate confidence score"""
        base_confidence = 0.7
        
        # Boost confidence for clear patterns
        user_input_lower = user_input.lower()
        patterns = self.intent_patterns.get(intent, [])
        
        for pattern in patterns:
            if re.search(pattern, user_input_lower):
                base_confidence += 0.1
        
        return min(1.0, base_confidence)
    
    def _extract_requirements(self, user_input: str, intent: UserIntent) -> Dict[str, Any]:
        """Extract key requirements from user input"""
        requirements = {}
        
        # Extract time-related requirements
        if re.search(r"(\d+)\s*(minute|phút)", user_input.lower()):
            match = re.search(r"(\d+)\s*(minute|phút)", user_input.lower())
            requirements["duration_minutes"] = int(match.group(1))
        
        # Extract audience requirements
        if re.search(r"beginner|người mới|cơ bản", user_input.lower()):
            requirements["target_audience"] = "beginner"
        elif re.search(r"advanced|nâng cao|chuyên sâu", user_input.lower()):
            requirements["target_audience"] = "advanced"
        
        return requirements
    
    def _generate_smart_questions(self, intent: UserIntent, expertise: UserExpertise) -> List[str]:
        """Generate smart follow-up questions"""
        questions = []
        
        # Intent-specific questions
        if intent == UserIntent.CREATE_PODCAST:
            questions.extend([
                "Thời lượng mong muốn cho podcast (5-30 phút)?",
                "Phong cách: trò chuyện hay thuyết trình?"
            ])
        elif intent == UserIntent.CREATE_VIDEO:
            questions.extend([
                "Loại video: explainer, tutorial, hay presentation?",
                "Thời lượng video mong muốn?"
            ])
        elif intent == UserIntent.CREATE_EDUCATION:
            questions.extend([
                "Đối tượng học viên: sinh viên, nhân viên, hay chuyên gia?",
                "Định dạng: bài giảng, bài tập, hay module tương tác?"
            ])
        
        # Expertise-based questions
        if expertise == UserExpertise.BEGINNER:
            questions.append("Bạn có muốn giải thích chi tiết các thuật ngữ không?")
        elif expertise == UserExpertise.ADVANCED:
            questions.append("Có cần optimization đặc biệt nào không?")
        
        # Limit to 3 questions max for better UX
        return questions[:3]
    
    def _create_processing_recommendations(self, intent: UserIntent, output_format: OutputFormat, 
                                         expertise: UserExpertise) -> Dict[str, Any]:
        """Create processing recommendations"""
        recommendations = {
            "processing_mode": "balanced",
            "quality_target": 0.8,
            "optimization_focus": "quality"
        }
        
        # Adjust based on expertise
        if expertise == UserExpertise.PROFESSIONAL:
            recommendations["quality_target"] = 0.9
            recommendations["optimization_focus"] = "quality"
        elif expertise == UserExpertise.BEGINNER:
            recommendations["processing_mode"] = "speed_optimized"
            recommendations["optimization_focus"] = "simplicity"
        
        # Adjust based on intent
        if intent == UserIntent.CREATE_PODCAST:
            recommendations["transformation_type"] = "podcast_script"
        elif intent == UserIntent.CREATE_VIDEO:
            recommendations["transformation_type"] = "video_scenario"
        elif intent == UserIntent.CREATE_EDUCATION:
            recommendations["transformation_type"] = "education_module"
        
        return recommendations


# Comprehensive test function
def test_advanced_intent_analyzer():
    """Test advanced intent analyzer with comprehensive cases"""
    analyzer = IntentAnalyzer()
    
    test_cases = [
        "Làm podcast từ file PDF này",
        "Tạo video scenario chuyên nghiệp từ document",
        "Dịch text này sang tiếng Việt",
        "Tạo module học tập cho sinh viên từ tài liệu",
        "Phân tích nội dung và tóm tắt",
        "Help me create podcast 15 minutes long"
    ]
    
    print("🧪 COMPREHENSIVE INTENT ANALYSIS TESTING")
    print("="*50)
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_input}")
        result = analyzer.analyze_intent(test_input)
        print(f"   📊 Intent: {result.primary_intent.value}")
        print(f"   📋 Output: {result.desired_output_format.value}")
        print(f"   👤 Expertise: {result.user_expertise_level.value}")
        print(f"   🎯 Confidence: {result.confidence_score:.1%}")
        print(f"   ❓ Questions: {len(result.suggested_questions)}")
        if result.suggested_questions:
            for q in result.suggested_questions:
                print(f"      - {q}")
        print(f"   ⚙️  Recommendations: {result.processing_recommendations}")
    
    print("\n🏆 INTENT ANALYSIS ENGINE: FULLY OPERATIONAL!")


if __name__ == "__main__":
    test_advanced_intent_analyzer()
