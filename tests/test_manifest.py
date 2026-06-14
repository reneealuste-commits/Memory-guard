from pathlib import Path

import pytest

from ebook_factory.manifest import load_manifest


def test_load_manifest(tmp_path: Path) -> None:
    (tmp_path / "chapters").mkdir()
    (tmp_path / "chapters" / "one.md").write_text("# One\n\nHello.", encoding="utf-8")
    (tmp_path / "book.yaml").write_text(
        """
title: Test Book
author: Test Author
chapters:
  - title: First
    file: chapters/one.md
""",
        encoding="utf-8",
    )
    manifest = load_manifest(tmp_path / "book.yaml")
    assert manifest.title == "Test Book"
    assert len(manifest.chapters) == 1
    assert manifest.chapters[0].title == "First"


def test_manifest_requires_title_and_author(tmp_path: Path) -> None:
    (tmp_path / "book.yaml").write_text("title: Only Title\n", encoding="utf-8")
    with pytest.raises(ValueError, match="author"):
        load_manifest(tmp_path / "book.yaml")
