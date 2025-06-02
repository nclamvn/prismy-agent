"""
Complete AI Commander Integration
Connect Claude Commander with actual PRISM services
"""

import asyncio
from typing import Dict, Any, Optional, List, Tuple
import json

# Import Claude Commander
from intelligent_claude_commander import TrueClaudeCommander, CustomerIntent, ServiceType

# Import PRISM services
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.infrastructure.content_transformation import (
    TransformationManager,
    TransformationRequest,
    TransformationType,
    TargetAudience,
    ContentDifficulty
)


class CompleteAICommander:
    """
    Complete AI Commander with full PRISM integration
    Claude as conductor + PRISM services as orchestra
    """
    
    def __init__(self):
        self.claude = TrueClaudeCommander()
        self.transformation_manager = TransformationManager()
        
        # Service mapping
        self.service_map = {
            ServiceType.VIDEO_CREATION: TransformationType.VIDEO_SCENARIO,
            ServiceType.PODCAST_GENERATION: TransformationType.PODCAST_SCRIPT,
            ServiceType.EDUCATION_MODULE: TransformationType.EDUCATION_MODULE,
            # Note: Translation would need separate handling
        }
        
        # Audience mapping based on complexity
        self.audience_map = {
            'simple': TargetAudience.CHILDREN,
            'moderate': TargetAudience.ADULTS,
            'complex': TargetAudience.PROFESSIONALS
        }
    
    async def serve_customer_complete(
        self,
        customer_name: str,
        request: str,
        provided_content: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Complete customer service flow from greeting to delivery
        """
        
        print(f"\n{'='*60}")
        print(f"🎯 Starting complete service for {customer_name}")
        
        # Step 1: Greet and analyze
        greeting, intent = await self.claude.greet_and_analyze(customer_name, request)
        print(f"\n💬 Claude: {greeting}")
        print(f"📊 Detected: {intent.primary_service.value} ({intent.confidence:.0%})")
        
        # Step 2: Check if we can handle this service
        if intent.primary_service not in self.service_map:
            return {
                "success": False,
                "message": f"Service {intent.primary_service.value} not yet implemented",
                "greeting": greeting,
                "intent": intent
            }
        
        # Step 3: Generate smart questions
        questions = await self.claude.generate_smart_questions(request, intent, provided_content)
        
        if questions:
            print(f"\n❓ Claude asks:")
            for i, q in enumerate(questions, 1):
                print(f"   {i}. {q.question}")
        
        # Step 4: Simulate answers (in real app, wait for user)
        answers = self._simulate_customer_answers(questions, intent)
        print(f"\n💭 Customer provides answers...")
        
        # Step 5: Execute transformation
        print(f"\n⚡ Executing {intent.primary_service.value} service...")
        
        try:
            # Create transformation request
            trans_request = TransformationRequest(
                source_text=provided_content or request,
                transformation_type=self.service_map[intent.primary_service],
                target_audience=self.audience_map.get(intent.complexity, TargetAudience.ADULTS),
                difficulty_level=ContentDifficulty.INTERMEDIATE,
                language=intent.language,
                duration_target=answers.get('duration', 5)
            )
            
            # Execute transformation
            response = await self.transformation_manager.transform_content(trans_request)
            
            if response.transformed_content:
                print(f"✅ Success! Quality score: {response.quality_score:.2f}")
                
                # Extract key info based on service type
                if intent.primary_service == ServiceType.VIDEO_CREATION:
                    result_preview = self._preview_video_result(response)
                elif intent.primary_service == ServiceType.PODCAST_GENERATION:
                    result_preview = self._preview_podcast_result(response)
                else:
                    result_preview = "Content transformed successfully!"
                
                print(f"\n📦 Result preview:")
                print(result_preview)
                
                return {
                    "success": True,
                    "greeting": greeting,
                    "intent": intent,
                    "questions": questions,
                    "transformation_response": response,
                    "preview": result_preview
                }
            else:
                raise Exception("No transformed content")
                
        except Exception as e:
            print(f"❌ Service error: {e}")
            return {
                "success": False,
                "error": str(e),
                "greeting": greeting,
                "intent": intent
            }
    
    def _simulate_customer_answers(self, questions: List, intent: CustomerIntent) -> Dict[str, Any]:
        """Simulate customer answers for testing"""
        answers = {
            'duration': 60,  # 1 minute default
            'platform': 'youtube',
            'style': 'professional',
            'audience': 'business professionals',
            'tone': 'conversational'
        }
        return answers
    
    def _preview_video_result(self, response) -> str:
        """Preview video transformation result"""
        try:
            data = json.loads(response.transformed_content)
            if 'content' in data and 'prompts' in data['content']:
                prompts = data['content']['prompts']
                return f"Generated {len(prompts)} video scenes for {data['content']['platform']}"
            else:
                return "Video script generated successfully"
        except:
            return "Video content created"
    
    def _preview_podcast_result(self, response) -> str:
        """Preview podcast transformation result"""
        try:
            # Extract first 200 chars of podcast script
            content = response.transformed_content[:200] + "..."
            return f"Podcast intro: {content}"
        except:
            return "Podcast script created"


# Test complete flow
async def test_complete_commander():
    """Test the complete AI Commander flow"""
    commander = CompleteAICommander()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Anh Minh",
            "request": "Tôi cần tạo video từ báo cáo tài chính Q4 cho nhà đầu tư",
            "content": "Doanh thu Q4 tăng 25% so với cùng kỳ. EBITDA margin đạt 22%. ROI từ R&D investment là 340%."
        },
        {
            "name": "Sarah",
            "request": "Create a podcast episode about AI trends in healthcare",
            "content": "AI is revolutionizing diagnostics, drug discovery, and personalized medicine..."
        }
    ]
    
    for scenario in scenarios:
        result = await commander.serve_customer_complete(
            scenario["name"],
            scenario["request"],
            scenario["content"]
        )
        
        if result["success"]:
            print(f"\n🎉 Service completed successfully!")
        else:
            print(f"\n⚠️ Service incomplete: {result.get('message', result.get('error'))}")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # Save to proper location
    print("Complete AI Commander ready for testing!")
    asyncio.run(test_complete_commander())
