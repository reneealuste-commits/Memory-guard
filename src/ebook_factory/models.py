from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Chapter:
    """A single chapter sourced from a Markdown file."""

    title: str
    source: Path
    order: int = 0


@dataclass
class BookManifest:
    """Book metadata and chapter list loaded from book.yaml."""

    title: str
    author: str
    language: str = "en"
    identifier: str | None = None
    description: str = ""
    publisher: str = "Ebook Factory"
    series: str = ""
    series_index: int | None = None
    chapters: list[Chapter] = field(default_factory=list)
    cover: Path | None = None
    css: Path | None = None

    @property
    def uid(self) -> str:
        return self.identifier or f"urn:ebook-factory:{self.title.lower().replace(' ', '-')}"
