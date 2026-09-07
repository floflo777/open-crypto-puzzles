# Negatives ledger, Arweave Puzzle #10

Every run used the certified oracle (SHA-512 x11513, AES-OpenSSL decrypt, `"kty":"RSA"`
gate). None of these runs carries a planted witness inside its own candidate space, since
the correct answer is unknown; the oracle itself is certified separately against the
solved sibling Arweave #8 (see the README's "Certified against" section). All dated
2026-07-25 unless noted otherwise.

| Family | Candidates | Notes |
|---|---|---|
| Curated left-to-right literal-token battery | 412 | reads the 5 keys as their obvious literal tokens, joined in image order |
| Grammar-calibrated pass | 1,798 | same reading style, expanded with the solved-siblings' answer grammar |
| 20-character hard-length reading of `[0-19]` | 6,492 | treats the bracket as a literal length specifier |
| "Paradise"-centric candidates across all lengths | 4,480 | follows a community reading of the dice/silhouette pair |
| Corrected structure: Palpatine not Vader, genesis key kept separate | 4,122 | |
| Corrected structure: slice-first-20 reading | 8,558 | |
| GPU sweep: image-order concatenation | 1,200,000 | rented GPU, certified exact-match gate |
| GPU sweep: separator concatenation | 800,000 | |
| GPU sweep: no-separator slice-to-20 over 6 orders | 640,000 | |
| GPU sweep: special-character connector variants | 660,000 | |
| GPU sweep: "Paradise"-pun forms | 40,000 | |
| Genesis-block message family | 9,187 | 314 genesis-block messages, 9 normalizations each |
| Pun/anagram/re-reading sweep, order A (genesis is the whole answer) | 660 | |
| Pun/anagram/re-reading sweep, pun image-order | 350,064 | |
| Pun/anagram/re-reading sweep, 2 extra orders | 230,400 each (460,800 total) | |
| Pun/anagram/re-reading sweep, Bible/Genesis-28-as-scripture axis | 35,910 + 532 | includes Hebrew transliterations |
| Curated 5-slot product with empty slots and slice-to-20 | 3,787,175 | |

One generator (a roughly 70,000-candidate literal `0..19` reading) was started and killed
before completion; it is not counted as a negative, since it never finished. Two further
candidate sets, an "on paper = on computer" notation reading (255,365 candidates) and a
wider exact-length-20 vocabulary set (2,196,517 candidates), were generated but not
confirmed run to exhaustion; they are not counted here either.

Also refuted, not a candidate sweep: forensic steganalysis of the puzzle image
(exiftool, binwalk, `zsteg -a`) found no LSB payload, no appended bytes, and no metadata
payload. A visually suspected "watermark strip" in a community-assembled composite image
was measured (cross-correlation against the authoritative on-chain PNG, peak correlation
0.41) and judged an upscaling artifact rather than a real signal, since that composite is
larger than every known authentic source of the image.

Cumulative: on the order of 8,010,190 candidates tested to completion across every
literal, pun, notation, and genesis-block reading found so far, 0 matches.

## Bounded Genesis 28 follow-up, 2026-09-04 UTC (contributed by @BorisLoveDev, PR #19)

I checked the README's explicitly untested full-passage lead in two finite forms.
Neither produced an exact escrow match. This is not a rejection of every scripture
reading or translation. The old private candidate lists are unavailable, so exact
non-overlap with every historical string cannot be asserted.

| Hypothesis | Unique strings | Stream entries | Witness positions, zero-based | Result | Runtime |
|---|---:|---:|---|---|---:|
| H1: full verse and passage wording | 448 | 451 | 0, 225, 302, 450, all recovered | 0 exact matches | 268.109 s |
| H2: numeric extraction from chapter text | 80 | 83 | 0, 41, 77, 82, all recovered | 0 exact matches | 49.454 s |

The two sets have no overlap: 528 distinct strings in total. Each stream entry is
checked against the real ciphertext and an independently encrypted witness fixture.
The first and last stream entries and the central entry are repeats of the witness;
its original occurrence accounts for the fourth expected match. Rate including both
checks was 1.682 and 1.678 stream entries/s respectively. Before-search calibration
measured 1.730 and 1.687 entries/s and predicted 260.731 and 49.197 seconds.

H1 scope: the KJV and WEB renderings of Genesis 28 from bible-api.com, each of its
22 verses separately plus inclusive spans 1-22, 10-22, 10-19, 12-19, 16-19 and 18-22.
Eight serializations: collapsed whitespace with original punctuation and case; lower
and upper case of that; words with punctuation removed and spaces retained, original
and lower case; words joined without spaces, original and lower case; joined words
with initial capitals. Internal apostrophes are retained. Duplicate strings are removed.

H2 scope: either the whole chapter or verses 6, 3, 18 joined in that order. From
each, take the first 20 characters of each serialization; the first 20 words and
serialize them; or word indices 6, 3, 18 with zero-based and one-based numbering and
serialize them. Same two translations and serialization rules. No arbitrary wordlist,
permutation or surrounding clue-token product is included.

Witness: deterministic RNG seed 20260905 selects one actual member of each family.
The original page's JavaScript encrypts the already-solved #8 JWK with that member
and fixed salt 0011223344556677. Every candidate traverses the same Python check()
for the real target and fixture target; no branch recognizes a witness specially.
Both the original JavaScript and Python recover the known sibling address. The
oracle selftest and independent Bitcoin BIP44/49/84/86 toolchain vectors passed.

Exact commands, from the repository root after acquiring inputs into the sibling
`arweave10-inputs` directory:

```
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H1.json --private-output ../arweave10-private --hypothesis H1
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H2.json --private-output ../arweave10-private --hypothesis H2
```

The working run used directory names `run-2026-09-05` and `private-results` in
those same positions. Parameters and input bytes are otherwise identical. Final
machine outputs are preserved in `genesis28-results.json` in this analysis directory.
See `../tools/REPRODUCE.md` for acquisition, source hashes, dependency versions,
selftests, `--plan` commands and the 590-second incomplete-run limit. No source
chapter text, candidate string or decrypted keyfile is included here.

### Oracle regression found before either search

Previously check() accepted any parsed RSA-labelled JWK, without checking its
address against ESCROW. Replacing the ciphertext with the real solved #8 ciphertext
and using its public answer returned True with address
`ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4`, although the target remained
`bkjJGw3NLxs8OAyRxgTL-QFpiB3lBJqZ76kDhWdB-Rs`. This is a reproduced false positive,
not a solve. check() now requires exact address equality, the selftest covers both
the positive and mismatched-target cases, and --stdin no longer prints a successful
answer string. `tools/test_oracle.py` exercises both regressions with the real
sibling ciphertext. The two searches above ran after this fix.

The original #10 page directly links the escrow and contains byte-identical
ciphertext to the oracle constant. On 2026-09-04 at 22:42:05 UTC its balance was
500022254930000 winston and the gateway GraphQL query for transactions owned by
that address returned no edges. This is a funding observation, not a derivation match.
