"""
Test cases for the Book class and its mixins.
"""

import json
import os
import tempfile
import unittest

from md_to_latex.core.Book import Book


class TestBookInit(unittest.TestCase):
    """Test Book initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up all files and directories
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_book_creation_with_metadata(self):
        """Test book creation with metadata.json."""
        # Create metadata
        metadata = {
            "title": "Test Book",
            "subtitle": "A Test",
            "author": "Test Author",
            "year": "2026",
            "edition": "First",
            "publisher": "Test Press",
        }
        metadata_file = os.path.join(self.temp_dir, "metadata.json")
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f)

        book = Book(self.temp_dir)
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.subtitle, "A Test")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.year, "2026")
        self.assertEqual(book.edition, "First")
        self.assertEqual(book.publisher, "Test Press")

    def test_book_creation_without_metadata(self):
        """Test book creation without metadata.json."""
        book = Book(self.temp_dir)
        # Should use directory name as title
        self.assertEqual(book.title, os.path.basename(self.temp_dir))
        self.assertIsNone(book.subtitle)
        self.assertIsNone(book.author)

    def test_parts_loading(self):
        """Test loading parts from parts directory."""
        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        # Create two parts
        for i in range(1, 3):
            part_dir = os.path.join(parts_dir, f"part-{i}-test")
            os.makedirs(part_dir)
            chapter_file = os.path.join(part_dir, "chapter-1.md")
            with open(chapter_file, "w", encoding="utf-8") as f:
                f.write(f"# Chapter {i}\n\nContent.")

        book = Book(self.temp_dir)
        self.assertEqual(len(book.parts), 2)

    def test_about_files_loading(self):
        """Test loading about files."""
        # Create about-the-book.md
        with open(
            os.path.join(self.temp_dir, "about-the-book.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("# About the Book\n\nThis is about the book.")

        # Create about-the-author.md
        with open(
            os.path.join(self.temp_dir, "about-the-author.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write("# About the Author\n\nThis is about the author.")

        book = Book(self.temp_dir)
        self.assertEqual(book.about_book_title, "About the Book")
        self.assertIn("This is about the book.", book.about_book)
        self.assertEqual(book.about_author_title, "About the Author")
        self.assertIn("This is about the author.", book.about_author)


class TestBookLoaderMixin(unittest.TestCase):
    """Test BookLoaderMixin methods."""

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

    def test_count_words(self):
        """Test word counting."""
        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        part_dir = os.path.join(parts_dir, "part-1-test")
        os.makedirs(part_dir)

        # Create chapter with known word count
        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Chapter\n\nOne two three four five.")

        book = Book(self.temp_dir)
        word_count = book._count_words()
        self.assertEqual(word_count, 5)

    def test_has_section_breaks_true(self):
        """Test section break detection when present."""
        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        part_dir = os.path.join(parts_dir, "part-1-test")
        os.makedirs(part_dir)

        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Chapter\n\nBefore\n\n---\n\nAfter")

        book = Book(self.temp_dir)
        self.assertTrue(book._has_section_breaks())

    def test_has_section_breaks_false(self):
        """Test section break detection when absent."""
        parts_dir = os.path.join(self.temp_dir, "parts")
        os.makedirs(parts_dir)

        part_dir = os.path.join(parts_dir, "part-1-test")
        os.makedirs(part_dir)

        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Chapter\n\nNo section breaks here.")

        book = Book(self.temp_dir)
        self.assertFalse(book._has_section_breaks())


class TestBookMarkdownMixin(unittest.TestCase):
    """Test BookMarkdownMixin methods."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.book = Book(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_process_markdown_bold(self):
        """Test bold processing."""
        text = "This is **bold** text."
        result = self.book._process_markdown(text)
        self.assertIn(r"\textbf{bold}", result)

    def test_process_markdown_italic(self):
        """Test italic processing."""
        text = "This is *italic* text."
        result = self.book._process_markdown(text)
        self.assertIn(r"\textit{italic}", result)

    def test_process_markdown_quotes(self):
        """Test quote processing."""
        text = 'He said "Hello".'
        result = self.book._process_markdown(text)
        self.assertIn(r"\say{Hello}", result)


class TestBookKebabCase(unittest.TestCase):
    """Test kebab-case conversion."""

    def test_kebab_case_spaces(self):
        """Test converting spaces to hyphens."""
        self.assertEqual(
            Book._to_kebab_case("My Book Title"), "my-book-title"
        )

    def test_kebab_case_special_chars(self):
        """Test removing special characters."""
        self.assertEqual(
            Book._to_kebab_case("Book: The Story!"), "book-the-story"
        )

    def test_kebab_case_underscores(self):
        """Test converting underscores to hyphens."""
        self.assertEqual(
            Book._to_kebab_case("My_Book_Title"), "my-book-title"
        )

    def test_kebab_case_mixed(self):
        """Test mixed case conversion."""
        self.assertEqual(Book._to_kebab_case("MixedCase"), "mixedcase")

    def test_kebab_case_multiple_spaces(self):
        """Test multiple consecutive spaces."""
        self.assertEqual(
            Book._to_kebab_case("Multiple   Spaces"), "multiple-spaces"
        )


if __name__ == "__main__":
    unittest.main()
