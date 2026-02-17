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


def main():
    """Main pipeline execution."""
    if len(sys.argv) < 2:
        console.print(
            "[yellow]Usage:[/yellow] python workflows/md_to_latex.py "
            "<book_directory_path>"
        )
        console.print("\n[cyan]Example:[/cyan]")
        console.print("  python workflows/md_to_latex.py /path/to/my-book")
        sys.exit(1)

    book_dir = sys.argv[1]

    # Validate directory exists
    if not os.path.isdir(book_dir):
        console.print(f"[red]✗ Error:[/red] Directory not found: {book_dir}")
        sys.exit(1)

    console.print(
        f"\n[bold blue]📚 Processing book directory:[/bold blue] "
        f"{book_dir}"
    )
    console.rule(style="dim")

    # Create book object
    book = Book(book_dir)

    console.print(f"[cyan]Book title:[/cyan] [bold]{book.title}[/bold]")
    console.print(f"[cyan]Number of parts:[/cyan] {len(book.parts)}")

    # Display structure
    for i, part in enumerate(book.parts, 1):
        console.print(
            f"  [dim]Part {i}:[/dim] {part.title} "
            f"[dim]({len(part.chapters)} chapters)[/dim]"
        )

    console.print("\n[bold green]⚙ Generating LaTeX/PDF...[/bold green]")
    console.rule(style="dim")

    # Generate LaTeX and PDF
    output_file = book.toLatex()

    console.rule(style="dim")
    console.print(
        f"[cyan]Output directory:[/cyan] [bold]{book.output_dir}[/bold]"
    )
    console.print(f"[cyan]Output file:[/cyan] [bold]{output_file}[/bold]")
    console.print("\n[bold green]✓ Done![/bold green]")


if __name__ == "__main__":
    main()
