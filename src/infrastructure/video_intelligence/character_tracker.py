"""
PRISM Video Intelligence - Character Tracker
Maintains character consistency across video scenes
"""

import json
import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum

class CharacterFeature(Enum):
    GENDER = "gender"
    AGE = "age"
    ETHNICITY = "ethnicity"
    SKIN_TONE = "skin_tone"
    HEIGHT = "height"
    BUILD = "build"
    HAIR_COLOR = "hair_color"
    HAIR_STYLE = "hair_style"
    FACIAL_FEATURES = "facial_features"
    CLOTHING_TOP = "clothing_top"
    CLOTHING_BOTTOM = "clothing_bottom"
    FOOTWEAR = "footwear"
    ACCESSORIES = "accessories"
    EXPRESSION = "expression"
    POSE = "pose"

@dataclass
class CharacterProfile:
    """Complete character profile for consistency tracking"""
    name: str
    gender: str = ""
    age: str = ""
    ethnicity: str = ""
    skin_tone: str = ""
    height: str = ""
    build: str = ""
    hair_color: str = ""
    hair_style: str = ""
    facial_features: str = ""
    clothing_top: str = ""
    clothing_bottom: str = ""
    footwear: str = ""
    accessories: str = ""
    
    # Dynamic features (can change between scenes)
    current_expression: str = ""
    current_pose: str = ""
    current_action: str = ""
    
    # Scene tracking
    first_appearance: int = 0
    last_appearance: int = 0
    appearance_count: int = 0
    
    def get_base_description(self) -> str:
        """Get stable character description for consistency"""
        features = []
        
        if self.gender: features.append(self.gender)
        if self.ethnicity: features.append(self.ethnicity)
        if self.age: features.append(f"{self.age} tuổi")
        if self.build: features.append(f"dáng {self.build}")
        if self.skin_tone: features.append(f"da {self.skin_tone}")
        if self.facial_features: features.append(self.facial_features)
        if self.hair_style and self.hair_color: 
            features.append(f"{self.hair_style} màu {self.hair_color}")
        if self.clothing_top: features.append(f"áo {self.clothing_top}")
        if self.clothing_bottom: features.append(f"quần {self.clothing_bottom}")
        if self.footwear: features.append(self.footwear)
        if self.accessories: features.append(self.accessories)
        
        return ", ".join(features)
    
    def update_dynamic_features(self, expression: str = "", pose: str = "", action: str = ""):
        """Update changeable features for current scene"""
        if expression: self.current_expression = expression
        if pose: self.current_pose = pose
        if action: self.current_action = action

