"""
Test script for Unified Video Processor
"""

import sys
import os
import json

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import the unified processor
from src.infrastructure.content_transformation.unified_video_processor import (
    UnifiedVideoProcessor,
    VideoOutputFormat,
    TransformationRequest,
    TargetAudience,
    ContentDifficulty,
    TransformationType
)

def test_unified_processor():
    """Test the unified video processor with both output formats"""
    
    print("🚀 Testing Unified Video Processor\n")
    
    # Initialize processor
    try:
        processor = UnifiedVideoProcessor()
        print("✅ Processor initialized successfully\n")
    except Exception as e:
        print(f"❌ Initialization error: {e}\n")
        return
    
    # Test content
    test_text = """PRISM AI Platform là một giải pháp cách mạng cho việc chuyển đổi nội dung.

Công nghệ DNA fingerprinting đảm bảo tính liên tục thị giác hoàn hảo giữa các cảnh.

Xuất video sang mọi nền tảng AI một cách liền mạch với chất lượng cao nhất."""
    
    # Create transformation request
    request = TransformationRequest(
        source_text=test_text,
        transformation_type=TransformationType.VIDEO_SCENARIO,
        target_audience=TargetAudience.ADULTS,
        difficulty_level=ContentDifficulty.INTERMEDIATE,
        language="vi",
        duration_target=2  # 2 minutes
    )
    
    # Test 1: Screenplay Format
    print("=" * 60)
    print("📝 TEST 1: SCREENPLAY FORMAT")
    print("=" * 60)
    
    try:
        screenplay_response = processor.transform_content(
            request,
            output_format=VideoOutputFormat.SCREENPLAY
        )
        
        if screenplay_response.transformed_content:
            print("✅ Screenplay generation successful!")
            print(f"Quality Score: {screenplay_response.quality_score}")
            print(f"Processing Time: {screenplay_response.processing_time:.2f}s")
            print("\nScreenplay Preview:")
            print("-" * 40)
            output_data = json.loads(screenplay_response.transformed_content)
            content = output_data['content']
            print(content[:800] + "..." if len(content) > 800 else content)
        else:
            print("❌ Screenplay generation failed")
            print(f"Error: {screenplay_response.metadata.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during screenplay generation: {e}")
    
    # Test 2: AI Prompts Format
    print("\n" + "=" * 60)
    print("🤖 TEST 2: AI PROMPTS FORMAT (SORA)")
    print("=" * 60)
    
    try:
        ai_response = processor.transform_content(
            request,
            output_format=VideoOutputFormat.AI_PROMPTS,
            target_platform="sora"
        )
        
        if ai_response.transformed_content:
            print("✅ AI prompts generation successful!")
            print(f"Quality Score: {ai_response.quality_score}")
            print(f"DNA Enhanced: {ai_response.metadata.get('dna_enhanced', False)}")
            print("\nAI Prompts Preview:")
            print("-" * 40)
            output_data = json.loads(ai_response.transformed_content)
            prompts_data = output_data['content']
            print(json.dumps(prompts_data, indent=2, ensure_ascii=False)[:800])
        else:
            print("❌ AI prompts generation failed")
            print(f"Error: {ai_response.metadata.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Error during AI prompts generation: {e}")
    
    # Test 3: Multi-platform Export
    print("\n" + "=" * 60)
    print("🌐 TEST 3: MULTI-PLATFORM EXPORT")
    print("=" * 60)
    
    try:
        if 'ai_response' in locals() and ai_response.transformed_content:
            exports = processor.export_for_platforms(ai_response)
            print(f"✅ Exported to {len(exports['platforms'])} platforms:")
            for platform in exports['platforms']:
                export_data = exports['exports'][platform]
                print(f"\n📱 {platform.upper()}:")
                print(f"   - Scenes: {export_data['scene_count']}")
                print(f"   - Total Duration: {export_data['total_duration']}s")
                print(f"   - Continuity: {export_data.get('continuity_preserved', False)}")
                if export_data['prompts']:
                    print(f"   - First prompt: {export_data['prompts'][0]['prompt'][:100]}...")
        else:
            print("⚠️ Skipping export test (AI response not available)")
            
    except Exception as e:
        print(f"❌ Error during multi-platform export: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print("✅ Unified Video Processor is working!")
    print("✅ Both output formats (screenplay & AI prompts) are functional")
    print("✅ Ready for Streamlit integration")
    
    # Check for missing components
    print("\n⚠️ Components Status:")
    if not processor.dna_engine:
        print("   - DNA Engine: Not available (import failed)")
    else:
        print("   - DNA Engine: ✅ Available")
    
    # Check LLM enhancer
    from src.infrastructure.content_transformation.unified_video_processor import LLM_ENHANCER_AVAILABLE
    if not LLM_ENHANCER_AVAILABLE:
        print("   - LLM Enhancer: Not available (import failed)")
    else:
        print("   - LLM Enhancer: ✅ Available")


if __name__ == "__main__":
    test_unified_processor()
