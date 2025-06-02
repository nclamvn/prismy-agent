#!/usr/bin/env python3
"""
Fix sys.path.append to proper imports
"""
import re
from pathlib import Path

# Read files that need fixing
with open('project_fix_imports.txt', 'r') as f:
    files_to_fix = [line.strip() for line in f if line.strip() and '.venv' not in line and 'agent_env' not in line]

print(f"🔧 Fixing imports in {len(files_to_fix)} files...\n")

for file_path in files_to_fix:
    if not Path(file_path).exists():
        continue
        
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Count sys.path.append occurrences
    count = content.count('sys.path.append')
    if count > 0:
        print(f"📄 {file_path}: {count} sys.path.append found")
        
        # Show the lines with sys.path.append
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'sys.path.append' in line:
                print(f"   Line {i+1}: {line.strip()}")

print("\n💡 Manual review needed - imports are context-specific")
print("Consider using relative imports or updating PYTHONPATH instead")
