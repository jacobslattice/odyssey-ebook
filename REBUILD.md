# Rebuild the EPUB

Need: Python 3. Standard library only. No pip packages.

```
python3 scripts/build_ebook.py
```

Run that from the root of this repository.

It reads:

- `english/book-01.md` through `english/book-24.md`
- `cover/cover-exact.jpg`

It writes:

- `ebook/Odyssey.epub`
- `ebook/Odyssey.md`

The jacket must stay the exact file (`sha256 8c39436a4243ca11596380909b87c7962319d20cc24398493c7b5432b2252bc3`). The builder refuses to run if the hash differs.

Imprint text and styles are inside `scripts/build_ebook.py`.
