# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Ask the Block 76 solver for the convention of a final Aoi block (closed 2026-10-31)

Closed. eyaler posted the Block 76 string on 2026-10-31 (pull request #49):
`EMERGENCY TOMI climate EMERGENCY`. Its MD5 starts with `f8e`, `MD5("EMERGENCY")` starts
with `1d`, and index 0 gives the escrow `13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd`; I re-derived
it, and it is in `analysis/calibration.md`. The convention is the plain
`[solution] TOMI [TOMI]` shape of blocks 72 to 74, with no twist, so it says nothing new
about Real Big Block. Original note:

Block 76 was swept on 2026-08-17 (tx
`2e271ac2f63f488cd14112bceeed56f159ecd98cb3ce753f08e2d94bb62714a3`) into an active
wallet whose only puzzle input is that block. Whoever did it holds, for a block the
author wrote in the same week as Real Big Block with the same tooling, the exact
serialization she used, the derivation index she took, and whether a "twist" sat on
top of the stated rule. The author herself wrote that she removed "one of the twists"
when she rehashed Real Big Block and, later, that she "lost any information on the
solution of that one" (`clues/author-posts.md`); no archive of the 2019 chapter
exists (established fact 6). The information that calibrates the remaining twist is
therefore in one person's hands, not in any public source.

What would confirm it: a convention that, applied to the "Second" chapter with the
certified case-flip rule, matches `14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W`.
What would kill it: a convention that is already one of the rows in
`analysis/tested.md`.
Cost: needs a person; no compute.

## 2. A bounded 2-character-edit sweep on the strongest base texts

The single-character-edit sweep (266,038,400 candidates, `analysis/tested.md`)
covers every one-character difference from 40 base texts and is exhaustive for
that distance. It does not cover 2-character differences, which would catch a
base text that is off by, for example, one inserted invisible character AND one
capitalization slip. A 2-character sweep restricted to the small set of NBSP and
line-ending pairs (rather than all positions) is a bounded space, not a full
40-base x 2-character search.

This is rank 2 because the copy-range question is much smaller than it
looked. Every contiguous span of the chapter, with both Stage One keep-tests
and the author's line-break bytes, is a certified negative (see killed
section below). A 2026-08-27 slice of this lead is also done: every subset of
the 6 in-sentence NBSPs, and every pair of paragraph-joins swapped between
`\n\n` and `\r\n\r\n`, on the full 273 with three keep-tests (221,520 texts, 0
match). A second slice, run 2026-08-23 on 16 certified bases (8 keep-sets of the
3 planted groups, with and without the Finney quote, across joins, trailing newline
and NBSP conventions): every pair of invisible-character insertions (NBSP, ZWSP, BOM,
TAB, CR, LF, SP) at two paragraph joins, and every insertion plus one case toggle of a
boundary letter, 48,379,696 texts with 4 witnesses per base, 0 match. What remains is
2-edits that are neither of those families, including edits inside a paragraph, on
the other 1-character bases.

What would confirm it: a match within the bounded 2-character space.
What would kill it: exhausting that bounded space with 0 match; the full,
unbounded 2-character space is not proposed here, since its cost is
disproportionate without a narrower reason to expect the answer lives there.
Cost: on the order of an hour on a rented GPU for the bounded version described
above; the private research folder priced this at roughly 45 minutes per base
text for a similarly scoped variant.

## 3. A non-uniform 2019 editor buffer, or a non-contiguous selection

The author's 2019-08-01 ASCII note is `13 10 13 10` between paragraphs. A
26-space SSR indent would have shown a run of ASCII 32 on asciivalue.com, which
she did not report, so a `pre-wrap` reader copy is a weak reading of her own
measurement. Empty `<p><br></p>` between every pair would usually produce more
than two CRLFs, which also sits badly with that measurement. Those two uniform
reconstructions are tested (12,848 and 3,030) and are negatives.

What remains is either empty `<p><br></p>` in some gaps only, or a
non-contiguous subset of paragraphs other than the 17 already swept and the
contiguous spans now swept. The full 2^(n-1) gap space and the full 2^273
subset space are not proposed here.

What would confirm it: such a sparse buffer or subset, with the certified
case-flip rule, matching the current escrow.
What would kill it: a reason to believe she copy-pasted a contiguous range
(already tested) or left a blank line between every paragraph (already tested).
Cost: needs a narrower reason before a search.

