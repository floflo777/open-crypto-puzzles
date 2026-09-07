# Arweave Puzzle #10 (500.02225493 AR, [OPEN])

Tiamat (@ArweaveP) published this puzzle on the Arweave permaweb on 2020-04-14: a single
torn-paper image showing 5 drawn keys (two dice, a handwritten "6 3 18", a silhouette
inside the Arweave logo's "a", the bracket notation "[0-19]", and a physical key tagged
"...nesis #28"), feeding one free-text field into the same client-side decrypt routine
used across this author's series. I reversed and certified the decrypt pipeline against a
solved sibling puzzle, but the author never published any length or charset constraint
for this puzzle specifically, unlike most of its siblings. Reading the 5 keys against the
answer grammar of 3 other solved puzzles in the series, I have tested on the order of 8
million literal, pun, and genesis-block candidate readings with 0 matches. The most
promising untested reading is the full biblical text the "[0-19]" bracket and the "6 3 18"
notation seem to point toward.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@ArweaveP on Twitter](https://twitter.com/arweavep) |
| Published | 2020-04-14, Arweave permaweb ([live page](https://arweave.net/1fLPMP_smP6ipdIYbYUAZtFPwO4crdYr4kMVf5uTivg)) |
| Prize | 500.02225493 AR (about $905 at AR = $1.81, 2026-08-16) |
| Chain | arweave |
| Escrow | `bkjJGw3NLxs8OAyRxgTL-QFpiB3lBJqZ76kDhWdB-Rs` ([explorer](https://viewblock.io/arweave/address/bkjJGw3NLxs8OAyRxgTL-QFpiB3lBJqZ76kDhWdB-Rs)) |
| Last on-chain check | 2026-08-16: funded and unspent, 500022254930000 winston |
| Status | OPEN |
| Puzzle type | word-selection, text-cipher |
| Target format | one case-sensitive free-text answer, unknown length, SHA-512 x11513, AES-decrypt to an Arweave JWK keyfile |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against solved sibling Arweave Puzzle Weave #8) |
| What remains | one unguessed token among the 5 drawn keys; the answer's exact length was never published |
| Series | Arweave Puzzles (this folder covers puzzle #10 only) |

## The puzzle as published

The live page (still up) shows one torn-paper drawing and a single free-text input field
with a button that submits the typed string to the decrypt routine; no `maxlength`, no
case-folding, no separator hint. The full
403-tweet @ArweaveP archive (2019-05-23 to 2022-10-15) contains exactly 3 length or
charset statements in total, and none of them is about puzzle #10 (2 are about puzzle #7,
one about puzzle #12). 3 users asked the length question directly under the #10
announcement and the author answered none of them; his only reply under that tweet is a
status line,
["1,2,4,8 = solved / 3,5,7,9 = not solved yet"](https://twitter.com/arweavep/status/1250036746802298885)
(2020-04-14). In a reply on the #10 thread on 2020-04-22, the confirmed solver of a later
puzzle in the series, @_LeFevre_, read the image as a reference to the Arweave genesis
block and a 2018 Palpatine meme, adding that the puzzle was "too vague to know what you
are actually supposed to be solving."

## What is understood

### Mechanism

The page reads the single free-text field verbatim (no trimming, no case-folding),
stretches it with SHA-512 applied 11,513 times, and uses the resulting 128-character hex
digest as an EvpKDF/AES-OpenSSL password to decrypt an embedded ciphertext. Success is
declared only if the plaintext contains the literal marker `"kty":"RSA"`. This is the
same CryptoJS bundle, including the same non-standard 1024-bit-key, 38-round Rijndael
quirk (crypto-js issue #293), used across this author's series. The visible `size="24"`
attribute on the input field is cosmetic, not the true answer length: sibling puzzle #7
uses `size="20"` but its real answer is 57 characters.

### Derivation and oracle

```
python3 tools/oracle.py --selftest       # reproduces the solved sibling Arweave #8
python3 tools/oracle.py "CandidateAnswerString"
python3 tools/oracle.py --stdin          # one candidate per line
```

A candidate is passed through exactly as typed (case-sensitive, no trimming).
`MATCH <address>` on a hit, `NO MATCH` otherwise. Since no dependency available to this
repository implements CryptoJS's non-standard Rijndael variant, the oracle reimplements
it in pure Python; the implementation was checked to reproduce a standard AES-256 library
exactly at the standard key size before being trusted at this puzzle's non-standard one.

### Certified against

`tools/oracle.py --selftest` decrypts the real ciphertext of the solved sibling Arweave
Puzzle Weave #8 with its published answer, `RasputinWilhelmAlekhine`, and recovers a JWK
whose derived address matches `ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4` exactly, the
address baked into that puzzle's own success page. Puzzle #8's escrow is already spent
(checked 2026-08-16), so this is historical calibration data, not a live prize. The
oracle's raw decrypt output was also checked byte-for-byte against this puzzle's own
JavaScript decryptor running under Node, on both matching and non-matching passphrases.

### Established facts

1. The escrow is funded and unspent: 500.02225493 AR, checked via
   `arweave.net/wallet/<address>/balance` on 2026-08-16.
2. No author statement about #10's answer length or charset exists anywhere in the
   403-tweet archive or the reply thread under the announcement.
3. 6 solved siblings across the series (3 decrypted locally: #5, #7, #8; 3 more reported
   by community research: #1, #2, #4) share one answer grammar: tokens concatenated with
   no separators, Capitalized proper nouns, plain digits for numbers, in-image
   punctuation allowed, total length ranging from 23 to 58 characters.
4. The Arweave genesis block's transaction index 28 decodes to the literal text "test";
   the community's own reversed display numbering instead maps its position 286 to "We'll
   see what happens." Both readings were checked and both fail.
5. No steganographic payload was found in the puzzle image (exiftool, binwalk,
   `zsteg -a` all negative).

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Literal-token batteries (curated, then grammar-calibrated) | 2,210 | certified oracle | 0 match | uncertified | 2026-07-25 |
| 20-character hard-length and "Paradise"-centric readings | 10,972 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Corrected-structure batteries, slice-to-20 variants | 12,680 | certified oracle | 0 match | uncertified | 2026-07-25 |
| GPU sweep: image-order, separator, slice, special-character, and pun concatenations | 3,340,000 | certified oracle on a rented GPU | 0 match | uncertified | 2026-07-25 |
| Genesis-block message family, 314 messages x 9 normalizations | 9,187 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Pun, anagram, and misdirection sweep across 3 slot orders | 847,966 | certified oracle | 0 match, refuted as a structure | uncertified | 2026-07-25 |
| Curated 5-slot product with empty slots and slice-to-20 | 3,787,175 | certified oracle | 0 match | uncertified | 2026-07-25 |
| Stego pass on the puzzle image | full file | exiftool, binwalk, zsteg -a | refuted: no hidden data | yes | 2026-07-25 |

Cumulative: on the order of 8,010,190 candidates tested to completion, 0 matches. 2 more
candidate sets (about 2,450,000 combined) were generated but not run to exhaustion and are
not counted here as negatives.

A bounded follow-up on 2026-09-04 UTC by @BorisLoveDev (PR #19) checked 448
full-passage strings and 80 numeric-extraction strings from Genesis 28, all with
complete witnesses: 0 exact matches; I replayed the second family locally with the
same counts and witness positions. The oracle was also corrected to reject a valid
wallet with a different address. Counts, scope and commands are in [analysis/tested.md](analysis/tested.md);
updated next steps are in [analysis/leads.md](analysis/leads.md).

## Open leads, ranked

1. **The exact wording of Bible Genesis chapter 28** (hours), the Jacob's Ladder / Bethel
   passage, transcribed as a long word-series the way solved sibling #7's 57-character
   answer is built. Two bounded KJV/WEB families (528 strings) are now negative; further
   enumeration needs evidence fixing the source and operator order. Confirmed by a candidate matching the escrow exactly; killed
   by exhausting every reasonable transcription of the passage.
2. **Non-public channels** (needs a person): the author's Telegram group, a later Discord,
   or a direct reply, none of which have produced a #10-specific hint in the public
   record searched so far. A community-notes author's contact email surfaced during this
   research is not the puzzle author and should not be treated as an official channel.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/puzzle-image.png` | the published torn-paper puzzle image, byte-exact |
| `analysis/tested.md` | the complete negatives ledger |
| `tools/oracle.py` | candidate checker: free-text answer to JWK address, certified against the solved sibling #8 |

## Sources

- Live puzzle page, Arweave permaweb, 2020-04-14: https://arweave.net/1fLPMP_smP6ipdIYbYUAZtFPwO4crdYr4kMVf5uTivg
- "1,2,4,8 = solved / 3,5,7,9 = not solved yet", Twitter, 2020-04-14: https://twitter.com/arweavep/status/1250036746802298885
- @_LeFevre_ reply in the #10 announcement thread, 2020-04-22, reproduced by the community research repository: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL10
- HomelessPhD/AR_Puzzles community repository, PZL10 entry: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL10
- Escrow wallet, viewblock.io: https://viewblock.io/arweave/address/bkjJGw3NLxs8OAyRxgTL-QFpiB3lBJqZ76kDhWdB-Rs

Credits: @BorisLoveDev (PR #19): exact-address oracle check, regression tests, and the two witnessed Genesis 28 families.
