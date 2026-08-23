#!/usr/bin/env python3
"""Build Odyssey.md and a valid EPUB 3 from english/book-*.md (stdlib only)."""

from __future__ import annotations

import html
import hashlib
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parent
ENGLISH = REPO / "odyssey" / "english"
EBOOK = REPO / "ebook"
COVER = REPO / "odyssey" / "cover" / "cover.jpg"
COVER_SHA256 = "8c39436a4243ca11596380909b87c7962319d20cc24398493c7b5432b2252bc3"

ROMAN = {
    1: "I",
    2: "II",
    3: "III",
    4: "IV",
    5: "V",
    6: "VI",
    7: "VII",
    8: "VIII",
    9: "IX",
    10: "X",
    11: "XI",
    12: "XII",
    13: "XIII",
    14: "XIV",
    15: "XV",
    16: "XVI",
    17: "XVII",
    18: "XVIII",
    19: "XIX",
    20: "XX",
    21: "XXI",
    22: "XXII",
    23: "XXIII",
    24: "XXIV",
}

EXPECTED_COUNTS = {
    1: 444,
    2: 434,
    3: 497,
    4: 847,
    5: 493,
    6: 331,
    7: 347,
    8: 586,
    9: 566,
    10: 573,
    11: 640,
    12: 453,
    13: 440,
    14: 533,
    15: 557,
    16: 480,
    17: 606,
    18: 428,
    19: 604,
    20: 394,
    21: 434,
    22: 501,
    23: 371,
    24: 548,
}
EXPECTED_MISSING = {10: {456}, 16: {101}, 23: {49}}
EXPECTED_TOTAL = 12107

# Stable identifier for this edition (not a person).
PUB_UUID = "urn:uuid:6f4e2c91-8a17-4b3d-9e05-2c8f1a7d4b60"
MODIFIED = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# Front-matter copy written for this edition.
IMPRINT = {
    "work": "The Odyssey",
    "subtitle": "Translated from the Greek",
    "author": "Author: Homer",
    "credit": "Translated from the Greek by Grok Bot.",
    "made": "This eBook created by Grok Bot.",
    "date": "19 August 2026",
    "rights": (
        "The Greek poem is in the public domain. "
        "This English translation is also placed in the public domain."
    ),
    "heading": "About this edition",
    "source": (
        "The Greek text is that of the Perseus Digital Library, "
        "tlg0012.tlg002.perseus-grc2 (Allen\u2019s Oxford Classical Text, "
        "by way of the 1919 Murray Loeb Greek), retrieved 18 August 2026."
    ),
    "method": (
        "This English was made from that Greek alone, not from Butler, "
        "Fagles, Wilson, Lattimore, or any other English Odyssey."
    ),
    "lines": (
        "Line numbers follow the Greek. This edition omits the plus-verses "
        "10.456, 16.101, and 23.49."
    ),
    "reading": (
        "At 11.134\u2013137 and again at 23.281\u201382, Teiresias says death "
        "will come from the sea. The Greek can also mean away from the sea. "
        "This edition keeps \u201cfrom the sea.\u201d"
    ),
}

VERSE_RE = re.compile(r"^(\d+)\t(.*)$")
SPEAKER_RE = re.compile(r"^>\s*(.*)$")


def source_path(book: int) -> Path:
    return ENGLISH / f"book-{book:02d}.md"


def parse_book(book: int) -> list[tuple[str, object]]:
    """Return a sequence of ('speaker', name) and ('verse', n, text)."""
    path = source_path(book)
    text = path.read_text(encoding="utf-8")
    events: list[tuple[str, object]] = []
    verses: dict[int, str] = {}
    for raw in text.splitlines():
        if not raw.strip() or raw.startswith("#"):
            continue
        m = VERSE_RE.match(raw)
        if m:
            n = int(m.group(1))
            body = m.group(2).rstrip()
            if n in verses:
                raise ValueError(f"duplicate verse {book}.{n}")
            verses[n] = body
            events.append(("verse", (n, body)))
            continue
        sm = SPEAKER_RE.match(raw)
        if sm:
            events.append(("speaker", sm.group(1).strip()))
            continue
        raise ValueError(f"unparsed line in book {book}: {raw!r}")

    count = len(verses)
    if count != EXPECTED_COUNTS[book]:
        raise ValueError(f"book {book}: expected {EXPECTED_COUNTS[book]} verses, got {count}")
    nums = set(verses)
    last = max(nums)
    missing = set(range(1, last + 1)) - nums
    if missing != EXPECTED_MISSING.get(book, set()):
        raise ValueError(f"book {book}: unexpected missing verses {sorted(missing)}")
    return events


def speaker_display(name: str) -> str:
    s = name.strip()
    if s.startswith("(") and s.endswith(")") and len(s) > 2:
        s = s[1:-1].strip()
    if s.lower() == "narrator":
        return "Narrator"
    return s


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def esc_attr(s: str) -> str:
    return html.escape(s, quote=True)


