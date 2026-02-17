import os

from pylatex import Document

from md_to_latex.core.BookFrontMatterMixin import BookFrontMatterMixin
from md_to_latex.core.BookLatexConfigMixin import BookLatexConfigMixin
from md_to_latex.core.BookLoaderMixin import BookLoaderMixin
from md_to_latex.core.BookMarkdownMixin import BookMarkdownMixin
from md_to_latex.core.BookOutputMixin import BookOutputMixin


class Book(
    BookLoaderMixin,
    BookMarkdownMixin,
    BookLatexConfigMixin,
    BookFrontMatterMixin,
    BookOutputMixin,
):
    """Represents a complete book with parts, chapters, and metadata."""

    def __init__(self, book_dir):
        """
        Initialize a Book from a directory.

        Args:
            book_dir: Path to the book directory
        """
        self.book_dir = book_dir
        self.metadata = self._load_metadata()
        self.title = self.metadata.get("title", os.path.basename(book_dir))
        self.subtitle = self.metadata.get("subtitle")
        self.author = self.metadata.get("author")
        self.year = self.metadata.get("year")
        self.edition = self.metadata.get("edition")
        self.publisher = self.metadata.get("publisher")
        self.parts = self._load_parts()
        self.about_author_title, self.about_author = self._load_about_file(
            "about-the-author.md"
        )
        self.about_book_title, self.about_book = self._load_about_file(
            "about-the-book.md"
        )
        self.output_dir = f"{book_dir}.latex"
        self.word_count = 0  # Will be calculated when generating

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

        self._setup_document_metadata(doc)
        self._add_front_matter(doc)

        for part in self.parts:
            part.to_latex(doc)

        output_path = os.path.join(self.output_dir, self.title)
        return self._generate_output(doc, output_path)
