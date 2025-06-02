#!/usr/bin/env python3
"""
Update claude_commander.py to integrate TransformationManager
"""

with open('src/ai_commander/enhanced_commander/claude_commander.py', 'r') as f:
    content = f.read()

# Add TransformationManager import
import_addition = """
# Content transformation integration
try:
    from infrastructure.content_transformation.transformation_manager import TransformationManager
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from infrastructure.content_transformation.transformation_manager import TransformationManager
"""

# Find where to insert (after adaptive_learning import)
import_pos = content.find("from adaptive_learning import AdaptiveLearner")
if import_pos != -1:
    end_of_line = content.find('\n', import_pos)
    content = content[:end_of_line+1] + import_addition + content[end_of_line+1:]

# Add transformation_manager to __init__
init_update = """        # Initialize content transformation
        self.transformation_manager = TransformationManager()
"""

# Find __init__ method
init_pos = content.find("self.learner = AdaptiveLearner()")
if init_pos != -1:
    end_of_line = content.find('\n', init_pos)
    content = content[:end_of_line+1] + init_update + content[end_of_line+1:]

# Save updated file
with open('src/ai_commander/enhanced_commander/claude_commander.py', 'w') as f:
    f.write(content)

print("✅ Updated claude_commander.py with TransformationManager!")
print("📋 Changes made:")
print("- Added TransformationManager import")
print("- Initialized transformation_manager in __init__")
