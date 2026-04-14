# md_to_latex

A library that transforms a directory of markdown files representing a book into a corresponding LaTeX PDF.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python workflows/pipeline.py <book_directory_path>
```

### Example

Try it out with the included example book:

```bash
python workflows/pipeline.py tests/input/example-book
```

This will generate `tests/input/example-book.latex/` containing the LaTeX source and PDF.

## Supported Markdown Features

The library supports the following Markdown elements:

- **Bold** and *Italic* text formatting
- **Headings**: `##` (subsection), `###` (subsection), `####` (subsubsection)
- **Quotes**: Implemented using LaTeX `\say` command and rendered in maroon font color

## Output Formatting

The generated PDF follows professional book formatting standards:

- **Font**: Attractive book-optimized typeface (EB Garamond)
- **Paper**: A4 size
- **Spacing**: Double-spaced text
- **Printing**: Formatted for double-sided printing
- **Margins**: One-inch margins on all sides
- **Pages**: Numbered throughout
  - Left pages (even): Page number on left, book title in center of header
  - Right pages (odd): Chapter name in center of header, page number on right
- **Table of Contents**: Automatically generated
- **Title Page**: Includes book title, subtitle (if provided), author, and total word count
- **Copyright Page**: Includes copyright notice, edition, publisher, and publication year (from metadata.json)
- **Chapter Breaks**: Each chapter ends with a page break
- **Section Headings**: Non-bold formatting for cleaner appearance

## Expected Book Directory Structure

Your book directory should have the following structure:

```
book/
├── metadata.json
├── about-the-author.md
├── about-the-book.md
├── part-1/
│   ├── chapter-01/
│   │   ├── 001.md
│   │   └── 002.md
│   └── chapter-02/
│       └── 001.md
└── part-2/
    └── chapter-03/
        └── 001.md
```

- **Book directory**: can be named anything (e.g. `book/`, `my-novel/`)
- **Part directories**: named `part-N` (e.g. `part-1`, `part-2`), placed directly inside the book directory. The title shown in output is derived from the number (e.g. "Part 1").
- **Chapter directories**: named `chapter-NN` (e.g. `chapter-01`, `chapter-12`), placed inside each part directory.
- **Markdown files**: named `NNN.md` (e.g. `001.md`, `002.md`), placed inside each chapter directory. Multiple files per chapter are concatenated in numeric order. The first line of the first file is used as the chapter title.
- **Supplementary files** (`about-the-author.md`, `about-the-book.md`, `metadata.json`): placed directly in the book directory.

### metadata.json Format

The `metadata.json` file should be placed in the root of your book directory with the following structure:

```json
{
  "title": "Your Book Title",
  "subtitle": "Optional Subtitle",
  "author": "Author Name",
  "year": "2026",
  "edition": "First Edition",
  "publisher": "Publisher Name"
}
```

All fields except `title` are optional. If `metadata.json` is not present, the directory name will be used as the title.

### Chapter File Format

Each chapter directory contains one or more `NNN.md` files (e.g. `001.md`, `002.md`). Files are read in numeric order and concatenated to form the chapter content.

The first line of the first file in each chapter directory is used as the chapter title:

```markdown
# Chapter Title

Chapter content starts here...
```

Subsequent files do not need a title heading — their content is appended directly.

## Library Structure

The library provides the following core classes:

- **Book** (`src/md_to_latex/core/Book.py`): Represents the complete book
- **Part** (`src/md_to_latex/core/Part.py`): Represents a book part
- **Chapter** (`src/md_to_latex/core/Chapter.py`): Represents a chapter

The `Book` class provides a `toLatex()` method that generates the LaTeX output using the Python library [PyLaTeX](https://github.com/JelteF/PyLaTeX).

## Output

The generated files (.tex, .pdf, and supporting files) are written to a new directory named `<book_directory_path>.latex`

## Testing

Run the basic tests to verify the installation:

```bash
python tests/test_basic.py
```

## Requirements

- Python 3.7+
- LaTeX distribution (e.g., TeX Live, MiKTeX) for PDF generation
- Required Python packages (see [requirements.txt](requirements.txt))
