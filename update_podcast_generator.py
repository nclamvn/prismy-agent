import re

# Read the podcast generator file
with open('src/infrastructure/content_transformation/podcast_generator.py', 'r') as f:
    content = f.read()

# Add import for quality enhancer
import_section = """from typing import Dict, List, Any
from .base_transformer import (
    BaseContentTransformer,
    TransformationType,
    TargetAudience, 
    ContentDifficulty,
    TransformationRequest,
    TransformationResponse
)
from ..ai_intelligence.quality_enhancer import QualityEnhancer"""

# Replace the import section
content = re.sub(
    r'from typing import.*?\n.*?TransformationResponse\s*\)',
    import_section,
    content,
    flags=re.DOTALL
)

# Add quality enhancer initialization in __init__
init_addition = '''
    def __init__(self):
        """Initialize Podcast Generator with AI enhancement"""
        super().__init__(TransformationType.PODCAST)
        self.quality_enhancer = QualityEnhancer()
'''

# Find and replace the __init__ method or add if not exists
if 'def __init__' not in content:
    # Add after class definition
    content = re.sub(
        r'(class PodcastGenerator.*?:.*?\n)',
        r'\1' + init_addition,
        content,
        flags=re.DOTALL
    )

# Write back
with open('src/infrastructure/content_transformation/podcast_generator.py', 'w') as f:
    f.write(content)

print("✅ Updated podcast_generator.py with quality enhancer import")
