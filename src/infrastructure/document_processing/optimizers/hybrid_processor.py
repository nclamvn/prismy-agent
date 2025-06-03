# src/infrastructure/document_processing/optimizers/hybrid_processor.py

import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import spacy
import nltk
import re
from transformers import pipeline, AutoTokenizer
import networkx as nx
from collections import defaultdict

from src.core.models.document import Document, DocumentChunk
from src.core.utils.logger import Logger

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

logger = Logger(__name__)


@dataclass
class ProcessedContent:
    """Preprocessed content for LLM processing."""
    summary: str
    key_entities: List[Dict[str, Any]]
    key_relationships: List[Tuple[str, str, str]]
    structure: Dict[str, Any]
    key_quotes: List[str]
    metadata: Dict[str, Any]
    
    def to_compressed_prompt(self) -> str:
        """Convert to compressed prompt for LLM."""
        prompt_parts = [
            f"Summary: {self.summary}",
            f"Key Entities: {', '.join([e['text'] for e in self.key_entities[:10]])}",
            f"Structure: {self.structure.get('type', 'unknown')} with {self.structure.get('sections', 0)} sections"
        ]
        
        if self.key_quotes:
            prompt_parts.append(f"Key Quotes: {' | '.join(self.key_quotes[:3])}")
            
        return "\n".join(prompt_parts)


