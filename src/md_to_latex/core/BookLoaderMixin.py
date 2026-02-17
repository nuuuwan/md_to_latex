import json
import os
import re

from rich.console import Console

from md_to_latex.core.Part import Part

console = Console()


class BookLoaderMixin:
    """Mixin for loading book data from files."""

    def _load_metadata(self):
        """Load metadata from metadata.json file."""
        metadata_path = os.path.join(self.book_dir, "metadata.json")
        if os.path.isfile(metadata_path):
            try:
                with open(metadata_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                console.print(
                    f"[yellow]⚠ Warning:[/yellow] "
                    f"Could not load metadata.json: {e}"
                )
                return {}
        return {}

    def _load_parts(self):
        """Load all parts from the parts directory."""
        parts = []
        parts_dir = os.path.join(self.book_dir, "parts")

        if not os.path.isdir(parts_dir):
            return parts

        # Get all part directories
        part_dirs = [
            d
            for d in os.listdir(parts_dir)
            if (
                os.path.isdir(os.path.join(parts_dir, d))
                and d.startswith("part-")
            )
        ]

        # Sort parts by number
        part_dirs.sort()

        for part_dir in part_dirs:
            part_path = os.path.join(parts_dir, part_dir)
            parts.append(Part(part_path))

        return parts

    def _load_about_file(self, filename):
        """Load content from an about file."""
        file_path = os.path.join(self.book_dir, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if not lines:
                return None, None
            # Extract title from first line
            title = re.sub(r"^#+\s*", "", lines[0].strip())
            # Content is everything after the first line
            content = "".join(lines[1:]) if len(lines) > 1 else ""
            return title, content
        return None, None

    def _count_words(self):
        """Count total words in all chapters."""
        word_count = 0
        for part in self.parts:
            for chapter in part.chapters:
                word_count += len(chapter.content.split())
        return word_count

    def _has_section_breaks(self):
        """Check if any chapter content contains section break markers."""
        pattern = re.compile(r"^\s*(---|\.\.\.)\s*$", re.MULTILINE)

        # Check all chapter content
        has_breaks_in_chapters = any(
            pattern.search(chapter.content)
            for part in self.parts
            for chapter in part.chapters
        )
        if has_breaks_in_chapters:
            return True

        # Check about files
        has_breaks_in_about = (
            self.about_book and pattern.search(self.about_book)
        ) or (self.about_author and pattern.search(self.about_author))
        return bool(has_breaks_in_about)
