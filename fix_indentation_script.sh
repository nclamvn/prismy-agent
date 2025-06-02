#!/bin/bash

echo "🔧 FIXING INDENTATION ERRORS..."

# Backup file
cp app_ultra_modern_fixed.py app_ultra_modern_fixed_backup_$(date +%s).py
echo "✅ Created backup"

# 1. Fix function name calls
echo "🔄 Fixing function calls..."
sed -i 's/real_text_processing_pipeline_fixed_with_chunking/real_text_processing_pipeline_fixed_no_data_loss/g' app_ultra_modern_fixed.py
sed -i 's/SmartTextChunker(/SmartTextChunkerFixed(/g' app_ultra_modern_fixed.py  
sed -i 's/get_real_openai_translation_chunked(/get_real_openai_translation_chunked_fixed(/g' app_ultra_modern_fixed.py

# 2. Create Python script to fix the duplicate function
cat > fix_file.py << 'PYEOF'
import re

print("🧹 Cleaning up duplicate functions...")

# Read the file
with open('app_ultra_modern_fixed.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the duplicate clean_combined_text function by removing the broken one
lines = content.split('\n')
new_lines = []
skip_lines = False
in_clean_function = False

for i, line in enumerate(lines):
    # Detect start of problematic function
    if 'def clean_combined_text(text: str) -> str:' in line:
        if in_clean_function:
            # This is the second definition, skip it
            skip_lines = True
            continue
        else:
            in_clean_function = True
    
    # Skip lines until we find the end of the duplicate function
    if skip_lines:
        if line.strip() == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('def '):
            skip_lines = False
        elif line.strip() == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('# FUNCTION'):
            skip_lines = False
        elif line.strip() == '' and i + 1 < len(lines) and lines[i + 1].strip().startswith('class '):
            skip_lines = False
        continue
    
    # Remove problematic lines
    if line.strip() == 'if':
        continue
    if 'test_chunking_system()' in line and '__name__' not in lines[max(0, i-1)]:
        continue
        
    new_lines.append(line)

# Join back
content = '\n'.join(new_lines)

# Ensure proper main block at the end
if 'if __name__ == "__main__":' not in content.split('\n')[-10:]:
    content += '\n\nif __name__ == "__main__":\n    main()\n'

# Write back
with open('app_ultra_modern_fixed.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed Python syntax issues")
PYEOF

# Run the Python fix
python3 fix_file.py
rm fix_file.py

echo ""
echo "🎯 TESTING SYNTAX..."
python3 -m py_compile app_ultra_modern_fixed.py

if [ $? -eq 0 ]; then
    echo "✅ SUCCESS: No syntax errors found!"
    echo ""
    echo "🚀 READY TO RUN:"
    echo "streamlit run app_ultra_modern_fixed.py"
else
    echo "❌ Still have syntax errors. Manual fix needed."
    echo ""
    echo "🔍 Manual fix guide:"
    echo "1. nano app_ultra_modern_fixed.py"
    echo "2. Find line ~4332 with duplicate clean_combined_text"
    echo "3. Remove the broken duplicate function"
    echo "4. Ensure file ends with: if __name__ == '__main__': main()"
fi

echo ""
echo "📋 CHANGES MADE:"
echo "- Fixed function name calls"
echo "- Removed duplicate clean_combined_text"
echo "- Fixed indentation errors"
echo "- Cleaned up main() block"
