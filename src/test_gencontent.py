import unittest
from gencontent import extract_title

class TestGenerateContent(unittest.TestCase):
    def test_simple_markdown_string(self):
        markdown1 = "# Hello"
        self.assertEqual(extract_title(markdown1), "Hello")

    def test_whitespace(self):
        markdown1 = "#   Hello "
        self.assertEqual(extract_title(markdown1), "Hello")

    def test_multiple_headers(self):
        markdown1 = " Hello\n## World\n### Goodbye"
        self.assertEqual(extract_title(markdown1), "Hello")

    def test_h1_not_on_first_line(self):
        markdown1 = "paragraph\n# Hello"
        self.assertEqual(extract_title(markdown1), "Hello")

    def test_heading_missing(self):
        markdown1 = "paragraph"
        with self.assertRaises(Exception):
            extract_title(markdown1)

