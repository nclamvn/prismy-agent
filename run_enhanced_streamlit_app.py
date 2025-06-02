#!/usr/bin/env python3
"""
🚀 LAUNCH ENHANCED STREAMLIT APP - PHASE 3B COMPLETE
"""

import streamlit as st
import sys
import os
import subprocess

def setup_paths():
    """Setup Python paths"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    return src_dir

def main():
    """Launch the enhanced Streamlit app"""
    print("🚀 LAUNCHING ENHANCED STREAMLIT APP")
    print("=" * 50)
    print("🎯 Phase 3B Complete - All Features Integrated!")
    print("📊 App will be available at: http://localhost:8511")
    print("🔄 Starting...")
    
    # Setup paths
    setup_paths()
    
    # Launch Streamlit
    try:
        subprocess.run([
            'streamlit', 'run', 
            'src/app/enhanced_main.py',
            '--server.port', '8511',
            '--server.headless', 'false'
        ])
    except KeyboardInterrupt:
        print("\n✅ App stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        print("\n🔧 Fallback: Try manual launch:")
        print("streamlit run src/app/enhanced_main.py --server.port 8511")

if __name__ == "__main__":
    main()
