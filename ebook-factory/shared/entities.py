"""HTML entity handling for multi-format book builds."""

from __future__ import annotations

import re

ENTITY_MAP = {
    "&mdash;": "\u2014",
    "&ndash;": "\u2013",
    "&rsquo;": "\u2019",
    "&lsquo;": "\u2018",
    "&rdquo;": "\u201d",
    "&ldquo;": "\u201c",
    "&middot;": "\u00b7",
    "&hellip;": "\u2026",
    "&nbsp;": "\u00a0",
    "&amp;": "&",
}

TAG_PATTERN = re.compile(r"</?(?:em|strong)>")


def entities_to_unicode(text: str) -> str:
    """Replace named HTML entities with literal Unicode."""
    result = text
    for entity, char in ENTITY_MAP.items():
        result = result.replace(entity, char)
    return result


def strip_inline_tags(text: str) -> str:
    """Remove simple <em>/<strong> tags for plain-text contexts."""
    return TAG_PATTERN.sub("", text)


def plain_text(text: str) -> str:
    """Entities to Unicode, tags stripped."""
    return strip_inline_tags(entities_to_unicode(text))


def escape_xml(text: str) -> str:
    """Escape text for XHTML after entity conversion."""
    t = entities_to_unicode(text)
    t = strip_inline_tags(t)
    return (
        t.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
