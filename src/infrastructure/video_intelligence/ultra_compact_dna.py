"""
PRISM Ultra-Compact DNA System
Lightweight but comprehensive visual fingerprinting
Optimized for 200+ chunk film scripts
"""

import json
import hashlib
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import re
import time

@dataclass
class CompactDNAFeature:
    """Ultra-compact DNA feature - only essential data"""
    value: str                    # Primary value
    confidence: float            # 0.0-1.0
    inheritance: str            # "keep", "evolve", "change"
    
    def __str__(self):
        return self.value

@dataclass 
class UltraCompactDNA:
    """Ultra-lightweight DNA for adjacency-based system"""
    chunk_id: int
    
    # VISUAL FEATURES (thị giác)
    characters: Dict[str, Dict[str, CompactDNAFeature]]  # {char_name: {feature: value}}
    environment: Dict[str, CompactDNAFeature]            # Location, lighting, props
    visual_style: Dict[str, CompactDNAFeature]           # Colors, composition, camera
    audio_visual: Dict[str, CompactDNAFeature]           # Sound, music, tone
    
    # EMOTIONAL CONTENT (cảm xúc nội dung)  
    narrative: Dict[str, CompactDNAFeature]              # Story flow, meaning
    emotions: Dict[str, CompactDNAFeature]               # Character emotions, mood
    atmosphere: Dict[str, CompactDNAFeature]             # Scene atmosphere, tension
    
    # ADJACENCY LINKS (only connect to neighbors)
    prev_link: Optional[str] = None                      # Previous chunk DNA hash
    next_prep: Optional[Dict] = None                     # Preparation for next chunk
    
    dna_hash: str = ""
    
    def generate_compact_hash(self) -> str:
        """Generate ultra-compact hash"""
        essential_data = {
            "chars": {name: {k: v.value for k, v in features.items()} 
                     for name, features in self.characters.items()},
            "env": {k: v.value for k, v in self.environment.items()},
            "id": self.chunk_id
        }
        content = json.dumps(essential_data, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:8]  # Only 8 chars

