#!/usr/bin/env python3
"""
🚀 Simple Enhanced App Launcher
"""

import streamlit
import sys
import os

# Setup paths
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)
sys.path.insert(0, current_dir)

print("🚀 Enhanced Translation App")
print("📊 Available at: http://localhost:8511")
print("🔄 Starting Streamlit...")

# Import test
try:
    from src.application.services.enhanced_translation_service import EnhancedTranslationService
    print("✅ Enhanced service import OK")
except Exception as e:
    print(f"❌ Service import failed: {e}")
    print("🔄 Continuing anyway...")

# Run Streamlit
if __name__ == "__main__":
    import subprocess
    subprocess.run([
        'streamlit', 'run', 
        'src/app/enhanced_main.py',
        '--server.port', '8511'
    ])
