"""
AI Commander - Intelligent User Experience Layer
Phase 7: ALL 4 WEEKS COMPLETE! 🏆

Automatically analyzes user intent and delivers optimal results with minimal input.
Features adaptive learning for continuous improvement.
"""

# Week 1: Intent Analysis
from .intent_analysis import IntentAnalyzer, IntentAnalysisResult, UserIntent, UserExpertise

# Week 2: Smart Requirements 
from .requirement_collector import SmartRequirementCollector, RequirementCollectionResult

# Week 3: Workflow Orchestration
from .workflow_orchestration import WorkflowOrchestrator, WorkflowResult

# Week 4: Adaptive Learning
from .adaptive_learning import AdaptiveLearner, LearningEvent, UserPattern

__all__ = [
    # Week 1
    'IntentAnalyzer',
    'IntentAnalysisResult', 
    'UserIntent',
    'UserExpertise',
    # Week 2
    'SmartRequirementCollector',
    'RequirementCollectionResult',
    # Week 3
    'WorkflowOrchestrator',
    'WorkflowResult',
    # Week 4
    'AdaptiveLearner',
    'LearningEvent',
    'UserPattern'
]
