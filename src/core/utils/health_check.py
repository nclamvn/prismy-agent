"""
Health check utilities
"""
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
from src.config.logging_config import get_logger

logger = get_logger(__name__)

class HealthStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"

@dataclass
class ComponentHealth:
    name: str
    status: HealthStatus
    message: str = ""
    details: Dict[str, Any] = None

class HealthChecker:
    """System health checker"""
    
    def __init__(self):
        self.checks = []
    
    def register_check(self, name: str, check_func):
        """Register a health check function"""
        self.checks.append((name, check_func))
    
    async def check_health(self) -> Dict[str, Any]:
        """Run all health checks"""
        logger.info("Starting health checks")
        
        results = []
        overall_status = HealthStatus.HEALTHY
        
        for name, check_func in self.checks:
            try:
                if asyncio.iscoroutinefunction(check_func):
                    health = await check_func()
                else:
                    health = check_func()
                
                results.append(health)
                
                # Update overall status
                if health.status == HealthStatus.UNHEALTHY:
                    overall_status = HealthStatus.UNHEALTHY
                elif health.status == HealthStatus.DEGRADED and overall_status == HealthStatus.HEALTHY:
                    overall_status = HealthStatus.DEGRADED
                    
            except Exception as e:
                logger.error(f"Health check failed for {name}: {e}")
                results.append(ComponentHealth(
                    name=name,
                    status=HealthStatus.UNHEALTHY,
                    message=str(e)
                ))
                overall_status = HealthStatus.UNHEALTHY
        
        return {
            "status": overall_status.value,
            "components": [
                {
                    "name": r.name,
                    "status": r.status.value,
                    "message": r.message,
                    "details": r.details or {}
                }
                for r in results
            ]
        }

# Example health checks
def check_database() -> ComponentHealth:
    """Check database connection"""
    # Simulate check
    return ComponentHealth(
        name="database",
        status=HealthStatus.HEALTHY,
        message="Database connection OK"
    )

async def check_llm_service() -> ComponentHealth:
    """Check LLM service"""
    try:
        from src.infrastructure.ai_intelligence.llm_service import get_llm_service
        llm = get_llm_service()
        # Simple check - just verify it initializes
        return ComponentHealth(
            name="llm_service",
            status=HealthStatus.HEALTHY,
            message="LLM service available"
        )
    except Exception as e:
        return ComponentHealth(
            name="llm_service",
            status=HealthStatus.UNHEALTHY,
            message=str(e)
        )

def check_disk_space() -> ComponentHealth:
    """Check disk space"""
    import shutil
    
    try:
        usage = shutil.disk_usage("/")
        percent_used = (usage.used / usage.total) * 100
        
        if percent_used > 90:
            status = HealthStatus.UNHEALTHY
        elif percent_used > 80:
            status = HealthStatus.DEGRADED
        else:
            status = HealthStatus.HEALTHY
            
        return ComponentHealth(
            name="disk_space",
            status=status,
            message=f"Disk usage: {percent_used:.1f}%",
            details={
                "total_gb": usage.total / (1024**3),
                "used_gb": usage.used / (1024**3),
                "free_gb": usage.free / (1024**3)
            }
        )
    except Exception as e:
        return ComponentHealth(
            name="disk_space",
            status=HealthStatus.UNHEALTHY,
            message=str(e)
        )
