"""
Context Awareness Engine
AI system for document-wide understanding and cross-chunk intelligence
"""

import time
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import re
import asyncio


class ContextType(Enum):
    """Types of context relationships"""
    SEQUENTIAL = "sequential"       # Time-based sequence
    CAUSAL = "causal"              # Cause-effect relationship
    COMPARATIVE = "comparative"     # Comparison between concepts
    DEFINITIONAL = "definitional"   # Definition relationships
    EXEMPLIFICATION = "exemplification"  # Example relationships
    ELABORATION = "elaboration"     # Further explanation
    CONTRADICTION = "contradiction" # Conflicting information
    SUMMARY = "summary"            # Summary relationships


class ContextScope(Enum):
    """Scope of context awareness"""
    LOCAL = "local"          # Within nearby chunks
    SECTION = "section"      # Within document section
    DOCUMENT = "document"    # Entire document
    CROSS_DOC = "cross_doc"  # Across multiple documents


@dataclass
class ContextRelation:
    """Relationship between chunks or concepts"""
    source_chunk_id: str
    target_chunk_id: str
    relation_type: ContextType
    confidence: float
    description: str
    evidence: List[str] = field(default_factory=list)


@dataclass
class ConceptTracker:
    """Track concept throughout document"""
    concept_name: str
    first_mention_chunk: str
    definitions: List[str] = field(default_factory=list)
    examples: List[str] = field(default_factory=list)
    related_concepts: Set[str] = field(default_factory=set)
    chunk_appearances: List[str] = field(default_factory=list)
    consistency_score: float = 1.0


@dataclass
class DocumentContext:
    """Complete document context information"""
    document_id: str
    main_themes: List[str]
    concept_map: Dict[str, ConceptTracker]
    chunk_relations: List[ContextRelation]
    narrative_flow: List[str]
    consistency_issues: List[str]
    processing_metadata: Dict[str, Any]