def build_markdown(books: dict[int, list]) -> str:
    parts = [
        "# The Odyssey",
        "",
        "translated from the Greek",
        "",
        IMPRINT["author"],
        "",
    ]
    parts.extend([
        IMPRINT["author"],
        "",
        IMPRINT["credit"],
        IMPRINT["made"],
        IMPRINT["date"],
        "",
        IMPRINT["rights"],
        "",
        "## " + IMPRINT["heading"],
        "",
        IMPRINT["source"],
        "",
        IMPRINT["method"],
        "",
        IMPRINT["lines"],
        "",
        IMPRINT["reading"],
        "",
    ])
    for book in range(1, 25):
        parts.append(f"# Book {ROMAN[book]}")
        parts.append("")
        for kind, payload in books[book]:
            if kind == "speaker":
                parts.append(f"> {payload}")
            else:
                n, text = payload
                parts.append(f"{n}\t{text}")
        parts.append("")
    return "\n".join(parts)


CSS = """\
/* The Odyssey — reading stylesheet */
html {
  font-size: 100%;
}
body {
  font-family: Georgia, "Palatino Linotype", Palatino, "Book Antiqua", "Times New Roman", serif;
  line-height: 1.55;
  max-width: 34em;
  margin: 0 auto;
  padding: 1.4em 1.2em 3em;
  hyphens: none;
  -webkit-hyphens: none;
}
h1 {
  font-weight: normal;
  text-align: center;
  line-height: 1.25;
  margin: 1.6em 0 1.2em;
}
h1.book-title {
  font-size: 1.55em;
  font-weight: normal;
  page-break-before: always;
  break-before: page;
  margin-top: 1.8em;
  margin-bottom: 1.4em;
}
p {
  margin: 0.85em 0;
}
.verse {
  margin: 0;
  padding: 0 0 0 3em;
  text-indent: -3em;
  page-break-inside: avoid;
  break-inside: avoid;
}
.ln {
  display: inline-block;
  width: 2.4em;
  margin-right: 0.6em;
  text-align: right;
  font-size: 0.72em;
  opacity: 0.42;
  font-variant-numeric: tabular-nums;
}
.tx {
  font-size: 1em;
}
.speaker {
  font-style: italic;
  margin: 1.15em 0 0.4em 3em;
  font-size: 0.95em;
  opacity: 0.82;
}
body.title-page {
  text-align: center;
  padding-top: 18%;
  max-width: 28em;
}
body.title-page h1,
body.title-page .author,
body.title-page .subtitle {
  text-align: center;
  display: block;
  width: 100%;
  margin-left: auto;
  margin-right: auto;
}
body.title-page h1 {
  font-size: 2.35em;
  letter-spacing: 0.06em;
  margin: 0 auto;
}
body.title-page .author {
  margin: 0.85em auto 0;
  font-size: 1.15em;
}
body.title-page .subtitle {
  font-style: italic;
  font-size: 1.12em;
  margin-top: 2.8em;
  margin-bottom: 0;
  opacity: 0.78;
}
body.imprint {
  max-width: 28em;
  font-size: 0.88em;
  padding-top: 3.2em;
}
body.imprint p {
  text-align: left;
  line-height: 1.5;
  margin: 0.7em 0;
}
body.imprint .imprint-title {
  margin-bottom: 0.15em;
}
body.imprint .imprint-sub {
  margin-top: 0;
  margin-bottom: 0.35em;
}
body.imprint .imprint-author {
  margin-top: 0;
  margin-bottom: 1.35em;
}
body.imprint .imprint-credit {
  margin-bottom: 0.15em;
}
body.imprint .imprint-made {
  margin-top: 0;
  margin-bottom: 0.15em;
}
body.imprint .imprint-date {
  margin-top: 0.7em;
  margin-bottom: 1.35em;
}
body.imprint h2.edition-head {
  font-size: 1em;
  font-weight: normal;
  text-align: left;
  margin: 1.7em 0 0.7em;
}
nav#toc ol {
  list-style: none;
  padding-left: 0;
}
nav#toc li {
  margin: 0.35em 0;
}
nav#toc a {
  text-decoration: none;
}
body.cover-page {
  margin: 0;
  padding: 0;
  max-width: none;
  text-align: center;
}
body.cover-page img {
  max-width: 100%;
  height: auto;
}
"""


