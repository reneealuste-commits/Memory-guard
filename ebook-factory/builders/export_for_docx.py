#!/usr/bin/env python3
"""Export meta and chapters to JSON for docx-js builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))

import meta  # noqa: E402
from content import CHAPTERS  # noqa: E402
from shared.constants import (  # noqa: E402
    DOCX_HEIGHT,
    DOCX_MARGIN_BOTTOM,
    DOCX_MARGIN_LEFT,
    DOCX_MARGIN_RIGHT,
    DOCX_MARGIN_TOP,
    DOCX_WIDTH,
)

meta_export = {
    "TITLE": meta.TITLE,
    "SUBTITLE": meta.SUBTITLE,
    "AUTHOR": meta.AUTHOR,
    "SERIES": meta.SERIES,
    "YEAR": meta.YEAR,
    "COPYRIGHT_HOLDER": meta.COPYRIGHT_HOLDER,
    "PEN_NAME": meta.PEN_NAME,
    "CODE_NAME": meta.CODE_NAME,
    "CODE_RULES": meta.CODE_RULES,
    "PARTS": meta.PARTS,
    "CHAPTER_TITLES": meta.CHAPTER_TITLES,
    "DEDICATION": meta.DEDICATION,
    "NOTE_BEFORE": meta.NOTE_BEFORE,
    "CLOSING_LETTER": meta.CLOSING_LETTER,
    "ABOUT_AUTHOR": meta.ABOUT_AUTHOR,
    "SERIES_LIST": meta.SERIES_LIST,
    "SOURCES": meta.SOURCES,
    "OUTPUT_BASENAME": meta.OUTPUT_BASENAME,
    "DOCX_WIDTH": DOCX_WIDTH,
    "DOCX_HEIGHT": DOCX_HEIGHT,
    "DOCX_MARGIN_TOP": DOCX_MARGIN_TOP,
    "DOCX_MARGIN_BOTTOM": DOCX_MARGIN_BOTTOM,
    "DOCX_MARGIN_LEFT": DOCX_MARGIN_LEFT,
    "DOCX_MARGIN_RIGHT": DOCX_MARGIN_RIGHT,
}

book_dir = ROOT / "books" / "book06_strong_son"
(book_dir / "meta_export.json").write_text(json.dumps(meta_export, indent=2))
(book_dir / "chapters_export.json").write_text(json.dumps({str(k): v for k, v in CHAPTERS.items()}, indent=2))
print("Exported JSON for DOCX builder")
