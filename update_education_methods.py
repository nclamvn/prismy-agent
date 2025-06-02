import re

# Read file
with open('src/infrastructure/content_transformation/education_module_builder.py', 'r') as f:
    content = f.read()

# Add llm_service initialization if not exists
if 'self.llm_service' not in content:
    content = re.sub(
        r'(def __init__.*?\n.*?super\(\).__init__.*?\))',
        r'\1\n        self.llm_service = get_llm_service()',
        content,
        flags=re.DOTALL
    )

# Update _create_learning_objectives to use LLM
new_objectives_method = '''    def _create_learning_objectives(self, request: TransformationRequest) -> List[str]:
        """Create learning objectives using LLM"""
        if self.llm_service:
            # Use LLM to generate relevant objectives
            objectives_text = self.llm_service.enhance_education_content(
                content=request.source_text[:300],
                module_type="objective",
                difficulty_level=request.difficulty_level.value,
                learning_style="clear"
            )
            # Split into list
            objectives = [obj.strip() for obj in objectives_text.split('\n') if obj.strip() and len(obj.strip()) > 10]
            return objectives[:5]  # Max 5 objectives
        
        # Fallback to templates
        topic = self._extract_topic(request.source_text)
        templates = self.LEARNING_OBJECTIVES.get(
            request.target_audience,
            self.LEARNING_OBJECTIVES[TargetAudience.ADULTS]
        )
        
        objectives = []
        for template in templates[:3]:
            objectives.append(template.format(topic))
        
        return objectives'''

# Replace method
content = re.sub(
    r'def _create_learning_objectives\(self.*?\n(?:.*?\n)*?return objectives',
    new_objectives_method[:-17],  # Remove last 'return objectives' as it's included
    content,
    flags=re.MULTILINE
)

# Update _create_exercises to use LLM
new_exercises_method = '''    def _create_exercises(self, request: TransformationRequest) -> List[Dict[str, Any]]:
        """Create exercises using LLM"""
        exercises = []
        
        if self.llm_service:
            # Generate exercise with LLM
            exercise_text = self.llm_service.enhance_education_content(
                content=request.source_text[:500],
                module_type="exercise",
                difficulty_level=request.difficulty_level.value,
                learning_style="interactive"
            )
            
            exercises.append({
                "type": "interactive",
                "title": "Practice Exercise",
                "content": exercise_text,
                "difficulty": request.difficulty_level.value
            })
        
        # Add some template-based exercises too
        assessment_types = self.ASSESSMENT_TYPES.get(
            request.difficulty_level,
            self.ASSESSMENT_TYPES[ContentDifficulty.INTERMEDIATE]
        )
        
        for ex_type in assessment_types[:2]:
            exercises.append({
                "type": ex_type,
                "title": f"{ex_type.replace('_', ' ').title()} Exercise",
                "content": f"Complete this {ex_type} exercise based on the lesson.",
                "difficulty": request.difficulty_level.value
            })
        
        return exercises'''

# Find and replace _create_exercises
if '_create_exercises' in content:
    content = re.sub(
        r'def _create_exercises\(self.*?\n(?:.*?\n)*?return exercises',
        new_exercises_method[:-16],
        content,
        flags=re.MULTILINE
    )

# Write back
with open('src/infrastructure/content_transformation/education_module_builder.py', 'w') as f:
    f.write(content)

print("✅ Updated education module builder to use LLM")
