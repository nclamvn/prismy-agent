# engines/semantic_chunking.py
"""
Semantic Chunking Engine™
Advanced document segmentation with semantic awareness
Core innovation of SDIP platform
"""

import re
import hashlib
from typing import List, Dict, Any, Tuple, Optional
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# Import our base classes
from core.base_classes import BaseSemanticChunker, SemanticChunk, DocumentType
from config.settings import config

class SemanticChunkingEngine(BaseSemanticChunker):
    """
    Professional-grade Semantic Chunking Engine™
    
    Features:
    - Context-aware segmentation
    - Document structure recognition  
    - Semantic relationship mapping
    - Optimal chunk boundary detection
    """
    
    def __init__(self):
        self.config = config.chunking
        self._download_nltk_data()
        
        # Patterns for document structure recognition
        self.header_patterns = [
            r'^#{1,6}\s+(.+)$',  # Markdown headers
            r'^([A-Z][A-Z\s]+)$',  # ALL CAPS headers  
            r'^\d+\.\s+(.+)$',   # Numbered sections
            r'^[A-Z][^.!?]*:$',  # Title case with colon
        ]
        
        self.list_patterns = [
            r'^\s*[-*+]\s+(.+)$',  # Bullet points
            r'^\s*\d+\.\s+(.+)$',  # Numbered lists
            r'^\s*[a-zA-Z]\.\s+(.+)$',  # Letter lists
        ]
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            print("📚 Downloading NLTK punkt tokenizer...")
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("📚 Downloading NLTK stopwords...")
            nltk.download('stopwords')
        
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
    
    def chunk_document(self, content: str, doc_type: DocumentType) -> List[SemanticChunk]:
        """
        Main chunking method - breaks document into semantic chunks
        This is the heart of the Semantic Chunking Engine™
        """
        print(f"🔍 Starting semantic chunking for {doc_type.value} document...")
        
        # Step 1: Preprocess content
        processed_content = self._preprocess_content(content)
        
        # Step 2: Identify document structure
        structure_map = self._analyze_document_structure(processed_content)
        
        # Step 3: Create initial chunks
        initial_chunks = self._create_structural_chunks(processed_content, structure_map)
        
        # Step 4: Analyze relationships
        relationship_map = self.analyze_semantic_relationships(initial_chunks)
        
        # Step 5: Update with relationships
        final_chunks = self._update_chunk_relationships(initial_chunks, relationship_map)
        
        print(f"✅ Created {len(final_chunks)} semantic chunks")
        return final_chunks
    
    def _preprocess_content(self, content: str) -> str:
        """Preprocess content for better chunking"""
        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content)
        return content.strip()
    
    def _analyze_document_structure(self, content: str) -> Dict[str, Any]:
        """Analyze document structure to identify semantic units"""
        structure = {
            'headers': [],
            'paragraphs': [],
            'lists': []
        }
        
        lines = content.split('\n')
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Check for headers
            if self._is_header(line):
                structure['headers'].append({
                    'line_num': i,
                    'text': line,
                    'level': self._get_header_level(line)
                })
            
            # Check for lists
            elif self._is_list_item(line):
                structure['lists'].append({
                    'line_num': i,
                    'text': line,
                    'type': self._get_list_type(line)
                })
            
            # Regular paragraph
            else:
                structure['paragraphs'].append({
                    'line_num': i,
                    'text': line
                })
        
        return structure
    
    def _is_header(self, line: str) -> bool:
        """Check if line is a header"""
        for pattern in self.header_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _get_header_level(self, line: str) -> int:
        """Get header importance level (1 = most important)"""
        if line.startswith('#'):
            return line.count('#')
        elif line.isupper():
            return 2
        elif re.match(r'^\d+\.\s+', line):
            return 3
        return 4
    
    def _is_list_item(self, line: str) -> bool:
        """Check if line is a list item"""
        for pattern in self.list_patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _get_list_type(self, line: str) -> str:
        """Determine list type"""
        if re.match(r'^\s*[-*+]\s+', line):
            return 'bullet'
        elif re.match(r'^\s*\d+\.\s+', line):
            return 'numbered'
        return 'lettered'
    
    def _create_structural_chunks(self, content: str, structure: Dict) -> List[SemanticChunk]:
        """Create initial chunks based on document structure"""
        chunks = []
        sentences = sent_tokenize(content)
        
        current_chunk = ""
        chunk_sentences = []
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            potential_chunk = current_chunk + " " + sentence if current_chunk else sentence
            
            if len(potential_chunk) > self.config.max_chunk_size and current_chunk:
                # Create chunk with current content
                chunk = self._create_chunk(
                    content=current_chunk.strip(),
                    context="paragraph",
                    position=len(chunks),
                    metadata={
                        'sentence_count': len(chunk_sentences),
                        'type': 'content_chunk'
                    }
                )
                chunks.append(chunk)
                
                # Start new chunk
                current_chunk = sentence
                chunk_sentences = [sentence]
            else:
                current_chunk = potential_chunk
                chunk_sentences.append(sentence)
        
        # Add final chunk
        if current_chunk.strip():
            chunk = self._create_chunk(
                content=current_chunk.strip(),
                context="paragraph",
                position=len(chunks),
                metadata={
                    'sentence_count': len(chunk_sentences),
                    'type': 'content_chunk'
                }
            )
            chunks.append(chunk)
        
        return chunks
    
    def _create_chunk(self, content: str, context: str, position: int, 
                     metadata: Dict = None) -> SemanticChunk:
        """Create a SemanticChunk object"""
        chunk_id = self._generate_chunk_id(content, position)
        confidence = self._calculate_semantic_confidence(content, context)
        
        return SemanticChunk(
            content=content,
            chunk_id=chunk_id,
            semantic_context=context,
            position=position,
            relationships=[],
            metadata=metadata or {},
            confidence_score=confidence
        )
    
    def _generate_chunk_id(self, content: str, position: int) -> str:
        """Generate unique chunk ID"""
        content_hash = hashlib.md5(content[:100].encode()).hexdigest()[:8]
        return f"chunk_{position:03d}_{content_hash}"
    
    def _calculate_semantic_confidence(self, content: str, context: str) -> float:
        """Calculate semantic coherence confidence score"""
        confidence = 0.5  # Base confidence
        
        # Boost confidence for structured content
        if context in ['section', 'header']:
            confidence += 0.2
        
        # Check sentence coherence
        sentences = sent_tokenize(content)
        if len(sentences) > 1:
            coherence_indicators = ['however', 'therefore', 'moreover', 'furthermore']
            coherence_count = sum(1 for sentence in sentences 
                                for indicator in coherence_indicators 
                                if indicator in sentence.lower())
            coherence_ratio = coherence_count / len(sentences)
            confidence += min(coherence_ratio * 0.3, 0.3)
        
        return max(0.1, min(1.0, confidence))
    
    def analyze_semantic_relationships(self, chunks: List[SemanticChunk]) -> Dict[str, List[str]]:
        """Analyze relationships between chunks"""
        relationships = {}
        
        for i, chunk in enumerate(chunks):
            related_chunks = []
            
            # Simple keyword-based relationship detection
            chunk_words = set(word.lower() for word in word_tokenize(chunk.content) 
                            if word.isalnum() and word.lower() not in self.stop_words)
            
            for j, other_chunk in enumerate(chunks):
                if i != j:
                    other_words = set(word.lower() for word in word_tokenize(other_chunk.content) 
                                    if word.isalnum() and word.lower() not in self.stop_words)
                    
                    if chunk_words and other_words:
                        overlap = len(chunk_words.intersection(other_words))
                        total_unique = len(chunk_words.union(other_words))
                        similarity = overlap / total_unique if total_unique > 0 else 0
                        
                        if similarity > 0.2:  # 20% similarity threshold
                            related_chunks.append(other_chunk.chunk_id)
            
            relationships[chunk.chunk_id] = related_chunks
        
        return relationships
    
    def _update_chunk_relationships(self, chunks: List[SemanticChunk], 
                                  relationships: Dict[str, List[str]]) -> List[SemanticChunk]:
        """Update chunks with relationship information"""
        for chunk in chunks:
            if chunk.chunk_id in relationships:
                chunk.relationships = relationships[chunk.chunk_id]
        
        return chunks
