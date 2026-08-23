#!/usr/bin/env python3
"""Rebuild cover/cover-exact.jpg from cover/parts/*.b64 if the jpg is not present."""
from __future__ import annotations
import base64
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COVER = ROOT / "cover" / "cover-exact.jpg"
PARTS = ROOT / "cover" / "parts"
NEED = "8c39436a4243ca11596380909b87c7962319d20cc24398493c7b5432b2252bc3"

def main() -> None:
    if COVER.is_file() and hashlib.sha256(COVER.read_bytes()).hexdigest() == NEED:
        print(f"cover already exact: {COVER}")
        return
    blobs = sorted(PARTS.glob("p*.b64"))
    if not blobs:
        raise SystemExit(f"missing {COVER} and no {PARTS}/p*.b64")
    data = base64.b64decode("".join(p.read_text() for p in blobs))
    digest = hashlib.sha256(data).hexdigest()
    if digest != NEED:
        raise SystemExit(f"assembled cover hash {digest} != {NEED}")
    COVER.parent.mkdir(parents=True, exist_ok=True)
    COVER.write_bytes(data)
    print(f"wrote {COVER} ({len(data)} bytes)")

if __name__ == "__main__":
    main()