class CharacterTracker:
    """
    Advanced character consistency tracking system
    Maintains visual continuity across video scenes
    """
    
    def __init__(self):
        self.characters: Dict[str, CharacterProfile] = {}
        self.character_aliases: Dict[str, str] = {}  # Handle "anh Minh", "em Lan", etc.
        self.scene_appearances: Dict[int, List[str]] = {}
        
        # Vietnamese character analysis patterns
        self.feature_patterns = {
            CharacterFeature.GENDER: [
                (r'(?:anh|ông|thầy|bác|chú)\s+(\w+)', 'nam'),
                (r'(?:em|cô|chị|bà|cô)\s+(\w+)', 'nữ'),
                (r'(\w+)(?:\s+là\s+(?:con trai|đàn ông|nam))', 'nam'),
                (r'(\w+)(?:\s+là\s+(?:con gái|phụ nữ|nữ))', 'nữ')
            ],
            CharacterFeature.AGE: [
                (r'(\d+)\s+tuổi', r'\1'),
                (r'(?:khoảng|gần|trên)\s+(\d+)', r'\1'),
                (r'(trẻ|già|trung niên|teen|thiếu niên)', r'\1')
            ],
            CharacterFeature.ETHNICITY: [
                (r'(việt nam|việt|kinh|chinese|nhật|hàn|tây|mỹ)', r'\1')
            ],
            CharacterFeature.SKIN_TONE: [
                (r'da\s+(trắng|đen|ngăm|bánh mật|vàng|nâu)', r'\1'),
                (r'(trắng|đen|ngăm)(?:\s+da)?', r'\1')
            ],
            CharacterFeature.BUILD: [
                (r'dáng\s+(gầy|béo|to|nhỏ|cao|thấp|mạnh mẽ)', r'\1'),
                (r'(gầy|béo|to|nhỏ|cao|thấp)(?:\s+người)?', r'\1')
            ],
            CharacterFeature.HAIR_COLOR: [
                (r'tóc\s+màu\s+(đen|nâu|vàng|đỏ|bạc|trắng)', r'\1'),
                (r'tóc\s+(đen|nâu|vàng|đỏ|bạc|trắng)', r'\1')
            ],
            CharacterFeature.HAIR_STYLE: [
                (r'(tóc ngắn|tóc dài|đầu trọc|mái tóc)', r'\1'),
                (r'mái\s+(ngắn|dài|bob|xoăn)', r'mái \1')
            ],
            CharacterFeature.FACIAL_FEATURES: [
                (r'(mặt tròn|mặt vuông|mặt dài|mặt khắc khổ|đẹp trai|xinh đẹp)', r'\1'),
                (r'khuôn mặt\s+([\w\s]+)', r'\1')
            ],
            CharacterFeature.CLOTHING_TOP: [
                (r'áo\s+(sơ mi|thun|khoác|vest|dài|ngắn)', r'\1'),
                (r'mặc\s+áo\s+([\w\s]+)', r'\1')
            ],
            CharacterFeature.CLOTHING_BOTTOM: [
                (r'quần\s+(dài|ngắn|jean|tây|thể thao)', r'\1'),
                (r'váy\s+(ngắn|dài|midi)', r'váy \1')
            ],
            CharacterFeature.FOOTWEAR: [
                (r'(chân trần|đi chân đất|giày|dép|sandal)', r'\1'),
                (r'đi\s+([\w\s]+)', r'\1')
            ]
        }
    
    def extract_character_profile(self, scene_content: str, scene_id: int, characters: List[str]) -> Dict[str, CharacterProfile]:
        """Extract character profiles from scene content"""
        profiles = {}
        
        for char_name in characters:
            if char_name in self.characters:
                profile = self.characters[char_name]
            else:
                profile = CharacterProfile(name=char_name, first_appearance=scene_id)
                
            # Extract features from scene content
            self._update_profile_from_content(profile, scene_content, char_name)
            
            # Update tracking info
            profile.last_appearance = scene_id
            profile.appearance_count += 1
            
            profiles[char_name] = profile
            self.characters[char_name] = profile
            
        # Track scene appearances
        self.scene_appearances[scene_id] = characters
        
        return profiles
    
    def _update_profile_from_content(self, profile: CharacterProfile, content: str, character_name: str):
        """Update character profile based on scene content"""
        # Create character-specific content (focus on mentions of this character)
        char_context = self._extract_character_context(content, character_name)
        
        # Extract each feature type
        for feature_type, patterns in self.feature_patterns.items():
            for pattern, replacement in patterns:
                matches = re.findall(pattern, char_context, re.IGNORECASE)
                if matches:
                    feature_value = matches[0] if isinstance(matches[0], str) else replacement
                    self._set_profile_feature(profile, feature_type, feature_value)
    
    def _extract_character_context(self, content: str, character_name: str) -> str:
        """Extract sentences that mention specific character"""
        sentences = re.split(r'[.!?]', content)
        char_sentences = []
        
        # Look for character name and common aliases
        search_terms = [
            character_name,
            f"anh {character_name}",
            f"em {character_name}",
            f"chị {character_name}",
            f"ông {character_name}",
            f"bà {character_name}"
        ]
        
        for sentence in sentences:
            for term in search_terms:
                if term.lower() in sentence.lower():
                    char_sentences.append(sentence.strip())
                    break
                    
        return " ".join(char_sentences)
    
    def _set_profile_feature(self, profile: CharacterProfile, feature_type: CharacterFeature, value: str):
        """Set feature value on profile"""
        # Only update if not already set (maintain consistency)
        feature_name = feature_type.value
        current_value = getattr(profile, feature_name, "")
        
        if not current_value and value:
            setattr(profile, feature_name, value)
    
    def get_character_consistency_prompt(self, character_name: str, scene_id: int) -> str:
        """Generate consistency prompt for character in current scene"""
        if character_name not in self.characters:
            return f"Nhân vật {character_name}"
            
        profile = self.characters[character_name]
        base_description = profile.get_base_description()
        
        # Add previous scene context if available
        previous_context = self._get_previous_scene_context(character_name, scene_id)
        
        consistency_prompt = f"""
NHÂN VẬT: {character_name}
ĐẶCTRƯNG CỐ ĐỊNH: {base_description}
{previous_context}
QUAN TRỌNG: Giữ nguyên hoàn toàn tất cả đặc điểm ngoại hình ở trên"""
        
        return consistency_prompt.strip()
    
    def _get_previous_scene_context(self, character_name: str, current_scene: int) -> str:
        """Get visual context from previous scenes"""
        context_parts = []
        
        # Look at last 2-3 scenes for context
        previous_scenes = []
        for scene_id in range(max(1, current_scene - 3), current_scene):
            if scene_id in self.scene_appearances and character_name in self.scene_appearances[scene_id]:
                previous_scenes.append(scene_id)
        
        if previous_scenes:
            context_parts.append(f"XUẤT HIỆN TRƯỚC: Scene {', '.join(map(str, previous_scenes))}")
            
        return "\n".join(context_parts)
    
    def validate_character_consistency(self, character_name: str, new_description: str) -> Dict[str, float]:
        """Validate consistency of new character description"""
        if character_name not in self.characters:
            return {"consistency_score": 1.0, "warnings": []}
            
        profile = self.characters[character_name]
        warnings = []
        consistency_scores = []
        
        # Check each feature for consistency
        for feature_type in CharacterFeature:
            if feature_type in [CharacterFeature.EXPRESSION, CharacterFeature.POSE]:
                continue  # Skip dynamic features
                
            feature_name = feature_type.value
            original_value = getattr(profile, feature_name, "")
            
            if original_value:
                # Check if new description conflicts
                if self._has_conflicting_feature(new_description, feature_type, original_value):
                    warnings.append(f"Conflict in {feature_name}: original='{original_value}'")
                    consistency_scores.append(0.0)
                else:
                    consistency_scores.append(1.0)
        
        overall_score = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0
        
        return {
            "consistency_score": overall_score,
            "warnings": warnings,
            "character_profile": asdict(profile)
        }
    
    def _has_conflicting_feature(self, description: str, feature_type: CharacterFeature, original_value: str) -> bool:
        """Check if description conflicts with original feature"""
        patterns = self.feature_patterns.get(feature_type, [])
        
        for pattern, _ in patterns:
            matches = re.findall(pattern, description, re.IGNORECASE)
            if matches and matches[0].lower() != original_value.lower():
                return True
                
        return False
    
    def get_all_characters_summary(self) -> Dict[str, Dict]:
        """Get summary of all tracked characters"""
        summary = {}
        for name, profile in self.characters.items():
            summary[name] = {
                "name": profile.name,
                "base_description": profile.get_base_description(),
                "appearances": profile.appearance_count,
                "first_scene": profile.first_appearance,
                "last_scene": profile.last_appearance
            }
        return summary
    
    def export_character_database(self) -> str:
        """Export character database as JSON"""
        export_data = {}
        for name, profile in self.characters.items():
            export_data[name] = asdict(profile)
        
        return json.dumps(export_data, ensure_ascii=False, indent=2)

