# BLM Collage: Welcome to the Brave New World (0.20107284 BTC, [OPEN])

Reddit user `u/stsh_n` posted a single collage image on 2020-10-08, titled "Bitcoin puzzle
(2000$)": a 1600x1200 composite of 2020 news imagery (COVID, the George Floyd protests, the
Trump-Biden election) instructing the reader to "find the seed phrase in this picture." An
escrow of 20,107,284 sats had already been funded on 2020-05-10, before the post. The author
never commented again. I confirmed the derivation format is either a BIP39 12-word mnemonic or
an old-Electrum (v1) 12-word mnemonic, both read straight off visible words on the collage, and
built an oracle that checks either format under every plausible path with zero false positives.
What I could not confirm is which 12 of roughly 30 candidate words are the real ones, or their
order: past campaigns, mine and the community's, anchored on 4 claimed word positions that I
traced back to 2 Reddit accounts with zero posts about this puzzle. Those anchors are retracted
here. The compute and the derivation paths are well covered; the open question is the input.

## At a glance

| | |
|---|---|
| Author | u/stsh_n, [Reddit](https://www.reddit.com/user/stsh_n/comments/j79zvj/bitcoin_puzzle_2000/) |
| Published | 2020-10-08, Reddit ([original post](https://www.reddit.com/user/stsh_n/comments/j79zvj/bitcoin_puzzle_2000/)) |
| Prize | 0.20107284 BTC (about $12,668 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ` ([explorer](https://mempool.space/address/1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ)) |
| Last on-chain check | 2026-08-16: funded and unspent (20,107,284 sats, 5 funding transactions, 0 spent) |
| Status | OPEN |
| Puzzle type | image-stego, word-selection, bip39-seed, text-cipher |
| Target format | BIP39 12 words at 4 candidate paths, or old-Electrum v1 12 words at 5 address indexes and 2 change values; both compressed and uncompressed P2PKH checked |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the raw priv=1 P2PKH vectors, the public BIP39 "abandon" test vector, and a public old-Electrum v1 test vector) |
| What remains | which 12 of about 30 candidate words on the collage form the phrase, their order, and which of the 2 formats applies |
| Series | none |

## The puzzle as published

The collage (`clues/welcome-to-the-brave-new-world.png`, 1600x1200, published as-is) layers
2020 news imagery: a masked crowd, a portrait with protest slogans ("BLACK LIVES MATTER", "NO
JUSTICE NO PEACE", "END POLICE BRUTALITY"), the Statue of Liberty holding a protest placard, a
Space Needle, a Great Seal pyramid coin, a rotated 12-position dial with 2 labeled pointers, a
column of geometric runes, and a title, "WELCOME TO THE BRAVE NEW WORLD," composed in
micro-text lifted from the Bitcoin whitepaper's transactions section. The only instruction is
printed across the middle: "FIND THE SEED PHRASE IN THE THIS PICTURE" (typo original). The
Reddit post itself carries no caption and no further comment; see `clues/author-posts.md`.

![Three measured regions of the published collage: the rotated dial with its two labeled pointers, the pedestal engraving, and the right-edge rune column](images/01-annotated-regions.png)
*Figure 1. The 3 regions of the collage with measured, reproducible pixel boundaries, drawn over the published image (source: data/candidate-regions.json, script tools/fig_regions.py), 2026-08-16.*

## What is understood

### Mechanism

Any 12-word candidate is read straight off visible or deciphered words on the collage; no
external material is involved. Two competing derivation families remain live:

- **BIP39**: 12 words, checksum-valid, PBKDF2-HMAC-SHA512 seed, then BIP32 child derivation
  under 4 candidate paths (`m/44'/0'/0'/0/0`, `m/44'/0'/0'/0/1`, `m/0/0`, `m/0'`), both
  compressed and uncompressed P2PKH.
- **old-Electrum (v1)**: 12 words from the 1626-word old-Electrum wordlist, no checksum, a
  100,000-round SHA-256 stretch to a master secret, then per-address derivation at 5 address
  indexes and 2 change values, uncompressed P2PKH.

The collage settles part of the fork by vocabulary: words like `breathe`, `fist`, `free`,
`needle`, `new`, `stop`, and `war` exist only in the old-Electrum wordlist, while words like
`camera`, `civil`, `food`, `liberty`, `police`, `proof`, `pyramid`, `riot`, `this`, and `vote`
exist only in the BIP39 wordlist. Confirming any single one of these as a real seed word would
settle the format outright.

![The 3 unknowns (format, word selection, word order) and the 2 candidate formats with their exclusive on-image words](images/02-format-fork.svg)
*Figure 2. The format fork: BIP39 versus old-Electrum v1, and the words on the image that are exclusive to each (source: data/format-fork.json, script tools/fig_format_fork.py), 2026-08-16.*

### Derivation and oracle

```
python3 tools/oracle.py --selftest                 # must print SELFTEST OK
python3 tools/oracle.py "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12"
python3 tools/oracle.py --stdin                     # one 12-word candidate per line
```

A candidate is tried first as a BIP39 mnemonic (checksum validated, all 4 paths, both
compressions), then as an old-Electrum v1 mnemonic (all 5 indexes, both change values). It
reports `MATCH <method> <address>` only on an exact address match against the escrow, `NO
MATCH` otherwise.

### Certified against

`tools/oracle.py --selftest` reproduces 4 independent vectors: the raw secp256k1 private key 1
mapped to its published uncompressed (`1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm`) and compressed
(`1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH`) P2PKH addresses; the public BIP39 all-zero-entropy test
vector ("abandon" times 11 plus "about") at `m/44'/0'/0'/0/0` compressed, which derives
`1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA`; and a public old-Electrum v1 test mnemonic, which derives
`1KCvshw5g3ndGYxQmAxKcTpJV5kbj6Lefo` at change 0, index 0. A negative control confirms neither
public vector matches the escrow. Reproduced 2026-08-16.

### Established facts

1. The escrow is funded and unspent: 5 incoming transactions totaling 20,107,284 sats, 0 spent,
   checked on [mempool.space](https://mempool.space/address/1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ)
   on 2026-08-16.
2. The image file carries no hidden data in its container: 0 EXIF fields, 0 bytes appended
   after the PNG end marker (checked with binwalk), the alpha channel is 100 percent opaque,
   and the least-significant-bit plane measures as noise. All seed material is in the visible
   collage, not in the file structure.
3. The dial is rotated about -73 degrees from vertical, not a multiple of 30 degrees, and its
   2 labeled pointers land at fractional hour positions (about 1.48 and 0.54), measured
   directly from the published image on 2026-08-02.
4. Two Reddit accounts most often cited as having confirmed word positions, `Big_Cut7029` and
   `Straight-Solution-39`, have zero posts about this puzzle anywhere in Reddit's full comment
   archive (searched via pullpush.io, which covers past the Wayback Machine's last snapshot).
   A third cited claim, from `Minase` on BitcoinTalk, is explicitly speculative in its own
   wording. I found no post from the author confirming any word, position, or format.
5. The geometric rune script (about 85 glyphs across 3 locations on the image) decodes as
   Russian-language prose under a monoalphabetic substitution, consistent with natural-language
   text by an index-of-coincidence check; it names no seed word directly.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Anchor-based families (clock order, claimed 4-tuple, anchored pools, passphrase sweep, wide path sweep) | about 1.6 million derivations across 6 sub-families | BIP39, 4 paths, comp/uncomp | 0 match | yes | 2026-06-13 |
| old-Electrum anchor-based campaigns (fixed pools, wide campaign, alternate positions) | about 24.1 million derivations | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| Community runs re-checked at the source (ac00300, ArmaCorex, demesmaeker) | 479,001,600 plus 377,200,000,000 plus 6 times 12 factorial | BIP39 | 0 match | reported by the runners | 2020 to 2022 |
| Anchor-free old-Electrum sweep (16-word pool, 6 exclusive words forced, 4 order frames) | about 3,750,000 seeds (about 30,000,000 addresses) | old-Electrum v1 | 0 match | yes | 2026-06-13 |
| Anchor-free BIP39 GPU sweeps: every 12-of-13 choice and every ordering of a 13-word pool read off the image, plus all orderings of 2 fixed 12-word sets (singled-out elements; the BitcoinTalk narrative reading) | 7,185,024,000 sequences (449,054,867 checksum-valid) | BIP39 GPU kernel, `m/44'/0'/0'/0/0` | 0 match | yes: kernel self-test on a planted target | 2026-08-02 |
| Steganography and file-structure channels | full file | binwalk, EXIF, LSB, zsteg | clean, no hidden channel | yes | 2026-06-13 |
| Cipher inventory (runes, Latin mottos, Bill Cipher fragment) | 14 elements | direct decode | no additional seed words found | yes | 2026-08-02 |

Cumulative: about 30 million derivations across the anchor-based and anchor-free families
through 2026-06-13, plus 449 million checksum-valid BIP39 derivations from 7.2 billion
sequences on 2026-08-02, 0 matches. The 13-word pool sweep fixes no position, but its words
are still the community pool; a sweep over a word pool re-derived directly from the image
has not been run (see "Open leads, ranked").

## Open leads, ranked

1. **Log the 3 already-launched btcrecover runs** (minutes, free). Prepared and executed
   against a pipeline whose own known-answer test passes, but their result was never written
   down. Confirmed if either rerun prints a match; killed as a source of new candidates once
   both are logged clean.
2. **Re-derive the word inventory from the image itself** (hours). Every large campaign to
   date, including the anchor-free sweep, still uses a fixed candidate pool rather than a fresh,
   systematic relisting of every word visible on the collage. Confirmed if a word absent from
   every prior pool derives the target once combined with the rest; killed if the relisting
   reproduces the same pool already tested.
3. **Cross the rune transcription against the Russian-prose cipher key** (minutes, free). The
   positioned 85-glyph transcription and the substitution-cipher hypothesis have never been
   directly checked against each other. Confirmed as closed if the decoded prose reads
   coherently start to finish; reopened as a candidate word source if it does not.
4. **Settle BIP39 versus old-Electrum from a source, not from more derivation** (needs new
   information). This single fact would cut the remaining search space roughly in half; no
   message signature or other author confirmation is known to exist.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/welcome-to-the-brave-new-world.png` | the published puzzle collage, byte-exact, sha256 recorded in puzzle.json |
| `clues/author-posts.md` | the complete author material: the original Reddit post, dated and linked |
| `data/candidate-regions.json` | the 3 measured pixel regions used in Figure 1 |
| `data/format-fork.json` | the 3 unknowns and the 2 candidate formats with their exclusive words, used in Figure 2 |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 4 ranked leads |
| `images/01-annotated-regions.png` | the annotated collage figure |
| `images/02-format-fork.svg` | the format-fork diagram |
| `tools/oracle.py` | candidate checker, BIP39 and old-Electrum v1 modes, both certified |
| `tools/fig_regions.py` | generates images/01-annotated-regions.png from data/candidate-regions.json |
| `tools/fig_format_fork.py` | generates images/02-format-fork.svg from data/format-fork.json |

## Sources

- u/stsh_n, "Bitcoin puzzle (2000$)", Reddit, 2020-10-08: https://www.reddit.com/user/stsh_n/comments/j79zvj/bitcoin_puzzle_2000/ (archived: https://web.archive.org/web/20210613000000/https://www.reddit.com/user/stsh_n/comments/j79zvj/bitcoin_puzzle_2000/)
- "Is this puzzle still valid?", r/bitcoinpuzzles, thread jrr7mo, checked 2026-08-16: https://www.reddit.com/r/bitcoinpuzzles/comments/jrr7mo/is_this_puzzle_still_valid_is_this_image_correct/
- BitcoinTalk topic 5404767 (community discussion, not author material), checked 2026-08-16: https://bitcointalk.org/index.php?topic=5404767.0
- Escrow address, mempool.space: https://mempool.space/address/1KfZGvwZxsvSmemoCmEV75uqcNzYBHjkHZ

Credits: @NoobSilence (issue #12): four positional sweeps on the 13-word and 19-word pools, recorded in `analysis/tested.md` as contributed.
