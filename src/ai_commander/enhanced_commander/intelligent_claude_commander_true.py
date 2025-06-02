"""
True Claude Integration - Claude analyzes EVERYTHING
No keyword shortcuts, pure AI intelligence
"""

import anthropic
import asyncio
from typing import Dict, Any, Optional, List, Tuple
import os
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

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


class TrueClaudeCommander:
    """
    True Claude Integration - Claude handles EVERYTHING
    """
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.handler = ClaudeResponseHandler()
        self.max_questions = 3
        
        if not self.claude:
            print("⚠️ WARNING: No Claude API key - using fallback mode")
        else:
            print("✅ Claude API connected - full AI intelligence active")
    
    async def greet_and_analyze(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """
        ALWAYS use Claude for analysis - no shortcuts
        """
        
        # CLAUDE FIRST - Always
        if self.claude:
            try:
                # Enhanced prompt for better accuracy
                prompt = f"""You are an AI concierge for PRISM platform.

Customer: {customer_name}
Request: "{request}"

Analyze what service they need:
- video_creation: They want to CREATE/MAKE/PRODUCE videos (keywords: video, clip, youtube, tiktok, visual content)
- podcast_generation: They want to CREATE/MAKE podcasts or audio content
- translation: They need to translate/convert between languages
- education_module: They need educational/training/lesson content
- general_inquiry: ONLY if absolutely none of the above match

Think step by step:
1. What is the customer trying to CREATE or DO?
2. Which service best matches their need?
3. How confident are you? (0.0-1.0)

Respond in this format:
Greeting: [Natural greeting in the same language as request]
Service: [exact service name from list above]
Confidence: [0.0-1.0]
Language: [vi or en]
Keywords: [main keywords that helped you decide]"""

                # Call Claude
                response = self.claude.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=300,
                    temperature=0.3  # Lower temperature for consistency
                )
                
                response_text = response.content[0].text
                print(f"🤖 Claude analyzed: {response_text[:100]}...")
                
                # Parse response
                greeting, intent_data = self.handler.parse_intent_response(response_text)
                
                # Extract keywords from response if provided
                keywords = intent_data.get('keywords', [])
                if isinstance(keywords, str):
                    keywords = [k.strip() for k in keywords.split(',')][:5]
                elif not keywords:
                    keywords = request.split()[:5]
                
                # Create intent
                intent = CustomerIntent(
                    primary_service=ServiceType(intent_data.get('service', 'general_inquiry')),
                    confidence=float(intent_data.get('confidence', 0.8)),
                    keywords=keywords,
                    language=intent_data.get('language', 'vi'),
                    complexity=intent_data.get('complexity', 'moderate')
                )
                
                # Use Claude's greeting or create one
                if not greeting or len(greeting) < 10:
                    greeting = self._create_greeting(customer_name, intent)
                
                print(f"✅ Claude decision: {intent.primary_service.value} ({intent.confidence:.0%})")
                return greeting, intent
                
            except Exception as e:
                print(f"❌ Claude error: {e}")
                # Only use fallback if Claude completely fails
                return self._emergency_fallback(customer_name, request)
        
        # No Claude available - use emergency fallback
        return self._emergency_fallback(customer_name, request)
    
    def _create_greeting(self, customer_name: str, intent: CustomerIntent) -> str:
        """Create appropriate greeting based on intent"""
        greetings = {
            ServiceType.VIDEO_CREATION: {
                'vi': f"Xin chào {customer_name}! Tôi sẽ giúp bạn tạo video chuyên nghiệp từ nội dung của bạn.",
                'en': f"Hi {customer_name}! I'll help you create professional videos from your content."
            },
            ServiceType.PODCAST_GENERATION: {
                'vi': f"Chào {customer_name}! Tôi sẽ hỗ trợ bạn tạo podcast hấp dẫn.",
                'en': f"Hello {customer_name}! I'll help you create an engaging podcast."
            },
            ServiceType.TRANSLATION: {
                'vi': f"Xin chào {customer_name}! Tôi sẽ giúp bạn dịch tài liệu chính xác.",
                'en': f"Hi {customer_name}! I'll help you translate your documents accurately."
            },
            ServiceType.GENERAL_INQUIRY: {
                'vi': f"Xin chào {customer_name}! Tôi sẵn sàng hỗ trợ bạn.",
                'en': f"Hello {customer_name}! I'm here to help you."
            }
        }
        
        service_greetings = greetings.get(intent.primary_service, greetings[ServiceType.GENERAL_INQUIRY])
        return service_greetings.get(intent.language, service_greetings['en'])
    
    def _emergency_fallback(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """
        Emergency fallback - only when Claude is completely unavailable
        Uses simple keyword matching as last resort
        """
        print("⚠️ Using emergency fallback (Claude unavailable)")
        
        request_lower = request.lower()
        
        # Simple keyword detection
        if any(word in request_lower for word in ['video', 'clip', 'youtube', 'tiktok', 'phim']):
            service = ServiceType.VIDEO_CREATION
        elif any(word in request_lower for word in ['podcast', 'audio', 'radio']):
            service = ServiceType.PODCAST_GENERATION
        elif any(word in request_lower for word in ['dịch', 'translate', 'translation']):
            service = ServiceType.TRANSLATION
        elif any(word in request_lower for word in ['education', 'lesson', 'học', 'giáo dục']):
            service = ServiceType.EDUCATION_MODULE
        else:
            service = ServiceType.GENERAL_INQUIRY
        
        intent = CustomerIntent(
            primary_service=service,
            confidence=0.6,  # Lower confidence for fallback
            keywords=request.split()[:5],
            language='vi' if any(ord(c) > 127 for c in request) else 'en',
            complexity='moderate'
        )
        
        greeting = self._create_greeting(customer_name, intent)
        return greeting, intent
    
    async def generate_smart_questions(self, request: str, intent: CustomerIntent, context: Optional[str] = None) -> List[SmartQuestion]:
        """
        Generate intelligent questions using Claude
        """
        if not self.claude:
            return self._fallback_questions(intent)
        
        try:
            prompt = f"""Based on this {intent.primary_service.value} request: "{request}"

Generate 1-3 essential questions to gather missing information.
Consider what's needed for high-quality {intent.primary_service.value}.

Current context: {context if context else 'None provided'}
Language: {intent.language}

For each question:
1. What specific information is missing?
2. Why is it important?
3. Keep questions natural and conversational

Format:
Question: [question text]
Purpose: [why needed]
Type: [text/number/choice]"""

            response = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.7
            )
            
            # Parse questions from response
            questions = self.handler.parse_questions_response(response.content[0].text)
            
            # Convert to SmartQuestion objects
            smart_questions = []
            for q in questions[:self.max_questions]:
                if isinstance(q, dict):
                    smart_questions.append(SmartQuestion(
                        question=q.get('question', ''),
                        purpose=q.get('purpose', 'Gather information'),
                        expected_type=q.get('expected_type', 'text')
                    ))
            
            return smart_questions if smart_questions else self._fallback_questions(intent)
            
        except Exception as e:
            print(f"❌ Questions generation error: {e}")
            return self._fallback_questions(intent)
    
    def _fallback_questions(self, intent: CustomerIntent) -> List[SmartQuestion]:
        """Fallback questions when Claude unavailable"""
        questions_map = {
            ServiceType.VIDEO_CREATION: [
                SmartQuestion("Video dài bao nhiêu phút?", "Determine duration", "number"),
                SmartQuestion("Dùng cho platform nào?", "Platform optimization", "choice")
            ],
            ServiceType.PODCAST_GENERATION: [
                SmartQuestion("Podcast duration?", "Set episode length", "number"),
                SmartQuestion("Who's your target audience?", "Content optimization", "text")
            ],
            ServiceType.TRANSLATION: [
                SmartQuestion("Translate to which language?", "Target language", "text"),
                SmartQuestion("Document type?", "Style selection", "choice")
            ]
        }
        return questions_map.get(intent.primary_service, [])[:self.max_questions]


