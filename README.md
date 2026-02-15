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
- **Table of Contents**: Automatically generated
- **Title Page**: Includes book title and total word count
- **Copyright Page**: Standard copyright notice on page 2
- **Chapter Breaks**: Each chapter ends with a page break

## Expected Book Directory Structure

Your book directory should have the following structure:

- **Parts**: Located in a `parts/` folder
  - Each part is in a subfolder named `part-<n>-<part_name>`
  - Chapter files for each part are stored within the respective part directory
  - **Important**: The first line of each chapter file is used as the chapter title
- **About sections**:
  - `about-the-author.md` - Information about the author
  - `about-the-book.md` - Book description and details
  - Both files should be in the root directory

### Chapter File Format

Each chapter markdown file should start with the chapter title on the first line:

```markdown
# Chapter Title

Chapter content starts here...
```

The first line (with or without the `#` marker) will be used as the chapter title in the LaTeX output.

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
