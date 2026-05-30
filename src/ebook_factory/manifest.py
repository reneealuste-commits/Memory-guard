from __future__ import annotations

from pathlib import Path

import yaml

from ebook_factory.models import BookManifest, Chapter


def load_manifest(path: Path) -> BookManifest:
    """Load book.yaml and resolve chapter paths relative to the manifest directory."""
    root = path.parent.resolve()
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError(f"Invalid manifest: expected mapping in {path}")

    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        raise ValueError("Manifest must include 'title' and 'author'")

    chapters: list[Chapter] = []
    for idx, entry in enumerate(data.get("chapters") or []):
        if isinstance(entry, str):
            source = root / entry
            chapters.append(Chapter(title=_title_from_path(source), source=source, order=idx))
        elif isinstance(entry, dict):
            source = root / entry["file"]
            chapters.append(
                Chapter(
                    title=entry.get("title") or _title_from_path(source),
                    source=source,
                    order=idx,
                )
            )
        else:
            raise ValueError(f"Invalid chapter entry at index {idx}")

    cover = data.get("cover")
    css = data.get("css")

    return BookManifest(
        title=title,
        author=author,
        language=data.get("language", "en"),
        identifier=data.get("identifier"),
        description=data.get("description", ""),
        publisher=data.get("publisher", "Ebook Factory"),
        chapters=chapters,
        cover=root / cover if cover else None,
        css=root / css if css else None,
    )


def _title_from_path(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()
