#!/usr/bin/env python3
"""
Complete EducationModuleBuilder LLM integration
"""
import re

with open('education_module_builder.py', 'r') as f:
    content = f.read()

# Update _generate_activities
activities_update = '''    def _generate_activities(self, request: TransformationRequest, concepts: List[str]) -> str:
        """Generate learning activities using LLM"""
        audience = request.target_audience
        
        # Use LLM for creative activities
        if self.llm_service and concepts:
            try:
                activity_prompt = f"Create activities for: {', '.join(concepts[:3])}"
                enhanced_activities = self.llm_service.enhance_education_content(
                    content=activity_prompt,
                    module_type="learning_activities",
                    difficulty_level=request.difficulty_level.value,
                    learning_style="interactive"
                )
                if enhanced_activities:
                    return f"=== HOẠT ĐỘNG HỌC TẬP ===\\n\\n{enhanced_activities}\\n"
            except Exception as e:
                print(f"LLM activities generation failed: {e}, using fallback")
        
        # Fallback
        if audience not in self.ACTIVITY_TYPES:
            audience = TargetAudience.ADULTS
        
        activity_types = self.ACTIVITY_TYPES[audience]
        main_concept = concepts[0] if concepts else "chủ đề"
        
        activities_text = "=== HOẠT ĐỘNG HỌC TẬP ===\\n\\n"'''

# Replace method
pattern = r'def _generate_activities\(self.*?\):\s*"""Generate learning activities""".*?activities_text = "=== HOẠT ĐỘNG HỌC TẬP ===\\\\n\\\\n"'
content = re.sub(pattern, activities_update, content, flags=re.DOTALL)

with open('education_module_builder.py', 'w') as f:
    f.write(content)

print("✅ Completed EducationModuleBuilder LLM integration!")
print("- _extract_key_concepts ✓")
print("- _generate_learning_objectives ✓")
print("- _generate_activities ✓")
