"""
Transformation Manager - Quản lý tất cả content transformers
Central manager for all content transformations
"""

from typing import Dict, List, Optional, Any
import logging
from dataclasses import dataclass
import time

from .base_transformer import (
    BaseContentTransformer,
    TransformationType,
    TransformationRequest,
    TransformationResponse,
    TransformationError,
    TargetAudience,
    ContentDifficulty
)

# Import các transformers
from .podcast_generator import PodcastGenerator
from .unified_video_processor import UnifiedVideoProcessor
from .education_module_builder import EducationModuleBuilder


@dataclass
class TransformationJob:
    """Job transformation với tracking"""
    job_id: str
    request: TransformationRequest
    status: str = "pending"  # pending, processing, completed, failed
    result: Optional[TransformationResponse] = None
    error: Optional[str] = None
    created_at: float = None
    completed_at: float = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = time.time()


class TransformationManager:
    """
    Central manager cho tất cả content transformations
    Handles routing, validation, và orchestration
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.transformers: Dict[TransformationType, BaseContentTransformer] = {}
        self._register_built_in_transformers()
        self.jobs: Dict[str, TransformationJob] = {}
        self._job_counter = 0
    
    def _register_built_in_transformers(self):
        """Register các transformers có sẵn"""
        transformers_to_register = [
            PodcastGenerator(),
            UnifiedVideoProcessor(), 
            EducationModuleBuilder()
        ]
        
        for transformer in transformers_to_register:
            self.register_transformer(transformer)
            
    def register_transformer(self, transformer: BaseContentTransformer):
        """
        Register một transformer mới
        
        Args:
            transformer: Transformer instance to register
        """
        transformer_type = transformer._get_transformer_type()
        
        if transformer_type in self.transformers:
            self.logger.warning(
                f"Overwriting existing transformer for type: {transformer_type}"
            )
        
        self.transformers[transformer_type] = transformer
        self.logger.info(f"Registered transformer for type: {transformer_type}")
    
    def get_available_transformations(self) -> List[Dict[str, Any]]:
        """Get danh sách các transformations khả dụng"""
        available = []
        
        for trans_type, transformer in self.transformers.items():
            info = transformer.get_transformer_info()
            available.append({
                "type": trans_type.value,
                "name": info["name"],
                "description": info["description"],
                "supported_audiences": info["supported_audiences"],
                "supported_difficulties": info["supported_difficulties"],
                "estimated_duration_range": info["estimated_duration_range"]
            })
        
        return available
    
    def validate_request(self, request: TransformationRequest) -> bool:
        """
        Validate transformation request
        
        Args:
            request: Request to validate
            
        Returns:
            True if valid
            
        Raises:
            TransformationError if invalid
        """
        # Check transformer exists
        if request.transformation_type not in self.transformers:
            raise TransformationError(
                f"Unsupported transformation type: {request.transformation_type}",
                transformer_type=request.transformation_type.value,
                error_code="UNSUPPORTED_TYPE"
            )
        
        # Get transformer
        transformer = self.transformers[request.transformation_type]
        
        # Validate using transformer's validation
        if not transformer.validate_request(request):
            raise TransformationError(
                "Request validation failed",
                transformer_type=request.transformation_type.value,
                error_code="VALIDATION_FAILED"
            )
        
        return True
    
    async def transform_content(
        self,
        request: TransformationRequest,
        track_job: bool = True
    ) -> TransformationResponse:
        """
        Transform content using appropriate transformer
        
        Args:
            request: Transformation request
            track_job: Whether to track as a job
            
        Returns:
            TransformationResponse
        """
        # Validate request
        self.validate_request(request)
        
        # Create job if tracking
        job_id = None
        if track_job:
            job_id = self._create_job(request)
        
        try:
            # Get transformer
            transformer = self.transformers[request.transformation_type]
            
            # Log transformation start
            self.logger.info(
                f"Starting transformation: {request.transformation_type.value}"
            )
            
            # Execute transformation
            response = await transformer.transform(request)
            
            # Update job if tracking
            if job_id:
                self._complete_job(job_id, response)
            
            # Log success
            self.logger.info(
                f"Transformation completed successfully. "
                f"Quality score: {response.quality_score}"
            )
            
            return response
            
        except Exception as e:
            # Update job if tracking
            if job_id:
                self._fail_job(job_id, str(e))
            
            # Log error
            self.logger.error(f"Transformation failed: {e}")
            
            # Re-raise
            if isinstance(e, TransformationError):
                raise
            else:
                raise TransformationError(
                    f"Transformation failed: {str(e)}",
                    transformer_type=request.transformation_type.value,
                    error_code="TRANSFORMATION_FAILED"
                )
    
    def estimate_duration(
        self,
        text: str,
        transformation_type: TransformationType,
        target_audience: TargetAudience
    ) -> int:
        """
        Estimate duration for transformation
        
        Args:
            text: Source text
            transformation_type: Type of transformation
            target_audience: Target audience
            
        Returns:
            Estimated duration in minutes
        """
        if transformation_type not in self.transformers:
            raise TransformationError(
                f"Unsupported transformation type: {transformation_type}",
                transformer_type=transformation_type.value,
                error_code="UNSUPPORTED_TYPE"
            )
        
        transformer = self.transformers[transformation_type]
        return transformer.estimate_duration(text, target_audience)
    
    def get_transformer_info(
        self,
        transformation_type: TransformationType
    ) -> Dict[str, Any]:
        """Get information about a specific transformer"""
        if transformation_type not in self.transformers:
            raise TransformationError(
                f"Unsupported transformation type: {transformation_type}",
                transformer_type=transformation_type.value,
                error_code="UNSUPPORTED_TYPE"
            )
        
        return self.transformers[transformation_type].get_transformer_info()
    
    # Job tracking methods
    def _create_job(self, request: TransformationRequest) -> str:
        """Create a new job"""
        self._job_counter += 1
        job_id = f"job_{self._job_counter}_{int(time.time())}"
        
        job = TransformationJob(
            job_id=job_id,
            request=request,
            status="processing"
        )
        
        self.jobs[job_id] = job
        return job_id
    
    def _complete_job(self, job_id: str, response: TransformationResponse):
        """Mark job as completed"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.status = "completed"
            job.result = response
            job.completed_at = time.time()
    
    def _fail_job(self, job_id: str, error: str):
        """Mark job as failed"""
        if job_id in self.jobs:
            job = self.jobs[job_id]
            job.status = "failed"
            job.error = error
            job.completed_at = time.time()
    
    def get_job_status(self, job_id: str) -> Optional[TransformationJob]:
        """Get job status"""
        return self.jobs.get(job_id)
    
    def get_recent_jobs(self, limit: int = 10) -> List[TransformationJob]:
        """Get recent jobs"""
        sorted_jobs = sorted(
            self.jobs.values(),
            key=lambda j: j.created_at,
            reverse=True
        )
        return sorted_jobs[:limit]
    
    def cleanup_old_jobs(self, max_age_seconds: int = 3600):
        """Clean up old completed/failed jobs"""
        current_time = time.time()
        jobs_to_remove = []
        
        for job_id, job in self.jobs.items():
            if job.status in ["completed", "failed"]:
                if current_time - job.created_at > max_age_seconds:
                    jobs_to_remove.append(job_id)
        
        for job_id in jobs_to_remove:
            del self.jobs[job_id]
        
        if jobs_to_remove:
            self.logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
    
    def get_supported_formats_for_video(self) -> List[str]:
        """Get supported output formats for video transformation"""
        if TransformationType.VIDEO_SCENARIO in self.transformers:
            video_processor = self.transformers[TransformationType.VIDEO_SCENARIO]
            if hasattr(video_processor, 'VideoOutputFormat'):
                return [fmt.value for fmt in video_processor.VideoOutputFormat]
        return ["screenplay", "ai_prompts"]  # Default formats
    
    def get_supported_ai_platforms(self) -> List[str]:
        """Get supported AI video platforms"""
        if TransformationType.VIDEO_SCENARIO in self.transformers:
            video_processor = self.transformers[TransformationType.VIDEO_SCENARIO]
            if hasattr(video_processor, 'AI_PLATFORMS'):
                return list(video_processor.AI_PLATFORMS.keys())
        return ["sora", "kling", "veo3", "runway"]  # Default platforms


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def test_manager():
        # Initialize manager
        manager = TransformationManager()
        
        # Get available transformations
        available = manager.get_available_transformations()
        print("\n📋 Available Transformations:")
        for trans in available:
            print(f"  - {trans['name']}: {trans['description']}")
        
        # Test video transformation
        test_text = """
        PRISM AI Platform là giải pháp cách mạng cho content transformation.
        Với DNA fingerprinting technology, đảm bảo visual continuity hoàn hảo.
        """
        
        request = TransformationRequest(
            source_text=test_text,
            transformation_type=TransformationType.VIDEO_SCENARIO,
            target_audience=TargetAudience.ADULTS,
            difficulty_level=ContentDifficulty.INTERMEDIATE,
            language="vi",
            duration_target=2
        )
        
        # Transform content
        print("\n🎬 Testing Video Transformation...")
        response = await manager.transform_content(request)
        
        if response.transformed_content:
            print("✅ Transformation successful!")
            print(f"Quality Score: {response.quality_score}")
            print(f"Processing Time: {response.processing_time:.2f}s")
        
        # Get supported formats
        print("\n📽️ Supported Video Formats:")
        formats = manager.get_supported_formats_for_video()
        for fmt in formats:
            print(f"  - {fmt}")
        
        print("\n🤖 Supported AI Platforms:")
        platforms = manager.get_supported_ai_platforms()
        for platform in platforms:
            print(f"  - {platform}")
    
    # Run test
    asyncio.run(test_manager())