class ContextAwarenessEngine:
    """
    AI engine for document-wide context understanding
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Default configuration
        self.default_config = {
            "enable_cross_chunk_analysis": True,
            "enable_concept_tracking": True,
            "enable_consistency_check": True,
            "context_window_size": 5,  # Number of chunks to consider for local context
            "concept_similarity_threshold": 0.7,
            "relation_confidence_threshold": 0.6
        }
        self.config = {**self.default_config, **self.config}
        
        # Document memory storage
        self.document_contexts: Dict[str, DocumentContext] = {}
        self.global_concept_registry: Dict[str, Set[str]] = {}  # concept -> documents
        
        # Initialize context patterns
        self._init_context_patterns()
    
    def _init_context_patterns(self):
        """Initialize patterns for context detection"""
        
        # Patterns to detect different types of relationships
        self.relation_patterns = {
            ContextType.SEQUENTIAL: [
                r"\b(trước đó|sau đó|tiếp theo|cuối cùng|đầu tiên)\b",
                r"\b(bước \d+|giai đoạn|phase)\b",
                r"\b(sau khi|trước khi|trong khi)\b"
            ],
            ContextType.CAUSAL: [
                r"\b(do đó|vì vậy|kết quả là|dẫn đến)\b",
                r"\b(bởi vì|do|vì|nguyên nhân)\b",
                r"\b(gây ra|tạo ra|sinh ra|dẫn tới)\b"
            ],
            ContextType.COMPARATIVE: [
                r"\b(so với|khác với|tương tự|giống như)\b",
                r"\b(trong khi|ngược lại|trái lại)\b",
                r"\b(hơn|kém|bằng|tốt hơn|xấu hơn)\b"
            ],
            ContextType.DEFINITIONAL: [
                r"\b(là|được định nghĩa|có nghĩa là|chính là)\b",
                r"\b(khái niệm|định nghĩa|thuật ngữ)\b",
                r"\b(được hiểu là|được gọi là)\b"
            ],
            ContextType.EXEMPLIFICATION: [
                r"\b(ví dụ|chẳng hạn|như|cụ thể)\b",
                r"\b(minh họa|thể hiện|cho thấy)\b",
                r"\b(trường hợp|tình huống|case)\b"
            ],
            ContextType.ELABORATION: [
                r"\b(hơn nữa|bên cạnh đó|ngoài ra)\b",
                r"\b(chi tiết|cụ thể hơn|sâu hơn)\b",
                r"\b(mở rộng|phát triển|bổ sung)\b"
            ],
            ContextType.CONTRADICTION: [
                r"\b(tuy nhiên|nhưng|mặc dù|dù)\b",
                r"\b(ngược lại|trái ngược|mâu thuẫn)\b",
                r"\b(không phải|không đúng|sai)\b"
            ],
            ContextType.SUMMARY: [
                r"\b(tóm lại|kết luận|như vậy)\b",
                r"\b(tổng kết|tổng quát|chung)\b",
                r"\b(nói chung|về cơ bản)\b"
            ]
        }
        
        # Concept detection patterns
        self.concept_patterns = [
            r"\b[A-Z][A-Za-z]*\b",  # Capitalized words
            r"\b(AI|ML|machine learning|deep learning)\b",
            r"\b(công nghệ|technology|hệ thống|system)\b",
            r"\b(thuật toán|algorithm|phương pháp|method)\b"
        ]
        
        # Consistency check patterns
        self.consistency_patterns = {
            "terminology": r"\b(AI|trí tuệ nhân tạo|artificial intelligence)\b",
            "tone": r"\b(bạn|quý vị|chúng ta|tôi|mình)\b",
            "tense": r"\b(sẽ|đã|đang|hiện tại|tương lai|quá khứ)\b"
        }
    
    async def analyze_document_context(self, chunks: List[Any], document_id: str = None) -> DocumentContext:
        """
        Analyze complete document context from chunks
        """
        start_time = time.time()
        
        doc_id = document_id or f"doc_{int(time.time())}"
        
        print(f"🧠 Analyzing document context for {doc_id}...")
        
        # Step 1: Extract and track concepts
        concept_map = await self._extract_and_track_concepts(chunks)
        
        # Step 2: Detect relationships between chunks
        chunk_relations = await self._detect_chunk_relationships(chunks)
        
        # Step 3: Analyze narrative flow
        narrative_flow = await self._analyze_narrative_flow(chunks, chunk_relations)
        
        # Step 4: Identify main themes
        main_themes = await self._identify_main_themes(concept_map, chunks)
        
        # Step 5: Check consistency
        consistency_issues = await self._check_consistency(chunks, concept_map)
        
        # Create document context
        doc_context = DocumentContext(
            document_id=doc_id,
            main_themes=main_themes,
            concept_map=concept_map,
            chunk_relations=chunk_relations,
            narrative_flow=narrative_flow,
            consistency_issues=consistency_issues,
            processing_metadata={
                "total_chunks": len(chunks),
                "total_concepts": len(concept_map),
                "total_relations": len(chunk_relations),
                "processing_time": time.time() - start_time,
                "analysis_timestamp": time.time()
            }
        )
        
        # Store in memory
        self.document_contexts[doc_id] = doc_context
        
        # Update global concept registry
        for concept in concept_map.keys():
            if concept not in self.global_concept_registry:
                self.global_concept_registry[concept] = set()
            self.global_concept_registry[concept].add(doc_id)
        
        print(f"✅ Context analysis completed in {doc_context.processing_metadata['processing_time']:.3f}s")
        print(f"   Concepts tracked: {len(concept_map)}")
        print(f"   Relations found: {len(chunk_relations)}")
        print(f"   Main themes: {len(main_themes)}")
        
        return doc_context
    
    async def _extract_and_track_concepts(self, chunks: List[Any]) -> Dict[str, ConceptTracker]:
        """Extract and track concepts throughout document"""
        concept_map = {}
        
        for chunk in chunks:
            # Extract concepts from chunk content
            chunk_content = chunk.content if hasattr(chunk, 'content') else str(chunk)
            chunk_id = chunk.chunk_id if hasattr(chunk, 'chunk_id') else f"chunk_{chunks.index(chunk)}"
            
            # Find concepts in this chunk
            chunk_concepts = self._extract_concepts_from_text(chunk_content)
            
            for concept in chunk_concepts:
                if concept not in concept_map:
                    # First time seeing this concept
                    concept_map[concept] = ConceptTracker(
                        concept_name=concept,
                        first_mention_chunk=chunk_id,
                        chunk_appearances=[chunk_id]
                    )
                    
                    # Check if this chunk defines the concept
                    if self._is_definition_chunk(chunk_content, concept):
                        concept_map[concept].definitions.append(chunk_content[:200] + "...")
                    
                    # Check if this chunk provides examples
                    if self._is_example_chunk(chunk_content, concept):
                        concept_map[concept].examples.append(chunk_content[:200] + "...")
                
                else:
                    # Concept seen before, track appearance
                    concept_map[concept].chunk_appearances.append(chunk_id)
                    
                    # Update definitions and examples
                    if self._is_definition_chunk(chunk_content, concept):
                        concept_map[concept].definitions.append(chunk_content[:200] + "...")
                    
                    if self._is_example_chunk(chunk_content, concept):
                        concept_map[concept].examples.append(chunk_content[:200] + "...")
        
        # Calculate consistency scores and related concepts
        for concept_name, tracker in concept_map.items():
            tracker.consistency_score = self._calculate_concept_consistency(tracker, chunks)
            tracker.related_concepts = self._find_related_concepts(concept_name, concept_map, chunks)
        
        return concept_map
    
    def _extract_concepts_from_text(self, text: str) -> List[str]:
        """Extract key concepts from text"""
        concepts = []
        
        # Use pre-defined patterns
        for pattern in self.concept_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            concepts.extend(matches)
        
        # Extract technical terms (capitalized consecutive words)
        tech_terms = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        concepts.extend(tech_terms)
        
        # Remove duplicates and filter
        unique_concepts = []
        seen = set()
        for concept in concepts:
            concept_clean = concept.strip().lower()
            if concept_clean not in seen and len(concept_clean) > 2:
                unique_concepts.append(concept)
                seen.add(concept_clean)
        
        return unique_concepts[:10]  # Top 10 concepts per chunk
    
    def _is_definition_chunk(self, text: str, concept: str) -> bool:
        """Check if chunk contains definition of concept"""
        definition_patterns = self.relation_patterns[ContextType.DEFINITIONAL]
        
        # Check if concept appears near definition patterns
        for pattern in definition_patterns:
            if re.search(rf'\b{re.escape(concept)}\b.*{pattern}', text, re.IGNORECASE):
                return True
            if re.search(rf'{pattern}.*\b{re.escape(concept)}\b', text, re.IGNORECASE):
                return True
        
        return False
    
    def _is_example_chunk(self, text: str, concept: str) -> bool:
        """Check if chunk contains examples of concept"""
        example_patterns = self.relation_patterns[ContextType.EXEMPLIFICATION]
        
        # Check if concept appears near example patterns
        for pattern in example_patterns:
            if re.search(rf'\b{re.escape(concept)}\b.*{pattern}', text, re.IGNORECASE):
                return True
            if re.search(rf'{pattern}.*\b{re.escape(concept)}\b', text, re.IGNORECASE):
                return True
        
        return False
    
    def _calculate_concept_consistency(self, tracker: ConceptTracker, chunks: List[Any]) -> float:
        """Calculate how consistently a concept is used"""
        if len(tracker.definitions) <= 1:
            return 1.0  # Only one or no definitions, assume consistent
        
        # Simple consistency check - can be enhanced
        # For now, more definitions = potentially less consistent
        consistency = max(0.1, 1.0 - (len(tracker.definitions) - 1) * 0.2)
        
        return consistency
    
    def _find_related_concepts(self, concept: str, concept_map: Dict[str, ConceptTracker], chunks: List[Any]) -> Set[str]:
        """Find concepts related to given concept"""
        related = set()
        
        concept_tracker = concept_map[concept]
        
        # Find concepts that appear in same chunks
        for other_concept, other_tracker in concept_map.items():
            if other_concept != concept:
                # Check for chunk overlap
                common_chunks = set(concept_tracker.chunk_appearances) & set(other_tracker.chunk_appearances)
                if len(common_chunks) >= 2:  # Appear together in at least 2 chunks
                    related.add(other_concept)
        
        return related
    
    async def _detect_chunk_relationships(self, chunks: List[Any]) -> List[ContextRelation]:
        """Detect relationships between chunks"""
        relations = []
        
        for i, chunk1 in enumerate(chunks):
            for j, chunk2 in enumerate(chunks):
                if i != j and abs(i - j) <= self.config.get("context_window_size", 5):
                    # Analyze relationship between chunk1 and chunk2
                    relation = await self._analyze_chunk_pair(chunk1, chunk2, i, j)
                    if relation and relation.confidence > self.config.get("relation_confidence_threshold", 0.6):
                        relations.append(relation)
        
        return relations
    
    async def _analyze_chunk_pair(self, chunk1: Any, chunk2: Any, idx1: int, idx2: int) -> Optional[ContextRelation]:
        """Analyze relationship between two chunks"""
        content1 = chunk1.content if hasattr(chunk1, 'content') else str(chunk1)
        content2 = chunk2.content if hasattr(chunk2, 'content') else str(chunk2)
        
        chunk_id1 = chunk1.chunk_id if hasattr(chunk1, 'chunk_id') else f"chunk_{idx1:03d}"
        chunk_id2 = chunk2.chunk_id if hasattr(chunk2, 'chunk_id') else f"chunk_{idx2:03d}"
        
        # Detect relationship type and confidence
        best_relation_type = None
        best_confidence = 0.0
        best_evidence = []
        
        for relation_type, patterns in self.relation_patterns.items():
            confidence, evidence = self._calculate_relation_confidence(
                content1, content2, patterns, relation_type
            )
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_relation_type = relation_type
                best_evidence = evidence
        
        if best_confidence > 0.3:  # Minimum threshold
            description = self._generate_relation_description(best_relation_type, chunk_id1, chunk_id2)
            
            return ContextRelation(
                source_chunk_id=chunk_id1,
                target_chunk_id=chunk_id2,
                relation_type=best_relation_type,
                confidence=best_confidence,
                description=description,
                evidence=best_evidence
            )
        
        return None
    
    def _calculate_relation_confidence(self, content1: str, content2: str, 
                                     patterns: List[str], relation_type: ContextType) -> Tuple[float, List[str]]:
        """Calculate confidence for a specific relation type"""
        evidence = []
        score = 0.0
        
        # Check for pattern matches
        for pattern in patterns:
            matches1 = re.findall(pattern, content1, re.IGNORECASE)
            matches2 = re.findall(pattern, content2, re.IGNORECASE)
            
            if matches1:
                evidence.extend([f"Pattern '{pattern}' in chunk 1: {matches1}"])
                score += 0.3
            
            if matches2:
                evidence.extend([f"Pattern '{pattern}' in chunk 2: {matches2}"])
                score += 0.3
        
        # Check for shared concepts
        concepts1 = set(self._extract_concepts_from_text(content1))
        concepts2 = set(self._extract_concepts_from_text(content2))
        shared_concepts = concepts1 & concepts2
        
        if shared_concepts:
            evidence.append(f"Shared concepts: {list(shared_concepts)}")
            score += len(shared_concepts) * 0.1
        
        # Normalize score
        confidence = min(1.0, score)
        
        return confidence, evidence
    
    def _generate_relation_description(self, relation_type: ContextType, chunk_id1: str, chunk_id2: str) -> str:
        """Generate human-readable description of relationship"""
        descriptions = {
            ContextType.SEQUENTIAL: f"{chunk_id1} occurs before {chunk_id2} in sequence",
            ContextType.CAUSAL: f"{chunk_id1} has a causal relationship with {chunk_id2}",
            ContextType.COMPARATIVE: f"{chunk_id1} is compared with {chunk_id2}",
            ContextType.DEFINITIONAL: f"{chunk_id1} provides definition related to {chunk_id2}",
            ContextType.EXEMPLIFICATION: f"{chunk_id1} provides examples for concepts in {chunk_id2}",
            ContextType.ELABORATION: f"{chunk_id1} elaborates on ideas from {chunk_id2}",
            ContextType.CONTRADICTION: f"{chunk_id1} contradicts information in {chunk_id2}",
            ContextType.SUMMARY: f"{chunk_id1} summarizes content from {chunk_id2}"
        }
        
        return descriptions.get(relation_type, f"{chunk_id1} is related to {chunk_id2}")
    
    async def _analyze_narrative_flow(self, chunks: List[Any], relations: List[ContextRelation]) -> List[str]:
        """Analyze the logical flow of information in document"""
        chunk_ids = [chunk.chunk_id if hasattr(chunk, 'chunk_id') else f"chunk_{i:03d}" 
                    for i, chunk in enumerate(chunks)]
        
        # Start with original order
        narrative_flow = chunk_ids.copy()
        
        # Adjust based on detected relationships
        sequential_relations = [r for r in relations if r.relation_type == ContextType.SEQUENTIAL]
        
        # Simple reordering based on sequential relationships
        # More sophisticated logic can be added here
        
        return narrative_flow
    
    async def _identify_main_themes(self, concept_map: Dict[str, ConceptTracker], chunks: List[Any]) -> List[str]:
        """Identify main themes of the document"""
        # Score concepts based on frequency and distribution
        concept_scores = {}
        
        for concept_name, tracker in concept_map.items():
            # Score based on number of appearances
            appearance_score = len(tracker.chunk_appearances)
            
            # Score based on having definitions
            definition_score = len(tracker.definitions) * 2
            
            # Score based on having examples
            example_score = len(tracker.examples)
            
            # Score based on consistency
            consistency_score = tracker.consistency_score * 5
            
            total_score = appearance_score + definition_score + example_score + consistency_score
            concept_scores[concept_name] = total_score
        
        # Get top themes
        sorted_concepts = sorted(concept_scores.items(), key=lambda x: x[1], reverse=True)
        main_themes = [concept for concept, score in sorted_concepts[:5] if score > 3]
        
        return main_themes
    
    async def _check_consistency(self, chunks: List[Any], concept_map: Dict[str, ConceptTracker]) -> List[str]:
        """Check for consistency issues in the document"""
        issues = []
        
        # Check terminology consistency
        terminology_variants = {}
        for concept_name, tracker in concept_map.items():
            # Simple check for AI-related terms
            if any(ai_term in concept_name.lower() for ai_term in ['ai', 'artificial', 'trí tuệ']):
                if 'ai_terms' not in terminology_variants:
                    terminology_variants['ai_terms'] = []
                terminology_variants['ai_terms'].append(concept_name)
        
        # Report terminology issues
        for term_group, variants in terminology_variants.items():
            if len(variants) > 2:
                issues.append(f"Multiple terminology variants for {term_group}: {variants}")
        
        # Check for contradictory relations
        contradiction_relations = [r for r in self.document_contexts.get('current', DocumentContext('', [], {}, [], [], [], {})).chunk_relations 
                                 if r.relation_type == ContextType.CONTRADICTION]
        
        for relation in contradiction_relations:
            issues.append(f"Potential contradiction between {relation.source_chunk_id} and {relation.target_chunk_id}")
        
        return issues
    
    def get_context_summary(self, document_id: str) -> Dict[str, Any]:
        """Get summary of document context"""
        if document_id not in self.document_contexts:
            return {"error": "Document not found"}
        
        context = self.document_contexts[document_id]
        
        return {
            "document_id": document_id,
            "main_themes": context.main_themes,
            "total_concepts": len(context.concept_map),
            "total_relations": len(context.chunk_relations),
            "consistency_issues_count": len(context.consistency_issues),
            "processing_time": context.processing_metadata.get("processing_time", 0),
            "narrative_flow_length": len(context.narrative_flow)
        }
    
    def get_concept_details(self, document_id: str, concept_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific concept"""
        if document_id not in self.document_contexts:
            return {"error": "Document not found"}
        
        context = self.document_contexts[document_id]
        
        if concept_name not in context.concept_map:
            return {"error": "Concept not found"}
        
        tracker = context.concept_map[concept_name]
        
        return {
            "concept_name": tracker.concept_name,
            "first_mention": tracker.first_mention_chunk,
            "total_appearances": len(tracker.chunk_appearances),
            "definitions_count": len(tracker.definitions),
            "examples_count": len(tracker.examples),
            "related_concepts": list(tracker.related_concepts),
            "consistency_score": tracker.consistency_score,
            "chunk_appearances": tracker.chunk_appearances
        }
