# src/api/v1/endpoints/document.py

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from typing import Optional, Dict, Any, List
import json
import uuid
from datetime import datetime

from src.core.models.requests import ProcessingRequest
from src.core.models.responses import ProcessingResponse, ProcessingStatus
from src.core.models.document import Document, ProcessedDocument
from src.core.utils.logger import Logger
from src.infrastructure.document_processing.document_processor import DocumentProcessor

logger = Logger(__name__)
router = APIRouter()

# Initialize document processor
document_processor = DocumentProcessor()

# In-memory storage for demo (replace with database in production)
processing_jobs = {}


@router.post("/process", response_model=ProcessingResponse)
async def process_document(
    file: UploadFile = File(...),
    output_format: str = Form(...),
    options: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """
    Process a document with advanced optimization.
    
    Args:
        file: Document file (txt, pdf, docx)
        output_format: Target format (translation, podcast, course, video, screenplay)
        options: JSON string with processing options:
            - target_language: For translation (e.g., "es", "fr", "ja")
            - quality_level: "high", "medium", "low"
            - budget_limit: Maximum cost in USD
            - use_cache: Whether to use caching (default: true)
            - podcast_style: "conversational", "educational", "narrative"
            - course_level: "beginner", "intermediate", "advanced"
            - video_duration: Target duration in seconds (e.g., 90)
    
    Returns:
        Processing job information
    """
    try:
        # Parse options
        processing_options = {}
        if options:
            try:
                processing_options = json.loads(options)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid options format")
        
        # Validate output format
        valid_formats = ["translation", "podcast", "course", "video", "screenplay"]
        if output_format not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid output format. Must be one of: {valid_formats}"
            )
        
        # Read file content
        content = await file.read()
        
        # Decode content
        try:
            text_content = content.decode('utf-8')
        except UnicodeDecodeError:
            # Try different encodings
            for encoding in ['latin-1', 'iso-8859-1', 'windows-1252']:
                try:
                    text_content = content.decode(encoding)
                    break
                except:
                    continue
            else:
                raise HTTPException(status_code=400, detail="Unable to decode file content")
        
        # Create document
        doc_id = str(uuid.uuid4())
        document = Document(
            id=doc_id,
            content=text_content,
            title=file.filename,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "upload_time": datetime.now().isoformat()
            }
        )
        
        # Create job ID
        job_id = str(uuid.uuid4())
        
        # Store job info
        processing_jobs[job_id] = {
            "status": "processing",
            "document_id": doc_id,
            "output_format": output_format,
            "options": processing_options,
            "created_at": datetime.now(),
            "result": None,
            "error": None
        }
        
        # Process in background
        background_tasks.add_task(
            process_document_task,
            job_id,
            document,
            output_format,
            processing_options
        )
        
        return ProcessingResponse(
            job_id=job_id,
            status="processing",
            message=f"Document processing started. Format: {output_format}",
            estimated_time=estimate_processing_time(document, output_format),
            metadata={
                "document_id": doc_id,
                "word_count": document.word_count,
                "estimated_cost": estimate_cost(document, output_format, processing_options)
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status/{job_id}", response_model=ProcessingResponse)
async def get_processing_status(job_id: str):
    """Get status of processing job."""
    if job_id not in processing_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = processing_jobs[job_id]
    
    response = ProcessingResponse(
        job_id=job_id,
        status=job["status"],
        message=get_status_message(job),
        metadata={}
    )
    
    if job["status"] == "completed" and job["result"]:
        result: ProcessedDocument = job["result"]
        response.result = {
            "content": result.processed_content,
            "format": result.output_format,
            "processing_time": result.processing_time,
            "total_cost": result.total_cost,
            "chunks_processed": len(result.chunks),
            "models_used": list(result.model_usage.keys()),
            "cache_hits": result.metadata.get("cache_hits", 0)
        }
        response.metadata = result.get_summary_stats()
        
    elif job["status"] == "failed":
        response.error = job.get("error", "Unknown error")
        
    return response


@router.post("/batch", response_model=List[ProcessingResponse])
async def process_batch(
    files: List[UploadFile] = File(...),
    output_format: str = Form(...),
    options: Optional[str] = Form(None),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    """Process multiple documents in batch."""
    try:
        # Parse options
        processing_options = {}
        if options:
            processing_options = json.loads(options)
            
        responses = []
        
        for file in files[:10]:  # Limit to 10 files
            # Create document
            content = await file.read()
            text_content = content.decode('utf-8', errors='replace')
            
            doc_id = str(uuid.uuid4())
            document = Document(
                id=doc_id,
                content=text_content,
                title=file.filename
            )
            
            # Create job
            job_id = str(uuid.uuid4())
            processing_jobs[job_id] = {
                "status": "queued",
                "document_id": doc_id,
                "output_format": output_format,
                "options": processing_options,
                "created_at": datetime.now()
            }
            
            # Add to background tasks
            background_tasks.add_task(
                process_document_task,
                job_id,
                document,
                output_format,
                processing_options
            )
            
            responses.append(ProcessingResponse(
                job_id=job_id,
                status="queued",
                message=f"Document {file.filename} queued for processing"
            ))
            
        return responses
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cost-estimate")
async def estimate_processing_cost(
    word_count: int,
    output_format: str,
    quality_level: str = "medium"
):
    """Estimate processing cost before upload."""
    try:
        # Create dummy document for estimation
        dummy_content = "word " * word_count
        document = Document(
            id="dummy",
            content=dummy_content
        )
        
        # Get cost breakdown
        from src.infrastructure.document_processing.orchestrators.cost_calculator import CostCalculator
        calculator = CostCalculator()
        
        # Define model strategy based on quality
        model_strategies = {
            "low": {
                "outline": "gpt-3.5-turbo",
                "main_processing": "gemini-1.5-flash",
                "refinement": "gpt-3.5-turbo"
            },
            "medium": {
                "outline": "gpt-3.5-turbo",
                "main_processing": "claude-3-sonnet-20240229",
                "refinement": "gpt-3.5-turbo"
            },
            "high": {
                "outline": "gpt-4-turbo-preview",
                "main_processing": "claude-3-opus-20240229",
                "refinement": "gpt-4-turbo-preview"
            }
        }
        
        strategy = model_strategies.get(quality_level, model_strategies["medium"])
        cost_breakdown = calculator.estimate_document_cost(
            document,
            output_format,
            strategy
        )
        
        return {
            "word_count": word_count,
            "output_format": output_format,
            "quality_level": quality_level,
            "estimated_cost_usd": round(cost_breakdown["total"], 2),
            "cost_breakdown": cost_breakdown,
            "estimated_time_minutes": round(word_count / 1000, 1),
            "recommended_budget": round(cost_breakdown["total"] * 1.2, 2)  # 20% buffer
        }
        
    except Exception as e:
        logger.error(f"Cost estimation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_processing_stats():
    """Get document processor statistics."""
    stats = document_processor.get_processing_stats()
    
    # Add job statistics
    job_stats = {
        "total_jobs": len(processing_jobs),
        "active_jobs": sum(1 for j in processing_jobs.values() if j["status"] == "processing"),
        "completed_jobs": sum(1 for j in processing_jobs.values() if j["status"] == "completed"),
        "failed_jobs": sum(1 for j in processing_jobs.values() if j["status"] == "failed")
    }
    
    stats["job_stats"] = job_stats
    
    return stats


@router.post("/optimize-cache")
async def optimize_cache():
    """Optimize document processor cache."""
    try:
        document_processor.optimize_cache()
        stats = document_processor.cache_manager.get_cache_stats()
        
        return {
            "message": "Cache optimized successfully",
            "cache_stats": stats
        }
        
    except Exception as e:
        logger.error(f"Cache optimization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Helper functions

async def process_document_task(
    job_id: str,
    document: Document,
    output_format: str,
    options: Dict[str, Any]
):
    """Background task to process document."""
    try:
        # Update job status
        processing_jobs[job_id]["status"] = "processing"
        
        # Process document
        result = await document_processor.process_document(
            document,
            output_format,
            options
        )
        
        # Update job with result
        processing_jobs[job_id]["status"] = "completed"
        processing_jobs[job_id]["result"] = result
        
    except Exception as e:
        logger.error(f"Processing task error: {str(e)}")
        processing_jobs[job_id]["status"] = "failed"
        processing_jobs[job_id]["error"] = str(e)


def estimate_processing_time(document: Document, output_format: str) -> float:
    """Estimate processing time in seconds."""
    base_time = document.word_count / 1000 * 60  # 1 minute per 1000 words
    
    # Format multipliers
    format_multipliers = {
        "translation": 0.8,
        "podcast": 1.2,
        "course": 1.5,
        "video": 1.0,
        "screenplay": 1.3
    }
    
    multiplier = format_multipliers.get(output_format, 1.0)
    
    return base_time * multiplier


def estimate_cost(
    document: Document,
    output_format: str,
    options: Dict[str, Any]
) -> Dict[str, float]:
    """Estimate processing cost."""
    quality_level = options.get("quality_level", "medium")
    
    # Base cost per 1000 words
    base_costs = {
        "low": 0.05,
        "medium": 0.15,
        "high": 0.50
    }
    
    base_cost = base_costs.get(quality_level, base_costs["medium"])
    word_thousands = document.word_count / 1000
    
    # Format multipliers
    format_multipliers = {
        "translation": 0.8,
        "podcast": 1.5,
        "course": 2.0,
        "video": 1.2,
        "screenplay": 1.4
    }
    
    multiplier = format_multipliers.get(output_format, 1.0)
    estimated_cost = base_cost * word_thousands * multiplier
    
    return {
        "estimated_usd": round(estimated_cost, 2),
        "min_usd": round(estimated_cost * 0.8, 2),
        "max_usd": round(estimated_cost * 1.2, 2)
    }


def get_status_message(job: Dict[str, Any]) -> str:
    """Get human-readable status message."""
    status = job["status"]
    
    if status == "processing":
        return "Document is being processed. This may take a few minutes."
    elif status == "completed":
        return "Document processing completed successfully."
    elif status == "failed":
        return f"Processing failed: {job.get('error', 'Unknown error')}"
    elif status == "queued":
        return "Document is queued for processing."
    else:
        return "Unknown status"
