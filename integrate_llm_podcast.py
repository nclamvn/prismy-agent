import re

# Read podcast generator
with open('src/infrastructure/content_transformation/podcast_generator.py', 'r') as f:
    content = f.read()

# Add imports
new_imports = """import time
import re
from typing import Dict, List, Any
from .base_transformer import (
    BaseContentTransformer,
    TransformationType,
    TargetAudience, 
    ContentDifficulty,
    TransformationRequest,
    TransformationResponse
)
from ..ai_intelligence.llm_service import get_llm_service"""

# Replace imports
content = re.sub(
    r'import time.*?from \.base_transformer.*?\)',
    new_imports,
    content,
    flags=re.DOTALL
)

# Add init method with LLM
init_code = '''
    def __init__(self):
        """Initialize with LLM enhancement"""
        super().__init__(TransformationType.PODCAST)
        self.llm_service = get_llm_service()
'''

# Add after class definition
if 'def __init__' not in content:
    content = re.sub(
        r'(class PodcastGenerator.*?""".*?""")',
        r'\1\n' + init_code,
        content,
        flags=re.DOTALL
    )

# Write back
with open('src/infrastructure/content_transformation/podcast_generator.py', 'w') as f:
    f.write(content)

print("✅ Integrated LLM into podcast_generator.py")
