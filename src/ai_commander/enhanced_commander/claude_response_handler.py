"""
Smart Claude Response Handler - Extract structured data from any Claude response
"""

import json
import re
from typing import Dict, Any, Optional, Tuple


class ClaudeResponseHandler:
    """
    Intelligent handler for Claude responses
    Extracts structured data regardless of response format
    """
    
    @staticmethod
    def extract_json(response_text: str) -> Optional[Dict[str, Any]]:
        """Extract JSON from Claude response"""
        
        # Method 1: Try direct JSON parse
        try:
            return json.loads(response_text)
        except:
            pass
        
        # Method 2: Find JSON block in markdown
        json_patterns = [
            r'```json\s*(.*?)\s*```',  # ```json ... ```
            r'```\s*(.*?)\s*```',       # ``` ... ```
            r'\{[^{}]*\{[^{}]*\}[^{}]*\}',  # Nested JSON
            r'\{[^{}]*\}'               # Simple JSON
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, response_text, re.DOTALL)
            for match in matches:
                try:
                    return json.loads(match)
                except:
                    continue
        
        return None
    
    @staticmethod
    def extract_structured_data(response_text: str, expected_fields: list) -> Dict[str, Any]:
        """Extract structured data based on expected fields"""
        
        result = {}
        
        # Try JSON first
        json_data = ClaudeResponseHandler.extract_json(response_text)
        if json_data:
            return json_data
        
        # Extract by patterns
        for field in expected_fields:
            # Common patterns for field extraction
            patterns = [
                rf'{field}:\s*"([^"]+)"',          # field: "value"
                rf'{field}:\s*([^\n,]+)',          # field: value
                rf'"{field}":\s*"([^"]+)"',        # "field": "value"
                rf'{field}\s*=\s*"([^"]+)"',       # field = "value"
                rf'{field}\s*-\s*([^\n]+)',        # field - value
            ]
            
            for pattern in patterns:
                match = re.search(pattern, response_text, re.IGNORECASE)
                if match:
                    result[field] = match.group(1).strip()
                    break
        
        return result
    
    @staticmethod
    def parse_intent_response(response_text: str) -> Tuple[str, Dict[str, Any]]:
        """Parse intent analysis response"""
        
        # Extract greeting
        greeting = ""
        if "Greeting:" in response_text:
            match = re.search(r'Greeting:\s*([^\n]+)', response_text)
            if match:
                greeting = match.group(1).strip()
        else:
            # First non-empty line
            lines = response_text.strip().split('\n')
            for line in lines:
                if line.strip() and not any(x in line.lower() for x in ['service', 'confidence']):
                    greeting = line.strip()
                    break
        
        # Extract service - CRITICAL FIX
        service = 'general_inquiry'
        
        # Look for service mentions
        service_match = re.search(r'Service:\s*(\w+)', response_text, re.IGNORECASE)
        if service_match:
            found_service = service_match.group(1).lower()
            # Validate service name
            valid_services = ['video_creation', 'podcast_generation', 'translation', 'education_module', 'general_inquiry']
            if found_service in valid_services:
                service = found_service
        
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
        
        # Build intent
        intent = {
            'service': service,
            'confidence': confidence,
            'keywords': [],
            'language': language,
            'complexity': 'moderate'
        }
        
        return greeting, intent
    
    @staticmethod
    def parse_questions_response(response_text: str) -> list:
        """Parse questions response"""
        
        questions = []
        
        # Try JSON extraction first
        json_data = ClaudeResponseHandler.extract_json(response_text)
        if json_data and 'questions' in json_data:
            return json_data['questions']
        
        # Pattern matching for questions
        question_patterns = [
            r'\d+\.\s*([^\n]+)',           # 1. Question
            r'[-*]\s*([^\n]+)',            # - Question or * Question
            r'Question \d+:\s*([^\n]+)',   # Question 1: ...
            r'Q\d+:\s*([^\n]+)',           # Q1: ...
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, response_text)
            if matches:
                for match in matches[:3]:  # Max 3 questions
                    questions.append({
                        'question': match.strip(),
                        'purpose': 'Gather requirements',
                        'expected_type': 'text'
                    })
                break
        
        return questions


# Test the handler
if __name__ == "__main__":
    test_responses = [
        """
        Greeting: Xin chào! Tôi sẽ giúp bạn tạo video.
        Service: video_creation
        Confidence: 0.9
        Language: vi
        """,
        
        """
        Xin chào anh Minh!
        
        Service: podcast_generation
        Confidence: 0.85
        """,
    ]
    
    handler = ClaudeResponseHandler()
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n--- Test {i} ---")
        greeting, intent = handler.parse_intent_response(response)
        print(f"Service: {intent['service']}")
        print(f"Greeting: {greeting}")
