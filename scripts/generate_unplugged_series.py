#!/usr/bin/env python3
"""Generate The Unplugged Al ebook series manuscripts."""

from __future__ import annotations

import sys
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
if str(WORKSPACE) not in sys.path:
    sys.path.insert(0, str(WORKSPACE))

SERIES_ROOT = WORKSPACE / "books" / "the-unplugged-al"

SERIES_META = {
    "series_title": "The Unplugged Man",
    "series_subtitle": (
        "Straight talk for men who are tired of bleeding in relationships "
        "and ready to lead their own life."
    ),
    "author": "The Unplugged Al",
    "publisher": "The Unplugged Al",
}

BOOKS = [
    {
        "slug": "01-frame-first",
        "index": 1,
        "title": "Frame First",
        "subtitle": (
            "How to hold your ground when she tests you, gets emotional, "
            "or tries to pull you off mission."
        ),
        "purpose": (
            "Teach men the single most important skill they lack — emotional control "
            "and leadership under pressure. This is the foundation everything else rests on."
        ),
        "chapters": [
            ("charm-is-theater", "Charm Is Theater — What Actually Matters After the First Few Weeks"),
            ("why-she-tests-you", "Why She Tests You (And Why Most Men Fail)"),
            ("real-meaning-of-frame", "The Real Meaning of Frame (It's Not What You Think)"),
            ("stay-calm-when-emotional", "How to Stay Calm When She Gets Emotional"),
            ("when-you-lose-frame", "What Happens When You Lose Frame (And How to Get It Back)"),
            ("the-no-test", "The \"No\" Test — The Cleanest Way to See Who She Really Is"),
            ("frame-when-angry-sad-distant", "Maintaining Frame When She's Angry, Sad, or Distant"),
            ("frame-in-everyday-life", "Frame in Everyday Life (Not Just When She's Testing You)"),
            ("price-of-losing-frame", "The Price of Losing Frame Over and Over"),
            ("frame-first-mans-code", "The Frame First Man's Code (10 Rules)"),
        ],
    },
    {
        "slug": "02-vetting-her",
        "index": 2,
        "title": "Vetting Her",
        "subtitle": (
            "How to see who she really is before you give her your time, heart, or resources."
        ),
        "purpose": (
            "Give men a practical, no-BS system to evaluate women instead of falling "
            "for charm, chemistry, or potential."
        ),
        "chapters": [
            ("three-types-of-women", "The Three Types of Women (And How They Actually Treat You)"),
            ("red-flags-early", "Red Flags That Show Up Early (But Most Men Ignore)"),
            ("green-flags-that-matter", "Green Flags That Actually Mean Something"),
            ("shes-different-lie", "Why \"She's Different\" Is Usually a Lie You Tell Yourself"),
            ("how-she-handles-no", "How She Handles \"No\" — The Most Important Test"),
            ("unhappy-unlucky-woman", "The Unhappy & Unlucky Woman (The One Who Will Drag You Down)"),
            ("single-mothers-hidden-costs", "Single Mothers — The Hidden Costs Most Men Don't Calculate"),
            ("how-she-treats-others", "How She Treats People Who Can't Do Anything for Her"),
            ("watching-over-time", "Watching Her Over Time (Not Just the First 90 Days)"),
            ("vetting-mans-code", "The Vetting Man's Code (10 Rules)"),
        ],
    },
    {
        "slug": "03-stop-simping",
        "index": 3,
        "title": "Stop Simping",
        "subtitle": (
            "Why you keep over-investing, pedestalizing, and choosing the same pain — "
            "and how to finally stop."
        ),
        "purpose": (
            "Address the root cause of most men's suffering in relationships: low self-respect "
            "and the habit of making women the center of their emotional world."
        ),
        "chapters": [
            ("what-simping-looks-like", "What Simping Actually Looks Like (It's Not Just Buying Gifts)"),
            ("why-you-started", "Why You Started Doing It (The Real Reason, Not the Story You Tell Yourself)"),
            ("cost-of-over-investing", "The Hidden Cost of Over-Investing Early"),
            ("are-you-simping-now", "How to Tell If You're Simping Right Now"),
            ("stop-making-her-purpose", "Stop Making Her Your Purpose"),
            ("nice-vs-weak", "The Difference Between Being Nice and Being Weak"),
            ("pull-energy-back", "How to Pull Your Energy Back Without Becoming Cold"),
            ("rebuilding-self-respect", "Rebuilding Your Self-Respect After Years of Simping"),
            ("what-happens-when-you-stop", "What Happens When You Finally Stop"),
            ("stop-simping-mans-code", "The Stop Simping Man's Code (10 Rules)"),
        ],
    },
    {
        "slug": "04-male-space",
        "index": 4,
        "title": "Male Space",
        "subtitle": "Why you need other men and a mission bigger than any woman.",
        "purpose": (
            "Teach men that putting all their emotional weight on one woman is a recipe "
            "for weakness and resentment — and how to build real male friendships and purpose instead."
        ),
        "chapters": [
            ("modern-mans-mistake", "The Modern Man's Biggest Mistake (Making Her Your Only Source)"),
            ("why-male-space-matters", "Why Male Space Matters More Than You Think"),
            ("real-male-friendships", "How to Build Real Male Friendships (Most Men Don't Know How)"),
            ("mission-first", "Mission First — What It Actually Means"),
            ("when-she-fights-purpose", "When a Woman Fights Your Purpose (The Real Test)"),
            ("support-vs-control", "The Difference Between Support and Control"),
            ("time-with-men-without-guilt", "How to Spend Time With Men Without Feeling Guilty"),
            ("protecting-energy-schedule", "Protecting Your Energy and Schedule"),
            ("nothing-but-her", "The Man Who Has Nothing But Her Usually Loses Her"),
            ("male-space-mans-code", "The Male Space Man's Code (10 Rules)"),
        ],
    },
    {
        "slug": "05-money-and-women",
        "index": 5,
        "title": "Money & Women",
        "subtitle": "How to protect your resources without becoming stingy or paranoid.",
        "purpose": (
            "Help men stop getting used financially while still being generous with the right woman. "
            "This is one of the biggest blind spots for men who grew up without strong male guidance."
        ),
        "chapters": [
            ("entitlement-trap", "The Entitlement Trap (Why Many Women Feel Your Money Is Theirs)"),
            ("provider-first-signs", "Early Signs She Sees You as a Provider First"),
            ("financial-frame", "How to Maintain Financial Frame Without Being Cheap"),
            ("generosity-vs-used", "The Difference Between Generosity and Being Used"),
            ("prenups-and-hard-talks", "Prenups, Assets, and Hard Conversations Most Men Avoid"),
            ("lose-financial-frame", "What Happens When You Lose Financial Frame"),
            ("building-wealth-open", "Building Wealth While Staying Open to the Right Woman"),
            ("successful-men-get-played", "How Successful Men Get Played (And How to Avoid It)"),
            ("no-to-money-test", "The Real Test: How She Reacts When You Say No to Money"),
            ("money-women-mans-code", "The Money & Women Man's Code (10 Rules)"),
        ],
    },
    {
        "slug": "06-the-unplugged-mans-code",
        "index": 6,
        "title": "The Unplugged Man's Code",
        "subtitle": "The final principles for self-respect, strong relationships, and peace.",
        "purpose": (
            "The capstone book. A clear, practical code that ties everything together so a man "
            "can live with clarity instead of repeating old patterns."
        ),
        "chapters": [
            ("not-broken-no-map", "You Are Not Broken — You Just Never Had the Map"),
            ("eighty-twenty-reality", "The 80/20 Reality (Stop Complaining, Start Improving)"),
            ("time-to-walk-away", "How to Know When It's Time to Walk Away"),
            ("recover-after-used", "How to Recover After You've Been Used or Heartbroken"),
            ("life-that-doesnt-collapse", "Building a Life That Doesn't Collapse When a Woman Leaves"),
            ("hard-vs-strong", "The Difference Between Being Hard and Being Strong"),
            ("lead-without-controlling", "How to Lead Without Controlling"),
            ("real-masculinity-2026", "What Real Masculinity Looks Like in 2026"),
            ("unplugged-mans-code", "The Unplugged Man's Code (Final 10 Principles)"),
            ("closing-letter", "Closing Letter — To the Man You're Becoming"),
        ],
    },
]


