from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from .text_chunker import SmartTextChunkerEnhanced, ChunkResult, ChunkMetadata
from processors.formula_processor import FormulaProcessor, Formula
import re
import logging
import json

logger = logging.getLogger(__name__)

@dataclass
class LayoutElement:
    """Represents a structural element in the document layout"""
    element_type: str  # 'paragraph', 'table', 'heading', 'list', etc.
    content: str
    metadata: Dict[str, Any]
    position: Tuple[int, int]  # start, end positions
    confidence: float

@dataclass
class FormulaElement(LayoutElement):
    """Layout element specifically for formulas"""
    formula: Formula

@dataclass
class LayoutChunk(ChunkResult):
    """Extended chunk result with layout information"""
    chunk_id: int
    text: str
    main_content: str
    metadata: ChunkMetadata
    context: Optional[str] = None
    layout_elements: List[LayoutElement] = None
    structure_type: str = 'paragraph'
    layout_metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.layout_elements is None:
            self.layout_elements = []
        if self.layout_metadata is None:
            self.layout_metadata = {}

class LayoutAwareChunker(SmartTextChunkerEnhanced):
    """Enhanced text chunker that preserves document layout and structure"""
    
    def __init__(
        self,
        max_chunk_size: int = 2800,
        overlap_size: int = 150,
        preserve_tables: bool = True,
        respect_headings: bool = True,
        handle_formulas: bool = True
    ):
        super().__init__(max_chunk_size, overlap_size)
        self.preserve_tables = preserve_tables
        self.respect_headings = respect_headings
        self.handle_formulas = handle_formulas
        
        # Initialize formula processor if needed
        if handle_formulas:
            self.formula_processor = FormulaProcessor()
        
        # Compile additional patterns for structure detection
        self._heading_pattern = re.compile(r'^(?:#{1,6}|\d+\.)\s+.+$', re.MULTILINE)
        self._table_pattern = re.compile(r'\|.+\|')
        self._list_pattern = re.compile(r'^\s*[-*+]\s+.+$', re.MULTILINE)
        
    def _detect_structure(self, text: str) -> List[LayoutElement]:
        """Detect structural elements in the text"""
        elements = []
        
        # Detect formulas if enabled
        if self.handle_formulas:
            formulas = self.formula_processor.detect_formulas(text)
            for formula in formulas:
                elements.append(FormulaElement(
                    element_type='formula',
                    content=formula.original_text,
                    metadata={
                        'formula_type': formula.formula_type,
                        'latex': formula.latex_repr,
                        'mathml': formula.mathml_repr
                    },
                    position=formula.position,
                    confidence=formula.confidence,
                    formula=formula
                ))
        
        # Detect headings
        if self.respect_headings:
            for match in self._heading_pattern.finditer(text):
                elements.append(LayoutElement(
                    element_type='heading',
                    content=match.group(),
                    metadata={'level': len(match.group().split()[0])},
                    position=(match.start(), match.end()),
                    confidence=0.9
                ))
        
        # Detect tables
        if self.preserve_tables:
            table_sections = []
            current_table = []
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                if self._table_pattern.match(line):
                    current_table.append((i, line))
                elif current_table:
                    if len(current_table) > 1:  # Minimum 2 rows for a table
                        start_pos = sum(len(lines[j]) + 1 for j in range(current_table[0][0]))
                        end_pos = start_pos + sum(len(line) + 1 for _, line in current_table)
                        table_content = '\n'.join(line for _, line in current_table)
                        
                        elements.append(LayoutElement(
                            element_type='table',
                            content=table_content,
                            metadata={
                                'rows': len(current_table),
                                'columns': len(current_table[0][1].split('|')) - 2
                            },
                            position=(start_pos, end_pos),
                            confidence=0.85
                        ))
                    current_table = []
        
        # Detect lists
        list_items = []
        for match in self._list_pattern.finditer(text):
            list_items.append(LayoutElement(
                element_type='list_item',
                content=match.group(),
                metadata={'indent': len(match.group()) - len(match.group().lstrip())},
                position=(match.start(), match.end()),
                confidence=0.8
            ))
        
        # Group consecutive list items
        if list_items:
            current_list = [list_items[0]]
            for item in list_items[1:]:
                if item.position[0] - current_list[-1].position[1] <= 2:  # Adjacent items
                    current_list.append(item)
                else:
                    # Add completed list
                    elements.append(LayoutElement(
                        element_type='list',
                        content='\n'.join(item.content for item in current_list),
                        metadata={'items': len(current_list)},
                        position=(current_list[0].position[0], current_list[-1].position[1]),
                        confidence=0.85
                    ))
                    current_list = [item]
            
            # Add final list
            if current_list:
                elements.append(LayoutElement(
                    element_type='list',
                    content='\n'.join(item.content for item in current_list),
                    metadata={'items': len(current_list)},
                    position=(current_list[0].position[0], current_list[-1].position[1]),
                    confidence=0.85
                ))
        
        return sorted(elements, key=lambda x: x.position[0])

    def _create_layout_chunk(
        self,
        text: str,
        start_pos: int,
        end_pos: int,
        chunk_id: int,
        elements: List[LayoutElement],
        placeholders: Dict[str, Formula]
    ) -> LayoutChunk:
        """Create a chunk with layout information and restored formulas"""
        # Get base chunk
        base_chunk = super()._create_chunk(text, start_pos, end_pos, chunk_id)
        
        # Filter elements for this chunk
        chunk_elements = [
            elem for elem in elements
            if start_pos <= elem.position[0] < end_pos
        ]
        
        # Restore formulas if present
        if placeholders:
            chunk_text = self.formula_processor.restore_formulas(
                base_chunk.text, placeholders
            )
            chunk_main_content = self.formula_processor.restore_formulas(
                base_chunk.main_content, placeholders
            )
        else:
            chunk_text = base_chunk.text
            chunk_main_content = base_chunk.main_content
        
        # Determine primary structure type
        structure_counts = {}
        for elem in chunk_elements:
            structure_counts[elem.element_type] = (
                structure_counts.get(elem.element_type, 0) + 1
            )
        
        primary_structure = max(
            structure_counts.items(),
            key=lambda x: x[1]
        )[0] if structure_counts else 'paragraph'
        
        # Create layout metadata
        layout_metadata = {
            'element_counts': structure_counts,
            'layout_confidence': sum(elem.confidence for elem in chunk_elements) / len(chunk_elements)
            if chunk_elements else 0.7,
            'has_formulas': any(
                isinstance(elem, FormulaElement) for elem in chunk_elements
            )
        }
        
        return LayoutChunk(
            chunk_id=chunk_id,
            text=chunk_text,
            main_content=chunk_main_content,
            metadata=base_chunk.metadata,
            context=base_chunk.context,
            layout_elements=chunk_elements,
            structure_type=primary_structure,
            layout_metadata=layout_metadata
        )

    def chunk_text(self, text: str) -> List[LayoutChunk]:
        """Chunk text while preserving layout structure and formulas"""
        if not text:
            raise ValueError("Text cannot be empty")
        
        # Detect structural elements including formulas
        elements = self._detect_structure(text)
        
        # Handle formulas if present
        if self.handle_formulas:
            formula_elements = [
                elem for elem in elements
                if isinstance(elem, FormulaElement)
            ]
            if formula_elements:
                # Replace formulas with placeholders
                formulas = [elem.formula for elem in formula_elements]
                text_with_placeholders, placeholders = (
                    self.formula_processor.replace_formulas_with_placeholders(
                        text, formulas
                    )
                )
            else:
                text_with_placeholders = text
                placeholders = {}
        else:
            text_with_placeholders = text
            placeholders = {}
        
        if len(text_with_placeholders) <= self.max_chunk_size:
            return [self._create_layout_chunk(
                text_with_placeholders, 0, len(text_with_placeholders), 0,
                elements, placeholders
            )]
        
        chunks = []
        chunk_id = 0
        current_pos = 0
        
        while current_pos < len(text_with_placeholders):
            chunk_end = min(current_pos + self.max_chunk_size, len(text_with_placeholders))
            
            # Find optimal cut point considering structure
            optimal_cut = self._find_structure_aware_cut(
                text_with_placeholders, current_pos, chunk_end, elements
            )
            
            chunk = self._create_layout_chunk(
                text_with_placeholders, current_pos, optimal_cut,
                chunk_id, elements, placeholders
            )
            chunks.append(chunk)
            
            current_pos = optimal_cut
            chunk_id += 1
        
        return chunks

    def _find_structure_aware_cut(
        self,
        text: str,
        start: int,
        max_end: int,
        elements: List[LayoutElement]
    ) -> int:
        """Find optimal cut point that respects document structure"""
        # Find elements that span the potential cut point
        spanning_elements = [
            elem for elem in elements
            if elem.position[0] < max_end and elem.position[1] > start
        ]
        
        if not spanning_elements:
            # No structural elements to consider
            return super()._find_optimal_cut_point(text, start, max_end)
        
        # Try to cut after a complete structural element
        for elem in reversed(spanning_elements):
            if elem.position[1] <= max_end:
                return elem.position[1]
        
        # If no good structural boundary found, use normal cut point
        return super()._find_optimal_cut_point(text, start, max_end)

    def to_json(self, chunk: LayoutChunk) -> str:
        """Convert a layout chunk to JSON format"""
        return json.dumps({
            'chunk_id': chunk.chunk_id,
            'text': chunk.text,
            'main_content': chunk.main_content,
            'metadata': vars(chunk.metadata),
            'context': chunk.context,
            'structure_type': chunk.structure_type,
            'layout_metadata': chunk.layout_metadata,
            'layout_elements': [
                {
                    'type': elem.element_type,
                    'content': elem.content,
                    'metadata': elem.metadata,
                    'position': elem.position,
                    'confidence': elem.confidence
                }
                for elem in chunk.layout_elements
            ]
        }, indent=2)
