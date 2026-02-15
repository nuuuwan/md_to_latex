import re

from pylatex import NoEscape, Section


class Chapter:
    """Represents a chapter in the book."""

    def __init__(self, file_path):
        """
        Initialize a Chapter from a markdown file.

        Args:
            file_path: Path to the markdown file
        """
        self.file_path = file_path
        self.title = self._extract_title()
        self.content = self._read_content()

    def _extract_title(self):
        """Extract chapter title from the first line of the file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()

        # Remove markdown heading markers if present
        title = re.sub(r"^#+\s*", "", first_line)
        return title

    def _read_content(self):
        """Read and parse the markdown content."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Skip the first line (chapter title) and join the rest
        content = "".join(lines[1:]) if len(lines) > 1 else ""

        return content

    def _parse_markdown_to_latex(self, text):
        """
        Convert markdown formatting to LaTeX.

        Supports:
        - Bold: **text** or __text__ -> \\textbf{text}
        - Italic: *text* or _text_ -> \\textit{text}
        - Quotes: "text" -> \\say{text} in maroon color
        - Headings: ## Heading -> \\subsection{Heading}
        """
        # Convert markdown headings to LaTeX sections
        # #### Heading -> \subsubsection{Heading}
        text = re.sub(r"####\s+(.+)", r"\\subsubsection{\1}", text)
        # ### Heading -> \subsection{Heading}
        text = re.sub(r"###\s+(.+)", r"\\subsection{\1}", text)
        # ## Heading -> \subsection{Heading}
        text = re.sub(r"##\s+(.+)", r"\\subsection{\1}", text)

        # Process bold and italic
        # (order matters to handle **_text_** correctly)
        # Use DOTALL flag to match across line breaks

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
        # Match * for italic (single asterisk not preceded/followed by another
        # *)
        text = re.sub(
            r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
            r"\\textit{\1}",
            text,
            flags=re.DOTALL,
        )
        # For underscores, match single underscores (not double)
        text = re.sub(
            r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)",
            r"\\textit{\1}",
            text,
            flags=re.DOTALL,
        )

        # Quotes: "text" -> \say{text}
        # (will be styled in maroon in the preamble)
        text = re.sub(r'"([^"]+)"', r"\\say{\1}", text)

        # Handle paragraphs (double newlines)
        text = re.sub(r"\n\n+", r"\n\n", text)

        return text

    def to_latex(self, doc):
        """
        Add this chapter to the LaTeX document.

        Args:
            doc: PyLaTeX Document object
        """
        with doc.create(Section(self.title)):
            latex_content = self._parse_markdown_to_latex(self.content)
            doc.append(NoEscape(latex_content))
