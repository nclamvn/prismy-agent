"""
Performance monitoring utilities
"""
import time
import functools
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)

def monitor_performance(
    log_args: bool = False,
    log_result: bool = False
):
    """
    Monitor function performance
    
    Args:
        log_args: Log function arguments
        log_result: Log function result
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            # Log start
            func_name = f"{func.__module__}.{func.__name__}"
            if log_args:
                logger.debug(f"Starting {func_name} with args={args}, kwargs={kwargs}")
            else:
                logger.debug(f"Starting {func_name}")
            
            try:
                result = await func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                # Log success
                if log_result:
                    logger.info(f"{func_name} completed in {elapsed:.2f}s, result={result}")
                else:
                    logger.info(f"{func_name} completed in {elapsed:.2f}s")
                
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{func_name} failed after {elapsed:.2f}s: {e}")
                raise
        
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            
            # Log start
            func_name = f"{func.__module__}.{func.__name__}"
            if log_args:
                logger.debug(f"Starting {func_name} with args={args}, kwargs={kwargs}")
            else:
                logger.debug(f"Starting {func_name}")
            
            try:
                result = func(*args, **kwargs)
                elapsed = time.time() - start_time
                
                # Log success
                if log_result:
                    logger.info(f"{func_name} completed in {elapsed:.2f}s, result={result}")
                else:
                    logger.info(f"{func_name} completed in {elapsed:.2f}s")
                
                return result
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(f"{func_name} failed after {elapsed:.2f}s: {e}")
                raise
        
        # Return appropriate wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator
