#!/usr/bin/env python3
"""
Fix TransformationType import in intelligence_orchestrator.py
"""

file_path = "src/infrastructure/ai_intelligence/intelligence_orchestrator.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find where TargetAudience is imported and add TransformationType to same line
fixed = False
for i, line in enumerate(lines):
    if 'from src.infrastructure.content_transformation.base_transformer import TargetAudience' in line:
        lines[i] = 'from src.infrastructure.content_transformation.base_transformer import TargetAudience, TransformationType\n'
        fixed = True
        print(f"✅ Added TransformationType to import on line {i+1}")
        break

if not fixed:
    # Add as new import if not found
    for i, line in enumerate(lines):
        if 'from src.infrastructure.content_transformation.base_transformer' in line:
            lines.insert(i+1, 'from src.infrastructure.content_transformation.base_transformer import TransformationType\n')
            fixed = True
            print(f"✅ Added TransformationType import after line {i+1}")
            break

if fixed:
    with open(file_path, 'w') as f:
        f.writelines(lines)
else:
    print("❌ Could not add import - manual fix needed")
