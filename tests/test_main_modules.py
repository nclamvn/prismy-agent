"""
Test main modules
"""
import sys
import asyncio
sys.path.insert(0, '.')

async def test_all_modules():
    """Test tất cả modules chính"""
    print("\n🧪 TESTING MAIN MODULES")
    print("="*60)
    
    # Test 1: Podcast Generator
    print("\n📻 Testing Podcast Generator...")
    try:
        from src.infrastructure.content_transformation.podcast_generator import PodcastGenerator
        from src.infrastructure.content_transformation.base_transformer import TransformationRequest, TargetAudience, ContentDifficulty
        
        generator = PodcastGenerator()
        request = TransformationRequest(
            source_text="Test content for podcast",
            transformation_type="podcast",
            target_audience=TargetAudience.ADULTS,
            difficulty_level=ContentDifficulty.INTERMEDIATE
        )
        
        # Test validation
        assert generator.validate_request(request) == True
        print("  ✅ Podcast Generator initialized successfully")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 2: Education Module Builder
    print("\n📚 Testing Education Module Builder...")
    try:
        from src.infrastructure.content_transformation.education_module_builder import EducationModuleBuilder
        
        builder = EducationModuleBuilder()
        audiences = builder.get_supported_audiences()
        assert len(audiences) > 0
        print(f"  ✅ Education Module supports {len(audiences)} audiences")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 3: Video Processor
    print("\n🎬 Testing Video Processor...")
    try:
        from src.infrastructure.content_transformation.unified_video_processor import UnifiedVideoProcessor
        
        processor = UnifiedVideoProcessor()
        print("  ✅ Video Processor initialized successfully")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 4: AI Commander
    print("\n🤖 Testing AI Commander...")
    try:
        from src.ai_commander.enhanced_commander.hotel_concierge_claude import EnhancedProductionCommander
        
        commander = EnhancedProductionCommander()
        print("  ✅ AI Commander initialized successfully")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    # Test 5: Translation Service
    print("\n🌐 Testing Translation Service...")
    try:
        from src.application.services.translation_service import TranslationService
        
        service = TranslationService(enable_cache=True)
        assert service.is_configured() == False  # No API key
        print("  ✅ Translation Service initialized (needs API key)")
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ Module testing complete!")

# Run tests
asyncio.run(test_all_modules())
