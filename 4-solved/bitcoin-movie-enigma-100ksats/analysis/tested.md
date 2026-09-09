# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts below were re-read from my own private research notes before writing this
folder.

## Both published image sets are identical

The rules page mentions "an alternative release, as a single image." I compared
every one of the 34 individual panel images against the corresponding region of the
combined alternative-release image, byte for byte (MD5).

Result: 34 of 34 panels match exactly. This channel is closed: the alternative
release carries no additional or different information, it is the same 34 stills
republished as one file. Date: 2026-08-03.

## Intruder criterion: MPAA rating equals R

Hypothesis: the 10 "intruder" films are exactly the ones rated R by the MPAA, and
the IMDb page field the rules point to is the certificate rating.

Method: count the films confirmed R-rated as more panels were identified.

Result: this criterion looked correct early, when only a partial set of films was
identified (10 of 18 identified films rated R at one point). It broke as soon as 2
more films were confirmed: with panel #4 (Mad Max, R) and panel #34 (rated R under
either of its 2 disputed identifications) added, the R-rated count reached 16 to 18
out of the identified films, well past 10. Refuted. Witness: this is a direct count
over the film corpus, not a search that could produce a false negative; re-counting
is immediate from `data/films.csv`. Date: 2026-08-04.

## Intruder criterion: won at least one Oscar

Hypothesis: the 10 intruders are the films that won at least one Academy Award.

Method: same approach, counting Oscar-winning films as identifications accumulated.

Result: looked correct at 10 of 21 identified films early on, refuted once panel
#24 (Ordinary People, a 4-Oscar winner including Best Picture) was confirmed
through a route independent of the reverse-image search used for most other
panels, pushing the count to 11 of 34. Date: 2026-08-04.

## Intruder criterion: adapted from a novel

Hypothesis: the 10 intruders are the films adapted from a published novel.

Method: same approach.

Result: looked correct at 10 of 31 identified films, refuted at 12 of 34 once
further identifications landed. Date: 2026-08-04.

## About 25 further intruder criteria

Method: the same accumulate-and-recount approach applied to about 25 further
candidate IMDb fields and binary properties (examples: country of origin,
decade of release, director's other Bitcoin-relevant work, runtime bracket, color
versus black and white, single-word versus multi-word title).

Result: none produced an exact 24-versus-10 split against the identified film set,
either from the start or after refutation by a later identification. Witness: each
criterion is a direct count over the film corpus and is immediately re-checkable;
no witness protocol beyond re-counting applies here. Date: 2026-08-04.

Methodological note, kept because it explains why no criterion is locked in below:
3 different criteria (MPAA=R, Oscar win, novel adaptation) each looked like the
answer while the film corpus was still incomplete, and each was broken by the very
next identification. With about 25 to 30 criteria tried against a set of only 34
films, landing on an exact 10-film split by chance is not strong evidence on its
own. My working rule is to not treat any criterion as confirmed before all 34
panels are identified with confidence.

## PNG EXIF and XMP on the published stills

Hypothesis: the 34 published `NN_crop.png` files carry the movie title, the BIP39
word, or some other payload in EXIF/XMP.

Method: download all 34 crops from bitcoinmovieenigma.com and read PIL `Image.info`
plus the TIFF EXIF block.

Result: every file carries the same payload, byte for byte in the XMP packet:
`dc:description` / `ImageDescription` is the literal string "nope", and
`dc:creator` / `Artist` is `@cryptop1r4t3`. That is a decoy, not a channel.
Witness: all 34 XMP packets compare equal; re-download and re-read to confirm.
Date: 2026-08-27.

## Title-to-word rule: unique 4-letter BIP39 prefix in the compact title

Hypothesis: the transform is "find the unique BIP39 4-letter prefix (or the whole
word, if it is 3 letters) as a substring of the title with spaces and punctuation
removed." Under that reading, "raidersofthe" contains `soft`, "theshining"
contains `shin` -> `shine`, "leontheprofessional" contains `prof` -> `profit`,
and "sharknado" contains `shar` -> `share`.

Method: run every 4-letter window of each compact title against the English BIP39
wordlist's unique prefixes.

Result: this produces at least one word for 33 of 34 community-identified titles.
The only title with no prefix and no literal substring is The Goonies (panel 8).
This is a measurement, not a match against the escrow. Date: 2026-08-27.

