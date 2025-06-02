#!/usr/bin/env python3
"""
Fix claude_commander.py initialization - Version 2
"""

with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    lines = f.readlines()

# Find and add after self.adaptive_learner
new_lines = []
added = False

for i, line in enumerate(lines):
    new_lines.append(line)
    
    # Add after adaptive_learner initialization
    if not added and 'self.adaptive_learner = AdaptiveLearner()' in line:
        new_lines.append('        \n')
        new_lines.append('        # Initialize content transformation\n')
        new_lines.append('        self.transformation_manager = TransformationManager()\n')
        added = True

# Write back
with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
    f.writelines(new_lines)

if added:
    print("✅ Successfully added transformation_manager initialization!")
else:
    print("❌ Could not find where to add initialization")
