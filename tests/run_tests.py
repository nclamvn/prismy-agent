#!/usr/bin/env python3
"""
Custom test runner - không dùng pytest
"""
import sys
import time
import traceback
from typing import List, Tuple

sys.path.insert(0, '.')

class TestRunner:
    """Simple test runner"""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        
    def run_test(self, test_func, test_name):
        """Run a single test"""
        try:
            print(f"  Running: {test_name}...", end='')
            start = time.time()
            test_func()
            elapsed = time.time() - start
            print(f" ✅ PASSED ({elapsed:.3f}s)")
            self.passed += 1
        except AssertionError as e:
            print(f" ❌ FAILED")
            self.failed += 1
            self.errors.append((test_name, str(e), traceback.format_exc()))
        except Exception as e:
            print(f" 💥 ERROR")
            self.failed += 1
            self.errors.append((test_name, str(e), traceback.format_exc()))
    
    def report(self):
        """Print test report"""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST RESULTS: {self.passed}/{total} passed")
        print(f"{'='*60}")
        
        if self.errors:
            print("\nFAILURES:")
            for name, error, trace in self.errors:
                print(f"\n❌ {name}")
                print(f"   Error: {error}")
                if '--verbose' in sys.argv:
                    print(f"   Trace:\n{trace}")
        
        return self.failed == 0

# TEST SUITE 1: Exceptions
def test_exceptions():
    """Test exception module"""
    from src.core.exceptions import (
        BaseAppException, LLMAPIKeyError, 
        TranslationTimeoutError, ValidationError
    )
    
    runner = TestRunner()
    print("\n🧪 TESTING: Exceptions")
    print("-" * 40)
    
    # Test 1: Base exception
    def test_base_exception():
        exc = BaseAppException("Test error", "TEST_ERROR", {"key": "value"})
        assert exc.message == "Test error"
        assert exc.error_code == "TEST_ERROR"
        assert exc.details == {"key": "value"}
        result = exc.to_dict()
        assert result["error"] == "TEST_ERROR"
        assert result["message"] == "Test error"
    
    runner.run_test(test_base_exception, "BaseAppException")
    
    # Test 2: LLM API Key Error
    def test_llm_api_key_error():
        exc = LLMAPIKeyError("Missing key", details={"provider": "openai"})
        assert exc.error_code == "LLMAPIKeyError"
        assert exc.details["provider"] == "openai"
        assert "Missing key" in str(exc)
    
    runner.run_test(test_llm_api_key_error, "LLMAPIKeyError")
    
    # Test 3: Translation Timeout
    def test_translation_timeout():
        exc = TranslationTimeoutError(
            "Timeout", 
            details={"timeout": 30, "text_length": 5000}
        )
        result = exc.to_dict()
        assert result["details"]["timeout"] == 30
        assert result["details"]["text_length"] == 5000
    
    runner.run_test(test_translation_timeout, "TranslationTimeoutError")
    
    # Test 4: Validation Error
    def test_validation_error():
        exc = ValidationError("Invalid input")
        assert exc.error_code == "ValidationError"
        assert exc.message == "Invalid input"
    
    runner.run_test(test_validation_error, "ValidationError")
    
    return runner

# TEST SUITE 2: Validation
def test_validation():
    """Test validation module"""
    from src.core.validation.validators import (
        TranslationRequestValidation,
        validate_api_key
    )
    from src.core.exceptions import InvalidInputError
    
    runner = TestRunner()
    print("\n🧪 TESTING: Validation")
    print("-" * 40)
    
    # Test 1: Valid translation request
    def test_valid_request():
        req = TranslationRequestValidation(
            source_text="Hello world",
            source_lang="en",
            target_lang="vi"
        )
        assert req.source_text == "Hello world"
        assert req.source_lang == "en"
    
    runner.run_test(test_valid_request, "Valid translation request")
    
    # Test 2: Invalid language
    def test_invalid_language():
        try:
            TranslationRequestValidation(
                source_text="Hello",
                source_lang="xyz",
                target_lang="vi"
            )
            assert False, "Should have raised error"
        except Exception:
            pass  # Expected
    
    runner.run_test(test_invalid_language, "Invalid language validation")
    
    # Test 3: API key validation
    def test_api_key():
        assert validate_api_key("sk-123456", "openai") == True
        try:
            validate_api_key("", "openai")
            assert False, "Should have raised error"
        except InvalidInputError:
            pass  # Expected
    
    runner.run_test(test_api_key, "API key validation")
    
    return runner

# TEST SUITE 3: Retry Mechanism
def test_retry():
    """Test retry mechanism"""
    from src.core.utils.retry import retry
    
    runner = TestRunner()
    print("\n🧪 TESTING: Retry Mechanism")
    print("-" * 40)
    
    # Test 1: Success on first try
    def test_success_first_try():
        call_count = 0
        
        @retry(max_attempts=3)
        def successful_func():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = successful_func()
        assert result == "success"
        assert call_count == 1
    
    runner.run_test(test_success_first_try, "Success on first attempt")
    
    # Test 2: Success after retries
    def test_success_after_retries():
        call_count = 0
        
        @retry(max_attempts=3, delay=0.01)
        def eventually_works():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("Not yet")
            return "success"
        
        result = eventually_works()
        assert result == "success"
        assert call_count == 3
    
    runner.run_test(test_success_after_retries, "Success after retries")
    
    return runner

# TEST SUITE 4: Health Checks
def test_health():
    """Test health check system"""
    from src.core.utils.health_check import (
        ComponentHealth, HealthStatus, check_disk_space
    )
    
    runner = TestRunner()
    print("\n🧪 TESTING: Health Checks")
    print("-" * 40)
    
    # Test 1: Component health
    def test_component_health():
        health = ComponentHealth(
            name="test",
            status=HealthStatus.HEALTHY,
            message="All good"
        )
        assert health.name == "test"
        assert health.status == HealthStatus.HEALTHY
    
    runner.run_test(test_component_health, "Component health creation")
    
    # Test 2: Disk space check
    def test_disk_check():
        result = check_disk_space()
        assert result.name == "disk_space"
        assert result.status in [
            HealthStatus.HEALTHY, 
            HealthStatus.DEGRADED, 
            HealthStatus.UNHEALTHY
        ]
        assert "Disk usage:" in result.message
    
    runner.run_test(test_disk_check, "Disk space check")
    
    return runner

# MAIN TEST RUNNER
def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🧪 CUSTOM TEST RUNNER")
    print("="*60)
    
    all_passed = True
    runners = []
    
    # Run all test suites
    test_suites = [
        test_exceptions,
        test_validation,
        test_retry,
        test_health
    ]
    
    for suite in test_suites:
        try:
            runner = suite()
            runners.append(runner)
            if runner.failed > 0:
                all_passed = False
        except Exception as e:
            print(f"\n💥 Suite failed: {e}")
            all_passed = False
    
    # Final report
    print("\n" + "="*60)
    print("📊 FINAL SUMMARY")
    print("="*60)
    
    total_passed = sum(r.passed for r in runners)
    total_failed = sum(r.failed for r in runners)
    total = total_passed + total_failed
    
    print(f"\nTotal Tests: {total}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
