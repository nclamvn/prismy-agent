import re

# Read file
with open('src/infrastructure/content_transformation/podcast_generator.py', 'r') as f:
    content = f.read()

# Find and update __init__ to include llm_service
if 'self.llm_service' not in content:
    # Add llm_service initialization
    content = re.sub(
        r'(def __init__.*?\n.*?super\(\).__init__.*?\))',
        r'\1\n        self.llm_service = get_llm_service()',
        content,
        flags=re.DOTALL
    )

# Update _generate_intro method to use LLM
new_generate_intro = '''    def _generate_intro(self, request: TransformationRequest) -> str:
        """Generate podcast intro using LLM"""
        # Use LLM for natural intro
        if self.llm_service:
            intro = self.llm_service.enhance_podcast_content(
                content=request.source_text[:200],  # First 200 chars as context
                section_type="intro",
                target_audience=request.target_audience.value,
                tone="conversational" if request.target_audience != TargetAudience.PROFESSIONALS else "professional"
            )
            return intro
        
        # Fallback to template if no LLM
        templates = self.INTRO_TEMPLATES.get(
            request.target_audience, 
            self.INTRO_TEMPLATES[TargetAudience.GENERAL]
        )
        
        intro = templates[0]
        topic_intro = f" {request.source_text[:100]}..."
        
        return intro + topic_intro'''

# Replace the method
content = re.sub(
    r'def _generate_intro\(self.*?\n(?:.*?\n)*?return.*?\n',
    new_generate_intro + '\n',
    content,
    flags=re.MULTILINE
)

# Update _generate_outro similarly
new_generate_outro = '''    def _generate_outro(self, request: TransformationRequest) -> str:
        """Generate podcast outro using LLM"""
        # Use LLM for natural outro
        if self.llm_service:
            outro = self.llm_service.enhance_podcast_content(
                content="End of episode summary",
                section_type="outro",
                target_audience=request.target_audience.value,
                tone="conversational"
            )
            return outro
        
        # Fallback to template
        templates = self.OUTRO_TEMPLATES.get(
            request.target_audience,
            self.OUTRO_TEMPLATES[TargetAudience.GENERAL]
        )
        
        return templates[0]'''

# Replace outro method
content = re.sub(
    r'def _generate_outro\(self.*?\n(?:.*?\n)*?return.*?\n',
    new_generate_outro + '\n',
    content,
    flags=re.MULTILINE
)

# Write back
with open('src/infrastructure/content_transformation/podcast_generator.py', 'w') as f:
    f.write(content)

print("✅ Updated podcast generator methods to use LLM")
