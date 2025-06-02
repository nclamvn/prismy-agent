"""See raw Claude response"""
import asyncio
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

async def test_raw():
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    request = "Tôi cần tạo video từ báo cáo tài chính Q4"
    
    prompt = f"""Request: "{request}"

IMPORTANT: Look for these keywords:
- If contains "tạo video", "create video", "make video" → Answer: video_creation
- If contains "podcast", "tạo podcast" → Answer: podcast_generation  
- If contains "dịch", "translate" → Answer: translation
- If contains "education", "lesson", "bài giảng" → Answer: education_module
- Otherwise → Answer: general_inquiry

For THIS specific request, what service is needed?

Format your response EXACTLY like this:
Greeting: [your greeting]
Service: [service name from above list]
Confidence: [number between 0 and 1]
Language: [vi or en]"""

    print("PROMPT SENT:")
    print(prompt)
    print("\n" + "="*60 + "\n")
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    print("CLAUDE RAW RESPONSE:")
    print(response.content[0].text)
    print("\n" + "="*60 + "\n")
    
    # Test parser
    from claude_response_handler import ClaudeResponseHandler
    handler = ClaudeResponseHandler()
    greeting, intent = handler.parse_intent_response(response.content[0].text)
    
    print("PARSED RESULT:")
    print(f"Service: {intent['service']}")
    print(f"Expected: video_creation")

asyncio.run(test_raw())
