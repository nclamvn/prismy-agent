#!/usr/bin/env python3
"""
Restructure project to proper Python package
"""
import os
from pathlib import Path

print("📦 Creating proper package structure...\n")

# Ensure all directories have __init__.py
directories_need_init = [
    "src",
    "src/core",
    "src/core/entities",
    "src/core/use_cases",
    "src/application",
    "src/application/services",
    "src/infrastructure",
    "src/infrastructure/ai_clients",
    "src/infrastructure/translation",
    "src/infrastructure/content_transformation",
    "src/ai_commander",
    "src/ai_commander/enhanced_commander",
]

created_count = 0
for dir_path in directories_need_init:
    init_file = Path(dir_path) / "__init__.py"
    if not init_file.exists():
        init_file.touch()
        print(f"✅ Created {init_file}")
        created_count += 1

print(f"\n📊 Created {created_count} __init__.py files")

# Create setup.py for proper imports
setup_content = '''from setuptools import setup, find_packages

setup(
    name="translate_export_agent",
    version="1.0.0",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "streamlit",
        "openai",
        "anthropic",
        "pydantic",
        "aiohttp",
        "pytest",
    ],
)
'''

with open("setup.py", "w") as f:
    f.write(setup_content)
print("\n✅ Created setup.py")

# Create .env.example
env_example = '''# API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# LLM Settings
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000

# App Settings
DEBUG=False
LOG_LEVEL=INFO
'''

with open(".env.example", "w") as f:
    f.write(env_example)
print("✅ Created .env.example")

print("\n🎯 Next: Install in development mode:")
print("   pip install -e .")
print("\n💡 Then you can use proper imports:")
print("   from src.application.services import TranslationService")
print("   from src.ai_commander.enhanced_commander import EnhancedProductionCommander")
