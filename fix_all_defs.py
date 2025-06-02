#!/usr/bin/env python3
"""
Fix ALL method definitions in education_module_builder.py
"""
import re

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    content = f.read()

# Split into lines
lines = content.split('\n')

# Fix all method definitions to have exactly 4 spaces
fixed_lines = []
for i, line in enumerate(lines):
    # Check if it's a method definition
    if re.search(r'^\s*def\s+\w+.*\(.*self', line):
        # This is a class method, should have exactly 4 spaces
        stripped = line.strip()
        fixed_line = '    ' + stripped  # 4 spaces
        fixed_lines.append(fixed_line)
        if line != fixed_line:
            print(f"Fixed line {i+1}: {stripped[:50]}...")
    else:
        fixed_lines.append(line)

# Join back
content = '\n'.join(fixed_lines)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("\n✅ Fixed all method definitions!")
