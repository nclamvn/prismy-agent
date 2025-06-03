# test_advanced_processing.py
"""
Test Advanced Document Processing Features
Tests PDF tables, DOCX structures, Excel formulas
"""

import asyncio
from processors.advanced_document_processor import AdvancedDocumentProcessor
from engines.semantic_chunking_enhanced import EnhancedSemanticChunkingEngine
from core.base_classes import DocumentType

def test_advanced_processor():
    """Test the advanced document processor"""
    print("🧪 Testing Advanced Document Processor...")
    
    processor = AdvancedDocumentProcessor()
    
    # Test with sample text content containing tables and formulas
    sample_content = """
# Sample Document with Advanced Features

This is a test document with various advanced elements.

=== TABLE 1 ===
Name        Age     City
John        25      New York
Jane        30      Los Angeles
Bob         35      Chicago

The formula =SUM(B2:B4) calculates the total age.
Another formula: =AVERAGE(B2:B4) gives the average.

## Technical Section

Some technical content with formulas:
- Excel reference: $A$1 + B2
- Range calculation: A1:A10
- Function usage: COUNT(A1:A100)

=== TABLE 2 ===
Product     Price   Quantity
Laptop      1000    5
Phone       500     10
Tablet      300     15

Total value formula: =B2*C2 + B3*C3 + B4*C4
    """
    
    # Test text processing
    result = processor._process_text(sample_content)
    
    print(f"✅ Text Processing Results:")
    print(f"   - Success: {result.success}")
    print(f"   - Content length: {len(result.content)} characters")
    print(f"   - Tables found: {len(result.tables)}")
    print(f"   - Formulas found: {len(result.formulas)}")
    print(f"   - Detected formulas:")
    for formula in result.formulas:
        print(f"     • {formula}")
    
    return result

def test_enhanced_chunking():
    """Test enhanced semantic chunking"""
    print("\n🧠 Testing Enhanced Semantic Chunking...")
    
    chunker = EnhancedSemanticChunkingEngine()
    
    # Sample content with advanced features
    sample_content = """
# Advanced Document Analysis

This document contains various types of content for testing enhanced chunking capabilities.

## Data Analysis Section

=== TABLE 1 ===
Quarter  Revenue  Expenses  Profit
Q1       100000   80000     20000
Q2       120000   85000     35000
Q3       110000   82000     28000
Q4       130000   90000     40000

The quarterly analysis shows growth trends. Using formulas:
- Total Revenue: =SUM(B2:B5) = 460000
- Average Profit: =AVERAGE(D2:D5) = 30750
- Growth Rate: =(B5-B2)/B2*100 = 30%

## Technical Implementation

The system uses advanced algorithms for processing. Key formulas include:
- Performance Index: $A$1 * COUNT(B1:B100)
- Efficiency Ratio: =AVERAGE(A1:A50)/MAX(B1:B50)

=== TABLE 2 ===
Metric      Value    Target   Status
CPU Usage   65%      80%      Good
Memory      4.2GB    8GB      Good
Disk Space  120GB    500GB    Good

This technical data requires careful analysis and translation preservation.
    """
    
    # Test enhanced chunking
    chunks = chunker.chunk_document(sample_content, DocumentType.TXT)
    
    print(f"✅ Enhanced Chunking Results:")
    print(f"   - Total chunks created: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\n📄 Chunk {i+1}:")
        print(f"   - ID: {chunk.chunk_id}")
        print(f"   - Context: {chunk.semantic_context}")
        print(f"   - Confidence: {chunk.confidence_score:.2f}")
        print(f"   - Has tables: {chunk.metadata.get('has_tables', False)}")
        print(f"   - Has formulas: {chunk.metadata.get('has_formulas', False)}")
        print(f"   - Content preview: {chunk.content[:100]}...")
        print(f"   - Relationships: {len(chunk.relationships)} related chunks")
    
    return chunks

async def test_integration():
    """Test integration with translation system"""
    print("\n🔄 Testing Integration with Translation System...")
    
    from translators.professional_translator import ProfessionalTranslator
    
    # Create test chunks with advanced features
    chunker = EnhancedSemanticChunkingEngine()
    sample_content = """
Financial Report Q4 2024

=== TABLE 1 ===
Department   Budget    Actual    Variance
Sales        500000    520000    +20000
Marketing    200000    180000    -20000
Operations   300000    295000    -5000

Key Performance Indicators:
- ROI Formula: =((B2-A2)/A2)*100 = 4%
- Efficiency: =C2/A2 = 1.04
- Total Variance: =SUM(D2:D4) = -5000

This financial data shows positive performance in sales department.
    """
    
    # Create chunks
    chunks = chunker.chunk_document(sample_content, DocumentType.TXT)
    
    # Test translation
    translator = ProfessionalTranslator()
    
    try:
        result = await translator.translate_document(
            chunks, 
            target_language="Vietnamese",
            source_language="English"
        )
        
        print(f"✅ Translation Integration Results:")
        print(f"   - Translation successful: {result.quality_score > 0}")
        print(f"   - Quality score: {result.quality_score:.2f}")
        print(f"   - Processing time: {result.processing_time:.2f}s")
        print(f"   - Chunks processed: {len(result.chunk_results)}")
        print(f"   - Translation preview: {result.translated_text[:200]}...")
        
    except Exception as e:
        print(f"⚠️ Translation test error: {e}")

def main():
    """Main test function"""
    print("🚀 Starting Advanced Document Processing Tests...")
    print("=" * 60)
    
    # Test 1: Advanced Processor
    processor_result = test_advanced_processor()
    
    # Test 2: Enhanced Chunking
    chunking_result = test_enhanced_chunking()
    
    # Test 3: Integration
    asyncio.run(test_integration())
    
    print("\n" + "=" * 60)
    print("🎯 Test Summary:")
    print(f"   - Advanced Processor: {'✅ PASS' if processor_result.success else '❌ FAIL'}")
    print(f"   - Enhanced Chunking: {'✅ PASS' if len(chunking_result) > 0 else '❌ FAIL'}")
    print(f"   - Formula Detection: {'✅ PASS' if len(processor_result.formulas) > 0 else '❌ FAIL'}")
    print("\n🎉 Advanced Document Processing Tests Complete!")

if __name__ == "__main__":
    main()