def chapter_body(book: dict, slug: str, title: str, index: int) -> str:
    """Return markdown body for a chapter."""
    from scripts.unplugged_content import get_chapter_content

    return get_chapter_content(book["slug"], slug, title, index, book)


def _yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_book(book: dict) -> None:
    root = SERIES_ROOT / book["slug"]
    chapters_dir = root / "chapters"
    chapters_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        f"title: {_yaml_quote(book['title'])}",
        f"author: {SERIES_META['author']}",
        "language: en",
        f"description: {_yaml_quote(book['subtitle'])}",
        f"publisher: {SERIES_META['publisher']}",
        f"series: {_yaml_quote(SERIES_META['series_title'])}",
        f"series_index: {book['index']}",
        f"identifier: urn:unplugged-al:{book['slug']}",
        "",
        "chapters:",
    ]
    for i, (slug, title) in enumerate(book["chapters"], start=1):
        fname = f"{i:02d}-{slug}.md"
        lines.append(f"  - title: {_yaml_quote(title)}")
        lines.append(f"    file: chapters/{fname}")
        content = chapter_body(book, slug, title, i)
        (chapters_dir / fname).write_text(content, encoding="utf-8")

    (root / "book.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_series_readme() -> None:
    SERIES_ROOT.mkdir(parents=True, exist_ok=True)
    rows = "\n".join(
        f"| {i} | {b['title']} | {b['subtitle'][:60]}... |" if len(b["subtitle"]) > 60
        else f"| {i} | {b['title']} | {b['subtitle']} |"
        for i, b in enumerate(BOOKS, 1)
    )
    text = f"""# {SERIES_META['series_title']}

**{SERIES_META['series_subtitle']}**

## Core Promise

This series teaches you how to stop repeating the same painful patterns with women, how to carry yourself with real strength, and how to build a life that doesn't fall apart every time a relationship ends or gets difficult.

## Target Reader

Men who have been through painful relationships, divorces, or years of feeling like they keep choosing the wrong women. Men who are ready to stop simping, stop over-investing, and start leading their own life with clarity and self-respect.

## Series Structure

Six short, powerful books (each 120–160 pages). Each book stands alone but builds on the one before it.

| # | Book | Subtitle |
|---|------|----------|
{rows}

## Build the Series

```bash
ebook-factory batch books/the-unplugged-al
```

## Build One Book

```bash
ebook-factory build books/the-unplugged-al/01-frame-first
```
"""
    (SERIES_ROOT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    write_series_readme()
    for book in BOOKS:
        write_book(book)
        print(f"Wrote {book['title']}")


if __name__ == "__main__":
    main()
