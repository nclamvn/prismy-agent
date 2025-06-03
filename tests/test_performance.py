"""
Performance benchmarks
"""
import sys
import time
import asyncio
from statistics import mean, stdev
sys.path.insert(0, '.')

def benchmark(func, iterations=10):
    """Benchmark a function"""
    times = []
    for _ in range(iterations):
        start = time.time()
        func()
        times.append(time.time() - start)
    
    return {
        "mean": mean(times),
        "stdev": stdev(times) if len(times) > 1 else 0,
        "min": min(times),
        "max": max(times),
        "iterations": iterations
    }

print("\n🏎️  PERFORMANCE BENCHMARKS")
print("="*60)

# Benchmark 1: Exception creation
print("\n📊 Exception Creation Performance:")
from src.core.exceptions import BaseAppException

def create_exception():
    exc = BaseAppException("Test", "TEST", {"data": "value"})
    exc.to_dict()

result = benchmark(create_exception, 1000)
print(f"  Mean: {result['mean']*1000:.3f}ms")
print(f"  Min:  {result['min']*1000:.3f}ms")
print(f"  Max:  {result['max']*1000:.3f}ms")

# Benchmark 2: Validation
print("\n📊 Validation Performance:")
from src.core.validation.validators import TextValidation

def validate_text():
    try:
        TextValidation(text="Hello world test", language="en")
    except:
        pass

result = benchmark(validate_text, 100)
print(f"  Mean: {result['mean']*1000:.3f}ms")
print(f"  Min:  {result['min']*1000:.3f}ms")
print(f"  Max:  {result['max']*1000:.3f}ms")

# Benchmark 3: Logging
print("\n📊 Logging Performance:")
from src.config.logging_config import get_logger
logger = get_logger("benchmark")

def log_message():
    logger.debug("Benchmark message")

result = benchmark(log_message, 1000)
print(f"  Mean: {result['mean']*1000:.3f}ms")
print(f"  Min:  {result['min']*1000:.3f}ms")
print(f"  Max:  {result['max']*1000:.3f}ms")

print("\n✅ Performance benchmarks complete!")
