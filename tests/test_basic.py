"""
Integration tests using the example books.
"""

import os
import unittest

from md_to_latex.core import Book


class TestExampleBook1(unittest.TestCase):
    """Test with the format-1 example book in tests/input/example-book-1."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.example_dir = os.path.join(
            os.path.dirname(__file__), "input", "example-book-1"
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
            "Example book not found at tests/input/example-book-1",
        )

    def test_book_format(self):
        """Test that format-1 book is detected as format 1."""
        if not self.has_example:
            self.skipTest("Example book not found")
        self.assertEqual(self.book.format, 1)

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

        part_names = [os.path.basename(p.part_dir) for p in self.book.parts]
        self.assertIn("part-1-introduction", part_names)
        self.assertIn("part-2-advanced-topics", part_names)
        self.assertEqual(len(self.book.parts), 2)

    def test_book_chapters(self):
        """Test that example book chapters are loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        parts_by_name = {
            os.path.basename(p.part_dir): p for p in self.book.parts
        }
        part1 = parts_by_name.get("part-1-introduction")
        part2 = parts_by_name.get("part-2-advanced-topics")
        self.assertIsNotNone(part1)
        self.assertIsNotNone(part2)
        self.assertEqual(len(part1.chapters), 2)
        self.assertEqual(len(part2.chapters), 1)

    def test_book_flat_chapters_empty(self):
        """Test that format-1 book has no flat chapters."""
        if not self.has_example:
            self.skipTest("Example book not found")
        self.assertEqual(self.book.chapters, [])

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


class TestExampleBook2(unittest.TestCase):
    """Test with the format-2 example book in tests/input/example-book-2."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        cls.example_dir = os.path.join(
            os.path.dirname(__file__), "input", "example-book-2"
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
            "Example book not found at tests/input/example-book-2",
        )

    def test_book_format(self):
        """Test that format-2 book is detected as format 2."""
        if not self.has_example:
            self.skipTest("Example book not found")
        self.assertEqual(self.book.format, 2)

    def test_book_metadata(self):
        """Test that format-2 book metadata is loaded correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertEqual(self.book.title, "The Example Novel")
        self.assertEqual(self.book.author, "Jane Doe")

    def test_book_parts_empty(self):
        """Test that format-2 book has no parts."""
        if not self.has_example:
            self.skipTest("Example book not found")
        self.assertEqual(self.book.parts, [])

    def test_book_flat_chapters(self):
        """Test that format-2 book loads flat chapters correctly."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertEqual(len(self.book.chapters), 3)
        titles = [ch.title for ch in self.book.chapters]
        self.assertIn("Getting Started", titles)
        self.assertIn("The Writing Process", titles)
        self.assertIn("Advanced Techniques", titles)

    def test_book_chapters_sorted(self):
        """Test that flat chapters are sorted by chapter number."""
        if not self.has_example:
            self.skipTest("Example book not found")

        titles = [ch.title for ch in self.book.chapters]
        self.assertEqual(titles[0], "Getting Started")
        self.assertEqual(titles[1], "The Writing Process")
        self.assertEqual(titles[2], "Advanced Techniques")

    def test_book_chapters_have_content(self):
        """Test that flat chapters have content."""
        if not self.has_example:
            self.skipTest("Example book not found")

        for chapter in self.book.chapters:
            self.assertGreater(len(chapter.content), 0)

    def test_book_word_count(self):
        """Test word counting for format-2 book."""
        if not self.has_example:
            self.skipTest("Example book not found")

        word_count = self.book._count_words()
        self.assertGreater(word_count, 0)

    def test_book_about_files(self):
        """Test that about files are loaded for format-2 book."""
        if not self.has_example:
            self.skipTest("Example book not found")

        self.assertIsNotNone(self.book.about_book)
        self.assertIsNotNone(self.book.about_author)


if __name__ == "__main__":
    unittest.main()
