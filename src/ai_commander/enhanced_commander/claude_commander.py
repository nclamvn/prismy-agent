"""
Claude Sonnet AI Commander - Professional Customer Service Experience
Giao tiếp thông minh với khách hàng từ nhận yêu cầu đến trả kết quả
"""

import asyncio
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass
import time

# Import existing AI Commander components
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_analysis import IntentAnalyzer, IntentAnalysisResult
from requirement_collector import SmartRequirementCollector, RequirementCollectionResult
from workflow_orchestration import WorkflowOrchestrator, WorkflowResult
from adaptive_learning import AdaptiveLearner

# Content transformation integration
try:
    from src.infrastructure.content_transformation.transformation_manager import TransformationManager
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from src.infrastructure.content_transformation.transformation_manager import TransformationManager


@dataclass
class CustomerConversation:
    """Cuộc hội thoại với khách hàng"""
    session_id: str
    customer_input: str
    content: Optional[str] = None
    claude_greeting: str = ""
    smart_questions: list = None
    customer_answers: Dict[str, str] = None
    final_result: str = ""
    conversation_history: list = None
    
    def __post_init__(self):
        if self.smart_questions is None:
            self.smart_questions = []
        if self.customer_answers is None:
            self.customer_answers = {}
        if self.conversation_history is None:
            self.conversation_history = []


