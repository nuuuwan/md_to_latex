import os
import re

from pylatex import NoEscape

from md_to_latex.core.Chapter import Chapter


class Part:
    """Represents a part of the book containing multiple chapters."""

    def __init__(self, part_dir):
        """
        Initialize a Part from a directory.

        Args:
            part_dir: Path to the part directory (e.g., part-1-introduction)
        """
        self.part_dir = part_dir
        self.title = self._extract_title()
        self.chapters = self._load_chapters()

    def _extract_title(self):
        """Extract part title from directory name (supports kebab-case)."""
        dirname = os.path.basename(self.part_dir)
        # Expected format: part-<n>-<name>
        match = re.match(r"part-(\d+)-(.+)", dirname)
        if match:
            part_num = int(match.group(1))
            part_name = match.group(2).replace('-', ' ').title()
            return f"Part {part_num}: {part_name}"
        # Fallback: part-<n>
        match = re.match(r"part-(\d+)$", dirname)
        if match:
            return f"Part {int(match.group(1))}"
        return dirname.title()

    def _load_chapters(self):
        """Load all chapter-<NN>-<name> subdirectories in the part directory."""
        chapters = []

        if not os.path.isdir(self.part_dir):
            return chapters

        # Get all chapter-<NN>-<name> subdirectories
        chapter_dirs = [
            d
            for d in os.listdir(self.part_dir)
            if (
                os.path.isdir(os.path.join(self.part_dir, d))
                and re.fullmatch(r"chapter-\d+-[a-z0-9\-]+", d)
            )
        ]

        # Sort by chapter number
        chapter_dirs.sort(key=lambda d: int(d.split("-")[1]))

        for chapter_dir in chapter_dirs:
            dir_path = os.path.join(self.part_dir, chapter_dir)
            chapters.append(Chapter(dir_path))

        return chapters

    def to_latex(self, doc):
        """
        Add this part to the LaTeX document.

        Args:
            doc: PyLaTeX Document object
        """
        # Add \part{title} command
        doc.append(NoEscape(r"\part{" + self.title + "}"))

        for chapter in self.chapters:
            chapter.to_latex(doc)
