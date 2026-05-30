#!/usr/bin/env python3
"""Build all formats for Book 6."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    steps = [
        [sys.executable, str(ROOT / "builders" / "export_for_docx.py")],
        [sys.executable, str(ROOT / "builders" / "build_pdf.py")],
        [sys.executable, str(ROOT / "builders" / "build_epub.py")],
        ["node", str(ROOT / "builders" / "build_docx.js")],
    ]
    for cmd in steps:
        print(">>", " ".join(cmd))
        subprocess.run(cmd, check=True, cwd=str(ROOT))

    # Page count for wrap
    from pypdf import PdfReader

    sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))
    import meta

    pdf = ROOT / "outputs" / f"{meta.OUTPUT_BASENAME}_interior.pdf"
    pages = len(PdfReader(str(pdf)).pages)
    cover = ROOT / "outputs" / f"{meta.OUTPUT_BASENAME}_kindle_cover.jpg"
    if cover.exists():
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "builders" / "build_wrap.py"),
                "--cover",
                str(cover),
                "--pages",
                str(pages),
            ],
            check=True,
            cwd=str(ROOT),
        )
    else:
        print(f"Cover not found at {cover}; skip wrap")

    print(f"All builds complete. Interior: {pages} pages.")


if __name__ == "__main__":
    main()
