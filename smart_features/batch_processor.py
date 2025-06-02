# smart_features/batch_processor.py
"""
Smart Batch Processing System
Intelligent handling of multiple documents with optimization
"""

import asyncio
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class BatchStrategy(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"

class Priority(Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class BatchDocument:
    """Single document in batch processing"""
    id: str
    content: str
    target_language: str
    source_language: str = "auto"
    priority: Priority = Priority.NORMAL
    metadata: Dict[str, Any] = None

@dataclass
class BatchResult:
    """Batch processing results"""
    total_documents: int
    successful_translations: int
    failed_translations: int
    total_processing_time: float
    average_quality_score: float
    documents_results: List[Dict[str, Any]]
    optimization_insights: Dict[str, Any]

class SmartBatchProcessor:
    """
    Intelligent batch processing with optimization and prioritization
    """
    
    def __init__(self):
        self.max_concurrent = 3
        self.quality_threshold = 0.8
        self.timeout_per_document = 30
        
        # Performance tracking
        self.processing_stats = {
            'total_processed': 0,
            'avg_processing_time': 0,
            'success_rate': 0
        }
    
    async def process_batch(self, documents: List[BatchDocument], 
                          strategy: BatchStrategy = BatchStrategy.ADAPTIVE) -> BatchResult:
        """
        Process multiple documents with smart optimization
        """
        print(f"📦 Starting batch processing - {len(documents)} documents")
        print(f"🎯 Strategy: {strategy.value}")
        
        start_time = time.time()
        
        # Analyze batch and optimize strategy
        optimized_strategy = self._optimize_batch_strategy(documents, strategy)
        print(f"🧠 Optimized strategy: {optimized_strategy['approach']}")
        
        # Sort documents by priority and complexity
        sorted_documents = self._prioritize_documents(documents)
        
        # Process documents based on strategy
        if optimized_strategy['approach'] == BatchStrategy.SEQUENTIAL:
            results = await self._process_sequential(sorted_documents)
        elif optimized_strategy['approach'] == BatchStrategy.PARALLEL:
            results = await self._process_parallel(sorted_documents)
        else:  # ADAPTIVE
            results = await self._process_adaptive(sorted_documents)
        
        # Calculate batch statistics
        total_time = time.time() - start_time
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful
        
        # Calculate average quality
        quality_scores = [r['quality_score'] for r in results if r['success']]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Generate optimization insights
        insights = self._generate_batch_insights(results, total_time)
        
        print(f"✅ Batch processing complete!")
        print(f"📊 Results: {successful}/{len(documents)} successful")
        print(f"⏱️ Total time: {total_time:.2f}s")
        print(f"📈 Average quality: {avg_quality:.2f}")
        
        return BatchResult(
            total_documents=len(documents),
            successful_translations=successful,
            failed_translations=failed,
            total_processing_time=total_time,
            average_quality_score=avg_quality,
            documents_results=results,
            optimization_insights=insights
        )
    
    def _optimize_batch_strategy(self, documents: List[BatchDocument], 
                               initial_strategy: BatchStrategy) -> Dict[str, Any]:
        """Optimize batch processing strategy based on documents"""
        doc_count = len(documents)
        avg_size = sum(len(doc.content) for doc in documents) / doc_count
        
        # Calculate complexity scores
        complexity_scores = []
        for doc in documents:
            score = self._estimate_document_complexity(doc.content)
            complexity_scores.append(score)
        
        avg_complexity = sum(complexity_scores) / len(complexity_scores)
        
        # Determine optimal strategy
        if doc_count <= 2:
            approach = BatchStrategy.SEQUENTIAL
            reason = "Small batch - sequential processing optimal"
        elif doc_count > 10 and avg_complexity < 0.5:
            approach = BatchStrategy.PARALLEL
            reason = "Large batch with simple documents - parallel processing"
        elif avg_complexity > 0.8:
            approach = BatchStrategy.SEQUENTIAL
            reason = "Complex documents - sequential for quality"
        else:
            approach = BatchStrategy.ADAPTIVE
            reason = "Mixed complexity - adaptive processing"
        
        return {
            'approach': approach,
            'reason': reason,
            'estimated_time': self._estimate_batch_time(documents, approach),
            'complexity_score': avg_complexity
        }
    
    def _prioritize_documents(self, documents: List[BatchDocument]) -> List[BatchDocument]:
        """Sort documents by priority and other factors"""
        priority_order = {
            Priority.URGENT: 4,
            Priority.HIGH: 3,
            Priority.NORMAL: 2,
            Priority.LOW: 1
        }
        
        return sorted(documents, key=lambda doc: (
            priority_order[doc.priority],
            -len(doc.content)  # Smaller documents first within same priority
        ), reverse=True)
    
    async def _process_sequential(self, documents: List[BatchDocument]) -> List[Dict[str, Any]]:
        """Process documents sequentially"""
        results = []
        
        for i, doc in enumerate(documents):
            print(f"🔄 Processing document {i+1}/{len(documents)} (Sequential)")
            result = await self._process_single_document(doc)
            results.append(result)
        
        return results
    
    async def _process_parallel(self, documents: List[BatchDocument]) -> List[Dict[str, Any]]:
        """Process documents in parallel"""
        print(f"⚡ Processing {len(documents)} documents in parallel")
        
        # Create semaphore to limit concurrent processing
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def process_with_semaphore(doc):
            async with semaphore:
                return await self._process_single_document(doc)
        
        # Process all documents concurrently
        tasks = [process_with_semaphore(doc) for doc in documents]
        results = await asyncio.gather(*tasks)
        
        return results
    
    async def _process_adaptive(self, documents: List[BatchDocument]) -> List[Dict[str, Any]]:
        """Process documents with adaptive strategy"""
        results = []
        
        # Split into priority groups
        urgent_docs = [doc for doc in documents if doc.priority == Priority.URGENT]
        other_docs = [doc for doc in documents if doc.priority != Priority.URGENT]
        
        # Process urgent documents first (sequential)
        if urgent_docs:
            print(f"🚨 Processing {len(urgent_docs)} urgent documents first")
            for doc in urgent_docs:
                result = await self._process_single_document(doc)
                results.append(result)
        
        # Process remaining documents in parallel
        if other_docs:
            print(f"⚡ Processing {len(other_docs)} remaining documents in parallel")
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def process_with_semaphore(doc):
                async with semaphore:
                    return await self._process_single_document(doc)
            
            tasks = [process_with_semaphore(doc) for doc in other_docs]
            parallel_results = await asyncio.gather(*tasks)
            results.extend(parallel_results)
        
        return results
    
    async def _process_single_document(self, document: BatchDocument) -> Dict[str, Any]:
        """Process a single document"""
        start_time = time.time()
        
        try:
            # Simulate document processing
            await asyncio.sleep(0.3)  # Simulate processing time
            
            # Mock translation result
            import random
            quality_score = 0.8 + (random.random() * 0.15)  # 0.8-0.95
            
            processing_time = time.time() - start_time
            
            return {
                'document_id': document.id,
                'success': True,
                'translated_text': f"[BATCH TRANSLATION] {document.content}",
                'quality_score': quality_score,
                'processing_time': processing_time,
                'target_language': document.target_language,
                'priority': document.priority.value,
                'error': None
            }
            
        except Exception as e:
            processing_time = time.time() - start_time
            return {
                'document_id': document.id,
                'success': False,
                'translated_text': '',
                'quality_score': 0,
                'processing_time': processing_time,
                'target_language': document.target_language,
                'priority': document.priority.value,
                'error': str(e)
            }
    
    def _estimate_document_complexity(self, content: str) -> float:
        """Estimate document complexity (0-1)"""
        # Simple complexity estimation
        word_count = len(content.split())
        char_count = len(content)
        
        # Factors that increase complexity
        complexity_score = 0
        
        # Length factor
        if word_count > 500:
            complexity_score += 0.3
        elif word_count > 200:
            complexity_score += 0.1
        
        # Special characters
        special_chars = len([c for c in content if not c.isalnum() and c not in ' .,!?'])
        if special_chars > char_count * 0.1:
            complexity_score += 0.2
        
        # Technical terms (simple check)
        technical_terms = ['API', 'algorithm', 'function', 'database', 'implementation']
        tech_count = sum(1 for term in technical_terms if term.lower() in content.lower())
        complexity_score += min(tech_count * 0.1, 0.3)
        
        return min(complexity_score, 1.0)
    
    def _estimate_batch_time(self, documents: List[BatchDocument], 
                           strategy: BatchStrategy) -> float:
        """Estimate total batch processing time"""
        individual_times = []
        
        for doc in documents:
            complexity = self._estimate_document_complexity(doc.content)
            base_time = len(doc.content.split()) * 0.02  # 0.02s per word
            estimated_time = base_time * (1 + complexity)
            individual_times.append(estimated_time)
        
        if strategy == BatchStrategy.SEQUENTIAL:
            return sum(individual_times)
        elif strategy == BatchStrategy.PARALLEL:
            return max(individual_times)  # Limited by slowest document
        else:  # ADAPTIVE
            return sum(individual_times) * 0.7  # 30% improvement from adaptive
    
    def _generate_batch_insights(self, results: List[Dict[str, Any]], 
                               total_time: float) -> Dict[str, Any]:
        """Generate optimization insights from batch results"""
        successful_results = [r for r in results if r['success']]
        
        insights = {
            'processing_efficiency': len(successful_results) / len(results),
            'average_processing_time': total_time / len(results),
            'quality_distribution': {
                'excellent': len([r for r in successful_results if r['quality_score'] > 0.9]),
                'good': len([r for r in successful_results if 0.8 <= r['quality_score'] <= 0.9]),
                'acceptable': len([r for r in successful_results if r['quality_score'] < 0.8])
            },
            'recommendations': []
        }
        
        # Generate recommendations
        if insights['processing_efficiency'] < 0.9:
            insights['recommendations'].append("Consider reviewing failed documents for patterns")
        
        if insights['average_processing_time'] > 2.0:
            insights['recommendations'].append("Consider optimizing document complexity or using parallel processing")
        
        if insights['quality_distribution']['acceptable'] > len(successful_results) * 0.2:
            insights['recommendations'].append("Consider using higher quality models for better results")
        
        return insights
