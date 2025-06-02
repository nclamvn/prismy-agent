# src/infrastructure/formula/formula_processor.py
import re
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass

# Simple path setup
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import or define formula classes
try:
    from src.core.interfaces.document_processing import FormulaProcessor
except ImportError:
    class FormulaProcessor:
        def detect_formulas(self, text):
            pass
        def process_latex(self, formula):
            pass
        def process_mathml(self, formula):
            pass

logger = logging.getLogger(__name__)

@dataclass
class FormulaMatch:
    """Represents a detected formula"""
    text: str
    start_pos: int
    end_pos: int
    formula_type: str
    confidence: float

class STEMFormulaProcessor(FormulaProcessor):
    """Simple formula processor for STEM content"""
    
    def __init__(self):
        """Initialize formula processor"""
        self.latex_patterns = [
            r'\$([^$]+)\$',  # $formula$
            r'\\\(([^\)]+)\\\)',  # \(formula\)
            r'\$\$([^$]+)\$\$',  # $$formula$$
            r'\\frac\{[^}]+\}\{[^}]+\}',  # \frac{a}{b}
            r'\\sqrt\{[^}]+\}',  # \sqrt{x}
        ]
        
        self.math_patterns = [
            r'[a-zA-Z]\s*[=]\s*[^,\n.;]+',  # x = y + z
            r'\b\d+\s*[+\-*/]\s*\d+\b',  # 2 + 3
            r'[∑∏∫∆∇∂]',  # Math symbols
            r'[≤≥≠≈≡∞±×÷√]',  # Math operators
        ]
        
        self.unit_patterns = [
            r'\b\d+\.?\d*\s*(mm|cm|m|km|g|kg|s|min|hr?|Hz|V|A|Ω|°C|°F|K)',
        ]
    
    def detect_formulas(self, text: str) -> List[Dict]:
        """Detect mathematical formulas in text"""
        formulas = []
        
        try:
            # Detect LaTeX formulas
            for pattern in self.latex_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    formulas.append({
                        'text': match.group(0),
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'formula_type': 'latex',
                        'confidence': 0.9
                    })
            
            # Detect math expressions
            for pattern in self.math_patterns:
                matches = re.finditer(pattern, text)
                for match in matches:
                    formulas.append({
                        'text': match.group(0),
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'formula_type': 'math',
                        'confidence': 0.7
                    })
            
            # Detect units
            for pattern in self.unit_patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    formulas.append({
                        'text': match.group(0),
                        'start_pos': match.start(),
                        'end_pos': match.end(),
                        'formula_type': 'unit',
                        'confidence': 0.8
                    })
            
            # Remove overlaps and sort
            formulas = self._remove_overlaps(formulas)
            formulas.sort(key=lambda x: x['start_pos'])
            
            return formulas
            
        except Exception as e:
            logger.error(f"Error detecting formulas: {str(e)}")
            return []
    
    def _remove_overlaps(self, formulas: List[Dict]) -> List[Dict]:
        """Remove overlapping formulas"""
        if not formulas:
            return formulas
        
        formulas.sort(key=lambda x: x['start_pos'])
        filtered = []
        
        for current in formulas:
            overlaps = False
            for existing in filtered:
                if (current['start_pos'] < existing['end_pos'] and 
                    current['end_pos'] > existing['start_pos']):
                    if current['confidence'] > existing['confidence']:
                        filtered.remove(existing)
                        break
                    else:
                        overlaps = True
                        break
            
            if not overlaps:
                filtered.append(current)
        
        return filtered
    
    def process_latex(self, formula: str) -> str:
        """Process LaTeX formula"""
        return f"[LATEX]{formula}[/LATEX]"
    
    def process_mathml(self, formula: str) -> str:
        """Process MathML formula"""
        return f"[MATHML]{formula}[/MATHML]"
    
    def preserve_formulas_in_text(self, text: str) -> tuple:
        """Replace formulas with preservation markers"""
        formulas = self.detect_formulas(text)
        formula_map = {}
        processed_text = text
        
        # Process in reverse order to maintain positions
        for i, formula in enumerate(reversed(formulas)):
            marker = f"[FORMULA_{len(formulas)-i-1}]"
            formula_map[marker] = formula
            
            processed_text = (
                processed_text[:formula['start_pos']] + 
                marker + 
                processed_text[formula['end_pos']:]
            )
        
        return processed_text, formula_map
    
    def restore_formulas_in_text(self, text: str, formula_map: Dict) -> str:
        """Restore preserved formulas"""
        restored_text = text
        for marker, formula_data in formula_map.items():
            if marker in restored_text:
                restored_text = restored_text.replace(marker, formula_data['text'])
        return restored_text

class FormulaProcessorFactory:
    """Factory for creating formula processors"""
    
    @staticmethod
    def create_processor(processor_type: str = "stem"):
        """Create formula processor"""
        if processor_type.lower() == "stem":
            return STEMFormulaProcessor()
        else:
            raise ValueError(f"Unknown processor type: {processor_type}")
    
    @staticmethod
    def get_available_processors() -> List[str]:
        """Get available processors"""
        return ["stem"]
