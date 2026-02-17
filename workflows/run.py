#!/usr/bin/env python3
"""
Pipeline for converting Markdown book directory to LaTeX/PDF.

Usage:
    python workflows/md_to_latex.py <book_directory_path>

Example:
    python workflows/md_to_latex.py /path/to/my-book
"""

import os
import sys

from rich.console import Console

from md_to_latex import Book

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

console = Console()


def _validate_arguments():
    """Validate command-line arguments and return book directory."""
    if len(sys.argv) < 2:
        console.print(
            "[yellow]Usage:[/yellow] python workflows/md_to_latex.py "
            "<book_directory_path>"
        )
        console.print("\n[cyan]Example:[/cyan]")
        console.print("  python workflows/md_to_latex.py /path/to/my-book")
        sys.exit(1)

    book_dir = sys.argv[1]

    if not os.path.isdir(book_dir):
        console.print(f"[red]✗ Error:[/red] Directory not found: {book_dir}")
        sys.exit(1)

    return book_dir


def _display_book_info(book):
    """Display book metadata and structure."""
    console.print(
        f"\n[bold blue]📚 Processing book directory:[/bold blue] "
        f"{book.book_dir}"
    )
    console.rule(style="dim")

    console.print(f"[cyan]Book title:[/cyan] [bold]{book.title}[/bold]")
    console.print(f"[cyan]Number of parts:[/cyan] {len(book.parts)}")

    for i, part in enumerate(book.parts, 1):
        console.print(
            f"  [dim]Part {i}:[/dim] {part.title} "
            f"[dim]({len(part.chapters)} chapters)[/dim]"
        )


def _display_output_info(book, output_file):
    """Display output information after generation."""
    console.rule(style="dim")
    console.print(
        f"[cyan]Output directory:[/cyan] [bold]{book.output_dir}[/bold]"
    )
    console.print(f"[cyan]Output file:[/cyan] [bold]{output_file}[/bold]")
    console.print("\n[bold green]✓ Done![/bold green]")


def main():
    """Main pipeline execution."""
    book_dir = _validate_arguments()

    # Create book object
    book = Book(book_dir)

    _display_book_info(book)

    console.print("\n[bold green]⚙ Generating LaTeX/PDF...[/bold green]")
    console.rule(style="dim")

    # Generate LaTeX and PDF
    output_file = book.toLatex()

    _display_output_info(book, output_file)


if __name__ == "__main__":
    main()
