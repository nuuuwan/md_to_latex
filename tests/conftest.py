"""
Test fixtures for md_to_latex tests.
"""

import json
import os
import shutil
import tempfile

import pytest


def _create_metadata_file(book_dir):
    """Create metadata.json file for test book."""
    metadata = {
        "title": "The Example Novel",
        "subtitle": "A Journey Through Markdown and LaTeX",
        "author": "Jane Doe",
        "year": "2026-02-17",
        "edition": "First Edition",
        "publisher": "Independent Press",
    }
    metadata_path = os.path.join(book_dir, "metadata.json")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)


def _create_about_files(book_dir):
    """Create about-the-book.md and about-the-author.md files."""
    about_book_content = (
        "# About The Book\n\nThis is an **example book** to demonstrate "
        "the *md_to_latex* library.\n"
    )
    about_book_path = os.path.join(book_dir, "about-the-book.md")
    with open(about_book_path, "w", encoding="utf-8") as f:
        f.write(about_book_content)

    about_author_content = (
        "# About the Author\n\n**John Doe** is an *author* and "
        '"software engineer" with a passion for writing.\n'
    )
    about_author_path = os.path.join(book_dir, "about-the-author.md")
    with open(about_author_path, "w", encoding="utf-8") as f:
        f.write(about_author_content)


def _create_chapter01(part1_dir):
    """Create chapter-01 content for Part 1."""
    ch1_dir = os.path.join(part1_dir, "chapter-01")
    os.makedirs(ch1_dir, exist_ok=True)

    ch1_file1 = (
        "# Introduction to Writing\n\n"
        "This chapter introduces the **art of writing**. "
        "Writing is *fundamental* to human communication.\n\n"
        "...\n\n"
        'As the famous author said, "Writing is thinking on paper."\n\n'
        "## Key Concepts\n\n"
        "Writing involves both **creativity** and *discipline*. "
        'The best writers understand that "practice makes perfect" '
        "and dedicate themselves to their craft.\n"
    )
    with open(os.path.join(ch1_dir, "001.md"), "w", encoding="utf-8") as f:
        f.write(ch1_file1)

    ch1_file2 = (
        "When you sit down to write, the blank page can feel daunting. "
        "But every great work begins with a single sentence.\n\n"
        "Remember that writing is a *process*, not a single act. "
        "Allow yourself to **draft freely** before refining.\n"
    )
    with open(os.path.join(ch1_dir, "002.md"), "w", encoding="utf-8") as f:
        f.write(ch1_file2)


def _create_chapter02(part1_dir):
    """Create chapter-02 content for Part 1."""
    ch2_dir = os.path.join(part1_dir, "chapter-02")
    os.makedirs(ch2_dir, exist_ok=True)

    ch2_file1 = (
        "# The Writing Process\n\n"
        "The **writing process** involves several *key stages*:\n\n"
        "1. **Planning**: Think about what you want to say\n"
        "2. **Drafting**: Write your first draft\n"
        "3. **Revising**: Improve your work\n"
        "4. **Editing**: Polish the details\n\n"
        'As Hemingway said, "The first draft of anything is garbage." '
        "This reminds us to embrace **revision** as a *crucial* part "
        "of the process. #ThisIsAHashtag\n"
    )
    with open(os.path.join(ch2_dir, "001.md"), "w", encoding="utf-8") as f:
        f.write(ch2_file1)


def _create_part1_chapters(part1_dir):
    """Create chapters for Part 1."""
    _create_chapter01(part1_dir)
    _create_chapter02(part1_dir)


def _create_part2_chapters(part2_dir):
    """Create chapters for Part 2."""
    ch3_dir = os.path.join(part2_dir, "chapter-03")
    os.makedirs(ch3_dir, exist_ok=True)

    ch3_file1 = (
        "# Advanced Techniques\n\n"
        "**Advanced writers** develop their own *unique voice*. "
        "This chapter explores sophisticated techniques.\n\n"
        "## Finding Your Voice\n\n"
        "Your voice should be **authentic** and *distinctive*. "
        'As writers often say, "Write what you know" and let your '
        "personality shine through.\n\n"
        "## Style and Tone\n\n"
        "Mastering **style** and *tone* takes practice. "
        'Remember that "less is more" when it comes to effective '
        "writing.\n"
    )
    with open(os.path.join(ch3_dir, "001.md"), "w", encoding="utf-8") as f:
        f.write(ch3_file1)


@pytest.fixture(scope="session")
def example_book_dir():
    """
    Create an example book directory structure for testing.

    This fixture creates a temporary directory with the full structure
    of an example book, including metadata, parts, chapters, and files.
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp(prefix="md_to_latex_test_")
    book_dir = os.path.join(temp_dir, "example-book")
    os.makedirs(book_dir)

    try:
        _create_metadata_file(book_dir)
        _create_about_files(book_dir)

        # Part 1
        part1_dir = os.path.join(book_dir, "part-1")
        os.makedirs(part1_dir)
        _create_part1_chapters(part1_dir)

        # Part 2
        part2_dir = os.path.join(book_dir, "part-2")
        os.makedirs(part2_dir)
        _create_part2_chapters(part2_dir)

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
