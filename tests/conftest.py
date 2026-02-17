"""
Test fixtures for md_to_latex tests.
"""

import json
import os
import shutil
import tempfile

import pytest


@pytest.fixture(scope="session")
def example_book_dir():
    """
    Create an example book directory structure for testing.

    This fixture creates a temporary directory with the full structure
    of an example book, including metadata, parts, chapters, and about files.
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="md_to_latex_test_")
    book_dir = os.path.join(temp_dir, "example-book")
    os.makedirs(book_dir)

    try:
        # Create metadata.json
        metadata = {
            "title": "The Example Novel",
            "subtitle": "A Journey Through Markdown and LaTeX",
            "author": "Jane Doe",
            "year": "2026",
            "edition": "First Edition",
            "publisher": "Independent Press",
        }
        with open(
            os.path.join(book_dir, "metadata.json"), "w", encoding="utf-8"
        ) as f:
            json.dump(metadata, f, indent=2)

        # Create about-the-book.md
        about_book_content = """# Example Book

This is an **example book** to demonstrate the *md_to_latex* library.
"""
        with open(
            os.path.join(book_dir, "about-the-book.md"), "w", encoding="utf-8"
        ) as f:
            f.write(about_book_content)

        # Create about-the-author.md
        about_author_content = """# About the Author

**John Doe** is an *author* and "software engineer" with a passion for writing.
"""
        with open(
            os.path.join(book_dir, "about-the-author.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(about_author_content)

        # Create parts directory structure
        parts_dir = os.path.join(book_dir, "parts")
        os.makedirs(parts_dir)

        # Part 1: Foundations
        part1_dir = os.path.join(parts_dir, "part-1-foundations")
        os.makedirs(part1_dir)

        chapter1_content = """# Introduction to Writing

This chapter introduces the **art of writing**. Writing is *fundamental* to human communication.

...

As the famous author said, "Writing is thinking on paper."

## Key Concepts

Writing involves both **creativity** and *discipline*. The best writers understand that "practice makes perfect" and dedicate themselves to their craft.
"""
        with open(
            os.path.join(part1_dir, "chapter-1-introduction.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(chapter1_content)

        chapter2_content = """# The Writing Process

The **writing process** involves several *key stages*:

1. **Planning**: Think about what you want to say
2. **Drafting**: Write your first draft
3. **Revising**: Improve your work
4. **Editing**: Polish the details

As Hemingway said, "The first draft of anything is garbage." This reminds us to embrace **revision** as a *crucial* part of the process.
"""
        with open(
            os.path.join(part1_dir, "chapter-2-process.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(chapter2_content)

        # Part 2: Advanced
        part2_dir = os.path.join(parts_dir, "part-2-advanced")
        os.makedirs(part2_dir)

        chapter3_content = """# Advanced Techniques

**Advanced writers** develop their own *unique voice*. This chapter explores sophisticated techniques.

## Finding Your Voice

Your voice should be **authentic** and *distinctive*. As writers often say, "Write what you know" and let your personality shine through.

## Style and Tone

Mastering **style** and *tone* takes practice. Remember that "less is more" when it comes to effective writing.
"""
        with open(
            os.path.join(part2_dir, "chapter-3-techniques.md"),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(chapter3_content)

        yield book_dir

    finally:
        # Cleanup temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session", autouse=True)
def create_example_book_in_tests_input(example_book_dir):
    """
    Copy the example book to tests/input/example-book for integration tests.

    This fixture automatically runs and ensures the example book exists
    in the expected location for all tests.
    """
    # Create tests/input directory if it doesn't exist
    tests_dir = os.path.dirname(__file__)
    input_dir = os.path.join(tests_dir, "input")
    os.makedirs(input_dir, exist_ok=True)

    # Target directory for example book
    target_dir = os.path.join(input_dir, "example-book")

    # Remove existing directory if present
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    # Copy example book to tests/input
    shutil.copytree(example_book_dir, target_dir)

    yield target_dir

    # Optionally cleanup after all tests (commented out to keep for inspection)
    # shutil.rmtree(target_dir, ignore_errors=True)
