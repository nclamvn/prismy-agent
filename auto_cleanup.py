#!/usr/bin/env python3
"""
Auto cleanup script - Move backup/test/broken files to archive
"""
import os
import shutil
from pathlib import Path

# Create archive directory
archive_dir = Path("archive_cleanup")
archive_dir.mkdir(exist_ok=True)

# Read cleanup list
with open('cleanup_list.txt', 'r') as f:
    files_to_move = [line.strip() for line in f if line.strip()]

print(f"🧹 Found {len(files_to_move)} files to archive")

# Move files
moved_count = 0
for file_path in files_to_move:
    if os.path.exists(file_path):
        # Create subdirectory structure in archive
        relative_path = Path(file_path).relative_to('.')
        archive_path = archive_dir / relative_path
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Move file
        shutil.move(file_path, archive_path)
        moved_count += 1
        print(f"  Moved: {file_path} → {archive_path}")

print(f"\n✅ Moved {moved_count} files to {archive_dir}/")
print("💡 You can delete archive_cleanup/ after review")
