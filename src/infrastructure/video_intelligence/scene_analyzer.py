"""
PRISM Video Intelligence - Scene Analyzer
Advanced scene breakdown for AI video generation with optimal timing
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class SceneType(Enum):
    DIALOGUE = "dialogue"
    ACTION = "action"
    TRANSITION = "transition"
    ESTABLISHING = "establishing"

@dataclass
class VideoScene:
    """Represents a single video scene optimized for AI generation"""
    id: int
    content: str
    scene_type: SceneType
    duration: float  # seconds
    characters: List[str]
    setting: str
    actions: List[str]
    dialogue: Optional[str] = None
    visual_elements: Dict = None
    continuity_requirements: Dict = None

class SceneAnalyzer:
    """
    Advanced scene analysis for video chunking
    Optimizes scenes for 5-10 second AI video generation
    """
    
    def __init__(self, target_duration: float = 8.0):
        self.target_duration = target_duration
        self.min_duration = 5.0
        self.max_duration = 12.0
        
    def analyze_script(self, script: str) -> List[VideoScene]:
        """
        Main method: Analyze script and break into optimal video scenes
        """
        # Clean and prepare script
        cleaned_script = self._clean_script(script)
        
        # Identify natural scene breaks
        raw_scenes = self._identify_scene_breaks(cleaned_script)
        
        # Optimize scene timing
        optimized_scenes = self._optimize_scene_timing(raw_scenes)
        
        # Extract scene metadata
        video_scenes = []
        for i, scene_content in enumerate(optimized_scenes):
            scene = self._create_video_scene(i + 1, scene_content)
            video_scenes.append(scene)
            
        return video_scenes
    
    def _clean_script(self, script: str) -> str:
        """Clean and normalize script text"""
        # Remove extra whitespace
        script = re.sub(r'\s+', ' ', script.strip())
        
        # Normalize punctuation
        script = re.sub(r'[.]{2,}', '...', script)
        script = re.sub(r'[!]{2,}', '!', script)
        script = re.sub(r'[?]{2,}', '?', script)
        
        return script
    
    def _identify_scene_breaks(self, script: str) -> List[str]:
        """Identify natural scene breaks in script"""
        # Scene break patterns
        scene_break_patterns = [
            r'\.(?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ])',  # Period + Capital
            r'[!?](?:\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ])',  # !? + Capital
            r'(?:sau đó|rồi|tiếp theo|lúc này|bỗng nhiên|đột nhiên)',  # Time transitions
            r'(?:cắt đến|chuyển cảnh|fade to|cut to)',  # Scene directions
        ]
        
        # Find potential break points
        break_points = [0]
        for pattern in scene_break_patterns:
            matches = list(re.finditer(pattern, script, re.IGNORECASE))
            for match in matches:
                break_points.append(match.start())
        
        # Sort and deduplicate
        break_points = sorted(list(set(break_points)))
        break_points.append(len(script))
        
        # Extract scenes
        scenes = []
        for i in range(len(break_points) - 1):
            start = break_points[i]
            end = break_points[i + 1]
            scene_text = script[start:end].strip()
            if scene_text:
                scenes.append(scene_text)
                
        return scenes
    
    def _optimize_scene_timing(self, raw_scenes: List[str]) -> List[str]:
        """Optimize scenes for target duration"""
        optimized = []
        
        for scene in raw_scenes:
            # Estimate reading/action time (words per second)
            word_count = len(scene.split())
            estimated_duration = self._estimate_scene_duration(scene)
            
            if estimated_duration <= self.max_duration:
                # Scene is good as-is
                optimized.append(scene)
            else:
                # Split long scene
                sub_scenes = self._split_long_scene(scene)
                optimized.extend(sub_scenes)
                
        # Merge very short scenes
        return self._merge_short_scenes(optimized)
    
    def _estimate_scene_duration(self, scene: str) -> float:
        """Estimate scene duration based on content"""
        words = scene.split()
        word_count = len(words)
        
        # Base reading time (words per second)
        base_wps = 2.5
        
        # Adjust for content type
        if self._contains_dialogue(scene):
            # Dialogue scenes are longer
            wps = 2.0
        elif self._contains_action(scene):
            # Action scenes can be faster
            wps = 3.0
        else:
            wps = base_wps
            
        return word_count / wps
    
    def _contains_dialogue(self, scene: str) -> bool:
        """Check if scene contains dialogue"""
        dialogue_markers = ['"', '"', '"', ':', 'nói', 'hỏi', 'trả lời', 'thì thầm']
        return any(marker in scene.lower() for marker in dialogue_markers)
    
    def _contains_action(self, scene: str) -> bool:
        """Check if scene contains action"""
        action_words = ['chạy', 'nhảy', 'đánh', 'ném', 'bắn', 'lái', 'bay', 'ngã', 'té']
        return any(word in scene.lower() for word in action_words)
    
    def _split_long_scene(self, scene: str) -> List[str]:
        """Split long scene into smaller chunks"""
        sentences = re.split(r'[.!?]', scene)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            test_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if self._estimate_scene_duration(test_chunk) <= self.target_duration:
                current_chunk = test_chunk
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
                
        if current_chunk:
            chunks.append(current_chunk.strip())
            
        return chunks
    
    def _merge_short_scenes(self, scenes: List[str]) -> List[str]:
        """Merge very short scenes together"""
        if not scenes:
            return scenes
            
        merged = []
        current_scene = scenes[0]
        
        for i in range(1, len(scenes)):
            next_scene = scenes[i]
            
            # Check if merging would still be under max duration
            combined = current_scene + " " + next_scene
            if self._estimate_scene_duration(combined) <= self.max_duration:
                current_scene = combined
            else:
                merged.append(current_scene)
                current_scene = next_scene
                
        merged.append(current_scene)
        return merged
    
    def _create_video_scene(self, scene_id: int, content: str) -> VideoScene:
        """Create VideoScene object with metadata"""
        # Determine scene type
        scene_type = self._classify_scene_type(content)
        
        # Extract characters
        characters = self._extract_characters(content)
        
        # Extract setting
        setting = self._extract_setting(content)
        
        # Extract actions
        actions = self._extract_actions(content)
        
        # Extract dialogue
        dialogue = self._extract_dialogue(content)
        
        # Calculate duration
        duration = self._estimate_scene_duration(content)
        
        return VideoScene(
            id=scene_id,
            content=content,
            scene_type=scene_type,
            duration=duration,
            characters=characters,
            setting=setting,
            actions=actions,
            dialogue=dialogue,
            visual_elements={},
            continuity_requirements={}
        )
    
    def _classify_scene_type(self, content: str) -> SceneType:
        """Classify scene type for optimization"""
        if self._contains_dialogue(content):
            return SceneType.DIALOGUE
        elif self._contains_action(content):
            return SceneType.ACTION
        elif any(word in content.lower() for word in ['fade', 'cut', 'chuyển', 'sau đó']):
            return SceneType.TRANSITION
        else:
            return SceneType.ESTABLISHING
    
    def _extract_characters(self, content: str) -> List[str]:
        """Extract character names from scene"""
        # Vietnamese name patterns
        name_patterns = [
            r'(?:anh|em|chị|ông|bà|cô|chú)\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)',
            r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)(?:\s+nói|\s+hỏi|\s+đi|\s+đứng)'
        ]
        
        characters = []
        for pattern in name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            characters.extend(matches)
            
        return list(set(characters))
    
    def _extract_setting(self, content: str) -> str:
        """Extract setting/location from scene"""
        location_keywords = [
            'nhà', 'ruộng', 'đường', 'phố', 'chợ', 'trường', 'công ty', 
            'rừng', 'núi', 'biển', 'sông', 'cầu', 'phòng', 'bếp'
        ]
        
        for keyword in location_keywords:
            if keyword in content.lower():
                return keyword
                
        return "unknown"
    
    def _extract_actions(self, content: str) -> List[str]:
        """Extract action verbs from scene"""
        action_patterns = [
            r'(\w+(?:đi|chạy|nhảy|đứng|ngồi|nằm|ăn|uống|cười|khóc|nhìn|nghe))',
            r'(đang\s+\w+)',
            r'(\w+ing)'  # For mixed language content
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            actions.extend(matches)
            
        return list(set(actions))
    
    def _extract_dialogue(self, content: str) -> Optional[str]:
        """Extract dialogue text from scene"""
        # Find quoted speech
        dialogue_patterns = [
            r'"([^"]+)"',
            r'"([^"]+)"',
            r'"([^"]+)"'
        ]
        
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, content)
            if matches:
                return matches[0]
                
        return None

# Example usage and test
if __name__ == "__main__":
    analyzer = SceneAnalyzer(target_duration=8.0)
    
    # Test script
    test_script = """
    Anh Minh bước ra khỏi nhà tranh nhỏ, ánh nắng sớm mai chiếu rọi lên khuôn mặt khắc khổ của anh. 
    Anh nhìn ra cánh đồng lúa xanh mướt phía xa, rồi bắt đầu bước đi trên con đường đất. 
    Trên đường, anh gặp em Lan đang cúi xuống hái rau bên vệ đường. 
    "Chào em Lan, sáng nay em dậy sớm quá!" anh Minh nói. 
    "Chào anh Minh! Em phải hái rau sớm để mang ra chợ bán" em Lan trả lời với nụ cười tươi.
    """
    
    scenes = analyzer.analyze_script(test_script)
    
    print("🎬 SCENE ANALYSIS RESULTS:")
    print("="*50)
    for scene in scenes:
        print(f"\n🎯 Scene {scene.id}: ({scene.duration:.1f}s)")
        print(f"   Type: {scene.scene_type.value}")
        print(f"   Characters: {scene.characters}")
        print(f"   Setting: {scene.setting}")
        print(f"   Content: {scene.content[:100]}...")
        if scene.dialogue:
            print(f"   Dialogue: {scene.dialogue}")
