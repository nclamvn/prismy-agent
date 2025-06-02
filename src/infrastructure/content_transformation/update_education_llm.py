#!/usr/bin/env python3
"""
Update education_module_builder.py to use LLM service
"""

# Read the current file
with open('education_module_builder.py', 'r') as f:
    content = f.read()

# 1. Update _extract_key_concepts to use LLM
update_1 = '''    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key concepts từ text using LLM"""
        # Try LLM first
        if self.llm_service:
            try:
                enhanced_concepts = self.llm_service.enhance_education_content(
                    content=text[:500],  # First 500 chars
                    module_type="concept_extraction",
                    difficulty_level="intermediate",
                    learning_style="analytical"
                )
                # Parse LLM response to extract concepts
                if enhanced_concepts:
                    concepts = [c.strip() for c in enhanced_concepts.split(',') if c.strip()]
                    if concepts:
                        return concepts[:5]  # Top 5 concepts
            except Exception as e:
                print(f"LLM concept extraction failed: {e}, using fallback")
        
        # Fallback to simple extraction
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        concepts = []
        
        # Look for important nouns và phrases
        important_patterns = ['''

# Replace the method
import re
pattern = r'def _extract_key_concepts\(self, text: str\) -> List\[str\]:\s*"""Extract key concepts từ text""".*?# Look for important nouns và phrases\s*important_patterns = \['
new_content = re.sub(pattern, update_1, content, flags=re.DOTALL)

# 2. Update _generate_learning_objectives to be more dynamic
update_2 = '''    def _generate_learning_objectives(self, request: TransformationRequest, concepts: List[str]) -> str:
        """Generate learning objectives section using LLM"""
        # Use LLM for better objectives
        if self.llm_service and concepts:
            try:
                objectives_prompt = f"Key concepts: {', '.join(concepts[:3])}"
                enhanced_objectives = self.llm_service.enhance_education_content(
                    content=objectives_prompt,
                    module_type="learning_objectives",
                    difficulty_level=request.difficulty_level.value,
                    learning_style="structured"
                )
                if enhanced_objectives:
                    return f"=== MỤC TIÊU HỌC TẬP ===\\n{enhanced_objectives}\\n"
            except Exception as e:
                print(f"LLM objectives generation failed: {e}, using fallback")
        
        # Fallback
        objectives = self._extract_learning_objectives(request)
        
        objectives_text = "=== MỤC TIÊU HỌC TẬP ===\\nSau khi hoàn thành module này, học viên sẽ có thể:\\n\\n"
        
        for i, objective in enumerate(objectives, 1):
            objectives_text += f"{i}. {objective}\\n"
        
        return objectives_text'''

# Replace the method
pattern2 = r'def _generate_learning_objectives\(self, request: TransformationRequest, concepts: List\[str\]\) -> str:.*?return objectives_text'
new_content = re.sub(pattern2, update_2, new_content, flags=re.DOTALL)

# Write updated content
with open('education_module_builder.py', 'w') as f:
    f.write(new_content)

print("✅ Updated Education Module Builder with LLM integration!")
print("\n📋 Changes made:")
print("1. _extract_key_concepts now uses LLM for better concept extraction")
print("2. _generate_learning_objectives uses LLM for dynamic objectives")
print("\n💡 Next steps: Update _generate_activities and _generate_assessment methods")
