"""
PRISM Video Intelligence Module
Advanced video chunking for seamless AI video generation
"""

from .scene_analyzer import SceneAnalyzer, VideoScene, SceneType
from .character_tracker import CharacterTracker, CharacterProfile, CharacterFeature
from .visual_context_builder import VisualContextBuilder, VisualReference, SceneVisualContext
from .video_chunking_orchestrator import VideoChunkingOrchestrator, VideoChunkingResult

__version__ = "1.0.0"
__author__ = "PRISM AI Platform"

# Main interface for easy usage
class VideoChunkingEngine:
    """Simplified interface for video chunking functionality"""
    
    def __init__(self, target_duration: float = 8.0):
        self.orchestrator = VideoChunkingOrchestrator(target_duration)
    
    def process_script(self, script: str, session_name: str = None):
        """Process movie script into AI-ready video chunks"""
        return self.orchestrator.process_script(script, session_name)
    
    def generate_production_guide(self, session_id: str):
        """Generate video production guide"""
        return self.orchestrator.generate_video_production_guide(session_id)
    
    def export_for_ai_platform(self, session_id: str, platform: str = "general"):
        """Export for specific AI video platform"""
        return self.orchestrator.export_for_ai_platforms(session_id, platform)

# Easy import for main functionality
__all__ = [
    'VideoChunkingEngine',
    'SceneAnalyzer', 
    'CharacterTracker',
    'VisualContextBuilder', 
    'VideoChunkingOrchestrator',
    'VideoScene',
    'CharacterProfile',
    'VisualReference',
    'VideoChunkingResult'
]
