#!/usr/bin/env python3
"""
Switch app to use hotel_concierge_claude with full features
"""

# Update import in ai_commander_streamlit.py
with open('src/app/ai_commander_streamlit.py', 'r') as f:
    content = f.read()

# Replace import
old_import = "from ai_commander.enhanced_commander.claude_commander import ClaudeCommander"
new_import = "from ai_commander.enhanced_commander.hotel_concierge_claude import EnhancedProductionCommander as ClaudeCommander"

content = content.replace(old_import, new_import)

# Write back
with open('src/app/ai_commander_streamlit.py', 'w') as f:
    f.write(content)

print("✅ Switched to hotel_concierge_claude!")
print("📋 Now you have:")
print("- Translation Service ✓")
print("- Transformation Manager ✓")
print("- All content creation features ✓")
