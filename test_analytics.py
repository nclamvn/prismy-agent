from analytics.analytics_engine import AnalyticsEngine
from datetime import datetime

print('📊 Testing Analytics Engine...')

# Create analytics engine
analytics = AnalyticsEngine()

# Simulate some translation records
test_translations = [
    {
        'success': True,
        'source_language': 'English',
        'target_language': 'Vietnamese',
        'original_text': 'Test document for analytics',
        'processing_time': 1.2,
        'quality_score': 0.92,
        'chunk_count': 1,
        'analysis': {'complexity': 'simple', 'content_type': 'general'},
        'retry_info': {'retry_count': 0, 'model_used': 'claude'},
        'smart_features_used': ['Intelligent Document Analysis', 'Smart Retry System']
    },
    {
        'success': True,
        'source_language': 'English', 
        'target_language': 'Vietnamese',
        'original_text': 'Technical documentation with complex algorithms and neural networks for machine learning deployment',
        'processing_time': 2.8,
        'quality_score': 0.88,
        'chunk_count': 2,
        'analysis': {'complexity': 'technical', 'content_type': 'technical'},
        'retry_info': {'retry_count': 1, 'model_used': 'gpt4'},
        'smart_features_used': ['Intelligent Document Analysis', 'Smart Retry System', 'Quality Optimization']
    },
    {
        'success': True,
        'source_language': 'French',
        'target_language': 'English', 
        'original_text': 'Simple business document',
        'processing_time': 0.8,
        'quality_score': 0.95,
        'chunk_count': 1,
        'analysis': {'complexity': 'simple', 'content_type': 'business'},
        'retry_info': {'retry_count': 0, 'model_used': 'claude'},
        'smart_features_used': ['Intelligent Document Analysis']
    }
]

# Record translations
for i, translation in enumerate(test_translations):
    record_id = analytics.record_translation(translation)
    print(f'✅ Recorded translation {i+1}: {record_id}')

# Get comprehensive insights
insights = analytics.get_comprehensive_insights()

print('\n📈 ANALYTICS INSIGHTS:')
print(f'  - Total Translations: {insights.total_translations}')
print(f'  - Success Rate: {insights.success_rate:.2%}')
print(f'  - Average Quality: {insights.average_quality:.2f}')
print(f'  - Average Processing Time: {insights.average_processing_time:.2f}s')
print(f'  - Most Common Languages: {insights.most_common_languages}')
print(f'  - Complexity Distribution: {insights.complexity_distribution}')

print('\n💡 RECOMMENDATIONS:')
for rec in insights.performance_recommendations:
    print(f'  • {rec}')

# Get real-time stats
real_time = analytics.get_real_time_stats()
print(f'\n⏱️ REAL-TIME STATS:')
print(f'  - Session Duration: {real_time["session_duration"]}')
print(f'  - Translations This Session: {real_time["translations_this_session"]}')
print(f'  - Total Translations: {real_time["total_translations_all_time"]}')

# Get performance metrics
performance = analytics.get_performance_metrics()
print(f'\n🎯 PERFORMANCE METRICS:')
print(f'  - Documents Processed: {performance["total_documents_processed"]}')
print(f'  - Success Rate: {performance["success_rate"]:.1f}%')
print(f'  - Smart Features Usage: {performance["smart_features_usage"]}')

print('\n✅ Analytics Engine working perfectly!')
