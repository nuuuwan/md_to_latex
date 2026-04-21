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


class TestChapterFromFile(unittest.TestCase):
    """Test Chapter.from_file() (flat format)."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def _write(self, filename, content):
        path = os.path.join(self.temp_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def test_title_from_heading(self):
        """Title is taken from the first # heading in the file."""
        path = self._write(
            "chapter-01-ignored-name.md",
            "# My Real Title\n\nSome content here.",
        )
        chapter = Chapter.from_file(path)
        self.assertEqual(chapter.title, "My Real Title")

    def test_title_fallback_to_filename(self):
        """Falls back to filename-derived title when no heading present."""
        path = self._write(
            "chapter-02-fallback-title.md",
            "No heading here, just content.",
        )
        chapter = Chapter.from_file(path)
        self.assertEqual(chapter.title, "Fallback Title")

    def test_content_loaded(self):
        """Content of the file is loaded in full."""
        path = self._write(
            "chapter-03-content.md",
            "# Chapter Three\n\nParagraph one.\n\nParagraph two.",
        )
        chapter = Chapter.from_file(path)
        self.assertIn("Paragraph one.", chapter.content)
        self.assertIn("Paragraph two.", chapter.content)

    def test_heading_stripped_in_to_latex(self):
        """The first # heading is stripped from content when rendering to LaTeX."""
        path = self._write(
            "chapter-04-heading.md",
            "# Keep This\n\nBody text.",
        )
        chapter = Chapter.from_file(path)
        # Heading is still in raw content
        self.assertIn("# Keep This", chapter.content)
        # But stripped heading is not re-emitted as \section* in to_latex output
        doc_content = chapter._strip_first_heading(chapter.content)
        self.assertNotIn("# Keep This", doc_content)
        self.assertIn("Body text.", doc_content)

    def test_title_leading_number_stripped(self):
        """Leading numbers are stripped from the heading-derived title."""
        for raw, expected in [
            ("# 1. My Chapter", "My Chapter"),
            ("# 2 The Next One", "The Next One"),
            ("# 10. Advanced", "Advanced"),
        ]:
            path = self._write(
                "chapter-06-numbered.md",
                f"{raw}\n\nContent.",
            )
            chapter = Chapter.from_file(path)
            self.assertEqual(chapter.title, expected)

    def test_title_uses_first_heading_only(self):
        """Only the first # heading is used as the title."""
        path = self._write(
            "chapter-05-multi-heading.md",
            "# First Heading\n\n## Second Heading\n\nContent.",
        )
        chapter = Chapter.from_file(path)
        self.assertEqual(chapter.title, "First Heading")


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

    def test_footnote_conversion(self):
        """Test footnote conversion."""
        chapter = self._make_chapter(
            "# Title\n\nSome text^[This is the footnote content] continues here."
        )
        latex = chapter._parse_markdown_to_latex(chapter.content)
        self.assertIn(r"\footnote{This is the footnote content}", latex)
        self.assertIn("Some text", latex)
        self.assertIn("continues here.", latex)

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
