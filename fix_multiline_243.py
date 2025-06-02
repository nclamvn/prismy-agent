#!/usr/bin/env python3
"""
Fix multi-line string at line 243
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find and fix the multi-line string starting at line 243
for i in range(240, min(250, len(lines))):
    if 'objectives_text = "=== MỤC TIÊU HỌC TẬP ===' in lines[i]:
        # Replace with proper string
        lines[i] = '        objectives_text = "=== MỤC TIÊU HỌC TẬP ===\\n"\n'
        lines[i+1] = '        objectives_text += "Sau khi hoàn thành module này, học viên sẽ có thể:\\n\\n"\n'
        print(f"Fixed multi-line string at line {i+1}")
        break

with open(file_path, 'w') as f:
    f.writelines(lines)

print("✅ Fixed multi-line string!")
