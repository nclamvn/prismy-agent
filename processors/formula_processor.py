import re
import logging
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import sympy
from latex2mathml.converter import convert as latex_to_mathml
from pix2tex.cli import LatexOCR
import cv2
import numpy as np

logger = logging.getLogger(__name__)

@dataclass
class Formula:
    """Represents a mathematical or scientific formula"""
    original_text: str
    latex_repr: str
    mathml_repr: str
    formula_type: str  # 'math', 'chemistry', 'physics'
    position: Tuple[int, int]  # start, end positions in text
    confidence: float
    metadata: Dict[str, Any]

class FormulaProcessor:
    """Process and preserve mathematical and scientific formulas in documents"""
    
    def __init__(self):
        """Initialize formula processing components"""
        self.latex_ocr = LatexOCR()
        
        # Regular expressions for formula detection
        self.patterns = {
            'inline_latex': r'\$[^$]+\$',
            'display_latex': r'\$\$[^$]+\$\$',
            'chemistry': r'(?:[A-Z][a-z]?\d*)+(?:\s*(?:[-+→⇌⟶⟷]\s*)?(?:[A-Z][a-z]?\d*)+)*',
            'physics': r'[A-Za-z]+\s*=\s*[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?\s*[A-Za-z]*'
        }
        
        # Compile patterns
        self.compiled_patterns = {
            key: re.compile(pattern)
            for key, pattern in self.patterns.items()
        }
        
        logger.info("Formula processor initialized successfully")
    
    def detect_formulas(self, text: str) -> List[Formula]:
        """Detect and extract formulas from text"""
        formulas = []
        
        # Find LaTeX formulas
        for match in self.compiled_patterns['inline_latex'].finditer(text):
            latex = match.group()[1:-1]  # Remove $ delimiters
            try:
                mathml = latex_to_mathml(latex)
                formulas.append(Formula(
                    original_text=match.group(),
                    latex_repr=latex,
                    mathml_repr=mathml,
                    formula_type='math',
                    position=(match.start(), match.end()),
                    confidence=0.95,
                    metadata={'style': 'inline'}
                ))
            except Exception as e:
                logger.warning(f"Failed to convert LaTeX to MathML: {e}")
        
        # Find display-style LaTeX
        for match in self.compiled_patterns['display_latex'].finditer(text):
            latex = match.group()[2:-2]  # Remove $$ delimiters
            try:
                mathml = latex_to_mathml(latex)
                formulas.append(Formula(
                    original_text=match.group(),
                    latex_repr=latex,
                    mathml_repr=mathml,
                    formula_type='math',
                    position=(match.start(), match.end()),
                    confidence=0.95,
                    metadata={'style': 'display'}
                ))
            except Exception as e:
                logger.warning(f"Failed to convert LaTeX to MathML: {e}")
        
        # Find chemical formulas
        for match in self.compiled_patterns['chemistry'].finditer(text):
            formula_text = match.group()
            if self._validate_chemical_formula(formula_text):
                formulas.append(Formula(
                    original_text=formula_text,
                    latex_repr=self._chemical_to_latex(formula_text),
                    mathml_repr='',  # Will be populated if needed
                    formula_type='chemistry',
                    position=(match.start(), match.end()),
                    confidence=0.9,
                    metadata={'elements': self._parse_chemical_elements(formula_text)}
                ))
        
        # Find physics equations
        for match in self.compiled_patterns['physics'].finditer(text):
            formula_text = match.group()
            formulas.append(Formula(
                original_text=formula_text,
                latex_repr=self._physics_to_latex(formula_text),
                mathml_repr='',  # Will be populated if needed
                formula_type='physics',
                position=(match.start(), match.end()),
                confidence=0.85,
                metadata={'units': self._extract_units(formula_text)}
            ))
        
        return sorted(formulas, key=lambda x: x.position[0])
    
    def extract_formulas_from_image(
        self,
        image: np.ndarray,
        formula_type: str = 'math'
    ) -> List[Formula]:
        """Extract formulas from images using OCR"""
        try:
            # Preprocess image
            processed_img = self._preprocess_image(image)
            
            # Use LaTeX OCR
            latex = self.latex_ocr(processed_img)
            
            if latex:
                try:
                    mathml = latex_to_mathml(latex)
                except Exception:
                    mathml = ''
                
                return [Formula(
                    original_text=latex,
                    latex_repr=latex,
                    mathml_repr=mathml,
                    formula_type=formula_type,
                    position=(0, 0),  # Image coordinates could be added if needed
                    confidence=0.8,
                    metadata={'source': 'image_ocr'}
                )]
            
            return []
            
        except Exception as e:
            logger.error(f"Failed to extract formulas from image: {e}")
            return []
    
    def _preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Preprocess image for formula detection"""
        # Convert to grayscale
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(thresh)
        
        return denoised
    
    def _validate_chemical_formula(self, formula: str) -> bool:
        """Validate chemical formula structure"""
        # Basic validation of chemical formula pattern
        elements = re.findall(r'[A-Z][a-z]?\d*', formula)
        return len(elements) > 0
    
    def _parse_chemical_elements(self, formula: str) -> List[Dict[str, Any]]:
        """Parse chemical formula into elements and quantities"""
        elements = []
        matches = re.finditer(r'([A-Z][a-z]?)(\d*)', formula)
        
        for match in matches:
            element = match.group(1)
            quantity = match.group(2)
            elements.append({
                'element': element,
                'quantity': int(quantity) if quantity else 1
            })
        
        return elements
    
    def _chemical_to_latex(self, formula: str) -> str:
        """Convert chemical formula to LaTeX"""
        # Replace numbers with subscripts
        latex = re.sub(r'(\d+)', r'_{\1}', formula)
        # Handle arrows
        latex = latex.replace('→', '\\rightarrow')
        latex = latex.replace('⇌', '\\rightleftharpoons')
        return latex
    
    def _physics_to_latex(self, formula: str) -> str:
        """Convert physics equation to LaTeX"""
        # Handle common physics notation
        latex = formula
        # Handle scientific notation
        latex = re.sub(
            r'(\d+\.?\d*)[eE]([-+]?\d+)',
            r'\1 \\times 10^{\2}',
            latex
        )
        # Handle units
        latex = re.sub(
            r'([A-Za-z]+)(\d+)',
            r'\1^{\2}',
            latex
        )
        return latex
    
    def _extract_units(self, formula: str) -> Dict[str, Any]:
        """Extract and parse units from physics formula"""
        units = re.findall(r'[A-Za-z]+$', formula)
        if units:
            return {'unit': units[0]}
        return {}
    
    def replace_formulas_with_placeholders(
        self,
        text: str,
        formulas: List[Formula]
    ) -> Tuple[str, Dict[str, Formula]]:
        """Replace formulas with placeholders for safe chunking"""
        modified_text = text
        placeholders = {}
        
        # Sort formulas in reverse order to preserve positions
        for formula in sorted(formulas, key=lambda x: x.position[0], reverse=True):
            placeholder = f"[FORMULA_{len(placeholders)}]"
            start, end = formula.position
            modified_text = (
                modified_text[:start] +
                placeholder +
                modified_text[end:]
            )
            placeholders[placeholder] = formula
        
        return modified_text, placeholders
    
    def restore_formulas(
        self,
        text: str,
        placeholders: Dict[str, Formula],
        output_format: str = 'original'
    ) -> str:
        """Restore formulas from placeholders"""
        result = text
        
        for placeholder, formula in placeholders.items():
            if output_format == 'latex':
                replacement = formula.latex_repr
            elif output_format == 'mathml':
                replacement = formula.mathml_repr
            else:
                replacement = formula.original_text
            
            result = result.replace(placeholder, replacement)
        
        return result
    
    def validate_formula(self, formula: Formula) -> bool:
        """Validate formula structure and conversion"""
        try:
            if formula.formula_type == 'math':
                # Try parsing with sympy
                sympy.parse_expr(formula.latex_repr)
            elif formula.formula_type == 'chemistry':
                return self._validate_chemical_formula(formula.original_text)
            return True
        except Exception:
            return False
