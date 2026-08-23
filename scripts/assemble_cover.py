#!/usr/bin/env python3
"""Assemble cover/cover-exact.jpg from cover/parts/*.b64 (exact original bytes)."""
from __future__ import annotations

import base64
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "cover" / "parts"
OUT = ROOT / "cover" / "cover-exact.jpg"


def main() -> None:
    files = sorted(PARTS.glob("part-*.b64"))
    if not files:
        raise SystemExit(f"no parts in {PARTS}")
    data = b"".join(base64.b64decode(p.read_text()) for p in files)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(data)
    print(f"wrote {OUT} ({len(data)} bytes) from {len(files)} parts")


if __name__ == "__main__":
    main()
