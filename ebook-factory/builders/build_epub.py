#!/usr/bin/env python3
"""Manual ZIP EPUB builder — no named HTML entities in XHTML."""

from __future__ import annotations

import html
import sys
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))

import meta  # noqa: E402
from content import CHAPTERS  # noqa: E402
from shared.constants import EPUB_UUID  # noqa: E402
from shared.entities import entities_to_unicode, escape_xml  # noqa: E402


def inline_markup(text: str) -> str:
    t = entities_to_unicode(text)
    t = t.replace("<em>", "<em>").replace("</em>", "</em>")
    t = t.replace("<strong>", "<strong>").replace("</strong>", "</strong>")
    # escape bare ampersands not part of tags
    parts = []
    i = 0
    while i < len(t):
        if t[i] == "<":
            end = t.find(">", i)
            parts.append(t[i : end + 1])
            i = end + 1
        else:
            j = i
            while j < len(t) and t[j] != "<":
                j += 1
            parts.append(html.escape(t[i:j]))
            i = j
    return "".join(parts)


def xhtml_doc(title: str, body_html: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
<title>{escape_xml(title)}</title>
<link rel="stylesheet" type="text/css" href="styles.css"/>
</head>
<body>
{body_html}
</body>
</html>
"""


def build_styles() -> str:
    return """body { font-family: Georgia, serif; line-height: 1.5; margin: 1em; }
h1 { color: #A8741A; text-align: center; }
h2 { text-align: center; }
.part { text-align: center; color: #A8741A; font-weight: bold; margin-top: 2em; }
.chapter-num { text-align: center; color: #A8741A; font-size: 0.85em; letter-spacing: 0.1em; }
.section-break { text-align: center; color: #888; margin: 1.5em 0; }
.code-rule { font-style: italic; margin-left: 1.5em; }
"""


def chapter_body(ch_num: int) -> str:
    parts = [
        f'<p class="chapter-num">CHAPTER {ch_num}</p>',
        f"<h1>{inline_markup(meta.CHAPTER_TITLES[ch_num - 1])}</h1>",
    ]
    for block in CHAPTERS[ch_num]:
        if block == "SECTION_BREAK":
            parts.append('<p class="section-break">* * *</p>')
        else:
            parts.append(f"<p>{inline_markup(block)}</p>")
    return "\n".join(parts)


def build_epub(output_path: Path) -> None:
    book_id = EPUB_UUID
    manifest_items = []
    spine_items = []
    nav_points = []
    toc_ol = []

    files: dict[str, str] = {}
    files["mimetype"] = "application/epub+zip"
    files["META-INF/container.xml"] = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>"""
    files["OEBPS/styles.css"] = build_styles()

    item_id = 0

    def add_item(href: str, content: str, media_type: str, spine: bool = True, title: str = ""):
        nonlocal item_id
        item_id += 1
        iid = f"item{item_id}"
        files[f"OEBPS/{href}"] = content
        manifest_items.append(
            f'<item id="{iid}" href="{href}" media-type="{media_type}"/>'
        )
        if spine:
            spine_items.append(f'<itemref idref="{iid}"/>')
        return iid, title

    add_item("styles.css", files["OEBPS/styles.css"], "text/css", spine=False)

    # Front matter
    front = [
        f"<h1>{inline_markup(meta.TITLE)}</h1>",
        f"<h2>{inline_markup(meta.SUBTITLE)}</h2>",
        f"<p style='text-align:center'>{inline_markup(meta.SERIES)}</p>",
    ]
    add_item("front.xhtml", xhtml_doc(meta.TITLE, "\n".join(front)), "application/xhtml+xml", title="Title Page")

    copy_body = (
        f"<p>Copyright © {meta.YEAR} {meta.COPYRIGHT_HOLDER}, writing as {meta.PEN_NAME}. "
        "All rights reserved.</p>"
    )
    add_item("copyright.xhtml", xhtml_doc("Copyright", copy_body), "application/xhtml+xml", title="Copyright")

    add_item(
        "dedication.xhtml",
        xhtml_doc("Dedication", f"<p>{inline_markup(meta.DEDICATION)}</p>"),
        "application/xhtml+xml",
        title="Dedication",
    )

    note_html = "".join(f"<p>{inline_markup(p)}</p>" for p in meta.NOTE_BEFORE)
    add_item("note.xhtml", xhtml_doc("Before You Read", note_html), "application/xhtml+xml", title="Before You Read")

    code_html = f"<h1>{inline_markup(meta.CODE_NAME)}</h1>"
    for i, rule in enumerate(meta.CODE_RULES, 1):
        code_html += f'<p class="code-rule">{i}. {inline_markup(rule)}</p>'
    add_item("code.xhtml", xhtml_doc("The Son's Code", code_html), "application/xhtml+xml", title="The Son's Code")

    part_nav = []
    current_part = 0
    for ch in range(1, 15):
        part_num = (ch - 1) // 4 + 1
        if part_num != current_part:
            current_part = part_num
            part = meta.PARTS[part_num - 1]
            part_nav.append({"part": part, "chapters": []})
        href = f"chapter_{ch:02d}.xhtml"
        ch_title = f"Chapter {ch}: {entities_to_unicode(meta.CHAPTER_TITLES[ch - 1])}"
        _, _ = add_item(href, xhtml_doc(ch_title, chapter_body(ch)), "application/xhtml+xml", title=ch_title)
        part_nav[-1]["chapters"].append((href, ch_title, ch))

    # Back matter
    closing = "".join(f"<p>{inline_markup(p)}</p>" for p in meta.CLOSING_LETTER)
    add_item("closing.xhtml", xhtml_doc("A Final Word", closing), "application/xhtml+xml", title="A Final Word")

    code_back = f"<h1>{inline_markup(meta.CODE_NAME)}</h1>"
    for i, rule in enumerate(meta.CODE_RULES, 1):
        code_back += f'<p class="code-rule">{i}. {inline_markup(rule)}</p>'
    add_item("code_summary.xhtml", xhtml_doc("Code Summary", code_back), "application/xhtml+xml", title="Code Summary")

    sources = "".join(f"<p>{inline_markup(s)}</p>" for s in meta.SOURCES)
    add_item("sources.xhtml", xhtml_doc("Sources", sources), "application/xhtml+xml", title="Sources")

    about = "".join(f"<p>{inline_markup(p)}</p>" for p in meta.ABOUT_AUTHOR)
    series = "".join(
        f"<p><em>{inline_markup(t)}</em> — {inline_markup(s)}</p>" for t, s in meta.SERIES_LIST
    )
    add_item(
        "about.xhtml",
        xhtml_doc("About", about + series),
        "application/xhtml+xml",
        title="About the Author",
    )

    # NCX
    play_order = 0
    ncx_nav = []
    nav_html_parts = ['<nav epub:type="toc" id="toc"><ol>']
    for pn, pdata in enumerate(part_nav, 1):
        play_order += 1
        part_label = entities_to_unicode(pdata["part"]["title"])
        ncx_nav.append(
            f'<navPoint id="navpart{pn}" playOrder="{play_order}">'
            f"<navLabel><text>{html.escape(part_label)}</text></navLabel>"
            f"<content src=\"chapter_{pdata['chapters'][0][2]:02d}.xhtml\"/>"
        )
        nav_html_parts.append(f"<li><span>{html.escape(part_label)}</span><ol>")
        for href, title, ch_num in pdata["chapters"]:
            play_order += 1
            ncx_nav.append(
                f'<navPoint id="navch{ch_num}" playOrder="{play_order}">'
                f"<navLabel><text>{html.escape(title)}</text></navLabel>"
                f'<content src="{href}"/>'
                "</navPoint>"
            )
            nav_html_parts.append(
                f'<li><a href="{href}">{html.escape(title)}</a></li>'
            )
        ncx_nav.append("</navPoint>")
        nav_html_parts.append("</ol></li>")
    nav_html_parts.append("</ol></nav>")

    ncx = f"""<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:uid" content="{book_id}"/>
<meta name="dtb:depth" content="2"/>
</head>
<docTitle><text>{html.escape(meta.TITLE)}</text></docTitle>
<navMap>
{''.join(ncx_nav)}
</navMap>
</ncx>"""
    add_item("toc.ncx", ncx, "application/x-dtbncx+xml", spine=False)

    nav_doc = xhtml_doc(
        "Navigation",
        "\n".join(nav_html_parts).replace('nav epub:type', 'nav epub:type'),
    )
    # fix nav namespace
    nav_doc = nav_doc.replace(
        "<html xmlns=",
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" ',
    ).replace('<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" "http://www.w3.org/1999/xhtml"',
              '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops"')
    add_item("nav.xhtml", nav_doc, "application/xhtml+xml", spine=False, title="Table of Contents")

    manifest_items.append('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>')

    opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookId">
<metadata xmlns:dc="http://purl.org/d/dc/elements/1.1/">
<dc:identifier id="BookId">{book_id}</dc:identifier>
<dc:title>{html.escape(meta.TITLE)}</dc:title>
<dc:creator>{html.escape(meta.AUTHOR)}</dc:creator>
<dc:language>en</dc:language>
<meta property="dcterms:modified">2026-05-30T00:00:00Z</meta>
</metadata>
<manifest>
{''.join(manifest_items)}
</manifest>
<spine toc="ncx">
{''.join(spine_items)}
</spine>
</package>"""
    files["OEBPS/content.opf"] = opf

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_path, "w") as zf:
        zf.writestr("mimetype", files["mimetype"], compress_type=zipfile.ZIP_STORED)
        for name, data in files.items():
            if name == "mimetype":
                continue
            zf.writestr(name, data, compress_type=zipfile.ZIP_DEFLATED)


if __name__ == "__main__":
    out = ROOT / "outputs" / f"{meta.OUTPUT_BASENAME}.epub"
    build_epub(out)
    print(f"Wrote {out}")
