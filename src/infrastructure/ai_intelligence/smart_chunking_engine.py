"""
Smart Chunking Engine 2.0 - IMPROVED
AI-powered intelligent content segmentation với semantic understanding
"""

import re
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio


class ChunkType(Enum):
    """Loại chunks được AI detect"""
    INTRODUCTION = "introduction"
    MAIN_CONCEPT = "main_concept"
    EXPLANATION = "explanation"
    EXAMPLE = "example"
    COMPARISON = "comparison"
    CONCLUSION = "conclusion"
    TRANSITION = "transition"
    DEFINITION = "definition"
    PROCESS = "process"
    ARGUMENT = "argument"


class SemanticComplexity(Enum):
    """Mức độ phức tạp semantic"""
    SIMPLE = "simple"           # Câu đơn, ý đơn giản
    MODERATE = "moderate"       # Câu phức, nhiều ý
    COMPLEX = "complex"         # Logic phức tạp, abstract
    EXPERT = "expert"           # Chuyên sâu, technical


@dataclass
class ChunkAnalysis:
    """Phân tích chi tiết của một chunk"""
    chunk_id: str
    content: str
    chunk_type: ChunkType
    semantic_complexity: SemanticComplexity
    key_concepts: List[str]
    relationships: List[str]  # IDs của chunks liên quan
    topic_score: float        # Độ quan trọng của topic (0-1)
    coherence_score: float    # Độ liên kết nội bộ (0-1)
    transformation_potential: Dict[str, float]  # Phù hợp cho format nào
    metadata: Dict[str, Any]


@dataclass
class DocumentStructure:
    """Cấu trúc document được AI phân tích"""
    main_topics: List[str]
    topic_hierarchy: Dict[str, List[str]]
    narrative_flow: List[str]  # Trình tự logic
    key_relationships: List[Tuple[str, str, str]]  # (chunk1, relation, chunk2)
    document_type: str
    overall_complexity: SemanticComplexity


