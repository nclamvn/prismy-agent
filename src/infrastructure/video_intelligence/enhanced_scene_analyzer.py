"""
PRISM Enhanced Scene Analyzer
Ultra-sophisticated scene detection with cinematic intelligence
"""

import re
import json
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import time

class SceneType(Enum):
    DIALOGUE = "dialogue"
    ACTION = "action"
    TRANSITION = "transition"
    ESTABLISHING = "establishing"
    CLOSE_UP = "close_up"
    WIDE_SHOT = "wide_shot"
    MONTAGE = "montage"

class CinematicElement(Enum):
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    CUT_TO = "cut_to"
    DISSOLVE = "dissolve"
    MATCH_CUT = "match_cut"
    CLOSE_UP = "close_up"
    WIDE_SHOT = "wide_shot"
    MEDIUM_SHOT = "medium_shot"

@dataclass
class EnhancedVideoScene:
    """Enhanced video scene with cinematic intelligence"""
    id: int
    content: str
    scene_type: SceneType
    duration: float
    characters: List[str] = field(default_factory=list)
    setting: str = ""
    actions: List[str] = field(default_factory=list)
    dialogue: Optional[str] = None
    
    # Enhanced cinematic features
    cinematic_elements: List[CinematicElement] = field(default_factory=list)
    camera_angles: List[str] = field(default_factory=list)
    emotional_tone: str = ""
    pacing: str = "moderate"  # slow, moderate, fast, varied
    visual_complexity: float = 0.5  # 0.0-1.0
    
    # Technical specifications
    recommended_shots: List[str] = field(default_factory=list)
    lighting_requirements: str = ""
    sound_design: str = ""
    
    # Continuity markers
    continuity_markers: Dict[str, str] = field(default_factory=dict)

