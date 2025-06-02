"""Simple test for video detection"""
import asyncio
from intelligent_claude_commander import IntelligentClaudeCommander

async def test():
    commander = IntelligentClaudeCommander()
    
    # Test video request
    greeting, intent = await commander.greet_and_analyze(
        "Anh Minh", 
        "Tôi cần tạo video từ báo cáo tài chính"
    )
    
    print(f"Service detected: {intent.primary_service.value}")
    print(f"Should be: video_creation")

asyncio.run(test())
