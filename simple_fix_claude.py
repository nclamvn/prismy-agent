import re

# Read file
with open('src/ai_commander/enhanced_commander/hotel_concierge_claude.py', 'r') as f:
    content = f.read()

# Add import re at top if not exists
if 'import re' not in content:
    content = content.replace('import json', 'import json\nimport re')

# Fix the JSON parsing in greet_customer
old_parse = 'result = json.loads(response.content[0].text)'
new_parse = '''try:
            response_text = response.content[0].text
            # Try to find JSON in response
            json_match = re.search(r'\\{.*\\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # Fallback if no JSON found
                result = {
                    "greeting": f"Xin chào {customer_name}! Tôi hiểu bạn cần: {initial_request}",
                    "intent": {
                        "service": "video_creation",
                        "confidence": 0.8,
                        "keywords": initial_request.split()[:5],
                        "language": "vi",
                        "complexity": "moderate"
                    }
                }
        except Exception as e:
            print(f"JSON parse error: {e}")
            result = {
                "greeting": f"Xin chào {customer_name}!",
                "intent": {
                    "service": "general_inquiry",
                    "confidence": 0.5,
                    "keywords": [],
                    "language": "vi",
                    "complexity": "simple"
                }
            }'''

# Replace with proper indentation
content = content.replace('        ' + old_parse, '        ' + new_parse)

# Write back
with open('src/ai_commander/enhanced_commander/hotel_concierge_claude.py', 'w') as f:
    f.write(content)

print("✅ Fixed JSON parsing")
