"""Text utilities shared across builders."""

from __future__ import annotations

from PIL import ImageDraw, ImageFont

from shared.entities import plain_text


def word_count_in_blocks(blocks: list) -> int:
    total = 0
    for block in blocks:
        if isinstance(block, str) and block != "SECTION_BREAK":
            total += len(plain_text(block).split())
        elif isinstance(block, dict) and block.get("type") == "paragraph":
            total += len(plain_text(block["text"]).split())
    return total


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text for PIL back-cover layout."""
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        test = f"{current} {word}"
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            lines.append(current)
            current = word
    lines.append(current)
    return lines
