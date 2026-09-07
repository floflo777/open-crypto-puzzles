# Negatives ledger, Arweave Puzzle Weave #12

The historical candidate sweeps below used the separately calibrated oracle (SHA-512 x11513, AES-OpenSSL decrypt,
`"kty":"RSA"` gate, exact 58-character length filter). None of these runs carries a
planted witness inside its own candidate space, since the correct answer is unknown; the
oracle itself is certified separately against the solved sibling Arweave #8 (see the
README's "Certified against" section). Rows 1-6 are dated 2026-07-25; rows 7-8 are dated
2026-08-18 and are described under the table.

| # | Configuration | Candidates | Result |
|---|---|---|---|
| 1 | Piece 4 hatching read as an ordering scheme: all 4! direction-to-digit assignments across 6 quadrant reading orders | 144 | refuted exhaustively: no assignment produces a valid 1-to-5 permutation or a 5-letter word |
| 2 | Round-1 bounded assembly: 4 sub-answers, 24 orders, 3 cases, length-filtered to exactly 58 | 104,184 (858 seconds) | 0 match |
| 3 | Round-2: the 2 length partitions that survived round 1, 6 orders, 36 color names, Gray/Grey spelling, 2 cases | 46,688 (441 seconds) | 0 match |
| 4 | "BLUE" literal readings, 6 bounded runs: orders, spellings, cases, anagrams | 3,266 | 0 match |
| 5 | Literal `Hexagon`, `BalaenopteraMusculus` (20 characters), and 4-number reorderings | 1,824 | 0 match |
| 6 | Piece 1 read as RGB decimal or hex numbers instead of color words, 4 orders x 5 piece-2 candidates x anagrams x 2 block orders, exact-58 constrained | 768 | 0 match |
| 7 | Piece-2 whale readings x full piece-1 name orderings: 15 length-exact piece-2 strings (the March 2020 round's investors, spelled-out date forms, whale readings) x 1,440 piece-1 strings (the six colour names in all 720 orderings, Gray/Grey) x 3 piece-4 cases of `Alien`, block order 1-2-3-4 | 64,800 (319 seconds) | 0 match |
| 8 | Piece-1 name-assignment expansion: both purple-family flags allowed to take any distinct pair from {Purple, Violet, Indigo}, Gray/Grey, all 720 orderings = 4,320 piece-1 strings x 3 piece-2 readings (`AndreessenHorowitz`, `UnionSquareVenture`, `SixteenMarchTwenty`) x 15 piece-4 anagram-cases (Alien/Aline/Anile/Elain/Liane x 3 cases), block order 1-2-3-4 | 194,400 | 0 match |
| 9 | Block order x geometry-derived piece 1: all 24 orders of the 4 blocks x 144 piece-1 strings x 9 case/spelling variants of `AndreessenHorowitz` x 7 piece-4 words | 217,728 | 0 match |
| 10 | Length-branch B: piece 1 = the three additive primaries (`RedGreenBlue`, 12 chars, all 6 orders) with piece 2 = `AndreessenHorowitz`+`CoinbaseVentures` (34), all 120 letter orders of ALIEN x 3 cases, 24 block orders | 103,680 | 0 match |
| 11 | Length-branch C: piece 1 = Red/Blue/Gray-Grey (11 chars, 12 orders) with piece 2 = `UnionSquareVentures`+`CoinbaseVentures` (35), same piece-4 and block-order coverage | 207,360 | 0 match |
| 12 | Length-branch D: piece 1 = Green/Blue (9 chars) with piece 2 = `AndreessenHorowitz`+`UnionSquareVentures` (37), same coverage | 34,560 | 0 match |
| 13 | Targeted stylistic candidates: 3 favoured piece-1 orderings x `AndreessenHorowitz` x piece 3 as `Hexagon`/`2111011` in 4 cases x 4 piece-4 words | 48 | 0 match |
| 14 | Broad piece-2 sweep at the forced length: 137 curated 18-character piece-2 candidates (investor spellings and cases, Forbes-headline phrases, spelled-out date forms, whale readings, the round's figure, named people) x 144 geometry-derived piece-1 strings x piece 3 as `2111011`/`Hexagon` in 4 cases x 9 piece-4 words | 710,208 | 0 match |
| 15 | Piece 1 as six bare hex colour codes (36 chars: 12 geometry orders x 2 cases x 4 blank-flag values) with piece 2 = the date exactly as drawn, 7 separator forms of 16-03-2020 (10 chars), x piece 3 as `2111011`/`Hexagon` x all 120 letter orders of ALIEN in 3 cases | 241,920 | 0 match |
| 16 | Piece 1 as six `#`-prefixed hex codes (42 chars, same variant set) with piece 2 = `a16z` in 4 cases (4 chars), same piece-3 and piece-4 coverage | 138,240 | 0 match |
| 17 | Joint-naming model: the four clues as words in one 58-character string rather than four concatenated sub-answers. Every ordered concatenation of the clue-implied vocabulary (38 tokens: blue, whale, hexagon, alien, the scientific name, the three investors, the Forbes headline terms, date forms) totalling exactly 58 characters, plus case variants of the 240 that contain all four clue words | 516,138 | 0 match |
| 18 | Piece 4 as a tincture sequence (20 initials) instead of five letters, reopening the algebra to p1 + p2 = 31: 576 tincture strings (6 square orders x 24 quadrant orders x colour/heraldic initials x case) against the four pairings that close the budget -- 28+3 (`USV`), 12+19 (`UnionSquareVentures`), 13+18 (`AndreessenHorowitz`), 11+20 | 414,720 | 0 match |
| 19 | Piece 4 ordered by hatch-line count (`LEINA`/`ANIEL` and cases) x 144 piece-1 strings x 4 `AndreessenHorowitz` variants x 4 piece-3 forms | 13,824 | 0 match |

## Notes on rows 7 and 8 (2026-08-18)

Method: a fast-reject front end to the certified oracle. The `"kty":"RSA"` gate lies
wholly inside plaintext block 0, so only the first ciphertext block is decrypted;
this takes the rate from 2.04 to 40.3 candidates/second/core, and 203/second measured
across 10 cores (the figure used for both rows). Any hit would have been re-checked
through the unmodified `tools/oracle.py` before being believed; there were none.

Witness: the fast path was certified before the runs by re-finding sibling #8's
published answer `RasputinWilhelmAlekhine` through the same code, and by rejecting a
truncated near miss, a case flip, and #8's answer against #12's own ciphertext. As with
rows 1-6, neither run carries a witness *inside its own candidate space*, because no
known-good #12 answer exists to plant. Call these certified-oracle, uncertified-space
negatives.

**Scope limit that applies to rows 7 and 8 only.** The fast path requires plaintext
block 0 to *begin* with `{"kty":"RSA"`, whereas `tools/oracle.py` accepts the gate
substring anywhere in the plaintext. Sibling #8's keyfile does begin at offset 0 (checked
byte-for-byte), and the same generator produced #12, so the assumption is well founded --
but it is an assumption. A candidate whose plaintext carried the gate at a non-zero
offset would have been missed by these two rows and by no earlier row.

Also refuted, not a candidate sweep: steganography in the jigsaw JPEG and the page's
favicon (no EXIF or XMP metadata, 0 trailing bytes after the JPEG end marker, `zsteg -a`
returns noise only, the favicon's alpha channel is ordinary anti-aliasing). The author's
full transaction history was paged to exhaustion; the only asset near the funding or
publication window is a PNG image byte-identical to sibling puzzle #11's, not a hint
specific to #12.

## Structural findings, 2026-08-18 (second pass)

**Piece 1's reading order is now derived from the image, not guessed.** The six flag
centroids were measured in the published raster: gray `808080` (257,213), violet
`7f00ff` (400,282), red `c00000` (97,304), green `3f8000` (295,356), blank `ffffff`
(410,414), purple `410080` (110,510). Grouping by x gives exactly three vertical pairs --
left (red, purple), middle (gray, green), right (violet, blank) -- which confirms the
community's "they go in pairs" note as a measurement rather than an impression. Twelve
principled reading orders (column-major and row-major, each in four directions, plus
tops-then-bottoms) replace the 720 arbitrary permutations, cutting the piece-1 space from
4,320 strings to 144 with no loss of any ordering that has a reason behind it. Rows 9 to
13 use that set. Note also that both purple-family flags are now allowed to take the
*same* name; an earlier pass wrongly forced them to differ.

**Piece 4 is exactly five letters.** Five hatched squares, all 88-89 pixels square, and
five orange glyphs, stable across thresholds from <100 to <160. The sixth square-like
contour that appears at looser thresholds is a puzzle-knob shadow at 69x65, a different
size. The community's six-letter-word hypothesis (alpine, saline, linear) is refuted:
there is no sixth letter to find.

**Hatching, measured.** Dominant hatch direction per quadrant, by Hough transform:
E (hori, diagBS, diagBS, vert), I (diagFS, hori, hori, diagFS), A (diagBS, vert, hori,
diagBS), L (vert, diagFS, diagBS, hori), N (vert, diagFS, diagFS, hori). The count of
*distinct* directions per square is 3,2,3,4,3, which is not a permutation of 1 to 5. This
is an independent confirmation of row 1's refutation, arrived at by measurement rather
than by enumeration.

**Piece 4 was enumerated over all 120 letter orders, not just dictionary words** (rows 10
to 12). The intended order need not be an English word, and only the five dictionary
anagrams had been tried before.

**Correction to an assumption about the author's style.** Sibling #8's answer
(`RasputinWilhelmAlekhine`) suggests concatenated proper nouns, and an earlier note here
leaned on that. Sibling #5's confirmed sub-answers are `*`, `48`, `GCE` and `Eris` -- a
literal symbol, a bare number, an acronym and a name. Digit strings such as `2111011` are
therefore fully in this author's range, and so are acronyms; piece 2 need not be a proper
noun at all. Puzzle #3's answers are four-character tokens including chess moves
(`e4d5`). Any future piece-2 search should not be restricted to names.

**Length algebra.** With piece 3 at 7 and piece 4 at 5, piece 1 + piece 2 = 46. The
investor names from the Forbes article of the drawn date concatenate to lengths that
close the budget at several piece-1 lengths: 28+18 (`AndreessenHorowitz`), 12+34
(`AndreessenHorowitz`+`CoinbaseVentures`), 11+35 (`UnionSquareVentures`+`CoinbaseVentures`)
and 9+37 (`AndreessenHorowitz`+`UnionSquareVentures`). Rows 9 to 12 cover all four. The
28+18 split is the only one where a single investor name closes the budget alone, which
is why it has attracted every solver, but it is now dead across all 24 block orders and
all 144 geometry-derived piece-1 orderings.

## Assumption audit on piece 1, 2026-08-18

Every negative in this folder assumes piece 1 resolves to a string built from the flags.
This audit enumerates the possible encodings, prices each against the length budget, and
records which are eliminated by measurement rather than by sweeping.

**The flag attributes are scaffolding, not payload.** The three binary attributes were
measured: a ball at the pole top on violet, red and green and none on gray, purple and
blank; the flag to the left of the pole on gray, red and blank and to the right on
violet, green and purple. All three pairs oppose on both attributes. Because the blank
flag's attributes are therefore *fully determined* by its partner, they carry no
information about it -- they exist to establish the pairing. Reading the eighteen
attribute bits as the answer (which would be 18 characters, pairing with a 28-character
piece 2) is refuted on that principle, without a sweep.

This also strengthens Blue independently of the length budget: the pairs are
(red, purple), (gray, green), (violet, blank), and exactly one additive primary sits in
each of the first two, so the blank completes R/G/B.

**Encodings, priced against p1 + p2 = 46:**

| encoding of piece 1 | len | forced len(p2) | status |
|---|---|---|---|
| six colour names | 28 | 18 | `AndreessenHorowitz`; dead, rows 9 and 14 |
| three primary names | 12 | 34 | AH+CoinbaseVentures; dead, row 10 |
| six bare hex codes | 36 | 10 | the date as drawn; dead, row 15 |
| six `#`-prefixed hex codes | 42 | 4 | `a16z`; dead, row 16 |
| eighteen attribute bits | 18 | 28 | refuted on principle, see above |
| six RGB decimal triples | 54 | -8 | eliminated by length |
| one colour name (`Blue`) | 4 | 42 | untested: no plausible 42-character piece 2 exists |
| one-letter abbreviations | 6 | 40 | untested: no plausible 40-character piece 2 exists |

**What the audit concludes.** Piece 1 as a colour-derived string is now dead in every
encoding whose length pairs with a piece-2 reading that has any support in the source
material. The two encodings still untested are untested precisely because nothing
plausible sits at the length they force. The binding constraint is the coupling
p1 + p2 = 46, and every pair that closes it exactly has been swept.

That is a reason to doubt the concatenation model itself rather than to keep varying
piece 1. The community's own README raises the alternative -- that the four pieces may
jointly indicate a single answer rather than concatenating -- and no negative in this
folder tests it, because all of them assume concatenation.

## Joint-naming reasoning, 2026-08-19

**Flag semaphore is refuted.** Pole angles from vertical measure -26.5, 7.7, 17.1, -9.5,
0.2 and 0.2 degrees. Semaphore requires multiples of 45; the largest deviation is 18.5
degrees. The pole angles are decorative, not a code.

**Piece 4's hatching is the Petra Sancta heraldic convention.** This appears to be new.
Each square is quartered and each quadrant carries parallel hatching in one of four
directions, which is the standard monochrome notation for heraldic tinctures: vertical =
gules (red), horizontal = azure (blue), diagonal from top-left = vert (green), diagonal
from top-right = purpure (purple). Measured with the orange glyph masked out:

| letter | TL | TR | BL | BR |
|---|---|---|---|---|
| E | azure | vert | vert | gules |
| I | purpure | azure | azure | purpure |
| A | vert | gules | azure | vert |
| L | gules | purpure | vert | azure |
| N | gules | purpure | purpure | azure |

That the hatching is a *colour* notation matters, because piece 1 is also about colour:
two of the four clues speak the same language. It also explains why the hatching is drawn
so carefully in four directions rather than arbitrarily.

**But the tinctures do not order the letters.** Tested exhaustively: no single quadrant
gives a bijection from the five letters to distinct colours (best is 4 distinct of 5); no
per-colour count across the five letters is a permutation of 1 to 5; and reading each
letter's four quadrants as a base-4 number under all 24 colour-to-digit assignments never
yields five consecutive values. This extends row 1's refutation rather than overturning
it: hatching is not an ordering scheme under the directional reading *or* the heraldic
one.

**The colour-reading algebra is now exhausted.** With piece 3 at 7 and piece 4 at 5, both
verified, piece 1 + piece 2 = 46. Every colour-derived piece 1 has been swept except one:

| piece 1 | len | forces piece 2 | status |
|---|---|---|---|
| six colour names | 28 | 18 | dead, rows 9 and 14 |
| three primary names | 12 | 34 | dead, row 10 |
| six bare hex codes | 36 | 10 | dead, row 15 |
| six #-prefixed codes | 42 | 4 | dead, row 16 |
| `Blue` alone, the IQ-test answer | 4 | 42 | the only survivor |

**On the 42-character survivor.** An Ethereum address is exactly 42 characters, and its
EIP-55 checksum is mixed-case, which would give a reason for the author's emphasis on
"58 chars CS". "Whale" is crypto slang for a large holder and a date would identify which
one. The fit is attractive and it is recorded here so nobody re-derives it -- but it
should be treated as refuted rather than open, for a factual reason: the $8.3 million
round that the drawn date points at was a private equity round, not an on-chain transfer.
There is no Arweave-related whale address associated with 16-03-2020 to find. A bech32
Bitcoin address is also 42 characters but is lowercase-only, so it cannot be what the
case-sensitivity emphasis is about.

**What is left.** Piece 3 = 7 is certain and piece 4 = 5 is measured, so if piece 1 is
colour-derived the algebra has no remaining room. Either piece 4's answer is not the five
letters -- the heraldic reading opens this, since a tincture sequence would be a different
length -- or one of the two "certain" pieces is not what it appears. Those are the two
places left to look.

## The tincture reading, worked out (2026-08-19)

**The measurement is verified.** Square I was re-read at 6x magnification and matches the
automated reading exactly: TL and BR hatched from top-right (purpure), TR and BL
horizontal (azure). The tincture table in the previous section can be relied on.

**Decodings tested and failed:**

- *Two bits per quadrant, one byte per square.* Four quadrants x 2 bits is exactly 8 bits,
  so five squares would give five ASCII characters. All 24 tincture-to-value assignments x
  24 quadrant orders x both bit orders (1,152 combinations): not one produces five
  alphanumeric bytes.
- *Forty bits as eight five-bit letters.* 1,782 distinct 8-letter strings arise across all
  assignments and orders; checked against the 29,853 eight-letter words in
  `/usr/share/dict/words`, **none is a word**.
- *The 20 initials as a literal sub-answer* (row 18). This is the reading that reopens the
  length algebra, since 58 - 7 - 20 = 31 admits four pairings including
  `RedGreenBlue` + `UnionSquareVentures` and a 13-character piece 1 with
  `AndreessenHorowitz`. All four swept, 0 match.

**A retraction.** Summing hatch lines per square by threshold profile gave 13, 14, 15, 16
and 17 -- five consecutive integers, which would have ranked the letters L, E, I, N, A.
That did not survive independent measurement. Counting the same lines as connected
components gives 12, 12, 11, 7, 11, and counting dark runs along a perpendicular scanline
gives 7, 15, 11, 13, 6. Three methods, no agreement. **The hatch-line count is not
reliably measurable at this resolution and the consecutive-integer pattern was an artifact
of one thresholding choice.** The ordering it suggested was tested anyway (row 19) and
fails. Anyone tempted by a count-based ordering here should measure it at least twice
before building on it.

**Where the tincture reading leaves things.** The heraldic identification stands as a
reading of the notation -- the hatching is a recognised colour convention, not decoration,
and it is drawn correctly in four distinct directions. But every decoding of it tested so
far, as bytes, as letters, and as a literal 20-character sub-answer, is negative. The
hatching still has no demonstrated role in the answer, under the directional reading
(row 1), the heraldic reading, or the count reading.

Cumulative: 3,014,356 assembled 58-character candidates tested against the escrow, 0
matches. 3 of the 4 sub-answers have a strong-to-certain reading; the gap is piece 2's
exact 18-character string.


## Dated transfer-address readings, 2026-09-05 (contributed by @BorisLoveDev, PR #21)

These three runs use the exact-address checker from PR #20, supplied with #12's
ciphertext and escrow address and with lowercase=False. The original-page fixture
and solved #8 vector pass before generation. These checks are separate from the
historical RSA-substring gate described above.

| ID | Construction | Unique candidates / stream records | Witness positions expected and found | Result | Rate and runtime |
|---|---|---|---|---|---|
| W1 | A four-character color word in three cases, two public USDT transfer addresses in three case forms including 0x, geometry digits, a five-letter reading in three cases, two block orders | 108 / 111 | [0,55,77,110] | Exhausted, no exact target match | 1.7696 records/s; estimate 62.726 s; actual 63.700 s |
| W2 | Same construction with sender/recipient from the dated HUSD emissions | 108 / 111 | [0,55,77,110] | Exhausted, no exact target match | 1.7811 records/s; estimate 62.320 s; actual 63.144 s |
| Q1 | Six proposed RGB/base64 sequences, the same USDT addresses without 0x in three cases, geometry digits, the five-letter reading in three cases, two block orders | 216 / 219 | [0,109,152,218] | Exhausted, no exact target match | 1.7791 records/s; estimate 123.096 s; actual 126.339 s |

All 432 candidate strings are distinct and exactly 58 characters. The expected
control is a candidate encrypted into a separate ciphertext by the original
JavaScript; it is recovered at its natural position plus head/middle/tail inserts.
The exact input lists remain private and are fingerprinted in the
[reports](../tools/REPRODUCE.md). These results exclude only those lists.

The USDT transaction receipt and block confirm 2020-03-16 12:03:36 UTC, block 9682464.
The HUSD receipts confirm 2020-03-16 02:49:29 UTC, block 0x93b482. These are public
operations matching the drawn date; no evidence establishes that either is intended.
The RGB/base64 reading also remains a hypothesis. No target match was obtained.

Primary posts: [USDT](https://x.com/whale_alert/status/1239522831525961729),
[HUSD emission one](https://x.com/whale_alert/status/1239383378400546817),
[HUSD emission two](https://x.com/whale_alert/status/1239383375674314753).
Recorded funding on 2026-09-05 00:12:55 UTC: 400.00248121 AR, no outgoing transactions.
