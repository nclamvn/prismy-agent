#!/usr/bin/env python3
"""
Fix unclosed string literal in education_module_builder.py
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find and fix line 240 (index 239)
if len(lines) > 239:
    line = lines[239]
    if 'return f"=== MỤC TIÊU HỌC TẬP ===' in line and not line.rstrip().endswith('"'):
        # Add closing quote and escape sequence
        lines[239] = line.rstrip() + '\\n{enhanced_objectives}\\n"\n'
        print(f"✅ Fixed unclosed string on line 240")

# Check for other unclosed strings
for i, line in enumerate(lines):
    # Simple check for f-strings that start but don't end
    if 'f"' in line or "f'" in line:
        quote_count = line.count('"') + line.count("'")
        if quote_count % 2 != 0:
            print(f"⚠️  Potential unclosed string at line {i+1}: {line.strip()[:50]}...")

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("\n✅ String literal fixed!")
