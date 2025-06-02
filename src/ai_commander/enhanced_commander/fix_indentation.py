# Read the file
with open('intelligent_claude_commander.py', 'r') as f:
    lines = f.readlines()

# Find and fix the indentation issue around line 168
fixed_lines = []
for i, line in enumerate(lines):
    if i > 0 and '"""Fallback when API unavailable"""' in line and not line.startswith('    '):
        # Add proper indentation
        fixed_lines.append('        """Fallback when API unavailable"""\n')
    else:
        fixed_lines.append(line)

# Write back
with open('intelligent_claude_commander.py', 'w') as f:
    f.writelines(fixed_lines)

print("✅ Fixed indentation")
