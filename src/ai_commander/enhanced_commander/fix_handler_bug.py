import re

# Read handler file
with open('claude_response_handler.py', 'r') as f:
    content = f.read()

# Fix the parse_intent_response method
new_parse_method = '''    @staticmethod
    def parse_intent_response(response_text: str) -> Tuple[str, Dict[str, Any]]:
        """Parse intent analysis response"""
        
        # Extract greeting (usually first line or after "Greeting:")
        greeting = ""
        if "Greeting:" in response_text:
            match = re.search(r'Greeting:\s*([^\n]+)', response_text)
            if match:
                greeting = match.group(1).strip()
        else:
            # First non-empty line
            lines = response_text.strip().split('\n')
            for line in lines:
                if line.strip() and not any(x in line.lower() for x in ['service', 'confidence', '{', '}']):
                    greeting = line.strip()
                    break
        
        # Extract service - IMPORTANT: Look for actual service names
        service = 'general_inquiry'  # default
        
        # Try different patterns
        service_patterns = [
            r'Service:\s*(\w+)',
            r'service:\s*(\w+)',
            r'"service":\s*"(\w+)"',
            r'service\s*=\s*(\w+)',
        ]
        
        for pattern in service_patterns:
            match = re.search(pattern, response_text, re.IGNORECASE)
            if match:
                found_service = match.group(1).lower()
                # Validate it's a real service
                valid_services = ['video_creation', 'podcast_generation', 'translation', 'education_module', 'general_inquiry']
                if found_service in valid_services:
                    service = found_service
                    break
        
        # Extract confidence
        confidence = 0.7
        conf_match = re.search(r'Confidence:\s*([\d.]+)', response_text, re.IGNORECASE)
        if conf_match:
            try:
                confidence = float(conf_match.group(1))
            except:
                pass
        
        # Extract language
        language = 'vi'
        lang_match = re.search(r'Language:\s*(\w+)', response_text, re.IGNORECASE)
        if lang_match:
            lang = lang_match.group(1).lower()
            if lang in ['en', 'vi']:
                language = lang
        
        # Build intent data
        intent = {
            'service': service,
            'confidence': confidence,
            'keywords': [],
            'language': language,
            'complexity': 'moderate'
        }
        
        return greeting, intent'''

# Replace the method
content = re.sub(
    r'@staticmethod\s+def parse_intent_response.*?return greeting, intent',
    new_parse_method,
    content,
    flags=re.DOTALL
)

# Write back
with open('claude_response_handler.py', 'w') as f:
    f.write(content)

print("✅ Fixed handler to properly parse service names")
