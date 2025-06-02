"""Test IntelligentClaudeCommander standalone"""
import asyncio
from intelligent_claude_commander import IntelligentClaudeCommander

async def test():
    # Create fresh instance
    commander = IntelligentClaudeCommander()
    
    test_requests = [
        "Tôi cần tạo video từ báo cáo",
        "Create a podcast about AI",
        "Dịch tài liệu sang tiếng Anh"
    ]
    
    for req in test_requests:
        print(f"\n{'='*50}")
        print(f"Request: {req}")
        
        greeting, intent = await commander.greet_and_analyze("Test", req)
        
        print(f"Service: {intent.primary_service.value}")
        print(f"Confidence: {intent.confidence:.0%}")
        print(f"Greeting: {greeting[:50]}...")

asyncio.run(test())
