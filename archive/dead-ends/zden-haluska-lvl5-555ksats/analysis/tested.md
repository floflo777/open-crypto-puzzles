# Negatives ledger, Zden LVL5

Method for every row: a candidate 32-byte key, built from the 64 measured rectangles under
the stated reading rule, is compared against the escrow address using both the compressed
and uncompressed P2PKH derivation. The rectangle geometry itself is certified byte-perfect
against the author's own published measurement script (`Analysis/crack_pzl.m` in the
community repository, see Sources): my own measurements reproduce it on all 64 rectangles.
The private-key-to-address comparator used during this testing history had no known-good
test vector at the time, so every row below is reported as candidates consumed with 0
matches, not as a certified-witnessed negative in this project's strict sense. The oracle
shipped in this folder (`tools/oracle.py`) closes that specific gap for any future search:
it self-tests against a standard public vector.

| Hypothesis | Volume | Result | Date |
|---|---|---|---|
| The mini-hint formula, both readings tried ("64/x - 1" and the corrected "64/x - x"), bound to every measured channel (outer area, inner area, shell, width, height, inner width, inner height, vertical and horizontal border thickness), the 4 author-defined "following" pairings plus column-major order, and every normalization (modulo 256, floor/round/truncate, min-max, fractional scaling) | over 3,200 distinct transform families, hundreds of thousands of keys | 0 match | 2026 |
| Composed operations in both orders (transform then sum, and sum then transform), offsets and delimiters, 2-stage divide-and-modulo combinations | about 3,000 distinct keys | 0 match | 2026 |
| Base and radix readings (LXIV = 64 suggesting base 64), a nibble model, a 0-255 linear scaling, a date-matrix reading, 6 traversal orders | thousands of keys | 0 match | 2026 |
| Author-error tolerance: 1-byte wildcard across 2,699 candidate bases and 7 stream variants (reversal, endianness, +/-1 shift, rotation) | about 155 million derivations | 0 match | 2026 |
| Author-error tolerance: 2-byte wildcard across the 12 canonical bases and all 496 position pairs | about 390 million derivations | 0 match | 2026 |
| A single mis-measured rectangle: width, height, inner width, inner height, or border thickness perturbed by 1 or 2 pixels | 1,536 perturbations | 0 match | 2026 |
| Raw sum divided by a constant 2 to 600, under 4 rounding modes, 6 traversal orders including a snake order, with and without reversal | 212,406 configurations, 68,186 unique keys | 0 match | 2026 |
| "Following" read as a neighbor in a sorted order: sorted by 9 different keys, ascending and descending, 2 pairings, all channels, with and without reversal | 153,736 unique keys | 0 match | 2026 |

Cumulative: over 545 million individual key derivations across the rows above, 0 matches.

## Ruled out as data, not as a reading error

- The numeric fragments `09111819` and `11122111` from the 2018 hint bundle read as calendar
  dates (2018-11-19 and 2021-12-11) rather than key material: no transform under the current
  formula produces them at the start or end of the derived key.
- The byte `0x77`, named in the same hint bundle as "part of the private key," is not
  producible naturally from the corrected formula ("64/x - x"); a separate normalization
  (min-max scaling) could inject a value like this almost anywhere in the output, so its
  presence is not a useful filter and is treated as bundle material for one of the author's
  other puzzles, not as a byte of LVL5's own key.
- A third-party repository's claim that 2 specific shell measurements divide evenly by 7 to
  produce `0x77` and `40` does not hold against the measurements in
  [data/rectangle-measurements.csv](../data/rectangle-measurements.csv): the actual values at
  those 2 positions do not match either claimed result under any channel.
