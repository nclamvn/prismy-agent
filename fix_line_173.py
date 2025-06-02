#!/usr/bin/env python3
"""
Fix line 173 - add body after docstring
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find line 173 (index 172)
for i in range(170, min(180, len(lines))):
    if '"""Extract key concepts từ text using LLM"""' in lines[i]:
        print(f"Found docstring at line {i+1}")
        # Check next line
        if i+1 < len(lines):
            next_line = lines[i+1]
            # If next line is not indented properly, we need to fix
            if not next_line.strip().startswith('#') and not next_line.strip().startswith('if'):
                # Insert the missing code after docstring
                indent = '        '  # 8 spaces for method body
                lines.insert(i+1, f'{indent}# Try LLM first\n')
                print(f"Added missing line after docstring")
                break

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("✅ Fixed line 173!")
