"""Tests for the chunk combiner module."""

import unittest
from chunking.chunk_combiner import combine_chunks_safely, clean_combined_text

class TestChunkCombiner(unittest.TestCase):
    """Test cases for chunk combination functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None  # Show full diffs in test output
    
    def test_empty_chunks(self):
        """Test handling of empty chunk list."""
        result = combine_chunks_safely([], 0)
        self.assertEqual(result, "[ERROR: No chunks to combine]")
    
    def test_single_chunk(self):
        """Test combining a single chunk."""
        chunks = [{
            'chunk_id': 0,
            'translated': 'Hello world',
            'original_content': 'Hello world'
        }]
        result = combine_chunks_safely(chunks, 1)
        self.assertEqual(result, 'Hello world')
    
    def test_multiple_chunks(self):
        """Test combining multiple chunks."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': 'First chunk',
                'original_content': 'First chunk'
            },
            {
                'chunk_id': 1,
                'translated': 'Second chunk',
                'original_content': 'Second chunk'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertEqual(result, 'First chunk\n\nSecond chunk')
    
    def test_error_chunk(self):
        """Test handling of error chunks."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': '[TRANSLATION ERROR] Failed',
                'original_content': 'Original text'
            }
        ]
        result = combine_chunks_safely(chunks, 1)
        self.assertTrue('Original text' in result)
        self.assertTrue('Translation Error' in result)
    
    def test_overlap_removal(self):
        """Test removal of overlapping content."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': 'This is a test sentence.',
                'original_content': 'This is a test sentence.'
            },
            {
                'chunk_id': 1,
                'translated': 'test sentence. This is another test.',
                'original_content': 'test sentence. This is another test.'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertEqual(result, 'This is a test sentence. This is another test.')
    
    def test_clean_combined_text(self):
        """Test text cleaning functionality."""
        text = "Multiple    spaces\n\n\n\nToo many newlines\t\tTabs"
        cleaned = clean_combined_text(text)
        self.assertFalse('    ' in cleaned)  # No quadruple spaces
        self.assertFalse('\n\n\n\n' in cleaned)  # No quadruple newlines
        self.assertFalse('\t' in cleaned)  # No tabs
    
    def test_out_of_order_chunks(self):
        """Test combining chunks that are out of order."""
        chunks = [
            {
                'chunk_id': 1,
                'translated': 'Second chunk',
                'original_content': 'Second chunk'
            },
            {
                'chunk_id': 0,
                'translated': 'First chunk',
                'original_content': 'First chunk'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertEqual(result, 'First chunk\n\nSecond chunk')
    
    def test_missing_chunks(self):
        """Test handling when expected chunks are missing."""
        chunks = [{
            'chunk_id': 0,
            'translated': 'Only chunk',
            'original_content': 'Only chunk'
        }]
        result = combine_chunks_safely(chunks, 2)  # Expect 2 but only got 1
        self.assertTrue('Only chunk' in result)

    def test_multiple_error_chunks(self):
        """Test handling multiple error chunks in sequence."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': '[TRANSLATION ERROR] Failed 1',
                'original_content': 'Original text 1'
            },
            {
                'chunk_id': 1,
                'translated': '[TRANSLATION ERROR] Failed 2',
                'original_content': 'Original text 2'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertTrue('Original text 1' in result)
        self.assertTrue('Original text 2' in result)
        self.assertTrue('Translation Error' in result)

    def test_mixed_error_and_success_chunks(self):
        """Test handling a mix of error and successful chunks."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': 'Successful translation',
                'original_content': 'Original text 1'
            },
            {
                'chunk_id': 1,
                'translated': '[TRANSLATION ERROR] Failed',
                'original_content': 'Original text 2'
            },
            {
                'chunk_id': 2,
                'translated': 'Another success',
                'original_content': 'Original text 3'
            }
        ]
        result = combine_chunks_safely(chunks, 3)
        self.assertTrue('Successful translation' in result)
        self.assertTrue('Original text 2' in result)
        self.assertTrue('Another success' in result)

    def test_empty_chunk_content(self):
        """Test handling chunks with empty content."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': '',
                'original_content': 'Original text 1'
            },
            {
                'chunk_id': 1,
                'translated': 'Valid content',
                'original_content': 'Original text 2'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertTrue('Valid content' in result)
        self.assertFalse('Original text 1' in result)

    def test_special_characters(self):
        """Test handling text with special characters and formatting."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': 'Text with *bold* and _italic_',
                'original_content': 'Original formatting'
            },
            {
                'chunk_id': 1,
                'translated': '# Heading\n- List item',
                'original_content': 'Original structure'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertTrue('*bold*' in result)
        self.assertTrue('# Heading' in result)
        self.assertTrue('- List item' in result)

    def test_unicode_characters(self):
        """Test handling text with Unicode characters."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': '你好，世界！',
                'original_content': 'Hello world!'
            },
            {
                'chunk_id': 1,
                'translated': 'Café über straße',
                'original_content': 'Original text'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertTrue('你好，世界！' in result)
        self.assertTrue('Café über straße' in result)

    def test_large_overlap_removal(self):
        """Test removal of large overlapping content."""
        chunks = [
            {
                'chunk_id': 0,
                'translated': 'This is a very long sentence that contains important information and context.',
                'original_content': 'Original long sentence'
            },
            {
                'chunk_id': 1,
                'translated': 'contains important information and context. Here is additional text.',
                'original_content': 'Original continuation'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertEqual(
            result,
            'This is a very long sentence that contains important information and context. Here is additional text.'
        )

    def test_invalid_chunk_data(self):
        """Test handling of chunks with missing or invalid data."""
        chunks = [
            {
                'chunk_id': 0,
                # Missing 'translated' field
                'original_content': 'Original text'
            },
            {
                'chunk_id': 1,
                'translated': None,  # Invalid translated field
                'original_content': 'Original text 2'
            }
        ]
        result = combine_chunks_safely(chunks, 2)
        self.assertTrue('Original text' in result or 'Error' in result)

if __name__ == '__main__':
    unittest.main()