class SmartChunkingEngine:
    """
    AI-powered chunking engine với semantic understanding - IMPROVED
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Default config
        self.default_config = {
            "min_chunk_size": 50,
            "max_chunk_size": 500,
            "semantic_threshold": 0.7,
            "topic_coherence_threshold": 0.6,
            "enable_topic_modeling": True,
            "enable_relationship_detection": True
        }
        self.config = {**self.default_config, **self.config}
        
        # AI patterns cho content analysis
        self._init_ai_patterns()
    
    def _init_ai_patterns(self):
        """Initialize AI patterns cho content detection - IMPROVED"""
        
        # Patterns để detect chunk types
        self.chunk_type_patterns = {
            ChunkType.INTRODUCTION: [
                r"\b(giới thiệu|mở đầu|bắt đầu|đầu tiên)\b",
                r"\b(hôm nay|trong bài này|chúng ta sẽ)\b",
                r"\b(tổng quan|khái quát|chung)\b"
            ],
            ChunkType.DEFINITION: [
                r"\b(là gì|định nghĩa|khái niệm)\b",
                r"\b(được hiểu là|có nghĩa là|chính là)\b",
                r"\b(thuật ngữ)\b"
            ],
            ChunkType.EXAMPLE: [
                r"\b(ví dụ|chẳng hạn|như là)\b",
                r"\b(cụ thể|minh họa|thể hiện)\b",
                r"\b(trường hợp|tình huống)\b"
            ],
            ChunkType.EXPLANATION: [
                r"\b(giải thích|lý do|tại sao)\b",
                r"\b(bởi vì|do đó|vì thế)\b",
                r"\b(nguyên nhân|cơ chế|cách thức)\b"
            ],
            ChunkType.COMPARISON: [
                r"\b(so với|khác với|tương tự)\b",
                r"\b(trong khi|ngược lại|đối lập)\b",
                r"\b(hơn|kém|bằng|giống)\b"
            ],
            ChunkType.CONCLUSION: [
                r"\b(kết luận|tóm lại|cuối cùng)\b",
                r"\b(như vậy|do đó|vì thế)\b",
                r"\b(tổng kết|kết thúc)\b"
            ]
        }
        
        # IMPROVED: Specific Vietnamese + English technical terms
        self.technical_terms = [
            "trí tuệ nhân tạo", "artificial intelligence", "AI",
            "machine learning", "deep learning", "neural network",
            "công nghệ", "technology", "innovation", "dữ liệu", "data",
            "hệ thống", "system", "platform", "algorithm", "thuật toán",
            "tự động hóa", "automation", "phân tích", "analysis"
        ]
        
        # IMPROVED: Domain-specific terms
        self.domain_terms = {
            "healthcare": ["y tế", "chẩn đoán", "bệnh", "điều trị"],
            "education": ["giáo dục", "học tập", "cá nhân hóa", "đào tạo"],
            "business": ["kinh doanh", "tối ưu hóa", "quy trình", "hiệu quả"],
            "ethics": ["đạo đức", "ethics", "trách nhiệm", "responsibility"]
        }
        
        # Complexity indicators - IMPROVED
        self.complexity_indicators = {
            SemanticComplexity.SIMPLE: [
                r"\b(là|có|được|sẽ|giúp|hỗ trợ)\b",  # Simple verbs
                r"\b(này|đó|đây|các|những)\b",        # Simple determiners
            ],
            SemanticComplexity.MODERATE: [
                r"\b(tuy nhiên|mặc dù|do đó|vì thế)\b",  # Connectors
                r"\b(phần lớn|một số|nhiều|thường)\b",   # Quantifiers
                r"\b(ứng dụng|sử dụng|thực hiện)\b"     # Action verbs
            ],
            SemanticComplexity.COMPLEX: [
                r"\b(phức tạp|sophisticated|advanced|cách mạng)\b",
                r"\b(optimization|efficiency|scalability)\b",
                r"\b(neural networks|deep learning)\b"
            ],
            SemanticComplexity.EXPERT: [
                r"\b(paradigm|methodology|framework|architecture)\b",
                r"\b(implementation|deployment|orchestration)\b",
                r"\b(enterprise|infrastructure|scalable)\b"
            ]
        }
    
    async def analyze_document(self, text: str) -> Tuple[List[ChunkAnalysis], DocumentStructure]:
        """
        Phân tích document hoàn chỉnh với AI
        """
        start_time = time.time()
        
        # Step 1: Intelligent segmentation
        raw_chunks = await self._intelligent_segmentation(text)
        
        # Step 2: Semantic analysis cho từng chunk
        chunk_analyses = []
        for i, chunk_text in enumerate(raw_chunks):
            analysis = await self._analyze_chunk(chunk_text, i, raw_chunks)
            chunk_analyses.append(analysis)
        
        # Step 3: Document structure analysis
        doc_structure = await self._analyze_document_structure(chunk_analyses, text)
        
        # Step 4: Relationship detection
        await self._detect_relationships(chunk_analyses)
        
        # Step 5: Optimization
        optimized_chunks = await self._optimize_chunks(chunk_analyses)
        
        processing_time = time.time() - start_time
        
        print(f"🧠 Smart chunking completed in {processing_time:.3f}s")
        print(f"   Chunks created: {len(optimized_chunks)}")
        print(f"   Topics detected: {len(doc_structure.main_topics)}")
        
        return optimized_chunks, doc_structure
    
    async def _intelligent_segmentation(self, text: str) -> List[str]:
        """
        Intelligent segmentation dựa trên semantic boundaries
        """
        # Preprocessing
        text = self._preprocess_text(text)
        
        # Multi-level segmentation
        segments = []
        
        # Level 1: Paragraph-based
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for paragraph in paragraphs:
            # Level 2: Sentence-based với semantic grouping
            sentences = self._split_sentences(paragraph)
            
            # Group sentences với semantic similarity
            semantic_groups = await self._group_sentences_semantically(sentences)
            
            segments.extend(semantic_groups)
        
        return segments
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocessing text cho better analysis"""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix punctuation
        text = re.sub(r'([.!?])\s*([A-ZÁĂÂÉÊÍÔƠƯÝ])', r'\1 \2', text)
        
        return text.strip()
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text thành sentences thông minh"""
        # Improved sentence splitting cho tiếng Việt
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    async def _group_sentences_semantically(self, sentences: List[str]) -> List[str]:
        """
        Group sentences dựa trên semantic similarity
        """
        if len(sentences) <= 2:
            return [' '.join(sentences)] if sentences else []
        
        groups = []
        current_group = [sentences[0]]
        
        for i in range(1, len(sentences)):
            # Simple semantic similarity check
            similarity = self._calculate_semantic_similarity(
                current_group[-1], 
                sentences[i]
            )
            
            if similarity > self.config.get("semantic_threshold", 0.7):
                current_group.append(sentences[i])
            else:
                # Start new group
                if current_group:
                    groups.append(' '.join(current_group))
                current_group = [sentences[i]]
        
        # Add last group
        if current_group:
            groups.append(' '.join(current_group))
        
        return groups
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity giữa 2 texts - IMPROVED
        """
        # Word overlap approach
        words1 = set(re.findall(r'\b\w+\b', text1.lower()))
        words2 = set(re.findall(r'\b\w+\b', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1 & words2)
        union = len(words1 | words2)
        
        jaccard_similarity = intersection / union if union > 0 else 0.0
        
        # IMPROVED: Boost similarity cho technical terms
        technical_boost = 0.0
        for term in self.technical_terms:
            if term.lower() in text1.lower() and term.lower() in text2.lower():
                technical_boost += 0.3
        
        # Domain boost
        domain_boost = 0.0
        for domain, terms in self.domain_terms.items():
            text1_has_domain = any(term in text1.lower() for term in terms)
            text2_has_domain = any(term in text2.lower() for term in terms)
            if text1_has_domain and text2_has_domain:
                domain_boost += 0.2
        
        return min(1.0, jaccard_similarity + technical_boost + domain_boost)
    
    async def _analyze_chunk(self, chunk_text: str, chunk_index: int, all_chunks: List[str]) -> ChunkAnalysis:
        """
        Deep analysis của một chunk
        """
        chunk_id = f"chunk_{chunk_index:03d}"
        
        # Detect chunk type
        chunk_type = self._detect_chunk_type(chunk_text)
        
        # Analyze semantic complexity
        complexity = self._analyze_semantic_complexity(chunk_text)
        
        # Extract key concepts - IMPROVED
        key_concepts = self._extract_key_concepts_improved(chunk_text)
        
        # Calculate transformation potential
        transformation_potential = self._calculate_transformation_potential(
            chunk_text, chunk_type, complexity
        )
        
        # Calculate scores
        topic_score = self._calculate_topic_importance(chunk_text, all_chunks)
        coherence_score = self._calculate_chunk_coherence(chunk_text)
        
        return ChunkAnalysis(
            chunk_id=chunk_id,
            content=chunk_text,
            chunk_type=chunk_type,
            semantic_complexity=complexity,
            key_concepts=key_concepts,
            relationships=[],  # Sẽ fill sau
            topic_score=topic_score,
            coherence_score=coherence_score,
            transformation_potential=transformation_potential,
            metadata={
                "word_count": len(chunk_text.split()),
                "char_count": len(chunk_text),
                "sentence_count": len(self._split_sentences(chunk_text)),
                "index": chunk_index
            }
        )
    
    def _extract_key_concepts_improved(self, text: str) -> List[str]:
        """Extract key concepts từ text - IMPROVED"""
        concepts = []
        
        # 1. Extract technical terms
        for term in self.technical_terms:
            if term.lower() in text.lower():
                concepts.append(term)
        
        # 2. Extract domain terms
        for domain, terms in self.domain_terms.items():
            for term in terms:
                if term.lower() in text.lower():
                    concepts.append(term)
        
        # 3. Extract proper nouns (capitalized words)
        proper_nouns = re.findall(r'\b[A-ZÁĂÂÉÊÍÔƠƯÝ][a-záăâéêíôơưý]+\b', text)
        concepts.extend(proper_nouns)
        
        # 4. Extract important Vietnamese words
        important_words = re.findall(r'\b(?:công nghệ|hệ thống|phương pháp|giải pháp|ứng dụng|phát triển)\b', text, re.IGNORECASE)
        concepts.extend(important_words)
        
        # Remove duplicates và filter
        unique_concepts = []
        seen = set()
        for concept in concepts:
            concept_lower = concept.lower()
            if concept_lower not in seen and len(concept) > 2:
                unique_concepts.append(concept)
                seen.add(concept_lower)
        
        # Sort by length (longer terms more important)
        unique_concepts.sort(key=len, reverse=True)
        
        return unique_concepts[:5]  # Top 5 concepts
    
    def _detect_chunk_type(self, text: str) -> ChunkType:
        """Detect loại chunk bằng AI patterns"""
        scores = {}
        
        for chunk_type, patterns in self.chunk_type_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            scores[chunk_type] = score
        
        if not any(scores.values()):
            return ChunkType.MAIN_CONCEPT  # Default
        
        return max(scores, key=scores.get)
    
    def _analyze_semantic_complexity(self, text: str) -> SemanticComplexity:
        """Analyze mức độ phức tạp semantic"""
        scores = {complexity: 0 for complexity in SemanticComplexity}
        
        for complexity, indicators in self.complexity_indicators.items():
            for indicator in indicators:
                matches = len(re.findall(indicator, text, re.IGNORECASE))
                scores[complexity] += matches
        
        # Adjust based on technical terms
        technical_count = sum(1 for term in self.technical_terms if term.lower() in text.lower())
        if technical_count >= 3:
            scores[SemanticComplexity.COMPLEX] += 2
        elif technical_count >= 1:
            scores[SemanticComplexity.MODERATE] += 1
        
        # Default based on length
        word_count = len(text.split())
        if word_count > 100:
            scores[SemanticComplexity.COMPLEX] += 1
        elif word_count > 50:
            scores[SemanticComplexity.MODERATE] += 1
        else:
            scores[SemanticComplexity.SIMPLE] += 1
        
        return max(scores, key=scores.get)
    
    def _calculate_transformation_potential(self, text: str, chunk_type: ChunkType, 
                                          complexity: SemanticComplexity) -> Dict[str, float]:
        """Calculate phù hợp cho các transformation formats"""
        
        potential = {
            "podcast_script": 0.5,
            "video_scenario": 0.5,
            "education_module": 0.5,
            "social_media": 0.5,
            "presentation": 0.5,
            "summary": 0.5
        }
        
        # Adjust based on chunk type
        type_adjustments = {
            ChunkType.INTRODUCTION: {
                "podcast_script": 0.4,
                "video_scenario": 0.3,
                "presentation": 0.4
            },
            ChunkType.EXAMPLE: {
                "education_module": 0.4,
                "video_scenario": 0.3,
                "social_media": 0.2
            },
            ChunkType.EXPLANATION: {
                "education_module": 0.4,
                "podcast_script": 0.3
            },
            ChunkType.CONCLUSION: {
                "summary": 0.4,
                "presentation": 0.3
            },
            ChunkType.DEFINITION: {
                "education_module": 0.4,
                "presentation": 0.3
            }
        }
        
        if chunk_type in type_adjustments:
            for format_type, adjustment in type_adjustments[chunk_type].items():
                potential[format_type] = min(1.0, potential[format_type] + adjustment)
        
        # Adjust based on complexity
        complexity_adjustments = {
            SemanticComplexity.SIMPLE: {"social_media": 0.2},
            SemanticComplexity.EXPERT: {"education_module": 0.2, "presentation": 0.2}
        }
        
        if complexity in complexity_adjustments:
            for format_type, adjustment in complexity_adjustments[complexity].items():
                potential[format_type] = min(1.0, potential[format_type] + adjustment)
        
        return potential
    
    def _calculate_topic_importance(self, chunk_text: str, all_chunks: List[str]) -> float:
        """Calculate tầm quan trọng của chunk trong document"""
        chunk_concepts = set(self._extract_key_concepts_improved(chunk_text))
        
        if not chunk_concepts:
            return 0.5
        
        all_text = ' '.join(all_chunks)
        
        importance_score = 0.0
        for concept in chunk_concepts:
            frequency = all_text.lower().count(concept.lower())
            # Normalize by document length
            normalized_freq = frequency / max(1, len(all_chunks))
            importance_score += min(1.0, normalized_freq * 2)
        
        return min(1.0, importance_score / len(chunk_concepts))
    
    def _calculate_chunk_coherence(self, text: str) -> float:
        """Calculate internal coherence của chunk"""
        sentences = self._split_sentences(text)
        
        if len(sentences) <= 1:
            return 1.0
        
        # Calculate average similarity between consecutive sentences
        similarities = []
        for i in range(len(sentences) - 1):
            sim = self._calculate_semantic_similarity(sentences[i], sentences[i + 1])
            similarities.append(sim)
        
        return sum(similarities) / len(similarities) if similarities else 1.0
    
    async def _analyze_document_structure(self, chunks: List[ChunkAnalysis], 
                                        full_text: str) -> DocumentStructure:
        """Analyze overall document structure"""
        
        # Extract main topics
        all_concepts = []
        for chunk in chunks:
            all_concepts.extend(chunk.key_concepts)
        
        # Count concept frequency
        concept_frequency = {}
        for concept in all_concepts:
            concept_frequency[concept] = concept_frequency.get(concept, 0) + 1
        
        # Top topics
        main_topics = [
            concept for concept, freq in 
            sorted(concept_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
            if freq > 1  # Only topics mentioned multiple times
        ]
        
        # Build topic hierarchy (simple version)
        topic_hierarchy = {topic: [] for topic in main_topics}
        
        # Narrative flow
        narrative_flow = [chunk.chunk_id for chunk in chunks]
        
        # Document type detection
        doc_type = self._detect_document_type(chunks)
        
        # Overall complexity
        complexities = [chunk.semantic_complexity for chunk in chunks]
        overall_complexity = max(set(complexities), key=complexities.count)
        
        return DocumentStructure(
            main_topics=main_topics,
            topic_hierarchy=topic_hierarchy,
            narrative_flow=narrative_flow,
            key_relationships=[],  # Sẽ fill sau
            document_type=doc_type,
            overall_complexity=overall_complexity
        )
    
    def _detect_document_type(self, chunks: List[ChunkAnalysis]) -> str:
        """Detect document type dựa trên chunk analysis"""
        type_indicators = {
            "educational": 0,
            "technical": 0,
            "narrative": 0,
            "analytical": 0,
            "instructional": 0
        }
        
        for chunk in chunks:
            if chunk.chunk_type == ChunkType.DEFINITION:
                type_indicators["educational"] += 2
            elif chunk.chunk_type == ChunkType.EXPLANATION:
                type_indicators["instructional"] += 2
            elif chunk.chunk_type == ChunkType.EXAMPLE:
                type_indicators["educational"] += 1
            elif chunk.semantic_complexity in [SemanticComplexity.COMPLEX, SemanticComplexity.EXPERT]:
                type_indicators["technical"] += 1
            elif chunk.chunk_type == ChunkType.ARGUMENT:
                type_indicators["analytical"] += 1
        
        return max(type_indicators, key=type_indicators.get)
    
    async def _detect_relationships(self, chunks: List[ChunkAnalysis]):
        """Detect relationships between chunks"""
        for i, chunk1 in enumerate(chunks):
            for j, chunk2 in enumerate(chunks):
                if i != j:
                    # Calculate relationship strength
                    similarity = self._calculate_semantic_similarity(
                        chunk1.content, chunk2.content
                    )
                    
                    if similarity > 0.6:  # Strong relationship threshold
                        chunk1.relationships.append(chunk2.chunk_id)
    
    async def _optimize_chunks(self, chunks: List[ChunkAnalysis]) -> List[ChunkAnalysis]:
        """Optimize chunks dựa trên analysis"""
        optimized = []
        
        for chunk in chunks:
            # Skip very low-quality chunks
            if chunk.coherence_score < 0.2 and chunk.topic_score < 0.2:
                continue
            
            # Keep all other chunks
            optimized.append(chunk)
        
        return optimized
