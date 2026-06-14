"""Chapter content registry for The Unplugged Al series."""

from __future__ import annotations

from scripts.content.book_01_02 import CHAPTERS as CHAPTERS_01_02
from scripts.content.book_03_04 import CHAPTERS as CHAPTERS_03_04
from scripts.content.book_05_06 import CHAPTERS as CHAPTERS_05_06

ALL_CHAPTERS = {**CHAPTERS_01_02, **CHAPTERS_03_04, **CHAPTERS_05_06}


def get_chapter_content(
    book_slug: str,
    chapter_slug: str,
    title: str,
    index: int,
    book: dict,
) -> str:
    key = (book_slug, chapter_slug)
    if key in ALL_CHAPTERS:
        return ALL_CHAPTERS[key]

    return f"""# {title}

*Book {book_slug} — Chapter {index}*

{book['purpose']}

This chapter is part of **{book['title']}** in *The Unplugged Al* series.
"""


def chapter_count() -> int:
    return len(ALL_CHAPTERS)
