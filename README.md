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

## Supported Markdown Features

The library supports the following Markdown elements:

- **Bold** and *Italic* text formatting
- **Quotes**: Implemented using LaTeX `\say` command and rendered in maroon font color

## Output Formatting

The generated PDF follows professional book formatting standards:

- **Font**: Attractive book-optimized typeface
- **Paper**: A4 size
- **Spacing**: Double-spaced text
- **Printing**: Formatted for double-sided printing
- **Margins**: One-inch margins on all sides
- **Pages**: Numbered throughout
- **Table of Contents**: Automatically generated

## Expected Book Directory Structure

Your book directory should have the following structure:

- **Parts**: Located in a `parts/` folder
  - Each part is in a subfolder named `part-<n>-<part_name>`
  - Chapter files for each part are stored within the respective part directory
- **About sections**:
  - `about-the-author.md` - Information about the author
  - `about-the-book.md` - Book description and details
  - Both files should be in the root directory

## Library Structure

The library provides the following core classes:

- **Book** (`src/md_to_latex/core/Book.py`): Represents the complete book
- **Part** (`src/md_to_latex/core/Part.py`): Represents a book part
- **Chapter** (`src/md_to_latex/core/Chapter.py`): Represents a chapter

The `Book` class provides a `toLatex()` method that generates the LaTeX output using the Python library [PyLaTeX](https://github.com/JelteF/PyLaTeX).

## Output

The generated files (.tex, .pdf, and supporting files) are written to a new directory named `<book_directory_path>.latex`