class UltraCompactDNAEngine:
    """
    Ultra-efficient DNA engine for large-scale film scripts
    Scientific organization of visual and emotional metadata
    """
    
    def __init__(self, source_language: str = "auto"):
        self.source_language = source_language
        self.adjacency_cache: Dict[int, UltraCompactDNA] = {}  # Only keep recent chunks
        self.cache_size = 3  # Only keep current + 2 neighbors
        
        # Scientific feature taxonomy
        self.feature_taxonomy = self._initialize_taxonomy()
        
    def _initialize_taxonomy(self) -> Dict:
        """Scientific taxonomy of visual and emotional features"""
        return {
            "character_anthropology": {
                "ethnicity": ["asian", "caucasian", "african", "hispanic", "mixed"],
                "age_group": ["child", "teen", "young_adult", "middle_aged", "elderly"],
                "gender": ["male", "female", "non_binary"],
                "build": ["slim", "average", "athletic", "heavy", "tall", "short"],
                "skin_tone": ["very_fair", "fair", "medium", "olive", "brown", "dark"]
            },
            "character_appearance": {
                "hair_color": ["black", "brown", "blonde", "red", "gray", "white"],
                "hair_style": ["short", "long", "curly", "straight", "bald"],
                "facial_features": ["round", "oval", "square", "angular", "soft"],
                "clothing_style": ["casual", "formal", "traditional", "modern", "work"],
                "accessories": ["glasses", "jewelry", "hat", "none"]
            },
            "environment_physical": {
                "location_type": ["indoor", "outdoor", "urban", "rural", "natural"],
                "architecture": ["traditional", "modern", "rustic", "industrial"],
                "landscape": ["flat", "hilly", "mountainous", "water", "forest"],
                "weather": ["sunny", "cloudy", "rainy", "stormy", "foggy"],
                "time_of_day": ["dawn", "morning", "noon", "afternoon", "evening", "night"]
            },
            "visual_technical": {
                "lighting_quality": ["natural", "artificial", "dramatic", "soft", "harsh"],
                "color_palette": ["warm", "cool", "neutral", "vibrant", "muted"],
                "camera_angle": ["eye_level", "high", "low", "close_up", "wide"],
                "composition": ["centered", "rule_of_thirds", "symmetrical", "dynamic"],
                "visual_style": ["realistic", "stylized", "cinematic", "documentary"]
            },
            "audio_elements": {
                "ambient_sound": ["quiet", "nature", "urban", "indoor", "mechanical"],
                "music_mood": ["upbeat", "melancholy", "tense", "peaceful", "dramatic"],
                "voice_tone": ["calm", "excited", "angry", "sad", "authoritative"],
                "sound_design": ["minimal", "rich", "echo", "clear", "muffled"]
            },
            "narrative_structure": {
                "story_beat": ["exposition", "inciting", "rising", "climax", "falling", "resolution"],
                "character_arc": ["introduction", "development", "conflict", "growth", "conclusion"],
                "pacing": ["slow", "moderate", "fast", "varied"],
                "tension_level": ["low", "building", "high", "peak", "release"]
            },
            "emotional_content": {
                "primary_emotion": ["joy", "sadness", "anger", "fear", "surprise", "disgust", "neutral"],
                "emotional_intensity": ["subtle", "moderate", "strong", "overwhelming"],
                "character_mood": ["happy", "sad", "angry", "calm", "excited", "worried"],
                "scene_atmosphere": ["peaceful", "tense", "romantic", "mysterious", "comedic", "dramatic"]
            }
        }
    
    def extract_ultra_compact_dna(self, chunk_content: str, chunk_id: int, 
                                characters: List[str], 
                                previous_dna: Optional[UltraCompactDNA] = None) -> UltraCompactDNA:
        """
        Extract ultra-compact DNA with scientific organization
        """
        
        # Detect language
        language = self._detect_language(chunk_content)
        
        # Extract each category using scientific taxonomy
        char_dna = self._extract_character_dna(chunk_content, characters, language)
        env_dna = self._extract_environment_dna(chunk_content, language)
        visual_dna = self._extract_visual_technical_dna(chunk_content, language)
        audio_dna = self._extract_audio_dna(chunk_content, language)
        narrative_dna = self._extract_narrative_dna(chunk_content, language)
        emotional_dna = self._extract_emotional_dna(chunk_content, language)
        atmosphere_dna = self._extract_atmosphere_dna(chunk_content, language)
        
        # Inherit from previous DNA (adjacency-based)
        if previous_dna:
            char_dna, env_dna, visual_dna = self._inherit_from_adjacent(
                char_dna, env_dna, visual_dna, previous_dna
            )
        
        # Create compact DNA
        dna = UltraCompactDNA(
            chunk_id=chunk_id,
            characters=char_dna,
            environment=env_dna,
            visual_style=visual_dna,
            audio_visual=audio_dna,
            narrative=narrative_dna,
            emotions=emotional_dna,
            atmosphere=atmosphere_dna,
            prev_link=previous_dna.dna_hash if previous_dna else None
        )
        
        # Generate compact hash
        dna.dna_hash = dna.generate_compact_hash()
        
        # Update adjacency cache (keep only recent)
        self._update_adjacency_cache(chunk_id, dna)
        
        return dna
    
    def _extract_character_dna(self, content: str, characters: List[str], language: str) -> Dict[str, Dict[str, CompactDNAFeature]]:
        """Extract character DNA using scientific anthropology"""
        char_dna = {}
        
        for char_name in characters:
            char_content = self._extract_character_context(content, char_name)
            char_features = {}
            
            # Anthropological features (immutable)
            if language == "vietnamese":
                patterns = {
                    "ethnicity": r'(việt nam|việt|kinh|tây|á đông|châu âu|châu phi)',
                    "age_group": self._classify_age_group(char_content),
                    "gender": r'(đàn ông|phụ nữ|nam|nữ|anh|em|chị)',
                    "build": r'(gầy|béo|cao|thấp|to|nhỏ|mạnh mẽ)',
                    "skin_tone": r'da\s*(trắng|đen|ngăm|bánh mật|nâu|vàng)'
                }
            else:
                patterns = {
                    "ethnicity": r'\b(asian|caucasian|african|hispanic|vietnamese)\b',
                    "age_group": self._classify_age_group(char_content),
                    "gender": r'\b(man|woman|male|female|boy|girl)\b',
                    "build": r'\b(thin|fat|tall|short|muscular|petite)\b',
                    "skin_tone": r'\b(pale|dark|tan|fair|olive|brown)\b'
                }
            
            # Extract and classify features
            for feature_type, pattern in patterns.items():
                if isinstance(pattern, str):
                    matches = re.findall(pattern, char_content, re.IGNORECASE)
                    if matches:
                        value = self._normalize_to_taxonomy(matches[0], "character_anthropology", feature_type)
                        char_features[feature_type] = CompactDNAFeature(
                            value=value,
                            confidence=0.9,
                            inheritance="keep"  # Anthropological features never change
                        )
                else:
                    # Pattern is a function result
                    value = pattern
                    if value:
                        char_features[feature_type] = CompactDNAFeature(
                            value=value,
                            confidence=0.8,
                            inheritance="keep"
                        )
            
            # Appearance features (semi-mutable)
            appearance_patterns = {
                "hair_color": r'tóc.*?(đen|nâu|vàng|bạc|đỏ)' if language == "vietnamese" else r'\b(black|brown|blonde|silver|red)\s*hair\b',
                "hair_style": r'(tóc ngắn|tóc dài|đầu trọc)' if language == "vietnamese" else r'\b(short|long|curly|straight)\s*hair\b',
                "clothing_style": r'(áo.*?|quần.*?)' if language == "vietnamese" else r'\b(shirt|pants|dress|suit)\b'
            }
            
            for feature_type, pattern in appearance_patterns.items():
                matches = re.findall(pattern, char_content, re.IGNORECASE)
                if matches:
                    value = self._normalize_to_taxonomy(matches[0], "character_appearance", feature_type)
                    char_features[feature_type] = CompactDNAFeature(
                        value=value,
                        confidence=0.7,
                        inheritance="evolve"  # Can change slowly
                    )
            
            if char_features:
                char_dna[char_name] = char_features
        
        return char_dna
    
    def _extract_environment_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract environment DNA using scientific taxonomy"""
        env_dna = {}
        
        if language == "vietnamese":
            patterns = {
                "location_type": r'(nhà|cửa hàng|trường|công ty|ngoài trời|trong nhà)',
                "architecture": r'(nhà tranh|nhà gỗ|nhà bê tông|hiện đại|cổ điển)',
                "landscape": r'(cánh đồng|ruộng|rừng|núi|biển|sông)',
                "weather": r'(nắng|mưa|gió|sương|quang đãng)',
                "time_of_day": r'(sáng|trưa|chiều|tối|đêm|sáng sớm|hoàng hôn)'
            }
        else:
            patterns = {
                "location_type": r'\b(house|shop|school|office|outdoor|indoor)\b',
                "architecture": r'\b(traditional|modern|rustic|industrial|classical)\b',
                "landscape": r'\b(field|forest|mountain|ocean|river|lake)\b',
                "weather": r'\b(sunny|rainy|windy|foggy|clear)\b',
                "time_of_day": r'\b(morning|noon|afternoon|evening|night|dawn|dusk)\b'
            }
        
        for feature_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                value = self._normalize_to_taxonomy(matches[0], "environment_physical", feature_type)
                
                # Determine inheritance based on feature type
                inheritance = "keep" if feature_type in ["location_type", "architecture"] else "evolve"
                
                env_dna[feature_type] = CompactDNAFeature(
                    value=value,
                    confidence=0.8,
                    inheritance=inheritance
                )
        
        return env_dna
    
    def _extract_visual_technical_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract visual technical DNA"""
        visual_dna = {}
        
        # Technical indicators
        if language == "vietnamese":
            patterns = {
                "lighting_quality": r'(ánh nắng|ánh sáng|sáng|tối|dịu|chói)',
                "color_palette": r'(màu.*?|sắc.*?|tông màu)',
                "camera_angle": r'(close up|wide shot|góc cao|góc thấp)'
            }
        else:
            patterns = {
                "lighting_quality": r'\b(natural light|artificial|bright|dim|soft|harsh)\b',
                "color_palette": r'\b(warm|cool|vibrant|muted|colorful)\b',
                "camera_angle": r'\b(close up|wide shot|high angle|low angle)\b'
            }
        
        for feature_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                value = self._normalize_to_taxonomy(matches[0], "visual_technical", feature_type)
                visual_dna[feature_type] = CompactDNAFeature(
                    value=value,
                    confidence=0.6,
                    inheritance="change"  # Technical aspects can change frequently
                )
        
        return visual_dna
    
    def _extract_audio_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract audio-visual DNA"""
        audio_dna = {}
        
        if language == "vietnamese":
            patterns = {
                "ambient_sound": r'(yên tĩnh|ồn ào|tiếng.*?|âm thanh)',
                "voice_tone": r'(to|nhỏ|dịu dàng|nghiêm túc|vui vẻ)',
                "music_mood": r'(buồn|vui|căng thẳng|yên bình)'
            }
        else:
            patterns = {
                "ambient_sound": r'\b(quiet|noisy|sound of|silence)\b',
                "voice_tone": r'\b(loud|soft|gentle|serious|cheerful)\b',
                "music_mood": r'\b(sad|happy|tense|peaceful|dramatic)\b'
            }
        
        for feature_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                value = self._normalize_to_taxonomy(matches[0], "audio_elements", feature_type)
                audio_dna[feature_type] = CompactDNAFeature(
                    value=value,
                    confidence=0.5,
                    inheritance="change"
                )
        
        return audio_dna
    
    def _extract_narrative_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract narrative structure DNA"""
        narrative_dna = {}
        
        # Determine story beat based on content analysis
        story_beat = self._analyze_story_beat(content)
        if story_beat:
            narrative_dna["story_beat"] = CompactDNAFeature(
                value=story_beat,
                confidence=0.7,
                inheritance="evolve"
            )
        
        # Determine pacing
        pacing = self._analyze_pacing(content)
        if pacing:
            narrative_dna["pacing"] = CompactDNAFeature(
                value=pacing,
                confidence=0.6,
                inheritance="change"
            )
        
        return narrative_dna
    
    def _extract_emotional_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract emotional content DNA"""
        emotional_dna = {}
        
        if language == "vietnamese":
            emotion_patterns = {
                "primary_emotion": r'(vui|buồn|giận|sợ|ngạc nhiên|bình thản)',
                "emotional_intensity": r'(nhẹ nhàng|mạnh mẽ|dữ dội|êm dịu)',
                "character_mood": r'(hạnh phúc|lo lắng|căng thẳng|thư giãn)'
            }
        else:
            emotion_patterns = {
                "primary_emotion": r'\b(happy|sad|angry|scared|surprised|calm)\b',
                "emotional_intensity": r'\b(subtle|strong|intense|gentle)\b',
                "character_mood": r'\b(joyful|worried|tense|relaxed)\b'
            }
        
        for feature_type, pattern in emotion_patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                value = self._normalize_to_taxonomy(matches[0], "emotional_content", feature_type)
                emotional_dna[feature_type] = CompactDNAFeature(
                    value=value,
                    confidence=0.7,
                    inheritance="change"  # Emotions change frequently
                )
        
        return emotional_dna
    
    def _extract_atmosphere_dna(self, content: str, language: str) -> Dict[str, CompactDNAFeature]:
        """Extract scene atmosphere DNA"""
        atmosphere_dna = {}
        
        if language == "vietnamese":
            patterns = {
                "scene_atmosphere": r'(yên bình|căng thẳng|lãng mạn|bí ẩn|hài hước|nghiêm túc)'
            }
        else:
            patterns = {
                "scene_atmosphere": r'\b(peaceful|tense|romantic|mysterious|comedic|dramatic)\b'
            }
        
        for feature_type, pattern in patterns.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                value = self._normalize_to_taxonomy(matches[0], "emotional_content", feature_type)
                atmosphere_dna[feature_type] = CompactDNAFeature(
                    value=value,
                    confidence=0.6,
                    inheritance="change"
                )
        
        return atmosphere_dna
    
    # Helper methods
    def _classify_age_group(self, content: str) -> str:
        """Classify age group from content"""
        age_match = re.search(r'(\d+)\s*tuổi', content)
        if age_match:
            age = int(age_match.group(1))
            if age < 13: return "child"
            elif age < 20: return "teen" 
            elif age < 35: return "young_adult"
            elif age < 55: return "middle_aged"
            else: return "elderly"
        
        # Fallback to keywords
        if any(word in content.lower() for word in ['trẻ em', 'bé', 'child']):
            return "child"
        elif any(word in content.lower() for word in ['thiếu niên', 'teen']):
            return "teen"
        else:
            return "young_adult"  # Default
    
    def _normalize_to_taxonomy(self, value: str, category: str, feature_type: str) -> str:
        """Normalize extracted value to scientific taxonomy"""
        value = value.lower().strip()
        
        # Get valid values for this feature type
        valid_values = self.feature_taxonomy.get(category, {}).get(feature_type, [])
        
        if not valid_values:
            return value
        
        # Direct match
        if value in valid_values:
            return value
        
        # Vietnamese to English mapping
        mappings = {
            "việt nam": "asian", "việt": "asian", "kinh": "asian", "tây": "caucasian",
            "đàn ông": "male", "phụ nữ": "female", "nam": "male", "nữ": "female",
            "gầy": "slim", "béo": "heavy", "cao": "tall", "thấp": "short",
            "trắng": "fair", "đen": "dark", "ngăm": "medium",
            "sáng": "morning", "trưa": "noon", "chiều": "afternoon", "tối": "evening"
        }
        
        mapped_value = mappings.get(value, value)
        if mapped_value in valid_values:
            return mapped_value
        
        # Partial match
        for valid_value in valid_values:
            if value in valid_value or valid_value in value:
                return valid_value
        
        # Default to first valid value
        return valid_values[0] if valid_values else value
    
    def _inherit_from_adjacent(self, current_char: Dict, current_env: Dict, current_visual: Dict,
                             previous_dna: UltraCompactDNA) -> Tuple[Dict, Dict, Dict]:
        """Inherit features from adjacent chunk only"""
        
        # Character inheritance (keep immutable features)
        for char_name, prev_features in previous_dna.characters.items():
            if char_name in current_char:
                for feature_name, prev_feature in prev_features.items():
                    if prev_feature.inheritance == "keep" and feature_name not in current_char[char_name]:
                        # Inherit with slightly reduced confidence
                        current_char[char_name][feature_name] = CompactDNAFeature(
                            value=prev_feature.value,
                            confidence=prev_feature.confidence * 0.95,
                            inheritance=prev_feature.inheritance
                        )
        
        # Environment inheritance (keep stable features)
        for feature_name, prev_feature in previous_dna.environment.items():
            if prev_feature.inheritance in ["keep", "evolve"] and feature_name not in current_env:
                current_env[feature_name] = CompactDNAFeature(
                    value=prev_feature.value,
                    confidence=prev_feature.confidence * 0.9,
                    inheritance=prev_feature.inheritance
                )
        
        return current_char, current_env, current_visual
    
    def _update_adjacency_cache(self, chunk_id: int, dna: UltraCompactDNA):
        """Update adjacency cache with size limit"""
        self.adjacency_cache[chunk_id] = dna
        
        # Keep only recent chunks (sliding window)
        if len(self.adjacency_cache) > self.cache_size:
            oldest_id = min(self.adjacency_cache.keys())
            del self.adjacency_cache[oldest_id]
    
    def _detect_language(self, content: str) -> str:
        """Detect content language"""
        vietnamese_chars = len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', content.lower()))
        if vietnamese_chars > 5:
            return "vietnamese"
        return "english"
    
    def _extract_character_context(self, content: str, character_name: str) -> str:
        """Extract character-specific context"""
        sentences = re.split(r'[.!?]', content)
        char_sentences = []
        
        search_terms = [character_name, f"anh {character_name}", f"em {character_name}"]
        
        for sentence in sentences:
            for term in search_terms:
                if term.lower() in sentence.lower():
                    char_sentences.append(sentence.strip())
                    break
        
        return " ".join(char_sentences)
    
    def _analyze_story_beat(self, content: str) -> str:
        """Analyze story beat from content"""
        # Simple heuristics
        if any(word in content.lower() for word in ['fade in', 'bắt đầu', 'mở đầu']):
            return "exposition"
        elif any(word in content.lower() for word in ['suddenly', 'bỗng nhiên', 'đột nhiên']):
            return "inciting"
        elif any(word in content.lower() for word in ['climax', 'cao trào']):
            return "climax"
        elif any(word in content.lower() for word in ['end', 'kết thúc', 'fade out']):
            return "resolution"
        else:
            return "rising"  # Default
    
    def _analyze_pacing(self, content: str) -> str:
        """Analyze pacing from content"""
        # Simple heuristics based on sentence length and action words
        sentences = len(re.split(r'[.!?]', content))
        action_words = len(re.findall(r'(chạy|nhảy|nhanh|nhanh chóng|run|jump|fast|quickly)', content, re.IGNORECASE))
        
        if action_words > 2:
            return "fast"
        elif sentences > 3:
            return "slow"
        else:
            return "moderate"
    
    def generate_ultra_compact_prompt(self, chunk_content: str, dna: UltraCompactDNA, 
                                    target_language: str = "auto") -> str:
        """
        Generate ultra-sophisticated prompt from compact DNA
        Optimized for AI video generation
        """
        
        if target_language == "auto":
            target_language = self._detect_language(chunk_content)
        
        if target_language == "vietnamese":
            return self._generate_vietnamese_compact_prompt(chunk_content, dna)
        else:
            return self._generate_english_compact_prompt(chunk_content, dna)
    
    def _generate_vietnamese_compact_prompt(self, content: str, dna: UltraCompactDNA) -> str:
        """Generate Vietnamese ultra-compact prompt"""
        
        prompt = f"""🎬 CẢNH {dna.chunk_id}: {content}

