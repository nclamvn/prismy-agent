import re

# Read file
with open('intelligent_claude_commander.py', 'r') as f:
    content = f.read()

# Add debug prints
debug_code = '''
        print(f"DEBUG: greet_and_analyze called with request: {request}")
        
        if not self.claude:
            print("DEBUG: No Claude client, using fallback")
            return self._fallback_greeting(customer_name, request)
        
        try:
            print("DEBUG: Attempting Claude API call...")'''

# Find the method and add debug
content = re.sub(
    r'(async def greet_and_analyze.*?\n.*?""".*?""")',
    r'\1' + debug_code,
    content,
    flags=re.DOTALL
)

# Also add debug in exception handler
content = re.sub(
    r'(except Exception as e:.*?\n.*?print\(f"Claude API error: {e}"\))',
    r'\1\n            print(f"DEBUG: Full exception: {type(e).__name__}: {str(e)}")\n            import traceback\n            traceback.print_exc()',
    content
)

# Write back
with open('intelligent_claude_commander.py', 'w') as f:
    f.write(content)

print("✅ Added debug to greet_and_analyze")
