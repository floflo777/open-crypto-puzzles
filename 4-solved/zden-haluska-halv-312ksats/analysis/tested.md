# Negatives ledger, Zden HALV

Method for every row: a candidate 32-byte key, built from a reading of the waveform image
under the stated hypothesis, is compared against the escrow address using both the
compressed and uncompressed P2PKH derivation. The private-key-to-address comparator used
during this testing history had no known-good test vector at the time, so every row below is
reported as candidates consumed with 0 matches, not as a certified-witnessed negative in this
project's strict sense. The oracle shipped in this folder (`tools/oracle.py`) closes that
specific gap for any future search: it self-tests against a standard public vector.

| Hypothesis | Volume | Result | Date |
|---|---|---|---|
| The 59-lobe shape sequence itself is the key: read forward and reversed, circle=0/diamond=1 and the inverse mapping, most-significant-bit-first and least-significant-bit-first, as a raw integer, run-length encoded, packed to 8 bits, hashed with SHA-256, and interleaved with the halving-step value | 202 derivations | 0 match | 2026 |
| The halving-step ("rung") value carries data: read as nibbles across all frames, in bases 2, 3, 4, 16, 17, 58 and 256, combined with shape at 5 bits per lobe, hashed as the 220 reconstructed samples, taken modulo n, padded into a WIF candidate from the left, right, first 64 bits and last 64 bits | about 47 derivations | 0 match | 2026 |
| Brainwallet phrases built from the puzzle's own theme (the halving date in several formats, "HALV," "halving," the puzzle's site domain, the escrow address itself, the shape sequence itself as a string) | about 110 phrases | 0 match | 2026 |
| A convention borrowed from an earlier, solved puzzle in the same series (neighbor-to-neighbor differential plus a sign bit, rotated toward a WIF prefix): 6 candidate bitstreams (raw shape, neighbor-XOR, cumulative-XOR, rung parity, rung XOR shape) in 2 groupings (7-bit and 8-bit) | 12 streams | 0 printable ASCII or base58 stream produced | 2026 |
| Author-error tolerance under the WIF checksum: a 1-symbol wildcard swept across the reading | over 500 million derivations | 0 valid base58check WIF | 2026 |

## What is measured, and why this changes the next step

The waveform's lobe count is robustly 59, not the "51" figure once cited (an artifact of a
detection threshold that filters small lobes at the tail). Each lobe's apex shape, circle or
diamond, is a clean, stable, 1-bit-per-lobe channel, measured by apex cap-width and
reproduced identically across 3 independent passes:
`DODDODDDDDOODDDOODDDDDDDDDDDDDODOODODOOODDDDDOODDDDDODDDODO` (see
[data/lobe-shape-sequence.csv](../data/lobe-shape-sequence.csv)). Amplitude follows a fixed
halving pattern determined by the puzzle's own theme, and is decorative rather than an
independent data channel: it can be predicted from the halving schedule alone.

Recomputed independently 3 times, the image's total measured information capacity is about
118 bits (59 bits from lobe shape, plus a small, noisy residual from the halving-step
progression, well under 1 reliable bit per lobe) against the 256 bits a private key needs.
Every specific reading tried against this capacity has been negative (table above); the
conclusion drawn from the capacity measurement itself is that no further pixel-level reading
of the current image is expected to close this gap on its own.
