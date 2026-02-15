#!/usr/bin/env python3
"""
Pipeline for converting Markdown book directory to LaTeX/PDF.

Usage:
    python workflows/pipeline.py <book_directory_path>

Example:
    python workflows/pipeline.py /path/to/my-book
"""

import os
import sys

from md_to_latex.core import Book

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def main():
    """Main pipeline execution."""
    if len(sys.argv) < 2:
        print("Usage: python workflows/pipeline.py <book_directory_path>")
        print("\nExample:")
        print("  python workflows/pipeline.py /path/to/my-book")
        sys.exit(1)

    book_dir = sys.argv[1]

    # Validate directory exists
    if not os.path.isdir(book_dir):
        print(f"Error: Directory not found: {book_dir}")
        sys.exit(1)

    print(f"Processing book directory: {book_dir}")
    print("-" * 60)

    # Create book object
    book = Book(book_dir)

    print(f"Book title: {book.title}")
    print(f"Number of parts: {len(book.parts)}")

    # Display structure
    for i, part in enumerate(book.parts, 1):
        print(f"  Part {i}: {part.title} ({len(part.chapters)} chapters)")

    print(f"\nGenerating LaTeX/PDF...")
    print("-" * 60)

    # Generate LaTeX and PDF
    output_file = book.toLatex()

    print("-" * 60)
    print(f"Output directory: {book.output_dir}")
    print(f"Output file: {output_file}")
    print("\nDone!")


if __name__ == "__main__":
    main()