## Intruders = G, PG, and TV-14 (keep R and PG-13, plus unrated)

Hypothesis: on the reconciled community film list, the 10 intruders are the
films whose IMDb / MPAA certificate is G, PG, or TV-14, i.e. panels 7, 8, 12,
18, 24, 25, 26, 30, 31, and 32. That set includes both wordless-under-literal
titles The Goonies and Sharknado, so the remaining 24 titles all have a BIP39
reading. Paths of Glory (APPROVED) and Spartacus (no MPAA claim on Wikidata)
were kept, not dropped.

Method: take the 24 keepers in panel order and, for each title with more than
one reading, the Cartesian product of the short alternative list in
`data/films.csv` (leftmost unique-prefix word plus the community substring
reading). 55,296 raw 24-word strings, of which 227 pass the BIP39 checksum.
Each checksum-valid mnemonic was run through `tools/oracle.py` (BIP84/49/44
and the 3 raw paths).

Result: 0 match. Uncertified: no known-good 24-word mnemonic for this escrow
exists to plant as a head/middle/tail witness in the same loop; the oracle
self-test against the public BIP39/BIP84 vectors passed the same day. Rate:
about 18,000 raw strings/s, checksum filter first, then the full derivation
only on the 227 valid mnemonics. Date: 2026-08-27.

## Title-to-word rule: base rate measurement