🧬 VÂN TAY HÌNH ẢNH [DNA: {dna.dna_hash}]"""
        
        # Characters (highest priority)
        if dna.characters:
            prompt += f"\n\n👥 NHÂN VẬT:"
            for char_name, features in dna.characters.items():
                char_desc = []
                for feature_name, feature in features.items():
                    char_desc.append(feature.value)
                prompt += f"\n• {char_name}: {', '.join(char_desc)}"
        
        # Environment (second priority)
        if dna.environment:
            prompt += f"\n\n🌍 BỐI CẢNH:"
            for feature_name, feature in dna.environment.items():
                prompt += f"\n• {feature_name.title()}: {feature.value}"
        
        # Visual style (third priority)
        if dna.visual_style:
            prompt += f"\n\n🎨 PHONG CÁCH:"
            for feature_name, feature in dna.visual_style.items():
                prompt += f"\n• {feature_name.title()}: {feature.value}"
        
        # Emotional content (fourth priority)
        emotional_elements = []
        if dna.emotions:
            emotional_elements.extend([f.value for f in dna.emotions.values()])
        if dna.atmosphere:
            emotional_elements.extend([f.value for f in dna.atmosphere.values()])
        
        if emotional_elements:
            prompt += f"\n\n💫 CẢM XÚC: {', '.join(emotional_elements)}"
        
        # Continuity link
        if dna.prev_link:
            prompt += f"\n\n🔗 LIÊN KẾT: {dna.prev_link}"
        
        prompt += f"""

