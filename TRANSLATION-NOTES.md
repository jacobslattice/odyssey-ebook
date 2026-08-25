# Translation notes

18–19 August 2026. A complete English *Odyssey*, not a claim that it is the best English *Odyssey*. The work was done as rigorously as the time allowed, and the thin spots are named.

## Methodology

**Greek only.** The Greek is Perseus `tlg0012.tlg002.perseus-grc2` (canonical-greekLit): the Allen-based text printed in the 1919 Murray Loeb. Only the Greek half was used. Murray’s English was not opened, nor Butler, Fagles, Wilson, Lattimore, Fitzgerald, Pope, Chapman, Kline, or any other English *Odyssey*, as source or crib. Lexica, grammars, scholia, and commentaries *on the Greek* were allowed.

**Line-for-line.** One English line per Greek line, same number. This edition has no plus-verses **10.456**, **16.101**, **23.49**. Those numbers were skipped and noted, not filled from memory or from another edition. Full count: **12,107** English verses.

**Voice.** Clear contemporary spoken English, faithful to the Greek. Not Victorian pastiche. Not a clone of a living translator. Gods stay gods; no slang modernization. A ten-line sample (1.1–10) set the register before the rest of the poem: “man of many turnings,” “reckless doing,” “day of coming home.”

**Book-by-book process.** For each book the Greek was read, hard clauses construed, then English written line for line. Verification was mechanical: unique numbered lines, no duplicates, expected gaps only.

**Names.** A locked spelling list (Odysseus, Telemachus, Penelope, Athena, and so on). A few Greek doublets were kept consistent and flagged: Agelaus for both Ἀγέλεως and Ἀγέλαος; Melanthius / Melantheus as the Greek switches. Some words were left visible rather than flattened: **lycabas**, **atta**, **sardonic**, **Bad-Ilium, not to be named**, **Nobody / nobody** for Οὖτις / μή τις.

**Epithets.** Translated as meaning, not stripped as decoration, and not left as raw Greek unless English had no honest word. Owl-eyed Athena, Odysseus of many devices, careful Penelope, thoughtful Telemachus spoke opposite, winged words — kept as formulas.

**Cruxes.** If a line was genuinely disputed, one English was chosen and noted. Examples: ἀβληχρὸς θάνατος ἐξ ἁλός (23.281–82) kept as “death from the sea,” though it can be read as death *away from* the sea; Amphimedon’s retelling in 24 is *his* compression, not a silent rewrite to match Books 19–23. The hanging of the twelve women and Melanthius’s mutilation are not softened.

## Tools and sources

**Greek text**

- PerseusDL/canonical-greekLit, `tlg0012.tlg002.perseus-grc2.xml`, fetched 18 August 2026.
- Numbered hexameters extracted from descendant `<l n="…">` elements.

**Lexica / grammar (allowed, used as needed)**

- LSJ / Cunliffe / Autenrieth for load-bearing words (πολύτροπος, ἀτασθαλία, νόστος, θυμός, ξεῖνος, μῆτις, σῆμα, ἄτη, and others).
- Formulaic lines were construed from the Greek in the file. Loaded words were checked. That is a known limit, not a secret.

**What was not used**

- Any English *Odyssey*.
- Murray’s facing English (the Loeb is named only as the print source of the *Greek*).
- Other modern editions as a base text.

**Files in this repository**

- English: `odyssey/english/book-01.md` … `book-24.md` — speaker tags and numbered lines
- Builder: `build_ebook.py`
- Jacket: `odyssey/cover/cover.jpg`

## Limits

**What held**

- Locking 1.1–10 before the rest of the poem, so the voice did not have to be renegotiated.
- One English line per Greek line, verified by script.

**What is thin**

- There has not been a full rereading of all 12,107 lines against the Greek. That is the largest quality risk.
- Formula consistency is good where it was locked and probably uneven on less frequent epithets.
- `epubcheck` was not run. Zip integrity and XML parse were checked.

This English is usable. It is not a finished literary edition.
