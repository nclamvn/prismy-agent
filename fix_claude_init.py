#!/usr/bin/env python3
"""
Fix claude_commander.py initialization
"""

with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    lines = f.readlines()

# Find __init__ method and add transformation_manager
new_lines = []
in_init = False
init_added = False

for i, line in enumerate(lines):
    new_lines.append(line)
    
    if 'def __init__(self):' in line:
        in_init = True
    
    # Add after self.learner = AdaptiveLearner()
    if in_init and not init_added and 'self.learner = AdaptiveLearner()' in line:
        new_lines.append('        # Initialize content transformation\n')
        new_lines.append('        self.transformation_manager = TransformationManager()\n')
        new_lines.append('\n')
        init_added = True

# Write back
with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Fixed initialization!")
print("- Added self.transformation_manager = TransformationManager()")