⚡ SIÊU QUAN TRỌNG:
- Duy trì CHÍNH XÁC 100% tất cả đặc điểm trong Vân Tay Hình Ảnh
- Chất lượng: 4K ultra-sharp, điện ảnh chuyên nghiệp
- Thời lượng: 8 giây mượt mà, liên tục hoàn hảo
- Style: Hyper-realistic, chi tiết sắc nét tuyệt đối

🎯 READY FOR PREMIUM AI VIDEO GENERATION!"""
        
        return prompt
    
    def _generate_english_compact_prompt(self, content: str, dna: UltraCompactDNA) -> str:
        """Generate English ultra-compact prompt"""
        
        prompt = f"""🎬 SCENE {dna.chunk_id}: {content}

🧬 VISUAL DNA FINGERPRINT [ID: {dna.dna_hash}]"""
        
        # Characters (highest priority)
        if dna.characters:
            prompt += f"\n\n👥 CHARACTERS:"
            for char_name, features in dna.characters.items():
                char_desc = []
                for feature_name, feature in features.items():
                    char_desc.append(feature.value)
                prompt += f"\n• {char_name}: {', '.join(char_desc)}"
        
        # Environment (second priority)
        if dna.environment:
            prompt += f"\n\n🌍 ENVIRONMENT:"
            for feature_name, feature in dna.environment.items():
                prompt += f"\n• {feature_name.title()}: {feature.value}"
        
        # Visual style (third priority)
        if dna.visual_style:
            prompt += f"\n\n🎨 VISUAL STYLE:"
            for feature_name, feature in dna.visual_style.items():
                prompt += f"\n• {feature_name.title()}: {feature.value}"
        
        # Emotional content (fourth priority)
        emotional_elements = []
        if dna.emotions:
            emotional_elements.extend([f.value for f in dna.emotions.values()])
        if dna.atmosphere:
            emotional_elements.extend([f.value for f in dna.atmosphere.values()])
        
        if emotional_elements:
            prompt += f"\n\n💫 EMOTIONAL TONE: {', '.join(emotional_elements)}"
        
        # Continuity link
        if dna.prev_link:
            prompt += f"\n\n🔗 CONTINUITY LINK: {dna.prev_link}"
        
        prompt += f"""

