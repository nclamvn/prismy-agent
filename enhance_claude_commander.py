"""
Enhanced Claude Commander with Hotel Concierge Workflow
Max 3 intelligent questions, smart routing, professional results
"""

import anthropic
import asyncio
import json
from typing import Dict, Any, Optional, List, Tuple
import os
from dataclasses import dataclass
from enum import Enum

# Load environment
from dotenv import load_dotenv
load_dotenv()


class ServiceType(Enum):
    """Types of services available"""
    TRANSLATION = "translation"
    VIDEO_CREATION = "video_creation"
    PODCAST_GENERATION = "podcast_generation"
    EDUCATION_MODULE = "education_module"
    GENERAL_INQUIRY = "general_inquiry"


@dataclass
class CustomerIntent:
    """Analyzed customer intent"""
    primary_service: ServiceType
    confidence: float
    keywords: List[str]
    language: str
    complexity: str  # simple, moderate, complex


@dataclass
class SmartQuestion:
    """Intelligent question for requirement gathering"""
    question: str
    purpose: str
    expected_type: str  # text, number, choice, file


class HotelConciergeClaude:
    """
    Claude as a Hotel Concierge - Professional, Smart, Efficient
    """
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.claude = anthropic.Anthropic(api_key=self.api_key) if self.api_key else None
        self.max_questions = 3
        
    async def greet_customer(self, customer_name: str, initial_request: str) -> Tuple[str, CustomerIntent]:
        """
        Professional greeting and intent analysis
        """
        if not self.claude:
            return self._mock_greeting(customer_name, initial_request)
            
        # Use Claude to analyze intent and create greeting
        prompt = f"""You are a professional AI concierge for PRISM AI Platform. 
A customer named {customer_name} just arrived with this request: "{initial_request}"

Analyze their intent and provide:
1. A warm, professional greeting (in Vietnamese if the request is in Vietnamese)
2. Classification of their primary service need
3. Confidence level (0-1)
4. Key keywords identified
5. Detected language
6. Complexity assessment

Format response as JSON:
{{
    "greeting": "...",
    "intent": {{
        "service": "translation|video_creation|podcast_generation|education_module|general_inquiry",
        "confidence": 0.85,
        "keywords": ["key1", "key2"],
        "language": "vi|en",
        "complexity": "simple|moderate|complex"
    }}
}}"""

        response = self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        result = json.loads(response.content[0].text)
        
        intent = CustomerIntent(
            primary_service=ServiceType(result['intent']['service']),
            confidence=result['intent']['confidence'],
            keywords=result['intent']['keywords'],
            language=result['intent']['language'],
            complexity=result['intent']['complexity']
        )
        
        return result['greeting'], intent
    
    async def gather_requirements(self, 
                                  initial_request: str, 
                                  intent: CustomerIntent,
                                  context: Optional[str] = None) -> List[SmartQuestion]:
        """
        Generate max 3 smart questions based on what's missing
        """
        if not self.claude:
            return self._mock_questions(intent)
        
        # Use Claude to generate smart questions
        prompt = f"""Based on this customer request for {intent.primary_service.value}:
"{initial_request}"

Context provided: {context if context else 'None'}

Generate UP TO 3 essential questions to gather missing requirements.
Only ask what's absolutely necessary. If the request is already complete, return empty list.

For each question provide:
1. The question text (in {intent.language})
2. Why it's needed
3. Expected answer type

Format as JSON:
{{
    "questions": [
        {{
            "question": "...",
            "purpose": "...",
            "expected_type": "text|number|choice|file"
        }}
    ]
}}"""

        response = self.claude.messages.create(
            model="claude-3-sonnet-20240229",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        result = json.loads(response.content[0].text)
        
        questions = []
        for q in result['questions'][:self.max_questions]:  # Enforce max 3
            questions.append(SmartQuestion(
                question=q['question'],
                purpose=q['purpose'],
                expected_type=q['expected_type']
            ))
            
        return questions
    
    async def route_to_service(self,
                               intent: CustomerIntent,
                               requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Smart routing to appropriate service with requirements
        """
        routing = {
            ServiceType.TRANSLATION: {
                "service": "TranslationService",
                "pipeline": "translation_pipeline",
                "required_params": ["source_text", "target_language", "document_type"]
            },
            ServiceType.VIDEO_CREATION: {
                "service": "UnifiedVideoProcessor", 
                "pipeline": "video_dna_pipeline",
                "required_params": ["content", "duration", "platform", "style"]
            },
            ServiceType.PODCAST_GENERATION: {
                "service": "PodcastGenerator",
                "pipeline": "podcast_pipeline", 
                "required_params": ["content", "duration", "target_audience", "tone"]
            },
            ServiceType.EDUCATION_MODULE: {
                "service": "EducationModuleBuilder",
                "pipeline": "education_pipeline",
                "required_params": ["content", "difficulty_level", "module_type", "duration"]
            }
        }
        
        service_config = routing.get(intent.primary_service, {})
        
        return {
            "service": service_config.get("service"),
            "pipeline": service_config.get("pipeline"),
            "parameters": requirements,
            "confidence": intent.confidence,
            "ready_to_process": self._validate_requirements(
                requirements, 
                service_config.get("required_params", [])
            )
        }
    
    def _validate_requirements(self, provided: Dict, required: List[str]) -> bool:
        """Check if all required parameters are provided"""
        return all(param in provided and provided[param] for param in required)
    
    def _mock_greeting(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """Fallback mock greeting"""
        greeting = f"Xin chào {customer_name}! Tôi là Claude, trợ lý AI của PRISM. "
        greeting += f"Tôi hiểu bạn cần: {request}. Để tối ưu kết quả, cho tôi hỏi thêm vài câu nhé!"
        
        # Simple intent detection
        intent = CustomerIntent(
            primary_service=ServiceType.GENERAL_INQUIRY,
            confidence=0.7,
            keywords=request.split()[:5],
            language="vi" if any(c > 'z' for c in request) else "en",
            complexity="moderate"
        )
        
        return greeting, intent
    
    def _mock_questions(self, intent: CustomerIntent) -> List[SmartQuestion]:
        """Fallback mock questions"""
        questions_map = {
            ServiceType.VIDEO_CREATION: [
                SmartQuestion("Thời lượng video mong muốn?", "Determine video length", "number"),
                SmartQuestion("Platform nào (YouTube/TikTok/Khác)?", "Platform optimization", "choice")
            ],
            ServiceType.PODCAST_GENERATION: [
                SmartQuestion("Đối tượng nghe là ai?", "Audience targeting", "text"),
                SmartQuestion("Tone giọng mong muốn?", "Style selection", "choice")
            ]
        }
        
        return questions_map.get(intent.primary_service, [])[:self.max_questions]


# Integration with existing system
class EnhancedProductionCommander:
    """
    Production Commander with Hotel Concierge Claude
    """
    
    def __init__(self):
        self.concierge = HotelConciergeClaude()
        # Import existing components
        try:
            from src.infrastructure.content_transformation import TransformationManager
            self.transformation_manager = TransformationManager()
        except:
            self.transformation_manager = None
            
    async def serve_customer(self, 
                             customer_name: str,
                             initial_request: str,
                             provided_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete customer service flow
        """
        # Step 1: Greet and analyze intent
        greeting, intent = await self.concierge.greet_customer(customer_name, initial_request)
        
        # Step 2: Gather requirements (max 3 questions)
        questions = await self.concierge.gather_requirements(
            initial_request, intent, provided_content
        )
        
        # Step 3: Simulate customer answers (in real app, would wait for responses)
        requirements = self._simulate_answers(questions, initial_request, provided_content)
        
        # Step 4: Route to appropriate service
        routing = await self.concierge.route_to_service(intent, requirements)
        
        # Step 5: Execute service (if ready)
        result = None
        if routing['ready_to_process'] and self.transformation_manager:
            result = await self._execute_service(routing)
        
        return {
            "greeting": greeting,
            "intent": intent,
            "questions": questions,
            "requirements": requirements,
            "routing": routing,
            "result": result,
            "success": bool(result)
        }
    
    def _simulate_answers(self, questions: List[SmartQuestion], 
                          request: str, content: str) -> Dict[str, Any]:
        """Simulate customer answers for testing"""
        answers = {
            "source_text": content or request,
            "target_language": "en",
            "duration": 60,
            "platform": "youtube", 
            "target_audience": "adults",
            "tone": "professional",
            "difficulty_level": "intermediate"
        }
        return answers
    
    async def _execute_service(self, routing: Dict[str, Any]) -> Any:
        """Execute the routed service"""
        # This would call the actual transformation manager
        return f"Executed {routing['service']} with {routing['pipeline']}"


# Test the enhanced commander
async def test_enhanced_claude():
    """Test the enhanced Claude Commander"""
    commander = EnhancedProductionCommander()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Anh Minh",
            "request": "Tôi cần tạo video từ báo cáo tài chính Q4",
            "content": "Revenue increased 25%, EBITDA margin at 22%"
        },
        {
            "name": "Ms. Sarah",
            "request": "Create a podcast from this blog post about AI trends",
            "content": "AI is transforming industries..."
        }
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"🎯 Customer: {scenario['name']}")
        print(f"📝 Request: {scenario['request']}")
        
        result = await commander.serve_customer(
            scenario['name'],
            scenario['request'],
            scenario.get('content')
        )
        
        print(f"\n💬 Claude: {result['greeting']}")
        print(f"🎯 Intent: {result['intent'].primary_service.value} "
              f"(confidence: {result['intent'].confidence:.0%})")
        
        if result['questions']:
            print(f"\n❓ Smart Questions (max 3):")
            for i, q in enumerate(result['questions'], 1):
                print(f"   {i}. {q.question}")
        
        print(f"\n🚀 Routing: {result['routing']['service']}")
        print(f"✅ Ready: {result['routing']['ready_to_process']}")
        
        if result['success']:
            print(f"🎉 Result: {result['result']}")


if __name__ == "__main__":
    # Save this as src/ai_commander/enhanced_commander/hotel_concierge_claude.py
    asyncio.run(test_enhanced_claude())
