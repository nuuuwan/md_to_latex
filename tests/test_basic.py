"""
Integration tests using the example book.
"""

import os
import unittest

from md_to_latex.core import Book


class TestExampleBook(unittest.TestCase):
    """Test with the example book in tests/input/example-book."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.example_dir = os.path.join(
            os.path.dirname(__file__), "input", "example-book"
        )
        if os.path.isdir(cls.example_dir):
            cls.book = Book(cls.example_dir)
            cls.has_example = True
        else:
            cls.has_example = False

    def test_example_book_exists(self):
        """Test that example book directory exists."""
        self.assertTrue(
            self.has_example,
            "Example book not found at tests/input/example-book",
        )

    def test_book_metadata(self):
        """Test that example book metadata is loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertEqual(self.book.title, "The Example Novel")
        self.assertEqual(
            self.book.subtitle, "A Journey Through Markdown and LaTeX"
        )
        self.assertEqual(self.book.author, "Jane Doe")
        self.assertEqual(self.book.year, "2026-02-17")
        self.assertEqual(self.book.edition, "First Edition")
        self.assertEqual(self.book.publisher, "Independent Press")

    def test_book_parts(self):
        """Test that example book parts are loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertEqual(len(self.book.parts), 2)

    def test_book_chapters(self):
        """Test that example book chapters are loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        # Part 1 should have 2 chapters
        self.assertEqual(len(self.book.parts[0].chapters), 2)
        # Part 2 should have 1 chapter
        self.assertEqual(len(self.book.parts[1].chapters), 1)

    def test_book_about_files(self):
        """Test that about files are loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertIsNotNone(self.book.about_book)
        self.assertIsNotNone(self.book.about_author)

    def test_book_word_count(self):
        """Test word counting."""
        if not self.has_example:
            self.skipTest("Example book not found")

        word_count = self.book._count_words()
        self.assertGreater(word_count, 0)


if __name__ == "__main__":
    unittest.main()
