#!/usr/bin/env python3
"""
Fix line 167 syntax error
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find and fix the problematic line
for i in range(165, min(170, len(lines))):
    if 'Chủ đề:' in lines[i] and '{topic}' in lines[i]:
        # This line needs proper f-string formatting
        # It should be inside an f-string
        lines[i] = '        Chủ đề: {topic}\n'
        print(f"✅ Fixed line {i+1}")

# Find the f-string start and ensure it's properly formatted
for i in range(160, min(170, len(lines))):
    if 'return f"""' in lines[i]:
        # Rebuild this entire f-string properly
        j = i
        # Find the end
        while j < len(lines) and '"""' not in lines[j][10:]:  # Skip the opening """
            j += 1
        
        # Replace with proper format
        lines[i] = '        return f"""=== MODULE GIÁO DỤC ===\n'
        lines[i+1] = 'Chủ đề: {topic}\n'
        lines[i+2] = 'Đối tượng: {request.target_audience.value}\n'  
        lines[i+3] = 'Độ khó: {request.difficulty_level.value}\n'
        lines[i+4] = '\n'
        lines[i+5] = '{content}"""\n'
        print(f"✅ Rebuilt f-string from line {i+1}")
        break

with open(file_path, 'w') as f:
    f.writelines(lines)

print("✅ Fixed!")
