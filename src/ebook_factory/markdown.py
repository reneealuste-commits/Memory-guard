from __future__ import annotations

import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc

from ebook_factory.models import Chapter


def render_chapter(chapter: Chapter) -> tuple[str, str]:
    """Return (html_body, plain_text_excerpt) for a chapter."""
    text = chapter.source.read_text(encoding="utf-8")
    html = markdown.markdown(
        text,
        extensions=[
            "meta",
            fenced_code.FencedCodeExtension(),
            tables.TableExtension(),
            toc.TocExtension(permalink=False),
            codehilite.CodeHiliteExtension(css_class="highlight"),
        ],
    )
    excerpt = _plain_excerpt(text)
    return html, excerpt


def _plain_excerpt(text: str, max_len: int = 500) -> str:
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]
    body = " ".join(lines)
    if len(body) <= max_len:
        return body
    return body[: max_len - 3].rsplit(" ", 1)[0] + "..."
