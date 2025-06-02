"""
PRISM Video Intelligence - Video Chunking Orchestrator
Main workflow orchestrator for seamless AI video generation
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import time
from datetime import datetime

# Import our components
from scene_analyzer import SceneAnalyzer, VideoScene
from character_tracker import CharacterTracker, CharacterProfile
from visual_context_builder import VisualContextBuilder, SceneVisualContext

@dataclass
class VideoChunkingResult:
    """Complete result from video chunking process"""
    session_id: str
    original_script: str
    total_scenes: int
    processing_time: float
    scenes: List[VideoScene]
    enhanced_prompts: List[str]
    character_profiles: Dict[str, CharacterProfile]
    continuity_score: float
    quality_metrics: Dict[str, float]
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for export"""
        return {
            "session_id": self.session_id,
            "original_script": self.original_script,
            "total_scenes": self.total_scenes,
            "processing_time": self.processing_time,
            "scenes": [self._scene_to_dict(scene) for scene in self.scenes],
            "enhanced_prompts": self.enhanced_prompts,
            "character_profiles": {name: asdict(profile) for name, profile in self.character_profiles.items()},
            "continuity_score": self.continuity_score,
            "quality_metrics": self.quality_metrics
        }

class VideoChunkingOrchestrator:
    """
    Main orchestrator for intelligent video chunking workflow
    Coordinates all components for seamless AI video generation
    """
    
    def __init__(self, target_duration: float = 8.0):
        self.scene_analyzer = SceneAnalyzer(target_duration=target_duration)
        self.character_tracker = CharacterTracker()
        self.visual_context_builder = VisualContextBuilder()
        
        self.target_duration = target_duration
        self.session_history: Dict[str, VideoChunkingResult] = {}
        
    def process_script(self, script: str, session_name: str = None) -> VideoChunkingResult:
        """
        Main method: Process script into AI-ready video chunks
        
        Args:
            script: Original movie script text
            session_name: Optional session identifier
            
        Returns:
            VideoChunkingResult with all processed data
        """
        start_time = time.time()
        
        # Generate session ID
        session_id = session_name or f"VS_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"🎬 Starting Video Chunking Session: {session_id}")
        print("="*60)
        
        # Step 1: Analyze and chunk script
        print("📋 Step 1: Analyzing script and creating optimal scenes...")
        scenes = self.scene_analyzer.analyze_script(script)
        print(f"   ✅ Created {len(scenes)} scenes")
        
        # Step 2: Extract character profiles
        print("👥 Step 2: Extracting character profiles and tracking consistency...")
        all_characters = set()
        for scene in scenes:
            all_characters.update(scene.characters)
        
        for scene in scenes:
            self.character_tracker.extract_character_profile(
                scene.content, scene.id, scene.characters
            )
        
        character_profiles = self.character_tracker.characters.copy()
        print(f"   ✅ Tracked {len(character_profiles)} characters")
        
        # Step 3: Build visual contexts and generate enhanced prompts
        print("🎨 Step 3: Building visual contexts and generating enhanced prompts...")
        enhanced_prompts = []
        
        for scene in scenes:
            enhanced_prompt = self.visual_context_builder.generate_enhanced_prompt(
                scene.content, scene.id, scene.characters
            )
            enhanced_prompts.append(enhanced_prompt)
        
        print(f"   ✅ Generated {len(enhanced_prompts)} enhanced prompts")
        
        # Step 4: Calculate quality metrics
        print("📊 Step 4: Calculating quality and continuity metrics...")
        quality_metrics = self._calculate_quality_metrics(scenes, character_profiles)
        continuity_score = self._calculate_continuity_score(scenes, character_profiles)
        
        processing_time = time.time() - start_time
        
        # Create result
        result = VideoChunkingResult(
            session_id=session_id,
            original_script=script,
            total_scenes=len(scenes),
            processing_time=processing_time,
            scenes=scenes,
            enhanced_prompts=enhanced_prompts,
            character_profiles=character_profiles,
            continuity_score=continuity_score,
            quality_metrics=quality_metrics
        )
        
        # Store in session history
        self.session_history[session_id] = result
        
        print(f"\n🏆 Video Chunking Complete!")
        print(f"   📊 Continuity Score: {continuity_score:.2f}")
        print(f"   ⏱️  Processing Time: {processing_time:.2f}s")
        print(f"   🎯 Average Scene Duration: {sum(s.duration for s in scenes)/len(scenes):.1f}s")
        
        return result
    
    def _calculate_quality_metrics(self, scenes: List[VideoScene], 
                                 character_profiles: Dict[str, CharacterProfile]) -> Dict[str, float]:
        """Calculate various quality metrics"""
        metrics = {}
        
        # Scene duration optimization
        target_durations = [abs(scene.duration - self.target_duration) for scene in scenes]
        duration_score = 1.0 - (sum(target_durations) / len(target_durations) / self.target_duration)
        metrics["duration_optimization"] = max(0, min(1, duration_score))
        
        # Character consistency
        character_appearances = {}
        for scene in scenes:
            for char in scene.characters:
                if char not in character_appearances:
                    character_appearances[char] = 0
                character_appearances[char] += 1
        
        consistency_scores = []
        for char_name, profile in character_profiles.items():
            if profile.appearance_count > 1:
                # Characters with multiple appearances should have consistent descriptions
                description_completeness = len([f for f in [
                    profile.gender, profile.age, profile.build, profile.clothing_top
                ] if f])
                consistency_scores.append(description_completeness / 4.0)
        
        metrics["character_consistency"] = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0
        
        # Scene type distribution
        scene_types = [scene.scene_type.value for scene in scenes]
        type_variety = len(set(scene_types)) / len(scene_types) if scene_types else 0
        metrics["scene_variety"] = type_variety
        
        # Dialogue coverage
        dialogue_scenes = sum(1 for scene in scenes if scene.dialogue)
        metrics["dialogue_coverage"] = dialogue_scenes / len(scenes) if scenes else 0
        
        # Overall quality score
        metrics["overall_quality"] = sum(metrics.values()) / len(metrics)
        
        return metrics
    
    def _calculate_continuity_score(self, scenes: List[VideoScene], 
                                  character_profiles: Dict[str, CharacterProfile]) -> float:
        """Calculate overall continuity score"""
        continuity_factors = []
        
        # Character continuity
        for char_name, profile in character_profiles.items():
            if profile.appearance_count > 1:
                # Check if character has consistent core features
                core_features = [profile.gender, profile.age, profile.ethnicity, profile.build]
                feature_completeness = len([f for f in core_features if f]) / len(core_features)
                continuity_factors.append(feature_completeness)
        
        # Scene flow continuity
        for i in range(1, len(scenes)):
            current_scene = scenes[i]
            previous_scene = scenes[i-1]
            
            # Check character overlap
            char_overlap = len(set(current_scene.characters) & set(previous_scene.characters))
            total_chars = len(set(current_scene.characters) | set(previous_scene.characters))
            
            if total_chars > 0:
                overlap_score = char_overlap / total_chars
                continuity_factors.append(overlap_score)
        
        return sum(continuity_factors) / len(continuity_factors) if continuity_factors else 0.8
    
    def generate_video_production_guide(self, session_id: str) -> str:
        """Generate comprehensive video production guide"""
        if session_id not in self.session_history:
            return "Session not found"
        
        result = self.session_history[session_id]
        
        guide = f"""
📋 VIDEO PRODUCTION GUIDE
Session: {result.session_id}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 PROJECT OVERVIEW:
- Total Scenes: {result.total_scenes}
- Target Duration: {sum(s.duration for s in result.scenes):.1f} seconds
- Continuity Score: {result.continuity_score:.2f}/1.0
- Quality Score: {result.quality_metrics['overall_quality']:.2f}/1.0

👥 CHARACTER PROFILES:
"""
        
        for char_name, profile in result.character_profiles.items():
            guide += f"""
- {char_name}:
  - Description: {profile.get_base_description()}
  - Appearances: {profile.appearance_count} scenes
  - Scenes: {profile.first_appearance}-{profile.last_appearance}
"""
        
        guide += f"""
🎬 SCENE BREAKDOWN:
"""
        
        for i, (scene, prompt) in enumerate(zip(result.scenes, result.enhanced_prompts)):
            guide += f"""
Scene {scene.id}: ({scene.duration:.1f}s) - {scene.scene_type.value}
Characters: {', '.join(scene.characters)}
Content: {scene.content[:100]}...

AI Generation Prompt:
{prompt}

---
"""
        
        guide += f"""
📊 PRODUCTION NOTES:
- Average Scene Duration: {sum(s.duration for s in result.scenes)/len(result.scenes):.1f}s
- Dialogue Scenes: {sum(1 for s in result.scenes if s.dialogue)}/{len(result.scenes)}
- Character Consistency: {result.quality_metrics['character_consistency']:.2f}
- Scene Variety: {result.quality_metrics['scene_variety']:.2f}

🎯 RECOMMENDED AI VIDEO GENERATION SETTINGS:
- Resolution: 1920x1080 or higher
- Frame Rate: 24fps for cinematic feel
- Duration per prompt: {self.target_duration}s
- Style: Cinematic, professional lighting
- Consistency: Use exact character descriptions from prompts

✅ READY FOR AI VIDEO GENERATION!
"""
        
        return guide
    
    def export_for_ai_platforms(self, session_id: str, platform: str = "general") -> Dict:
        """Export data formatted for specific AI video platforms"""
        if session_id not in self.session_history:
            return {}
        
        result = self.session_history[session_id]
        
        if platform == "runaway":
            # Format for Runway ML
            return {
                "project_name": result.session_id,
                "scenes": [
                    {
                        "scene_id": i + 1,
                        "prompt": prompt,
                        "duration": scene.duration,
                        "style": "cinematic",
                        "resolution": "1920x1080"
                    }
                    for i, (scene, prompt) in enumerate(zip(result.scenes, result.enhanced_prompts))
                ]
            }
        
        elif platform == "pika":
            # Format for Pika Labs
            return {
                "video_project": {
                    "name": result.session_id,
                    "clips": [
                        {
                            "clip_number": i + 1,
                            "text_prompt": prompt,
                            "duration_seconds": scene.duration,
                            "aspect_ratio": "16:9",
                            "style": "realistic"
                        }
                        for i, (scene, prompt) in enumerate(zip(result.scenes, result.enhanced_prompts))
                    ]
                }
            }
        
        else:
            # General format
            return result.to_dict()
    
    def get_session_summary(self) -> Dict[str, Dict]:
        """Get summary of all processing sessions"""
        summary = {}
        
        for session_id, result in self.session_history.items():
            summary[session_id] = {
                "total_scenes": result.total_scenes,
                "continuity_score": result.continuity_score,
                "processing_time": result.processing_time,
                "characters": list(result.character_profiles.keys()),
                "quality_score": result.quality_metrics['overall_quality']
            }
        
        return summary

