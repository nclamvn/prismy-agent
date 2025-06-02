#!/usr/bin/env python3
"""
Fix EOL string literal errors
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Fix line 236 (index 235)
for i in range(234, min(240, len(lines))):
    line = lines[i]
    if 'return f"=== MỤC TIÊU HỌC TẬP ===' in line and not line.rstrip().endswith('"'):
        # Close the string properly
        lines[i] = line.rstrip() + '\\n{enhanced_objectives}\\n"\n'
        print(f"✅ Fixed EOL at line {i+1}")

# Check for other unclosed strings
for i, line in enumerate(lines):
    if 'return f"' in line or 'return f\'' in line:
        # Count quotes
        if line.count('"') % 2 != 0 or line.count("'") % 2 != 0:
            if not line.rstrip().endswith('"') and not line.rstrip().endswith("'"):
                print(f"Found unclosed string at line {i+1}: {line.strip()[:50]}...")

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("\n✅ String literals fixed!")
