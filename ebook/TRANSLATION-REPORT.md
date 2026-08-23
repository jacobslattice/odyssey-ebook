# Odyssey translation — method report

For Chris, via Producer. Homeric Translator. 18–19 August 2026 (MT). First person. No chapter dumps.

This is a working draft of a whole *Odyssey*, not a claim that it is the best English *Odyssey*. I did the most rigorous job I could in the time, and I am honest about where it is thin.

---

## 1. Methodology

**Greek only.** I fetched Perseus `tlg0012.tlg002.perseus-grc2` (canonical-greekLit) and extracted numbered hexameters into `greek/book-01.txt` … `book-24.txt`. That file is the Allen-based Greek printed in the 1919 Murray Loeb. I used the Greek half only. I did not open Murray’s English, or Butler, Fagles, Wilson, Lattimore, Fitzgerald, Pope, Chapman, Kline, or any other English *Odyssey*, as source or crib. Lexica, grammars, scholia, and commentaries *on the Greek* were allowed. I did not use Wikipedia or other English plot guides for the translation or for the compiled notes.

**Line-for-line.** One English line per Greek line, same number. This edition has no plus-verses **10.456**, **16.101**, **23.49**. I skipped those numbers and noted them. I did not invent the missing verses from memory or from another edition. Full count: **12,107** English verses.

**Voice.** Clear contemporary spoken English, faithful to the Greek in front of me. Not Victorian pastiche. Not a clone of a living translator. Gods stay gods; no slang modernization. A ten-line sample (1.1–10) was locked with Producer before the rest of the poem: “man of many turnings,” “reckless doing,” “day of coming home.” That register was the house style.

**Book-by-book process.** For each book I read the Greek file, construed hard clauses before writing English, wrote incrementally to `locked/book-NN.md`, copied to `english/`, snapshotted a line-count file, wrote `notes/book-NN.md` from *our* English (Greek only for loaded words), then `chmod a-w` the four files. Verification was mechanical: unique numbered lines, no duplicates, expected gaps only. Producer asked for one-line status only when a book finished, then no stop between books.

**Names.** A locked spelling list (Odysseus, Telemachus, Penelope, Athena, …). A few Greek doublets I kept consistent in English and flagged: Agelaus for both Ἀγέλεως and Ἀγέλαος; Melanthius / Melantheus as the Greek switches. Some words I left visible rather than flattening: **lycabas**, **atta**, **sardonic**, **Bad-Ilium, not to be named**, **Nobody / nobody** for Οὖτις / μή τις.

**Epithets.** Translated as meaning, not stripped as decoration, and not left as raw Greek unless English had no honest word. Grey-eyed Athena, Odysseus of many devices, careful Penelope, thoughtful Telemachus spoke opposite, winged words — kept as formulas, not reinvented each time.

**Cruxes.** If a line was genuinely disputed I picked one English and noted it. I did not paper over it. Examples I would still mark on a second pass: ἀβληχρὸς θάνατος ἐξ ἁλός (23.281–82) kept as “death from the sea,” though it can be read as death *away from* the sea; Amphimedon’s retelling in 24 is *his* compression (no twelve women, Zeus woke Odysseus, he bid Penelope set the bow), not a silent rewrite to match Books 19–23; 24.398’s nominative Ὀδυσεῦς vs who kisses the wrist. The hanging of the twelve women and Melanthius’s mutilation are not softened.

**Notes.** Per-book notes summarize only our English: who is on stage, what happens, loaded words the Greek forced, disputes. The compiled guide (`Odyssey-Notes.md`) is a shorter Cliffs-Notes of the ebook only — not of Wikipedia, not of anyone else’s *Odyssey*.

---

## 2. Tools and sources

**Greek text**
- PerseusDL/canonical-greekLit, `tlg0012.tlg002.perseus-grc2.xml` (1,560,139 bytes), fetched 18 August 2026, 6:04 PM MT.
- Local: `/workspace/odyssey/raw/tlg0012.tlg002.perseus-grc2.xml`
- Extractor: `scripts/extract_greek.py` — descendant `<l n=“…”>` elements, one verse per line, `N<TAB>Greek`.
- Line census: `greek/LINECOUNTS.txt`

**Lexica / grammar (allowed, used as needed, not as a second plot)**
- LSJ / Cunliffe / Autenrieth for load-bearing words (πολύτροπος, ἀτασθαλία, νόστος, θυμός, ξεῖνος, μῆτις, σῆμα, ἄτη, ἀθηρηλοιγός, etc.).
- I did not systematically re-lexicate every line. Formulaic lines I construed from the Greek in the file and from training knowledge of Homeric Greek, then checked the loaded ones. That is a known weakness, not a secret.

**What I did not use**
- Any English *Odyssey*.
- Murray’s facing English (the Loeb is named only as the print source of the *Greek*).
- Other modern editions as a base text. I stayed on this Allen-based file. If a later book had a real editorial problem I would have checked Allen OCT / van Thiel / West against *this* file and said so. I did not switch base mid-poem.

**Working formats**
- Greek: `greek/book-NN.txt`
- English: `english/book-NN.md` — `# Odyssey Book N` (Book 24 header is the shorter `# Odyssey 24`), `> Speaker` tags, `N<TAB>line`
- Locked copies + snapshots: `locked/book-NN.md`, `locked/book-NN-<count>.md`
- Per-book notes: `notes/book-NN.md`
- Naming quirk: books 1–9 are zero-padded (`book-01.md`); 10–24 are not (`book-10.md`). Both are complete.