class ClaudeSonnetCommander:
    """
    Claude Sonnet powered AI Commander
    Chuyên gia tư vấn và xử lý yêu cầu khách hàng
    """
    
    def __init__(self):
        """Initialize Claude Sonnet AI Commander"""
        print("🤖 Initializing Claude Sonnet AI Commander...")
        
        # Initialize backend AI systems
        self.intent_analyzer = IntentAnalyzer()
        self.requirement_collector = SmartRequirementCollector()
        self.workflow_orchestrator = WorkflowOrchestrator()
        self.adaptive_learner = AdaptiveLearner()
        
        # Initialize content transformation
        self.transformation_manager = TransformationManager()
        
        # Claude conversation templates
        self.conversation_templates = self._load_conversation_templates()
        
        print("✅ Claude Sonnet AI Commander ready for customer service!")
    
    def _load_conversation_templates(self) -> Dict[str, str]:
        """Load professional conversation templates"""
        return {
            "greeting_template": """
Chào {customer_name}! Tôi là Claude, trợ lý AI thông minh của hệ thống dịch thuật.

Tôi hiểu bạn muốn: "{customer_request}"

{intent_analysis}

Để đảm bảo kết quả hoàn hảo nhất, cho tôi hỏi thêm:
{smart_questions}

Tôi sẽ xử lý ngay khi nhận được thông tin từ bạn! 🚀
            """,
            
            "processing_template": """
Cảm ơn bạn! Tôi đã hiểu rõ yêu cầu:

📋 Yêu cầu: {intent}
👤 Đối tượng: {audience}  
🎯 Chất lượng: {quality_target}
⚡ Chiến lược: {strategy}

Đang xử lý với hệ thống AI 7 tầng... ⏳
            """,
            
            "completion_template": """
✅ Hoàn thành! Đây là kết quả cho bạn:

{result_content}

📊 Thông tin kỹ thuật:
- Chất lượng đạt được: {quality}%
- Thời gian xử lý: {processing_time}s
- Chiến lược: {strategy}
- AI stages: {ai_stages}

{additional_suggestions}

Bạn có hài lòng với kết quả này không? Cần điều chỉnh gì thêm không ạ? 💬
            """
        }
    
    async def handle_customer_request(self, customer_input: str, 
                                    customer_name: str = "bạn",
                                    content: str = None) -> CustomerConversation:
        """
        Xử lý yêu cầu khách hàng với trải nghiệm chuyên nghiệp
        
        Args:
            customer_input: Yêu cầu của khách hàng
            customer_name: Tên khách hàng (tùy chọn)
            content: Nội dung cần xử lý (nếu có)
            
        Returns:
            CustomerConversation: Cuộc hội thoại hoàn chỉnh
        """
        session_id = f"session_{int(time.time())}"
        conversation = CustomerConversation(
            session_id=session_id,
            customer_input=customer_input,
            content=content
        )
        
        print(f"🤖 Claude Commander processing request: {customer_input}")
        
        # STEP 1: CLAUDE ANALYZES INTENT & CREATES GREETING
        print("🧠 Step 1: Intelligent intent analysis...")
        intent_result = self.intent_analyzer.analyze_intent(customer_input)
        
        # STEP 2: CLAUDE GENERATES SMART QUESTIONS
        print("🤔 Step 2: Generating smart questions...")
        req_result = self.requirement_collector.collect_requirements(intent_result)
        
        # STEP 3: CLAUDE CREATES PROFESSIONAL GREETING
        conversation.claude_greeting = self._create_claude_greeting(
            customer_input, customer_name, intent_result, req_result
        )
        conversation.smart_questions = [q.text for q in req_result.questions_asked]
        
        print("💬 Claude greeting created!")
        
        # STEP 4: SIMULATE CUSTOMER ANSWERS (in real app, wait for customer)
        print("⏳ Simulating customer answers...")
        conversation.customer_answers = self._simulate_customer_answers(req_result.questions_asked)
        
        # STEP 5: CLAUDE PROCESSES WITH AI INTELLIGENCE
        print("⚡ Step 5: Processing with AI intelligence...")
        processing_message = self._create_processing_message(intent_result, conversation.customer_answers)
        conversation.conversation_history.append(processing_message)
        
        # STEP 6: EXECUTE WORKFLOW
        workflow_result = await self.workflow_orchestrator.orchestrate_workflow(
            intent_result, req_result, content or customer_input
        )

        # Process content transformation if applicable
        if workflow_result.success and hasattr(self, 'transformation_manager'):
            trans_result = await self.process_transformation_request(
                intent_result, 
                req_result,
                {'content': customer_input, 'context': content}
            )
            if trans_result:
                workflow_result.output_data['transformation_result'] = trans_result

        
        # STEP 7: CLAUDE DELIVERS PROFESSIONAL RESULTS
        print("🎯 Step 7: Delivering professional results...")
        conversation.final_result = self._create_completion_message(
            workflow_result, intent_result, conversation.customer_answers
        )
        
        # STEP 8: RECORD LEARNING EVENT
        self.adaptive_learner.record_learning_event(
            customer_input, intent_result, req_result, workflow_result
        )
        
        print(f"✅ Customer service completed for session {session_id}")
        return conversation

    async def process_transformation_request(self, intent_result, req_result, customer_info):
        """Process content transformation based on customer requirements"""
        try:
            # Map intent to transformation type
            transformation_map = {
                "create_podcast": "podcast",
                "create_video": "video", 
                "create_education": "education"
            }
            
            trans_type = transformation_map.get(intent_result.primary_intent)
            if not trans_type:
                return None
                
            # Create transformation request
            from src.infrastructure.content_transformation.base_transformer import TransformationRequest
            trans_request = TransformationRequest(
                source_text=customer_info.get('content', ''),
                transformation_type=trans_type,
                target_audience=req_result.requirements.get('audience', 'general'),
                context=customer_info.get('context', '')
            )
            
            # Process with transformation manager
            result = await self.transformation_manager.transform_content(trans_request)
            return result
            
        except Exception as e:
            print(f"Transformation error: {e}")
            return None


    async def process_transformation_request(self, intent_result, req_result, customer_info):
        """Process content transformation based on customer requirements"""
        try:
            # Map intent to transformation type
            transformation_map = {
                "create_podcast": "podcast",
                "create_video": "video", 
                "create_education": "education"
            }
            
            trans_type = transformation_map.get(intent_result.primary_intent)
            if not trans_type:
                return None
                
            # Create transformation request
            from src.infrastructure.content_transformation.base_transformer import TransformationRequest
            trans_request = TransformationRequest(
                source_text=customer_info.get('content', ''),
                transformation_type=trans_type,
                target_audience=req_result.requirements.get('audience', 'general'),
                context=customer_info.get('context', '')
            )
            
            # Process with transformation manager
            result = await self.transformation_manager.transform_content(trans_request)
            return result
            
        except Exception as e:
            print(f"Transformation error: {e}")
            return None

    
    def _create_claude_greeting(self, customer_input: str, customer_name: str,
                              intent_result: IntentAnalysisResult,
                              req_result: RequirementCollectionResult) -> str:
        """Create professional Claude greeting"""
        
        # Analyze intent for greeting
        intent_descriptions = {
            "create_podcast": "tạo podcast script chuyên nghiệp",
            "create_video": "tạo video scenario hấp dẫn", 
            "create_education": "tạo module học tập tương tác",
            "translate_only": "dịch thuật chính xác",
            "analyze_content": "phân tích nội dung chi tiết"
        }
        
        intent_desc = intent_descriptions.get(intent_result.primary_intent.value, "xử lý nội dung")
        
        # Create smart questions text
        questions_text = ""
        for i, question in enumerate(req_result.questions_asked, 1):
            questions_text += f"{i}. {question.text}\n"
        
        if not questions_text:
            questions_text = "Tôi có đủ thông tin để bắt đầu xử lý ngay!"
        
        greeting = self.conversation_templates["greeting_template"].format(
            customer_name=customer_name,
            customer_request=customer_input,
            intent_analysis=f"🎯 Tôi nhận thấy bạn muốn {intent_desc} (độ tin cậy: {intent_result.confidence_score:.0%})",
            smart_questions=questions_text
        )
        
        return greeting.strip()
    
    def _simulate_customer_answers(self, questions) -> Dict[str, str]:
        """Simulate customer answers (in real app, collect from UI)"""
        answers = {}
        
        # Intelligent defaults based on question types
        for question in questions:
            if "thời lượng" in question.text.lower():
                if "podcast" in question.text.lower():
                    answers[question.id] = "15-20 phút"
                else:
                    answers[question.id] = "5-10 phút"
            elif "phong cách" in question.text.lower():
                answers[question.id] = "Chuyên nghiệp, dễ hiểu"
            elif "đối tượng" in question.text.lower():
                answers[question.id] = "Nhân viên công ty"
            elif "loại" in question.text.lower():
                answers[question.id] = "Presentation chuyên nghiệp"
            else:
                answers[question.id] = "Theo gợi ý của AI Commander"
        
        return answers
    
    def _create_processing_message(self, intent_result: IntentAnalysisResult, 
                                 customer_answers: Dict[str, str]) -> str:
        """Create processing status message"""
        
        # Determine strategy based on user expertise
        strategy_mapping = {
            "professional": "Chất lượng tối đa",
            "advanced": "Cân bằng chất lượng-tốc độ", 
            "intermediate": "Tối ưu toàn diện",
            "beginner": "Tốc độ ưu tiên"
        }
        
        strategy = strategy_mapping.get(intent_result.user_expertise_level.value, "Cân bằng tối ưu")
        
        processing_msg = self.conversation_templates["processing_template"].format(
            intent=intent_result.primary_intent.value.replace("_", " ").title(),
            audience=customer_answers.get("target_audience", "Đa dạng"),
            quality_target="90%" if intent_result.user_expertise_level.value == "professional" else "85%",
            strategy=strategy
        )
        
        return processing_msg.strip()
    
    def _create_completion_message(self, workflow_result: WorkflowResult,
                                 intent_result: IntentAnalysisResult,
                                 customer_answers: Dict[str, str]) -> str:
        """Create professional completion message with results"""
        
        # Add suggestions based on result quality
        suggestions = ""
        if workflow_result.quality_achieved >= 0.9:
            suggestions = "🌟 Kết quả xuất sắc! Bạn có thể sử dụng ngay."
        elif workflow_result.quality_achieved >= 0.8:
            suggestions = "✨ Chất lượng tốt! Có thể cần điều chỉnh nhỏ theo sở thích."
        else:
            suggestions = "💡 Kết quả khả dụng. Đề xuất chạy lại với chế độ chất lượng cao hơn."
        
        completion_msg = self.conversation_templates["completion_template"].format(
            result_content=workflow_result.final_output,
            quality=f"{workflow_result.quality_achieved*100:.0f}",
            processing_time=f"{workflow_result.processing_time:.2f}",
            strategy=workflow_result.workflow_steps[0] if workflow_result.workflow_steps else "Auto-optimized",
            ai_stages=len(workflow_result.workflow_steps),
            additional_suggestions=suggestions
        )
        
        return completion_msg.strip()
    
    def display_conversation(self, conversation: CustomerConversation):
        """Display complete customer conversation"""
        print("\n" + "="*80)
        print("🤖 CLAUDE SONNET AI COMMANDER - CUSTOMER SERVICE LOG")
        print("="*80)
        
        print(f"\n📞 SESSION: {conversation.session_id}")
        print(f"📝 CUSTOMER REQUEST: {conversation.customer_input}")
        
        print(f"\n💬 CLAUDE GREETING:")
        print("-" * 50)
        print(conversation.claude_greeting)
        
        if conversation.customer_answers:
            print(f"\n📋 CUSTOMER ANSWERS:")
            for question_id, answer in conversation.customer_answers.items():
                print(f"   • {question_id}: {answer}")
        
        if conversation.conversation_history:
            print(f"\n⚡ PROCESSING STATUS:")
            print("-" * 50)
            for message in conversation.conversation_history:
                print(message)
        
        print(f"\n🎯 FINAL RESULT:")
        print("-" * 50)
        print(conversation.final_result)
        
        print("\n" + "="*80)
        print("✅ CUSTOMER SERVICE COMPLETED")
        print("="*80)


