"""
Integration test for complete Video Intelligence Engine
"""

from video_chunking_orchestrator import VideoChunkingOrchestrator
import json

def test_complete_workflow():
    """Test complete video chunking workflow"""
    
    # Real Vietnamese movie script sample
    script = """
    FADE IN:
    
    EXT. NHÀNGƯỜI VIỆTNAM - SÁNG SỚM
    
    Anh MINH (40 tuổi, gầy, da ngăm đen, mặt khắc khổ) bước ra khỏi nhà tranh nhỏ.
    Anh mặc áo sơ mi nâu cũ và quần đen. Chân trần.
    
    Ánh nắng mai chiếu rọi xuống khuôn mặt anh. Anh nhìn ra cánh đồng lúa.
    
    CUT TO:
    
    EXT. CON ĐƯỜNG ĐẤT - CONTINUOUS
    
    Anh Minh đi bộ trên con đường đất giữa hai bên ruộng lúa xanh.
    Không khí nông thôn yên bình, chỉ có tiếng chim hót.
    
    Anh dừng lại khi thấy em LAN (25 tuổi, xinh đẹp, mặc áo bà ba trắng) 
    đang hái rau bên vệ đường.
    
    MINH
    Chào em Lan! Sáng nay em dậy sớm quá!
    
    LAN
    (đứng thẳng lên, cười tươi)
    Chào anh Minh! Em phải hái rau sớm 
    để mang ra chợ bán.
    
    MINH
    Mùa này rau của em bán được giá không?
    
    LAN
    Cũng được anh ạ. Nhưng em mong 
    mưa xuống để rau tươi hơn.
    
    Hai người trò chuyện vài phút. Sau đó anh Minh vẫy tay chào và 
    tiếp tục đi về phía cánh đồng.
    
    CUT TO:
    
    EXT. CÁNH ĐỒNG LÚA - SÁNG
    
    Anh Minh đứng giữa cánh đồng, nhìn những bông lúa chín vàng.
    Gió nhẹ thổi qua, tạo thành những đợt sóng lúa đẹp mắt.
    
    FADE OUT.
    """
    
    print("🎬 TESTING COMPLETE VIDEO INTELLIGENCE WORKFLOW")
    print("="*60)
    
    # Initialize orchestrator
    orchestrator = VideoChunkingOrchestrator(target_duration=8.0)
    
    # Process script
    result = orchestrator.process_script(script, "Professional_Test_Script")
    
    # Display results
    print(f"\n📊 DETAILED RESULTS:")
    print(f"   🎬 Total Scenes: {result.total_scenes}")
    print(f"   👥 Characters Found: {len(result.character_profiles)}")
    print(f"   ⏱️  Processing Time: {result.processing_time:.3f}s")
    print(f"   🎯 Continuity Score: {result.continuity_score:.2f}")
    print(f"   📈 Quality Score: {result.quality_metrics['overall_quality']:.2f}")
    
    print(f"\n👥 CHARACTER PROFILES:")
    for name, profile in result.character_profiles.items():
        if profile.appearance_count > 0:  # Only show real characters
            print(f"   • {name}: {profile.get_base_description()}")
            print(f"     Appearances: {profile.appearance_count} scenes")
    
    print(f"\n🎬 SCENE BREAKDOWN:")
    for i, scene in enumerate(result.scenes[:3]):  # Show first 3 scenes
        print(f"   Scene {scene.id}: {scene.duration:.1f}s - {scene.scene_type.value}")
        print(f"   Content: {scene.content[:80]}...")
        print(f"   Characters: {scene.characters}")
        print()
    
    print(f"\n🎯 ENHANCED PROMPT SAMPLE (Scene 1):")
    print("="*50)
    print(result.enhanced_prompts[0])
    
    # Export for AI platforms
    print(f"\n🚀 AI PLATFORM EXPORTS:")
    
    runway_export = orchestrator.export_for_ai_platforms(result.session_id, "runaway")
    print(f"   Runway ML: {len(runway_export.get('scenes', []))} scenes ready")
    
    pika_export = orchestrator.export_for_ai_platforms(result.session_id, "pika")
    print(f"   Pika Labs: {len(pika_export.get('video_project', {}).get('clips', []))} clips ready")
    
    # Generate production guide
    guide = orchestrator.generate_video_production_guide(result.session_id)
    print(f"\n📋 PRODUCTION GUIDE: {len(guide)} characters generated")
    
    # Save results to file
    with open(f"video_chunking_result_{result.session_id}.json", "w", encoding="utf-8") as f:
        json.dump(result.to_dict(), f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ COMPLETE WORKFLOW TEST SUCCESSFUL!")
    print(f"   📁 Results saved to: video_chunking_result_{result.session_id}.json")
    print(f"   🎬 Ready for AI video generation!")
    
    return result

if __name__ == "__main__":
    test_complete_workflow()
