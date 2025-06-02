"""
LLM Prompt Enhancer for PRISM Video DNA
Converts basic chunks + DNA into professional video generation prompts
"""

import time
from typing import Dict, List, Any, Optional
import json

class LLMPromptEnhancer:
    """
    Enhance PRISM DNA chunks with LLM to create professional video prompts
    
    Features:
    - Convert script chunks into detailed video descriptions
    - Maintain DNA continuity through prompts
    - Optimize for Sora, Kling, Veo 3, Runway ML
    - Professional cinematography suggestions
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = None
        
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                self.client = openai.OpenAI(api_key=api_key)
                print(f"✅ LLM Enhancer initialized with {model}")
            except ImportError:
                print("⚠️ OpenAI not installed. Install with: pip install openai")
        else:
            print("⚠️ LLM Enhancer in simulation mode (no API key)")
    
    def enhance_chunk_prompts(self, chunks: List[Dict], dna_chain: List[str], 
                            target_platform: str = "sora") -> List[Dict]:
        """
        Enhance all chunks with LLM-generated professional prompts
        """
        
        enhanced_chunks = []
        
        for i, chunk in enumerate(chunks):
            print(f"🎬 Enhancing chunk {i+1}/{len(chunks)}...")
            
            # Get context from previous chunks
            context = self._build_context(chunks, i)
            
            # Generate enhanced prompt
            enhanced_prompt = self._generate_enhanced_prompt(
                chunk, context, dna_chain[i] if i < len(dna_chain) else None, target_platform
            )
            
            # Update chunk with enhanced prompt
            enhanced_chunk = chunk.copy()
            enhanced_chunk["ai_prompt"] = enhanced_prompt
            enhanced_chunk["enhanced_by_llm"] = True
            enhanced_chunk["target_platform"] = target_platform
            enhanced_chunk["original_prompt"] = chunk.get("ai_prompt", "")
            
            enhanced_chunks.append(enhanced_chunk)
            
            # Rate limiting
            if self.client:
                time.sleep(0.5)
        
        return enhanced_chunks
    
    def _generate_enhanced_prompt(self, chunk: Dict, context: str, 
                                dna_hash: str, platform: str) -> str:
        """Generate enhanced prompt using LLM or fallback"""
        
        if not self.client:
            return self._generate_professional_fallback(chunk, dna_hash, platform)
        
        try:
            # Build LLM prompt for enhancement
            system_prompt = f"""You are a professional video director and prompt engineer for AI video generation platforms like {platform.upper()}.

Convert script chunks into detailed, cinematic video generation prompts that:
1. Include specific camera angles, lighting, and visual details
2. Maintain character consistency and visual continuity
3. Optimize for {platform.upper()} video generation
4. Create professional, film-quality descriptions
5. Focus on visual storytelling and cinematic quality"""

            user_prompt = f"""Convert this script chunk into a professional video generation prompt:

SCRIPT CONTENT: {chunk['content']}
CHARACTERS: {', '.join(chunk['characters']) if chunk['characters'] else 'None'}
SCENE TYPE: {chunk['scene_type']}
DURATION: {chunk['duration']} seconds
EMOTIONAL TONE: {chunk.get('emotional_tone', 'neutral')}

PREVIOUS SCENES CONTEXT:
{context}

Create a detailed, visual description optimized for {platform.upper()} that maintains continuity."""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=400,
                temperature=0.7
            )
            
            enhanced_prompt = response.choices[0].message.content
            
            # Add PRISM DNA header
            final_prompt = f"""🎬 PRISM ENHANCED PROMPT [DNA: {dna_hash}]

{enhanced_prompt}

🧬 DNA CONTINUITY: Maintains visual consistency with DNA fingerprint {dna_hash}
🎯 Platform: {platform.upper()} optimized
⚡ Quality: 4K professional cinematic"""

            return final_prompt
            
        except Exception as e:
            print(f"⚠️ LLM enhancement failed: {e}")
            return self._generate_professional_fallback(chunk, dna_hash, platform)
    
    def _generate_professional_fallback(self, chunk: Dict, dna_hash: str, platform: str) -> str:
        """Professional fallback prompt when LLM not available"""
        
        content = chunk['content']
        characters = chunk['characters'] if chunk['characters'] else []
        
        # Enhanced fallback with more professional details
        enhanced_description = self._enhance_content_description(content, characters, chunk)
        
        return f"""🎬 PRISM PROFESSIONAL PROMPT [DNA: {dna_hash}]

📋 ENHANCED SCENE DESCRIPTION:
{enhanced_description}

🎥 CINEMATIC SPECIFICATIONS:
- Duration: {chunk['duration']} seconds
- Shot Type: {self._suggest_shot_type(content)}
- Camera Movement: {self._suggest_camera_movement(chunk.get('emotional_tone', 'neutral'))}
- Lighting: {self._suggest_lighting(chunk.get('scene_type', 'establishing'))}
- Visual Style: Hyper-realistic, 4K ultra-sharp, professional cinematography

