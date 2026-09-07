# Tested (full negatives ledger)

Every row uses `tools/oracle.py`: a candidate only counts as a match if the derived P2PKH
address equals `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ` exactly, under either the BIP39 4-path
comp/uncomp reading or the old-Electrum v1 5-index 2-change reading. Witness: the oracle's own
`--selftest` reproduces the priv=1 P2PKH vectors, a public BIP39 test vector, and a public
old-Electrum v1 test vector before every run described below; a negative control confirms
neither public vector matches the escrow. Rate: BIP39 about 1,680 derivations/s on one CPU
core (10 workers under contention), old-Electrum v1 about 280 seeds/s on one CPU core (the
100,000-round key stretch dominates), about 58,800 candidates/s on one rented GPU for the
old-Electrum v1 path, and about 17,500 to 18,800 seeds/s on 24 CPU workers with btcrecover.

## Anchor-based hypotheses (all assumed one or more of the 4 positions below)

The following families all assumed that 4 specific words sit at 4 specific positions in the
12-word phrase: `tower` at position 3, `subject` at position 6, `time` at position 8, `real`
at position 11 (a fifth variant used `moon` at position 13). I later found these 4 anchors are
not traceable to the puzzle author (see "What is understood"): they come from 2 Reddit
accounts whose posting history contains zero messages about this puzzle. I list the runs here
because they still cover real derivation space, but I no longer treat a miss on this space as
informative about the anchor-free space.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Clock-ordered, 1 word per hour position | 15,552 sequences (233 BIP39 checksum-valid) | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| Anchored on the "8 of 12 right" claim, 4-tuple orderings | 116,280 sequences | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| Anchored bounded residue over 4 word pools | 1,451,520 sequences (about 90,489 checksum-valid) | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| Clock-ordered sequences times 21 thematic passphrases | 4,893 combinations | BIP39 with passphrase | 0 match | yes | 2026-06-13 |
| Wide path sweep (BIP44 account/index range plus Electrum v2) | about 47 paths times the 5 top sequences | BIP39/Electrum v2 | 0 match | yes | 2026-06-13 |
| Fixed pool of 10 words, all orderings | 8,467,200 raw (528,842 checksum-valid) | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| Fixed pool of 9 words, all orderings | 30,481,920 raw (1,903,907 checksum-valid) | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| 4 whitepaper-derived 12-word sets, all orderings | 1,451,520 sequences | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| Fixed anchor pool of 8 words, all orderings | 403,200 derivations | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| Wider anchored campaign, 462 word sets times all orderings | about 18,626,400 derivations | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| Alternate-position campaign, 126 word sets times all orderings | about 5,080,320 derivations | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| btcrecover run 1, raw permutation space | 499,000,000 candidates launched | BIP39 | not recorded | yes (tool's own known-answer test) | 2026-06-13 |
| btcrecover run 2, close-word and typo variants of the anchors | 274,000,000 candidates launched | BIP39 | not recorded | yes | 2026-06-13 |
| btcrecover run 3, 50 thematic passphrases | 880,000 candidates launched | BIP39 with passphrase | not recorded | yes | 2026-06-13 |
| Community run, ac00300, one fixed 12-word set, all orderings | 479,001,600 permutations | BIP39, m/44' | 0 match | reported by the runner, not reproduced by me | 2020 to 2021 |
| Community run, ArmaCorex, mnemonics with and without passphrase | 377,200,000,000 mnemonics | BIP39 | 0 match | reported by the runner, not reproduced by me | 2021 to 2022 |
| Community run, demesmaeker, 6 word sets, all orderings each | 6 times 12 factorial | BIP39 | 0 match | reported by the runner, not reproduced by me | 2021 to 2022 |

Runs 1 to 3 above (btcrecover) were launched and their result section was never filled in: this
is "not recorded", not "0 match". Re-running them and logging the result is the fastest open
lead (see "Open leads, ranked" in the README).

## Anchor-free hypotheses

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| C(16,12) over a 16-word candidate pool, 6 image-exclusive icons forced present, 4 orderings of the remaining 8 slots | about 3,750,000 seeds (about 30,000,000 addresses across both change values) | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| Every 12-of-13 choice and every ordering of a 13-word pool read off the image without positions (`moon tower real black subject time first food this proof order receive mask`) | 6,227,020,800 sequences (389,185,926 checksum-valid) | BIP39 GPU kernel, `m/44'/0'/0'/0/0`, 12.7 million sequences/s, 489 s | 0 match | yes: the kernel's self-test recovers a planted target before the run | 2026-08-02 |
| One fixed 12-word set built from the singled-out elements (Bill Cipher `day`, rune fragment `add two`, `black`, hidden labels `real subject food`, dial `moon tower`, repeated `this first`, heading `order`), all orderings | 479,001,600 (29,935,319 checksum-valid) | same, 37 s | 0 match | yes | 2026-08-02 |
| The narrative set from the BitcoinTalk timeline reading (`black peace love health change future vote blue city march work mask`), all orderings | 479,001,600 (29,933,622 checksum-valid) | same, 37 s | 0 match | yes | 2026-08-02 |
| Old-Electrum icon blocks (`stop fist war new breathe needle`, `moon tower time`, `black subject real`) read forward and reverse in every block order | 1,086 candidates | old-Electrum v1 | 0 match | yes | 2026-08-02 |
| Structured "fresh" old-Electrum core, partial ordering sweep | 1,536 of 42,240 possible orderings generated | old-Electrum v1 | 0 match | yes | 2026-08-02 |
| Visual-block rotations and reversals of the collage's Electrum-exclusive words | 1,578 candidates | old-Electrum v1 | 0 match | yes | 2026-08-02 |
| Spatial and clockwise reading orders of the same word set | 896 candidates | old-Electrum v1 | 0 match | yes | 2026-08-02 |
| Dial- and number-indexed word blocks | 590 candidates | old-Electrum v1 | 0 match | yes | 2026-08-02 |

## Contributed positional sweeps (@NoobSilence, issue #12, 2026-09-04)

Reported in issue #12 after the anchor-free runs above; recorded as contributed. The
counts are consistent with four free positions drawn from the whole pool with
repetition (13^4 = 28,561 orderings, about 1 in 16 checksum-valid; 19^4 = 130,321). No
witness protocol was described, so the rows are uncertified.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Base `moon tower X black subject X first X this X order receive`, positions 3, 6, 8, 10 free over the 13-word pool | 28,561 orderings, 1,752 checksum-valid | BIP39 `m/44'/0'/0'/0/0` | 0 match | uncertified | 2026-09-04 |
| Same base and pool, old-Electrum legacy path | 28,561 | old-Electrum v1 | 0 match | uncertified | 2026-09-04 |
| Same base, positions free over a 19-word pool that adds drawn objects (`camera mask liberty eye pyramid vote police` and similar) | 130,321 orderings, 8,148 checksum-valid | BIP39 `m/44'/0'/0'/0/0` | 0 match | uncertified | 2026-09-04 |
| Counting-read base `tower camera X black mask X first X this X order world`, positions 3, 6, 8, 10 free over the 13-word pool | 28,561 orderings, 1,763 checksum-valid | BIP39 `m/44'/0'/0'/0/0` | 0 match | uncertified | 2026-09-04 |

The 13-word pool sweep is the largest test of the space that does not depend on the 4
refuted anchor positions: no position is fixed and every 12-of-13 choice is covered. Its
words, though, are still the community pool (7 of the 13 are words the retracted anchor
lists carry), and the old-Electrum campaign above still forces 6 specific words present.
A sweep over a pool re-derived directly from the image, independent of those lists, has
not been run (see the leads).

## Steganography and cipher channels (all ruled out as separate carriers, not as word sources)

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Hidden data in file structure (EXIF, appended bytes, LSB plane, alpha channel) | full file | binwalk, EXIF read, LSB histogram, zsteg | 0 EXIF fields, 0 appended bytes, LSB about 0.5 (noise), alpha 100 percent opaque, zsteg empty | yes (clean-file baseline) | 2026-06-13 |
| Geometric rune script (3 locations, about 85 glyphs) as an independent seed source | 85 glyphs transcribed | monoalphabetic substitution, index-of-coincidence check | decodes as Russian-language prose, not seed words | yes (index of coincidence matches natural-language text) | 2026-08-02 |
| 3 Latin mottos on the coin | 3 phrases | direct translation | ordinary Latin mottos ("know the causes of things", "let justice be done though the world perish", a proverb about a pot calling a kettle black), no seed words | yes | 2026-06-13 |
| Bill Cipher fragment above the Trump/Biden panel | 1 fragment | direct decode | reads "DAY", not a BIP39 or old-Electrum word | yes | 2026-08-02 |

## Geometry measurements that refute the 4 anchors independently

On 2026-08-02 I measured the dial region directly (the crop is `[265:685, 729:1140]` in the
published image, at native resolution, no upscaling). The dial is rotated about -73 degrees
from vertical, not a multiple of 30 degrees; positions 5 and 6 are not legible (covered by the
seal artwork); and the 2 labeled pointers land at fractional hour positions (the "TOWER"
pointer at about 1.48, not 1 or 2; the "MOON" pointer at about 0.54, not any whole hour). This
is a second, independent line of evidence (pixel geometry, not account history) against the
`tower` at position 3 and `moon` at position 13 claims: a 12-position dial has no position 13
at all.

## Community claims re-checked at the source (not taken on trust)

I searched Reddit's full comment archive (pullpush.io, which covers past the Wayback Machine's
last snapshot of the original post) for the 2 accounts most often cited as having confirmed
seed-word positions: `Big_Cut7029` (the "8 of 12 right" claim) and `Straight-Solution-39`
(`tower` at position 3, `moon` at position 13). Neither account has ever posted anything about
this puzzle, on this thread or any other. A third claim, from `Minase` on BitcoinTalk, is
explicitly speculative in its own wording ("an interesting phrase", offered right after "still
nothing"). The puzzle author, `u/stsh_n`, posted the image once, with the title "Bitcoin puzzle
(2000$)" and no other text, and has not posted again since 2020-10-08.
