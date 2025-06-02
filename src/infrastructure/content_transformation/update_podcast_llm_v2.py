#!/usr/bin/env python3
"""
Update podcast_generator.py to use LLM service - Version 2
"""

# Read the current file
with open('podcast_generator.py', 'r') as f:
    lines = f.readlines()

# Find and update _generate_intro method
in_intro_method = False
intro_start_line = -1
new_lines = []

for i, line in enumerate(lines):
    if 'def _generate_intro(self' in line:
        in_intro_method = True
        intro_start_line = i
        # Add the new method
        new_lines.append('    def _generate_intro(self, request: TransformationRequest) -> str:\n')
        new_lines.append('        """Generate intro phù hợp với audience using LLM"""\n')
        new_lines.append('        audience = request.target_audience\n')
        new_lines.append('        \n')
        new_lines.append('        # Use LLM if available\n')
        new_lines.append('        if self.llm_service:\n')
        new_lines.append('            try:\n')
        new_lines.append('                intro = self.llm_service.enhance_podcast_content(\n')
        new_lines.append('                    content=request.source_text[:200],\n')
        new_lines.append('                    section_type="intro",\n')
        new_lines.append('                    target_audience=audience.value,\n')
        new_lines.append('                    tone="conversational" if audience != TargetAudience.PROFESSIONALS else "professional"\n')
        new_lines.append('                )\n')
        new_lines.append('                return intro.strip()\n')
        new_lines.append('            except Exception as e:\n')
        new_lines.append('                print(f"LLM enhancement failed: {e}, using fallback")\n')
        new_lines.append('        \n')
        new_lines.append('        # Fallback to template if LLM fails\n')
        new_lines.append('        if audience not in self.INTRO_TEMPLATES:\n')
        new_lines.append('            audience = TargetAudience.GENERAL\n')
        new_lines.append('        \n')
        new_lines.append('        templates = self.INTRO_TEMPLATES[audience]\n')
        new_lines.append('        intro_template = templates[0]\n')
        new_lines.append('        \n')
        new_lines.append('        if request.context:\n')
        new_lines.append('            intro_template += f" {request.context}"\n')
        new_lines.append('        \n')
        new_lines.append('        return intro_template\n')
        new_lines.append('    \n')
        continue
    
    # Skip original method lines
    if in_intro_method:
        if line.strip() and not line[0].isspace() and 'def' in line:
            # Found next method, stop skipping
            in_intro_method = False
            new_lines.append(line)
        elif 'return intro_template' in line:
            # End of method
            in_intro_method = False
            continue
        else:
            # Skip this line
            continue
    else:
        new_lines.append(line)

# Write the updated content
with open('podcast_generator.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Updated _generate_intro to use LLM")
print("✅ Podcast Generator now uses LLM for dynamic content generation!")
print("\n📋 Summary of changes:")
print("- _generate_intro now calls self.llm_service.enhance_podcast_content()")
print("- Fallback to templates if LLM fails")
print("- Dynamic content based on audience type")
