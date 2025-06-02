#!/usr/bin/env python3
"""
Fix import paths to use absolute imports from src
"""
import os
from pathlib import Path

files_to_fix = [
    "src/application/services/translation_service.py",
    "src/application/services/enhanced_translation_service.py"
]

replacements = {
    "from core.": "from src.core.",
    "from infrastructure.": "from src.infrastructure.",
    "from application.": "from src.application.",
    "import core.": "import src.core.",
    "import infrastructure.": "import src.infrastructure.",
    "import application.": "import src.application.",
}

for file_path in files_to_fix:
    if not Path(file_path).exists():
        continue
        
    print(f"🔧 Fixing {file_path}")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    original = content
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    if content != original:
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"  ✅ Updated imports")
    else:
        print(f"  ℹ️  No changes needed")

print("\n✅ Import paths fixed!")
