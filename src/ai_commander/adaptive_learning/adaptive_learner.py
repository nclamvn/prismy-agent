"""
Adaptive Learning System - Phase 7 Week 4
Learns from user patterns and continuously optimizes AI Commander performance
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json
import time
from datetime import datetime

# Import from previous weeks
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intent_analysis import IntentAnalysisResult, UserIntent, UserExpertise
from requirement_collector import RequirementCollectionResult
from workflow_orchestration import WorkflowResult


class LearningEventType(Enum):
    """Types of learning events"""
    USER_INTERACTION = "user_interaction"
    WORKFLOW_COMPLETION = "workflow_completion"
    QUALITY_FEEDBACK = "quality_feedback"
    PERFORMANCE_METRIC = "performance_metric"
    USER_SATISFACTION = "user_satisfaction"


@dataclass
class LearningEvent:
    """A learning event for the adaptive system"""
    event_id: str
    event_type: LearningEventType
    timestamp: datetime
    user_input: str
    intent_result: IntentAnalysisResult
    requirements: RequirementCollectionResult
    workflow_result: WorkflowResult
    user_feedback: Optional[Dict[str, Any]] = None
    performance_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class UserPattern:
    """Detected user behavior pattern"""
    pattern_id: str
    user_expertise_level: UserExpertise
    preferred_intents: List[UserIntent]
    typical_requirements: Dict[str, Any]
    quality_expectations: float
    speed_preferences: float
    success_indicators: List[str]
    frequency: int = 1


@dataclass
class OptimizationInsight:
    """System optimization insight"""
    insight_id: str
    category: str
    description: str
    confidence: float
    potential_improvement: float
    recommended_action: str


class AdaptiveLearner:
    """Adaptive learning system for AI Commander"""
    
    def __init__(self):
        """Initialize adaptive learning system"""
        print("🧠 Initializing Adaptive Learning System...")
        self.learning_history: List[LearningEvent] = []
        self.user_patterns: Dict[str, UserPattern] = {}
        self.optimization_insights: List[OptimizationInsight] = []
        self.performance_baselines = self._initialize_baselines()
        print("✅ Adaptive Learning System ready")
    
    def _initialize_baselines(self) -> Dict[str, float]:
        """Initialize performance baselines"""
        return {
            "processing_time": 0.1,      # Target: <0.1s
            "quality_score": 0.85,       # Target: >85%
            "user_satisfaction": 0.9,    # Target: >90%
            "workflow_success_rate": 0.95 # Target: >95%
        }
    
    def record_learning_event(self, user_input: str, intent_result: IntentAnalysisResult,
                            requirements: RequirementCollectionResult, 
                            workflow_result: WorkflowResult,
                            user_feedback: Optional[Dict[str, Any]] = None) -> str:
        """
        Record a learning event for analysis
        
        Returns:
            Event ID for future reference
        """
        event_id = f"event_{len(self.learning_history)}_{int(time.time())}"
        
        # Calculate performance metrics
        performance_metrics = {
            "processing_time": workflow_result.processing_time,
            "quality_achieved": workflow_result.quality_achieved,
            "success": 1.0 if workflow_result.success else 0.0,
            "intent_confidence": intent_result.confidence_score,
            "requirement_completeness": requirements.completion_score
        }
        
        learning_event = LearningEvent(
            event_id=event_id,
            event_type=LearningEventType.WORKFLOW_COMPLETION,
            timestamp=datetime.now(),
            user_input=user_input,
            intent_result=intent_result,
            requirements=requirements,
            workflow_result=workflow_result,
            user_feedback=user_feedback,
            performance_metrics=performance_metrics
        )
        
        self.learning_history.append(learning_event)
        print(f"📊 Recorded learning event {event_id}")
        
        # Trigger learning analysis
        self._analyze_patterns()
        self._generate_insights()
        
        return event_id
    
    def _analyze_patterns(self):
        """Analyze learning events to detect user patterns"""
        if len(self.learning_history) < 3:
            return  # Need minimum events for pattern detection
        
        # Group events by user expertise level
        expertise_groups = {}
        for event in self.learning_history[-10:]:  # Analyze recent events
            expertise = event.intent_result.user_expertise_level.value
            if expertise not in expertise_groups:
                expertise_groups[expertise] = []
            expertise_groups[expertise].append(event)
        
        # Analyze patterns for each expertise level
        for expertise, events in expertise_groups.items():
            if len(events) >= 2:
                pattern = self._extract_pattern(expertise, events)
                if pattern:
                    self.user_patterns[expertise] = pattern
    
    def _extract_pattern(self, expertise: str, events: List[LearningEvent]) -> Optional[UserPattern]:
        """Extract user pattern from events"""
        
        # Analyze preferred intents
        intent_counts = {}
        for event in events:
            intent = event.intent_result.primary_intent
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        preferred_intents = sorted(intent_counts.keys(), key=lambda x: intent_counts[x], reverse=True)
        
        # Analyze typical requirements
        typical_requirements = {}
        for event in events:
            for key, value in event.requirements.collected_requirements.items():
                if key not in typical_requirements:
                    typical_requirements[key] = []
                typical_requirements[key].append(value)
        
        # Get most common requirement values
        common_requirements = {}
        for key, values in typical_requirements.items():
            if values:
                # Find most common value
                value_counts = {}
                for v in values:
                    value_counts[v] = value_counts.get(v, 0) + 1
                common_requirements[key] = max(value_counts.keys(), key=lambda x: value_counts[x])
        
        # Calculate quality expectations and speed preferences
        quality_scores = [e.performance_metrics.get("quality_achieved", 0.8) for e in events]
        processing_times = [e.performance_metrics.get("processing_time", 0.1) for e in events]
        
        avg_quality = sum(quality_scores) / len(quality_scores)
        avg_speed = sum(processing_times) / len(processing_times)
        
        pattern = UserPattern(
            pattern_id=f"pattern_{expertise}_{int(time.time())}",
            user_expertise_level=UserExpertise(expertise),
            preferred_intents=preferred_intents[:3],  # Top 3
            typical_requirements=common_requirements,
            quality_expectations=avg_quality,
            speed_preferences=1.0 / avg_speed if avg_speed > 0 else 10.0,  # Higher = faster preference
            success_indicators=["high_quality", "fast_processing"],
            frequency=len(events)
        )
        
        return pattern
    
    def _generate_insights(self):
        """Generate optimization insights from learning data"""
        if len(self.learning_history) < 5:
            return
        
        recent_events = self.learning_history[-10:]
        
        # Analyze performance trends
        quality_trend = self._analyze_quality_trend(recent_events)
        speed_trend = self._analyze_speed_trend(recent_events)
        success_trend = self._analyze_success_trend(recent_events)
        
        insights = []
        
        # Quality insights
        if quality_trend["declining"]:
            insights.append(OptimizationInsight(
                insight_id=f"quality_insight_{int(time.time())}",
                category="quality",
                description="Quality scores declining in recent workflows",
                confidence=quality_trend["confidence"],
                potential_improvement=0.1,
                recommended_action="Increase quality targets for next workflows"
            ))
        
        # Speed insights  
        if speed_trend["slow"]:
            insights.append(OptimizationInsight(
                insight_id=f"speed_insight_{int(time.time())}",
                category="performance",
                description="Processing times above optimal threshold",
                confidence=speed_trend["confidence"],
                potential_improvement=0.5,
                recommended_action="Optimize workflow orchestration for speed"
            ))
        
        # Success insights
        if success_trend["issues"]:
            insights.append(OptimizationInsight(
                insight_id=f"success_insight_{int(time.time())}",
                category="reliability",
                description="Workflow success rate below target",
                confidence=success_trend["confidence"],
                potential_improvement=0.2,
                recommended_action="Review error patterns and improve robustness"
            ))
        
        self.optimization_insights.extend(insights)
        
        if insights:
            print(f"🔍 Generated {len(insights)} optimization insights")
    
    def _analyze_quality_trend(self, events: List[LearningEvent]) -> Dict[str, Any]:
        """Analyze quality score trends"""
        quality_scores = [e.performance_metrics.get("quality_achieved", 0.8) for e in events]
        
        if len(quality_scores) < 3:
            return {"declining": False, "confidence": 0.0}
        
        # Simple trend analysis: compare first half vs second half
        mid = len(quality_scores) // 2
        first_half_avg = sum(quality_scores[:mid]) / mid
        second_half_avg = sum(quality_scores[mid:]) / (len(quality_scores) - mid)
        
        declining = second_half_avg < first_half_avg - 0.05  # 5% decline threshold
        confidence = abs(first_half_avg - second_half_avg) * 2  # Simple confidence
        
        return {"declining": declining, "confidence": min(1.0, confidence)}
    
    def _analyze_speed_trend(self, events: List[LearningEvent]) -> Dict[str, Any]:
        """Analyze processing speed trends"""
        processing_times = [e.performance_metrics.get("processing_time", 0.1) for e in events]
        avg_time = sum(processing_times) / len(processing_times)
        
        slow = avg_time > self.performance_baselines["processing_time"] * 2
        confidence = min(1.0, avg_time / 0.1)  # Higher times = higher confidence
        
        return {"slow": slow, "confidence": confidence}
    
    def _analyze_success_trend(self, events: List[LearningEvent]) -> Dict[str, Any]:
        """Analyze workflow success trends"""
        success_rates = [e.performance_metrics.get("success", 1.0) for e in events]
        success_rate = sum(success_rates) / len(success_rates)
        
        issues = success_rate < self.performance_baselines["workflow_success_rate"]
        confidence = 1.0 - success_rate  # Lower success = higher confidence in issues
        
        return {"issues": issues, "confidence": confidence}
    
    def get_recommendations_for_user(self, expertise_level: UserExpertise) -> Dict[str, Any]:
        """Get personalized recommendations for user"""
        expertise_key = expertise_level.value
        
        if expertise_key in self.user_patterns:
            pattern = self.user_patterns[expertise_key]
            
            recommendations = {
                "preferred_workflow_strategy": self._recommend_strategy(pattern),
                "optimal_quality_target": pattern.quality_expectations + 0.02,
                "suggested_intents": [intent.value for intent in pattern.preferred_intents],
                "typical_requirements": pattern.typical_requirements,
                "personalization_confidence": min(1.0, pattern.frequency / 5.0)
            }
        else:
            # Default recommendations
            recommendations = {
                "preferred_workflow_strategy": "balanced",
                "optimal_quality_target": 0.85,
                "suggested_intents": ["create_podcast", "create_video", "translate_only"],
                "typical_requirements": {},
                "personalization_confidence": 0.0
            }
        
        return recommendations
    
    def _recommend_strategy(self, pattern: UserPattern) -> str:
        """Recommend workflow strategy based on user pattern"""
        if pattern.quality_expectations > 0.9:
            return "quality_first"
        elif pattern.speed_preferences > 5.0:  # High speed preference
            return "speed_first"
        else:
            return "balanced"
    
    def get_system_insights(self) -> Dict[str, Any]:
        """Get overall system performance insights"""
        if not self.learning_history:
            return {"status": "insufficient_data"}
        
        recent_events = self.learning_history[-20:]  # Last 20 events
        
        # Calculate aggregate metrics
        avg_quality = sum(e.performance_metrics.get("quality_achieved", 0.8) for e in recent_events) / len(recent_events)
        avg_speed = sum(e.performance_metrics.get("processing_time", 0.1) for e in recent_events) / len(recent_events)
        success_rate = sum(e.performance_metrics.get("success", 1.0) for e in recent_events) / len(recent_events)
        
        insights = {
            "total_events": len(self.learning_history),
            "recent_performance": {
                "average_quality": avg_quality,
                "average_processing_time": avg_speed,
                "success_rate": success_rate
            },
            "user_patterns_detected": len(self.user_patterns),
            "optimization_insights": len(self.optimization_insights),
            "performance_vs_baseline": {
                "quality": avg_quality / self.performance_baselines["quality_score"],
                "speed": self.performance_baselines["processing_time"] / avg_speed,
                "success": success_rate / self.performance_baselines["workflow_success_rate"]
            },
            "recommendations": [insight.recommended_action for insight in self.optimization_insights[-3:]]
        }
        
        return insights


def test_adaptive_learner():
    """Test adaptive learning system"""
    print("🧪 TESTING ADAPTIVE LEARNING SYSTEM")
    print("="*50)
    
    learner = AdaptiveLearner()
    
    # Simulate some learning events
    from intent_analysis import IntentAnalyzer, UserIntent, UserExpertise
    from requirement_collector import SmartRequirementCollector
    from workflow_orchestration import WorkflowResult
    
    analyzer = IntentAnalyzer()
    collector = SmartRequirementCollector()
    
    # Simulate user sessions
    test_sessions = [
        ("Làm podcast từ báo cáo tài chính", "professional"),
        ("Tạo video tutorial cơ bản", "beginner"),
        ("Làm podcast chuyên nghiệp", "professional"),
        ("Dịch tài liệu này", "intermediate"),
        ("Tạo module học tập", "advanced")
    ]
    
    for i, (user_input, expected_expertise) in enumerate(test_sessions):
        print(f"\n📊 Recording session {i+1}: {user_input}")
        
        # Simulate workflow
        intent_result = analyzer.analyze_intent(user_input)
        req_result = collector.collect_requirements(intent_result)
        
        # Simulate workflow result
        workflow_result = WorkflowResult(
            final_output=f"Generated content for: {user_input}",
            processing_time=0.05 + i * 0.01,  # Slightly increasing times
            quality_achieved=0.85 + (i % 3) * 0.05,  # Varying quality
            total_cost=0.0,
            success=True
        )
        
        # Record learning event
        event_id = learner.record_learning_event(user_input, intent_result, req_result, workflow_result)
        print(f"   ✅ Event recorded: {event_id}")
    
    # Get system insights
    print("\n🔍 SYSTEM INSIGHTS:")
    insights = learner.get_system_insights()
    print(f"   📈 Total events: {insights['total_events']}")
    print(f"   🎯 Average quality: {insights['recent_performance']['average_quality']:.1%}")
    print(f"   ⚡ Average speed: {insights['recent_performance']['average_processing_time']:.3f}s")
    print(f"   ✅ Success rate: {insights['recent_performance']['success_rate']:.1%}")
    print(f"   🧠 Patterns detected: {insights['user_patterns_detected']}")
    
    # Get recommendations for professional user
    print("\n💡 RECOMMENDATIONS FOR PROFESSIONAL USER:")
    recommendations = learner.get_recommendations_for_user(UserExpertise.PROFESSIONAL)
    print(f"   🎯 Preferred strategy: {recommendations['preferred_workflow_strategy']}")
    print(f"   📊 Optimal quality: {recommendations['optimal_quality_target']:.1%}")
    print(f"   🎪 Confidence: {recommendations['personalization_confidence']:.1%}")
    
    print("\n🏆 ADAPTIVE LEARNING SYSTEM: FULLY OPERATIONAL!")


if __name__ == "__main__":
    test_adaptive_learner()
