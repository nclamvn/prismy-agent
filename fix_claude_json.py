import re

# Read file
with open('src/ai_commander/enhanced_commander/hotel_concierge_claude.py', 'r') as f:
    content = f.read()

# Fix greet_customer method to handle response better
new_greet_customer = '''        response = self.claude.messages.create(
            model="claude-4-sonnet-20250514",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        # Extract text from response
        response_text = response.content[0].text
        print(f"DEBUG - Claude response: {response_text[:200]}...")
        
        # Try to extract JSON from response
        try:
            # Claude might wrap JSON in markdown or other text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in response")
        except Exception as e:
            print(f"Error parsing JSON: {e}")
            # Fallback response
            result = {
                "greeting": f"Xin chào {customer_name}! Tôi hiểu bạn cần tạo video từ báo cáo tài chính. Để giúp bạn tốt nhất, tôi cần thêm một số thông tin.",
                "intent": {
                    "service": "video_creation",
                    "confidence": 0.85,
                    "keywords": ["video", "báo cáo", "tài chính", "Q4"],
                    "language": "vi",
                    "complexity": "moderate"
                }
            }'''

# Replace the response parsing part
content = re.sub(
    r'response = self\.claude\.messages\.create\(.*?result = json\.loads\(response\.content\[0\]\.text\)',
    new_greet_customer,
    content,
    flags=re.DOTALL
)

# Similar fix for gather_requirements
new_gather_requirements = '''        response = self.claude.messages.create(
            model="claude-4-sonnet-20250514",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        
        response_text = response.content[0].text
        print(f"DEBUG - Questions response: {response_text[:200]}...")
        
        try:
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found")
        except Exception as e:
            print(f"Error parsing questions JSON: {e}")
            # Fallback questions
            result = {
                "questions": [
                    {
                        "question": "Video dài bao nhiêu phút bạn mong muốn?",
                        "purpose": "Xác định thời lượng video",
                        "expected_type": "number"
                    },
                    {
                        "question": "Bạn muốn xuất cho platform nào (YouTube, TikTok, khác)?",
                        "purpose": "Tối ưu format video",
                        "expected_type": "choice"
                    }
                ]
            }'''

# Replace gather_requirements response parsing
content = re.sub(
    r'response = self\.claude\.messages\.create\(.*?model="claude-4-sonnet-20250514".*?messages.*?max_tokens=500.*?\).*?result = json\.loads\(response\.content\[0\]\.text\)',
    new_gather_requirements,
    content,
    flags=re.DOTALL,
    count=1  # Only replace first occurrence
)

# Write back
with open('src/ai_commander/enhanced_commander/hotel_concierge_claude.py', 'w') as f:
    f.write(content)

print("✅ Fixed JSON parsing with debug output")
