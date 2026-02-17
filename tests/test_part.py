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

    def test_part_creation(self):
        """Test basic part creation."""
        part_dir = os.path.join(self.temp_dir, "part-1-introduction")
        os.makedirs(part_dir)

        # Create a test chapter
        chapter_file = os.path.join(part_dir, "chapter-1.md")
        with open(chapter_file, "w", encoding="utf-8") as f:
            f.write("# Chapter One\n\nContent here.")

        part = Part(part_dir)
        self.assertEqual(part.title, "Introduction")
        self.assertEqual(len(part.chapters), 1)

    def test_title_extraction_from_dirname(self):
        """Test title extraction from directory name."""
        test_cases = [
            ("part-1-introduction", "Introduction"),
            ("part-2-the-journey", "The Journey"),
            ("part-3-advanced-topics", "Advanced Topics"),
            ("part-10-conclusion", "Conclusion"),
        ]

        for dirname, expected_title in test_cases:
            part_dir = os.path.join(self.temp_dir, dirname)
            os.makedirs(part_dir, exist_ok=True)

            part = Part(part_dir)
            self.assertEqual(part.title, expected_title)

            # Clean up for next iteration
            os.rmdir(part_dir)

    def test_chapter_loading(self):
        """Test chapter loading from directory."""
        part_dir = os.path.join(self.temp_dir, "part-1-test")
        os.makedirs(part_dir)

        # Create multiple chapters
        chapters = ["chapter-1.md", "chapter-2.md", "chapter-3.md"]
        for chapter_file in chapters:
            file_path = os.path.join(part_dir, chapter_file)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {chapter_file}\n\nContent.")

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 3)

    def test_chapter_sorting(self):
        """Test that chapters are loaded in sorted order."""
        part_dir = os.path.join(self.temp_dir, "part-1-test")
        os.makedirs(part_dir)

        # Create chapters in non-alphabetical order
        chapters = ["chapter-3.md", "chapter-1.md", "chapter-2.md"]
        for chapter_file in chapters:
            file_path = os.path.join(part_dir, chapter_file)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Chapter {chapter_file[-4]}\n\nContent.")

        part = Part(part_dir)
        # Should be sorted: chapter-1, chapter-2, chapter-3
        self.assertEqual(part.chapters[0].title, "Chapter 1")
        self.assertEqual(part.chapters[1].title, "Chapter 2")
        self.assertEqual(part.chapters[2].title, "Chapter 3")

    def test_empty_directory(self):
        """Test part with no chapters."""
        part_dir = os.path.join(self.temp_dir, "part-1-empty")
        os.makedirs(part_dir)

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 0)

    def test_non_markdown_files_ignored(self):
        """Test that non-markdown files are ignored."""
        part_dir = os.path.join(self.temp_dir, "part-1-test")
        os.makedirs(part_dir)

        # Create markdown and non-markdown files
        with open(
            os.path.join(part_dir, "chapter.md"), "w", encoding="utf-8"
        ) as f:
            f.write("# Chapter\n\nContent.")

        with open(
            os.path.join(part_dir, "notes.txt"), "w", encoding="utf-8"
        ) as f:
            f.write("Some notes")

        part = Part(part_dir)
        self.assertEqual(len(part.chapters), 1)


if __name__ == "__main__":
    unittest.main()
