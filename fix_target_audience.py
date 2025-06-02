#!/usr/bin/env python3
"""
Fix TargetAudience import in intelligence_orchestrator.py
"""

file_path = "src/infrastructure/ai_intelligence/intelligence_orchestrator.py"

# Read file
with open(file_path, 'r') as f:
    lines = f.readlines()

# Find where to add import (after other imports)
import_added = False
new_lines = []

for i, line in enumerate(lines):
    new_lines.append(line)
    
    # Add import after the last 'from' or 'import' line in the header
    if not import_added and i < 50 and line.strip() and not line.startswith('from') and not line.startswith('import'):
        # Check if previous lines had imports
        if any('import' in lines[j] for j in range(max(0, i-5), i)):
            new_lines.insert(-1, "from src.infrastructure.content_transformation.base_transformer import TargetAudience\n")
            import_added = True
            print(f"✅ Added TargetAudience import at line {i}")

# Write back
with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("✅ Fixed TargetAudience import!")
