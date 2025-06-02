import re

# Read file
with open('intelligent_claude_commander.py', 'r') as f:
    content = f.read()

# Add more explicit examples in prompt
better_prompt = '''prompt = f"""You are a professional AI concierge for PRISM AI Platform.

Customer: {customer_name}
Request: "{request}"

CRITICAL SERVICE DETECTION:
- video_creation: Keywords like "video", "clip", "visual", "youtube", "tiktok", "phim", "tạo video"
- podcast_generation: Keywords like "podcast", "audio", "episode", "radio"
- translation: Keywords like "dịch", "translate", "ngôn ngữ", "language"
- education_module: Keywords like "lesson", "course", "education", "bài giảng", "khóa học"
- general_inquiry: ONLY if absolutely none of the above

For this request, detect if they want to CREATE content (video/podcast/education) or just asking questions.

Example: "Tôi cần tạo video" -> video_creation
Example: "Create video from report" -> video_creation

Please provide:
1. A warm greeting in same language (1-2 sentences)
2. The PRIMARY service they need (be specific!)
3. Confidence level (0.0-1.0)
4. Keywords that helped you decide
5. Language: vi or en
6. Complexity: simple, moderate, or complex"""'''

# Replace prompt
content = re.sub(
    r'prompt = f"""You are a professional.*?Focus on what they WANT TO CREATE, not just general questions\."""',
    better_prompt,
    content,
    flags=re.DOTALL
)

# Also improve fallback detection
better_fallback = '''    def _fallback_greeting(self, customer_name: str, request: str) -> Tuple[str, CustomerIntent]:
        """Fallback when API unavailable"""
        request_lower = request.lower()
        
        # More comprehensive keyword matching
        if any(word in request_lower for word in ['video', 'clip', 'visual', 'youtube', 'tiktok', 'phim', 'tạo video']):
            service = ServiceType.VIDEO_CREATION
        elif any(word in request_lower for word in ['podcast', 'audio', 'episode', 'radio']):
            service = ServiceType.PODCAST_GENERATION
        elif any(word in request_lower for word in ['dịch', 'translate', 'translation', 'ngôn ngữ']):
            service = ServiceType.TRANSLATION
        elif any(word in request_lower for word in ['education', 'giáo dục', 'lesson', 'bài giảng', 'course']):
            service = ServiceType.EDUCATION_MODULE
        else:
            service = ServiceType.GENERAL_INQUIRY
        
        # Better greeting based on detected service
        greetings = {
            ServiceType.VIDEO_CREATION: f"Xin chào {customer_name}! Tôi sẽ giúp bạn tạo video chuyên nghiệp.",
            ServiceType.PODCAST_GENERATION: f"Hi {customer_name}! I'll help you create an engaging podcast.",
            ServiceType.TRANSLATION: f"Xin chào {customer_name}! Tôi sẽ hỗ trợ dịch thuật cho bạn.",
            ServiceType.GENERAL_INQUIRY: f"Xin chào {customer_name}! Tôi sẵn sàng hỗ trợ bạn."
        }
        
        greeting = greetings.get(service, greetings[ServiceType.GENERAL_INQUIRY])'''

# Replace fallback method
content = re.sub(
    r'def _fallback_greeting\(self.*?\n.*?""".*?""".*?return greeting, intent',
    better_fallback + '\n        \n        intent = CustomerIntent(\n            primary_service=service,\n            confidence=0.8 if service != ServiceType.GENERAL_INQUIRY else 0.5,\n            keywords=[w for w in request.split() if len(w) > 2][:5],\n            language=\'vi\' if any(ord(c) > 127 for c in request) else \'en\',\n            complexity=\'moderate\'\n        )\n        \n        return greeting, intent',
    content,
    flags=re.DOTALL
)

# Write back
with open('intelligent_claude_commander.py', 'w') as f:
    f.write(content)

print("✅ Improved video detection")
