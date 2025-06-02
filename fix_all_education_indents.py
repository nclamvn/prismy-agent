#!/usr/bin/env python3
"""
Fix ALL indentation issues in education_module_builder.py
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

fixed_lines = []
in_class = False
in_method = False
method_indent = 4  # Standard indent for class methods

for i, line in enumerate(lines):
    stripped = line.strip()
    
    # Track class definition
    if stripped.startswith('class EducationModuleBuilder'):
        in_class = True
        fixed_lines.append(line)
        continue
    
    # Fix method definitions
    if in_class and stripped.startswith('def ') and '(self' in stripped:
        # This is a class method - should have exactly 4 spaces
        fixed_lines.append('    ' + stripped + '\n')
        in_method = True
        print(f"Fixed method at line {i+1}: {stripped[:40]}...")
        continue
    
    # Fix docstrings after method definitions
    if in_method and stripped.startswith('"""') and line[0] != ' ':
        # Docstring should be indented 8 spaces (method body)
        fixed_lines.append('        ' + stripped + '\n')
        if stripped.endswith('"""'):
            in_method = False
        continue
    
    # Keep other lines as is
    fixed_lines.append(line)

# Write back
with open(file_path, 'w') as f:
    f.writelines(fixed_lines)

print("\n✅ Fixed all method indentations!")

# Now check for methods without body
print("\n🔍 Checking for methods without implementation...")
for i in range(len(fixed_lines) - 1):
    if fixed_lines[i].strip().endswith('"""') and fixed_lines[i+1].strip() and not fixed_lines[i+1].startswith(' '):
        print(f"Warning: Method at line {i} might need implementation")