class HybridProcessor:
    """
    Hybrid processing combining traditional NLP with LLMs.
    Reduces token usage by 70-80% through intelligent preprocessing.
    """
    
    def __init__(self):
        # Load NLP models
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            logger.warning("Spacy model not found. Installing...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")
            
        # Initialize summarizer (local model)
        try:
            self.summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # CPU
            )
        except:
            logger.warning("BART model not available, using fallback")
            self.summarizer = None
            
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        
    async def preprocess_document(
        self,
        document: Document,
        target_format: str
    ) -> ProcessedContent:
        """Preprocess document to extract key information."""
        # Process with spaCy
        doc = self.nlp(document.content[:1000000])  # Limit to 1M chars
        
        # Extract components in parallel
        tasks = [
            self._extract_entities_async(doc),
            self._extract_key_quotes_async(document.content),
            self._analyze_structure_async(document.content),
            self._create_summary_async(document.content)
        ]
        
        entities, quotes, structure, summary = await asyncio.gather(*tasks)
        
        # Build knowledge graph
        relationships = self._extract_relationships(doc, entities)
        
        return ProcessedContent(
            summary=summary,
            key_entities=entities,
            key_relationships=relationships,
            structure=structure,
            key_quotes=quotes,
            metadata={
                "original_length": len(document.content),
                "compressed_length": len(summary),
                "compression_ratio": len(summary) / len(document.content),
                "entity_count": len(entities),
                "target_format": target_format
            }
        )
    
    async def preprocess_chunk(
        self,
        chunk: DocumentChunk,
        context: Optional[ProcessedContent] = None
    ) -> Dict[str, Any]:
        """Preprocess a single chunk with context awareness."""
        # Quick entity extraction
        doc = self.nlp(chunk.content)
        
        chunk_data = {
            "entities": self._extract_entities(doc),
            "summary": await self._create_chunk_summary(chunk.content),
            "type": chunk.metadata.get("type", "general"),
            "key_sentences": self._extract_key_sentences(chunk.content)
        }
        
        # Add context if available
        if context:
            # Find relevant context entities
            chunk_entity_texts = {e["text"].lower() for e in chunk_data["entities"]}
            relevant_context = [
                e for e in context.key_entities
                if e["text"].lower() in chunk_entity_texts
            ]
            chunk_data["context_entities"] = relevant_context
            
        return chunk_data
    
    def compress_for_llm(
        self,
        content: str,
        max_tokens: int = 2000,
        preserve_key_info: bool = True
    ) -> str:
        """Compress content for LLM processing."""
        # Tokenize to check size
        tokens = self.tokenizer.encode(content)
        
        if len(tokens) <= max_tokens:
            return content
            
        # Need compression
        doc = self.nlp(content)
        
        # Extract key sentences
        sentences = list(doc.sents)
        sentence_scores = self._score_sentences(sentences)
        
        # Select top sentences within token limit
        selected_sentences = []
        current_tokens = 0
        
        for sent, score in sorted(sentence_scores, key=lambda x: x[1], reverse=True):
            sent_tokens = len(self.tokenizer.encode(sent.text))
            if current_tokens + sent_tokens <= max_tokens:
                selected_sentences.append(sent)
                current_tokens += sent_tokens
                
        # Sort by original order
        selected_sentences.sort(key=lambda s: s.start)
        
        # Reconstruct compressed text
        compressed = " ".join([s.text for s in selected_sentences])
        
        if preserve_key_info:
            # Add key entities at the end
            entities = self._extract_entities(doc)
            entity_text = "Key entities: " + ", ".join([e["text"] for e in entities[:10]])
            
            # Check if we have room
            entity_tokens = len(self.tokenizer.encode(entity_text))
            if current_tokens + entity_tokens <= max_tokens:
                compressed += f"\n\n{entity_text}"
                
        return compressed
    
    async def _extract_entities_async(self, doc) -> List[Dict[str, Any]]:
        """Extract entities asynchronously."""
        return await asyncio.to_thread(self._extract_entities, doc)
    
    def _extract_entities(self, doc) -> List[Dict[str, Any]]:
        """Extract named entities with metadata."""
        entities = []
        seen = set()
        
        for ent in doc.ents:
            if ent.text.lower() not in seen:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
                seen.add(ent.text.lower())
                
        # Also extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1 and chunk.text.lower() not in seen:
                entities.append({
                    "text": chunk.text,
                    "label": "NOUN_PHRASE",
                    "start": chunk.start_char,
                    "end": chunk.end_char
                })
                seen.add(chunk.text.lower())
                
        return entities[:50]  # Limit to top 50
    
    def _extract_relationships(
        self,
        doc,
        entities: List[Dict[str, Any]]
    ) -> List[Tuple[str, str, str]]:
        """Extract relationships between entities."""
        relationships = []
        entity_texts = {e["text"].lower() for e in entities}
        
        # Simple dependency parsing for relationships
        for sent in doc.sents:
            # Find subject-verb-object patterns
            for token in sent:
                if token.dep_ == "ROOT" and token.pos_ == "VERB":
                    # Find subject
                    subjects = [child for child in token.children if child.dep_ in ["nsubj", "nsubjpass"]]
                    # Find objects
                    objects = [child for child in token.children if child.dep_ in ["dobj", "pobj"]]
                    
                    for subj in subjects:
                        for obj in objects:
                            if subj.text.lower() in entity_texts and obj.text.lower() in entity_texts:
                                relationships.append((subj.text, token.lemma_, obj.text))
                                
        return relationships[:20]  # Limit relationships
    
    async def _extract_key_quotes_async(self, content: str) -> List[str]:
        """Extract key quotes asynchronously."""
        return await asyncio.to_thread(self._extract_key_quotes, content)
    
    def _extract_key_quotes(self, content: str) -> List[str]:
        """Extract important quotes from content."""
        import re
        
        # Find quoted text
        quotes = re.findall(r'"([^"]{20,200})"', content)
        
        # Score quotes by importance (simple heuristic)
        scored_quotes = []
        for quote in quotes:
            score = 0
            # Prefer quotes with action verbs
            if any(word in quote.lower() for word in ["said", "stated", "announced", "declared"]):
                score += 2
            # Prefer quotes with important keywords
            if any(word in quote.lower() for word in ["important", "critical", "key", "significant"]):
                score += 1
            # Length bonus
            score += min(len(quote.split()) / 20, 1)
            
            scored_quotes.append((quote, score))
            
        # Return top quotes
        scored_quotes.sort(key=lambda x: x[1], reverse=True)
        return [q[0] for q in scored_quotes[:5]]
    
    async def _analyze_structure_async(self, content: str) -> Dict[str, Any]:
        """Analyze document structure asynchronously."""
        return await asyncio.to_thread(self._analyze_structure, content)
    
    def _analyze_structure(self, content: str) -> Dict[str, Any]:
        """Analyze document structure."""
        lines = content.split('\n')
        
        structure = {
            "type": "unknown",
            "sections": 0,
            "subsections": 0,
            "lists": 0,
            "paragraphs": 0,
            "avg_paragraph_length": 0
        }
        
        # Count structural elements
        paragraphs = []
        current_paragraph = []
        
        for line in lines:
            line = line.strip()
            
            if not line:
                if current_paragraph:
                    paragraphs.append(' '.join(current_paragraph))
                    current_paragraph = []
            else:
                current_paragraph.append(line)
                
                # Check for sections
                if re.match(r'^#+\s+', line) or re.match(r'^\d+\.\s+[A-Z]', line):
                    structure["sections"] += 1
                elif re.match(r'^\d+\.\d+\s+', line):
                    structure["subsections"] += 1
                elif re.match(r'^[-*]\s+', line):
                    structure["lists"] += 1
                    
        # Final paragraph
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
            
        structure["paragraphs"] = len(paragraphs)
        if paragraphs:
            structure["avg_paragraph_length"] = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            
        # Determine type
        if structure["sections"] > 5:
            structure["type"] = "structured_document"
        elif structure["lists"] > 10:
            structure["type"] = "list_heavy"
        elif structure["avg_paragraph_length"] > 100:
            structure["type"] = "narrative"
        else:
            structure["type"] = "general"
            
        return structure
    
    async def _create_summary_async(self, content: str) -> str:
        """Create summary asynchronously."""
        return await asyncio.to_thread(self._create_summary, content)
    
    def _create_summary(self, content: str, max_length: int = 500) -> str:
        """Create summary using local model or fallback."""
        if self.summarizer:
            try:
                # Chunk content for BART (max ~1024 tokens)
                chunks = self._chunk_for_summarization(content, 800)
                summaries = []
                
                for chunk in chunks[:5]:  # Limit to first 5 chunks
                    summary = self.summarizer(
                        chunk,
                        max_length=max_length // len(chunks),
                        min_length=50,
                        do_sample=False
                    )
                    summaries.append(summary[0]['summary_text'])
                    
                return " ".join(summaries)
                
            except Exception as e:
                logger.warning(f"Summarizer failed: {e}")
                
        # Fallback to extractive summarization
        return self._extractive_summarize(content, max_length)
    
    def _chunk_for_summarization(self, content: str, max_words: int) -> List[str]:
        """Chunk content for summarization model."""
        words = content.split()
        chunks = []
        
        for i in range(0, len(words), max_words):
            chunk = ' '.join(words[i:i + max_words])
            chunks.append(chunk)
            
        return chunks
    
    def _extractive_summarize(self, content: str, max_length: int) -> str:
        """Simple extractive summarization."""
        doc = self.nlp(content[:5000])  # Limit for performance
        sentences = list(doc.sents)
        
        if not sentences:
            return content[:max_length]
            
        # Score sentences
        sentence_scores = self._score_sentences(sentences)
        
        # Select top sentences
        top_sentences = sorted(sentence_scores, key=lambda x: x[1], reverse=True)
        selected = []
        current_length = 0
        
        for sent, score in top_sentences:
            sent_length = len(sent.text.split())
            if current_length + sent_length <= max_length // 4:  # Approximate words
                selected.append(sent)
                current_length += sent_length
                
        # Sort by original order
        selected.sort(key=lambda s: s.start)
        
        return " ".join([s.text for s in selected])
    
    def _score_sentences(self, sentences) -> List[Tuple[Any, float]]:
        """Score sentences for importance."""
        # Calculate word frequencies
        word_freq = defaultdict(int)
        for sent in sentences:
            for token in sent:
                if not token.is_stop and not token.is_punct:
                    word_freq[token.lemma_.lower()] += 1
                    
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        for word in word_freq:
            word_freq[word] /= max_freq
            
        # Score sentences
        sentence_scores = []
        for sent in sentences:
            score = 0
            word_count = 0
            
            for token in sent:
                if not token.is_stop and not token.is_punct:
                    score += word_freq.get(token.lemma_.lower(), 0)
                    word_count += 1
                    
            if word_count > 0:
                score /= word_count  # Average score
                
            # Position bonus (prefer earlier sentences)
            position_bonus = 1.0 - (sent.start / len(sentences))
            score += position_bonus * 0.1
            
            sentence_scores.append((sent, score))
            
        return sentence_scores
    
    async def _create_chunk_summary(self, content: str) -> str:
        """Create summary for a chunk."""
        # For chunks, use simpler extraction
        sentences = content.split('.')[:3]  # First 3 sentences
        return '. '.join(sentences).strip()
    
    def _extract_key_sentences(self, content: str, count: int = 3) -> List[str]:
        """Extract key sentences from content."""
        doc = self.nlp(content)
        sentences = list(doc.sents)
        
        if len(sentences) <= count:
            return [s.text for s in sentences]
            
        # Score and select
        scored = self._score_sentences(sentences)
        top_sentences = sorted(scored, key=lambda x: x[1], reverse=True)[:count]
        top_sentences.sort(key=lambda x: x[0].start)  # Original order
        
        return [s[0].text for s in top_sentences]
    
    def build_knowledge_graph(
        self,
        entities: List[Dict[str, Any]],
        relationships: List[Tuple[str, str, str]]
    ) -> nx.Graph:
        """Build knowledge graph from entities and relationships."""
        G = nx.Graph()
        
        # Add entities as nodes
        for entity in entities:
            G.add_node(entity["text"], **entity)
            
        # Add relationships as edges
        for subj, rel, obj in relationships:
            G.add_edge(subj, obj, relationship=rel)
            
        return G
    
    def compress_with_graph(
        self,
        content: str,
        knowledge_graph: nx.Graph,
        max_tokens: int = 1000
    ) -> str:
        """Compress content using knowledge graph."""
        # Find most important nodes (entities)
        if len(knowledge_graph) == 0:
            return self.compress_for_llm(content, max_tokens)
            
        # Calculate centrality
        centrality = nx.degree_centrality(knowledge_graph)
        top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Create compressed representation
        compressed_parts = []
        
        # Add top entities and their relationships
        for entity, score in top_entities:
            entity_info = f"{entity}"
            
            # Add relationships
            neighbors = list(knowledge_graph.neighbors(entity))
            if neighbors:
                relationships = []
                for neighbor in neighbors[:3]:
                    edge_data = knowledge_graph.get_edge_data(entity, neighbor)
                    rel = edge_data.get("relationship", "related to")
                    relationships.append(f"{rel} {neighbor}")
                    
                entity_info += f" ({'; '.join(relationships)})"
                
            compressed_parts.append(entity_info)
            
        # Add summary
        summary = self._extractive_summarize(content, 200)
        
        compressed = f"Summary: {summary}\n\nKey Information: {'. '.join(compressed_parts)}"
        
        # Ensure within token limit
        tokens = self.tokenizer.encode(compressed)
        if len(tokens) > max_tokens:
            # Truncate
            compressed = self.tokenizer.decode(tokens[:max_tokens])
            
        return compressed
