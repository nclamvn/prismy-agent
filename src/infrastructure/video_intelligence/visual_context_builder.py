"""
PRISM Video Intelligence - Visual Context Builder
Creates comprehensive visual reference templates for seamless video generation
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class ContextType(Enum):
    CHARACTER = "character"
    SETTING = "setting"
    LIGHTING = "lighting"
    CAMERA = "camera"
    PROPS = "props"
    ATMOSPHERE = "atmosphere"

@dataclass
class VisualReference:
    """Visual reference template for consistent AI generation"""
    scene_id: int
    context_type: ContextType
    primary_description: str
    detailed_features: Dict[str, str]
    consistency_keywords: List[str]
    reference_strength: float  # 0.0 to 1.0
    evolution_notes: str = ""

@dataclass
class SceneVisualContext:
    """Complete visual context for a scene"""
    scene_id: int
    characters: Dict[str, VisualReference]
    setting: VisualReference
    lighting: VisualReference
    atmosphere: VisualReference
    props: List[VisualReference]
    camera_angle: str = ""
    composition_notes: str = ""

class VisualContextBuilder:
    """
    Advanced visual context building for seamless video generation
    Creates detailed reference templates that maintain visual continuity
    """
    
    def __init__(self):
        self.scene_contexts: Dict[int, SceneVisualContext] = {}
        self.global_references: Dict[str, VisualReference] = {}
        
        # Vietnamese visual description patterns
        self.visual_patterns = {
            'character_physical': [
                r'(đàn ông|phụ nữ|nam|nữ)\s+(việt nam|việt|kinh|tây)',
                r'(\d+)\s+tuổi',
                r'dáng\s+(gầy|béo|cao|thấp|mạnh mẽ|nhỏ nhắn)',
                r'da\s+(trắng|đen|ngăm|bánh mật|nâu)',
                r'mặt\s+(tròn|vuông|dài|oval|khắc khổ)',
                r'tóc\s+(ngắn|dài|xoăn|thẳng)\s*(màu\s+)?(đen|nâu|vàng)?'
            ],
            'character_clothing': [
                r'áo\s+(sơ mi|thun|khoác|vest|dài|ngắn)\s*(màu\s+)?([\w\s]+)?',
                r'quần\s+(dài|ngắn|jean|tây|thể thao)\s*(màu\s+)?([\w\s]+)?',
                r'váy\s+(ngắn|dài|midi)\s*(màu\s+)?([\w\s]+)?',
                r'(chân trần|đi chân đất|giày|dép|sandal)',
                r'đeo\s+(kính|nhẫn|vòng cổ|đồng hồ)'
            ],
            'setting_location': [
                r'(nhà tranh|nhà gỗ|nhà bê tông|villa|chung cư)',
                r'(nông thôn|thành phố|vùng quê|trung tâm)',
                r'(cánh đồng|ruộng lúa|vườn|rừng|núi|biển)',
                r'(đường đất|đường nhựa|con đường|lối mòn)',
                r'(phòng|bếp|sân|vườn|cầu thang)'
            ],
            'lighting_time': [
                r'(sáng sớm|buổi sáng|trưa|chiều|tối|đêm)',
                r'(ánh nắng|ánh sáng|bóng tối|hoàng hôn|bình minh)',
                r'(sáng|tối|mờ|rực rỡ|dịu nhẹ)',
                r'(nắng|mưa|sương|mây|quang đãng)'
            ],
            'atmosphere_mood': [
                r'(yên bình|náo nhiệt|buồn|vui|căng thẳng|thư giãn)',
                r'(ấm áp|lạnh|mát mẻ|oi bức|thoáng đãng)',
                r'(thân thiện|nghiêm túc|lãng mạn|bí ẩn|đáng sợ)'
            ],
            'props_objects': [
                r'(xe đạp|xe máy|ô tô|thúng|giỏ|túi)',
                r'(cây|hoa|rau|lúa|cỏ)',
                r'(bàn|ghế|tivi|tủ|giường)',
                r'(điện thoại|máy tính|sách|báo)'
            ]
        }
    
    def build_scene_context(self, scene_content: str, scene_id: int, 
                           characters: List[str], previous_context: Optional[SceneVisualContext] = None) -> SceneVisualContext:
        """Build comprehensive visual context for a scene"""
        
        # Extract visual elements
        character_refs = self._build_character_references(scene_content, scene_id, characters, previous_context)
        setting_ref = self._build_setting_reference(scene_content, scene_id, previous_context)
        lighting_ref = self._build_lighting_reference(scene_content, scene_id, previous_context)
        atmosphere_ref = self._build_atmosphere_reference(scene_content, scene_id, previous_context)
        props_refs = self._build_props_references(scene_content, scene_id, previous_context)
        
        # Create scene context
        scene_context = SceneVisualContext(
            scene_id=scene_id,
            characters=character_refs,
            setting=setting_ref,
            lighting=lighting_ref,
            atmosphere=atmosphere_ref,
            props=props_refs,
            camera_angle=self._extract_camera_info(scene_content),
            composition_notes=self._generate_composition_notes(scene_content)
        )
        
        # Store for future reference
        self.scene_contexts[scene_id] = scene_context
        
        return scene_context
    
    def _build_character_references(self, content: str, scene_id: int, 
                                  characters: List[str], previous_context: Optional[SceneVisualContext]) -> Dict[str, VisualReference]:
        """Build character visual references"""
        char_refs = {}
        
        for char_name in characters:
            # Extract character-specific description
            char_description = self._extract_character_description(content, char_name)
            
            # Get previous reference if available
            previous_ref = None
            if previous_context and char_name in previous_context.characters:
                previous_ref = previous_context.characters[char_name]
            
            # Build detailed features
            detailed_features = self._extract_detailed_features(char_description, 'character')
            
            # Inherit stable features from previous scenes
            if previous_ref:
                detailed_features = self._merge_character_features(detailed_features, previous_ref.detailed_features)
            
            # Create consistency keywords
            consistency_keywords = self._generate_consistency_keywords(detailed_features, 'character')
            
            # Create reference
            char_ref = VisualReference(
                scene_id=scene_id,
                context_type=ContextType.CHARACTER,
                primary_description=self._create_primary_description(detailed_features, 'character'),
                detailed_features=detailed_features,
                consistency_keywords=consistency_keywords,
                reference_strength=0.9  # High strength for character consistency
            )
            
            char_refs[char_name] = char_ref
        
        return char_refs
    
    def _build_setting_reference(self, content: str, scene_id: int, 
                               previous_context: Optional[SceneVisualContext]) -> VisualReference:
        """Build setting visual reference"""
        setting_description = self._extract_setting_description(content)
        detailed_features = self._extract_detailed_features(setting_description, 'setting')
        
        # Inherit setting continuity from previous scene if same location
        if previous_context and self._is_same_location(detailed_features, previous_context.setting.detailed_features):
            detailed_features = self._merge_setting_features(detailed_features, previous_context.setting.detailed_features)
            reference_strength = 0.8  # High continuity
        else:
            reference_strength = 0.6  # New location
        
        consistency_keywords = self._generate_consistency_keywords(detailed_features, 'setting')
        
        return VisualReference(
            scene_id=scene_id,
            context_type=ContextType.SETTING,
            primary_description=self._create_primary_description(detailed_features, 'setting'),
            detailed_features=detailed_features,
            consistency_keywords=consistency_keywords,
            reference_strength=reference_strength
        )
    
    def _build_lighting_reference(self, content: str, scene_id: int,
                                previous_context: Optional[SceneVisualContext]) -> VisualReference:
        """Build lighting visual reference"""
        lighting_description = self._extract_lighting_description(content)
        detailed_features = self._extract_detailed_features(lighting_description, 'lighting')
        
        # Check for time continuity
        if previous_context and self._is_continuous_time(detailed_features, previous_context.lighting.detailed_features):
            detailed_features = self._merge_lighting_features(detailed_features, previous_context.lighting.detailed_features)
            reference_strength = 0.7
        else:
            reference_strength = 0.5
        
        consistency_keywords = self._generate_consistency_keywords(detailed_features, 'lighting')
        
        return VisualReference(
            scene_id=scene_id,
            context_type=ContextType.LIGHTING,
            primary_description=self._create_primary_description(detailed_features, 'lighting'),
            detailed_features=detailed_features,
            consistency_keywords=consistency_keywords,
            reference_strength=reference_strength
        )
    
    def _build_atmosphere_reference(self, content: str, scene_id: int,
                                  previous_context: Optional[SceneVisualContext]) -> VisualReference:
        """Build atmosphere visual reference"""
        atmosphere_description = self._extract_atmosphere_description(content)
        detailed_features = self._extract_detailed_features(atmosphere_description, 'atmosphere')
        consistency_keywords = self._generate_consistency_keywords(detailed_features, 'atmosphere')
        
        return VisualReference(
            scene_id=scene_id,
            context_type=ContextType.ATMOSPHERE,
            primary_description=self._create_primary_description(detailed_features, 'atmosphere'),
            detailed_features=detailed_features,
            consistency_keywords=consistency_keywords,
            reference_strength=0.4  # Atmosphere can change more freely
        )
    
    def _build_props_references(self, content: str, scene_id: int,
                              previous_context: Optional[SceneVisualContext]) -> List[VisualReference]:
        """Build props visual references"""
        props_descriptions = self._extract_props_descriptions(content)
        props_refs = []
        
        for prop_desc in props_descriptions:
            detailed_features = self._extract_detailed_features(prop_desc, 'props')
            consistency_keywords = self._generate_consistency_keywords(detailed_features, 'props')
            
            prop_ref = VisualReference(
                scene_id=scene_id,
                context_type=ContextType.PROPS,
                primary_description=prop_desc,
                detailed_features=detailed_features,
                consistency_keywords=consistency_keywords,
                reference_strength=0.3
            )
            
            props_refs.append(prop_ref)
        
        return props_refs
    
    # MISSING METHODS - ADD THESE:
    
    def _extract_character_description(self, content: str, character_name: str) -> str:
        """Extract character-specific visual description"""
        sentences = re.split(r'[.!?]', content)
        char_sentences = []
        
        search_terms = [character_name, f"anh {character_name}", f"em {character_name}"]
        
        for sentence in sentences:
            for term in search_terms:
                if term.lower() in sentence.lower():
                    char_sentences.append(sentence.strip())
                    break
        
        return " ".join(char_sentences)
    
    def _extract_setting_description(self, content: str) -> str:
        """Extract setting/location description"""
        setting_keywords = ['nhà', 'đường', 'ruộng', 'cánh đồng', 'nông thôn', 'thành phố', 'vườn', 'rừng']
        sentences = re.split(r'[.!?]', content)
        setting_sentences = []
        
        for sentence in sentences:
            for keyword in setting_keywords:
                if keyword in sentence.lower():
                    setting_sentences.append(sentence.strip())
                    break
        
        return " ".join(setting_sentences)
    
    def _extract_lighting_description(self, content: str) -> str:
        """Extract lighting/time description"""
        lighting_keywords = ['ánh nắng', 'sáng', 'tối', 'chiều', 'mai', 'đêm', 'bóng', 'sáng sớm']
        sentences = re.split(r'[.!?]', content)
        lighting_sentences = []
        
        for sentence in sentences:
            for keyword in lighting_keywords:
                if keyword in sentence.lower():
                    lighting_sentences.append(sentence.strip())
                    break
        
        return " ".join(lighting_sentences)
    
    def _extract_atmosphere_description(self, content: str) -> str:
        """Extract atmosphere/mood description"""
        mood_keywords = ['yên bình', 'vui', 'buồn', 'căng thẳng', 'ấm áp', 'lạnh', 'tươi']
        sentences = re.split(r'[.!?]', content)
        mood_sentences = []
        
        for sentence in sentences:
            for keyword in mood_keywords:
                if keyword in sentence.lower():
                    mood_sentences.append(sentence.strip())
                    break
        
        if not mood_sentences:
            return "Bầu không khí tự nhiên"
        
        return " ".join(mood_sentences)
    
    def _extract_props_descriptions(self, content: str) -> List[str]:
        """Extract props/objects descriptions"""
        props_keywords = ['xe', 'cây', 'hoa', 'rau', 'bàn', 'ghế', 'túi', 'giỏ']
        props = []
        
        for keyword in props_keywords:
            if keyword in content.lower():
                props.append(keyword)
        
        return props
    
    def _extract_camera_info(self, content: str) -> str:
        """Extract camera angle information"""
        camera_keywords = ['close up', 'wide shot', 'medium shot', 'góc cao', 'góc thấp']
        
        for keyword in camera_keywords:
            if keyword in content.lower():
                return keyword
        
        return "Medium shot"
    
    def _generate_composition_notes(self, content: str) -> str:
        """Generate composition notes"""
        return "Composition cân đối, tập trung vào nhân vật chính"
    
    def _is_same_location(self, current_features: Dict, previous_features: Dict) -> bool:
        """Check if location is the same as previous scene"""
        current_locations = set(current_features.values())
        previous_locations = set(previous_features.values())
        return len(current_locations.intersection(previous_locations)) > 0
    
    def _is_continuous_time(self, current_features: Dict, previous_features: Dict) -> bool:
        """Check if time is continuous with previous scene"""
        return True  # Simplified for now
    
    def _merge_setting_features(self, current: Dict, previous: Dict) -> Dict:
        """Merge setting features for continuity"""
        merged = previous.copy()
        merged.update(current)
        return merged
    
    def _merge_lighting_features(self, current: Dict, previous: Dict) -> Dict:
        """Merge lighting features for continuity"""
        merged = previous.copy()
        merged.update(current)
        return merged
    
    def _extract_detailed_features(self, description: str, context_type: str) -> Dict[str, str]:
        """Extract detailed visual features from description"""
        features = {}
        
        if context_type == 'character':
            patterns = self.visual_patterns['character_physical'] + self.visual_patterns['character_clothing']
        elif context_type == 'setting':
            patterns = self.visual_patterns['setting_location']
        elif context_type == 'lighting':
            patterns = self.visual_patterns['lighting_time']
        elif context_type == 'atmosphere':
            patterns = self.visual_patterns['atmosphere_mood']
        else:
            patterns = self.visual_patterns['props_objects']
        
        for i, pattern in enumerate(patterns):
            matches = re.findall(pattern, description, re.IGNORECASE)
            if matches:
                features[f"feature_{i}"] = matches[0] if isinstance(matches[0], str) else " ".join(matches[0])
        
        return features
    
    def _merge_character_features(self, new_features: Dict[str, str], 
                                previous_features: Dict[str, str]) -> Dict[str, str]:
        """Merge character features, keeping stable traits"""
        merged = previous_features.copy()
        
        # Only update dynamic features, keep stable ones
        stable_traits = ['feature_0', 'feature_1', 'feature_2', 'feature_3', 'feature_4', 'feature_5']
        
        for key, value in new_features.items():
            if key not in stable_traits or key not in merged:
                merged[key] = value
        
        return merged
    
    def _generate_consistency_keywords(self, features: Dict[str, str], context_type: str) -> List[str]:
        """Generate keywords for consistency checking"""
        keywords = []
        
        for feature_value in features.values():
            if isinstance(feature_value, str):
                words = feature_value.split()
                keywords.extend([word for word in words if len(word) > 2])
        
        return list(set(keywords))
    
    def _create_primary_description(self, features: Dict[str, str], context_type: str) -> str:
        """Create primary description from features"""
        descriptions = []
        
        for feature_value in features.values():
            if isinstance(feature_value, str) and feature_value.strip():
                descriptions.append(feature_value.strip())
        
        return ", ".join(descriptions) if descriptions else f"Chưa xác định {context_type}"
    
    def generate_enhanced_prompt(self, scene_content: str, scene_id: int, 
                               characters: List[str]) -> str:
        """Generate enhanced prompt with visual context"""
        
        # Get previous scene context
        previous_context = None
        if scene_id > 1 and (scene_id - 1) in self.scene_contexts:
            previous_context = self.scene_contexts[scene_id - 1]
        
        # Build current scene context
        current_context = self.build_scene_context(scene_content, scene_id, characters, previous_context)
        
        # Generate enhanced prompt
        enhanced_prompt = f"""
