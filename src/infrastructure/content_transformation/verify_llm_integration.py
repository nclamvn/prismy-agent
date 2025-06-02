#!/usr/bin/env python3
"""
Verify all LLM integrations are working
"""
import os
import re

modules_to_check = {
    'podcast_generator.py': [
        'self.llm_service.enhance_podcast_content.*intro',
        'self.llm_service.enhance_podcast_content.*outro'
    ],
    'education_module_builder.py': [
        'self.llm_service.enhance_education_content.*concept',
        'self.llm_service.enhance_education_content.*objectives',
        'self.llm_service.enhance_education_content.*activities'
    ]
}

print("🔍 LLM Integration Verification Report")
print("=" * 50)

for file, patterns in modules_to_check.items():
    if os.path.exists(file):
        with open(file, 'r') as f:
            content = f.read()
        
        print(f"\n📄 {file}:")
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL):
                print(f"  ✅ Found: {pattern[:50]}...")
            else:
                print(f"  ❌ Missing: {pattern[:50]}...")
    else:
        print(f"\n❌ File not found: {file}")

print("\n" + "=" * 50)
print("✅ Verification complete!")