class EnhancedSceneAnalyzer:
    """
    Ultra-sophisticated scene analysis with cinematic intelligence
    Professional film industry standards
    """
    
    def __init__(self, target_duration: float = 8.0, language: str = "auto"):
        self.target_duration = target_duration
        self.min_duration = 4.0
        self.max_duration = 15.0
        self.language = language
        
        # Cinematic intelligence patterns
        self.cinematic_patterns = self._build_cinematic_patterns()
        self.pacing_indicators = self._build_pacing_indicators()
        self.emotional_indicators = self._build_emotional_indicators()
        
    def _build_cinematic_patterns(self) -> Dict[str, Dict[str, List[str]]]:
        """Build comprehensive cinematic pattern recognition"""
        return {
            "vietnamese": {
                "scene_transitions": [
                    r'(?i)(fade\s+in|fade\s+out|cut\s+to|dissolve|chuyển\s+cảnh)',
                    r'(?i)(cắt\s+đến|chuyển\s+sang|fade|cut)',
                    r'(?i)(sau\s+đó|tiếp\s+theo|lúc\s+này|đồng\s+thời)',
                    r'(?i)(ext\.|int\.|ngoại\s+cảnh|nội\s+cảnh)'
                ],
                "camera_directions": [
                    r'(?i)(close\s+up|wide\s+shot|medium\s+shot)',
                    r'(?i)(cận\s+cảnh|toàn\s+cảnh|góc\s+rộng|góc\s+hẹp)',
                    r'(?i)(camera\s+.*?|máy\s+quay|góc\s+quay)',
                    r'(?i)(từ\s+trên\s+xuống|từ\s+dưới\s+lên|ngang\s+mắt)'
                ],
                "dialogue_markers": [
                    r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][A-Za-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\s*\n.*?"([^"]*)"',
                    r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][A-Za-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\s*:',
                    r'(nói|hỏi|thì\s+thầm|la\s+lên|thốt\s+lên)'
                ],
                "action_sequences": [
                    r'(chạy|nhảy|đánh|bắn|lái\s+xe|bay|rơi|ngã)',
                    r'(nhanh\s+chóng|từ\s+từ|đột\s+ngột|bỗng\s+nhiên)',
                    r'(cùng\s+lúc|đồng\s+thời|trong\s+khi|liền\s+sau)'
                ]
            },
            "english": {
                "scene_transitions": [
                    r'(?i)(fade\s+in|fade\s+out|cut\s+to|dissolve|transition)',
                    r'(?i)(ext\.|int\.|exterior|interior)',
                    r'(?i)(meanwhile|later|then|next|suddenly)'
                ],
                "camera_directions": [
                    r'(?i)(close\s+up|wide\s+shot|medium\s+shot|extreme)',
                    r'(?i)(camera\s+.*?|angle|pov|point\s+of\s+view)',
                    r'(?i)(overhead|low\s+angle|high\s+angle|eye\s+level)'
                ],
                "dialogue_markers": [
                    r'([A-Z][A-Za-z]+)\s*\n.*?"([^"]*)"',
                    r'([A-Z][A-Za-z]+)\s*:',
                    r'(says|asks|whispers|shouts|exclaims)'
                ],
                "action_sequences": [
                    r'(runs|jumps|fights|shoots|drives|flies|falls)',
                    r'(quickly|slowly|suddenly|gradually)',
                    r'(simultaneously|meanwhile|during|while)'
                ]
            }
        }
    
    def _build_pacing_indicators(self) -> Dict[str, List[str]]:
        """Build pacing detection patterns"""
        return {
            "fast": [
                r'(nhanh|rapid|quick|fast|sudden|immediate)',
                r'(chạy|nhảy|đánh|bắn|run|jump|fight|chase)',
                r'(cấp\s+tốc|gấp\s+rút|vội\s+vã|urgent|rush)'
            ],
            "slow": [
                r'(chậm|slow|gradual|gentle|peaceful)',
                r'(từ\s+từ|nhẹ\s+nhàng|slowly|gently)',
                r'(yên\s+bình|tĩnh\s+lặng|calm|quiet|serene)'
            ],
            "varied": [
                r'(thay\s+đổi|biến\s+thiên|varies|changes)',
                r'(từ.*?đến|from.*?to)',
                r'(lúc.*?lúc|sometimes.*?sometimes)'
            ]
        }
    
    def _build_emotional_indicators(self) -> Dict[str, List[str]]:
        """Build emotional tone detection"""
        return {
            "joyful": [r'(vui|cười|hạnh\s+phúc|happy|joy|laugh|smile)'],
            "sad": [r'(buồn|khóc|đau\s+khổ|sad|cry|sorrow|grief)'],
            "tense": [r'(căng\s+thẳng|lo\s+lắng|tense|anxious|worried)'],
            "romantic": [r'(lãng\s+mạn|yêu|tình\s+cảm|romantic|love|tender)'],
            "mysterious": [r'(bí\s+ẩn|kỳ\s+lạ|mysterious|strange|eerie)'],
            "action": [r'(hành\s+động|phiêu\s+lưu|action|adventure|thrill)']
        }
    
    def analyze_script_enhanced(self, script: str) -> List[EnhancedVideoScene]:
        """
        Enhanced script analysis with cinematic intelligence
        """
        
        print("🎬 Enhanced Scene Analysis Starting...")
        start_time = time.time()
        
        # Detect language
        language = self._detect_language_advanced(script)
        patterns = self.cinematic_patterns.get(language, self.cinematic_patterns["english"])
        
        # Step 1: Intelligent scene segmentation
        raw_segments = self._intelligent_scene_segmentation(script, patterns)
        print(f"   📋 Initial segmentation: {len(raw_segments)} segments")
        
        # Step 2: Cinematic analysis
        analyzed_segments = []
        for i, segment in enumerate(raw_segments):
            analyzed_segment = self._analyze_segment_cinematics(segment, i + 1, patterns, language)
            analyzed_segments.append(analyzed_segment)
        
        # Step 3: Duration optimization
        optimized_scenes = self._optimize_scene_durations(analyzed_segments)
        print(f"   ⏱️  Duration optimization: {len(optimized_scenes)} final scenes")
        
        # Step 4: Continuity analysis
        continuity_enhanced_scenes = self._analyze_continuity(optimized_scenes)
        
        processing_time = time.time() - start_time
        print(f"   ✅ Enhanced analysis complete: {processing_time:.2f}s")
        
        return continuity_enhanced_scenes
    
    def _detect_language_advanced(self, script: str) -> str:
        """Advanced language detection with multiple indicators"""
        
        # Character-based detection
        vietnamese_chars = len(re.findall(r'[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', script.lower()))
        total_chars = len(re.findall(r'[a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]', script.lower()))
        
        # Word-based detection
        vietnamese_keywords = len(re.findall(r'\b(?:anh|em|chị|tuổi|sáng|chiều|tối|nhà|đường|nói|hỏi)\b', script.lower()))
        english_keywords = len(re.findall(r'\b(?:the|and|is|are|said|asked|house|street|morning|evening)\b', script.lower()))
        
        # Structure-based detection
        vietnamese_titles = len(re.findall(r'\b(?:anh|em|chị|ông|bà)\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ]', script))
        
        # Scoring
        vietnamese_score = 0
        english_score = 0
        
        if total_chars > 0:
            vietnamese_score += (vietnamese_chars / total_chars) * 40
        
        vietnamese_score += vietnamese_keywords * 5
        vietnamese_score += vietnamese_titles * 3
        english_score += english_keywords * 3
        
        return "vietnamese" if vietnamese_score > english_score else "english"
    
    def _intelligent_scene_segmentation(self, script: str, patterns: Dict) -> List[str]:
        """Intelligent scene segmentation using multiple criteria"""
        
        # Find all potential break points
        break_points = [0]
        
        # Cinematic transitions (highest priority)
        for pattern in patterns["scene_transitions"]:
            matches = list(re.finditer(pattern, script, re.MULTILINE | re.IGNORECASE))
            for match in matches:
                break_points.append(match.start())
        
        # Dialogue changes (medium priority)
        dialogue_pattern = r'^([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][A-Za-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\s*$'
        matches = list(re.finditer(dialogue_pattern, script, re.MULTILINE))
        for match in matches:
            break_points.append(match.start())
        
        # Natural breaks (paragraph breaks, etc.)
        paragraph_breaks = [m.start() for m in re.finditer(r'\n\s*\n', script)]
        break_points.extend(paragraph_breaks)
        
        # Sort and deduplicate
        break_points = sorted(list(set(break_points)))
        break_points.append(len(script))
        
        # Extract segments
        segments = []
        for i in range(len(break_points) - 1):
            start = break_points[i]
            end = break_points[i + 1]
            segment = script[start:end].strip()
            if segment and len(segment) > 10:  # Minimum segment length
                segments.append(segment)
        
        return segments
    
    def _analyze_segment_cinematics(self, segment: str, segment_id: int, 
                                  patterns: Dict, language: str) -> EnhancedVideoScene:
        """Analyze cinematic elements of a segment"""
        
        # Basic analysis
        scene_type = self._classify_scene_type_advanced(segment, patterns)
        duration = self._estimate_duration_advanced(segment, scene_type)
        
        # Extract cinematic elements
        cinematic_elements = self._extract_cinematic_elements(segment, patterns)
        camera_angles = self._extract_camera_directions(segment, patterns)
        
        # Analyze emotional tone
        emotional_tone = self._analyze_emotional_tone(segment)
        
        # Determine pacing
        pacing = self._analyze_pacing(segment)
        
        # Calculate visual complexity
        visual_complexity = self._calculate_visual_complexity(segment)
        
        # Extract dialogue and actions
        dialogue = self._extract_dialogue_advanced(segment)
        actions = self._extract_actions_advanced(segment)
        
        # Generate recommendations
        recommended_shots = self._generate_shot_recommendations(segment, scene_type)
        lighting_requirements = self._analyze_lighting_requirements(segment)
        sound_design = self._analyze_sound_requirements(segment)
        
        return EnhancedVideoScene(
            id=segment_id,
            content=segment,
            scene_type=scene_type,
            duration=duration,
            cinematic_elements=cinematic_elements,
            camera_angles=camera_angles,
            emotional_tone=emotional_tone,
            pacing=pacing,
            visual_complexity=visual_complexity,
            dialogue=dialogue,
            actions=actions,
            recommended_shots=recommended_shots,
            lighting_requirements=lighting_requirements,
            sound_design=sound_design
        )
    
    def _classify_scene_type_advanced(self, segment: str, patterns: Dict) -> SceneType:
        """Advanced scene type classification"""
        
        # Check for dialogue
        dialogue_indicators = 0
        for pattern in patterns["dialogue_markers"]:
            if re.search(pattern, segment, re.IGNORECASE):
                dialogue_indicators += 1
        
        # Check for action
        action_indicators = 0
        for pattern in patterns["action_sequences"]:
            if re.search(pattern, segment, re.IGNORECASE):
                action_indicators += 1
        
        # Check for transitions
        transition_indicators = 0
        for pattern in patterns["scene_transitions"]:
            if re.search(pattern, segment, re.IGNORECASE):
                transition_indicators += 1
        
        # Check for camera directions
        camera_indicators = 0
        for pattern in patterns["camera_directions"]:
            if re.search(pattern, segment, re.IGNORECASE):
                camera_indicators += 1
        
        # Classification logic
        if transition_indicators > 0:
            return SceneType.TRANSITION
        elif dialogue_indicators >= 2:
            return SceneType.DIALOGUE
        elif action_indicators >= 2:
            return SceneType.ACTION
        elif camera_indicators > 0:
            if re.search(r'(?i)(close\s+up|cận\s+cảnh)', segment):
                return SceneType.CLOSE_UP
            elif re.search(r'(?i)(wide\s+shot|toàn\s+cảnh)', segment):
                return SceneType.WIDE_SHOT
        else:
            return SceneType.ESTABLISHING
    
    def _estimate_duration_advanced(self, segment: str, scene_type: SceneType) -> float:
        """Advanced duration estimation based on content analysis"""
        
        # Base duration calculation
        word_count = len(segment.split())
        
        # Adjust for scene type
        if scene_type == SceneType.DIALOGUE:
            base_wps = 2.0  # words per second for dialogue
        elif scene_type == SceneType.ACTION:
            base_wps = 3.5  # faster for action
        elif scene_type == SceneType.TRANSITION:
            base_wps = 4.0  # very fast for transitions
        else:
            base_wps = 2.5  # standard
        
        # Adjust for content complexity
        complexity_factors = {
            "character_count": len(re.findall(r'[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+', segment)) * 0.5,
            "dialogue_count": len(re.findall(r'"[^"]*"', segment)) * 1.0,
            "action_count": len(re.findall(r'(chạy|nhảy|đánh|run|jump|fight)', segment, re.IGNORECASE)) * 0.3
        }
        
        complexity_adjustment = sum(complexity_factors.values()) / 10.0
        adjusted_wps = base_wps - complexity_adjustment
        
        estimated_duration = word_count / max(1.0, adjusted_wps)
        
        # Clamp to reasonable bounds
        return max(self.min_duration, min(self.max_duration, estimated_duration))
    
    def _extract_cinematic_elements(self, segment: str, patterns: Dict) -> List[CinematicElement]:
        """Extract cinematic elements from segment"""
        elements = []
        
        cinematic_mapping = {
            r'(?i)fade\s+in': CinematicElement.FADE_IN,
            r'(?i)fade\s+out': CinematicElement.FADE_OUT,
            r'(?i)cut\s+to': CinematicElement.CUT_TO,
            r'(?i)dissolve': CinematicElement.DISSOLVE,
            r'(?i)close\s+up': CinematicElement.CLOSE_UP,
            r'(?i)wide\s+shot': CinematicElement.WIDE_SHOT,
            r'(?i)medium\s+shot': CinematicElement.MEDIUM_SHOT
        }
        
        for pattern, element in cinematic_mapping.items():
            if re.search(pattern, segment):
                elements.append(element)
        
        return elements
    
    def _extract_camera_directions(self, segment: str, patterns: Dict) -> List[str]:
        """Extract camera direction information"""
        directions = []
        
        for pattern in patterns["camera_directions"]:
            matches = re.findall(pattern, segment, re.IGNORECASE)
            directions.extend(matches)
        
        return list(set(directions))
    
    def _analyze_emotional_tone(self, segment: str) -> str:
        """Analyze emotional tone of segment"""
        emotion_scores = {}
        
        for emotion, patterns in self.emotional_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, segment, re.IGNORECASE))
                score += matches
            emotion_scores[emotion] = score
        
        if not emotion_scores or max(emotion_scores.values()) == 0:
            return "neutral"
        
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def _analyze_pacing(self, segment: str) -> str:
        """Analyze pacing of segment"""
        pacing_scores = {}
        
        for pacing_type, patterns in self.pacing_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, segment, re.IGNORECASE))
                score += matches
            pacing_scores[pacing_type] = score
        
        if not pacing_scores or max(pacing_scores.values()) == 0:
            return "moderate"
        
        return max(pacing_scores.items(), key=lambda x: x[1])[0]
    
    def _calculate_visual_complexity(self, segment: str) -> float:
        """Calculate visual complexity score"""
        complexity_factors = {
            "character_count": len(re.findall(r'[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+', segment)) / 10.0,
            "action_density": len(re.findall(r'(chạy|nhảy|đánh|bắn|run|jump|fight|shoot)', segment, re.IGNORECASE)) / 5.0,
            "location_changes": len(re.findall(r'(cut\s+to|chuyển|fade)', segment, re.IGNORECASE)) / 3.0,
            "dialogue_complexity": len(re.findall(r'"[^"]{20,}"', segment)) / 5.0
        }
        
        total_complexity = sum(complexity_factors.values())
        return min(1.0, total_complexity)
    
    def _extract_dialogue_advanced(self, segment: str) -> Optional[str]:
        """Advanced dialogue extraction"""
        dialogue_patterns = [
            r'"([^"]+)"',
            r'"([^"]+)"',
            r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zA-Zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\s*:\s*([^.\n]+)'
        ]
        
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, segment, re.IGNORECASE)
            if matches:
                return matches[0] if isinstance(matches[0], str) else matches[0][1]
        
        return None
    
    def _extract_actions_advanced(self, segment: str) -> List[str]:
        """Advanced action extraction"""
        action_patterns = [
            r'(bước\s+ra|đi\s+bộ|chạy\s+nhanh|nhảy\s+lên)',
            r'(nhìn|nghe|cười|khóc|nói|hỏi)',
            r'(walks|runs|jumps|looks|listens|smiles|cries|says|asks)'
        ]
        
        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, segment, re.IGNORECASE)
            actions.extend(matches)
        
        return list(set(actions))
    
    def _generate_shot_recommendations(self, segment: str, scene_type: SceneType) -> List[str]:
        """Generate cinematography recommendations"""
        recommendations = []
        
        # Base recommendations by scene type
        if scene_type == SceneType.DIALOGUE:
            recommendations.extend(["Medium shot", "Over-shoulder shots", "Close-up for emotions"])
        elif scene_type == SceneType.ACTION:
            recommendations.extend(["Wide shot for context", "Dynamic camera movement", "Quick cuts"])
        elif scene_type == SceneType.ESTABLISHING:
            recommendations.extend(["Wide establishing shot", "Slow camera movement", "Environmental details"])
        
        # Context-specific recommendations
        if re.search(r'(cận\s+cảnh|close\s+up)', segment, re.IGNORECASE):
            recommendations.append("Extreme close-up")
        
        if re.search(r'(chạy|nhảy|run|jump)', segment, re.IGNORECASE):
            recommendations.append("Tracking shot")
        
        return recommendations
    
    def _analyze_lighting_requirements(self, segment: str) -> str:
        """Analyze lighting requirements"""
        lighting_indicators = {
            "natural": r'(ánh\s+nắng|sunlight|daylight|sáng\s+sớm|morning)',
            "dramatic": r'(bóng\s+tối|shadow|dramatic|căng\s+thẳng|tense)',
            "soft": r'(dịu\s+nhẹ|soft|gentle|ấm\s+áp|warm)',
            "bright": r'(sáng\s+rực|bright|brilliant|rực\s+rỡ)',
            "dim": r'(mờ\s+ảo|dim|low\s+light|tối)'
        }
        
        for lighting_type, pattern in lighting_indicators.items():
            if re.search(pattern, segment, re.IGNORECASE):
                return lighting_type
        
        return "natural"
    
    def _analyze_sound_requirements(self, segment: str) -> str:
        """Analyze sound design requirements"""
        sound_indicators = {
            "ambient": r'(yên\s+tĩnh|quiet|peaceful|ambient)',
            "dynamic": r'(ồn\s+ào|loud|dynamic|action)',
            "dialogue": r'(nói\s+chuyện|conversation|dialogue|talk)',
            "music": r'(nhạc|music|melody|rhythm)',
            "effects": r'(tiếng|sound\s+of|noise|effect)'
        }
        
        for sound_type, pattern in sound_indicators.items():
            if re.search(pattern, segment, re.IGNORECASE):
                return sound_type
        
        return "ambient"
    
    def _optimize_scene_durations(self, scenes: List[EnhancedVideoScene]) -> List[EnhancedVideoScene]:
        """Optimize scene durations for target length"""
        optimized_scenes = []
        
        for scene in scenes:
            # Adjust duration based on target
            if scene.duration > self.max_duration:
                # Split long scenes
                optimized_scenes.extend(self._split_long_scene(scene))
            elif scene.duration < self.min_duration:
                # Mark for potential merging
                scene.continuity_markers["merge_candidate"] = "true"
                optimized_scenes.append(scene)
            else:
                optimized_scenes.append(scene)
        
        # Merge short adjacent scenes if possible
        return self._merge_short_scenes(optimized_scenes)
    
    def _split_long_scene(self, scene: EnhancedVideoScene) -> List[EnhancedVideoScene]:
        """Split long scene into optimal chunks"""
        # Split by natural breaks
        sentences = re.split(r'[.!?]', scene.content)
        
        chunks = []
        current_chunk = ""
        current_duration = 0
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            sentence_duration = len(sentence.split()) / 2.5
            
            if current_duration + sentence_duration <= self.target_duration:
                current_chunk += sentence + ". "
                current_duration += sentence_duration
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + ". "
                current_duration = sentence_duration
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Create new scenes from chunks
        split_scenes = []
        for i, chunk in enumerate(chunks):
            new_scene = EnhancedVideoScene(
                id=scene.id + i * 0.1,  # Sub-scene numbering
                content=chunk,
                scene_type=scene.scene_type,
                duration=len(chunk.split()) / 2.5,
                cinematic_elements=scene.cinematic_elements,
                emotional_tone=scene.emotional_tone,
                pacing=scene.pacing
            )
            split_scenes.append(new_scene)
        
        return split_scenes
    
    def _merge_short_scenes(self, scenes: List[EnhancedVideoScene]) -> List[EnhancedVideoScene]:
        """Merge short adjacent scenes"""
        if not scenes:
            return scenes
        
        merged = []
        current_scene = scenes[0]
        
        for i in range(1, len(scenes)):
            next_scene = scenes[i]
            
            # Check if both scenes are merge candidates and compatible
            if (current_scene.continuity_markers.get("merge_candidate") == "true" and
                next_scene.continuity_markers.get("merge_candidate") == "true" and
                current_scene.scene_type == next_scene.scene_type and
                current_scene.duration + next_scene.duration <= self.max_duration):
                
                # Merge scenes
                merged_content = current_scene.content + " " + next_scene.content
                merged_duration = current_scene.duration + next_scene.duration
                
                current_scene.content = merged_content
                current_scene.duration = merged_duration
                current_scene.continuity_markers.pop("merge_candidate", None)
            else:
                merged.append(current_scene)
                current_scene = next_scene
        
        merged.append(current_scene)
        return merged
    
    def _analyze_continuity(self, scenes: List[EnhancedVideoScene]) -> List[EnhancedVideoScene]:
        """Analyze and mark continuity requirements"""
        
        for i, scene in enumerate(scenes):
            # Mark character continuity
            if i > 0:
                prev_scene = scenes[i-1]
                # Check for character overlap
                # This will be enhanced with character tracking
                scene.continuity_markers["previous_scene"] = str(prev_scene.id)
                
            # Mark setting continuity
            # This will be enhanced with setting analysis
            
            # Mark temporal continuity
            # This will be enhanced with temporal analysis
        
        return scenes

