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
        """Extract part title from directory name."""
        dirname = os.path.basename(self.part_dir)
        # Expected format: part-<n>-<part_name>
        match = re.match(r"part-\d+-(.+)", dirname)
        if match:
            title = match.group(1)
            # Replace hyphens and underscores with spaces, capitalize
            title = title.replace("-", " ").replace("_", " ").title()
            return title
        return dirname.title()

    def _load_chapters(self):
        """Load all markdown files in the part directory as chapters."""
        chapters = []

        if not os.path.isdir(self.part_dir):
            return chapters

        # Get all .md files in the directory
        md_files = [f for f in os.listdir(self.part_dir) if f.endswith(".md")]

        # Sort files alphabetically
        md_files.sort()

        for md_file in md_files:
            file_path = os.path.join(self.part_dir, md_file)
            chapters.append(Chapter(file_path))

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
