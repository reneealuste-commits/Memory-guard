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

## Development

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
