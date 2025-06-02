#!/usr/bin/env python3
"""
Fix ai_intelligence __init__.py
"""

init_file = "src/infrastructure/ai_intelligence/__init__.py"

# Read current content
with open(init_file, 'r') as f:
    content = f.read()

# Uncomment the IntelligenceOrchestrator import
content = content.replace(
    "#from .intelligence_orchestrator import IntelligenceOrchestrator, ProcessingResult, WorkflowStage",
    "from .intelligence_orchestrator import IntelligenceOrchestrator, ProcessingResult, WorkflowStage"
)

# Write back
with open(init_file, 'w') as f:
    f.write(content)

print("✅ Fixed IntelligenceOrchestrator import!")
