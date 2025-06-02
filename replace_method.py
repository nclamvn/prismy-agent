#!/usr/bin/env python3
"""
Replace the problematic method entirely
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    content = f.read()

# Simple working version of the method
new_method = '''    def _generate_module_header(self, request: TransformationRequest, concepts: List[str]) -> str:
        """Generate module header với metadata"""
        topic = concepts[0] if concepts else "chủ đề"
        
        header = f"=== MODULE GIÁO DỤC ===\\n"
        header += f"Chủ đề: {topic}\\n"
        header += f"Đối tượng: {request.target_audience.value}\\n"
        header += f"Độ khó: {request.difficulty_level.value}\\n"
        
        return header
'''

# Find and replace the method
import re
pattern = r'def _generate_module_header\(self.*?\n.*?""".*?""".*?return.*?"""'
if re.search(pattern, content, re.DOTALL):
    content = re.sub(pattern, new_method.strip(), content, flags=re.DOTALL)
    print("✅ Replaced entire method with working version")

with open(file_path, 'w') as f:
    f.write(content)