# Test Claude Sonnet AI Commander
async def test_claude_commander():
    """Test Claude Sonnet AI Commander with customer scenarios"""
    
    commander = ClaudeSonnetCommander()
    
    print("🧪 TESTING CLAUDE SONNET AI COMMANDER")
    print("="*60)
    
    # Test Scenario 1: Professional Podcast Creation
    print("\n🎙️ SCENARIO 1: Professional Podcast Creation")
    conversation1 = await commander.handle_customer_request(
        customer_input="Tôi cần làm podcast doanh nghiệp từ báo cáo Q4 này",
        customer_name="Anh Minh",
        content="Doanh thu Q4 tăng 25% đạt 150 tỷ. EBITDA margin cải thiện lên 22%. ROI đầu tư R&D đạt 340%."
    )
    
    commander.display_conversation(conversation1)
    
    # Test Scenario 2: Educational Video
    print("\n\n🎬 SCENARIO 2: Educational Video Creation")
    conversation2 = await commander.handle_customer_request(
        customer_input="Làm video giải thích AI cho nhân viên mới",
        customer_name="Chị Lan",
        content="Artificial Intelligence là khả năng máy móc thực hiện các tác vụ thông minh như con người."
    )
    
    commander.display_conversation(conversation2)
    
    print("\n🏆 CLAUDE SONNET AI COMMANDER: READY FOR CUSTOMER SERVICE!")


if __name__ == "__main__":
    asyncio.run(test_claude_commander())
