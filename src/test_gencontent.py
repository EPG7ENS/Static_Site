import unittest
from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Tolkein Fan Club\nMore Text..."
        result = extract_title(markdown)
        self.assertEqual(result,"Tolkein Fan Club")
        
    def test_extract_title_no_h1_raises(self):
            markdown = "## Not an h1\nJust text"
            with self.assertRaises(Exception):
                extract_title(markdown)   