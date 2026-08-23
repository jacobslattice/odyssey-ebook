# Odyssey ebook

A public-domain English *Odyssey*, made from the Greek (Perseus `tlg0012.tlg002.perseus-grc2`), not from another English translation.

Anyone with Python 3 (stdlib only) and this repository can rebuild the same EPUB.

## Rebuild

From the repository root:

```
python3 scripts/build_ebook.py
```

### Inputs the builder reads

| Path | What it is |
| --- | --- |
| `english/book-01.md` … `english/book-24.md` | Line-for-line English (12,107 verses) |
| `cover/cover-exact.jpg` | Jacket image. SHA-256 must be `8c39436a4243ca11596380909b87c7962319d20cc24398493c7b5432b2252bc3` |
| `scripts/build_ebook.py` | Builder (imprint copy and CSS live in this file) |

No other data files.

### Output

| Path | What it is |
| --- | --- |
| `ebook/Odyssey.epub` | EPUB 3 |
| `ebook/Odyssey.md` | Same English as one markdown file |

Expected: 12,107 verses; plus-verses 10.456, 16.101, and 23.49 omitted; cover hash unchanged.

## Also in this repo

- `ebook/TRANSLATION-REPORT.md` — method
- `REBUILD.md` — same rebuild steps, short form
