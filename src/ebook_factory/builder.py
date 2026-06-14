from __future__ import annotations

from datetime import datetime
from importlib import resources
from pathlib import Path

from ebooklib import epub
from jinja2 import Template

from ebook_factory.markdown import render_chapter
from ebook_factory.models import BookManifest, Chapter

_TITLE_PAGE = Template(
    """<div class="title-page">
  {% if series %}<p class="series-label">{{ series }}</p>{% endif %}
  {% if series_index %}<p class="book-number">Book {{ series_index }}</p>{% endif %}
  <h1>{{ title }}</h1>
  <div class="title-rule"></div>
  {% if description %}<p class="subtitle">{{ description }}</p>{% endif %}
  <p class="author">{{ author }}</p>
</div>"""
)

_COPYRIGHT_PAGE = Template(
    """<div class="copyright-page">
  <h1>{{ title }}</h1>
  <p>Copyright &copy; {{ year }} {{ author }}. All rights reserved.</p>
  <p>No part of this publication may be reproduced, distributed, or transmitted in any form
  or by any means without the prior written permission of the publisher,
  except for brief quotations in reviews and certain noncommercial uses permitted by law.</p>
  <p>This book is intended for educational and personal development purposes.
  It is not a substitute for professional legal, financial, medical, or therapeutic advice.</p>
  {% if series %}<p>Part of the <em>{{ series }}</em> series{% if series_index %} — Book {{ series_index }}{% endif %}.</p>{% endif %}
  <p>Published by {{ publisher }}</p>
</div>"""
)

_CHAPTER_WRAP = Template(
    """<html xmlns="http://www.w3.org/1999/xhtml">
<head><title>{{ title }}</title></head>
<body>
  <div class="chapter-body">
    {% if series_index %}<p class="chapter-opener">Book {{ series_index }} &middot; Chapter {{ chapter_num }}</p>{% endif %}
    <h1>{{ title }}</h1>
    {{ body | safe }}
  </div>
</body>
</html>"""
)

_TOC_PAGE = Template(
    """<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head><title>Table of Contents</title></head>
<body>
  <nav epub:type="toc" id="toc" class="toc-page" role="doc-toc">
    <h1>Table of Contents</h1>
    <ol>
      {% for chapter in chapters %}
      <li><a href="{{ chapter.href }}">{{ chapter.title }}</a></li>
      {% endfor %}
    </ol>
  </nav>
</body>
</html>"""
)


