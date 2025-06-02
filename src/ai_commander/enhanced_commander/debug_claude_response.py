"""Debug Claude responses"""
import asyncio
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

async def debug_claude():
    client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    # Test prompt
    prompt = """You are an AI assistant for PRISM platform that creates videos, podcasts, and educational content.

Customer request: "Tôi cần tạo video từ báo cáo tài chính Q4"

What service does this customer need? Choose ONE:
- video_creation (they want to create/make a video)
- podcast_generation (they want to create a podcast)
- translation (they need translation)
- general_inquiry (just asking questions)

Think step by step:
1. They said "tạo video" which means "create video"
2. They have content (financial report)
3. They want to transform it into video format

Answer with just the service name."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    
    print("Claude response:")
    print(response.content[0].text)
    print("\nExpected: video_creation")

asyncio.run(debug_claude())
