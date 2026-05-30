from pathlib import Path

from ebook_factory.builder import build_epub
from ebook_factory.manifest import load_manifest


def test_build_epub(tmp_path: Path) -> None:
    chapters = tmp_path / "chapters"
    chapters.mkdir()
    (chapters / "intro.md").write_text("# Intro\n\nParagraph one.", encoding="utf-8")
    (tmp_path / "book.yaml").write_text(
        """
title: Built Book
author: Factory Bot
description: A test manuscript.
chapters:
  - chapters/intro.md
""",
        encoding="utf-8",
    )
    manifest = load_manifest(tmp_path / "book.yaml")
    out = tmp_path / "out.epub"
    result = build_epub(manifest, out)
    assert result == out
    assert out.is_file()
    assert out.stat().st_size > 1000


def test_build_epub_with_string_chapters(tmp_path: Path) -> None:
    (tmp_path / "ch.md").write_text("# Chapter\n\nBody.", encoding="utf-8")
    (tmp_path / "book.yaml").write_text(
        "title: S\nauthor: A\nchapters:\n  - ch.md\n",
        encoding="utf-8",
    )
    manifest = load_manifest(tmp_path / "book.yaml")
    assert manifest.chapters[0].title == "Ch"
