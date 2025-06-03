"""Test all transformers with LLM enhancement"""
import asyncio
from src.infrastructure.content_transformation import (
    TransformationManager,
    TransformationRequest,
    TransformationType,
    TargetAudience,
    ContentDifficulty
)

async def test_all():
    manager = TransformationManager()
    
    # Test content
    test_text = "Artificial Intelligence is revolutionizing healthcare through predictive analytics and personalized treatment plans."
    
    # Test Podcast
    print("🎙️ Testing Podcast Generator...")
    request = TransformationRequest(
        source_text=test_text,
        transformation_type=TransformationType.PODCAST_SCRIPT,
        target_audience=TargetAudience.ADULTS,
        difficulty_level=ContentDifficulty.INTERMEDIATE
    )
    
    try:
        response = await manager.transform_content(request)
        print("✅ Podcast: Success")
        print(f"   Quality Score: {response.quality_score}")
    except Exception as e:
        print(f"❌ Podcast Error: {e}")
    
    # Test Education
    print("\n📚 Testing Education Module...")
    request.transformation_type = TransformationType.EDUCATION_MODULE
    
    try:
        response = await manager.transform_content(request)
        print("✅ Education: Success")
        print(f"   Quality Score: {response.quality_score}")
    except Exception as e:
        print(f"❌ Education Error: {e}")
    
    # Test Video
    print("\n🎬 Testing Video Processor...")
    request.transformation_type = TransformationType.VIDEO_SCENARIO
    
    try:
        response = await manager.transform_content(request)
        print("✅ Video: Success")
        print(f"   Quality Score: {response.quality_score}")
    except Exception as e:
        print(f"❌ Video Error: {e}")
    
    print("\n🎯 All transformers tested!")

if __name__ == "__main__":
    asyncio.run(test_all())
