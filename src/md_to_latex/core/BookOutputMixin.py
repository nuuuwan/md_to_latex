import os
import subprocess
import sys

from rich.console import Console

console = Console()


class BookOutputMixin:
    """Mixin for generating output files."""

    def _compile_pdf(self, tex_dir, tex_filename):
        """Compile LaTeX to PDF using pdflatex."""
        # Run pdflatex twice to generate table of contents
        # First pass creates .toc file, second pass uses it
        for _ in range(2):
            result = subprocess.run(
                ["pdflatex", "--interaction=nonstopmode", tex_filename],
                cwd=tex_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                console.print("[red]✗ pdflatex failed[/red]")
                console.print("[dim]stdout:[/dim]", result.stdout)
                console.print("[dim]stderr:[/dim]", result.stderr)
                msg = (
                    f"pdflatex failed with return code "
                    f"{result.returncode}"
                )
                raise RuntimeError(msg)

    def _generate_output(self, doc, output_path):
        """Generate PDF or LaTeX file."""
        try:
            # Generate the .tex file first
            doc.generate_tex(output_path)
            tex_file = f"{output_path}.tex"
            tex_dir = os.path.dirname(tex_file)
            tex_filename = os.path.basename(tex_file)

            self._compile_pdf(tex_dir, tex_filename)

            pdf_path = f"{output_path}.pdf"
            console.print(
                f"[green]✓ PDF generated successfully:[/green] "
                f"[bold]{pdf_path}[/bold]"
            )

            # Open the PDF on macOS
            if sys.platform == "darwin":
                subprocess.run(["open", pdf_path], check=False)

            return pdf_path
        except Exception as e:
            console.print(f"[red]✗ Error generating PDF:[/red] {e}")
            doc.generate_tex(output_path)
            console.print(
                f"[yellow]→ LaTeX file saved:[/yellow] "
                f"[bold]{output_path}.tex[/bold]"
            )
            return f"{output_path}.tex"
