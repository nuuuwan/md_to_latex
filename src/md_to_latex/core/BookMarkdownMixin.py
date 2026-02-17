import re


class BookMarkdownMixin:
    """Mixin for markdown to LaTeX conversion."""

    def _process_markdown(self, text):
        """Convert markdown formatting to LaTeX."""
        # First escape LaTeX special characters
        # Escape underscores that are not part of markdown italic
        text = re.sub(r"_(?!_)", r"\\_", text)

        # Section breaks: --- or ... on their own line
        text = re.sub(
            r"^\s*(---|\.\.\.)\s*$",
            r"\n\n\\scenebreak\n\n",
            text,
            flags=re.MULTILINE,
        )

        # Bold: **text**
        text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text, flags=re.DOTALL)

        # Italic: *text*
        text = re.sub(
            r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)",
            r"\\textit{\1}",
            text,
            flags=re.DOTALL,
        )

        # Quotes: "text" -> \say{text}
        text = re.sub(r'"([^"]+)"', r"\\say{\1}", text)

        # Clean up problematic Unicode characters
        text = text.replace("\u2028", " ")
        text = text.replace("\u2029", "\n\n")

        return text
