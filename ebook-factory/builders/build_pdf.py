#!/usr/bin/env python3
"""ReportLab PDF builder for Honest Father Series books."""

from __future__ import annotations

import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch as INCH
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "books" / "book06_strong_son"))

import meta  # noqa: E402
from content import CHAPTERS  # noqa: E402
from shared.constants import (  # noqa: E402
    ACCENT_RGB,
    PDF_BODY_FONT,
    PDF_BODY_LEADING,
    PDF_BODY_SIZE,
    PDF_HEADING_FONT,
    PDF_MARGIN_BOTTOM,
    PDF_MARGIN_LEFT,
    PDF_MARGIN_RIGHT,
    PDF_MARGIN_TOP,
    PDF_TRIM,
)
from shared.entities import entities_to_unicode  # noqa: E402


def _p(text: str) -> str:
    """Convert entity markup to ReportLab-friendly XML."""
    t = entities_to_unicode(text)
    t = t.replace("&", "&amp;")
    t = t.replace("<em>", "<i>").replace("</em>", "</i>")
    t = t.replace("<strong>", "<b>").replace("</strong>", "</b>")
    return t


def build_styles():
    styles = getSampleStyleSheet()
    gold = colors.Color(*ACCENT_RGB)
    body = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName=PDF_BODY_FONT,
        fontSize=PDF_BODY_SIZE,
        leading=PDF_BODY_LEADING,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
    )
    title = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontName=PDF_HEADING_FONT,
        fontSize=22,
        leading=26,
        alignment=TA_CENTER,
        textColor=gold,
        spaceAfter=6,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName=PDF_BODY_FONT,
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=24,
    )
    part = ParagraphStyle(
        "Part",
        parent=styles["Heading2"],
        fontName=PDF_HEADING_FONT,
        fontSize=14,
        leading=18,
        alignment=TA_CENTER,
        textColor=gold,
        spaceBefore=18,
        spaceAfter=12,
    )
    ch_num = ParagraphStyle(
        "ChNum",
        fontName=PDF_HEADING_FONT,
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=gold,
        spaceBefore=12,
        spaceAfter=2,
    )
    ch_title = ParagraphStyle(
        "ChTitle",
        fontName=PDF_HEADING_FONT,
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
    center = ParagraphStyle(
        "Center",
        parent=body,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )
    code_label = ParagraphStyle(
        "CodeLabel",
        parent=styles["Heading2"],
        fontName=PDF_HEADING_FONT,
        fontSize=13,
        leading=17,
        alignment=TA_CENTER,
        textColor=gold,
        spaceBefore=12,
        spaceAfter=10,
    )
    code_rule = ParagraphStyle(
        "CodeRule",
        parent=body,
        fontName=PDF_BODY_FONT,
        fontSize=10.5,
        leading=14.5,
        leftIndent=24,
        rightIndent=24,
        fontStyle="Italic",
        spaceAfter=6,
    )
    return {
        "body": body,
        "title": title,
        "subtitle": subtitle,
        "part": part,
        "ch_num": ch_num,
        "ch_title": ch_title,
        "center": center,
        "code_label": code_label,
        "code_rule": code_rule,
    }


def add_front_matter(story, st):
    story.append(Spacer(1, 1.5 * INCH))
    story.append(Paragraph(_p(meta.TITLE), st["title"]))
    story.append(Paragraph(_p(meta.SUBTITLE), st["subtitle"]))
    story.append(Spacer(1, 0.5 * INCH))
    story.append(Paragraph(_p(meta.SERIES), st["center"]))
    story.append(PageBreak())

    story.append(Spacer(1, 0.5 * INCH))
    story.append(Paragraph("Copyright", st["ch_title"]))
    story.append(
        Paragraph(
            _p(
                f"Copyright &copy; {meta.YEAR} {meta.COPYRIGHT_HOLDER}, writing as {meta.PEN_NAME}. "
                "All rights reserved."
            ),
            st["body"],
        )
    )
    story.append(PageBreak())

    story.append(Spacer(1, 2 * INCH))
    story.append(Paragraph("Dedication", st["ch_title"]))
    story.append(Paragraph(_p(meta.DEDICATION), st["body"]))
    story.append(PageBreak())

    story.append(Paragraph("Before You Read", st["ch_title"]))
    for para in meta.NOTE_BEFORE:
        story.append(Paragraph(_p(para), st["body"]))
    story.append(PageBreak())

    story.append(Paragraph(_p(meta.CODE_NAME.replace("&rsquo;", "'")), st["code_label"]))
    for i, rule in enumerate(meta.CODE_RULES, 1):
        story.append(Paragraph(_p(f"{i}. {rule}"), st["code_rule"]))
    story.append(PageBreak())


def add_chapters(story, st):
    part_idx = 0
    for ch_num in range(1, 15):
        part_num = (ch_num - 1) // 4 + 1
        if part_num != part_idx:
            part_idx = part_num
            part = meta.PARTS[part_num - 1]
            story.append(Paragraph(_p(part["title"]), st["part"]))
            story.append(Spacer(1, 6))

        story.append(Paragraph(f"CHAPTER {ch_num}", st["ch_num"]))
        story.append(Paragraph(_p(meta.CHAPTER_TITLES[ch_num - 1]), st["ch_title"]))
        # accent rule simulated via spacer + thin line would need canvas; skip for flow

        for block in CHAPTERS[ch_num]:
            if block == "SECTION_BREAK":
                story.append(Spacer(1, 6))
                story.append(Paragraph("* * *", st["center"]))
                story.append(Spacer(1, 6))
            else:
                story.append(Paragraph(_p(block), st["body"]))
        story.append(PageBreak())


def add_back_matter(story, st):
    story.append(Paragraph("A Final Word", st["ch_title"]))
    for para in meta.CLOSING_LETTER:
        story.append(Paragraph(_p(para), st["body"]))
    story.append(PageBreak())

    story.append(Paragraph(_p(meta.CODE_NAME.replace("&rsquo;", "'")), st["code_label"]))
    for i, rule in enumerate(meta.CODE_RULES, 1):
        story.append(Paragraph(_p(f"{i}. {rule}"), st["code_rule"]))
    story.append(PageBreak())

    story.append(Paragraph("Sources", st["ch_title"]))
    for src in meta.SOURCES:
        story.append(Paragraph(_p(src), st["body"]))
    story.append(PageBreak())

    story.append(Paragraph("About the Author", st["ch_title"]))
    for para in meta.ABOUT_AUTHOR:
        story.append(Paragraph(_p(para), st["body"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Books in This Series", st["ch_title"]))
    for title, sub in meta.SERIES_LIST:
        story.append(Paragraph(_p(f"<i>{title}</i> &mdash; {sub}"), st["body"]))


def build_pdf(output_path: Path) -> int:
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=PDF_TRIM,
        leftMargin=PDF_MARGIN_LEFT,
        rightMargin=PDF_MARGIN_RIGHT,
        topMargin=PDF_MARGIN_TOP,
        bottomMargin=PDF_MARGIN_BOTTOM,
        title=meta.TITLE,
        author=meta.AUTHOR,
    )
    st = build_styles()
    story = []
    add_front_matter(story, st)
    add_chapters(story, st)
    add_back_matter(story, st)
    doc.build(story)
    from pypdf import PdfReader

    return len(PdfReader(str(output_path)).pages)


if __name__ == "__main__":
    out = ROOT / "outputs" / f"{meta.OUTPUT_BASENAME}_interior.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    pages = build_pdf(out)
    print(f"Wrote {out} ({pages} pages)")
