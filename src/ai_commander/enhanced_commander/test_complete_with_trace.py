"""Test complete commander with detailed trace"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(__file__))

from complete_ai_commander import CompleteAICommander

# Patch to see what's happening
original_serve = CompleteAICommander.serve_customer_complete

async def traced_serve(self, customer_name, request, content=None):
    print(f"\n🔍 TRACING serve_customer_complete")
    print(f"   Request: {request}")
    
    # Check Claude commander
    print(f"   Claude commander: {type(self.claude).__name__}")
    
    # Call original
    result = await original_serve(self, customer_name, request, content)
    
    print(f"\n   📊 Result:")
    print(f"      Success: {result.get('success')}")
    print(f"      Intent: {result.get('intent').primary_service.value if result.get('intent') else 'None'}")
    print(f"      Message: {result.get('message', 'N/A')}")
    
    return result

CompleteAICommander.serve_customer_complete = traced_serve

async def test():
    commander = CompleteAICommander()
    
    # Test just video request
    await commander.serve_customer_complete(
        "Test User",
        "Tôi cần tạo video từ báo cáo",
        "Sample content"
    )

asyncio.run(test())
