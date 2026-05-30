from pathlib import Path

from ebook_factory.factory import build_batch, build_from_manifest
from ebook_factory.templates import scaffold_book


def test_scaffold_and_build(tmp_path: Path) -> None:
    book_dir = tmp_path / "demo"
    scaffold_book(book_dir)
    result = build_from_manifest(book_dir / "book.yaml")
    assert result.suffix == ".epub"
    assert result.is_file()


def test_batch_build(tmp_path: Path) -> None:
    for name in ("alpha", "beta"):
        root = tmp_path / "books" / name
        scaffold_book(root)
    built = build_batch(tmp_path / "books")
    assert len(built) == 2
    assert all(p.suffix == ".epub" for p in built)
