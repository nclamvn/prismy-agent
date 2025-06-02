"""
Health check endpoints
"""
from fastapi import APIRouter
from src.core.utils.health_check import HealthChecker, check_disk_space, check_llm_service

router = APIRouter()

@router.get("/")
async def health_check():
    """System health check"""
    checker = HealthChecker()
    checker.register_check("disk_space", check_disk_space)
    checker.register_check("llm_service", check_llm_service)
    
    health = await checker.check_health()
    return health

@router.get("/ready")
async def readiness():
    """Readiness probe"""
    # Check if all services are ready
    return {"status": "ready"}

@router.get("/live")
async def liveness():
    """Liveness probe"""
    return {"status": "alive"}
