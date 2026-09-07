# Negatives ledger, Arweave Puzzle #3

## Historical claims: uncertified

The following rows were inherited from the 2026-06-22 notes. They lack per-run planted
witnesses and exact candidate lists. A separate solved-sibling self-test does not certify
these searches. Counts and labels are preserved as reported, not independently verified.
For example, `36^4` is 1,679,616, and `8^8` enumerates tuples with repetition rather than
permutations (`8!`). The historical total therefore remains approximate.

| # | Configuration | Candidates | Result |
|---|---|---|---|
| B1 | Top-12 uncertain readings, hedged anchors | 332,000 | 0 match |
| B2 | Free-slot diagnostic: each of the 8 slots freed alone over `[a-z0-9]^4`, other 7 at top-1 reading | 8 x 1,680,000 = 13,440,000 | 0 match in all 8 runs |
| B3 | Free slot 1, with contested anchors (slot 5 = a year, slot 7 = a different word, slot 8 = a literal count) | 1,680,000 | 0 match |
| B4 | Free slots 1, 2, 8 with an extended charset (symbols and digits added) | 2,080,000 | 0 match |
| B5 | 4 anchors locked, 4 uncertain slots swept with complete wordlists | 1,800,000 | 0 match |
| B6 | One anchor (slot 3, 5, 7, or 8) relaxed at a time over a full list, the other 7 locked | approximately 25,000,000 to 31,000,000 each, 4 configurations | 0 match |
| B7 | All 8 slots, top-8 candidates each (early wordlists) | 16,700,000 | 0 match |
| B8 | Word-order permutations of one 8-word set (the original best-guess reading) | 8^8 = 16,777,216 | 0 match |
| B9 | Word-order permutations of a second 8-word set (revised reading) | 8^8 = 16,777,216 | 0 match |
| B10 | 2 anchors locked, 6 uncertain slots swept with enriched wordlists (round 2) | 2,270,000 | 0 match |
| B11 | All 8 slots, top-6 candidates each (consolidated wordlists) | 1,680,000 | 0 match |
| B12 | All 8 slots, top-8 candidates each (consolidated wordlists) | 16,700,000 | 0 match |
| B13 | All 8 slots, top-10 candidates each (consolidated wordlists) | 100,000,000 | 0 match |
| B14 | Grammar-filtered top-4 reading (proper-noun-style additions) | 65,000 | 0 match |
| B15 | Word-order permutations of a third 8-word set (grammar-filtered reading) | 8^8 = 16,777,216 | 0 match |
| B16 | Word-order permutations of the same set, alternate tie-break | 8^8 = 16,777,216 | 0 match |

Historical observation, not a candidate sweep: forensic steganalysis of all 8 rebus images and the
page itself (exiftool, binwalk, `zsteg -a`) found no LSB payload, no appended bytes, no
metadata payload, and no discrepancy in the alpha channel. This does not prove that every possible hiding method is absent.

Previously deprioritized: Norse mythology as a reading for slot 5 (checked against the Discord export's
683 messages from the author; every apparent reference is to a project codename, not
mythology). Previously deprioritized: `sha3`/Keccak as a reading for slot 3 (the drawn glyph and the
author's own hash-size discussion point to SHA-384, not SHA-3). Also refuted: Base58 as
Arweave's own on-chain address encoding (Arweave addresses use base64url; a "Base58" OTC
trading desk that was active in the author's Discord in early 2019 remains a candidate
source for that slot's 4-character token).

Historical claimed total: on the order of 330,000,000 candidates. These rows do not
prove that at least two readings are wrong. The 2026-09-05 audit also fixed the oracle
to require exact target-address equality; see the regression tests and source review.


## Witnessed runs, 2026-09-05 (contributed by @BorisLoveDev, PR #20)

| ID | Constraint | Unique candidates | Stream elements | Method and witness | Result | Runtime |
|---|---|---|---|---|---|---|
| H1 | ArweaveID first-image reading; pool sizes 1×4×1×2×4×2×3×2 | 384 | 387 | Exact-address Python oracle; original-page JS encrypted control; expected/observed positions [0,193,302,386] | Exhausted, no target match | 225.966 s |

Measured rate 1.7498 stream elements/s; estimate 221.168 s; RNG seed 20260905.
Parameters, command, hashes and coverage limits are in [REPRODUCE.md](../tools/REPRODUCE.md)
and [source-review.md](source-review.md). Historical overlap cannot be measured because
B1-B16 did not preserve their candidate lists.

### Further finite readings

| ID | Constraint | Unique candidates | Stream elements | Method and witness | Result | Runtime |
|---|---|---|---|---|---|---|
| H2 | Literal unpadded count, optional short geographic abbreviation; slot sizes 4x2x1x1x2x2x2x1; lengths 29/30 | 64 | 67 | Same exact-address checker and original-page fixture; expected/observed [0,33,36,66] | Exhausted, no target match | 39.065 s |
| H3 | Literal ribbon letters and HA+SH rebus, two readings per slot | 256 | 259 | Same checker and fixture; expected/observed [0,129,140,258] | Exhausted, no target match | 151.615 s |
| H4 | Literal ribbon letters, year notation, contemporary geographic/mining/service readings; sizes 4x4x2x2x2x2x2x1 | 512 | 515 | Same checker and fixture; expected/observed [0,257,278,514] | Exhausted, no target match | 298.870 s |

Rates were 1.7216, 1.7451 and 1.7206 stream elements/s; pre-run estimates were
38.918, 148.418 and 299.321 seconds. H1-H4 contain 1,216 mutually disjoint candidates.
Each stream also contains three planted copies of a candidate encrypted into a
separate control ciphertext; the fourth control hit is its natural occurrence.
These are finite reading tests, not exhaustive statements about the drawings.

The original `proceed()` accepts empty input cells and concatenates them without
padding. A 28-character synthetic answer with four empty cells passed the original
form and Python checker; replacing empty cells with spaces failed. This establishes
form behavior, not the intended length of the author's answer. The optional
`--allow-short-slots` flag covers H2; four-character slots remain the default.

Per-run reports: [H2](h2-result.json), [H3](h3-result.json), [H4](h4-result.json).
The exact readings remain outside Git, as for H1. The reports preserve their input
fingerprints, counts, rates and observed controls; a public checkout alone cannot
reconstruct those exact private input files. No solution is claimed.
