"""
Video Scenario Creator
Biến text thành video scenarios với scenes, camera angles, và visual descriptions
"""

import time
import re
from typing import Dict, List, Any, Tuple
from .base_transformer import (
    BaseContentTransformer,
    TransformationType,
    TargetAudience, 
    ContentDifficulty,
    TransformationRequest,
    TransformationResponse
)


class VideoScenarioCreator(BaseContentTransformer):
    """
    Creator biến text thành video scenario với scenes và camera work
    """
    
    # Camera angles cho các loại content
    CAMERA_ANGLES = {
        "intro": ["Wide shot", "Medium shot", "Close-up"],
        "explanation": ["Medium shot", "Close-up", "Over-shoulder"],
        "demonstration": ["Wide shot", "Medium shot", "Detail shot"],
        "conclusion": ["Medium shot", "Wide shot", "Fade out"]
    }
    
    # Visual styles theo audience
    VISUAL_STYLES = {
        TargetAudience.CHILDREN: {
            "colors": "bright, colorful",
            "pace": "slow, playful",
            "graphics": "animated, cartoon-style",
            "music": "upbeat, cheerful"
        },
        TargetAudience.TEENAGERS: {
            "colors": "vibrant, trendy",
            "pace": "fast, dynamic",
            "graphics": "modern, sleek",
            "music": "energetic, contemporary"
        },
        TargetAudience.ADULTS: {
            "colors": "professional, balanced",
            "pace": "moderate, clear",
            "graphics": "clean, informative",
            "music": "background, subtle"
        },
        TargetAudience.PROFESSIONALS: {
            "colors": "corporate, sophisticated", 
            "pace": "steady, focused",
            "graphics": "data-driven, charts",
            "music": "minimal, professional"
        },
        TargetAudience.GENERAL: {
            "colors": "neutral, accessible",
            "pace": "moderate, engaging",
            "graphics": "simple, clear",
            "music": "universal appeal"
        }
    }
    
    # Scene transitions
    TRANSITIONS = [
        "Fade in",
        "Cut to",
        "Dissolve to", 
        "Zoom into",
        "Pan to",
        "Slide transition"
    ]
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config)
        
        self.default_config = {
            "include_camera_directions": True,
            "include_lighting_notes": True,
            "include_music_cues": True,
            "include_graphics_suggestions": True,
            "scene_duration_target": 30  # seconds per scene
        }
        self.config = {**self.default_config, **(config or {})}
    
    def _get_transformer_type(self) -> TransformationType:
        return TransformationType.VIDEO_SCENARIO
    
    async def transform(self, request: TransformationRequest) -> TransformationResponse:
        """Transform text thành video scenario"""
        start_time = time.time()
        
        if not self.validate_request(request):
            raise ValueError("Invalid transformation request")
        
        # Build video scenario
        scenario = await self._build_video_scenario(request)
        
        processing_time = time.time() - start_time
        
        # Calculate metadata
        scenes = self._count_scenes(scenario)
        estimated_duration = self.estimate_duration(scenario, request.target_audience)
        
        response = TransformationResponse(
            transformed_content=scenario,
            transformation_type=self.transformer_type,
            metadata={
                "scene_count": scenes,
                "total_shots": scenes * 3,  # Average 3 shots per scene
                "visual_style": self.VISUAL_STYLES.get(request.target_audience, {}).get("pace", "moderate"),
                "includes_camera_work": self.config.get("include_camera_directions", True),
                "includes_lighting": self.config.get("include_lighting_notes", True),
                "difficulty": request.difficulty_level.value,
                "language": request.language
            },
            processing_time=processing_time,
            quality_score=0.0,  # Sẽ calculate sau
            estimated_duration=estimated_duration
        )
        
        # Calculate quality score
        response.quality_score = self.calculate_quality_score(request, response)
        
        return response
    
    async def _build_video_scenario(self, request: TransformationRequest) -> str:
        """Build complete video scenario"""
        
        # 1. Analyze content và chia scenes
        scenes = self._analyze_and_create_scenes(request)
        
        # 2. Generate scenario header
        header = self._generate_scenario_header(request)
        
        # 3. Build từng scene với camera work
        scenario_parts = [header]
        
        for i, scene in enumerate(scenes, 1):
            scene_content = self._build_scene(scene, i, request)
            scenario_parts.append(scene_content)
        
        # 4. Add closing notes
        closing = self._generate_closing_notes(request)
        scenario_parts.append(closing)
        
        return "\n\n".join(scenario_parts)
    
    def _generate_scenario_header(self, request: TransformationRequest) -> str:
        """Generate scenario header với production notes"""
        style = self.VISUAL_STYLES.get(request.target_audience, self.VISUAL_STYLES[TargetAudience.GENERAL])
        
        header = f"""=== VIDEO SCENARIO ===
Target Audience: {request.target_audience.value.title()}
Difficulty Level: {request.difficulty_level.value.title()}
Visual Style: {style['colors']}, {style['pace']} pacing
Graphics Style: {style['graphics']}
Music Style: {style['music']}

PRODUCTION NOTES:
- Lighting: {self._get_lighting_recommendation(request.target_audience)}
- Color Palette: {style['colors']}
- Pacing: {style['pace']}"""
        
        return header
    
    def _get_lighting_recommendation(self, audience: TargetAudience) -> str:
        """Get lighting recommendation theo audience"""
        lighting_map = {
            TargetAudience.CHILDREN: "Bright, soft lighting, no harsh shadows",
            TargetAudience.TEENAGERS: "Dynamic lighting, some mood lighting",
            TargetAudience.ADULTS: "Professional, even lighting",
            TargetAudience.PROFESSIONALS: "Corporate lighting, well-lit, no distractions",
            TargetAudience.GENERAL: "Natural, balanced lighting"
        }
        return lighting_map.get(audience, lighting_map[TargetAudience.GENERAL])
    
    def _analyze_and_create_scenes(self, request: TransformationRequest) -> List[Dict[str, Any]]:
        """Analyze content và tạo scenes"""
        text = request.source_text
        
        # Split content thành logical chunks
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        
        scenes = []
        
        # Scene 1: Opening
        scenes.append({
            "type": "intro",
            "content": "Opening sequence",
            "purpose": "Introduce topic and engage audience"
        })
        
        # Main content scenes  
        for i, paragraph in enumerate(paragraphs):
            scene_type = self._determine_scene_type(paragraph, i, len(paragraphs))
            scenes.append({
                "type": scene_type,
                "content": paragraph,
                "purpose": self._get_scene_purpose(scene_type)
            })
        
        # Scene cuối: Closing
        scenes.append({
            "type": "conclusion",
            "content": "Closing sequence",
            "purpose": "Summarize and call-to-action"
        })
        
        return scenes
    
    def _determine_scene_type(self, content: str, index: int, total: int) -> str:
        """Determine scene type dựa trên content"""
        if index == 0:
            return "introduction"
        elif index == total - 1:
            return "conclusion"
        elif "?" in content:
            return "question"
        elif any(word in content.lower() for word in ["ví dụ", "chẳng hạn", "như"]):
            return "example"
        else:
            return "explanation"
    
    def _get_scene_purpose(self, scene_type: str) -> str:
        """Get purpose description cho scene type"""
        purposes = {
            "intro": "Capture attention and introduce topic",
            "introduction": "Set context and main points",
            "explanation": "Explain key concepts clearly",
            "example": "Demonstrate with concrete examples",
            "question": "Engage audience with questions",
            "conclusion": "Summarize and provide closure"
        }
        return purposes.get(scene_type, "Convey information effectively")
    
    def _build_scene(self, scene: Dict[str, Any], scene_number: int, request: TransformationRequest) -> str:
        """Build detailed scene với camera work"""
        
        scene_type = scene["type"]
        content = scene["content"]
        purpose = scene["purpose"]
        
        # Choose appropriate camera angles
        angles = self.CAMERA_ANGLES.get(scene_type, self.CAMERA_ANGLES["explanation"])
        
        # Build scene
        scene_parts = [
            f"=== SCENE {scene_number}: {scene_type.upper()} ===",
            f"Purpose: {purpose}",
            ""
        ]
        
        if scene_type == "intro":
            scene_content = self._build_intro_scene(request)
        elif scene_type == "conclusion":
            scene_content = self._build_conclusion_scene(request)
        else:
            scene_content = self._build_content_scene(content, angles, request)
        
        scene_parts.append(scene_content)
        
        return "\n".join(scene_parts)
    
    def _build_intro_scene(self, request: TransformationRequest) -> str:
        """Build intro scene"""
        style = self.VISUAL_STYLES.get(request.target_audience, self.VISUAL_STYLES[TargetAudience.GENERAL])
        
        return f"""SHOT 1: Wide shot (5 seconds)
- Visual: Title card với {style['graphics']} style
- Audio: {style['music']} intro music
- Text overlay: Topic title

SHOT 2: Medium shot (3 seconds) 
- Visual: Host/presenter introduction
- Camera: {self.CAMERA_ANGLES['intro'][1]}
- Lighting: {self._get_lighting_recommendation(request.target_audience)}

SHOT 3: Close-up (2 seconds)
- Visual: Engaging opening line
- Transition: {self.TRANSITIONS[0]} to main content"""
    
    def _build_content_scene(self, content: str, angles: List[str], request: TransformationRequest) -> str:
        """Build main content scene"""
        shots = []
        
        # Chia content thành shots
        sentences = [s.strip() + '.' for s in content.split('.') if s.strip()]
        
        for i, sentence in enumerate(sentences):
            shot_num = i + 1
            angle = angles[i % len(angles)]
            
            visual_desc = self._generate_visual_description(sentence, request.target_audience)
            
            shot = f"""SHOT {shot_num}: {angle} ({self._estimate_shot_duration(sentence)} seconds)
- Visual: {visual_desc}
- Audio: "{sentence}"
- Camera: {angle}"""
            
            if self.config.get("include_graphics_suggestions", True):
                graphics = self._suggest_graphics(sentence)
                if graphics:
                    shot += f"\n- Graphics: {graphics}"
            
            shots.append(shot)
        
        return "\n\n".join(shots)
    
    def _build_conclusion_scene(self, request: TransformationRequest) -> str:
        """Build conclusion scene"""
        return f"""SHOT 1: Medium shot (4 seconds)
- Visual: Summary of key points
- Audio: Recap main message
- Graphics: Key points overlay

SHOT 2: Wide shot (3 seconds)
- Visual: Call-to-action
- Camera: Pull back to show full context
- Transition: {self.TRANSITIONS[-1]}

SHOT 3: Fade out (3 seconds)
- Visual: End card với contact/follow info
- Audio: Outro music fade in"""
    
    def _generate_visual_description(self, content: str, audience: TargetAudience) -> str:
        """Generate visual description cho content"""
        style = self.VISUAL_STYLES.get(audience, self.VISUAL_STYLES[TargetAudience.GENERAL])
        
        if "AI" in content or "trí tuệ nhân tạo" in content.lower():
            return f"Technology graphics, {style['graphics']} style, showing AI concepts"
        elif "công nghệ" in content.lower():
            return f"Modern tech visuals, {style['colors']} color scheme"
        elif "làm việc" in content.lower():
            return f"Workplace scenes, professional environment"
        else:
            return f"Supporting visuals, {style['graphics']} style"
    
    def _suggest_graphics(self, content: str) -> str:
        """Suggest graphics cho content"""
        graphics_map = {
            "AI": "AI brain animation, neural network graphics",
            "công nghệ": "Tech icons, digital elements",
            "tự động": "Automation graphics, process flows",
            "quan trọng": "Highlighting effects, emphasis graphics"
        }
        
        for keyword, graphic in graphics_map.items():
            if keyword.lower() in content.lower():
                return graphic
        
        return ""
    
    def _estimate_shot_duration(self, text: str) -> int:
        """Estimate shot duration dựa trên text length"""
        word_count = len(text.split())
        # Average 2-3 words per second for comfortable viewing
        return max(2, min(8, word_count // 2))
    
    def _count_scenes(self, scenario: str) -> int:
        """Count number of scenes trong scenario"""
        return len(re.findall(r'=== SCENE \d+:', scenario))
    
    def _generate_closing_notes(self, request: TransformationRequest) -> str:
        """Generate closing production notes"""
        return f"""=== PRODUCTION NOTES ===
Total estimated duration: {self.estimate_duration("dummy", request.target_audience)} minutes
Post-production: Add graphics, music, color correction
Distribution: Optimize for {request.target_audience.value} audience
Quality check: Ensure {request.difficulty_level.value} level clarity"""
    
    def get_supported_audiences(self) -> List[TargetAudience]:
        """Video supports tất cả audiences"""
        return list(TargetAudience)
    
    def get_supported_difficulties(self) -> List[ContentDifficulty]:
        """Video supports tất cả difficulty levels"""
        return list(ContentDifficulty)
    
    def estimate_duration(self, text: str, target_audience: TargetAudience) -> int:
        """Estimate video duration in minutes"""
        # Base on content length và audience attention span
        if isinstance(text, str):
            word_count = len(text.split())
        else:
            word_count = 100  # Default estimate
        
        # Attention spans by audience
        attention_factors = {
            TargetAudience.CHILDREN: 0.5,      # Shorter videos
            TargetAudience.TEENAGERS: 0.7,     # Medium length
            TargetAudience.YOUNG_ADULTS: 1.0,  # Standard
            TargetAudience.ADULTS: 1.2,        # Can be longer
            TargetAudience.SENIORS: 0.8,       # Moderate length
            TargetAudience.PROFESSIONALS: 1.5, # Longer, detailed
            TargetAudience.GENERAL: 1.0        # Standard
        }
        
        factor = attention_factors.get(target_audience, 1.0)
        base_duration = max(1, word_count // 50)  # 50 words per minute of video
        
        return max(1, round(base_duration * factor))
