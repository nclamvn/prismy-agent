"""Test response handler directly"""
from claude_response_handler import ClaudeResponseHandler

# Test various response formats
test_responses = [
    # Test 1: Clear service mention
    """
    Greeting: Xin chào! Tôi sẽ giúp bạn tạo video.
    Service: video_creation
    Confidence: 0.9
    Language: vi
    """,
    
    # Test 2: Natural response
    """
    Xin chào anh Minh! Tôi sẽ giúp anh tạo video từ báo cáo.
    
    I understand you need video_creation service.
    My confidence is 0.95
    The language is Vietnamese
    """,
    
    # Test 3: What Claude might actually return
    """
    Greeting: Xin chào anh Minh! Rất vui được hỗ trợ anh với việc tạo video từ báo cáo tài chính quý 4.
    Service: general_inquiry
    Confidence: 0.95
    Language: vi
    """
]

handler = ClaudeResponseHandler()

for i, response in enumerate(test_responses, 1):
    print(f"\n--- Test {i} ---")
    greeting, intent = handler.parse_intent_response(response)
    print(f"Service parsed: {intent.get('service', 'NOT FOUND')}")
    print(f"Greeting: {greeting[:50]}...")
