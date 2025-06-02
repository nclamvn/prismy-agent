# Fix confidence display
content = open('src/app/simple_ai_commander_test.py', 'r').read()

# Find and fix the confidence display
content = content.replace(
    'st.metric("Confidence", f"{data.get(\'confidence\', 0):.0%}")',
    'st.metric("Confidence", f"{float(data.get(\'confidence\', 0)):.0%}")'
)

open('src/app/simple_ai_commander_test.py', 'w').write(content)
print("Fixed confidence display!")
