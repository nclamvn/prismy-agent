"""
Simple test to verify setup
"""
def test_basic():
    """Basic test"""
    assert 1 + 1 == 2

def test_import():
    """Test imports work"""
    from src.core.exceptions import BaseAppException
    exc = BaseAppException("test", "TEST")
    assert exc.message == "test"
