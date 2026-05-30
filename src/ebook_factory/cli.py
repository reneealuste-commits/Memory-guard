from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from ebook_factory import __version__
from ebook_factory.factory import build_batch, build_from_manifest
from ebook_factory.templates import scaffold_book

app = typer.Typer(
    name="ebook-factory",
    help="Turn Markdown manuscripts into production-ready EPUB ebooks.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def init(
    path: Path = typer.Argument(Path("my-book"), help="Directory for the new book project"),
) -> None:
    """Scaffold a new book with book.yaml and sample chapters."""
    try:
        root = scaffold_book(path)
    except FileExistsError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"[green]Created book project at[/green] {root}")
    console.print("  • book.yaml")
    console.print("  • chapters/*.md")
    console.print("\nNext: [bold]ebook-factory build[/bold] " + str(path))


@app.command()
def build(
    source: Path = typer.Argument(
        Path("."),
        help="Path to book.yaml or directory containing it",
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output EPUB path (default: <book>/dist/<title>.epub)",
    ),
) -> None:
    """Build one EPUB from a book manifest."""
    source = source.resolve()
    manifest = source / "book.yaml" if source.is_dir() else source
    if not manifest.is_file():
        console.print(f"[red]No book.yaml at[/red] {manifest}")
        raise typer.Exit(1)

    try:
        result = build_from_manifest(manifest, output)
    except (ValueError, FileNotFoundError) as exc:
        console.print(f"[red]Build failed:[/red] {exc}")
        raise typer.Exit(1) from exc

    console.print(f"[green]Built[/green] {result}")


@app.command("batch")
def batch_build(
    books_dir: Path = typer.Argument(Path("books"), help="Root directory to scan for book.yaml"),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output directory for all EPUBs",
    ),
) -> None:
    """Build every book.yaml found under a directory tree."""
    try:
        results = build_batch(books_dir, output)
    except FileNotFoundError as exc:
        console.print(f"[red]{exc}[/red]")
        raise typer.Exit(1) from exc

    table = Table(title="Batch build complete")
    table.add_column("EPUB", style="cyan")
    for path in results:
        table.add_row(str(path))
    console.print(table)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(False, "--version", "-V", help="Show version and exit"),
) -> None:
    if version:
        console.print(f"ebook-factory {__version__}")
        raise typer.Exit()


if __name__ == "__main__":
    app()
