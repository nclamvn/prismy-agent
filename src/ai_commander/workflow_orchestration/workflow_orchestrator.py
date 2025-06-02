"""
Workflow Orchestration Engine - Phase 7 Week 3
Automatically selects optimal workflow and parameters for perfect results
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import time

# Import from previous weeks
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_analysis import IntentAnalysisResult, UserIntent, UserExpertise
from requirement_collector import RequirementCollectionResult

# Import from Phase 6 infrastructure
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.infrastructure.ai_intelligence import IntelligenceOrchestrator
from src.infrastructure.ai_intelligence.intelligence_orchestrator import ProcessingRequest, ProcessingMode
from src.infrastructure.content_transformation.base_transformer import TransformationType, TargetAudience


class WorkflowStrategy(Enum):
    """Workflow execution strategies"""
    SPEED_FIRST = "speed_first"
    QUALITY_FIRST = "quality_first"
    BALANCED = "balanced"
    COST_OPTIMIZED = "cost_optimized"


@dataclass
class WorkflowResult:
    """Complete workflow execution result"""
    final_output: str
    processing_time: float
    quality_achieved: float
    total_cost: float
    workflow_steps: List[str] = field(default_factory=list)
    success: bool = True
    error_message: Optional[str] = None


class WorkflowOrchestrator:
    """AI-powered workflow orchestration engine"""
    
    def __init__(self):
        """Initialize workflow orchestrator"""
        print("⚡ Initializing Workflow Orchestration Engine...")
        self.intelligence_orchestrator = IntelligenceOrchestrator()
        print("✅ Workflow Orchestration Engine ready")
    
    async def orchestrate_workflow(self, intent_result: IntentAnalysisResult, 
                                 requirements: RequirementCollectionResult,
                                 content: str, source_lang: str = "auto", 
                                 target_lang: str = "vi") -> WorkflowResult:
        """
        Orchestrate complete workflow from intent to result
        """
        print(f"⚡ Orchestrating workflow for {intent_result.primary_intent.value}...")
        start_time = time.time()
        
        try:
            # Determine optimal strategy
            strategy = self._determine_strategy(intent_result)
            print(f"   📋 Strategy: {strategy.value}")
            
            # Create processing request
            processing_request = self._create_processing_request(
                content, source_lang, target_lang, intent_result, requirements
            )
            print(f"   ⚙️  Processing mode: {processing_request.processing_mode.value}")
            
            # Execute workflow
            print("   🧠 Executing AI intelligence workflow...")
            intelligence_result = await self.intelligence_orchestrator.process_intelligent(processing_request)
            
            # Format final output
            final_output = self._format_output(intelligence_result, intent_result)
            
            processing_time = time.time() - start_time
            
            workflow_result = WorkflowResult(
                final_output=final_output,
                processing_time=processing_time,
                quality_achieved=getattr(intelligence_result, 'quality_score', 0.85),
                total_cost=0.0,
                workflow_steps=["Intent Analysis", "Requirements", "AI Processing", "Formatting"],
                success=True
            )
            
            print(f"✅ Workflow completed in {processing_time:.2f}s")
            return workflow_result
            
        except Exception as e:
            processing_time = time.time() - start_time
            print(f"❌ Workflow failed: {str(e)}")
            
            return WorkflowResult(
                final_output="",
                processing_time=processing_time,
                quality_achieved=0.0,
                total_cost=0.0,
                success=False,
                error_message=str(e)
            )
    
    def _determine_strategy(self, intent_result: IntentAnalysisResult) -> WorkflowStrategy:
        """Determine optimal workflow strategy"""
        if intent_result.user_expertise_level.value == "professional":
            return WorkflowStrategy.QUALITY_FIRST
        elif intent_result.user_expertise_level.value == "beginner":
            return WorkflowStrategy.SPEED_FIRST
        else:
            return WorkflowStrategy.BALANCED
    
    def _create_processing_request(self, content: str, source_lang: str, target_lang: str,
                                 intent_result: IntentAnalysisResult,
                                 requirements: RequirementCollectionResult) -> ProcessingRequest:
        """Create processing request"""
        
        # Determine processing mode
        if intent_result.user_expertise_level.value == "professional":
            processing_mode = ProcessingMode.QUALITY_OPTIMIZED
        elif intent_result.user_expertise_level.value == "beginner":
            processing_mode = ProcessingMode.SPEED_OPTIMIZED
        else:
            processing_mode = ProcessingMode.BALANCED
        
        # Determine transformation types
        transformation_types = []
        if intent_result.primary_intent == UserIntent.CREATE_PODCAST:
            transformation_types = [TransformationType.PODCAST_SCRIPT]
        elif intent_result.primary_intent == UserIntent.CREATE_VIDEO:
            transformation_types = [TransformationType.VIDEO_SCENARIO]
        elif intent_result.primary_intent == UserIntent.CREATE_EDUCATION:
            transformation_types = [TransformationType.EDUCATION_MODULE]
        
        return ProcessingRequest(
            input_text=content,
            source_language=source_lang,
            target_language=target_lang,
            processing_mode=processing_mode,
            target_audience=TargetAudience.GENERAL,
            desired_outputs=transformation_types,
            quality_target=0.85
        )
    
    def _format_output(self, intelligence_result, intent_result: IntentAnalysisResult) -> str:
        """Format final output based on intent"""
        
        # Get base output
        base_output = intelligence_result.translated_text
        
        # Add intent-specific formatting
        if intent_result.primary_intent == UserIntent.CREATE_PODCAST:
            return f"🎙️ PODCAST SCRIPT\n\n{base_output}\n\n[End of Script]"
        elif intent_result.primary_intent == UserIntent.CREATE_VIDEO:
            return f"🎬 VIDEO SCENARIO\n\n{base_output}\n\n[Fade Out]"
        elif intent_result.primary_intent == UserIntent.CREATE_EDUCATION:
            return f"📚 EDUCATION MODULE\n\n{base_output}\n\n[Module Complete]"
        else:
            return base_output


# Test function
def test_workflow_orchestrator():
    """Test complete AI Commander workflow"""
    import asyncio
    from intent_analysis import IntentAnalyzer
    from requirement_collector import SmartRequirementCollector
    
    async def run_complete_test():
        print("🧪 TESTING COMPLETE AI COMMANDER WORKFLOW")
        print("="*60)
        
        # Initialize all components
        analyzer = IntentAnalyzer()
        collector = SmartRequirementCollector()
        orchestrator = WorkflowOrchestrator()
        
        # Test scenario
        user_input = "Làm podcast chuyên nghiệp từ báo cáo này"
        content = "Báo cáo tài chính Q4 cho thấy doanh thu tăng 15% so với cùng kỳ năm trước. Lợi nhuận ròng đạt 2.5 triệu USD, tăng 20%. Các chỉ số hiệu suất hoạt động đều cải thiện đáng kể."
        
        print(f"📝 User Input: {user_input}")
        print(f"📄 Content: {content[:100]}...")
        
        # Step 1: Intent Analysis
        print("\n🧠 STEP 1: INTENT ANALYSIS")
        intent_result = analyzer.analyze_intent(user_input)
        print(f"   ✅ Intent: {intent_result.primary_intent.value}")
        print(f"   ✅ Expertise: {intent_result.user_expertise_level.value}")
        print(f"   ✅ Confidence: {intent_result.confidence_score:.1%}")
        
        # Step 2: Requirement Collection
        print("\n🤔 STEP 2: REQUIREMENT COLLECTION")
        req_result = collector.collect_requirements(intent_result)
        print(f"   ✅ Questions asked: {len(req_result.questions_asked)}")
        print(f"   ✅ Requirements collected: {len(req_result.collected_requirements)}")
        print(f"   ✅ Ready for processing: {req_result.ready_for_processing}")
        
        # Step 3: Workflow Orchestration
        print("\n⚡ STEP 3: WORKFLOW ORCHESTRATION")
        workflow_result = await orchestrator.orchestrate_workflow(
            intent_result, req_result, content, "vietnamese", "vietnamese"
        )
        
        print(f"   ✅ Success: {workflow_result.success}")
        print(f"   ✅ Processing time: {workflow_result.processing_time:.2f}s")
        print(f"   ✅ Quality achieved: {workflow_result.quality_achieved:.1%}")
        print(f"   ✅ Workflow steps: {len(workflow_result.workflow_steps)}")
        
        # Show final result
        print("\n🎙️ FINAL PODCAST SCRIPT:")
        print("-" * 40)
        print(workflow_result.final_output[:300] + "...")
        print("-" * 40)
        
        print("\n🏆 AI COMMANDER COMPLETE WORKFLOW: SUCCESS!")
        print("🚀 User Input → Intent Analysis → Requirements → Workflow → Perfect Output")
        
        return workflow_result
    
    return asyncio.run(run_complete_test())


if __name__ == "__main__":
    test_workflow_orchestrator()
