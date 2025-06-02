import re

# Read file
with open('intelligent_claude_commander.py', 'r') as f:
    content = f.read()

# Much simpler, clearer prompt
simple_prompt = '''prompt = f"""Customer: {customer_name}
Request: "{request}"

What service do they need?
- video_creation (want to create/make video)  
- podcast_generation (want to create podcast)
- translation (need translation)
- education_module (need educational content)
- general_inquiry (just asking questions)

Reply format:
Greeting: [warm greeting in same language as request]
Service: [one of the above]
Confidence: [0.0-1.0]
Language: [vi or en]"""'''

# Replace the complex prompt
content = re.sub(
    r'prompt = f""".*?Language: vi or en"""',
    simple_prompt,
    content,
    flags=re.DOTALL
)

# Write back
with open('intelligent_claude_commander.py', 'w') as f:
    f.write(content)

print("✅ Simplified Claude prompt for better detection")
