#!/usr/bin/env python3
"""
Add transformation workflow to claude_commander.py
"""

# Read current file
with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    content = f.read()

# Add new method after handle_customer_request
new_method = '''
    async def process_transformation_request(self, intent_result, req_result, customer_info):
        """Process content transformation based on customer requirements"""
        try:
            # Map intent to transformation type
            transformation_map = {
                "create_podcast": "podcast",
                "create_video": "video", 
                "create_education": "education"
            }
            
            trans_type = transformation_map.get(intent_result.primary_intent)
            if not trans_type:
                return None
                
            # Create transformation request
            from infrastructure.content_transformation.base_transformer import TransformationRequest
            trans_request = TransformationRequest(
                source_text=customer_info.get('content', ''),
                transformation_type=trans_type,
                target_audience=req_result.requirements.get('audience', 'general'),
                context=customer_info.get('context', '')
            )
            
            # Process with transformation manager
            result = await self.transformation_manager.transform_content(trans_request)
            return result
            
        except Exception as e:
            print(f"Transformation error: {e}")
            return None
'''

# Find position to insert (after handle_customer_request method)
import re
pattern = r'(async def handle_customer_request.*?return conversation)'
match = re.search(pattern, content, re.DOTALL)

if match:
    end_pos = match.end()
    content = content[:end_pos] + '\n' + new_method + content[end_pos:]
    
    with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
        f.write(content)
    print("✅ Added process_transformation_request method!")
else:
    print("❌ Could not find insertion point")