# Test the true integration
async def test_true_claude():
    """Test true Claude integration"""
    commander = TrueClaudeCommander()
    
    test_cases = [
        ("Anh Minh", "Tôi cần tạo video từ báo cáo tài chính Q4"),
        ("Sarah", "I want to create a podcast about AI trends"),
        ("Chị Lan", "Dịch hộ tôi tài liệu này sang tiếng Anh"),
        ("John", "I need help with something"),  # Vague request
        ("Mai", "Làm content cho YouTube về cooking"),  # Indirect video request
    ]
    
    print("\n" + "="*60)
    print("🧪 TESTING TRUE CLAUDE INTEGRATION")
    print("="*60)
    
    for name, request in test_cases:
        print(f"\n{'='*50}")
        print(f"👤 Customer: {name}")
        print(f"💬 Request: {request}")
        
        # Analyze with Claude
        greeting, intent = await commander.greet_and_analyze(name, request)
        
        print(f"\n🤖 Greeting: {greeting}")
        print(f"🎯 Service: {intent.primary_service.value}")
        print(f"📊 Confidence: {intent.confidence:.0%}")
        print(f"🔑 Keywords: {', '.join(intent.keywords)}")
        
        # Generate questions
        questions = await commander.generate_smart_questions(request, intent)
        if questions:
            print(f"\n❓ Smart Questions:")
            for i, q in enumerate(questions, 1):
                print(f"   {i}. {q.question}")
                print(f"      Purpose: {q.purpose}")


if __name__ == "__main__":
    asyncio.run(test_true_claude())
