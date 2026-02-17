from pylatex import Command, NoEscape, Package


class BookLatexConfigMixin:
    """Mixin for LaTeX document configuration."""

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
            NoEscape(r"\renewcommand{\say}[1]{\textcolor{maroon}{``#1''}}")
        )

    def _add_section_break_command(self, doc):
        """Add custom section break command."""
        doc.preamble.append(
            NoEscape(
                r"\newcommand{\scenebreak}{%"
                "\n"
                r"  \par\bigskip%"
                "\n"
                r"  \centerline{\large\ldots}%"
                "\n"
                r"  \bigskip\par%"
                "\n"
                r"}%"
            )
        )

    def _configure_headers(self, doc):
        """Configure custom headers and footers."""
        # Remove bold from section headings
        doc.preamble.append(
            NoEscape(r"\titleformat{\section}{\Large}{\thesection}{1em}{}")
        )
        doc.preamble.append(
            NoEscape(
                r"\titleformat{\subsection}{\large}{\thesubsection}{1em}{}"
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
        """Configure LaTeX document with book formatting."""
        doc.documentclass = Command(
            "documentclass",
            options=["a4paper", "twoside", "12pt"],
            arguments=["book"],
        )
        self._add_formatting_packages(doc)
        self._add_font_packages(doc)
        self._add_quote_styling(doc)
        if self._has_section_breaks():
            self._add_section_break_command(doc)
        self._configure_headers(doc)
