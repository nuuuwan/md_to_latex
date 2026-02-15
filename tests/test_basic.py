"""
Test the md_to_latex library.
"""

import os
import sys

from md_to_latex.core import Book, Chapter

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_chapter_markdown_parsing():
    """Test that Chapter correctly parses markdown formatting."""
    # Create a test markdown file
    test_dir = os.path.dirname(__file__)
    test_file = os.path.join(test_dir, "test_chapter.md")

    with open(test_file, "w") as f:
        f.write("# Test Chapter\n\n")
        f.write("This is **bold** and *italic* text.\n\n")
        f.write('A quote: "Hello, World!"\n')

    chapter = Chapter(test_file)
    content = chapter._parse_markdown_to_latex(chapter.content)

    # Verify bold conversion
    assert r"\textbf{bold}" in content

    # Verify italic conversion
    assert r"\textit{italic}" in content

    # Verify quote conversion
    assert r"\say{Hello, World!}" in content

    # Clean up
    os.remove(test_file)

    print("✓ Chapter markdown parsing test passed")


def test_book_structure():
    """Test that Book correctly loads structure."""
    example_dir = os.path.join(
        os.path.dirname(__file__), "input", "example-book"
    )

    if not os.path.isdir(example_dir):
        print("⚠ Skipping book structure test (example-book not found)")
        return

    book = Book(example_dir)

    # Verify book loaded
    assert book.title == "example-book"

    # Verify parts loaded
    assert len(book.parts) == 2

    # Verify chapters loaded
    assert len(book.parts[0].chapters) == 2  # Part 1 has 2 chapters
    assert len(book.parts[1].chapters) == 1  # Part 2 has 1 chapter

    # Verify about files loaded
    assert book.about_book is not None
    assert book.about_author is not None

    print("✓ Book structure test passed")


def main():
    """Run all tests."""
    print("Running md_to_latex tests...")
    print("-" * 60)

    test_chapter_markdown_parsing()
    test_book_structure()

    print("-" * 60)
    print("All tests passed!")


if __name__ == "__main__":
    main()
