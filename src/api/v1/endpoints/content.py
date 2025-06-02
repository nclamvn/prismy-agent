"""
Content transformation endpoints
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, Literal
from src.infrastructure.content_transformation.transformation_manager import TransformationManager
from src.infrastructure.content_transformation.base_transformer import (
    TransformationRequest, TargetAudience, ContentDifficulty
)
from src.config.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter()

# Initialize manager
transformation_manager = TransformationManager()

class TransformRequest(BaseModel):
    """Content transformation request"""
    content: str = Field(..., min_length=1, max_length=100000)
    transformation_type: Literal["podcast", "education", "video"]
    target_audience: Literal["children", "teenagers", "adults", "professionals"]
    difficulty: Optional[Literal["beginner", "intermediate", "advanced"]] = "intermediate"
    output_format: Optional[str] = None

@router.post("/transform")
async def transform_content(request: TransformRequest):
    """Transform content to different formats"""
    try:
        # Map string values to enums
        audience_map = {
            "children": TargetAudience.CHILDREN,
            "teenagers": TargetAudience.TEENAGERS,
            "adults": TargetAudience.ADULTS,
            "professionals": TargetAudience.PROFESSIONALS
        }
        
        difficulty_map = {
            "beginner": ContentDifficulty.BEGINNER,
            "intermediate": ContentDifficulty.INTERMEDIATE,
            "advanced": ContentDifficulty.ADVANCED
        }
        
        # Create transformation request
        trans_request = TransformationRequest(
            source_text=request.content,
            transformation_type=request.transformation_type,
            target_audience=audience_map[request.target_audience],
            difficulty_level=difficulty_map[request.difficulty]
        )
        
        # Transform
        result = await transformation_manager.transform_content(trans_request)
        
        return {
            "success": result.success,
            "transformed_content": result.transformed_content,
            "metadata": result.metadata,
            "quality_score": result.quality_score,
            "processing_time": result.processing_time
        }
        
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types")
async def get_transformation_types():
    """Get available transformation types"""
    return {
        "types": [
            {
                "id": "podcast",
                "name": "Podcast Script",
                "description": "Convert content to engaging podcast script"
            },
            {
                "id": "education",
                "name": "Education Module",
                "description": "Create structured learning materials"
            },
            {
                "id": "video",
                "name": "Video Script",
                "description": "Generate video screenplay or AI prompts"
            }
        ]
    }