## 4. Identify what "76" indexes for Block 76 (closed: the block was swept 2026-08-17)

A method confirmed on 3 other blocks in the same series (56, 57, 58) uses the
block's own number as a position index into a specific corpus (a numbered post
by Satoshi Nakamoto or Hal Finney on bitcointalk, read in a specific order). The
same method, tried against every corpus and ordering available (Satoshi's and
Hal Finney's bitcointalk posts, Hal Finney's tweets), does not produce a post
containing "change" or "from" at position 76. The corpus this method should
index for block 76 has not been identified; candidates not yet tried include the
complete list of Hal Finney's tweets (only 58 were recovered through the
official API; a fuller archive may exist), Satoshi's SourceForge posts, the
Bitcoin whitepaper or v0.1 source code read as a sequence of numbered units, and
the author's own r/Grycoin posts read as their own numbered sequence.

What would confirm it: a position-76 item in the right corpus containing "change
to" or "from change to", tested through `tools/oracle.py --block76-filter` and
then a full derivation.
What would kill it: exhausting the remaining candidate corpora with no match at
position 76.
Cost: minutes per corpus once a candidate corpus is assembled.

## 5. A short, human-reasoned answer to "change to" / "from change to" (closed: the block was swept 2026-08-17)

The author's own hint structure (a short, freeform-text question plus a short
TOMI expansion, confirmed on more than a dozen other blocks) argues for a short,
punchy answer rather than a long dictionary phrase. The scripted sweep in
`analysis/tested.md` covers dictionary and corpus vocabulary exhaustively within
its stated bounds, but a human-reasoned short answer with unusual capitalization
or punctuation (the author's own confirmed style on other blocks, for example
"NGD" for "net zero" or "JD6" for "QWERTY") is a different kind of hypothesis
than a word-list sweep can reach.

What would confirm it: any short candidate, tested through
`tools/oracle.py --block76-filter` first (a near-instant filter) and then
through a full derivation.
What would kill it, in the useful sense: nothing kills this lead outright; it
stays open as a standing invitation, same as any human-reasoned wordplay block
in the series.
Cost: minutes per candidate; no sweep implied.

## Killed: contiguous copy-paste spans of the chapter

Killed 2026-08-27. The author said to copy-paste and change only capitalization,
and that the hashed bytes have two line breaks between paragraphs. Every
contiguous span of 2 or more of the 273 paragraphs, joined with `\n`, `\r\n`,
`\n\n`, or `\r\n\r\n`, with no flip, with the certified first-character
keep-test, and with the first-letter keep-test, including NBSP-to-space and
edge-space strip when those characters are present in the span, is a negative:
1,469,908 unique texts, 0 match. Witness: 3 planted texts recovered. Rate:
530/s. 63 paragraphs start with a double quote, so the two keep-tests are not
the same; both were run. What this does not kill is a non-contiguous selection,
or a contiguous selection that is then edited by two or more characters.

## Killed: the 27 posts between the rehash and the shutdown

Killed 2026-08-27. Full re-read of the author's Grycoin comments from
2019-07-30 to 2019-08-04 (arctic-shift archive of r/Grycoin, plus the Real Big
Block Discussion thread) produced no new paragraph group. It did pin down the
line-break bytes already used in the 2026-08-27 copy search: before the rehash,
one CRLF between paragraphs; after the rehash, Enter twice = `13 10 13 10`.
She also said, on Grycoin Block 2 (2019-08-03), to copy-paste and change only
capitalization. Those constraints are in `analysis/tested.md`; they did not
yield a match.

## Stage One reproduction: the MD5 and two reimplementation gotchas (issue #1)

stakeados (issue #1) wrote down the exact Stage One value, which this folder reproduced during
research but never recorded as a number:

- source: bitcointalk topic 155054, first post, raw HTML (ISO-8859-1, ASCII body)
- md5: `9dd2efb9bc976c2095bd534d7b8d431c`
- derives to `19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN` at `m/44'/0'/0'/0/0`

Both reimplementation gotchas they flag are already handled in `tools/oracle.py`, but neither
was stated in prose: a paragraph break is `<br><br>`, so a single `<br>` (as in the
"[edited slightly]" line) does not start a new paragraph; and the byte encoding is ISO-8859-1,
not UTF-8. Recording the MD5 makes the Stage One reproduction checkable without re-deriving
from the post.
