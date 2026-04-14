"""
Test cases for the Part class.
"""

import os
import tempfile
import unittest

from md_to_latex.core.Part import Part


class TestPartInit(unittest.TestCase):
    """Test Part initialization."""

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

    def _make_chapter_dir(self, part_dir, dirname, title="Chapter Title"):
        ch_dir = os.path.join(part_dir, dirname)
        os.makedirs(ch_dir, exist_ok=True)
        with open(os.path.join(ch_dir, "001.md"), "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\nContent.")
        return ch_dir

    def test_part_creation(self):
        """Test basic part creation."""
        part_dir = os.path.join(self.temp_dir, "part-1")
        os.makedirs(part_dir)
        self._make_chapter_dir(part_dir, "chapter-01", "Chapter One")

        part = Part(part_dir)
        self.assertEqual(part.title, "Part 1")
        self.assertEqual(len(part.chapters), 1)

    def test_title_extraction_from_dirname(self):
        """Test title extraction from directory name."""
        test_cases = [
            ("part-1", "Part 1"),
            ("part-2", "Part 2"),
            ("part-10", "Part 10"),
        ]

        for dirname, expected_title in test_cases:
            part_dir = os.path.join(self.temp_dir, dirname)
            os.makedirs(part_dir, exist_ok=True)

            part = Part(part_dir)
            self.assertEqual(part.title, expected_title)

            os.rmdir(part_dir)

    def test_chapter_loading(self):
        """Test chapter loading from subdirectories."""
        part_dir = os.path.join(self.temp_dir, "part-1")
        os.makedirs(part_dir)

        for i in range(1, 4):
            self._make_chapter_dir(part_dir, f"chapter-0{i}", f"Chapter {i}")

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 3)

    def test_chapter_sorting(self):
        """Test that chapters are loaded in sorted order."""
        part_dir = os.path.join(self.temp_dir, "part-1")
        os.makedirs(part_dir)

        # Create chapters in non-sequential order
        for i in [3, 1, 2]:
            self._make_chapter_dir(part_dir, f"chapter-0{i}", f"Chapter {i}")

        part = Part(part_dir)
        self.assertEqual(part.chapters[0].title, "Chapter 1")
        self.assertEqual(part.chapters[1].title, "Chapter 2")
        self.assertEqual(part.chapters[2].title, "Chapter 3")

    def test_empty_directory(self):
        """Test part with no chapters."""
        part_dir = os.path.join(self.temp_dir, "part-1")
        os.makedirs(part_dir)

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 0)

    def test_non_chapter_dirs_ignored(self):
        """Test that directories not matching chapter-NN are ignored."""
        part_dir = os.path.join(self.temp_dir, "part-1")
        os.makedirs(part_dir)

        self._make_chapter_dir(part_dir, "chapter-01", "Real Chapter")

        # Extra dirs that should be ignored
        os.makedirs(os.path.join(part_dir, "notes"), exist_ok=True)
        os.makedirs(os.path.join(part_dir, "chapter-bad"), exist_ok=True)

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 1)


if __name__ == "__main__":
    unittest.main()
