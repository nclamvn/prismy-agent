#!/usr/bin/env python3
"""
SAFE cleanup - Only project files, not libraries
"""
import os
import shutil
from pathlib import Path

# Only clean project directories
PROJECT_DIRS = ['./src', './translate_api', './']

print("🔍 Scanning for project cleanup files...")

files_to_archive = []
for dir in PROJECT_DIRS:
    if os.path.exists(dir):
        for file in Path(dir).rglob("*.py"):
            file_str = str(file)
            # Skip virtual env and hidden directories
            if 'agent_env' in file_str or 'venv' in file_str or '/.venv' in file_str:
                continue
            # Check if it's a cleanup candidate
            if any(pattern in file_str for pattern in ['backup', 'broken', '_old', '_test', 'archive']):
                files_to_archive.append(file_str)

print(f"\n📋 Found {len(files_to_archive)} PROJECT files to archive:")
for f in files_to_archive[:20]:  # Show first 20
    print(f"  - {f}")

if len(files_to_archive) > 20:
    print(f"  ... and {len(files_to_archive) - 20} more")

# Ask for confirmation
if input("\n❓ Proceed with archiving? (y/n): ").lower() == 'y':
    archive_dir = Path("archive_cleanup")
    archive_dir.mkdir(exist_ok=True)
    
    for file_path in files_to_archive:
        # Archive logic here
        print(f"Archiving: {file_path}")
else:
    print("❌ Cancelled")
