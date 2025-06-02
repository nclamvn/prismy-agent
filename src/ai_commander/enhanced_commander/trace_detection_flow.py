"""Trace the full detection flow"""
import asyncio
from intelligent_claude_commander import IntelligentClaudeCommander
import anthropic

# Monkey patch to trace
original_greet = IntelligentClaudeCommander.greet_and_analyze

async def traced_greet_and_analyze(self, customer_name: str, request: str):
    print(f"\n🔍 TRACE: greet_and_analyze called")
    print(f"   Customer: {customer_name}")
    print(f"   Request: {request}")
    
    # Check if Claude client exists
    print(f"   Claude client: {'YES' if self.claude else 'NO'}")
    
    if not self.claude:
        print("   ⚠️ Using fallback (no Claude)")
        return self._fallback_greeting(customer_name, request)
    
    # Get the prompt that will be sent
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
    
    print(f"\n   📝 Sending prompt to Claude...")
    
    try:
        response = self.claude.messages.create(
            model="claude-3-5-sonnet-20241022",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        
        response_text = response.content[0].text
        print(f"   📨 Claude response: {response_text[:100]}...")
        
        # Parse response
        greeting, intent_data = self.handler.parse_intent_response(response_text)
        print(f"   📊 Parsed service: {intent_data.get('service')}")
        
        # Create intent - THIS MIGHT BE THE ISSUE
        from intelligent_claude_commander import CustomerIntent, ServiceType
        intent = CustomerIntent(
            primary_service=ServiceType(intent_data.get('service', 'general_inquiry')),
            confidence=float(intent_data.get('confidence', 0.7)),
            keywords=intent_data.get('keywords', request.split()[:5]),
            language=intent_data.get('language', 'vi'),
            complexity=intent_data.get('complexity', 'moderate')
        )
        
        print(f"   ✅ Final intent: {intent.primary_service.value}")
        
        return greeting or f"Xin chào {customer_name}!", intent
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return self._fallback_greeting(customer_name, request)

# Apply patch
IntelligentClaudeCommander.greet_and_analyze = traced_greet_and_analyze

# Test
async def test():
    commander = IntelligentClaudeCommander()
    greeting, intent = await commander.greet_and_analyze(
        "Anh Minh",
        "Tôi cần tạo video từ báo cáo tài chính Q4"
    )
    print(f"\n🎯 FINAL RESULT: {intent.primary_service.value}")

asyncio.run(test())
