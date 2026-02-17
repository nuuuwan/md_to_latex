from pylatex import Command, NoEscape, Section


class BookFrontMatterMixin:
    """Mixin for generating book front matter."""

    def _build_title(self):
        """Build title string with metadata (subtitle and word count)."""
        title_parts = [self.title]
        if self.subtitle:
            title_parts.append(f"{{\\small {self.subtitle}}}")
        title_parts.append(f"{{\\normalsize {self.word_count:,} words}}")
        return "\\\\\n\\vspace{0.5em}\n".join(title_parts)

    def _setup_document_metadata(self, doc):
        """Set up document title, author, date, and custom commands."""
        title_with_metadata = self._build_title()
        doc.preamble.append(Command("title", NoEscape(title_with_metadata)))

        # Add author if specified in metadata
        if self.author:
            doc.preamble.append(Command("author", self.author))

        # Add date (year from metadata or today's date)
        if self.year:
            doc.preamble.append(Command("date", self.year))
        else:
            doc.preamble.append(Command("date", NoEscape(r"\today")))

        # Define book title command for headers
        doc.preamble.append(
            NoEscape(f"\\newcommand{{\\booktitle}}{{{self.title}}}")
        )

    def _add_copyright_page(self, doc):
        """Add copyright page with book metadata."""
        doc.append(NoEscape(r"\thispagestyle{empty}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\begin{center}"))

        # Add book metadata
        if self.edition:
            doc.append(NoEscape(f"{self.edition}\\\\"))
            doc.append(NoEscape(r"\vspace{0.5em}"))

        if self.publisher:
            doc.append(NoEscape(f"Published by {self.publisher}\\\\"))
            doc.append(NoEscape(r"\vspace{0.5em}"))

        if self.year:
            copyright_line = f"Copyright \\copyright\\ {self.year}"
            if self.author:
                copyright_line += f" by {self.author}"
            doc.append(NoEscape(copyright_line + r"\\"))
            doc.append(NoEscape(r"\vspace{1em}"))

        doc.append(NoEscape(r"\end{center}"))
        doc.append(NoEscape(r"\vspace*{\fill}"))
        doc.append(NoEscape(r"\newpage"))

    def _add_about_sections(self, doc):
        """Add about book and about author sections."""
        if self.about_book:
            title = self.about_book_title or "About the Book"
            with doc.create(Section(title, numbering=False)):
                processed_content = self._process_markdown(self.about_book)
                doc.append(NoEscape(processed_content))

        if self.about_author:
            title = self.about_author_title or "About the Author"
            with doc.create(Section(title, numbering=False)):
                processed_content = self._process_markdown(self.about_author)
                doc.append(NoEscape(processed_content))

    def _add_front_matter(self, doc):
        """Add title, table of contents, and about sections."""
        doc.append(NoEscape(r"\maketitle"))
        self._add_copyright_page(doc)
        doc.append(NoEscape(r"\tableofcontents"))
        self._add_about_sections(doc)