CẢNH {scene_id}: {scene_content}

THAM CHIẾU VISUAL:

NHÂN VẬT:"""
        
        for char_name, char_ref in current_context.characters.items():
            enhanced_prompt += f"""
- {char_name}: {char_ref.primary_description}
  Keywords: {', '.join(char_ref.consistency_keywords[:5])}"""
        
        enhanced_prompt += f"""

BỐI CẢNH: {current_context.setting.primary_description}
ÁNH SÁNG: {current_context.lighting.primary_description}
KHÔNG KHÍ: {current_context.atmosphere.primary_description}"""
        
        if current_context.props:
            enhanced_prompt += f"""
ĐẠO CỤ: {', '.join([prop.primary_description for prop in current_context.props])}"""
        
        enhanced_prompt += f"""

QUAN TRỌNG: Giữ nguyên hoàn toàn đặc điểm ngoại hình của các nhân vật từ cảnh trước.
CHẤT LƯỢNG: Độ phân giải cao, chi tiết sắc nét, phong cách điện ảnh chuyên nghiệp.
"""
        
        return enhanced_prompt.strip()
    
    def get_continuity_report(self) -> Dict[str, any]:
        """Generate continuity report across all scenes"""
        report = {
            "total_scenes": len(self.scene_contexts),
            "character_consistency": {},
            "setting_transitions": [],
            "lighting_changes": [],
            "potential_issues": []
        }
        
        # Analyze character consistency
        all_characters = set()
        for context in self.scene_contexts.values():
            all_characters.update(context.characters.keys())
        
        for char_name in all_characters:
            appearances = []
            for scene_id, context in self.scene_contexts.items():
                if char_name in context.characters:
                    appearances.append(scene_id)
            
            report["character_consistency"][char_name] = {
                "appearances": appearances,
                "total_scenes": len(appearances)
            }
        
        return report

# Example usage and test
if __name__ == "__main__":
    builder = VisualContextBuilder()
    
    # Test scene 1
    scene1_content = """
    Anh Minh bước ra khỏi nhà tranh nhỏ, ánh nắng sớm mai chiếu rọi lên khuôn mặt khắc khổ của anh.
    Anh là một người đàn ông Việt Nam 40 tuổi, dáng người gầy, da ngăm đen, mặc áo sơ mi nâu.
    """
    
    # Test scene 2  
    scene2_content = """
    Anh Minh đi trên con đường đất, cùng bối cảnh nông thôn như trước.
    """
    
    print("🎨 VISUAL CONTEXT BUILDER RESULTS:")
    print("="*50)
    
    # Build context for scene 1
    enhanced_prompt1 = builder.generate_enhanced_prompt(scene1_content, 1, ["Minh"])
    print(f"\n🎬 SCENE 1 ENHANCED PROMPT:")
    print(enhanced_prompt1)
    
    # Build context for scene 2 (with continuity)
    enhanced_prompt2 = builder.generate_enhanced_prompt(scene2_content, 2, ["Minh"])
    print(f"\n🎬 SCENE 2 ENHANCED PROMPT:")
    print(enhanced_prompt2)
    
    # Generate continuity report
    report = builder.get_continuity_report()
    print(f"\n📊 CONTINUITY REPORT:")
    print(f"Total Scenes: {report['total_scenes']}")
    print(f"Characters: {list(report['character_consistency'].keys())}")