This is a measurement, not a hypothesis test with a pass or fail result: of the 33
titles identified as of 2026-08-04, 29 contain at least one English BIP39 word as a
literal substring of the title (for example, "Die Hard" contains "hard"; "A
Clockwork Orange" contains 4 candidates: "clock," "orange," "range," "work"). Four
titles contain none: The Goonies, Barry Lyndon, Sharknado, and Raiders of the Lost
Ark. The literal-substring rate across the 33 identified titles is about 14%,
counted per candidate word against the full BIP39 wordlist. This measurement rules
out "every title contains exactly one obvious word" as the full rule (4 titles have
none, several have more than one), but does not by itself say which of several
candidate words is the intended one, or what the rule is for the 4 titles with none.

## Community metadata-rule sweeps (issue #9, 2026-08-22 to 2026-08-23)

Contributed in issue #9 and recorded here as reported by the runners, not re-run by me.
They test the intruder criterion under the community film list, so a match would need both
that list and the rule to be right at once.

timothy-barus: every intruder predicate expressible from IMDb metadata that selects exactly
10 of the 34 panels, three of which leave at most two panels wordless and so are fully
coverable with 2048-word wildcards. Three rules swept exhaustively (shares a release year,
released 2000 or later, ten shortest by runtime): 314,069,483,520 raw candidates,
1,226,826,312 checksum-valid seeds, derived at BIP84 m/84'/0'/0'/0/{0,1,2} and matched
against the escrow hash160. Witnessed: GPU reproduces the CPU reference byte for byte, three
planted witness mnemonics recovered from head, middle and tail, checksum rate within 0.6
sigma of raw/256. Result: 0 match.

SmallCakekoo: 25 single-field IMDb boolean criteria cross-tested pairwise with AND/OR, 600
combinations, 17 of which produce an exact 10-panel split; all 17 run through full derivation
and address check, 0 match. Separately, an IMDb-connections hypothesis (30 documented
cross-references among the 34 films, exactly 10 films with zero in-set connections) tested two
ways: 1,828,915,200 candidates over every sourced IMDb-keyword word for the titles with no
literal BIP39 substring, and all 131,128,140 ways to choose which 10 of 34 to drop under one
fixed word per panel. Result: 0 match in either.

Standing after these: every clean IMDb-metadata rule that leaves at most two panels wordless
has been swept and is empty. The open problem is the title-to-word rule for the three titles
that yield no BIP39 word under the community list (The Goonies, Leon, Sharknado), which is a
reading question, not a compute one. See leads.md.

## Sweeps on the consensus film list, 2026-09-01 and 2026-09-02

Oracle: the public BIP84 vector (`abandon` x 23 plus `art`) reproduced, target the
escrow's hash160; enumeration with a BIP39 checksum filter in C (OpenMP), derivation on
CPU (BIP84, BIP44, BIP49, BIP86 and raw paths) or on a 24-word port of the shared GPU
engine (BIP84 `0/0` only). "Witness 3/3" means 3 synthetic 24-word mnemonics planted at
head, middle and tail of that run and recovered by the normal path; "vector only" means
no witness was planted in that run and it is uncertified.

| Hypothesis | Raw candidates | Derivations | Witness | Result |
|---|---|---|---|---|
| Older identifications: the titles without a literal word fixed as intruders, plus 5 of the remaining 29 | 4.0e8 | 1,563,007 | 3/3 | 0 match |
| Same, with panels 3 and 5 as Aliens and Alien | 2.2e8 | 875,811 | 3/3 | 0 match |
| Consensus list: 6 wordless or ambiguous panels fixed as intruders plus 4 of the other 28, literal words | 5.95e7 | 231,806 | 3/3 | 0 match |
| Same, with panel 14 as The Man in the Iron Mask (`iron`, `mask`, `man`, `ask`) | 1.67e8 | 651,882 | 3/3 | 0 match |
| Consensus list, words from substrings of 3 or more letters, 4 wordless panels fixed plus 6 of 30 (GPU, 445 s) | 1.52e10 | 59,321,852 | 3/3 | 0 match |
| The natural partition (the 24 titles with an obvious word), 178 derivation paths, 4 seed constructions, no checksum filter | 512 | 512 x 712 | vector only | 0 match |
| Natural partition, forward and backward, one position free over the 2048 words | 5.0e7 | 955,206 | vector only | 0 match |
| Kubrick x5 plus Jean Reno x5 as the 10 intruders (panel 14 = Iron Mask), panel 8 free, `share` or `tornado` for 26, `soft` for 32 | 3.1e6 | 12,344 | vector only | 0 match |
| Same, ambiguities widened (`eye`/`wide`, `cat`, `run`, `load`, `host`, `ski`, `ride`, `tip`) | 1.0e9 | 3,981,013 | vector only | 0 match |
| Release year or runtime read as a BIP39 index (10 variants), 11 intruders plus 9 of 33 | 3.9e8 | 1,502,910 | vector only | 0 match |
| 6 deterministic 4-letter-prefix rules, 4 wordless panels fixed plus 6 of 30 | 3.6e6 | 13,914 | vector only | 0 match |
| 40 neighbour rules (alphabetical neighbour, longest common prefix, letter counts), keepers = 20th-century films | 1.8e7 | 68,958 | vector only | 0 match |

Totals: about 1.6e10 raw candidates and 62,644,358 derivations with witnesses (5 runs),
about 1.5e9 raw candidates and 6,534,857 derivations without (7 runs), 0 match. Two runs
were interrupted and are not counted: substrings of 3 or more letters with panel 14 as
Iron Mask (85 million of 178 million lines), and a no-checksum pilot on the GPU. Rate:
about 13,000 derivations/s on 24 CPU cores across 7 paths; about 170,000 derivations/s on
one GPU for BIP84 `0/0`. Dates: 2026-09-01 and 2026-09-02.

What this closes: on the consensus list, the intruders are not "the titles with no
literal word plus a few others" at any depth up to substrings of 3 letters, and the
Kubrick plus Reno split does not solve with a single free position. What it leaves: that
split at two free positions, and the two rules themselves.

## Panel 14, settled 2026-09-03

I had kept panel 14 as Eyes Wide Shut against the community's The Man in the Iron
Mask. On 2026-08-29 deviceio121 posted two frames from
[youtube 3PcEZNC7IPw at 2:18](https://www.youtube.com/watch?v=3PcEZNC7IPw), which is
MGM's official "Judgement Day" scene from The Man in the Iron Mask (the video's own
title). The frame shows the same masked group as the panel: the woman in the gold mask
and red-and-gold turban at left, the man in the long wig holding a gold bearded mask
on a stick at centre. Panel 14 is The Man in the Iron Mask, and the Kubrick plus Reno
split stands at exactly 10.


## Confirmed solve, 2026-09-07

The title-opening-prefix reading and five thematic film groups yield an exact
escrow-address match at m/84'/0'/0'/0/0. The 24-word phrase fails the BIP39
checksum (encoded 47, expected 119); checksum-filtered negatives therefore
do not cover this answer. The oracle now derives without that assumption and
its self-test reproduces the actual solution. Independent manual BIP32 and
Bech32 calculations agree. The payout of 99,766 sats (234 sats fee) confirmed
in block 965998. See the README and
[payout verification](payout-verification-2026-09-07.json).
