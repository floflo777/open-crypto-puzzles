# Trithemius: Wealth in Poetry (0.0312463 BTC, [OPEN])

Writing under the pseudonym "Trithemius," the author published an article on Medium/Coinmonks in
2019 titled "Securing Bitcoin Seed Phrases in Stories," teaching a method for hiding a 12-word
BIP39 seed inside an ordinary narrative: a numeric key, specific to the author, picks word
positions out of the story text. The article demonstrates the method with two fully worked
examples and closes by stating that the reader has, by finishing the article, read every word
needed to recover a wallet holding 0.03 BTC. I calibrated the only certain part of the mechanism,
the tokenization rule, against both worked examples, then ran roughly 900,000 derivations across
three large campaigns covering numeric keys, derivation families, and passphrases. All are
negative. The escrow remains unclaimed seven years on, and the real carrier text and numeric key,
by the author's own design, are not guessable from the article alone.

## At a glance

| | |
|---|---|
| Author | pseudonym "Trithemius", Medium/Coinmonks |
| Published | 2019-02-11, [Medium/Coinmonks](https://medium.com/coinmonks/securing-bitcoin-seed-phrases-in-stories-d8eb43a02254) |
| Prize | 3,124,630 sats (about $1,969 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `1K4ezpLybootYF23TM4a8Y4NyP7auysnRo` ([explorer](https://mempool.space/address/1K4ezpLybootYF23TM4a8Y4NyP7auysnRo)) |
| Last on-chain check | 2026-11-04: funded and unspent, 2 funding transactions, 3,124,630 sats total (3,050,269 sats at block 562454 + 74,361 sats at block 570781) |
| Status | OPEN |
| Puzzle type | bip39-seed, text-cipher, brainwallet |
| Target format | BIP39 12 words, position selected by an author-specific numeric key applied to the article text; passphrase and derivation path not confirmed |
| Certified oracle | yes: `tools/oracle.py --selftest` (BIP39 BIP44/49/84 via two independent implementations, raw-key wiki vectors, raw-hash brainwallet variants, Electrum 2.x-4.x standard and old families via keystore agreement) |
| What remains | the real carrier text and the numeric key; both are author-specific by the article's own design |
| Series | none |

## The puzzle as published

The article (archived locally, byte-identical to a third-party mirror,
[medium.com/coinmonks](https://medium.com/coinmonks/securing-bitcoin-seed-phrases-in-stories-d8eb43a02254),
2019-02-11) opens with a story about the author's grandfather smuggling gold while fleeing China,
then teaches "trithemian seeds." It demonstrates two encoding methods, each with its own story and
seed: a phone number whose digits give word positions in a courtship story, and a formula
`position[i] = i*10 + digit[i]` applied to the concatenated digits of a location's latitude and
longitude, run against a story about a letter to a court. The article closes: "The beauty of
trithemian seeds is that they hide in plain sight. If you've read this far, you've read every
word required to access a wallet with .03 BTC. Good luck!" and "Only you know which story
contains your wealth."

## What is understood

### Mechanism

The chain is: article text, tokenized into words, then a numeric key (unknown, author-specific)
selects 12 word positions, giving a candidate 12-word phrase to run through BIP39 and every
standard derivation path. Tokenization is the one calibrated link: of 4 tokenizers tried, exactly
2 reproduce the word positions of both published worked examples exactly, which is why those two
are treated as certain rather than assumed.

### Derivation and oracle

A certified oracle ships in this folder: `tools/oracle.py`. Its self-test asserts the official
BIP32/39/44/49/84 vectors through two independent implementations (a manual BIP32 walk and the
bip_utils builders), the two documented Bitcoin-wiki raw-key address pairs, the BIP39 checksum
validator against the `mnemonic` package, and agreement with the `electrum` package's own
`BIP32_KeyStore` and `Old_KeyStore` on generated seeds. Candidate families: BIP39 (BIP44/49/84,
compressed), raw-text hashing (sha256 and sha256d over six serializations, both key
compressions), Electrum 2.x-4.x standard (PBKDF2 "electrum" salt, BIP32 root, m/0/n and m/1/n,
gated on the real restore check), and Electrum 1.x old (mn_decode, 100000-round sha256 stretch,
uncompressed keys). Compare against the escrow address at
[mempool.space](https://mempool.space/address/1K4ezpLybootYF23TM4a8Y4NyP7auysnRo).

A 2026-11-04 re-verification also settled two factual questions. The "witch collapse practice
feed shame open despair creek road again ice least" example is a genuine old-Electrum seed: all
twelve words decode via Electrum's old 1626-word list to hex seed 25a39767960aafbdba67ad41f5657826
(it is not BIP39 - "witch" is not in the BIP39 wordlist - and it fails the Electrum '01' restore
gate). And the embedded Steganographia photograph shows the 1606 Frankfurt title page only: the
page promises "PRÆFIXA EST HVIC OPERI SVA CLAVIS" but contains no cipher table; its only numeral
is the year 1606.

### Established facts

1. Tokenization is calibrated: 2 of 4 tested tokenizers reproduce the exact word positions of
   both of the author's published examples.
2. The article's own GPS-formula example, applied to the full narrative rather than just the
   demonstration letter, leaves 2 of the 12 word slots with zero valid BIP39 options, which
   confirms that published example is a worked demonstration, not the real wallet key.
3. A stylometric pass (surprisal and substitution scoring across the full narrative) found BIP39
   words statistically indistinguishable from the rest of the text, meaning there is no detectable
   insertion fingerprint marking which words are the real seed.
4. Forensic analysis of the archived article file (33 MIME parts, every embedded image at full
   resolution) found no appended data, no hidden metadata, and no zero-width characters.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Rows dated 2026-08-02 remain
uncertified (the code they ran had no acceptance test). Rows dated 2026-11-04 are certified:
they ran through `tools/oracle.py`, whose self-test proves the acceptance path on known-good
vectors before any search.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Numeric-key enumeration: coordinate formats, landmarks, in-article numbers, phone/GPS/cumulative methods, multiple carriers | 541 keys, about 300,000 derivations | address comparison, compressed and uncompressed | 0 match | uncertified | 2026-08-02 |
| Derivation-family sweep on the 4 clean example seeds: BIP44/49/84 multi-account, raw BIP32 paths, master key, old Electrum v1/v2 | about 500,000 addresses derived | address comparison | 0 match | uncertified | 2026-08-02 |
| Passphrase (25th word) sweep on the 4 clean seeds: curated article-derived terms, full-phrase candidates, brute-force wordlists | about 78,000 derivations | address comparison | 0 match | uncertified | 2026-08-02 |
| Image steganography: full-resolution originals, LSB analysis on lossless formats | 11 images | bit-plane analysis | pure noise (bit ratio about 0.5), 0 WIF or hex64 strings recovered | uncertified | 2026-08-02 |
| Direct WIF/hex scan of the raw article file | 125 base58-like substrings | BIP38/WIF checksum check | 0 pass the checksum (all image data false positives) | uncertified | 2026-08-02 |

## Open leads, ranked

1. **Author-specific numeric key or author contact** (open, class person). The 2026-11-04
   campaign closed the mechanical leads: the Steganographia photograph carries no cipher table
   (only the 1606 imprint), and every numeric-key source derivable from the article, its images'
   legible content (the Venezuelan banknote serial B35409659 and date), the article's embedded
   timestamps, and the escrow's own funding amounts and block heights is certified-negative
   across BIP39, raw-hash, Electrum-standard and Electrum-old families. What remains is a
   key that is a real-world number of the author's (the article's own methods point at personal
   phone numbers and coordinates of personally meaningful landmarks) or a wallet family outside
   the modeled set. The authors ("Sharon & Philippe", Medium @onesourgrape) published nothing
   else and left no other trace; their article invited DMs.
2. **Wallet families not yet modeled** (open, class insight). If the author restored from the
   phrase with something other than BIP39 or Electrum (a 24-word phrase, a BIP38 intermediate,
   custom derivation paths, or a brainwallet service with a non-sha256 KDF), the certified
   negatives do not reach it. Any new candidate string from any future source is one
   `tools/oracle.py --phrase` call away from a definitive answer.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | the article's two worked examples and closing lines, quoted verbatim with the source URL and date |
| `analysis/tested.md` | the complete negatives ledger, marked uncertified |
| `analysis/leads.md` | full notes behind the ranked leads |

## Sources

- Trithemius, "Securing Bitcoin Seed Phrases in Stories," Medium/Coinmonks, 2019-02-11: https://medium.com/coinmonks/securing-bitcoin-seed-phrases-in-stories-d8eb43a02254
- Community tracker confirming the puzzle is still unsolved: https://privatekeys.pw/puzzles/0.03-btc-coinmonks-puzzle
- BitcoinTalk thread on the puzzle (opened 2026-10-20): https://bitcointalk.org/index.php?topic=5597422.0
- Community scan repo with article archive (sliding-window BIP39 and old-Electrum attempts, negative): https://github.com/HomelessPhD/Wealth_in_Poetry
- Community tabula-recta attempt with keyword REVOLUTION, negative: https://github.com/vortomastro/TrithemiusCipher
- Source of the Steganographia title-page photograph (Jesus College blog, August 2015): https://jesuslibraries.wordpress.com/2015/08/01/august-2015-book-of-the-month-steganographia-by-johannes-trithemius-1606/