👥 CHARACTER CONTINUITY:
{self._describe_character_continuity(characters)}

🌍 ENVIRONMENT DETAILS:
{self._describe_environment(content)}

🧬 DNA FINGERPRINT: {dna_hash}
- Ensures perfect visual continuity with previous scenes
- Maintains character appearance and environmental consistency

🎯 {platform.upper()} OPTIMIZED:
- Quality: Professional cinema grade
- Style: Photorealistic with cinematic depth
- Motion: Smooth, natural movement
- Composition: Rule of thirds, professional framing

⚡ READY FOR AI VIDEO GENERATION"""
    
    def _enhance_content_description(self, content: str, characters: List[str], chunk: Dict) -> str:
        """Create enhanced description of the content"""
        
        if not characters:
            return f"A professionally shot scene: {content}. Cinematic quality with attention to visual detail and composition."
        
        char_desc = f"featuring {', '.join(characters)}" if len(characters) == 1 else f"featuring characters {', '.join(characters)}"
        
        return f"A {chunk.get('emotional_tone', 'neutral')} scene {char_desc}. {content}. Shot with professional cinematography, attention to character expression and environmental details."
    
    def _suggest_shot_type(self, content: str) -> str:
        """Suggest appropriate shot type based on content"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ['close', 'face', 'eyes', 'expression']):
            return "Close-up"
        elif any(word in content_lower for word in ['walk', 'move', 'enter', 'leave']):
            return "Medium shot with movement"
        elif any(word in content_lower for word in ['office', 'room', 'building', 'ext.']):
            return "Wide establishing shot"
        else:
            return "Medium shot"
    
    def _suggest_camera_movement(self, emotional_tone: str) -> str:
        """Suggest camera movement based on emotional tone"""
        movements = {
            'intense': 'Dynamic tracking',
            'calm': 'Steady, smooth',
            'exciting': 'Dynamic with slight movement',
            'dramatic': 'Slow push-in',
            'neutral': 'Steady, professional'
        }
        return movements.get(emotional_tone, 'Steady, professional')
    
    def _suggest_lighting(self, scene_type: str) -> str:
        """Suggest lighting based on scene type"""
        lighting = {
            'dialogue': 'Soft, even lighting for clear character visibility',
            'action': 'Dynamic lighting with contrast',
            'establishing': 'Natural environmental lighting',
            'dramatic': 'Dramatic lighting with shadows'
        }
        return lighting.get(scene_type, 'Professional cinematic lighting')
    
    def _describe_character_continuity(self, characters: List[str]) -> str:
        """Describe character continuity requirements"""
        if not characters:
            return "No specific characters in this scene"
        
        return f"Maintain exact appearance consistency for: {', '.join(characters)}. Same clothing, hairstyle, facial features, and mannerisms as established in previous scenes."
    
    def _describe_environment(self, content: str) -> str:
        """Describe environment based on content"""
        content_lower = content.lower()
        
        if 'office' in content_lower:
            return "Modern office environment with professional lighting and contemporary furniture"
        elif 'ext.' in content_lower:
            return "Exterior location with natural lighting and environmental details"
        elif 'conference' in content_lower or 'table' in content_lower:
            return "Professional meeting space with conference table and business environment"
        else:
            return "Appropriate environmental setting that matches the scene context"
    
    def _build_context(self, chunks: List[Dict], current_index: int) -> str:
        """Build context from previous chunks"""
        
        if current_index == 0:
            return "This is the opening scene."
        
        context_chunks = chunks[max(0, current_index-2):current_index]
        context = []
        
        for i, chunk in enumerate(context_chunks):
            context.append(f"Previous scene {i+1}: {chunk['content']}")
        
        return "\n".join(context) if context else "This follows the opening scene."

# Quick enhancement function
def enhance_video_prompts(chunks: List[Dict], dna_chain: List[str], 
                         api_key: Optional[str] = None, platform: str = "sora") -> List[Dict]:
    """
    Quick function to enhance video prompts
    
    Usage:
        enhanced = enhance_video_prompts(chunks, dna_chain, api_key="your-key", platform="sora")
    """
    enhancer = LLMPromptEnhancer(api_key=api_key)
    return enhancer.enhance_chunk_prompts(chunks, dna_chain, platform)

if __name__ == "__main__":
    # Test the enhancer
    test_chunks = [
        {
            "content": "JENNY (29, venture capitalist) leans forward at the conference table.",
            "characters": ["Jenny"],
            "scene_type": "dialogue",
            "duration": 8.0,
            "emotional_tone": "focused"
        }
    ]
    
    print("🎬 Testing LLM Prompt Enhancer...")
    enhanced = enhance_video_prompts(test_chunks, ["abc123"], platform="sora")
    
    print("\n🚀 ENHANCED PROMPT:")
    print("="*60)
    print(enhanced[0]["ai_prompt"])
