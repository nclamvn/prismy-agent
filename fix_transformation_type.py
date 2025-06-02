#!/usr/bin/env python3
"""
Fix TransformationType import in education_module_builder.py
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    content = f.read()

# Add TransformationType to the base_transformer import line
if "from .base_transformer import" in content and "TransformationType" not in content:
    content = content.replace(
        "from .base_transformer import (",
        "from .base_transformer import (\n    TransformationType,"
    )
    print("✅ Added TransformationType to imports")
else:
    print("ℹ️  TransformationType already imported or import pattern different")

# Write back
with open(file_path, 'w') as f:
    f.write(content)
