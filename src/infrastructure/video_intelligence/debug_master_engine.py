"""
Debug and fix master engine error
"""

# Test individual components first
from advanced_character_intelligence import AdvancedCharacterIntelligence
from enhanced_scene_analyzer import EnhancedSceneAnalyzer
from enhanced_language_detection import EnhancedLanguageDetection
from ultra_compact_dna import UltraCompactDNAEngine

def test_components():
    print("🔍 Testing individual components...")
    
    # Test Character Intelligence
    print("👥 Testing Character Intelligence...")
    char_intel = AdvancedCharacterIntelligence("english")
    test_content = "MINH walks to LAN who is harvesting vegetables"
    characters = char_intel.extract_characters_ultra_smart(test_content, "english")
    print(f"   Characters: {characters}")
    
    # Test Scene Analyzer
    print("🎬 Testing Scene Analyzer...")
    scene_analyzer = EnhancedSceneAnalyzer(8.0, "english")
    test_script = "MINH walks. LAN smiles."
    scenes = scene_analyzer.analyze_script_enhanced(test_script)
    print(f"   Scenes: {len(scenes)}")
    
    # Test DNA Engine
    print("🧬 Testing DNA Engine...")
    dna_engine = UltraCompactDNAEngine("english")
    test_chunk = "MINH (40, Vietnamese man) walks to LAN (25, beautiful woman)"
    test_characters = ["Minh", "Lan"]
    
    try:
        dna = dna_engine.extract_ultra_compact_dna(test_chunk, 1, test_characters, None)
        print(f"   DNA generated: {dna.dna_hash}")
        
        # Test prompt generation
        prompt = dna_engine.generate_ultra_compact_prompt(test_chunk, dna, "english")
        print(f"   Prompt generated: {len(prompt)} chars")
        
    except Exception as e:
        print(f"   ❌ DNA Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_components()
