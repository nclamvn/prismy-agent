"""Deep debug why Claude is not being called"""
import asyncio
from intelligent_claude_commander import IntelligentClaudeCommander
import os

async def debug():
    commander = IntelligentClaudeCommander()
    
    print(f"1. Commander initialized")
    print(f"   - Has Claude client: {commander.claude is not None}")
    print(f"   - API key exists: {os.getenv('ANTHROPIC_API_KEY') is not None}")
    
    # Manually test the greet_and_analyze method
    request = "Tôi cần tạo video từ báo cáo"
    customer = "Test"
    
    print(f"\n2. Testing greet_and_analyze")
    print(f"   - Request: {request}")
    
    # Check if method exists
    print(f"   - Method exists: {hasattr(commander, 'greet_and_analyze')}")
    
    # Call method with debug
    try:
        # Check the actual prompt being used
        if commander.claude:
            print(f"   - Claude client type: {type(commander.claude)}")
            
            # Get prompt that would be sent
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
            
            print(f"\n3. Testing direct API call")
            response = commander.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200
            )
            print(f"   - API Response: {response.content[0].text}")
        
        print(f"\n4. Testing greet_and_analyze method")
        greeting, intent = await commander.greet_and_analyze(customer, request)
        print(f"   - Service: {intent.primary_service.value}")
        print(f"   - Confidence: {intent.confidence}")
        print(f"   - Is using fallback: {intent.confidence == 0.7}")
        
    except Exception as e:
        print(f"   - ERROR: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(debug())
