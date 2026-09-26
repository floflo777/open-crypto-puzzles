# Open leads, full notes

## 1. A clarification from the author on 3 exact bindings

The geometry is fully certified and the mini-hint formula is read at the pixel level, but 3
specific meanings are not fixed by anything the author has published:

- What "x" refers to in "64/x - x": a value that varies per rectangle or per pair (most
  likely a border-thickness measurement), or a single fixed constant.
- The exact normalization meant by "apply more operations to obtain the results in byte
  range": which specific rounding or scaling step turns a raw sum into a single byte.
- The exact sense of "following": which of the several spatially plausible pairings (or a
  sorted-order pairing not yet fully explored) the author means.

Once any one of these is fixed by new information, the already-certified geometry becomes
the 32 key bytes by direct calculation, with no further search needed. The author has a
track record of eventually clarifying hints for other puzzles in the same series (a
correction was already issued once, in 2021, for this puzzle itself), so a direct question
to the author is the highest-ranked lead here.

## 2. A higher-fidelity source for the mini-hint glyphs

The 2021 mini-hint is read at the pixel level from the published image itself; a source
image at higher resolution than what has been published (if one exists) could resolve
ambiguity in the glyph reading directly, without needing the author's own clarification.

## 3. A wider author-error tolerance sweep

A 3-byte wildcard tolerance sweep on 1 or 2 of the candidate bases already tried (roughly
660 million derivations per base) is a bounded search, not an open-ended one, but its
expected value is marginal against the leads above and it has not been run.
