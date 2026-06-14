# Ebook Factory

Turn Markdown manuscripts into production-ready **EPUB** ebooks. Define a book in YAML, write chapters in Markdown, and run one command to package title page, table of contents, and styled HTML.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Scaffold a new book
ebook-factory init my-book

# Build EPUB
ebook-factory build my-book
# → my-book/dist/My-Book.epub
```

## Project layout

```
my-book/
├── book.yaml          # metadata + chapter list
├── chapters/
│   ├── 01-intro.md
│   └── 02-body.md
└── dist/              # generated EPUBs
```

### `book.yaml`

```yaml
title: My Novel
author: Jane Doe
language: en
description: A tagline shown on the title page.
publisher: My Press

# optional
cover: assets/cover.jpg
css: assets/custom.css

chapters:
  - title: Prologue
    file: chapters/00-prologue.md
  - chapters/01-chapter-one.md   # title inferred from filename
```

## CLI

| Command | Description |
|---------|-------------|
| `ebook-factory init [path]` | Create a starter book project |
| `ebook-factory build [path]` | Build one EPUB from `book.yaml` or a book directory |
| `ebook-factory batch [dir]` | Build every `book.yaml` under a directory tree |
| `ebook-factory --version` | Show version |

Options:

- `build -o path.epub` — custom output file
- `batch -o dist/` — custom output directory

## Batch publishing

Organize multiple titles under one folder:

```
books/
├── cookbook/
│   ├── book.yaml
│   └── chapters/...
└── guide/
    ├── book.yaml
    └── chapters/...
```

```bash
ebook-factory batch books/
# → books/dist/cookbook/..., books/dist/guide/...
```

## Sample

Build the included example:

```bash
ebook-factory build examples/sample-book
```

## The Unplugged Al Series

A six-book series lives under `books/the-unplugged-al/`:

| # | Book | Focus |
|---|------|-------|
| 1 | Frame First | Emotional control & leadership |
| 2 | Vetting Her | Seeing women clearly |
| 3 | Stop Simping | Self-respect & over-investing |
| 4 | Male Space | Brotherhood & mission |
| 5 | Money & Women | Financial frame & entitlement |
| 6 | The Unplugged Man's Code | Final principles & integration |

Regenerate manuscripts from source content:

```bash
python3 scripts/generate_unplugged_series.py
```

Build the full series:

```bash
ebook-factory batch books/the-unplugged-al
```

### Download ready-made EPUBs

All six books are bundled in one zip (for Google Drive, Kindle, etc.):

**`releases/the-unplugged-al-epubs.zip`**

On GitHub: open the repo → `releases` folder → click the zip → **Download**.

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
