import unittest
import re
from src.documentation.doc_extractor import DocExtractor

class TestDocExtractor(unittest.TestCase):
    def setUp(self):
        self.doc_extractor = DocExtractor()

    def test_extract_contributing_with_valid_content(self):
        content = "# Title\n\n## Contributing\nThis is the contributing section.\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertEqual(result, "This is the contributing section.")

    def test_extract_contributing_with_no_contributing_section(self):
        content = "# Title\n\n## Installation\nThis is the installation section.\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertIsNone(result)

    def test_extract_contributing_with_empty_contributing_section(self):
        content = "# Title\n\n## Contributing\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertIsNone(result)

    def test_extract_contributing_case_insensitive(self):
        content = "# Title\n\n## CONTRIBUTING\nThis is the contributing section.\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertEqual(result, "This is the contributing section.")

    def test_extract_contributing_with_single_hash(self):
        content = "# Title\n\n# Contributing\nThis is the contributing section.\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertEqual(result, "This is the contributing section.")

    def test_extract_contributing_with_multiple_paragraphs(self):
        content = "# Title\n\n## Contributing\nParagraph 1.\n\nParagraph 2.\n\n# Another Section"
        result = self.doc_extractor.extract_contributing(content)
        self.assertEqual(result, "Paragraph 1.\n\nParagraph 2.")

    def test_extract_contributing_at_end_of_file(self):
        content = "# Title\n\n## Contributing\nThis is the contributing section."
        result = self.doc_extractor.extract_contributing(content)
        self.assertEqual(result, "This is the contributing section.")

if __name__ == '__main__':
    unittest.main()
