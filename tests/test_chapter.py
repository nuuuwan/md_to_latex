"""
Test cases for the Chapter class.
"""

import os
import tempfile
import unittest

from md_to_latex.core.Chapter import Chapter


class TestChapterInit(unittest.TestCase):
    """Test Chapter initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_chapter.md")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_chapter_creation(self):
        """Test basic chapter creation."""
        content = "# Test Chapter\n\nThis is test content."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        self.assertEqual(chapter.title, "Test Chapter")
        self.assertIn("This is test content.", chapter.content)

    def test_title_extraction(self):
        """Test title extraction from different heading formats."""
        test_cases = [
            ("# Single Hash", "Single Hash"),
            ("## Double Hash", "Double Hash"),
            ("### Triple Hash", "Triple Hash"),
            ("#### Quad Hash", "Quad Hash"),
        ]

        for content, expected_title in test_cases:
            with open(self.test_file, "w", encoding="utf-8") as f:
                f.write(f"{content}\n\nContent here.")

            chapter = Chapter(self.test_file)
            self.assertEqual(chapter.title, expected_title)


class TestMarkdownParsing(unittest.TestCase):
    """Test markdown to LaTeX conversion."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_chapter.md")

    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        os.rmdir(self.temp_dir)

    def test_bold_conversion(self):
        """Test bold markdown conversion."""
        content = "# Title\n\nThis is **bold** text."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textbf{bold}", latex)

    def test_italic_conversion(self):
        """Test italic markdown conversion."""
        content = "# Title\n\nThis is *italic* text."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textit{italic}", latex)

    def test_bold_italic_conversion(self):
        """Test bold+italic markdown conversion."""
        content = "# Title\n\nThis is ***bold italic*** text."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textbf{\textit{bold italic}}", latex)

    def test_quote_conversion(self):
        """Test quote markdown conversion."""
        content = '# Title\n\nHe said "Hello World".'
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\say{Hello World}", latex)

    def test_heading_conversion(self):
        """Test heading conversion."""
        content = "# Title\n\n## Subsection\n\nContent here."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\subsection{Subsection}", latex)

    def test_section_break_conversion(self):
        """Test section break conversion."""
        test_cases = ["---", "..."]

        for break_marker in test_cases:
            content = (
                f"# Title\n\nBefore break.\n\n{break_marker}\n\nAfter break."
            )
            with open(self.test_file, "w", encoding="utf-8") as f:
                f.write(content)

            chapter = Chapter(self.test_file)
            latex = chapter._parse_markdown_to_latex(chapter.content)
            self.assertIn(r"\scenebreak", latex)

    def test_underscore_escape(self):
        """Test underscore escaping."""
        content = "# Title\n\nWith_underscore text."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"With\_underscore", latex)

    def test_unicode_cleanup(self):
        """Test problematic Unicode character cleanup."""
        content = "# Title\n\nText with\u2028line separator."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertNotIn("\u2028", latex)


if __name__ == "__main__":
    unittest.main()
