#!/usr/bin/env python3
"""
Fix ALL import paths in the project
"""
import os
from pathlib import Path

# Find all Python files in src/
python_files = []
for root, dirs, files in os.walk('src'):
    # Skip __pycache__ and .pyc files
    if '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py'):
            python_files.append(os.path.join(root, file))

print(f"🔍 Found {len(python_files)} Python files to check\n")

replacements = {
    "from core.": "from src.core.",
    "from infrastructure.": "from src.infrastructure.",
    "from application.": "from src.application.",
    "from ai_commander.": "from src.ai_commander.",
    "import core.": "import src.core.",
    "import infrastructure.": "import src.infrastructure.",
    "import application.": "import src.application.",
    "import ai_commander.": "import src.ai_commander.",
}

fixed_count = 0
for file_path in python_files:
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"✅ Fixed: {file_path}")
        fixed_count += 1

print(f"\n📊 Fixed {fixed_count} files")
print("✅ All imports updated to use 'src.' prefix")