# Test enhanced scene analyzer
if __name__ == "__main__":
    analyzer = EnhancedSceneAnalyzer(target_duration=8.0, language="vietnamese")
    
    test_script = """
    FADE IN:
    
    EXT. NHÀ VIỆT NAM - SÁNG SỚM
    
    Wide shot: Anh MINH (40 tuổi, đàn ông Việt Nam, dáng gầy, da ngăm đen, mặt khắc khổ) 
    bước ra khỏi nhà tranh nhỏ. Ánh nắng sáng sớm chiếu rọi lên khuôn mặt nghiêm túc của anh.
    
    CUT TO:
    
    EXT. CON ĐƯỜNG ĐẤT - CONTINUOUS
    
    Medium shot: Anh Minh đi bộ nhanh chóng trên con đường đất giữa cánh đồng lúa xanh.
    
    Close up: Anh dừng lại khi thấy em LAN (25 tuổi, xinh đẹp, mặc áo bà ba trắng) đang hái rau.
    
    MINH
    (vui vẻ)
    Chào em Lan! Sáng nay em dậy sớm quá!
    
    LAN
    (cười tươi)
    Chào anh Minh! Em phải hái rau sớm để mang ra chợ bán.
    
    FADE OUT.
    """
    
    print("🎬 TESTING ENHANCED SCENE ANALYZER:")
    print("="*60)
    
    scenes = analyzer.analyze_script_enhanced(test_script)
    
    print(f"\n📊 ENHANCED ANALYSIS RESULTS:")
    print(f"   🎬 Total Scenes: {len(scenes)}")
    
    for i, scene in enumerate(scenes[:3]):  # Show first 3 scenes
        print(f"\n🎯 Scene {scene.id}:")
        print(f"   Type: {scene.scene_type.value}")
        print(f"   Duration: {scene.duration:.1f}s")
        print(f"   Emotional Tone: {scene.emotional_tone}")
        print(f"   Pacing: {scene.pacing}")
        print(f"   Visual Complexity: {scene.visual_complexity:.2f}")
        print(f"   Cinematic Elements: {[e.value for e in scene.cinematic_elements]}")
        print(f"   Camera Angles: {scene.camera_angles}")
        print(f"   Recommended Shots: {scene.recommended_shots}")
        print(f"   Lighting: {scene.lighting_requirements}")
        print(f"   Sound: {scene.sound_design}")
        print(f"   Content: {scene.content[:100]}...")
    
    print(f"\n✅ ENHANCED SCENE ANALYZER READY! 🎬🎯")