# Example usage and test
if __name__ == "__main__":
    orchestrator = VideoChunkingOrchestrator(target_duration=8.0)
    
    # Test script
    test_script = """
    Anh Minh bước ra khỏi nhà tranh nhỏ, ánh nắng sớm mai chiếu rọi lên khuôn mặt khắc khổ của anh. 
    Anh là một người đàn ông Việt Nam 40 tuổi, dáng người gầy, da ngăm đen, mặc áo sơ mi nâu và quần đen.
    
    Anh nhìn ra cánh đồng lúa xanh mướt phía xa, rồi bắt đầu bước đi trên con đường đất. 
    Không khí nông thôn yên bình, chỉ có tiếng chim hót và gió thổi qua lá lúa.
    
    Trên đường, anh gặp em Lan đang cúi xuống hái rau bên vệ đường. 
    Em là một cô gái trẻ khoảng 25 tuổi, mặc áo bà ba trắng, tóc dài buộc gọn.
    
    "Chào em Lan, sáng nay em dậy sớm quá!" anh Minh nói với nụ cười thân thiện.
    "Chào anh Minh! Em phải hái rau sớm để mang ra chợ bán" em Lan trả lời, đứng thẳng lên và cười tươi.
    
    Hai người trò chuyện vài câu về mùa màng, rồi anh Minh tiếp tục đi về phía cánh đồng.
    """
    
    print("🚀 TESTING VIDEO CHUNKING ORCHESTRATOR:")
    print("="*60)
    
    # Process script
    result = orchestrator.process_script(test_script, "Demo_Video_Script")
    
    print(f"\n📋 PROCESSING RESULTS:")
    print(f"   Session ID: {result.session_id}")
    print(f"   Total Scenes: {result.total_scenes}")
    print(f"   Characters: {list(result.character_profiles.keys())}")
    print(f"   Continuity Score: {result.continuity_score:.2f}")
    
    # Show first enhanced prompt
    print(f"\n🎬 SAMPLE ENHANCED PROMPT (Scene 1):")
    print("="*40)
    print(result.enhanced_prompts[0])
    
    # Generate production guide
    print(f"\n📋 PRODUCTION GUIDE PREVIEW:")
    print("="*40)
    guide = orchestrator.generate_video_production_guide(result.session_id)
    print(guide[:500] + "...")
    
    print(f"\n✅ VIDEO CHUNKING ENGINE READY FOR PRODUCTION! 🎬🚀")

    def _scene_to_dict(self, scene):
        """Convert scene to dict with proper enum handling"""
        scene_dict = asdict(scene)
        scene_dict['scene_type'] = scene.scene_type.value  # Convert enum to string
        return scene_dict
