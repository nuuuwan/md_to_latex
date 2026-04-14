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
        self.chapter_dir = os.path.join(
            self.temp_dir, "chapter-01-getting-started"
        )
        os.makedirs(self.chapter_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def _write(self, filename, content):
        path = os.path.join(self.chapter_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def test_chapter_creation(self):
        """Test basic chapter creation."""
        self._write("001.md", "# Test Chapter\n\nThis is test content.")

        chapter = Chapter(self.chapter_dir)
        # Title is derived from directory name, not the # heading in the file
        self.assertEqual(chapter.title, "Getting Started")
        self.assertIn("This is test content.", chapter.content)

    def test_title_extraction(self):
        """Test title extraction from directory name."""
        test_cases = [
            ("chapter-01-getting-started", "Getting Started"),
            ("chapter-02-the-writing-process", "The Writing Process"),
            ("chapter-10-final-thoughts", "Final Thoughts"),
        ]
        for dirname, expected_title in test_cases:
            chapter_dir = os.path.join(self.temp_dir, dirname)
            os.makedirs(chapter_dir, exist_ok=True)
            with open(os.path.join(chapter_dir, "001.md"), "w") as f:
                f.write("# Some Heading\n\nContent here.")

            chapter = Chapter(chapter_dir)
            self.assertEqual(chapter.title, expected_title)

    def test_multiple_files_concatenated(self):
        """Test that content from multiple NNN.md files is concatenated."""
        self._write("001.md", "# Section One\n\nFile one content.")
        self._write("002.md", "File two content.")

        chapter = Chapter(self.chapter_dir)
        self.assertIn("File one content.", chapter.content)
        self.assertIn("File two content.", chapter.content)

    def test_files_sorted_numerically(self):
        """Test that NNN.md files are read in numeric order."""
        self._write("003.md", "Third.")
        self._write("001.md", "# Title\n\nFirst.")
        self._write("002.md", "Second.")

        chapter = Chapter(self.chapter_dir)
        idx_first = chapter.content.index("First.")
        idx_second = chapter.content.index("Second.")
        idx_third = chapter.content.index("Third.")
        self.assertLess(idx_first, idx_second)
        self.assertLess(idx_second, idx_third)

    def test_empty_chapter_dir(self):
        """Test chapter with no markdown files."""
        chapter = Chapter(self.chapter_dir)
        self.assertEqual(chapter.content, "")


class TestMarkdownParsing(unittest.TestCase):
    """Test markdown to LaTeX conversion."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.chapter_dir = os.path.join(self.temp_dir, "chapter-01")
        os.makedirs(self.chapter_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def _make_chapter(self, content):
        path = os.path.join(self.chapter_dir, "001.md")
        # Remove any existing files
        for f in os.listdir(self.chapter_dir):
            os.remove(os.path.join(self.chapter_dir, f))
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return Chapter(self.chapter_dir)

    def test_bold_conversion(self):
        """Test bold markdown conversion."""
        chapter = self._make_chapter("# Title\n\nThis is **bold** text.")
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textbf{bold}", latex)

    def test_italic_conversion(self):
        """Test italic markdown conversion."""
        chapter = self._make_chapter("# Title\n\nThis is *italic* text.")
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textit{italic}", latex)

    def test_bold_italic_conversion(self):
        """Test bold+italic markdown conversion."""
        chapter = self._make_chapter(
            "# Title\n\nThis is ***bold italic*** text."
        )
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\textbf{\textit{bold italic}}", latex)

    def test_quote_conversion(self):
        """Test quote markdown conversion."""
        chapter = self._make_chapter('# Title\n\nHe said "Hello World".')
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\say{Hello World}", latex)

    def test_heading_conversion(self):
        """Test heading conversion."""
        chapter = self._make_chapter(
            "# Title\n\n## Subsection\n\nContent here."
        )
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\subsection*{Subsection}", latex)

    def test_section_break_conversion(self):
        """Test section break conversion."""
        for break_marker in ["---", "..."]:
            chapter = self._make_chapter(
                f"# Title\n\nBefore break.\n\n{break_marker}\n\nAfter break."
            )
            latex = chapter._parse_markdown_to_latex(chapter.content)
            self.assertIn(r"\scenebreak", latex)

    def test_underscore_escape(self):
        """Test underscore escaping."""
        chapter = self._make_chapter("# Title\n\nWith_underscore text.")
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"With\_underscore", latex)

    def test_hashtag_escape(self):
        """Test that inline hashtags are escaped for LaTeX."""
        chapter = self._make_chapter("# Title\n\nText #ThisIsAHashtag here.")
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\#ThisIsAHashtag", latex)

    def test_unicode_cleanup(self):
        """Test problematic Unicode character cleanup."""
        chapter = self._make_chapter(
            "# Title\n\nText with\u2028line separator."
        )
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertNotIn("\u2028", latex)


if __name__ == "__main__":
    unittest.main()
