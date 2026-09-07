# Arweave Puzzle #3 (1000.165838006237 AR, [OPEN])

Tiamat (@ArweaveP), an Arweave community member and application developer, published
this puzzle on 2019-05-27. Eight hand-drawn rebuses supply four characters each to a
client-side decryptor. The prize wallet remains funded with 1000.165838006237 AR
(balance and outgoing-transaction query checked 2026-09-04 UTC).

I reproduced the decryptor and now require the recovered wallet address to equal the
published escrow. The earlier oracle accepted any parseable RSA wallet; a known-good
sibling wallet now also serves as a wrong-target regression test. Historical search rows
lack planted witnesses, so they do not prove how many image readings are wrong.
The puzzle remains unsolved. See [source review](analysis/source-review.md).

## At a glance

| | |
|---|---|
| Author | Tiamat, [@ArweaveP on Twitter](https://twitter.com/arweavep) |
| Published | 2019-05-27, Twitter ([announcement](https://twitter.com/arweavep/status/1132936723162378240)) |
| Prize | 1000.165838006237 AR (about $1,810 at AR = $1.81, 2026-08-16) |
| Chain | arweave |
| Escrow | `wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0` ([explorer](https://viewblock.io/arweave/address/wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0)) |
| Last on-chain check | 2026-09-04 UTC: balance 1000165838006237 winston; outgoing query returned no transactions |
| Status | OPEN |
| Puzzle type | word-selection, text-cipher |
| Target format | 8 four-character rebus answers, concatenated and lowercased, SHA-512 x11513, AES-decrypt to an Arweave JWK keyfile |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against solved sibling Arweave Puzzle Weave #8) |
| What remains | identify a complete eight-slot reading; the number of incorrect slots is unknown |
| Series | Arweave Puzzles (this folder covers puzzle #3 only) |

## The puzzle as published

The live page (still up on the permaweb) shows one composite drawing split into 8 rebus
regions and 32 single-character input boxes grouped 4 at a time, one group per region.
Typing an answer into each group, concatenating in DOM order and lowercasing, and
clicking "proceed" runs the decrypt routine against the page's embedded ciphertext. The
author's only two per-image hints, both from his own tweet history: on the eighth image,
["Did anybody count the dots?"](https://twitter.com/arweavep/status/1152887601529073665)
(2019-07-21); on the third image,
["With N.1.7.0.0 release, third pic became obsolete"](https://twitter.com/arweavep/status/1177235139035836417)
(2019-09-26), a reference to an Arweave software release that replaced one mining
algorithm with another. On 2020-03-04 he
[ranked the series by difficulty](https://twitter.com/arweavep/status/1235199397371277315)
as "3, 9, 8, 5, 7", placing #3 first, meaning hardest.

## What is understood

### Mechanism

The page concatenates the 8 typed answers in DOM order, lowercases the result, stretches
it with SHA-512 applied 11,513 times, and uses the resulting 128-character hex digest as
an EvpKDF/AES-OpenSSL password to decrypt an embedded ciphertext. Success is declared
by the original page if the decrypted plaintext contains the literal marker `"kty":"RSA"`.
My oracle additionally parses the JSON, derives the modulus address and requires exact
equality with the escrow. The marker alone is not proof of a solution.
This CryptoJS bundle carries a documented
library quirk (crypto-js issue #293): overriding the AES key size to 32 words turns the
cipher into a non-standard 1024-bit-key, 38-round Rijndael variant rather than textbook
AES-256. Earlier forensic notes report no payload from exiftool, binwalk and `zsteg -a`.
That observation does not exclude every possible steganographic mechanism.

### Derivation and oracle

```
python3 tools/oracle.py --selftest       # reproduces the solved sibling Arweave #8
python3 tools/oracle.py --stdin          # one candidate per line
```

A candidate is the eight answers concatenated in image order with **no inserted spaces**
(lowercased automatically). Spaces are significant input characters and are not trimmed. `MATCH <address>`
on a hit. Single-candidate mode prints `NO MATCH` otherwise; stdin mode prints hits only. Since no dependency available to this repository
implements CryptoJS's non-standard Rijndael variant, the oracle reimplements it in pure
Python; the implementation was checked to reproduce a standard AES-256 library exactly at
the standard key size before being trusted at this puzzle's non-standard one.

### Certified against

`tools/oracle.py --selftest` decrypts the real ciphertext of the solved sibling Arweave
Puzzle Weave #8 with its published answer, `RasputinWilhelmAlekhine`, and recovers a JWK
whose derived address matches `ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4` exactly, the
address baked into that puzzle's own success page. Puzzle #8's escrow is already spent
(checked 2026-08-16), so this is historical calibration data, not a live prize. The
oracle's raw decrypt output was also checked byte-for-byte against this puzzle's own
JavaScript decryptor running under Node, on both matching and non-matching passphrases.

### Established facts

1. The escrow is funded and unspent: 1000.165838006237 AR, checked via
   `arweave.net/wallet/<address>/balance` on 2026-09-04 UTC.
2. The decrypt mechanism is reproduced byte-for-byte from the live page's own script.
3. Historical forensic tools reported no hidden payload; that is a limited observation.
4. Historical free-slot sweeps were not witnessed and cannot establish a lower bound on
   the number of wrong readings.
5. Solved siblings provide examples of names, notation and counts. They do not establish
   a universal grammar. Contemporary ecosystem references remain viable for #3.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Free-slot diagnostic (each of 8 slots freed alone, other 7 at best guess) | 13,440,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Curated top-N batteries under an Arweave-jargon reading (5 configurations) | 6,147,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Extended-charset and single-anchor-relaxation sweeps | approximately 102,000,000 to 126,000,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Top-8 and top-10 consolidated readings, all 8 slots | 133,400,000 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Word-order permutation sweeps, 3 different 8-word sets | 67,108,864 | certified oracle | 0 match | uncertified | 2026-06-22 |
| Forensic inspection of images and page | full file | exiftool, binwalk, zsteg -a | no payload reported by those tools | historical report | 2026-06-22 |
| H1: ArweaveID first-image reading with bounded alternatives | 384 unique, 387 stream elements | exact-address oracle | no match | original-page fixture at all four expected positions | 2026-09-05 |

Historical claim: on the order of 330,000,000 candidates, without per-run witnesses or
reproducible candidate lists. I do not count that as certified coverage.

## Open leads, ranked

1. **A sharper visual and OSINT reading of slots 1 and 7** (hours), the two most
   speculative images, plus arbitration between the leading candidates for slot 5 (a
   chess notation versus a year) and slot 8 (a service name versus a literal count).
   Use dated primary sources to check each proposed reference, alongside the solved siblings.
   Only a complete candidate matching the escrow confirms a reading. A bounded negative
   excludes its exact candidate set, not every interpretation of an image.
2. **Bounded 2-slot sweeps on the most-suspect slot pairs** (minutes once a reading is
   fixed), covering the case where exactly 2 of the current readings are wrong at once.
   Not yet run, since the readings to sweep around are still in flux.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/slot-1.png` ... `clues/slot-8.png` | the 8 official rebus images, one per answer slot, as published on the puzzle page |
| `clues/puzzle-composite.png` | the full composite drawing all 8 regions are cut from |
| `analysis/tested.md` | 16 historical configurations and one witnessed search |
| `analysis/source-review.md` | source attribution, chronology and coverage limits |
| `tools/REPRODUCE.md` | commands, source hashes and local input contract |
| `tools/oracle.py` | candidate checker: 8 answers to JWK address, certified against the solved sibling #8 |

## Sources

- Puzzle Weave 3 announcement, Twitter, 2019-05-27: https://twitter.com/arweavep/status/1132936723162378240
- Live puzzle page, Arweave permaweb: https://kszeqgxezf5quhzld4nhpasyilhxphclq2peqi5mrn7utxmqhwga.arweave.net/VLJIGuTJewofKx8ad4JYQs93nEuGnkgjrIt_Sd2QPYw
- "Did anybody count the dots?", Twitter, 2019-07-21: https://twitter.com/arweavep/status/1152887601529073665
- "With N.1.7.0.0 release, third pic became obsolete", Twitter, 2019-09-26: https://twitter.com/arweavep/status/1177235139035836417
- "The list of unsolved Arweave puzzles ordered by difficulty probably looks like: 3, 9, 8, 5, 7", Twitter, 2020-03-04: https://twitter.com/arweavep/status/1235199397371277315
- HomelessPhD/AR_Puzzles community repository, PZL3 entry: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL3
- Escrow wallet, viewblock.io: https://viewblock.io/arweave/address/wHP6OPG5GMF5dedo_CD8AAy6x8La-gfI5b5pk65Tx_0