def xhtml_shell(title: str, body_class: str, body: str, extra_head: str = "") -> str:
    cls = f' class="{body_class}"' if body_class else ""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<!DOCTYPE html>\n"
        '<html xmlns="http://www.w3.org/1999/xhtml" '
        'xmlns:epub="http://www.idpf.org/2007/ops" '
        'xml:lang="en" lang="en">\n'
        "<head>\n"
        '  <meta charset="utf-8"/>\n'
        f"  <title>{esc(title)}</title>\n"
        '  <link rel="stylesheet" type="text/css" href="style.css"/>\n'
        f"{extra_head}"
        "</head>\n"
        f"<body{cls}>\n"
        f"{body}"
        "</body>\n"
        "</html>\n"
    )


def title_xhtml() -> str:
    body = (
        '  <section epub:type="titlepage">\n'
        "    <h1>The Odyssey</h1>\n"
        '    <p class="author" style="text-align:center;display:block;width:100%;margin-left:auto;margin-right:auto;">Homer</p>\n'
        '    <p class="subtitle" style="text-align:center;display:block;width:100%;margin-left:auto;margin-right:auto;">translated from the Greek</p>\n'
        "  </section>\n"
    )
    return xhtml_shell("The Odyssey", "title-page", body)


def copyright_xhtml() -> str:
    body = (
        '  <section epub:type="copyright-page">\n'
        f'    <p class="imprint-title">{esc(IMPRINT["work"])}</p>\n'
        f'    <p class="imprint-author">{esc(IMPRINT["author"])}</p>\n'
        f'    <p class="imprint-credit">{esc(IMPRINT["credit"])}</p>\n'
        f'    <p class="imprint-made">{esc(IMPRINT["made"])}</p>\n'
        f'    <p class="imprint-date">{esc(IMPRINT["date"])}</p>\n'
        f"    <p>{esc(IMPRINT['rights'])}</p>\n"
        f'    <h2 class="edition-head">{esc(IMPRINT["heading"])}</h2>\n'
        f"    <p>{esc(IMPRINT['source'])}</p>\n"
        f"    <p>{esc(IMPRINT['method'])}</p>\n"
        f"    <p>{esc(IMPRINT['lines'])}</p>\n"
        f"    <p>{esc(IMPRINT['reading'])}</p>\n"
        "  </section>\n"
    )
    return xhtml_shell(IMPRINT["heading"], "imprint", body)


def book_xhtml(book: int, events: list) -> str:
    roman = ROMAN[book]
    title = f"Book {roman}"
    lines = [
        f'  <section epub:type="chapter" id="book-{book}">\n',
        f'    <h1 class="book-title">{esc(title)}</h1>\n',
    ]
    for kind, payload in events:
        if kind == "speaker":
            shown = speaker_display(payload)
            lines.append(f'    <p class="speaker">{esc(shown)}</p>\n')
        else:
            n, text = payload
            lines.append(
                f'    <p class="verse" id="b{book}-l{n}">'
                f'<span class="ln">{n}</span>'
                f'<span class="tx">{esc(text)}</span></p>\n'
            )
    lines.append("  </section>\n")
    return xhtml_shell(title, "book", "".join(lines))


def nav_xhtml() -> str:
    items = [
        '      <li><a href="title.xhtml">Title</a></li>',
        '      <li><a href="copyright.xhtml">About this edition</a></li>',
    ]
    for book in range(1, 25):
        items.append(
            f'      <li><a href="book-{book:02d}.xhtml">Book {ROMAN[book]}</a></li>'
        )
    body = (
        '  <nav epub:type="toc" id="toc">\n'
        "    <h1>Contents</h1>\n"
        "    <ol>\n"
        + "\n".join(items)
        + "\n    </ol>\n"
        "  </nav>\n"
        '  <nav epub:type="landmarks" id="landmarks" hidden="hidden">\n'
        "    <ol>\n"
        '      <li><a epub:type="frontmatter" href="title.xhtml">Title page</a></li>\n'
        '      <li><a epub:type="bodymatter" href="book-01.xhtml">Book I</a></li>\n'
        "    </ol>\n"
        "  </nav>\n"
    )
    return xhtml_shell("Contents", "", body)


def toc_ncx() -> str:
    points = [
        ("np-title", 1, "Title", "title.xhtml"),
        ("np-copyright", 2, "About this edition", "copyright.xhtml"),
    ]
    play = 3
    for book in range(1, 25):
        points.append(
            (f"np-book-{book:02d}", play, f"Book {ROMAN[book]}", f"book-{book:02d}.xhtml")
        )
        play += 1
    nav_points = []
    for pid, order, label, src in points:
        nav_points.append(
            f'    <navPoint id="{pid}" playOrder="{order}">\n'
            f"      <navLabel><text>{esc(label)}</text></navLabel>\n"
            f'      <content src="{src}"/>\n'
            "    </navPoint>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
        "  <head>\n"
        f'    <meta name="dtb:uid" content="{PUB_UUID}"/>\n'
        '    <meta name="dtb:depth" content="1"/>\n'
        '    <meta name="dtb:totalPageCount" content="0"/>\n'
        '    <meta name="dtb:maxPageNumber" content="0"/>\n'
        "  </head>\n"
        "  <docTitle><text>The Odyssey</text></docTitle>\n"
        "  <navMap>\n"
        + "\n".join(nav_points)
        + "\n  </navMap>\n"
        "</ncx>\n"
    )


