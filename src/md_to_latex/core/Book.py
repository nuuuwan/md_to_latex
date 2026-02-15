import os
import re
import subprocess
import sys

from pylatex import Command, Document, NoEscape, Package, Section

from md_to_latex.core.Part import Part


class Book:
    """Represents a complete book with parts, chapters, and metadata."""

    def __init__(self, book_dir):
        """
        Initialize a Book from a directory.

        Args:
            book_dir: Path to the book directory
        """
        self.book_dir = book_dir
        self.title = os.path.basename(book_dir)
        self.parts = self._load_parts()
        self.about_author_title, self.about_author = self._load_about_file(
            "about-the-author.md"
        )
        self.about_book_title, self.about_book = self._load_about_file(
            "about-the-book.md"
        )
        self.output_dir = f"{book_dir}.latex"
        self.word_count = 0  # Will be calculated when generating

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

    def _process_markdown(self, text):
        """Convert markdown formatting to LaTeX."""
        # First escape LaTeX special characters (except those used in markdown)
        # Escape underscores that are not part of markdown italic
        text = re.sub(r"_(?!_)", r"\\_", text)

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

    def _add_formatting_packages(self, doc):
        """Add formatting packages to document preamble."""
        doc.preamble.append(
            Package(
                "geometry",
                options=["margin=1in", "a4paper", "headheight=15pt"],
            )
        )
        doc.preamble.append(Package("setspace"))
        doc.preamble.append(Command("doublespacing"))
        doc.preamble.append(Package("microtype"))
        doc.preamble.append(Package("booktabs"))
        doc.preamble.append(Package("fancyhdr"))
        doc.preamble.append(Package("titlesec"))

    def _add_font_packages(self, doc):
        """Add font packages to document preamble."""
        doc.preamble.append(Package("ebgaramond"))
        doc.preamble.append(Package("inputenc", options=["utf8"]))
        doc.preamble.append(Package("fontenc", options=["T1"]))

    def _add_quote_styling(self, doc):
        """Add quote styling with maroon color."""
        doc.preamble.append(Package("dirtytalk"))
        doc.preamble.append(Package("xcolor"))
        doc.preamble.append(NoEscape(r"\definecolor{maroon}{RGB}{128,0,0}"))
        doc.preamble.append(
            NoEscape(r"\renewcommand{\say}[1]" r"{\textcolor{maroon}{``#1''}}")
        )

    def _configure_headers(self, doc):
        """Configure custom headers and footers."""
        # Remove bold from section headings
        doc.preamble.append(
            NoEscape(r"\titleformat{\section}{\Large}{\thesection}{1em}{}")
        )
        doc.preamble.append(
            NoEscape(
                r"\titleformat{\subsection}{\large}" r"{\thesubsection}{1em}{}"
            )
        )

        # Set up fancy headers
        doc.preamble.append(NoEscape(r"\pagestyle{fancy}"))
        doc.preamble.append(NoEscape(r"\fancyhf{}"))

        # Left page (even): book title in center, page number on left
        doc.preamble.append(NoEscape(r"\fancyhead[LE]{\thepage}"))
        doc.preamble.append(NoEscape(r"\fancyhead[CE]{\booktitle}"))

        # Right page (odd): chapter name in center, page number on right
        doc.preamble.append(NoEscape(r"\fancyhead[RO]{\thepage}"))
        doc.preamble.append(NoEscape(r"\fancyhead[CO]{\leftmark}"))

        # Remove header rule
        doc.preamble.append(NoEscape(r"\renewcommand{\headrulewidth}{0pt}"))

    def _configure_document(self, doc):
        r"""
        Configure the LaTeX document with formatting specifications.

        Settings:
        - A4 paper, double-sided printing
        - One-inch margins all around
        - Double-spacing
        - Attractive book font (EB Garamond)
        - Maroon color for quotes using \say command
        - Table of contents
        - Page numbering
        """
        doc.documentclass = Command(
            "documentclass",
            options=["a4paper", "twoside", "12pt"],
            arguments=["book"],
        )
        self._add_formatting_packages(doc)
        self._add_font_packages(doc)
        self._add_quote_styling(doc)
        self._configure_headers(doc)

    def _add_front_matter(self, doc):
        """Add title, table of contents, and about sections."""
        doc.append(NoEscape(r"\maketitle"))

        # Add copyright page
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\begin{center}"))
        doc.append(NoEscape(r"\textbf{Copyright Notice}\\"))
        doc.append(NoEscape(r"\vspace{1em}"))
        doc.append(
            NoEscape(
                r"All rights reserved. No part of this publication may be "
                r"reproduced, distributed, or transmitted in any form or by "
                r"any means without the prior written permission of the author."
            )
        )
        doc.append(NoEscape(r"\end{center}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\newpage"))

        doc.append(NoEscape(r"\tableofcontents"))
        doc.append(NoEscape(r"\newpage"))

        if self.about_book:
            title = self.about_book_title or "About the Book"
            with doc.create(Section(title, numbering=False)):
                processed_content = self._process_markdown(self.about_book)
                doc.append(NoEscape(processed_content))
            doc.append(NoEscape(r"\newpage"))

        if self.about_author:
            title = self.about_author_title or "About the Author"
            with doc.create(Section(title, numbering=False)):
                processed_content = self._process_markdown(self.about_author)
                doc.append(NoEscape(processed_content))
            doc.append(NoEscape(r"\newpage"))

    def _generate_output(self, doc, output_path):
        """Generate PDF or LaTeX file."""
        try:
            doc.generate_pdf(output_path, clean_tex=False, compiler="pdflatex")
            pdf_path = f"{output_path}.pdf"
            print(f"PDF generated successfully: {pdf_path}")

            # Open the PDF on macOS
            if sys.platform == "darwin":
                subprocess.run(["open", pdf_path])

            return pdf_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            doc.generate_tex(output_path)
            print(f"LaTeX file saved: {output_path}.tex")
            return f"{output_path}.tex"

    def toLatex(self):
        """
        Generate the LaTeX document and compile to PDF.

        Returns:
            Path to the generated PDF file
        """
        os.makedirs(self.output_dir, exist_ok=True)

        doc = Document(
            documentclass="book",
            document_options=["a4paper", "twoside", "12pt"],
        )

        self._configure_document(doc)

        # Calculate word count
        self.word_count = self._count_words()

        # Add title with word count
        title_with_count = (
            f"{self.title}\\\\\\vspace{{0.5em}}"
            f"{{\\large Word Count: {self.word_count:,}}}"
        )
        doc.preamble.append(Command("title", NoEscape(title_with_count)))
        doc.preamble.append(Command("date", NoEscape(r"\today")))

        # Define book title command for headers
        doc.preamble.append(
            NoEscape(f"\\newcommand{{\\booktitle}}{{{self.title}}}")
        )

        self._add_front_matter(doc)

        for part in self.parts:
            part.to_latex(doc)

        output_path = os.path.join(self.output_dir, self.title)
        return self._generate_output(doc, output_path)
