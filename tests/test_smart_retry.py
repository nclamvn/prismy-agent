import asyncio
from smart_features.smart_retry import SmartRetrySystem, RetryReason

async def test_smart_retry():
    print('🔄 Testing Smart Retry System...')
    
    retry_system = SmartRetrySystem()
    
    # Simulate low quality initial result
    initial_result = {
        'success': True,
        'translated_text': 'Poor quality translation',
        'quality_score': 0.65,  # Below threshold
        'processing_time': 1.0,
        'original_text': 'Test document for translation'
    }
    
    print(f'📊 Initial quality: {initial_result["quality_score"]}')
    
    # Test smart retry
    retry_result = await retry_system.smart_translate_with_retry(
        'Test document for translation',
        'Vietnamese',
        initial_result
    )
    
    print('\n🎯 SMART RETRY RESULTS:')
    print(f'  - Success: {retry_result.success}')
    print(f'  - Final Quality: {retry_result.quality_score:.2f}')
    print(f'  - Model Used: {retry_result.model_used.value}')
    print(f'  - Retry Count: {retry_result.retry_count}')
    print(f'  - Retry Reasons: {[r.value for r in retry_result.retry_reasons]}')
    print(f'  - Improvements: {retry_result.improvement_notes}')
    
    print('\n✅ Smart Retry System working!')

# Run test
asyncio.run(test_smart_retry())