⚡ ULTRA-CRITICAL REQUIREMENTS:
- Maintain EXACT 100% accuracy of all Visual DNA features above
- Quality: 4K ultra-sharp, professional cinematic
- Duration: 8 seconds smooth, perfect continuity
- Style: Hyper-realistic, absolute sharp details

🎯 READY FOR PREMIUM AI VIDEO GENERATION!"""
        
        return prompt

# Test ultra-compact DNA engine
if __name__ == "__main__":
    engine = UltraCompactDNAEngine(source_language="vietnamese")
    
    # Test chunks for adjacency
    chunks = [
        "Anh MINH (40 tuổi, đàn ông Việt Nam, gầy, da ngăm) bước ra khỏi nhà tranh. Sáng sớm yên bình.",
        "Anh Minh đi trên đường đất nông thôn, vẫn nghiêm túc như trước.",
        "Anh gặp em LAN (25 tuổi, xinh đẹp) đang hái rau. Hai người cười vui vẻ.",
        "Họ trò chuyện thân thiện trong ánh nắng ấm áp."
    ]
    
    characters_list = [["Minh"], ["Minh"], ["Minh", "Lan"], ["Minh", "Lan"]]
    
    print("🧬 TESTING ULTRA-COMPACT DNA SYSTEM (ADJACENCY-BASED):")
    print("="*70)
    
    dna_chain = []
    for i, (chunk, chars) in enumerate(zip(chunks, characters_list)):
        previous_dna = dna_chain[-1] if dna_chain else None
        
        dna = engine.extract_ultra_compact_dna(chunk, i+1, chars, previous_dna)
        dna_chain.append(dna)
        
        print(f"\n🎬 CHUNK {i+1} - DNA: {dna.dna_hash}")
        print(f"   Characters: {len(dna.characters)} with {sum(len(f) for f in dna.characters.values())} features")
        print(f"   Environment: {len(dna.environment)} features")
        print(f"   Emotions: {len(dna.emotions)} features")
        print(f"   Previous link: {dna.prev_link}")
        
        if i == 1:  # Show prompt for chunk 2
            prompt = engine.generate_ultra_compact_prompt(chunk, dna)
            print(f"\n🎯 ULTRA-COMPACT PROMPT PREVIEW:")
            print("="*50)
            print(prompt[:300] + "...")
    
    print(f"\n📊 SYSTEM EFFICIENCY:")
    print(f"   Cache size: {len(engine.adjacency_cache)} chunks")
    print(f"   Memory footprint: Ultra-compact for 200+ chunks")
    print(f"   DNA inheritance: Adjacency-based (optimal)")
    
    print(f"\n✅ ULTRA-COMPACT DNA SYSTEM READY FOR PRODUCTION! 🚂🧬")
