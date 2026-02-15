import os

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
        self.about_author = self._load_about_file("about-the-author.md")
        self.about_book = self._load_about_file("about-the-book.md")
        self.output_dir = f"{book_dir}.latex"

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
                return f.read()
        return None

    def _add_formatting_packages(self, doc):
        """Add formatting packages to document preamble."""
        doc.preamble.append(
            Package(
                "geometry",
                options=["margin=1in", "a4paper"],
            )
        )
        doc.preamble.append(Package("setspace"))
        doc.preamble.append(Command("doublespacing"))
        doc.preamble.append(Package("microtype"))
        doc.preamble.append(Package("booktabs"))

    def _add_font_packages(self, doc):
        """Add font packages to document preamble."""
        doc.preamble.append(Package("palatino"))
        doc.preamble.append(Package("mathpazo"))
        doc.preamble.append(Package("inputenc", options=["utf8"]))
        doc.preamble.append(Package("fontenc", options=["T1"]))

    def _add_quote_styling(self, doc):
        """Add quote styling with maroon color."""
        doc.preamble.append(Package("dirtytalk"))
        doc.preamble.append(Package("xcolor"))
        doc.preamble.append(NoEscape(r"\definecolor{maroon}{RGB}{128,0,0}"))
        doc.preamble.append(
            NoEscape(
                r"\renewcommand{\say}[1]"
                r"{\textcolor{maroon}{\guillemotleft #1\guillemotright}}"
            )
        )

    def _configure_document(self, doc):
        r"""
        Configure the LaTeX document with formatting specifications.

        Settings:
        - A4 paper, double-sided printing
        - One-inch margins all around
        - Double-spacing
        - Attractive book font (Palatino)
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

    def _add_front_matter(self, doc):
        """Add title, table of contents, and about sections."""
        doc.append(NoEscape(r"\maketitle"))
        doc.append(NoEscape(r"\tableofcontents"))
        doc.append(NoEscape(r"\newpage"))

        if self.about_book:
            with doc.create(Section("About the Book", numbering=False)):
                doc.append(self.about_book)
            doc.append(NoEscape(r"\newpage"))

        if self.about_author:
            with doc.create(Section("About the Author", numbering=False)):
                doc.append(self.about_author)
            doc.append(NoEscape(r"\newpage"))

    def _generate_output(self, doc, output_path):
        """Generate PDF or LaTeX file."""
        try:
            doc.generate_pdf(
                output_path, clean_tex=False, compiler="pdflatex"
            )
            print(f"PDF generated successfully: {output_path}.pdf")
            return f"{output_path}.pdf"
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

        doc.preamble.append(Command("title", self.title))
        doc.preamble.append(Command("date", NoEscape(r"\today")))

        self._add_front_matter(doc)

        for part in self.parts:
            part.to_latex(doc)

        output_path = os.path.join(self.output_dir, self.title)
        return self._generate_output(doc, output_path)
