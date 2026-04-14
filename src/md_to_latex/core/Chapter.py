import os
import re

from pylatex import NoEscape


class Chapter:
    """Represents a chapter in the book."""

    def __init__(self, chapter_dir):
        """
        Initialize a Chapter from a directory containing NNN.md files.

        Args:
            chapter_dir: Path to the chapter directory (e.g., chapter-01)
        """
        self.chapter_dir = chapter_dir
        self._md_files = self._sorted_md_files()
        self.title = self._extract_title()
        self.content = self._read_content()

    def _sorted_md_files(self):
        """Return sorted list of NNN.md file paths in the chapter dir."""
        if not os.path.isdir(self.chapter_dir):
            return []
        files = [
            f
            for f in os.listdir(self.chapter_dir)
            if re.fullmatch(r"\d+\.md", f)
        ]
        files.sort(key=lambda f: int(re.match(r"(\d+)\.md", f).group(1)))
        return [os.path.join(self.chapter_dir, f) for f in files]

    def _extract_title(self):
        """Extract chapter title from the kebab-case directory name."""
        dirname = os.path.basename(self.chapter_dir)
        # Expected format: chapter-<NN>-<name>
        match = re.match(r"chapter-(\d+)-(.+)", dirname)
        if match:
            chapter_name = match.group(2).replace("-", " ").title()
            return chapter_name
        # Fallback: chapter-<NN>
        match = re.match(r"chapter-(\d+)$", dirname)
        if match:
            return f"Chapter {int(match.group(1))}"
        return dirname.title()

    def _read_content(self):
        """Read and concatenate content from all NNN.md files."""
        parts = []
        for file_path in self._md_files:
            with open(file_path, "r", encoding="utf-8") as f:
                parts.append(f.read())
        return "".join(parts)

    def _convert_headings(self, text):
        """Convert markdown headings to LaTeX sections."""
        text = re.sub(r"####\s+(.+)", r"\\subsubsection*{\1}", text)
        text = re.sub(r"###\s+(.+)", r"\\subsection*{\1}", text)
        text = re.sub(r"##\s+(.+)", r"\\subsection*{\1}", text)
        text = re.sub(r"#\s+(.+)", r"\\section*{\1}", text)
        return text

    def _convert_bold_italic(self, text):
        """Convert bold and italic markdown to LaTeX."""
        # Bold and italic: ***text*** or ___text___
        text = re.sub(
            r"\*\*\*(.+?)\*\*\*",
            r"\\textbf{\\textit{\1}}",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"___(.+?)___", r"\\textbf{\\textit{\1}}", text, flags=re.DOTALL
        )

        # Bold: **text** or __text__
        text = re.sub(
            r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.DOTALL
        )
        text = re.sub(r"__(.+?)__", r"\\textbf{\1}", text, flags=re.DOTALL)

        # Italic: *text* or _text_
        text = re.sub(
            r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
            r"\\textit{\1}",
            text,
            flags=re.DOTALL,
        )
        text = re.sub(
            r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)",
            r"\\textit{\1}",
            text,
            flags=re.DOTALL,
        )
        return text

    def _parse_markdown_to_latex(self, text):
        """
        Convert markdown formatting to LaTeX.

        Supports:
        - Bold: **text** or __text__ -> \\textbf{text}
        - Italic: *text* or _text_ -> \\textit{text}
        - Quotes: "text" -> \\say{text} in maroon color
        - Headings: ## Heading -> \\subsection{Heading}
        - Section breaks: --- or ... -> \\scenebreak
        """
        text = self._convert_bold_italic(text)
        text = self._convert_headings(text)

        # Section breaks: --- or ... on their own line
        text = re.sub(
            r"^\s*(---|\.\.\.)\s*$",
            r"\n\n\\scenebreak\n\n",
            text,
            flags=re.MULTILINE,
        )

        # Escape remaining underscores (those not part of markdown)
        text = re.sub(r"_", r"\\_", text)

        # Escape hash signs (those not part of LaTeX commands)
        text = re.sub(r"(?<!\\)#", r"\\#", text)

        # Quotes: "text" -> \say{text}
        text = re.sub(r'"([^"]+)"', r"\\say{\1}", text)

        # Handle paragraphs (double newlines)
        text = re.sub(r"\n\n+", r"\n\n", text)

        # Clean up problematic Unicode characters
        # U+2028 (line separator) and U+2029 (paragraph separator)
        text = text.replace("\u2028", " ")
        text = text.replace("\u2029", "\n\n")

        return text

    def to_latex(self, doc):
        """
        Add this chapter to the LaTeX document.

        Args:
            doc: PyLaTeX Document object
        """
        doc.append(NoEscape(r"\chapter{" + self.title + "}"))
        latex_content = self._parse_markdown_to_latex(self.content)
        doc.append(NoEscape(latex_content))

        # Add page break after chapter
        doc.append(NoEscape(r"\newpage"))