# Example usage and test
if __name__ == "__main__":
    tracker = CharacterTracker()
    
    # Test character extraction
    test_content = """
    Anh Minh bước ra khỏi nhà tranh nhỏ, ánh nắng sớm mai chiếu rọi lên khuôn mặt khắc khổ của anh.
    Anh là một người đàn ông Việt Nam 40 tuổi, dáng người gầy, da ngăm đen.
    Anh mặc áo sơ mi màu nâu, quần đen và đi chân trần.
    """
    
    characters = ["Minh"]
    profiles = tracker.extract_character_profile(test_content, 1, characters)
    
    print("🎭 CHARACTER TRACKING RESULTS:")
    print("="*50)
    
    for name, profile in profiles.items():
        print(f"\n👤 Character: {name}")
        print(f"   Description: {profile.get_base_description()}")
        print(f"   Appearances: {profile.appearance_count}")
        
    # Test consistency prompt
    consistency_prompt = tracker.get_character_consistency_prompt("Minh", 2)
    print(f"\n🎯 CONSISTENCY PROMPT:")
    print(consistency_prompt)
    
    # Test validation
    new_desc = "Anh Minh người gầy da ngăm đen mặc áo nâu"
    validation = tracker.validate_character_consistency("Minh", new_desc)
    print(f"\n✅ CONSISTENCY VALIDATION:")
    print(f"   Score: {validation['consistency_score']:.2f}")
    print(f"   Warnings: {validation['warnings']}")
