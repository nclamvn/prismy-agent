"""
Video DNA Creator - PRISM Video DNA Integration
SUPERIOR TO SORA - Perfect visual continuity for AI video generation
"""

import sys
import os

# Add proper path for video intelligence
current_dir = os.path.dirname(__file__)
video_intelligence_path = os.path.join(current_dir, '..', 'video_intelligence')
sys.path.append(video_intelligence_path)
sys.path.append(os.path.join(current_dir, '..', '..'))

from typing import List, Dict, Any, Optional
import json
import time
from datetime import datetime

# Import PRISM Video DNA Engine
try:
    from prism_video_dna_production import PrismVideoDNAProduction
    PRISM_AVAILABLE = True
    print("✅ PRISM Video DNA Engine imported successfully")
except ImportError as e:
    PRISM_AVAILABLE = False
    print(f"⚠️ PRISM Video DNA not available: {e}")

class VideoDNACreator:
    """
    Video DNA Creator with PRISM integration for AI Commander
    
    Features:
    - Ultra-Compact DNA System for perfect visual continuity
    - Advanced Character Intelligence (95%+ accuracy)  
    - Enhanced Scene Analysis with cinematic intelligence
    - Multi-platform export (Runway ML, Pika Labs, Stable Video)
    - Production-ready AI prompts
    """
    
    def __init__(self, target_duration: float = 8.0):
        self.target_duration = target_duration
        self.prism_engine = None
        self.session_id = f"VIDEO_DNA_{int(time.time())}"
        
        if PRISM_AVAILABLE:
            try:
                self.prism_engine = PrismVideoDNAProduction(target_duration=target_duration)
                print("🧬 PRISM Video DNA Engine initialized - SUPERIOR TO SORA")
            except Exception as e:
                print(f"⚠️ PRISM initialization error: {e}")
    
    def create_video_with_dna(
        self, 
        script: str, 
        session_name: Optional[str] = None,
        export_platform: str = "all"
    ) -> Dict[str, Any]:
        """
        Create video scenario with DNA fingerprinting for perfect continuity
        """
        
        start_time = time.time()
        
        if not self.prism_engine:
            return self._fallback_response(script)
        
        try:
            # Process script with PRISM Video DNA Engine
            result = self.prism_engine.process_script_production(
                script=script,
                session_name=session_name or self.session_id
            )
            
            if not result.success:
                return self._error_response(result.error_message)
            
            # Enhanced response for AI Commander
            response = {
                "success": True,
                "session_id": result.session_id,
                "processing_time": result.processing_time,
                
                # Video metadata
                "video_data": {
                    "total_chunks": result.total_chunks,
                    "total_duration": result.total_duration,
                    "characters": result.characters,
                    "language": result.detected_language
                },
                
                # Quality metrics  
                "quality": {
                    "character_accuracy": result.character_accuracy,
                    "scene_intelligence": result.scene_intelligence,
                    "visual_continuity": result.visual_continuity,
                    "overall_score": result.overall_quality,
                    "grade": self._get_grade(result.overall_quality)
                },
                
                # DNA chain and chunks
                "chunks": result.chunks,
                "dna_chain": result.dna_chain,
                
                # Export formats
                "exports": result.export_formats,
                
                # Production info
                "prism_info": {
                    "engine": "PRISM Video DNA 2.0.0",
                    "superiority": "SUPERIOR TO SORA AND ALL EXISTING AI VIDEO TOOLS",
                    "processing_speed": f"{getattr(result, 'processing_speed', 0):.1f} chunks/sec",
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            return response
            
        except Exception as e:
            return self._error_response(f"Video DNA processing failed: {str(e)}")
    
    def _get_grade(self, score: float) -> str:
        """Convert score to letter grade"""
        if score >= 0.9: return "A+"
        elif score >= 0.8: return "A" 
        elif score >= 0.7: return "B+"
        elif score >= 0.6: return "B"
        else: return "C"
    
    def _fallback_response(self, script: str) -> Dict[str, Any]:
        """Fallback when PRISM not available"""
        return {
            "success": False,
            "error": "PRISM Video DNA Engine not available",
            "fallback": True,
            "script_length": len(script),
            "recommendation": "Install PRISM Video DNA for superior results"
        }
    
    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Error response"""
        return {
            "success": False,
            "error": error_msg,
            "session_id": self.session_id,
            "timestamp": datetime.now().isoformat()
        }

# Quick access function
def create_video_dna(script: str, duration: float = 8.0) -> Dict[str, Any]:
    """Quick function to create video with DNA"""
    creator = VideoDNACreator(target_duration=duration)
    return creator.create_video_with_dna(script)

if __name__ == "__main__":
    # Test the video DNA creator
    test_script = """
    FADE IN:
    
    EXT. TECH STARTUP OFFICE - DAY
    
    ALEX (30, Vietnamese entrepreneur) codes at his desk.
    
    ALEX
    Today we launch the future.
    
    SARAH (28, AI engineer) shows him a hologram.
    
    SARAH  
    The AI is ready.
    
    FADE OUT.
    """
    
    print("🎬 Testing Video DNA Creator...")
    result = create_video_dna(test_script)
    
    if result["success"]:
        print("✅ Video DNA creation successful!")
        print(f"📊 Quality: {result['quality']['grade']}")
        print(f"🎯 Chunks: {result['video_data']['total_chunks']}")
    else:
        print(f"❌ Error: {result.get('error')}")
