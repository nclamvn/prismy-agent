"""Debug full Claude interaction"""
import asyncio
from intelligent_claude_commander import IntelligentClaudeCommander

# Patch to see raw response
import intelligent_claude_commander

original_parse = intelligent_claude_commander.ClaudeResponseHandler.parse_intent_response

def debug_parse(response_text):
    print("\n=== RAW CLAUDE RESPONSE ===")
    print(response_text)
    print("=== END RESPONSE ===\n")
    return original_parse(response_text)

intelligent_claude_commander.ClaudeResponseHandler.parse_intent_response = debug_parse

async def test():
    commander = IntelligentClaudeCommander()
    greeting, intent = await commander.greet_and_analyze(
        "Anh Minh", 
        "Tôi cần tạo video từ báo cáo tài chính"
    )
    
    print(f"Parsed service: {intent.primary_service.value}")
    print(f"Expected: video_creation")

asyncio.run(test())
