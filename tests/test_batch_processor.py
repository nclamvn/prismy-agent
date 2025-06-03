import asyncio
from smart_features.batch_processor import SmartBatchProcessor, BatchDocument, Priority, BatchStrategy

async def test_batch_processing():
    print('📦 Testing Smart Batch Processing...')
    
    processor = SmartBatchProcessor()
    
    # Create test documents with different priorities
    documents = [
        BatchDocument(
            id="doc1",
            content="# Urgent Report\nThis is an urgent business report that needs immediate translation.",
            target_language="Vietnamese",
            priority=Priority.URGENT
        ),
        BatchDocument(
            id="doc2", 
            content="Simple document for translation testing.",
            target_language="Vietnamese",
            priority=Priority.NORMAL
        ),
        BatchDocument(
            id="doc3",
            content="# Technical Documentation\nThis API provides advanced functionality for machine learning model deployment with complex algorithms and neural networks.",
            target_language="Vietnamese",
            priority=Priority.HIGH
        ),
        BatchDocument(
            id="doc4",
            content="Short memo.",
            target_language="Vietnamese", 
            priority=Priority.LOW
        )
    ]
    
    print(f'📊 Processing {len(documents)} documents')
    
    # Test adaptive batch processing
    result = await processor.process_batch(documents, BatchStrategy.ADAPTIVE)
    
    print('\n🎯 BATCH PROCESSING RESULTS:')
    print(f'  - Total Documents: {result.total_documents}')
    print(f'  - Successful: {result.successful_translations}')
    print(f'  - Failed: {result.failed_translations}')
    print(f'  - Total Time: {result.total_processing_time:.2f}s')
    print(f'  - Average Quality: {result.average_quality_score:.2f}')
    
    print('\n📈 OPTIMIZATION INSIGHTS:')
    insights = result.optimization_insights
    print(f'  - Processing Efficiency: {insights["processing_efficiency"]:.2f}')
    print(f'  - Avg Time per Doc: {insights["average_processing_time"]:.2f}s')
    print(f'  - Quality Distribution: {insights["quality_distribution"]}')
    
    if insights['recommendations']:
        print('\n💡 RECOMMENDATIONS:')
        for rec in insights['recommendations']:
            print(f'  - {rec}')
    
    print('\n✅ Smart Batch Processing working!')

# Run test
asyncio.run(test_batch_processing())
