#!/usr/bin/env python3
"""
Final fix for education module builder
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    content = f.read()

# Find the _generate_module_header method and replace it completely
import re

# First, let's remove any corrupted version
lines = content.split('\n')
new_lines = []
skip_until = -1

for i, line in enumerate(lines):
    if i < skip_until:
        continue
        
    if 'def _generate_module_header' in line:
        # Add the corrected method
        new_lines.append('    def _generate_module_header(self, request: TransformationRequest, concepts: List[str]) -> str:')
        new_lines.append('        """Generate module header với metadata"""')
        new_lines.append('        topic = concepts[0] if concepts else "chủ đề"')
        new_lines.append('        ')
        new_lines.append('        header = f"=== MODULE GIÁO DỤC ===\\n"')
        new_lines.append('        header += f"Chủ đề: {topic}\\n"')
        new_lines.append('        header += f"Đối tượng: {request.target_audience.value}\\n"')
        new_lines.append('        header += f"Độ khó: {request.difficulty_level.value}\\n\\n"')
        new_lines.append('        ')
        new_lines.append('        return header')
        new_lines.append('')
        
        # Skip until we find the next method
        j = i + 1
        while j < len(lines) and not (lines[j].strip().startswith('def ') and lines[j].strip() != 'def '):
            j += 1
        skip_until = j
        continue
    
    new_lines.append(line)

# Write clean version
with open(file_path, 'w') as f:
    f.write('\n'.join(new_lines))

print("✅ Education module cleaned and fixed!")
