#!/usr/bin/env python3
"""
Complete PodcastGenerator LLM integration - Add outro
"""

with open('podcast_generator.py', 'r') as f:
    lines = f.readlines()

# Find and update _generate_outro method
in_outro = False
new_lines = []

for i, line in enumerate(lines):
    if 'def _generate_outro(self' in line:
        in_outro = True
        # Add updated method
        new_lines.extend([
            '    def _generate_outro(self, request: TransformationRequest) -> str:\n',
            '        """Generate outro phù hợp với audience using LLM"""\n',
            '        audience = request.target_audience\n',
            '        \n',
            '        # Use LLM if available\n',
            '        if self.llm_service:\n',
            '            try:\n',
            '                outro = self.llm_service.enhance_podcast_content(\n',
            '                    content="Kết thúc podcast về " + request.source_text[:50],\n',
            '                    section_type="outro",\n',
            '                    target_audience=audience.value,\n',
            '                    tone="warm"\n',
            '                )\n',
            '                return outro.strip()\n',
            '            except Exception as e:\n',
            '                print(f"LLM outro generation failed: {e}, using fallback")\n',
            '        \n',
            '        # Fallback to template\n',
            '        if audience not in self.OUTRO_TEMPLATES:\n',
            '            audience = TargetAudience.GENERAL\n',
            '        \n',
            '        templates = self.OUTRO_TEMPLATES[audience]\n',
            '        return templates[0]\n',
            '    \n'
        ])
        continue
    
    if in_outro:
        if line.strip() and not line[0].isspace() and 'def' in line:
            in_outro = False
            new_lines.append(line)
        elif 'return templates[0]' in line:
            in_outro = False
            continue
    else:
        new_lines.append(line)

with open('podcast_generator.py', 'w') as f:
    f.writelines(new_lines)

print("✅ Completed PodcastGenerator LLM integration!")
print("- _generate_intro ✓")
print("- _generate_outro ✓")
