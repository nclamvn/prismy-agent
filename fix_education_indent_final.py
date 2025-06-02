#!/usr/bin/env python3
"""
Fix indentation in education_module_builder.py - def statement wrong indent
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    content = f.read()

# Fix the specific indentation issue
lines = content.split('\n')

# Find and fix line with wrong indentation
for i, line in enumerate(lines):
    if i == 172:  # Line 173 (0-indexed)
        # This def should be indented at class method level (4 spaces)
        if 'def _extract_key_concepts' in line:
            lines[i] = '    def _extract_key_concepts(self, text: str) -> List[str]:'
            print(f"✅ Fixed indentation for line {i+1}")

# Rejoin and save
content = '\n'.join(lines)

with open(file_path, 'w') as f:
    f.write(content)

print("✅ Fixed function definition indentation!")
