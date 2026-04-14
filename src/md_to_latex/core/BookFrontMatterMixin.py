from datetime import datetime

from pylatex import Command, NoEscape, Section


class BookFrontMatterMixin:
    """Mixin for generating book front matter."""

    def _build_title(self):
        """Build title string with metadata (subtitle and word count)."""
        title_parts = [
            f"{{\\fontsize{{24}}{{28.8}}\\selectfont {self.title}}}"
        ]
        if self.subtitle:
            title_parts.append(
                f"{{\\fontsize{{12}}{{14.4}}\\selectfont {self.subtitle}}}"
            )
        return "\\\\\n\\vspace{0.5em}\n".join(title_parts)

    def _format_date_str(self):
        """Format self.year into a display date string."""
        if not self.year:
            return r"{\fontsize{9}{10.8}\selectfont \today}"
        for fmt in ("%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(self.year, fmt).strftime("%B %d, %Y")
            except ValueError:
                pass
        return self.year

    def _build_date_block(self):
        """Build the date + word count preamble block."""
        date_str = self._format_date_str()
        date_part = f"{{\\fontsize{{9}}{{10.8}}\\selectfont {date_str}}}"
        word_part = (
            f"{{\\fontsize{{12}}{{14.4}}\\selectfont"
            f" {self.word_count:,} words}}"
        )
        return "\\\\\n\\vspace{0.3em}\n".join([date_part, word_part])

    def _setup_document_metadata(self, doc):
        """Set up document title, author, date, and custom commands."""
        title_with_metadata = self._build_title()
        doc.preamble.append(Command("title", NoEscape(title_with_metadata)))

        if self.author:
            author_text = (
                f"{{\\fontsize{{18}}{{21.6}}\\selectfont"
                f" By {self.author}}}"
            )
            doc.preamble.append(Command("author", NoEscape(author_text)))

        date_text = self._build_date_block()
        doc.preamble.append(Command("date", NoEscape(date_text)))

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
            doc.append(NoEscape(r"\newpage"))
            title = self.about_book_title or "About The Book"
            with doc.create(Section(title, numbering=False)):
                processed_content = self._process_markdown(self.about_book)
                doc.append(NoEscape(processed_content))

        if self.about_author:
            doc.append(NoEscape(r"\newpage"))
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
