"""
Intelligent Claude Commander with Smart Response Handling
"""

import anthropic
import asyncio
from typing import Dict, Any, Optional, List, Tuple
import os
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# Import our smart handler
import sys
sys.path.append(os.path.dirname(__file__))
from claude_response_handler import ClaudeResponseHandler

load_dotenv()


class ServiceType(Enum):
    TRANSLATION = "translation"
    VIDEO_CREATION = "video_creation"
    PODCAST_GENERATION = "podcast_generation"
    EDUCATION_MODULE = "education_module"
    GENERAL_INQUIRY = "general_inquiry"


@dataclass
class CustomerIntent:
    primary_service: ServiceType
    confidence: float
    keywords: List[str]
    language: str
    complexity: str


@dataclass
class SmartQuestion:
    question: str
    purpose: str
    expected_type: str


class IntelligentClaudeCommander:
    """
    Claude Commander with intelligent response handling
    No more JSON parsing errors!
    """
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.handler = ClaudeResponseHandler()
        self.max_questions = 3
        
    async def greet_and_analyze(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """Greet customer and analyze intent with Claude"""
        
        if not self.claude:
            return self._fallback_greeting(customer_name, request)
        
        prompt = f"""You are a professional AI concierge for PRISM AI Platform.

Customer: {customer_name}
Request: "{request}"

CRITICAL SERVICE DETECTION:
- video_creation: Keywords like "video", "clip", "visual", "youtube", "tiktok", "phim", "tạo video"
- podcast_generation: Keywords like "podcast", "audio", "episode", "radio"
- translation: Keywords like "dịch", "translate", "ngôn ngữ", "language"
- education_module: Keywords like "lesson", "course", "education", "bài giảng", "khóa học"
- general_inquiry: ONLY if absolutely none of the above

For this request, detect if they want to CREATE content (video/podcast/education) or just asking questions.

Example: "Tôi cần tạo video" -> video_creation
Example: "Create video from report" -> video_creation

Please provide:
1. A warm greeting in same language (1-2 sentences)
2. The PRIMARY service they need (be specific!)
3. Confidence level (0.0-1.0)
4. Keywords that helped you decide
5. Language: vi or en
6. Complexity: simple, moderate, or complex"""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7
            )
            
            response_text = response.content[0].text
            greeting, intent_data = self.handler.parse_intent_response(response_text)
            
            # Create intent object
            intent = CustomerIntent(
                primary_service=ServiceType(intent_data.get('service', 'general_inquiry')),
                confidence=float(intent_data.get('confidence', 0.7)),
                keywords=intent_data.get('keywords', request.split()[:5]),
                language=intent_data.get('language', 'vi'),
                complexity=intent_data.get('complexity', 'moderate')
            )
            
            return greeting or f"Xin chào {customer_name}!", intent
            
        except Exception as e:
            print(f"Claude API error: {e}")
            return self._fallback_greeting(customer_name, request)
    
    async def generate_smart_questions(self, request: str, intent: CustomerIntent, context: Optional[str] = None) -> List[SmartQuestion]:
        """Generate intelligent questions with Claude"""
        
        if not self.claude:
            return self._fallback_questions(intent)
        
        prompt = f"""Based on this {intent.primary_service.value} request: "{request}"

Generate 1-3 essential questions to gather missing requirements.
Only ask what's absolutely necessary.

Context: {context if context else 'None'}
Language: {intent.language}

For each question, consider:
- What information is missing?
- What would improve the output quality?
- What's specific to {intent.primary_service.value}?

Keep questions natural and conversational."""

        try:
            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.8
            )
            
            response_text = response.content[0].text
            questions_data = self.handler.parse_questions_response(response_text)
            
            questions = []
            for q_data in questions_data[:self.max_questions]:
                if isinstance(q_data, dict):
                    questions.append(SmartQuestion(
                        question=q_data.get('question', ''),
                        purpose=q_data.get('purpose', 'Gather requirements'),
                        expected_type=q_data.get('expected_type', 'text')
                    ))
                elif isinstance(q_data, str):
                    questions.append(SmartQuestion(
                        question=q_data,
                        purpose='Gather requirements',
                        expected_type='text'
                    ))
            
            return questions if questions else self._fallback_questions(intent)
            
        except Exception as e:
            print(f"Questions generation error: {e}")
            return self._fallback_questions(intent)
    
        def _fallback_greeting(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """Fallback when API unavailable"""
        request_lower = request.lower()
        
        # More comprehensive keyword matching
        if any(word in request_lower for word in ['video', 'clip', 'visual', 'youtube', 'tiktok', 'phim', 'tạo video']):
            service = ServiceType.VIDEO_CREATION
        elif any(word in request_lower for word in ['podcast', 'audio', 'episode', 'radio']):
            service = ServiceType.PODCAST_GENERATION
        elif any(word in request_lower for word in ['dịch', 'translate', 'translation', 'ngôn ngữ']):
            service = ServiceType.TRANSLATION
        elif any(word in request_lower for word in ['education', 'giáo dục', 'lesson', 'bài giảng', 'course']):
            service = ServiceType.EDUCATION_MODULE
        else:
            service = ServiceType.GENERAL_INQUIRY
        
        # Better greeting based on detected service
        greetings = {
            ServiceType.VIDEO_CREATION: f"Xin chào {customer_name}! Tôi sẽ giúp bạn tạo video chuyên nghiệp.",
            ServiceType.PODCAST_GENERATION: f"Hi {customer_name}! I'll help you create an engaging podcast.",
            ServiceType.TRANSLATION: f"Xin chào {customer_name}! Tôi sẽ hỗ trợ dịch thuật cho bạn.",
            ServiceType.GENERAL_INQUIRY: f"Xin chào {customer_name}! Tôi sẵn sàng hỗ trợ bạn."
        }
        
        greeting = greetings.get(service, greetings[ServiceType.GENERAL_INQUIRY])
        
        intent = CustomerIntent(
            primary_service=service,
            confidence=0.8 if service != ServiceType.GENERAL_INQUIRY else 0.5,
            keywords=[w for w in request.split() if len(w) > 2][:5],
            language='vi' if any(ord(c) > 127 for c in request) else 'en',
            complexity='moderate'
        )
        
        return greeting, intent
    
    def _fallback_questions(self, intent: CustomerIntent) -> List[SmartQuestion]:
        """Fallback questions when API unavailable"""
        questions_map = {
            ServiceType.VIDEO_CREATION: [
                SmartQuestion("Thời lượng video mong muốn (phút)?", "Duration", "number"),
                SmartQuestion("Platform nào (YouTube/TikTok)?", "Platform", "choice"),
                SmartQuestion("Phong cách video?", "Style", "choice")
            ],
            ServiceType.PODCAST_GENERATION: [
                SmartQuestion("Podcast dài bao nhiêu phút?", "Duration", "number"),
                SmartQuestion("Đối tượng nghe?", "Audience", "text"),
                SmartQuestion("Tone giọng?", "Tone", "choice")
            ]
        }
        
        return questions_map.get(intent.primary_service, [])[:self.max_questions]


# Test the commander
async def test_intelligent_claude():
    """Test intelligent Claude commander"""
    commander = IntelligentClaudeCommander()
    
    test_cases = [
        ("Anh Minh", "Tôi cần tạo video từ báo cáo tài chính Q4 cho nhà đầu tư"),
        ("Sarah", "I need a podcast about AI trends in healthcare for doctors"),
        ("Chị Lan", "Dịch tài liệu kỹ thuật 50 trang sang tiếng Anh")
    ]
    
    for name, request in test_cases:
        print(f"\n{'='*60}")
        print(f"👤 Customer: {name}")
        print(f"📝 Request: {request}")
        
        # Get greeting and intent
        greeting, intent = await commander.greet_and_analyze(name, request)
        
        print(f"\n🤖 Claude: {greeting}")
        print(f"📊 Analysis:")
        print(f"   - Service: {intent.primary_service.value}")
        print(f"   - Confidence: {intent.confidence:.0%}")
        print(f"   - Language: {intent.language}")
        print(f"   - Complexity: {intent.complexity}")
        
        # Generate questions
        questions = await commander.generate_smart_questions(request, intent)
        
        if questions:
            print(f"\n❓ Smart Questions:")
            for i, q in enumerate(questions, 1):
                print(f"   {i}. {q.question}")
    
    print(f"\n{'='*60}")
    print("✅ Intelligent Claude Commander with robust parsing!")


if __name__ == "__main__":
    asyncio.run(test_intelligent_claude())