def content_opf() -> str:
    manifest_items = [
        '    <item id="cover-image" href="cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
        '    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '    <item id="css" href="style.css" media-type="text/css"/>',
        '    <item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>',
        '    <item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml"/>',
    ]
    # Jacket is cover-image only. Do not put the painting in the linear spine.
    spine_refs = [
        '    <itemref idref="title"/>',
        '    <itemref idref="copyright"/>',
    ]
    for book in range(1, 25):
        bid = f"book-{book:02d}"
        manifest_items.append(
            f'    <item id="{bid}" href="{bid}.xhtml" media-type="application/xhtml+xml"/>'
        )
        spine_refs.append(f'    <itemref idref="{bid}"/>')
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" '
        'unique-identifier="pub-id" xml:lang="en">\n'
        '  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'    <dc:identifier id="pub-id">{PUB_UUID}</dc:identifier>\n'
        "    <dc:title>The Odyssey</dc:title>\n"
        "    <dc:language>en</dc:language>\n"
        '    <dc:creator id="author">Homer</dc:creator>\n'
        '    <meta refines="#author" property="role" scheme="marc:relators">aut</meta>\n'
        '    <meta refines="#author" property="file-as">Homer</meta>\n'
        "    <dc:description>translated from the Greek</dc:description>\n"
        '    <meta name="cover" content="cover-image"/>\n'
        f'    <meta property="dcterms:modified">{MODIFIED}</meta>\n'
        "  </metadata>\n"
        "  <manifest>\n"
        + "\n".join(manifest_items)
        + "\n  </manifest>\n"
        '  <spine toc="ncx">\n'
        + "\n".join(spine_refs)
        + "\n  </spine>\n"
        "</package>\n"
    )


CONTAINER_XML = """\
<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""


def write_epub(path: Path, files: dict[str, bytes]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as zf:
        info = zipfile.ZipInfo("mimetype")
        info.compress_type = zipfile.ZIP_STORED
        info.extra = b""
        zf.writestr(info, b"application/epub+zip")
        for name, data in files.items():
            zi = zipfile.ZipInfo(name)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.extra = b""
            zf.writestr(zi, data)


def assert_xml(name: str, data: bytes) -> None:
    try:
        ET.fromstring(data)
    except ET.ParseError as e:
        raise ValueError(f"invalid XML in {name}: {e}") from e


def main() -> None:
    if not COVER.is_file():
        raise SystemExit(f"missing exact cover: {COVER}")
    cover_bytes = COVER.read_bytes()
    digest = hashlib.sha256(cover_bytes).hexdigest()
    if digest != COVER_SHA256:
        raise SystemExit(f"cover hash mismatch: {digest}")

    EBOOK.mkdir(parents=True, exist_ok=True)
    books = {}
    total = 0
    for book in range(1, 25):
        events = parse_book(book)
        books[book] = events
        total += sum(1 for k, _ in events if k == "verse")
    if total != EXPECTED_TOTAL:
        raise SystemExit(f"total verses {total} != {EXPECTED_TOTAL}")

    md = build_markdown(books)
    md_path = EBOOK / "Odyssey.md"
    md_path.write_text(md, encoding="utf-8")

    files: dict[str, bytes] = {
        "META-INF/container.xml": CONTAINER_XML.encode("utf-8"),
        "OEBPS/content.opf": content_opf().encode("utf-8"),
        "OEBPS/toc.ncx": toc_ncx().encode("utf-8"),
        "OEBPS/nav.xhtml": nav_xhtml().encode("utf-8"),
        "OEBPS/style.css": CSS.encode("utf-8"),
        "OEBPS/cover.jpg": cover_bytes,
        "OEBPS/title.xhtml": title_xhtml().encode("utf-8"),
        "OEBPS/copyright.xhtml": copyright_xhtml().encode("utf-8"),
    }
    for book in range(1, 25):
        files[f"OEBPS/book-{book:02d}.xhtml"] = book_xhtml(book, books[book]).encode("utf-8")

    for name, data in files.items():
        if name.endswith((".xhtml", ".xml", ".opf", ".ncx")):
            assert_xml(name, data)

    epub_path = EBOOK / "Odyssey.epub"
    write_epub(epub_path, files)
    print(f"wrote {md_path} ({md_path.stat().st_size} bytes)")
    print(f"wrote {epub_path} ({epub_path.stat().st_size} bytes)")
    print(f"verses: {total}")
    print(f"cover: {COVER} ({len(cover_bytes)} bytes) sha256={digest}")


if __name__ == "__main__":
    main()
