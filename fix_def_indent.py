#!/usr/bin/env python3
"""
Fix def indentation on line 172
"""

file_path = "src/infrastructure/content_transformation/education_module_builder.py"

with open(file_path, 'r') as f:
    lines = f.readlines()

# Fix line 172 (index 171)
if len(lines) > 171:
    # Line 172 should have exactly 4 spaces (class method indent)
    if 'def _extract_key_concepts' in lines[171]:
        lines[171] = '    def _extract_key_concepts(self, text: str) -> List[str]:\n'
        print("✅ Fixed line 172 indentation")

# Write back
with open(file_path, 'w') as f:
    f.writelines(lines)

print("✅ Def statement indentation fixed!")
