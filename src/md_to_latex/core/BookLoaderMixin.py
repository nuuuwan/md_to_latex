import json
import os
import re

from rich.console import Console

from md_to_latex.core.Chapter import Chapter
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

    def _detect_format(self):
        """
        Detect the book format.

        Returns 1 if the book uses part/chapter directories (format 1),
        or 2 if chapters are top-level .md files (format 2).
        """
        if not os.path.isdir(self.book_dir):
            return 1
        entries = os.listdir(self.book_dir)
        has_parts = any(
            re.fullmatch(r"part-\d+-[a-z0-9\-]+", e)
            and os.path.isdir(os.path.join(self.book_dir, e))
            for e in entries
        )
        if has_parts:
            return 1
        has_flat_chapters = any(
            re.fullmatch(r"chapter-\d+.*\.md", e) for e in entries
        )
        if has_flat_chapters:
            return 2
        return 1

    def _load_parts(self):
        """Load all parts directly from the book directory."""
        parts = []

        if not os.path.isdir(self.book_dir):
            return parts

        # Get all part-<N>-<name> directories directly inside the book dir
        part_dirs = [
            d
            for d in os.listdir(self.book_dir)
            if (
                os.path.isdir(os.path.join(self.book_dir, d))
                and re.fullmatch(r"part-\d+-[a-z0-9\-]+", d)
            )
        ]

        # Sort parts by number
        part_dirs.sort(key=lambda d: int(d.split("-")[1]))

        for part_dir in part_dirs:
            part_path = os.path.join(self.book_dir, part_dir)
            parts.append(Part(part_path))

        return parts

    def _load_chapters_flat(self):
        """Load chapters from top-level chapter-NN-*.md files (format 2)."""
        if not os.path.isdir(self.book_dir):
            return []

        files = [
            f
            for f in os.listdir(self.book_dir)
            if re.fullmatch(r"chapter-\d+.*\.md", f)
        ]
        files.sort(key=lambda f: int(re.match(r"chapter-(\d+)", f).group(1)))

        return [
            Chapter.from_file(os.path.join(self.book_dir, f)) for f in files
        ]

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
        for chapter in self.chapters:
            word_count += len(chapter.content.split())
        return word_count

    def _has_section_breaks(self):
        """Check if any chapter content contains section break markers."""
        pattern = re.compile(r"^\s*(---|\.\.\.)\s*$", re.MULTILINE)

        all_chapters = [
            chapter for part in self.parts for chapter in part.chapters
        ] + list(self.chapters)

        if any(pattern.search(ch.content) for ch in all_chapters):
            return True

        has_breaks_in_about = (
            self.about_book and pattern.search(self.about_book)
        ) or (self.about_author and pattern.search(self.about_author))
        return bool(has_breaks_in_about)
