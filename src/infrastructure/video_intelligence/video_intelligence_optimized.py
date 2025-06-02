"""
PRISM Video Intelligence - Production Optimized Version
Ready for integration with PRISM web platform
"""

from scene_analyzer import SceneAnalyzer
from character_tracker import CharacterTracker  
from visual_context_builder import VisualContextBuilder
from video_chunking_orchestrator import VideoChunkingOrchestrator
from character_optimizer import CharacterOptimizer

class PrismVideoIntelligence:
    """
    Production-ready Video Intelligence Engine
    Optimized for PRISM platform integration
    """
    
    def __init__(self, target_duration: float = 8.0):
        self.scene_analyzer = SceneAnalyzer(target_duration)
        self.character_tracker = CharacterTracker()
        self.visual_context_builder = VisualContextBuilder()
        self.character_optimizer = CharacterOptimizer()
        self.target_duration = target_duration
    
    def process_movie_script(self, script: str, session_name: str = None) -> dict:
        """
        Main API method for PRISM platform
        Process movie script into AI-ready video chunks
        """
        try:
            # Step 1: Analyze scenes
            scenes = self.scene_analyzer.analyze_script(script)
            
            # Step 2: Optimize character extraction
            for scene in scenes:
                optimized_chars = self.character_optimizer.extract_characters(scene.content)
                scene.characters = optimized_chars
            
            # Step 3: Track characters
            all_characters = set()
            for scene in scenes:
                all_characters.update(scene.characters)
            
            for scene in scenes:
                self.character_tracker.extract_character_profile(
                    scene.content, scene.id, scene.characters
                )
            
            # Step 4: Generate enhanced prompts
            enhanced_prompts = []
            for scene in scenes:
                enhanced_prompt = self.visual_context_builder.generate_enhanced_prompt(
                    scene.content, scene.id, scene.characters
                )
                enhanced_prompts.append(enhanced_prompt)
            
            # Step 5: Create production-ready output
            result = {
                "success": True,
                "session_id": session_name or f"VS_{int(time.time())}",
                "total_scenes": len(scenes),
                "average_duration": sum(s.duration for s in scenes) / len(scenes),
                "total_duration": sum(s.duration for s in scenes),
                "characters": list(all_characters),
                "scenes": [
                    {
                        "id": scene.id,
                        "content": scene.content,
                        "duration": scene.duration,
                        "type": scene.scene_type.value,
                        "characters": scene.characters,
                        "enhanced_prompt": enhanced_prompts[i],
                        "ai_generation_ready": True
                    }
                    for i, scene in enumerate(scenes)
                ],
                "production_notes": {
                    "target_duration": self.target_duration,
                    "character_count": len(all_characters),
                    "scene_count": len(scenes),
                    "ready_for_ai_generation": True
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Error processing script"
            }

# Test production version
if __name__ == "__main__":
    import time
    
    engine = PrismVideoIntelligence(target_duration=8.0)
    
    test_script = """
    Anh MINH (40 tuổi, gầy, da ngăm đen) bước ra khỏi nhà tranh.
    Anh nhìn ra cánh đồng lúa xanh mướt và bắt đầu đi.
    
    Trên đường, anh gặp em LAN (25 tuổi, xinh đẹp) đang hái rau.
    
    MINH: "Chào em Lan!"
    LAN: "Chào anh Minh! Sáng nay anh dậy sớm quá!"
    """
    
    print("🚀 TESTING PRODUCTION-READY ENGINE:")
    print("="*50)
    
    result = engine.process_movie_script(test_script, "Production_Test")
    
    if result["success"]:
        print(f"✅ Success!")
        print(f"   📊 Scenes: {result['total_scenes']}")
        print(f"   👥 Characters: {result['characters']}")
        print(f"   ⏱️  Duration: {result['total_duration']:.1f}s")
        print(f"   🎬 Sample Enhanced Prompt:")
        print("   " + "="*40)
        print("   " + result['scenes'][0]['enhanced_prompt'][:200] + "...")
    else:
        print(f"❌ Error: {result['error']}")
