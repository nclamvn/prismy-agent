# analytics/analytics_engine.py
"""
Professional Analytics Engine
Advanced analytics and insights for SDIP system
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import pandas as pd

class AnalyticsEvent(Enum):
    TRANSLATION_STARTED = "translation_started"
    TRANSLATION_COMPLETED = "translation_completed"
    TRANSLATION_FAILED = "translation_failed"
    DOCUMENT_ANALYZED = "document_analyzed"
    RETRY_TRIGGERED = "retry_triggered"
    BATCH_PROCESSED = "batch_processed"

@dataclass
class TranslationRecord:
    """Individual translation record for analytics"""
    id: str
    timestamp: datetime
    source_language: str
    target_language: str
    document_length: int
    complexity: str
    content_type: str
    processing_time: float
    quality_score: float
    chunk_count: int
    retry_count: int
    success: bool
    model_used: str
    smart_features_used: List[str]
    cost_estimate: float = 0.0

@dataclass
class AnalyticsInsights:
    """Analytics insights and recommendations"""
    total_translations: int
    success_rate: float
    average_quality: float
    average_processing_time: float
    most_common_languages: Dict[str, int]
    complexity_distribution: Dict[str, int]
    quality_trends: List[Dict[str, Any]]
    performance_recommendations: List[str]
    cost_analysis: Dict[str, float]

class AnalyticsEngine:
    """
    Professional analytics engine with real-time insights
    """
    
    def __init__(self):
        self.records: List[TranslationRecord] = []
        self.session_stats = {
            'session_start': datetime.now(),
            'translations_this_session': 0,
            'total_processing_time': 0,
            'average_quality_this_session': 0
        }
        
        # Cost per model (mock pricing)
        self.model_costs = {
            'claude': 0.015,  # per 1k tokens
            'gpt4': 0.03,
            'gemini': 0.001,
            'backup': 0.0005
        }
    
    def record_translation(self, translation_data: Dict[str, Any]) -> str:
        """Record a translation event for analytics"""
        record_id = f"trans_{int(time.time())}_{len(self.records)}"
        
        # Extract data from translation result
        record = TranslationRecord(
            id=record_id,
            timestamp=datetime.now(),
            source_language=translation_data.get('source_language', 'auto'),
            target_language=translation_data.get('target_language', 'unknown'),
            document_length=len(translation_data.get('original_text', '')),
            complexity=translation_data.get('analysis', {}).get('complexity', 'unknown'),
            content_type=translation_data.get('analysis', {}).get('content_type', 'general'),
            processing_time=translation_data.get('processing_time', 0),
            quality_score=translation_data.get('quality_score', 0),
            chunk_count=translation_data.get('chunk_count', 0),
            retry_count=translation_data.get('retry_info', {}).get('retry_count', 0),
            success=translation_data.get('success', False),
            model_used=translation_data.get('retry_info', {}).get('model_used', 'claude'),
            smart_features_used=translation_data.get('smart_features_used', []),
            cost_estimate=self._calculate_cost_estimate(translation_data)
        )
        
        self.records.append(record)
        self._update_session_stats(record)
        
        print(f"📊 Analytics: Recorded translation {record_id}")
        return record_id
    
    def get_comprehensive_insights(self, days: int = 30) -> AnalyticsInsights:
        """Generate comprehensive analytics insights"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_records = [r for r in self.records if r.timestamp >= cutoff_date]
        
        if not recent_records:
            return self._empty_insights()
        
        # Basic metrics
        total_translations = len(recent_records)
        successful_records = [r for r in recent_records if r.success]
        success_rate = len(successful_records) / total_translations if total_translations > 0 else 0
        
        # Quality and performance metrics
        if successful_records:
            average_quality = sum(r.quality_score for r in successful_records) / len(successful_records)
            average_processing_time = sum(r.processing_time for r in successful_records) / len(successful_records)
        else:
            average_quality = 0
            average_processing_time = 0
        
        # Language analysis
        language_pairs = {}
        for record in recent_records:
            pair = f"{record.source_language} → {record.target_language}"
            language_pairs[pair] = language_pairs.get(pair, 0) + 1
        
        most_common_languages = dict(sorted(language_pairs.items(), key=lambda x: x[1], reverse=True)[:5])
        
        # Complexity distribution
        complexity_dist = {}
        for record in recent_records:
            complexity_dist[record.complexity] = complexity_dist.get(record.complexity, 0) + 1
        
        # Quality trends (last 7 days)
        quality_trends = self._calculate_quality_trends(recent_records)
        
        # Performance recommendations
        recommendations = self._generate_performance_recommendations(recent_records)
        
        # Cost analysis
        cost_analysis = self._analyze_costs(recent_records)
        
        return AnalyticsInsights(
            total_translations=total_translations,
            success_rate=success_rate,
            average_quality=average_quality,
            average_processing_time=average_processing_time,
            most_common_languages=most_common_languages,
            complexity_distribution=complexity_dist,
            quality_trends=quality_trends,
            performance_recommendations=recommendations,
            cost_analysis=cost_analysis
        )
    
    def get_real_time_stats(self) -> Dict[str, Any]:
        """Get real-time session statistics"""
        return {
            'session_duration': str(datetime.now() - self.session_stats['session_start']),
            'translations_this_session': self.session_stats['translations_this_session'],
            'total_translations_all_time': len(self.records),
            'average_quality_this_session': self.session_stats['average_quality_this_session'],
            'total_processing_time': self.session_stats['total_processing_time'],
            'last_translation': self.records[-1].timestamp.strftime('%H:%M:%S') if self.records else 'None'
        }
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get detailed performance metrics"""
        if not self.records:
            return {}
        
        successful_records = [r for r in self.records if r.success]
        
        return {
            'total_documents_processed': len(self.records),
            'success_rate': len(successful_records) / len(self.records) * 100,
            'average_quality_score': sum(r.quality_score for r in successful_records) / len(successful_records) if successful_records else 0,
            'average_processing_time': sum(r.processing_time for r in successful_records) / len(successful_records) if successful_records else 0,
            'total_chunks_processed': sum(r.chunk_count for r in self.records),
            'smart_features_usage': self._analyze_smart_features_usage(),
            'model_performance': self._analyze_model_performance(),
            'complexity_performance': self._analyze_complexity_performance()
        }
    
    def export_analytics_data(self, format_type: str = "json") -> str:
        """Export analytics data in specified format"""
        if format_type == "json":
            return json.dumps([asdict(record) for record in self.records], default=str, indent=2)
        elif format_type == "csv":
            if not self.records:
                return "No data to export"
            
            # Create DataFrame from records
            df = pd.DataFrame([asdict(record) for record in self.records])
            return df.to_csv(index=False)
        else:
            return "Unsupported format"
    
    def _calculate_cost_estimate(self, translation_data: Dict[str, Any]) -> float:
        """Calculate estimated cost for translation"""
        document_length = len(translation_data.get('original_text', ''))
        model_used = translation_data.get('retry_info', {}).get('model_used', 'claude')
        
        # Rough token estimate (1 token ≈ 4 characters)
        estimated_tokens = document_length / 4
        cost_per_1k_tokens = self.model_costs.get(model_used, 0.01)
        
        return (estimated_tokens / 1000) * cost_per_1k_tokens
    
    def _update_session_stats(self, record: TranslationRecord):
        """Update session statistics"""
        self.session_stats['translations_this_session'] += 1
        self.session_stats['total_processing_time'] += record.processing_time
        
        if record.success:
            current_avg = self.session_stats['average_quality_this_session']
            session_count = self.session_stats['translations_this_session']
            
            # Update running average
            self.session_stats['average_quality_this_session'] = \
                ((current_avg * (session_count - 1)) + record.quality_score) / session_count
    
    def _empty_insights(self) -> AnalyticsInsights:
        """Return empty insights when no data available"""
        return AnalyticsInsights(
            total_translations=0,
            success_rate=0,
            average_quality=0,
            average_processing_time=0,
            most_common_languages={},
            complexity_distribution={},
            quality_trends=[],
            performance_recommendations=["No data available - start translating to see insights!"],
            cost_analysis={}
        )
    
    def _calculate_quality_trends(self, records: List[TranslationRecord]) -> List[Dict[str, Any]]:
        """Calculate quality trends over time"""
        if not records:
            return []
        
        # Group by day and calculate daily averages
        daily_quality = {}
        for record in records:
            if record.success:
                day = record.timestamp.date()
                if day not in daily_quality:
                    daily_quality[day] = []
                daily_quality[day].append(record.quality_score)
        
        trends = []
        for day, scores in daily_quality.items():
            trends.append({
                'date': day.isoformat(),
                'average_quality': sum(scores) / len(scores),
                'translation_count': len(scores)
            })
        
        return sorted(trends, key=lambda x: x['date'])
    
    def _generate_performance_recommendations(self, records: List[TranslationRecord]) -> List[str]:
        """Generate performance recommendations based on data"""
        recommendations = []
        
        if not records:
            return ["No data available for recommendations"]
        
        successful_records = [r for r in records if r.success]
        
        # Success rate analysis
        success_rate = len(successful_records) / len(records)
        if success_rate < 0.9:
            recommendations.append("Consider optimizing input document quality to improve success rate")
        
        # Quality analysis
        if successful_records:
            avg_quality = sum(r.quality_score for r in successful_records) / len(successful_records)
            if avg_quality < 0.85:
                recommendations.append("Quality scores below optimal - consider using higher-tier models")
        
        # Processing time analysis
        if successful_records:
            avg_time = sum(r.processing_time for r in successful_records) / len(successful_records)
            if avg_time > 3.0:
                recommendations.append("Processing times are high - consider document optimization or parallel processing")
        
        # Complexity analysis
        complex_docs = [r for r in records if r.complexity in ['complex', 'technical']]
        if len(complex_docs) > len(records) * 0.5:
            recommendations.append("High complexity documents detected - consider specialized processing")
        
        if not recommendations:
            recommendations.append("Performance is optimal - continue current approach!")
        
        return recommendations
    
    def _analyze_costs(self, records: List[TranslationRecord]) -> Dict[str, float]:
        """Analyze cost patterns"""
        total_cost = sum(r.cost_estimate for r in records)
        
        model_costs = {}
        for record in records:
            model = record.model_used
            model_costs[model] = model_costs.get(model, 0) + record.cost_estimate
        
        return {
            'total_estimated_cost': total_cost,
            'average_cost_per_translation': total_cost / len(records) if records else 0,
            'cost_by_model': model_costs
        }
    
    def _analyze_smart_features_usage(self) -> Dict[str, int]:
        """Analyze smart features usage patterns"""
        feature_usage = {}
        
        for record in self.records:
            for feature in record.smart_features_used:
                feature_usage[feature] = feature_usage.get(feature, 0) + 1
        
        return feature_usage
    
    def _analyze_model_performance(self) -> Dict[str, Dict[str, float]]:
        """Analyze performance by model"""
        model_stats = {}
        
        for record in self.records:
            if record.success:
                model = record.model_used
                if model not in model_stats:
                    model_stats[model] = {'quality_scores': [], 'processing_times': []}
                
                model_stats[model]['quality_scores'].append(record.quality_score)
                model_stats[model]['processing_times'].append(record.processing_time)
        
        # Calculate averages
        model_performance = {}
        for model, stats in model_stats.items():
            model_performance[model] = {
                'average_quality': sum(stats['quality_scores']) / len(stats['quality_scores']),
                'average_processing_time': sum(stats['processing_times']) / len(stats['processing_times']),
                'usage_count': len(stats['quality_scores'])
            }
        
        return model_performance
    
    def _analyze_complexity_performance(self) -> Dict[str, Dict[str, float]]:
        """Analyze performance by document complexity"""
        complexity_stats = {}
        
        for record in self.records:
            if record.success:
                complexity = record.complexity
                if complexity not in complexity_stats:
                    complexity_stats[complexity] = {'quality_scores': [], 'processing_times': []}
                
                complexity_stats[complexity]['quality_scores'].append(record.quality_score)
                complexity_stats[complexity]['processing_times'].append(record.processing_time)
        
        # Calculate averages
        complexity_performance = {}
        for complexity, stats in complexity_stats.items():
            complexity_performance[complexity] = {
                'average_quality': sum(stats['quality_scores']) / len(stats['quality_scores']),
                'average_processing_time': sum(stats['processing_times']) / len(stats['processing_times']),
                'document_count': len(stats['quality_scores'])
            }
        
        return complexity_performance
