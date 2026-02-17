"""
Test cases for LaTeX generation.
"""

import json
import os
import tempfile
import unittest

from pylatex import Document

from md_to_latex.core.Book import Book
from md_to_latex.core.Chapter import Chapter
from md_to_latex.core.Part import Part


class TestChapterLatexGeneration(unittest.TestCase):
    """Test Chapter LaTeX generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_chapter.md")

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_chapter_to_latex(self):
        """Test chapter LaTeX generation."""
        content = "# Test Chapter\n\nThis is **bold** text."
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(content)

        chapter = Chapter(self.test_file)
        doc = Document()
        chapter.to_latex(doc)

        # Generate LaTeX string
        latex_str = doc.dumps()
        self.assertIn("Test Chapter", latex_str)
        self.assertIn(r"\textbf{bold}", latex_str)


class TestPartLatexGeneration(unittest.TestCase):
    """Test Part LaTeX generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.part_dir = os.path.join(self.temp_dir, "part-1-introduction")
        os.makedirs(self.part_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_part_to_latex(self):
        """Test part LaTeX generation."""
        # Create a chapter
        chapter_file = os.path.join(self.part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# First Chapter\n\nContent here.")

        part = Part(self.part_dir)
        doc = Document()
        part.to_latex(doc)

        # Generate LaTeX string
        latex_str = doc.dumps()
        self.assertIn(r"\part{Introduction}", latex_str)
        self.assertIn("First Chapter", latex_str)


class TestBookLatexGeneration(unittest.TestCase):
    """Test Book LaTeX generation."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_book_latex_document_creation(self):
        """Test that book creates a valid LaTeX document."""
        # Create minimal book structure
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "year": "2026",
        }
        with open(
            os.path.join(self.temp_dir, "metadata.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(metadata, f)

        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        part_dir = os.path.join(parts_dir, "part-1-test")
        os.makedirs(part_dir)

        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Test Chapter\n\nTest content.")

        book = Book(self.temp_dir)

        # Create document
        doc = Document(
            documentclass="book",
            document_options=["a4paper", "twoside", "12pt"],
        )

        book._configure_document(doc)
        book.word_count = book._count_words()
        book._setup_document_metadata(doc)

        # Generate LaTeX string
        latex_str = doc.dumps()

        # Verify essential LaTeX elements
        self.assertIn(r"\documentclass", latex_str)
        self.assertIn(r"\begin{document}", latex_str)
        self.assertIn(r"\end{document}", latex_str)
        self.assertIn("Test Book", latex_str)
        self.assertIn("Test Author", latex_str)

    def test_book_latex_has_packages(self):
        """Test that book includes required packages."""
        book = Book(self.temp_dir)
        doc = Document()
        book._configure_document(doc)

        latex_str = doc.dumps()

        # Check for essential packages
        packages = [
            "geometry",
            "setspace",
            "microtype",
            "ebgaramond",
            "inputenc",
            "fontenc",
            "dirtytalk",
            "xcolor",
            "fancyhdr",
            "titlesec",
        ]

        for package in packages:
            self.assertIn(package, latex_str)

    def test_book_latex_has_custom_commands(self):
        """Test that book includes custom LaTeX commands."""
        book = Book(self.temp_dir)
        doc = Document()
        book._configure_document(doc)

        latex_str = doc.dumps()

        # Check for custom commands
        self.assertIn(r"\definecolor{maroon}", latex_str)
        self.assertIn(r"\doublespacing", latex_str)

    def test_book_tex_file_generation(self):
        """Test that book generates .tex file."""
        # Create minimal book structure
        metadata = {"title": "Test Book"}
        with open(
            os.path.join(self.temp_dir, "metadata.json"),
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(metadata, f)

        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        part_dir = os.path.join(parts_dir, "part-1-test")
        os.makedirs(part_dir)

        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Test Chapter\n\nTest content.")

        book = Book(self.temp_dir)
        os.makedirs(book.output_dir, exist_ok=True)

        doc = Document(
            documentclass="book",
            document_options=["a4paper", "twoside", "12pt"],
        )
        book._configure_document(doc)
        book.word_count = book._count_words()
        book._setup_document_metadata(doc)
        book._add_front_matter(doc)

        # Generate .tex file
        file_name = book._to_kebab_case(book.title)
        output_path = os.path.join(book.output_dir, file_name)
        doc.generate_tex(output_path)

        # Verify .tex file was created
        tex_file = f"{output_path}.tex"
        self.assertTrue(os.path.exists(tex_file))

        # Verify .tex file has content
        with open(tex_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Test Book", content)
            self.assertIn(r"\maketitle", content)


class TestExampleBookLatexGeneration(unittest.TestCase):
    """Test full LaTeX generation with the example book."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.example_dir = os.path.join(
            os.path.dirname(__file__), "input", "example-book"
        )
        cls.has_example = os.path.isdir(cls.example_dir)

    def test_generate_example_book_latex(self):
        """Test generating LaTeX and PDF from the example book."""
        if not self.has_example:
            self.skipTest("Example book not found")

        book = Book(self.example_dir)

        # Generate LaTeX and PDF using the full pipeline
        output_file = book.toLatex()

        # Verify output directory exists
        self.assertTrue(
            os.path.exists(book.output_dir),
            f"Output directory not found: {book.output_dir}",
        )

        # Verify output file was created
        self.assertTrue(
            os.path.exists(output_file),
            f"Output file not found: {output_file}",
        )

        # Get the base name for the files
        file_name = book._to_kebab_case(book.title)
        tex_file = os.path.join(book.output_dir, f"{file_name}.tex")
        pdf_file = os.path.join(book.output_dir, f"{file_name}.pdf")

        # Verify .tex file was created
        self.assertTrue(
            os.path.exists(tex_file), f"LaTeX file not found at {tex_file}"
        )

        # Verify .tex file has expected content
        with open(tex_file, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("The Example Novel", content)
            self.assertIn("Jane Doe", content)
            self.assertIn(r"\maketitle", content)
            self.assertIn(r"\tableofcontents", content)
            self.assertIn(r"\part{Foundations}", content)
            self.assertIn(r"\part{Advanced}", content)

        # Verify .tex file size is reasonable (not empty)
        file_size = os.path.getsize(tex_file)
        self.assertGreater(
            file_size, 1000, f"LaTeX file too small: {file_size} bytes"
        )

        # If PDF generation succeeded, verify PDF exists and has content
        if output_file.endswith(".pdf"):
            self.assertTrue(
                os.path.exists(pdf_file), f"PDF file not found at {pdf_file}"
            )
            # Verify PDF file size is reasonable (not empty)
            pdf_size = os.path.getsize(pdf_file)
            self.assertGreater(
                pdf_size, 5000, f"PDF file too small: {pdf_size} bytes"
            )


if __name__ == "__main__":
    unittest.main()
