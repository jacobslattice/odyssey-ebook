# Rebuild

python3 scripts/build_ebook.py

The builder expects:
- /workspace/odyssey/english/book-NN.md
- /workspace/odyssey/scripts/build_ebook.py
- /workspace/contest/epub-art/cover-exact.jpg

On a checkout of this repo, either keep those absolute paths or edit the three Path constants at the top of scripts/build_ebook.py to point at english/, this script, and cover/cover-exact.jpg.

Cover SHA-256 must remain 8c39436a4243ca11596380909b87c7962319d20cc24398493c7b5432b2252bc3.
