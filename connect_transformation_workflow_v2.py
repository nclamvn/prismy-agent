#!/usr/bin/env python3
"""
Connect transformation workflow - Version 2
"""

with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    content = f.read()

# Find the workflow orchestration call
import re

# Add transformation processing after workflow orchestration
addition = '''
        # Process content transformation if applicable
        if workflow_result.success and hasattr(self, 'transformation_manager'):
            trans_result = await self.process_transformation_request(
                intent_result, 
                req_result,
                {'content': customer_input, 'context': content}
            )
            if trans_result:
                workflow_result.output_data['transformation_result'] = trans_result
'''

# Find pattern: workflow_result = await self.workflow_orchestrator.orchestrate_workflow(
pattern = r'(workflow_result = await self\.workflow_orchestrator\.orchestrate_workflow\([^)]+\))'
match = re.search(pattern, content)

if match:
    end_pos = match.end()
    # Find the next line break
    next_newline = content.find('\n', end_pos)
    if next_newline != -1:
        content = content[:next_newline] + '\n' + addition + content[next_newline:]
        
        with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
            f.write(content)
        print("✅ Connected transformation workflow!")
        print("📋 Added transformation processing after workflow orchestration")
        print("🎯 AI Commander now integrates with TransformationManager!")
else:
    # Try to see what's around line 167
    lines = content.split('\n')
    print("❌ Pattern not found. Line 167 area:")
    for i in range(165, 170):
        if i < len(lines):
            print(f"{i}: {lines[i]}")
