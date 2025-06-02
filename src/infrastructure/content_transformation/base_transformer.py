"""
Base Content Transformer
Abstract interface cho tất cả content transformers
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time


class TransformationType(Enum):
    """Các loại content transformation"""
    PODCAST_SCRIPT = "podcast_script"
    VIDEO_SCENARIO = "video_scenario"
    EDUCATION_MODULE = "education_module"
    SOCIAL_MEDIA = "social_media"
    PRESENTATION = "presentation"
    SUMMARY = "summary"


class ContentDifficulty(Enum):
    """Mức độ khó của content"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TargetAudience(Enum):
    """Đối tượng mục tiêu"""
    CHILDREN = "children"           # Trẻ em (6-12)
    TEENAGERS = "teenagers"         # Thiếu niên (13-17)
    YOUNG_ADULTS = "young_adults"   # Thanh niên (18-25)
    ADULTS = "adults"               # Người lớn (26-65)
    SENIORS = "seniors"             # Người cao tuổi (65+)
    PROFESSIONALS = "professionals"  # Chuyên gia
    GENERAL = "general"             # Đại chúng


@dataclass
class TransformationRequest:
    """Request cho content transformation"""
    source_text: str
    transformation_type: TransformationType
    target_audience: TargetAudience = TargetAudience.GENERAL
    difficulty_level: ContentDifficulty = ContentDifficulty.INTERMEDIATE
    language: str = "vi"
    context: Optional[str] = None
    style_preferences: Dict[str, Any] = None
    duration_target: Optional[int] = None  # phút
    
    def __post_init__(self):
        if self.style_preferences is None:
            self.style_preferences = {}


@dataclass
class TransformationResponse:
    """Response từ content transformation"""
    transformed_content: str
    transformation_type: TransformationType
    metadata: Dict[str, Any]
    processing_time: float
    quality_score: float
    estimated_duration: Optional[int] = None  # phút
    additional_assets: Dict[str, Any] = None  # files, images, etc.
    
    def __post_init__(self):
        if self.additional_assets is None:
            self.additional_assets = {}


class BaseContentTransformer(ABC):
    """
    Abstract base class cho tất cả content transformers
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.transformer_type = self._get_transformer_type()
    
    @abstractmethod
    def _get_transformer_type(self) -> TransformationType:
        """Trả về loại transformer"""
        pass
    
    @abstractmethod
    async def transform(self, request: TransformationRequest) -> TransformationResponse:
        """
        Transform content theo yêu cầu
        
        Args:
            request: Transformation request với text và parameters
            
        Returns:
            TransformationResponse với content đã transform
        """
        pass
    
    @abstractmethod
    def get_supported_audiences(self) -> List[TargetAudience]:
        """Trả về danh sách audiences được support"""
        pass
    
    @abstractmethod
    def get_supported_difficulties(self) -> List[ContentDifficulty]:
        """Trả về danh sách difficulty levels được support"""
        pass
    
    @abstractmethod
    def estimate_duration(self, text: str, target_audience: TargetAudience) -> int:
        """Ước tính duration (phút) của content sau transform"""
        pass
    
    def validate_request(self, request: TransformationRequest) -> bool:
        """Validate transformation request"""
        if not request.source_text.strip():
            return False
        
        if request.target_audience not in self.get_supported_audiences():
            return False
            
        if request.difficulty_level not in self.get_supported_difficulties():
            return False
        
        return True
    
    def get_transformer_info(self) -> Dict[str, Any]:
        """Lấy thông tin về transformer"""
        return {
            "type": self.transformer_type.value,
            "supported_audiences": [a.value for a in self.get_supported_audiences()],
            "supported_difficulties": [d.value for d in self.get_supported_difficulties()],
            "config": self.config
        }
    
    def calculate_quality_score(self, request: TransformationRequest, 
                              response: TransformationResponse) -> float:
        """Tính quality score cho transformation"""
        # Base implementation - có thể override
        scores = []
        
        # Length appropriateness
        length_ratio = len(response.transformed_content) / len(request.source_text)
        if self.transformer_type == TransformationType.PODCAST_SCRIPT:
            # Podcast script should be longer (thêm narration)
            length_score = 1.0 if 1.2 <= length_ratio <= 2.0 else 0.7
        elif self.transformer_type == TransformationType.SUMMARY:
            # Summary should be shorter
            length_score = 1.0 if 0.2 <= length_ratio <= 0.5 else 0.7
        else:
            # Other types, similar length
            length_score = 1.0 if 0.8 <= length_ratio <= 1.5 else 0.8
        
        scores.append(length_score)
        
        # Processing time score (faster is better)
        time_score = 1.0 if response.processing_time < 5.0 else 0.8
        scores.append(time_score)
        
        # Content completeness (has content)
        completeness_score = 1.0 if response.transformed_content.strip() else 0.0
        scores.append(completeness_score)
        
        return sum(scores) / len(scores)


class TransformationError(Exception):
    """Base exception cho transformation errors"""
    
    def __init__(self, message: str, transformer_type: str, error_code: Optional[str] = None):
        self.message = message
        self.transformer_type = transformer_type
        self.error_code = error_code
        super().__init__(f"[{transformer_type}] {message}")


class UnsupportedTransformationError(TransformationError):
    """Raised khi transformation type không được support"""
    pass


class InvalidRequestError(TransformationError):
    """Raised khi request không valid"""
    pass
