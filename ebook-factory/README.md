# The Honest Father Series — Ebook Factory

Book production pipeline for Amazon KDP titles under **Uncle Al** / The Honest Father Series.

## Book 6: A Strong Son

Final book in the series. **12,467 words** · **14 chapters** · **4 parts** · **10-rule Son's Code**.

### Build

```bash
cd ebook-factory
pip install -r requirements.txt
npm install
python3 builders/prepare_cover.py   # after cover source PNG exists
python3 builders/build_all.py
```

### Outputs (`outputs/`)

| File | Format |
|------|--------|
| `06_a_strong_son_interior.pdf` | Paperback interior (6×9, ReportLab) |
| `06_a_strong_son.epub` | Kindle (manual ZIP, Unicode XHTML) |
| `06_a_strong_son.docx` | Editable manuscript + auto TOC (docx-js) |
| `06_a_strong_son_kindle_cover.jpg` | Kindle cover (1600×2560) |
| `06_a_strong_son_wrap_rgb.jpg` | Paperback wrap (RGB) |
| `06_a_strong_son_wrap_cmyk.pdf` | Paperback wrap (CMYK via Ghostscript) |

See `outputs/KDP_UPLOAD_06_a_strong_son.md` for upload metadata.

### Architecture

- `books/book06_strong_son/content.py` — chapter prose (HTML entities)
- `books/book06_strong_son/meta.py` — metadata, Son's Code, back matter
- `builders/` — PDF, EPUB, DOCX, wrap, cover prep

### Critical rules

- EPUB: **no named HTML entities** in XHTML (KDP XML parser rejects them)
- DOCX TOC: docx-js `TableOfContents` + `updateFields: true`
- Wrap spine: blank under 79 pages
- Back cover text: always use `wrap()` — never raw `draw.text()` for paragraphs
