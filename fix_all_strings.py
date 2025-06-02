#!/usr/bin/env python3
"""
Fix ALL unclosed string literals
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Fix specific lines
fixes = {
    160: 'return f"""=== MODULE GIÁO DỤC ===\n{content}"""\n',  # Line 161 (index 160)
    254: 'objectives_text += f"{i}. {objective}\\n"\n',  # Line 255 (index 254)
}

for line_idx, fix in fixes.items():
    if len(lines) > line_idx:
        old_line = lines[line_idx].strip()
        lines[line_idx] = '        ' + fix  # Add proper indentation
        print(f"✅ Fixed line {line_idx + 1}: {old_line[:40]}...")

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("\n✅ All string literals fixed!")
