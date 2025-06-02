import re

# Read the file
with open('src/ai_commander/enhanced_commander/intelligent_claude_commander.py', 'r') as f:
    content = f.read()

# Update the prompt for better service detection
new_prompt = '''prompt = f"""You are a professional AI concierge for PRISM AI Platform.

Customer: {customer_name}
Request: "{request}"

IMPORTANT: Detect the PRIMARY SERVICE they need:
- translation: if they need document/content translation between languages
- video_creation: if they want to create/generate videos from content  
- podcast_generation: if they want to create podcasts/audio content
- education_module: if they need educational content/lessons/courses
- general_inquiry: ONLY if none of the above match

Please provide:
1. A warm greeting in the same language as request (1-2 sentences)
2. Service detection with these exact values
3. Your confidence level (0.0-1.0)
4. Main keywords from their request
5. Language: vi or en
6. Complexity: simple, moderate, or complex

Focus on what they WANT TO CREATE, not just general questions."""'''

# Replace the old prompt
content = re.sub(
    r'prompt = f"""You are a professional.*?You can respond in any format - natural text, JSON, or mixed\."""',
    new_prompt,
    content,
    flags=re.DOTALL
)

# Write back
with open('src/ai_commander/enhanced_commander/intelligent_claude_commander.py', 'w') as f:
    f.write(content)

print("✅ Fixed service detection prompt")
