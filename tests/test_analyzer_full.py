from smart_features.document_analyzer import IntelligentDocumentAnalyzer

print('🧠 Testing Smart Document Analysis...')
analyzer = IntelligentDocumentAnalyzer()

# Simple test document
test_content = "# AI Translation\n\nArtificial Intelligence has revolutionized translation technology. Modern systems use advanced algorithms and neural networks to process multiple languages simultaneously.\n\n## Key Features\n- Semantic understanding\n- Real-time processing\n- Quality assurance"

print(f'📄 Document length: {len(test_content)} characters')

# Perform analysis
analysis = analyzer.analyze_document(test_content)

print('\n📊 ANALYSIS RESULTS:')
print(f'  - Complexity: {analysis.complexity.value}')
print(f'  - Content Type: {analysis.content_type.value}')
print(f'  - Estimated Time: {analysis.estimated_time:.2f}s')
print(f'  - Confidence Prediction: {analysis.confidence_prediction:.2f}')
print(f'  - Recommended Chunk Size: {analysis.recommended_chunk_size}')
print(f'  - Key Features: {analysis.key_features}')
print(f'  - Optimization Suggestions: {analysis.optimization_suggestions}')

print('\n✅ Smart Analysis Complete!')
