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

Please:
1. Create a warm, professional greeting in the same language as the request
2. Analyze their intent

Provide:
- A natural greeting (1-2 sentences)
- Service type: translation, video_creation, podcast_generation, education_module, or general_inquiry
- Confidence: 0.0 to 1.0
- Keywords: main keywords from request
- Language: vi or en
- Complexity: simple, moderate, or complex

You can respond in any format - natural text, JSON, or mixed."""

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
        # Simple intent detection
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['video', 'clip']):
            service = ServiceType.VIDEO_CREATION
        elif 'podcast' in request_lower:
            service = ServiceType.PODCAST_GENERATION
        elif any(word in request_lower for word in ['dịch', 'translate']):
            service = ServiceType.TRANSLATION
        elif any(word in request_lower for word in ['education', 'giáo dục', 'lesson']):
            service = ServiceType.EDUCATION_MODULE
        else:
            service = ServiceType.GENERAL_INQUIRY
        
        greeting = f"Xin chào {customer_name}! Tôi sẽ hỗ trợ bạn với yêu cầu này."
        
        intent = CustomerIntent(
            primary_service=service,
            confidence=0.7,
            keywords=request.split()[:5],
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
