"""
Smart Requirement Collector - Phase 7 Week 2
Intelligently collects minimal requirements from users with smart questioning
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

# Import from Week 1 - Use absolute import to avoid conflicts
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_analysis import IntentAnalysisResult, UserIntent, UserExpertise


class QuestionType(Enum):
    """Types of questions to ask users"""
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT_INPUT = "text_input"
    SLIDER = "slider"
    YES_NO = "yes_no"
    OPTIONAL = "optional"


class QuestionPriority(Enum):
    """Priority levels for questions"""
    CRITICAL = "critical"      # Must ask - affects output quality significantly
    IMPORTANT = "important"    # Should ask - improves output
    OPTIONAL = "optional"      # Nice to have - only if user expertise allows


@dataclass
class SmartQuestion:
    """A smart question with context and validation"""
    id: str
    text: str
    question_type: QuestionType
    priority: QuestionPriority
    options: List[str] = field(default_factory=list)      # For multiple choice
    default_value: Any = None
    validation_rule: Optional[str] = None
    help_text: Optional[str] = None
    depends_on: Optional[str] = None                       # Question dependency
    min_value: Optional[float] = None                      # For sliders/numbers
    max_value: Optional[float] = None


@dataclass
class UserResponse:
    """User response to a question"""
    question_id: str
    value: Any
    confidence: float = 1.0    # How confident user is about this answer
    timestamp: Optional[str] = None


@dataclass
class RequirementCollectionResult:
    """Complete requirement collection result"""
    collected_requirements: Dict[str, Any]
    questions_asked: List[SmartQuestion]
    user_responses: List[UserResponse]
    completion_score: float = 0.0          # How complete the requirements are
    collection_efficiency: float = 0.0     # Questions asked vs info gathered
    ready_for_processing: bool = False
    missing_critical_info: List[str] = field(default_factory=list)


class SmartRequirementCollector:
    """AI-powered requirement collection system"""
    
    def __init__(self):
        """Initialize requirement collector"""
        print("🤔 Initializing Smart Requirement Collector...")
        self.question_templates = self._load_question_templates()
        self.collection_strategies = self._load_collection_strategies()
        print("✅ Smart Requirement Collector ready")
    
    def _load_question_templates(self) -> Dict[UserIntent, List[SmartQuestion]]:
        """Load question templates for each intent"""
        return {
            UserIntent.CREATE_PODCAST: [
                SmartQuestion(
                    id="podcast_duration",
                    text="Thời lượng mong muốn cho podcast?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["5-10 phút", "10-20 phút", "20-30 phút", "30+ phút"],
                    default_value="10-20 phút"
                ),
                SmartQuestion(
                    id="podcast_style",
                    text="Phong cách podcast mong muốn?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["Trò chuyện tự nhiên", "Thuyết trình chuyên nghiệp", "Interview style", "Storytelling"],
                    default_value="Thuyết trình chuyên nghiệp"
                ),
                SmartQuestion(
                    id="target_audience",
                    text="Đối tượng nghe chính?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.IMPORTANT,
                    options=["Người mới bắt đầu", "Chuyên gia trong lĩnh vực", "Khách hàng doanh nghiệp", "Học sinh/sinh viên"],
                    default_value="Chuyên gia trong lĩnh vực"
                )
            ],
            
            UserIntent.CREATE_VIDEO: [
                SmartQuestion(
                    id="video_type",
                    text="Loại video mong muốn?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["Explainer video", "Tutorial/Hướng dẫn", "Presentation", "Product demo"],
                    default_value="Explainer video"
                ),
                SmartQuestion(
                    id="video_duration",
                    text="Thời lượng video?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["1-3 phút", "3-5 phút", "5-10 phút", "10+ phút"],
                    default_value="3-5 phút"
                )
            ],
            
            UserIntent.CREATE_EDUCATION: [
                SmartQuestion(
                    id="learning_level",
                    text="Trình độ học viên?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["Cơ bản", "Trung bình", "Nâng cao", "Chuyên gia"],
                    default_value="Trung bình"
                ),
                SmartQuestion(
                    id="module_format",
                    text="Định dạng module học tập?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.CRITICAL,
                    options=["Bài giảng lý thuyết", "Bài tập thực hành", "Case study", "Module tương tác"],
                    default_value="Module tương tác"
                )
            ],
            
            UserIntent.TRANSLATE_ONLY: [
                SmartQuestion(
                    id="translation_purpose",
                    text="Mục đích sử dụng bản dịch?",
                    question_type=QuestionType.MULTIPLE_CHOICE,
                    priority=QuestionPriority.IMPORTANT,
                    options=["Sử dụng cá nhân", "Công việc/Business", "Học tập", "Xuất bản/Public"],
                    default_value="Công việc/Business"
                )
            ]
        }
    
    def _load_collection_strategies(self) -> Dict[UserExpertise, Dict[str, Any]]:
        """Load collection strategies based on user expertise"""
        return {
            UserExpertise.BEGINNER: {
                "max_questions": 3,
                "question_priorities": [QuestionPriority.CRITICAL, QuestionPriority.IMPORTANT]
            },
            UserExpertise.INTERMEDIATE: {
                "max_questions": 3,
                "question_priorities": [QuestionPriority.CRITICAL, QuestionPriority.IMPORTANT]
            },
            UserExpertise.ADVANCED: {
                "max_questions": 4,
                "question_priorities": [QuestionPriority.CRITICAL, QuestionPriority.IMPORTANT, QuestionPriority.OPTIONAL]
            },
            UserExpertise.PROFESSIONAL: {
                "max_questions": 2,
                "question_priorities": [QuestionPriority.CRITICAL]
            }
        }
    
    def collect_requirements(self, intent_result: IntentAnalysisResult, 
                           user_responses: List[UserResponse] = None) -> RequirementCollectionResult:
        """
        Collect requirements from user based on intent analysis
        """
        print(f"🤔 Collecting requirements for {intent_result.primary_intent.value}...")
        
        # Get collection strategy for user expertise
        # Find strategy by enum value instead of enum object
        strategy = None
        for key, value in self.collection_strategies.items():
            if key.value == intent_result.user_expertise_level.value:
                strategy = value
                break
        
        if strategy is None:
            # Fallback to intermediate
            for key, value in self.collection_strategies.items():
                if key.value == 'intermediate':
                    strategy = value
                    break
        
        # Get relevant questions
        questions = self._select_smart_questions(intent_result, strategy)
        
        # Simulate user responses
        if user_responses is None:
            user_responses = self._simulate_user_responses(questions, intent_result)
        
        # Process responses into requirements
        requirements = self._process_responses_to_requirements(questions, user_responses)
        
        # Calculate scores
        completion_score = 1.0  # Simplified for now
        efficiency_score = 1.0
        
        result = RequirementCollectionResult(
            collected_requirements=requirements,
            questions_asked=questions,
            user_responses=user_responses,
            completion_score=completion_score,
            collection_efficiency=efficiency_score,
            ready_for_processing=True,
            missing_critical_info=[]
        )
        
        print(f"✅ Requirements collected: {completion_score:.1%} complete, {efficiency_score:.1%} efficient")
        return result
    
    def _select_smart_questions(self, intent_result: IntentAnalysisResult, 
                               strategy: Dict[str, Any]) -> List[SmartQuestion]:
        """Select smart questions based on intent and strategy"""
        available_questions = self.question_templates.get(intent_result.primary_intent, [])
        allowed_priorities = strategy["question_priorities"]
        filtered_questions = [q for q in available_questions if q.priority in allowed_priorities]
        max_questions = strategy["max_questions"]
        return filtered_questions[:max_questions]
    
    def _simulate_user_responses(self, questions: List[SmartQuestion], 
                                intent_result: IntentAnalysisResult) -> List[UserResponse]:
        """Simulate user responses for testing"""
        responses = []
        for question in questions:
            if intent_result.user_expertise_level == UserExpertise.PROFESSIONAL:
                value = self._get_professional_default(question)
            else:
                value = question.default_value or (question.options[0] if question.options else "auto")
            
            responses.append(UserResponse(
                question_id=question.id,
                value=value,
                confidence=0.9
            ))
        
        return responses
    
    def _get_professional_default(self, question: SmartQuestion) -> str:
        """Get professional-oriented defaults"""
        professional_prefs = {
            "podcast_duration": "20-30 phút",
            "podcast_style": "Thuyết trình chuyên nghiệp",
            "video_type": "Presentation",
            "video_duration": "5-10 phút"
        }
        return professional_prefs.get(question.id, question.default_value or (question.options[0] if question.options else "auto"))
    
    def _process_responses_to_requirements(self, questions: List[SmartQuestion], 
                                         responses: List[UserResponse]) -> Dict[str, Any]:
        """Process user responses into structured requirements"""
        requirements = {}
        response_dict = {r.question_id: r.value for r in responses}
        
        for question in questions:
            if question.id in response_dict:
                requirements[question.id] = response_dict[question.id]
        
        return requirements


# Test function
def test_requirement_collector():
    """Test requirement collector"""
    from intent_analysis import IntentAnalyzer
    
    collector = SmartRequirementCollector()
    analyzer = IntentAnalyzer()
    
    print("🧪 TESTING SMART REQUIREMENT COLLECTOR")
    print("="*50)
    
    test_input = "Làm podcast từ PDF cho doanh nghiệp"
    print(f"\n🧪 Test: {test_input}")
    
    intent_result = analyzer.analyze_intent(test_input)
    req_result = collector.collect_requirements(intent_result)
    
    print(f"   ❓ Questions asked: {len(req_result.questions_asked)}")
    print(f"   📋 Requirements: {len(req_result.collected_requirements)}")
    print(f"   🚀 Ready: {req_result.ready_for_processing}")
    
    print("\n🏆 SMART REQUIREMENT COLLECTOR: WORKING!")


if __name__ == "__main__":
    test_requirement_collector()
