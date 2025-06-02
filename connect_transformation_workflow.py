#!/usr/bin/env python3
"""
Connect transformation workflow in handle_customer_request
"""

with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    content = f.read()

# Find handle_customer_request method and add transformation call
import re

# Add transformation processing after workflow orchestration
addition = '''
        # Process content transformation if applicable
        if workflow_result.success and hasattr(self, 'transformation_manager'):
            trans_result = await self.process_transformation_request(
                intent_result, 
                req_result,
                {'content': customer_input, 'context': customer_context}
            )
            if trans_result:
                workflow_result.output_data['transformation_result'] = trans_result
'''

# Find position after workflow execution
pattern = r'(workflow_result = self\.workflow_orchestrator\.execute_workflow.*?\))'
match = re.search(pattern, content, re.DOTALL)

if match:
    end_pos = match.end()
    # Find the next line break
    next_newline = content.find('\n', end_pos)
    if next_newline != -1:
        content = content[:next_newline] + '\n' + addition + content[next_newline:]
        
        with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
            f.write(content)
        print("✅ Connected transformation workflow to handle_customer_request!")
        print("🎯 Now AI Commander will automatically process transformations!")
else:
    print("❌ Could not find workflow execution point")
