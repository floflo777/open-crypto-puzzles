# Zden Cryptopuzzle LVL.5 (555,550 sats, [DEAD END])

**Swept on 2026-09-22.** The escrow `1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7` was emptied in block 968,171 by
[transaction e2544433](https://mempool.space/tx/e2544433184d0fe4157ca10a8e1ce753bb52a7b0bbcf833740d7448ed25e8e8e),
551,745 sats to `bc1qw50q83k7psugw5z5548kwnxqqjxjxvx2pkvz0s`, a plain spend with no message,
reported in [issue #34](https://github.com/floflo777/open-crypto-puzzles/issues/34) by deviceio121.
Nobody has published the key or the reading of the hint as of 2026-09-26. The research below is
kept as it stood; if the solver reads this, an issue with the derivation gets full credit here.

## At a glance

| | |
|---|---|
| Author | Zden (Zdenek Haluska), [crypto.haluska.sk](https://crypto.haluska.sk/), [@Zd3N on X](https://twitter.com/Zd3N) |
| Published | 2018-11-09 (original image); corrected 2021-12-12 ([tweet](https://twitter.com/Zd3N/status/1060955171591766018)) |
| Prize | 555,550 sats (about $350 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7` ([explorer](https://mempool.space/address/1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7)) |
| Last on-chain check | 2026-08-16: funded and unspent (555,550 sats, across 4 funding transactions from 2018-10-20 to 2021-12-03) |
| Status | OPEN |
| Puzzle type | geometry, raw-private-key |
| Target format | a 256-bit private key as direct hex (not WIF, not BIP39), P2PKH |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against a standard public vector, private key 1; the puzzle's own rectangle-to-key reading is not certified, see below) |
| What remains | the exact meaning of 3 terms in the author's own published hint |
| Series | Zden's crypto.haluska.sk puzzle series (LTC, Codex, Demobit, Janus, HALV and others) |

## Why this is a dead end

The prize is gone: the only escrow of this puzzle was swept by an unknown party on 2026-09-22,
almost 8 years after publication, and no solution has been published. The geometry, the oracle
and the 545 million negatives remain valid material for whoever wants to reconstruct the key
from the public solution once it appears.


Zden (Zdenek Haluska), author of a series of algorithmic crypto puzzles at
crypto.haluska.sk, published LVL.5 in November 2018: a single image of 64 rectangles
arranged in an 8x8 grid, with the private key to a funded Bitcoin address encoded in their
shapes. He issued a hint the following month and a corrected version of the image in
December 2021, after 3 years unsolved. I measured the rectangle geometry and certified it
byte-perfect against the author's own published script; I read the hint's formula at the
pixel level. I have tried over 545 million candidate keys built from more than 3,200 distinct
readings of that formula, with zero matches. What is missing is not more computation: it is
the exact meaning of 3 terms in the author's own hint that nothing published so far pins
down.

## The puzzle as published

The puzzle is a single published image, `crypto5.png`, announced 2018-11-09 with the caption
"Level 5 - Find the private key in this image." A hint bundle followed on 2018-12-24: "Sum of
two consecutive following rectangles areas creates one byte of the private key. Apply more
operations to obtain the results in byte range." On 2021-12-12, after the puzzle had gone 3
years unsolved, the author republished the image as `crypto5fix.png` with the note "the
original release was uncomplete," struck out the word "consecutive" from the hint, and added
2 short white pixel lines plus a small 4-line pixel formula in the image's bottom-left
corner. No rectangle geometry changed between the two versions. Full quotes with links are in
[clues/author-posts.md](clues/author-posts.md).

## What is understood

### Mechanism

The image shows 64 rectangles in row-major 8x8 order. Each exposes 3 measurable quantities:
outer area (width times height), inner area (the area inside its border), and the shell (the
difference between the two). The hint states that the sum of 2 "following" rectangles' areas,
after an unspecified operation, forms 1 byte of the private key: 32 such bytes make the
256-bit key. The author's own MATLAB measurement script (in the community repository, see
Sources) defines 4 candidate spatial senses of "following" (simple consecutive order,
column blocks, column-major pairs, and interleaved columns). The 2021 pixel hint reads, once
corrected for an earlier transcription error, as "-1 times x plus 64 divided by x," where "x"
most likely refers to a per-rectangle border-thickness measurement, though this binding is
not confirmed by the author. The key is understood to be direct hex, not a WIF or BIP39
encoding: a base58/WIF character-stream reading was tried and never produces a valid checksum
(see [analysis/tested.md](analysis/tested.md)).

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<64 hex chars>"
```

`MATCH <address> (<compressed|uncompressed>)` on a hit, `NO MATCH` otherwise, exit 0 or 1.
This oracle checks a finished 32-byte key candidate against the escrow; it does not implement
the still-open rectangle-to-key reading itself.

### Certified against

`tools/oracle.py --selftest` reproduces the address for private key 1 (the generator point),
a standard vector reproduced in Bitcoin educational material, unrelated to this puzzle. This
certifies the derivation pipeline (secp256k1, hash160, base58check) used by the oracle. The
rectangle geometry is separately certified: my measurements reproduce the author's own
published MATLAB script output on all 64 rectangles, exactly.

### Established facts

1. I confirmed the escrow is funded and unspent as of 2026-08-16 (checked via
   [mempool.space](https://mempool.space)), across 4 funding transactions from 2018-10-20 to
   2021-12-03.
2. My rectangle measurements (`data/rectangle-measurements.csv`) reproduce the author's own
   canonical output exactly, on all 64 rectangles, by 2 independent measurement methods.
3. The 2018 and 2021 images are pixel-identical except for 2 short white lines and the
   bottom-left mini-hint; no rectangle geometry changed.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Volume | Result |
|---|---|---|
| Mini-hint formula bound to every channel, pairing and normalization | over 3,200 families | 0 match |
| Composed operations, offsets, 2-stage divide-and-modulo | about 3,000 keys | 0 match |
| Base/radix readings, nibble model, date-matrix reading | thousands of keys | 0 match |
| 1-byte author-error tolerance across 2,699 bases | about 155 million derivations | 0 match |
| 2-byte author-error tolerance across 12 bases | about 390 million derivations | 0 match |
| Raw sum over a constant divisor, 6 traversal orders | 212,406 configurations | 0 match |
| "Following" as a sorted-order neighbor | 153,736 unique keys | 0 match |

All of the above predate this folder's certified oracle; every row is reported as candidates
consumed, not as a witnessed negative in this project's strict sense.

## Open leads, ranked

1. **A clarification from the author on 3 exact bindings** (needs a person). What "x" means
   in the formula, the exact byte-range normalization, and the exact sense of "following."
   Full details in [analysis/leads.md](analysis/leads.md).
2. **A higher-fidelity source for the mini-hint glyphs** (needs new information).
3. **A wider author-error tolerance sweep** (bounded, low priority). About 660 million
   derivations per base tried, marginal expected value against lead 1.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/crypto5.png` | the original 2018 puzzle image, byte-exact |
| `clues/crypto5fix.png` | the corrected 2021 puzzle image, byte-exact |
| `clues/author-posts.md` | dated quotes from the announcement, hint bundle, and 2021 correction, with links |
| `data/rectangle-measurements.csv` | width, height, outer area, inner area and shell for all 64 rectangles |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 3 ranked leads |
| `tools/oracle.py` | candidate checker, certified against a standard public vector |

## Sources

- Zden, original announcement, X, 2018-11-09: https://twitter.com/Zd3N/status/1060955171591766018
- Zden, Christmas hint bundle, X, 2018-12-24: https://twitter.com/Zd3N/status/1077146640090316800
- Zden's puzzle site: https://crypto.haluska.sk/
- Community documentation and the author's own measurement script: https://github.com/HomelessPhD/Zden_LVL5
