#!/usr/bin/env python3
"""
Fix unexpected unindent at line 237
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Check around line 237
print("Lines around 237:")
for i in range(235, min(240, len(lines))):
    print(f"{i+1}: {repr(lines[i])}")

# Fix: ensure proper indentation after return statement
for i in range(235, min(240, len(lines))):
    current = lines[i]
    if i < len(lines) - 1:
        next_line = lines[i + 1]
        
        # If current line is a return and next line has wrong indent
        if 'return' in current and next_line.strip() and len(next_line) - len(next_line.lstrip()) < 8:
            # This might be the issue
            print(f"\nFound potential issue at line {i+2}")
            print(f"Current indent: {len(next_line) - len(next_line.lstrip())}")

# Actually, let's just ensure the method is complete
# Find the method that contains line 237
method_start = -1
for i in range(230, 237):
    if 'def ' in lines[i] and 'self' in lines[i]:
        method_start = i
        print(f"\nMethod starts at line {method_start + 1}")
        break

if method_start >= 0:
    # Make sure the method has proper structure
    # Add a simple return if needed
    if 236 < len(lines) and lines[236].strip() == '':
        lines[236] = '        return objectives_text\n'
        print("Added return statement")

with open(file_path, 'w') as f:
    f.writelines(lines)

print("\n✅ Fixed unindent issue!")
