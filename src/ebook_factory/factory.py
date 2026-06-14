from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ebook_factory.builder import build_epub
from ebook_factory.manifest import load_manifest

console = Console()


def build_from_manifest(manifest_path: Path, output: Path | None = None) -> Path:
    """Build a single EPUB from a book.yaml manifest."""
    manifest_path = manifest_path.resolve()
    manifest = load_manifest(manifest_path)
    out = output or (manifest_path.parent / "dist" / f"{_safe_filename(manifest.title)}.epub")
    out = out.resolve()
    return build_epub(manifest, out)


def build_batch(books_dir: Path, output_dir: Path | None = None) -> list[Path]:
    """Find every book.yaml under books_dir and build all matching EPUBs."""
    books_dir = books_dir.resolve()
    out_root = (output_dir or books_dir / "dist").resolve()
    manifests = sorted(books_dir.rglob("book.yaml"))

    if not manifests:
        raise FileNotFoundError(f"No book.yaml found under {books_dir}")

    built: list[Path] = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for manifest_path in manifests:
            rel = manifest_path.parent.relative_to(books_dir)
            task = progress.add_task(f"Building {rel}…", total=None)
            manifest = load_manifest(manifest_path)
            out = out_root / rel / f"{_safe_filename(manifest.title)}.epub"
            build_epub(manifest, out)
            built.append(out)
            progress.update(task, description=f"[green]✓[/green] {rel}")

    return built


def _safe_filename(title: str) -> str:
    return "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip().replace(" ", "-")
