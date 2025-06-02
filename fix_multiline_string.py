#!/usr/bin/env python3
"""
Fix multi-line string format issues
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

# Read entire file
with open(file_path, 'r') as f:
    content = f.read()

# Fix the multi-line f-string starting around line 161
# Replace the problematic section
old_pattern = '''return f"""=== MODULE GIÁO DỤC ===
{content}"""'''

new_pattern = '''return f"""=== MODULE GIÁO DỤC ===
Chủ đề: {topic}
Đối tượng: {request.target_audience.value}
Độ khó: {request.difficulty_level.value}

{content}"""'''

# Try to fix by finding and replacing the pattern
if 'return f"""=== MODULE GIÁO DỤC ===' in content:
    # Find the start and end of this return statement
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if 'return f"""=== MODULE GIÁO DỤC ===' in line:
            # Find the closing """
            j = i + 1
            while j < len(lines) and '"""' not in lines[j]:
                j += 1
            
            # Replace this section
            indent = '        '  # 8 spaces for method body
            new_lines = [
                f'{indent}return f"""=== MODULE GIÁO DỤC ===',
                f'{indent}Chủ đề: {{topic}}',
                f'{indent}Đối tượng: {{request.target_audience.value}}',
                f'{indent}Độ khó: {{request.difficulty_level.value}}',
                f'{indent}',
                f'{indent}{{content}}"""'
            ]
            
            # Replace lines i to j
            lines[i:j+1] = new_lines
            print(f"✅ Fixed multi-line f-string at line {i+1}")
            break
    
    content = '\n'.join(lines)

# Write back
with open(file_path, 'w') as f:
    f.write(content)

print("✅ Multi-line string fixed!")