**Ebook and compiled notes**
- Concatenated markdown: `/workspace/odyssey/ebook/Odyssey.md` (700,911 bytes; 12,107 numbered lines; same three gaps).
- EPUB 3: `/workspace/odyssey/ebook/Odyssey.epub` (372,882 bytes). Built with a stdlib-only script, `scripts/build_ebook.py` — mimetype first and uncompressed, one XHTML file per book, muted line numbers, italic speaker lines, `toc.ncx` + `nav.xhtml`. Title page: *The Odyssey* / A translation from the Greek. No famous-translator name. `epubcheck` was not installed; zip integrity and XML parse were checked by hand.
- Compiled notes: `/workspace/odyssey/ebook/Odyssey-Notes.md` (~19,800 words). Front arc, 24 chapters (On stage / What happens / Loaded words), formulas, cast, plus-verse list.

---

## 3. Lessons learned

**What worked**
- Locking a 1.1–10 sample with Producer before the rest of the poem. The voice did not have to be renegotiated book by book.
- One English line per Greek line, verified by script. That caught missing and duplicate verses immediately.
- Write-protecting a finished book. After we started doing that, finished books stopped getting clobbered.
- Incremental write-to-disk in chunks. Long books in memory-only drafts died.
- Notes that are only allowed to talk about *our* English. That kept the guide honest when the per-book notes were uneven.
- Reporting to Producer in one line per finished book, then not stopping. The job actually finished.

**What was slow or fragile**
- Parallel book-writers on the same files. Early on, several executors at once produced duplicate Book 1 lines, empty first runs, and wrecked partials (there is still a `book-06.WRECKED.md` in `english/`). Two-at-a-time was better; one writer per file with `locked/` as the live target was the thing that held.
- Filename padding (`book-01` vs `book-10`) and header drift (`# Odyssey Book 1` vs `# Odyssey 24`). Harmless to a reader, annoying to a build script.
- Per-book notes quality. Books 1–8 and 17–24 are full. Books 9–16 are short checklists (~2 KB each). The compiled guide had to go back to the English for those. The first compiled-notes pass also stopped at the poem-wide arc (~1,200 words) and had to be resumed; a later pass collided with itself and needed a cleanup. The finished guide is clean (24 chapters, no duplicate headings).
- I did not do a full second reading of all 12,107 lines against the Greek after the first draft. Books I finished myself late (22–23 especially) had more live construal; some middle books were first-draft-and-lock. That is the largest quality risk.
- Formula consistency is good where I locked it (winged words, careful Penelope, grey-eyed Athena) and probably uneven on less frequent epithets.
- `epubcheck` never ran. The EPUB opens and the spine/TOC look right. A real validator would still be worth a pass.

**What I would do differently on a second pass**
- One writer, one book, lock immediately. Never five books at once.
- Normalize filenames and headers before translating, not after.
- A short loaded-word glossary *before* Book 1 (πολύτροπος, ἀτασθαλία, νόστος, θυμός, ξεῖνος, μῆτις, κλέος, σῆμα, ἄτη, ἄπτερος μῦθος) and a formula sheet, so mid-poem drift is harder.
- Same notes depth for every book, written the day the English is locked, not deferred.
- A review pass: read the English aloud, then check it against the Greek again, especially Books 4, 8–16, and 24 (the second Nekyia and the peace).
- Run `epubcheck`. Fix the Book 24 header. Decide the 23.281–82 sea-death reading in one sentence and stick it in the ebook’s note-on-text, not only in the notes.
- If this were a published text I would want a classicist to sample a few books against the Greek. I am not going to pretend that step happened.

---

## 4. Current deliverable state

**Done and on disk**

| What | Path | State |
|---|---|---|
| Greek (extracted) | `/workspace/odyssey/greek/book-01.txt` … `book-24.txt` | Complete. 12,107 verses. Gaps: 10.456, 16.101, 23.49. |
| English draft | `/workspace/odyssey/english/book-01.md` … `book-24.md` | Complete, write-protected. Same counts. |
| Locked copies | `/workspace/odyssey/locked/book-NN.md` (+ snapshots) | Same text. Extra wreckage/partials from early collisions still sit beside them; they are not the draft. |
| Per-book notes | `/workspace/odyssey/notes/book-NN.md` | All 24 exist. 9–16 are thin. |
| Ebook (EPUB) | `/workspace/odyssey/ebook/Odyssey.epub` | Built, 372,882 bytes. Not epubcheck’d. |
| Ebook (markdown) | `/workspace/odyssey/ebook/Odyssey.md` | 700,911 bytes. Same 12,107 lines. |
| Compiled notes | `/workspace/odyssey/ebook/Odyssey-Notes.md` | ~19,800 words, 24 chapters. |
| House style / plan | `/workspace/odyssey/STYLE.md`, `PLAN.md`, `README.md` | Locked. |

Producer already has the two delivery paths: `Odyssey.epub` and `Odyssey-Notes.md`.

**Unfinished or known-weak**
- No full Greek-to-English review pass on the whole poem.
- Per-book notes 9–16 are checklists, not the same grain as 1–8 / 17–24.
- Header and filename inconsistency (cosmetic).
- EPUB not run through epubcheck.
- A few cruxes remain one-choice-plus-note, not settled.
- Early junk files in `english/` and `locked/` (`*.WRECKED.md`, `*.partial.md`, chunk files). They are not in the ebook.
- This is a first complete draft. It is usable. It is not a finished literary edition.

I would rather Chris have that last sentence than a cleaner story.