def build_epub(manifest: BookManifest, output: Path) -> Path:
    """Assemble an EPUB from a book manifest and write to output."""
    _validate_sources(manifest)

    book = epub.EpubBook()
    book.set_identifier(manifest.uid)
    book.set_title(manifest.title)
    book.set_language(manifest.language)
    book.add_author(manifest.author)

    default_css = _load_default_css()
    nav_css = epub.EpubItem(
        uid="style_default",
        file_name="style/default.css",
        media_type="text/css",
        content=default_css.encode("utf-8"),
    )
    book.add_item(nav_css)

    if manifest.css and manifest.css.is_file():
        custom = manifest.css.read_bytes()
        custom_item = epub.EpubItem(
            uid="style_custom",
            file_name="style/custom.css",
            media_type="text/css",
            content=custom,
        )
        book.add_item(custom_item)
        style_paths = ["style/default.css", "style/custom.css"]
    else:
        style_paths = ["style/default.css"]

    spine: list[epub.EpubItem] = []
    toc: list[epub.Link] = []
    chapter_entries: list[tuple[str, str]] = []

    if manifest.cover and manifest.cover.is_file():
        _add_cover(book, manifest.cover)

    title_page = epub.EpubHtml(
        title="Title",
        file_name="title.xhtml",
        lang=manifest.language,
    )
    title_page.content = _TITLE_PAGE.render(
        title=manifest.title,
        author=manifest.author,
        description=manifest.description,
        series=manifest.series,
        series_index=manifest.series_index,
    )
    title_page.add_item(nav_css)
    book.add_item(title_page)
    spine.append(title_page)

    copyright_page = epub.EpubHtml(
        title="Copyright",
        file_name="copyright.xhtml",
        lang=manifest.language,
    )
    copyright_page.content = _COPYRIGHT_PAGE.render(
        title=manifest.title,
        author=manifest.author,
        publisher=manifest.publisher,
        series=manifest.series,
        series_index=manifest.series_index,
        year=datetime.now().year,
    )
    copyright_page.add_link(href=style_paths[0], rel="stylesheet", type="text/css")
    book.add_item(copyright_page)
    spine.append(copyright_page)

    for chapter in sorted(manifest.chapters, key=lambda c: c.order):
        item = _chapter_to_epub(
            chapter,
            manifest.language,
            style_paths,
            series_index=manifest.series_index,
        )
        for css_path in style_paths:
            css_item = next(
                (i for i in book.get_items() if getattr(i, "file_name", None) == css_path),
                nav_css,
            )
            item.add_item(css_item)
        book.add_item(item)
        spine.append(item)
        toc.append(epub.Link(item.file_name, chapter.title, item.id))
        chapter_entries.append((chapter.title, item.file_name))

    toc_page = _create_toc_page(manifest, chapter_entries, style_paths)
    book.add_item(toc_page)
    spine.insert(1, toc_page)

    book.toc = tuple(toc)
    book.guide = [
        {"type": "toc", "title": "Table of Contents", "item": toc_page},
    ]
    book.spine = ["nav", *spine]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    output.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(output), book)
    return output


def _validate_sources(manifest: BookManifest) -> None:
    if not manifest.chapters:
        raise ValueError("Book has no chapters")
    for ch in manifest.chapters:
        if not ch.source.is_file():
            raise FileNotFoundError(f"Chapter not found: {ch.source}")


def _create_toc_page(
    manifest: BookManifest,
    chapter_entries: list[tuple[str, str]],
    style_paths: list[str],
) -> epub.EpubHtml:
    """Build a reader-visible HTML table of contents for KDP front matter."""
    toc_page = epub.EpubHtml(
        title="Table of Contents",
        file_name="toc.xhtml",
        lang=manifest.language,
    )
    toc_page.content = _TOC_PAGE.render(
        chapters=[{"title": title, "href": href} for title, href in chapter_entries],
    )
    toc_page.add_link(href=style_paths[0], rel="stylesheet", type="text/css")
    if len(style_paths) > 1:
        toc_page.add_link(href=style_paths[1], rel="stylesheet", type="text/css")
    return toc_page


def _chapter_to_epub(
    chapter: Chapter,
    language: str,
    style_paths: list[str],
    series_index: int | None = None,
) -> epub.EpubHtml:
    html_body, _ = render_chapter(chapter)
    slug = _slugify(chapter.title)
    item = epub.EpubHtml(
        title=chapter.title,
        file_name=f"chapters/{chapter.order:02d}-{slug}.xhtml",
        lang=language,
    )
    item.content = _CHAPTER_WRAP.render(
        title=chapter.title,
        body=html_body,
        series_index=series_index,
        chapter_num=chapter.order + 1,
    )
    item.add_link(href=style_paths[0], rel="stylesheet", type="text/css")
    if len(style_paths) > 1:
        item.add_link(href=style_paths[1], rel="stylesheet", type="text/css")
    return item


def _add_cover(book: epub.EpubBook, cover_path: Path) -> None:
    suffix = cover_path.suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png", ".gif"}:
        return
    book.set_cover(f"cover{suffix}", cover_path.read_bytes())


def _load_default_css() -> str:
    return resources.files("ebook_factory.styles").joinpath("default.css").read_text(encoding="utf-8")


def _slugify(text: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in text.lower()).strip("-")[:48]
