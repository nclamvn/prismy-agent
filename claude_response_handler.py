"""
Smart Claude Response Handler - Extract structured data from any Claude response
"""

import json
import re
from typing import Dict, Any, Optional, Tuple
import yaml


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
        
        # Method 3: Try YAML format
        try:
            # Claude sometimes returns YAML-like format
            yaml_text = response_text
            # Remove markdown code blocks
            yaml_text = re.sub(r'```.*?```', '', yaml_text, flags=re.DOTALL)
            data = yaml.safe_load(yaml_text)
            if isinstance(data, dict):
                return data
        except:
            pass
        
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
        
        # Extract greeting (usually first paragraph)
        lines = response_text.strip().split('\n')
        greeting = ""
        for line in lines:
            if line.strip() and not any(x in line.lower() for x in ['json', 'intent', 'service', '{', '}']):
                greeting = line.strip()
                break
        
        # Try to extract intent data
        intent_data = ClaudeResponseHandler.extract_structured_data(
            response_text,
            ['service', 'confidence', 'keywords', 'language', 'complexity']
        )
        
        # Provide defaults if missing
        intent = {
            'service': intent_data.get('service', 'general_inquiry'),
            'confidence': float(intent_data.get('confidence', 0.7)),
            'keywords': intent_data.get('keywords', []),
            'language': intent_data.get('language', 'vi'),
            'complexity': intent_data.get('complexity', 'moderate')
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
        # Look for numbered questions
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


# Example usage
if __name__ == "__main__":
    # Test with various Claude response formats
    test_responses = [
        # Format 1: Clean JSON
        '{"greeting": "Xin chào!", "intent": {"service": "video_creation", "confidence": 0.9}}',
        
        # Format 2: Markdown with JSON
        '''
        Xin chào Anh Minh! Tôi sẽ giúp anh tạo video.
        
        ```json
        {
            "intent": {
                "service": "video_creation",
                "confidence": 0.85
            }
        }
        ```
        ''',
        
        # Format 3: Natural text
        '''
        Chào anh Minh! Tôi hiểu anh cần tạo video từ báo cáo tài chính.
        
        Service: video_creation
        Confidence: 0.9
        Language: Vietnamese
        Complexity: moderate
        ''',
        
        # Format 4: Mixed format
        '''
        Greeting: "Xin chào anh!"
        
        Intent analysis:
        - service = "podcast_generation"
        - confidence = 85%
        - keywords = ["podcast", "AI", "healthcare"]
        '''
    ]
    
    handler = ClaudeResponseHandler()
    
    for i, response in enumerate(test_responses, 1):
        print(f"\n--- Test {i} ---")
        print(f"Response: {response[:100]}...")
        
        greeting, intent = handler.parse_intent_response(response)
        print(f"Extracted greeting: {greeting}")
        print(f"Extracted intent: {intent}")
