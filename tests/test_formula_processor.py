import pytest
import numpy as np
import cv2
from processors.formula_processor import FormulaProcessor, Formula

@pytest.fixture
def formula_processor():
    return FormulaProcessor()

@pytest.fixture
def sample_math_text():
    return """Consider the quadratic equation $ax^2 + bx + c = 0$ and its solution:
    $$x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$$
    This is known as the quadratic formula."""

@pytest.fixture
def sample_chemistry_text():
    return """The reaction between hydrogen and oxygen:
    2H₂ + O₂ → 2H₂O
    And the equilibrium reaction:
    N₂ + 3H₂ ⇌ 2NH₃"""

@pytest.fixture
def sample_physics_text():
    return """Einstein's famous equation E = mc² and Newton's law F = ma.
    The gravitational force F = G(m1m2)/r²."""

@pytest.fixture
def formula_image():
    # Create a synthetic image with a formula
    img = np.ones((100, 300), dtype=np.uint8) * 255
    cv2.putText(
        img, "E = mc^2", (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2
    )
    return img

class TestFormulaProcessor:
    def test_initialization(self, formula_processor):
        """Test proper initialization of FormulaProcessor"""
        assert isinstance(formula_processor, FormulaProcessor)
        assert hasattr(formula_processor, 'latex_ocr')
        assert all(key in formula_processor.patterns for key in [
            'inline_latex', 'display_latex', 'chemistry', 'physics'
        ])

    def test_math_formula_detection(self, formula_processor, sample_math_text):
        """Test detection of mathematical formulas"""
        formulas = formula_processor.detect_formulas(sample_math_text)
        
        assert len(formulas) >= 2
        assert any(f.formula_type == 'math' for f in formulas)
        
        # Check inline formula
        inline_formulas = [
            f for f in formulas
            if f.metadata.get('style') == 'inline'
        ]
        assert len(inline_formulas) >= 1
        assert 'ax^2' in inline_formulas[0].latex_repr
        
        # Check display formula
        display_formulas = [
            f for f in formulas
            if f.metadata.get('style') == 'display'
        ]
        assert len(display_formulas) >= 1
        assert '\\sqrt' in display_formulas[0].latex_repr
        assert 'mathml' in display_formulas[0].mathml_repr.lower()

    def test_chemistry_formula_detection(
        self,
        formula_processor,
        sample_chemistry_text
    ):
        """Test detection of chemical formulas"""
        formulas = formula_processor.detect_formulas(sample_chemistry_text)
        
        assert len(formulas) >= 4  # H₂, O₂, H₂O, NH₃
        chemistry_formulas = [
            f for f in formulas
            if f.formula_type == 'chemistry'
        ]
        
        assert len(chemistry_formulas) >= 4
        
        # Verify chemical formula parsing
        for formula in chemistry_formulas:
            assert formula.metadata.get('elements')
            assert all(
                'element' in elem and 'quantity' in elem
                for elem in formula.metadata['elements']
            )

    def test_physics_formula_detection(
        self,
        formula_processor,
        sample_physics_text
    ):
        """Test detection of physics formulas"""
        formulas = formula_processor.detect_formulas(sample_physics_text)
        
        assert len(formulas) >= 3  # E=mc², F=ma, F=G(m1m2)/r²
        physics_formulas = [
            f for f in formulas
            if f.formula_type == 'physics'
        ]
        
        assert len(physics_formulas) >= 3
        
        # Check specific formulas
        assert any('E = mc' in f.original_text for f in physics_formulas)
        assert any('F = ma' in f.original_text for f in physics_formulas)

    def test_formula_image_extraction(self, formula_processor, formula_image):
        """Test extraction of formulas from images"""
        formulas = formula_processor.extract_formulas_from_image(formula_image)
        
        assert len(formulas) > 0
        assert all(isinstance(f, Formula) for f in formulas)
        
        first_formula = formulas[0]
        assert first_formula.latex_repr
        assert 0 <= first_formula.confidence <= 1
        assert first_formula.metadata.get('source') == 'image_ocr'

    def test_placeholder_replacement(
        self,
        formula_processor,
        sample_math_text
    ):
        """Test formula placeholder replacement and restoration"""
        # Detect formulas
        formulas = formula_processor.detect_formulas(sample_math_text)
        
        # Replace with placeholders
        modified_text, placeholders = (
            formula_processor.replace_formulas_with_placeholders(
                sample_math_text, formulas
            )
        )
        
        # Verify placeholders
        assert all(f"[FORMULA_{i}]" in modified_text for i in range(len(formulas)))
        assert len(placeholders) == len(formulas)
        
        # Restore formulas
        restored_text = formula_processor.restore_formulas(
            modified_text, placeholders
        )
        assert restored_text == sample_math_text
        
        # Test different output formats
        latex_text = formula_processor.restore_formulas(
            modified_text, placeholders, output_format='latex'
        )
        assert '\\frac' in latex_text
        
        mathml_text = formula_processor.restore_formulas(
            modified_text, placeholders, output_format='mathml'
        )
        assert '<math' in mathml_text

    def test_chemical_formula_validation(self, formula_processor):
        """Test chemical formula validation"""
        valid_formulas = ['H2O', 'NaCl', 'C6H12O6']
        invalid_formulas = ['H2O2x', 'abc', '123']
        
        for formula in valid_formulas:
            assert formula_processor._validate_chemical_formula(formula)
        
        for formula in invalid_formulas:
            assert not formula_processor._validate_chemical_formula(formula)

    def test_formula_conversion(self, formula_processor):
        """Test formula conversion between formats"""
        # Test chemical formula to LaTeX
        chemical = '2H2O'
        latex = formula_processor._chemical_to_latex(chemical)
        assert '_' in latex  # Should have subscripts
        
        # Test physics formula to LaTeX
        physics = '3.6e-4 m/s'
        latex = formula_processor._physics_to_latex(physics)
        assert '\\times 10' in latex  # Should use scientific notation

    def test_error_handling(self, formula_processor):
        """Test error handling for invalid inputs"""
        # Test with invalid LaTeX
        invalid_latex = '$\\invalid{formula}$'
        formulas = formula_processor.detect_formulas(invalid_latex)
        assert len(formulas) == 0
        
        # Test with invalid image
        invalid_image = np.zeros((10, 10), dtype=np.uint8)
        formulas = formula_processor.extract_formulas_from_image(invalid_image)
        assert len(formulas) == 0

    def test_formula_validation(self, formula_processor):
        """Test formula structure validation"""
        # Create test formulas
        valid_math = Formula(
            original_text='x^2 + 2x + 1',
            latex_repr='x^2 + 2x + 1',
            mathml_repr='<math>...</math>',
            formula_type='math',
            position=(0, 11),
            confidence=0.9,
            metadata={}
        )
        
        valid_chemistry = Formula(
            original_text='H2O',
            latex_repr='H_2O',
            mathml_repr='',
            formula_type='chemistry',
            position=(0, 3),
            confidence=0.9,
            metadata={'elements': [
                {'element': 'H', 'quantity': 2},
                {'element': 'O', 'quantity': 1}
            ]}
        )
        
        # Test validation
        assert formula_processor.validate_formula(valid_math)
        assert formula_processor.validate_formula(valid_chemistry)

    def test_performance(self, formula_processor, sample_math_text):
        """Test performance with large texts"""
        import time
        
        # Create a large text with many formulas
        large_text = sample_math_text * 100
        
        start_time = time.time()
        formulas = formula_processor.detect_formulas(large_text)
        processing_time = time.time() - start_time
        
        assert processing_time < 30  # seconds
        assert len(formulas) > 0
