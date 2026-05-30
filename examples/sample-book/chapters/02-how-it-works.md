# How It Works

The factory follows three steps:

1. **Manifest** — `book.yaml` declares title, author, and chapter files.
2. **Render** — Each `.md` chapter becomes styled HTML.
3. **Package** — Chapters, table of contents, and metadata are written as EPUB.

## Project layout

```
my-book/
├── book.yaml
├── chapters/
│   ├── 01-intro.md
│   └── 02-more.md
└── dist/
    └── my-book.epub
```

## Tables and code

| Step       | Tool              |
|------------|-------------------|
| Authoring  | Markdown          |
| Config     | YAML              |
| Output     | EPUB 3            |

```bash
ebook-factory init my-novel
ebook-factory build my-novel
```
