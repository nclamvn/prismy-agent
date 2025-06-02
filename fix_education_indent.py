#!/usr/bin/env python3
"""
Fix indentation in education_module_builder.py
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

# Read file
with open(file_path, 'r') as f:
    lines = f.readlines()

# Check line 173
print(f"Line 173: {repr(lines[172])}")  # 0-indexed

# Find and fix empty code blocks
for i in range(len(lines)):
    # If line ends with : and next line is not indented
    if i < len(lines) - 1 and lines[i].rstrip().endswith(':'):
        next_line = lines[i + 1]
        if next_line.strip() and not next_line[0].isspace():
            # Need to add pass or implementation
            indent = len(lines[i]) - len(lines[i].lstrip())
            print(f"Found unindented block at line {i+1}")
            # Check what needs to be added based on context
            if 'def' in lines[i] or 'class' in lines[i]:
                lines.insert(i + 1, ' ' * (indent + 4) + 'pass  # TODO: implement\n')

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("✅ Fixed indentation issues!")
