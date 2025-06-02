"""
PRISM Enhanced Language Detection
Ultra-sophisticated multi-modal language identification
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class LanguageSignature:
    """Comprehensive language signature"""
    language: str
    confidence: float
    evidence: List[str]
    character_patterns: Dict[str, float]
    linguistic_patterns: Dict[str, float]
    cultural_patterns: Dict[str, float]

class EnhancedLanguageDetection:
    """
    Ultra-sophisticated language detection using multiple modalities
    """
    
    def __init__(self):
        self.language_signatures = self._build_language_signatures()
        self.cultural_indicators = self._build_cultural_indicators()
        self.linguistic_patterns = self._build_linguistic_patterns()
        
    def _build_language_signatures(self) -> Dict[str, Dict]:
        """Build comprehensive language signatures"""
        return {
            "vietnamese": {
                "special_chars": "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ",
                "tone_markers": "àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹ",
                "unique_letters": "đăâêôơư",
                "character_ranges": [(0x00C0, 0x00FF), (0x1EA0, 0x1EF9)],
                "grammatical_markers": [
                    r'\b(?:là|có|được|đã|sẽ|đang|rồi|mà|thì|nên)\b',
                    r'\b(?:một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)\b',
                    r'\b(?:này|đó|kia|nào|gì|ai|đâu|khi|nào)\b'
                ]
            },
            
            "english": {
                "special_chars": "",
                "tone_markers": "",
                "unique_letters": "",
                "character_ranges": [(0x0041, 0x005A), (0x0061, 0x007A)],
                "grammatical_markers": [
                    r'\b(?:is|are|was|were|have|has|had|will|would|can|could|should)\b',
                    r'\b(?:the|a|an|and|or|but|if|when|where|how|why|what)\b',
                    r'\b(?:one|two|three|four|five|six|seven|eight|nine|ten)\b'
                ]
            },
            
            "chinese": {
                "special_chars": "的是了我不人在他有這個上們來到時大地為子中你說生國年著就那和要她出也得裡後自以會家可下而過天去能對小多然於心學麼之都好看起發當沒成只如事把還用第樣道想作種開要因為就是這麼樣子",
                "tone_markers": "",
                "unique_letters": "",
                "character_ranges": [(0x4E00, 0x9FFF), (0x3400, 0x4DBF)],
                "grammatical_markers": [r'[的了是在有這個那和要也就都能可會要因為什麼怎麼樣]']
            },
            
            "korean": {
                "special_chars": "가나다라마바사아자차카타파하",
                "tone_markers": "",
                "unique_letters": "",
                "character_ranges": [(0xAC00, 0xD7AF), (0x1100, 0x11FF)],
                "grammatical_markers": [r'[이가은는을를과와의에서로부터까지]']
            },
            
            "japanese": {
                "special_chars": "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん",
                "tone_markers": "",
                "unique_letters": "",
                "character_ranges": [(0x3040, 0x309F), (0x30A0, 0x30FF), (0x4E00, 0x9FFF)],
                "grammatical_markers": [r'[はがをにでとからまで]', r'です|ます|だ|である']
            }
        }
    
    def _build_cultural_indicators(self) -> Dict[str, List[str]]:
        """Build cultural context indicators"""
        return {
            "vietnamese": [
                # Names and titles
                r'\b(?:anh|em|chị|ông|bà|cô|chú|thầy)\s+[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+',
                # Common Vietnamese names
                r'\b(?:Minh|Lan|Hương|Linh|Anh|Dung|Hải|Nam|Mai|Hoa|Tuấn|Hùng|Long|Phong|Đức|Khang|Thành|Hoàng|Quang|Thu|Loan|Nga|Thảo|Trang|Vy)\b',
                # Places
                r'\b(?:Việt\s+Nam|Hà\s+Nội|Tp\.\s+Hồ\s+Chí\s+Minh|Sài\s+Gòn|Đà\s+Nẵng|Huế|Cần\s+Thơ|Hải\s+Phòng|Nha\s+Trang|Đà\s+Lạt)\b',
                # Cultural terms
                r'\b(?:áo\s+dài|bánh\s+mì|phở|bún\s+bò|cơm\s+tấm|chả\s+cá|gỏi\s+cuốn|nem\s+rán|bún\s+chả|bánh\s+xèo)\b',
                # Time expressions
                r'\b(?:hôm\s+nay|ngày\s+mai|hôm\s+qua|tuần\s+sau|tháng\s+trước|năm\s+nay|giờ\s+này|lúc\s+nào)\b'
            ],
            
            "english": [
                # Common names
                r'\b(?:John|Mary|James|Sarah|Michael|Lisa|David|Karen|Robert|Susan|William|Jessica|Richard|Nancy|Joseph|Ashley)\b',
                # Places
                r'\b(?:New\s+York|Los\s+Angeles|Chicago|Houston|Phoenix|Philadelphia|San\s+Antonio|San\s+Diego|Dallas|San\s+Jose|Austin|Jacksonville)\b',
                # Cultural terms
                r'\b(?:hamburger|pizza|hot\s+dog|sandwich|coffee|tea|breakfast|lunch|dinner|weekend|holiday)\b',
                # Time expressions
                r'\b(?:today|tomorrow|yesterday|next\s+week|last\s+month|this\s+year|right\s+now|sometime)\b'
            ]
        }
    
    def _build_linguistic_patterns(self) -> Dict[str, List[str]]:
        """Build linguistic structure patterns"""
        return {
            "vietnamese": [
                # Word order patterns (SVO)
                r'\b[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+\s+(?:là|có|được|đã|sẽ|đang)\s+[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+',
                # Classifiers
                r'\b(?:một|hai|ba|bốn|năm)\s+(?:cái|con|chiếc|người|quyển|tờ|ly|chai|hộp)\b',
                # Question particles
                r'\b(?:không|chưa|đâu|gì|sao|thế\s+nào)\?',
                # Aspect markers
                r'\b(?:đã|đang|sẽ|vừa|vừa\s+mới|sắp|sửa)\s+[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+'
            ],
            
            "english": [
                # Word order patterns (SVO)
                r'\b[A-Z][a-z]+\s+(?:is|are|was|were|has|have|had|will|would|can|could|should)\s+[a-z]+',
                # Plural markers
                r'\b[a-z]+s\b',
                # Past tense markers
                r'\b[a-z]+ed\b',
                # Progressive markers
                r'\b(?:is|are|was|were)\s+[a-z]+ing\b',
                # Question formation
                r'\b(?:What|Where|When|Why|How|Who|Which)\s+(?:is|are|was|were|do|does|did|will|would|can|could)\b'
            ]
        }
    
    def detect_language_comprehensive(self, text: str) -> LanguageSignature:
        """Comprehensive language detection using multiple modalities"""
        
        # Clean text for analysis
        cleaned_text = self._clean_text_for_analysis(text)
        
        # Multi-modal analysis
        character_analysis = self._analyze_character_patterns(cleaned_text)
        linguistic_analysis = self._analyze_linguistic_patterns(cleaned_text)
        cultural_analysis = self._analyze_cultural_patterns(cleaned_text)
        structure_analysis = self._analyze_script_structure(text)
        
        # Calculate composite scores
        language_scores = self._calculate_composite_scores(
            character_analysis, linguistic_analysis, cultural_analysis, structure_analysis
        )
        
        # Select best match
        if not language_scores:
            # Fallback
            return LanguageSignature(
                language="english",
                confidence=0.5,
                evidence=["fallback_detection"],
                character_patterns={},
                linguistic_patterns={},
                cultural_patterns={}
            )
        
        best_language = max(language_scores.items(), key=lambda x: x[1]["total_score"])
        language = best_language[0]
        score_data = best_language[1]
        
        # Build comprehensive signature
        signature = LanguageSignature(
            language=language,
            confidence=score_data["total_score"],
            evidence=score_data["evidence"],
            character_patterns=character_analysis.get(language, {}),
            linguistic_patterns=linguistic_analysis.get(language, {}),
            cultural_patterns=cultural_analysis.get(language, {})
        )
        
        return signature
    
    def _clean_text_for_analysis(self, text: str) -> str:
        """Clean text while preserving linguistic features"""
        # Remove script directions but keep dialogue and descriptions
        cleaned = re.sub(r'\b(?:EXT\.|INT\.|FADE|CUT|DISSOLVE)\b[^\n]*', '', text, flags=re.IGNORECASE)
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove parentheticals in some cases but keep content
        cleaned = re.sub(r'\([^)]*\)', '', cleaned)
        
        return cleaned.strip()
    
    def _analyze_character_patterns(self, text: str) -> Dict[str, Dict[str, float]]:
        """Analyze character-based patterns"""
        results = {}
        total_chars = len(text)
        
        if total_chars == 0:
            return results
        
        for language, signature in self.language_signatures.items():
            scores = {}
            
            # Special character analysis
            special_chars = signature.get("special_chars", "")
            if special_chars:
                special_char_count = sum(1 for char in text if char in special_chars)
                scores["special_chars"] = (special_char_count / total_chars) * 100
            else:
                scores["special_chars"] = 0
            
            # Tone marker analysis
            tone_markers = signature.get("tone_markers", "")
            if tone_markers:
                tone_count = sum(1 for char in text if char in tone_markers)
                scores["tone_markers"] = (tone_count / total_chars) * 50
            else:
                scores["tone_markers"] = 0
            
            # Unique letter analysis
            unique_letters = signature.get("unique_letters", "")
            if unique_letters:
                unique_count = sum(1 for char in text if char in unique_letters)
                scores["unique_letters"] = (unique_count / total_chars) * 200
            else:
                scores["unique_letters"] = 0
            
            # Unicode range analysis
            char_ranges = signature.get("character_ranges", [])
            range_matches = 0
            for char in text:
                char_code = ord(char)
                for start, end in char_ranges:
                    if start <= char_code <= end:
                        range_matches += 1
                        break
            
            scores["unicode_ranges"] = (range_matches / total_chars) * 80 if total_chars > 0 else 0
            
            results[language] = scores
        
        return results
    
    def _analyze_linguistic_patterns(self, text: str) -> Dict[str, Dict[str, float]]:
        """Analyze linguistic structure patterns"""
        results = {}
        
        for language, patterns in self.linguistic_patterns.items():
            scores = {}
            total_score = 0
            
            for i, pattern in enumerate(patterns):
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                pattern_score = matches * (5 - i)  # Weight earlier patterns higher
                scores[f"pattern_{i}"] = pattern_score
                total_score += pattern_score
            
            scores["total_linguistic"] = total_score
            results[language] = scores
        
        return results
    
    def _analyze_cultural_patterns(self, text: str) -> Dict[str, Dict[str, float]]:
        """Analyze cultural context patterns"""
        results = {}
        
        for language, patterns in self.cultural_indicators.items():
            scores = {}
            total_score = 0
            
            for i, pattern in enumerate(patterns):
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                pattern_score = matches * 10  # Cultural indicators are strong signals
                scores[f"cultural_{i}"] = pattern_score
                total_score += pattern_score
            
            scores["total_cultural"] = total_score
            results[language] = scores
        
        return results
    
    def _analyze_script_structure(self, text: str) -> Dict[str, float]:
        """Analyze script structure for language clues"""
        structure_scores = {}
        
        # Analyze dialogue structure
        vietnamese_dialogue = len(re.findall(r'([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][A-Za-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+)\s*\n', text, re.MULTILINE))
        english_dialogue = len(re.findall(r'([A-Z][A-Za-z]+)\s*\n', text, re.MULTILINE))
        
        structure_scores["vietnamese"] = vietnamese_dialogue * 5
        structure_scores["english"] = english_dialogue * 3
        
        # Analyze scene directions
        vietnamese_directions = len(re.findall(r'(cảnh|chuyển|fade|cut)', text, re.IGNORECASE))
        english_directions = len(re.findall(r'(scene|fade|cut|ext|int)', text, re.IGNORECASE))
        
        structure_scores["vietnamese"] = structure_scores.get("vietnamese", 0) + vietnamese_directions * 2
        structure_scores["english"] = structure_scores.get("english", 0) + english_directions * 2
        
        return structure_scores
    
    def _calculate_composite_scores(self, character_analysis: Dict, linguistic_analysis: Dict, 
                                  cultural_analysis: Dict, structure_analysis: Dict) -> Dict[str, Dict]:
        """Calculate composite scores for each language"""
        
        composite_scores = {}
        
        # Get all possible languages
        all_languages = set()
        all_languages.update(character_analysis.keys())
        all_languages.update(linguistic_analysis.keys())
        all_languages.update(cultural_analysis.keys())
        all_languages.update(structure_analysis.keys())
        
        for language in all_languages:
            evidence = []
            
            # Character score (weight: 30%)
            char_scores = character_analysis.get(language, {})
            char_total = sum(char_scores.values())
            char_weighted = char_total * 0.3
            
            if char_total > 0:
                evidence.append(f"Character patterns: {char_total:.1f}")
            
            # Linguistic score (weight: 25%)
            ling_scores = linguistic_analysis.get(language, {})
            ling_total = ling_scores.get("total_linguistic", 0)
            ling_weighted = ling_total * 0.25
            
            if ling_total > 0:
                evidence.append(f"Linguistic patterns: {ling_total:.1f}")
            
            # Cultural score (weight: 25%)
            cult_scores = cultural_analysis.get(language, {})
            cult_total = cult_scores.get("total_cultural", 0)
            cult_weighted = cult_total * 0.25
            
            if cult_total > 0:
                evidence.append(f"Cultural indicators: {cult_total:.1f}")
            
            # Structure score (weight: 20%)
            struct_score = structure_analysis.get(language, 0)
            struct_weighted = struct_score * 0.2
            
            if struct_score > 0:
                evidence.append(f"Script structure: {struct_score:.1f}")
            
            # Total composite score
            total_score = char_weighted + ling_weighted + cult_weighted + struct_weighted
            
            # Normalize to 0-1 range
            normalized_score = min(1.0, total_score / 100.0)
            
            composite_scores[language] = {
                "total_score": normalized_score,
                "character_score": char_weighted,
                "linguistic_score": ling_weighted,
                "cultural_score": cult_weighted,
                "structure_score": struct_weighted,
                "evidence": evidence
            }
        
        return composite_scores

# Test enhanced language detection
if __name__ == "__main__":
    detector = EnhancedLanguageDetection()
    
    test_texts = [
        """
        FADE IN:
        
        EXT. NHÀ VIỆT NAM - SÁNG SỚM
        
        Anh MINH (40 tuổi, đàn ông Việt Nam, dáng gầy, da ngăm đen) bước ra khỏi nhà tranh nhỏ.
        
        MINH
        Chào em Lan! Sáng nay em dậy sớm quá!
        
        LAN
        Chào anh Minh! Em phải hái rau sớm để mang ra chợ bán.
        """,
        
        """
        FADE IN:
        
        EXT. AMERICAN HOUSE - MORNING
        
        JOHN (40 years old, tall American man, thin build) walks out of his small house.
        
        JOHN
        Good morning, Sarah! You're up early today!
        
        SARAH
        Good morning, John! I have to pick vegetables early to take them to market.
        """
    ]
    
    print("🧠 TESTING ENHANCED LANGUAGE DETECTION:")
    print("="*60)
    
    for i, text in enumerate(test_texts):
        print(f"\n🔍 Test {i+1}:")
        signature = detector.detect_language_comprehensive(text)
        
        print(f"   Language: {signature.language}")
        print(f"   Confidence: {signature.confidence:.3f}")
        print(f"   Evidence: {signature.evidence}")
        print(f"   Character patterns: {sum(signature.character_patterns.values()):.1f}")
        print(f"   Linguistic patterns: {sum(signature.linguistic_patterns.values()):.1f}")
        print(f"   Cultural patterns: {sum(signature.cultural_patterns.values()):.1f}")
    
    print(f"\n✅ ENHANCED LANGUAGE DETECTION READY! 🧠🎯")
