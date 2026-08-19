# GSMG.io Puzzle (5.0068982 BTC across 2 addresses, [OPEN])

GSMG.io, a Netherlands-based crypto-trading platform introduced publicly in
January 2019, funded a multi-stage web puzzle with 5 BTC on 2019-04-13 and
challenged the public to solve it and keep the coins. The puzzle chains cryptograms,
an image, and several classical ciphers across a dozen web pages; every stage since
2019 has been passed by the community. What remains is the final gate, which on
2020-05-11 split into two independent, still-locked pieces held at two separate
addresses: a small encrypted blob and a much larger one nicknamed "Dualite" in the
page's own markup. Both are OpenSSL-format AES ciphertext with an unknown password.
The mechanical chain from the published page down to each blob is fully mapped and
reproducible; what is missing is the password (or, on the older readings, a direct
32-byte reduction) that opens either one.

## At a glance

| | |
|---|---|
| Author | pseudonymous, Telegram handle `@SoWut`, name shown as "Jrk Bgrt"; real identity not publicly resolved |
| Published | 2019-04-13, escrow funding transaction ([mempool.space](https://mempool.space/tx/73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02)) |
| Prize | 1.2563451 BTC + 3.7505531 BTC = 5.0068982 BTC across 2 addresses (about $315,435 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` ([explorer](https://mempool.space/address/1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)) and `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` ([explorer](https://mempool.space/address/17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa)) |
| Last on-chain check | 2026-08-16: both funded and unspent (1.2563451 BTC and 3.7505531 BTC) |
| Status | OPEN |
| Puzzle type | text-cipher, pixel-code, web-tree, raw-private-key |
| Target format | a candidate answer string X; password = sha256(X) hex; decrypts an OpenSSL "Salted__" AES-256-CBC blob printed on the final page; plaintext reduces to a 32-byte private key; uncompressed secp256k1 public key; P2PKH address |
| Certified oracle | yes, in two independent parts: `tools/oracle.py --selftest` (address-derivation half certified against the escrow's own on-chain public key; AES-decrypt half certified against a self-made round-trip vector; see "Certified against") |
| What remains | a password, or a direct reduction, that turns an already fully-decoded object into a 32-byte private key matching one of the two addresses |
| Series | none |

## The puzzle as published

The puzzle's escrow address, `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`, received its
first funding, exactly 5 BTC in a single transaction, on 2019-04-13
([txid `73e48ff5...`](https://mempool.space/tx/73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02)).
GSMG.io itself, [gsmg.io](https://www.gsmg.io/), presents itself as an automated
crypto-trading platform; the puzzle is a separate, unpaid challenge run from the
same domain.

The puzzle is a chain of web pages, each unlocked by solving the one before it. A
community-maintained repository documents the public stage order
([github.com/puzzlehunt/gsmgio-5btc-puzzle](https://github.com/puzzlehunt/gsmgio-5btc-puzzle)),
and a bitcointalk thread has discussed the puzzle since 2025
([topic 5532424](https://bitcointalk.org/index.php?topic=5532424.0)): an opening
cryptogram, three numbered "phase" pages, an image page ("the seed is planted"), a
substitution-cipher page nicknamed "SalPhaseIon", a page called "follow the white
rabbit", a branching page called "the Architect Choice", and a final page. Every
stage in this chain has been passed by the community since 2019.

The final page's body is a sequence of 1075 single-character tokens. Decoded
through the page's own straightforward transforms (binary-to-ASCII on two marked
sections), two of those tokens spell out, verbatim: `matrixsumlist` and
`ourfirsthintisyourlastcommand`. The same page also embeds a 14x14 pixel image and
two base64-encoded text blocks in two separate `<textarea>` elements, the second one
titled "Dualite" in the page's own markup.

![The published stage chain, solved end to end, forking into the two final gates that remain locked](images/01-structure-stages.svg)
*Figure 1. The stage chain and the fork into the two final gates (source: data/stage-chain.json, script tools/fig_stages.py), 2026-08-16.*

On 2020-05-11, 2.5 BTC moved from `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` to a new
address, `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`
([txid `2aa9a4a9...`](https://mempool.space/tx/2aa9a4a90be819d5122d70c993280785a0508f163521e7b38cebb4db0b071b13)),
and again on 2024-04-24, a further 1.25 BTC moved the same way
([txid `88cdb3cd...`](https://mempool.space/tx/88cdb3cdca12b471551b1b26188508a14ca5fd8a415223ffb7c190381c9b9df3)).
Both transactions consumed only `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`'s own funds as
inputs and sent part of the total to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, with the
remainder returned to `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` itself as change; neither
transaction paid out to any third party. `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` has
received 44 incoming transactions in total and has never sent a single satoshi.

## What is understood

### Mechanism

Reaching the final page requires solving a chain of classical ciphers across the
stage sequence in Figure 1: a Vigenere-family cipher, a Bifid cipher applied to a
570-character segment with the keyed square `DBIFHCEG` and a period equal to the
full segment length, and a bit-plane reading of a 14x14 pixel image (the low bit of
each pixel's color, read in a spiral from the top-left corner, spells the ASCII
string `gsmg.io/theseedisplanted`). The Bifid step's output splits into two
interleaved streams; the odd-position stream, with the two Base58-ambiguous letters
I and O removed, reduces to exactly 256 symbols drawn from a 23-letter alphabet.
Every attempt so far to turn that 256-symbol object directly into a 32-byte private
key has failed (see "What has been tested").

The final page separately publishes a small OpenSSL "Salted__" AES-256-CBC blob (96
bytes total: 8-byte header, 8-byte salt `3ab585348552415d`, 80 bytes of ciphertext,
enough for a 64-byte plaintext after PKCS7 padding). The password is reported to be
`sha256(X).hexdigest()` for an answer string X the solver must find; this repository
ships an oracle for exactly this half of the final gate (below). The page's second,
much larger blob, titled "Dualite", is confirmed by direct measurement (byte
histogram and autocorrelation) to be well-formed AES-CBC ciphertext rather than
noise or a decorative filler value, but no password has ever been found for it.
Given the 2020-05-11 and 2024-04-24 transfers described above, I believe, without
having confirmed it, that the small blob gates
`1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` and the "Dualite" blob gates
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`; nothing published states this explicitly, and
confirming or killing it would need decrypting one of the two blobs.

![Candidate answer to P2PKH address, six stages linked by sha256, AES-256-CBC decryption, secp256k1 and HASH160](images/02-pipeline-derivation.svg)
*Figure 2. The final-gate derivation pipeline `tools/oracle.py` implements for the small blob (source: data/pipeline-stages.json, script tools/fig_pipeline.py), 2026-08-16.*

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<candidate answer>"
python3 tools/oracle.py --stdin
```

Given a candidate answer string X, the oracle computes `sha256(X).hexdigest()` as
the password, decrypts the small blob printed on the final page with that
password, and, if the PKCS7 padding validates, tries 4 standard readings of the
resulting plaintext (the plaintext's own SHA-256; its first 32 bytes; its last 32
bytes; the SHA-256 of its first 64 bytes) as a 32-byte private key. For each
reading it derives the uncompressed secp256k1 public key and compares the P2PKH
address against `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. `MATCH <address>
reading=<name> priv_hex=<hex> wif=<wif>` on a hit, `NO MATCH` otherwise, exit code
0 or 1. This oracle does not test the "Dualite" blob or
`17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, since no password-generation hypothesis for
that blob has more support than any other (see `analysis/leads.md`).

This is a different, and independently reproducible, check from the puzzle's own
answer-checking tool referenced informally by some solvers, which is not published
and which this repository has no access to.

### Certified against

`tools/oracle.py --selftest` certifies the pipeline's two halves independently,
since X is unsolved and no end-to-end known-good vector exists:

1. **Address derivation**: the escrow's own uncompressed public key, recovered from
   its 2024-04-24 spending transaction
   ([txid `88cdb3cd...`](https://mempool.space/tx/88cdb3cdca12b471551b1b26188508a14ca5fd8a415223ffb7c190381c9b9df3)),
   `04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a4649c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559`,
   hashes byte-exact to `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`. This certifies the
   HASH160-plus-Base58Check half of the pipeline against a real, independently
   checkable fact.
2. **AES decrypt**: a self-made OpenSSL-compatible blob (a 64-byte test plaintext,
   encrypted with a test password using the same EVP_BytesToKey MD5 key derivation
   and AES-256-CBC scheme) decrypts back to the exact original plaintext with the
   correct password, and produces no valid PKCS7 padding with a wrong password.
   This is a synthetic vector, not one from the puzzle, since no real password is
   known.
3. The published blob itself is confirmed to decode to the documented shape: 96
   bytes, header `Salted__`, salt `3ab585348552415d`.

Reproduced 2026-08-16.

### Established facts

1. `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` was first funded with exactly 5 BTC on
   2019-04-13 and is funded and partially spent as of 2026-08-16, holding
   1.2563451 BTC (checked via [mempool.space](https://mempool.space)).
2. `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa` was first funded on 2020-05-11, entirely
   from `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`'s own outputs, and is funded and
   unspent as of 2026-08-16, holding 3.7505531 BTC.
3. Both of `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`'s 2 outgoing transactions
   (2020-05-11 and 2024-04-24) spent only that address's own funds and paid part of
   the total to `17ucy1K9ZUAaoY6JVtM932W9jUp5LXfyHa`, with the rest returned to
   `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe` as change; neither is a third-party sweep.
4. The final page's body is 1075 single-character tokens (confirmed by direct
   extraction and byte count from an archived capture of the page).
5. The Bifid decoding of the 570-character segment (keyed square `DBIFHCEG`,
   period 570) reproduces byte for byte and starts with the plaintext `BTCSEED`.
6. The odd-position stream of that decoding, with I and O removed, is exactly 256
   characters over a 23-letter alphabet; of the 7 letter-pairs that could be
   removed from the 285-letter stream to reach exactly 256 symbols, only the I/O
   pair leaves a Base58-valid alphabet.
7. The 14x14 image, read as described above, spells `gsmg.io/theseedisplanted`
   exactly, with no residual bits.
8. The final page's HTML markup carries no additional hidden channel beyond the
   1075 tokens, the image, and the two text blocks (checked directly).

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| 256-symbol object reduces to a key via a letter-to-bit mask (linear and 20 spatial orders) | 335,000,000 candidates | direct address comparison | 0 match | yes | 2026-07-28 |
| 256-symbol object's alphabet splits into a 16-letter and a 7-letter group | 490,314 candidates | direct address comparison | 0 match | yes | 2026-07-28 |
| The 32 target numbers are ASCII codes of a 32-character window of a known object | 34,000 candidates | direct address comparison | 0 match | yes | 2026-07-28 |
| 256-symbol object read as a single Base58 number | 17,304 candidates | direct address comparison | 0 match | yes | 2026-07-28 |
| A substring of the object is a Base58Check string to decode | 123,728 candidates | Base58Check checksum, then address comparison | 0 match, 0 valid checksum | yes | 2026-07-28 |
| Large "Dualite" blob read directly as bits, no password | 59,269 candidates | direct address comparison | 0 match | yes | 2026-07-30 |
| Literal password strings harvested from 1,017 archived scripts, replayed under a fixed appearance filter | 116,043 candidates | AES decrypt then address comparison | 0 match | yes | 2026-07-28 |

Cumulative: approximately 335.7 million candidates tested as direct reductions of
the 256-symbol object or the large blob, all negative; a further 116,043-candidate
partial replay of historical literal password guesses, also negative. Full scope
and method notes for each row, including why the literal-string replay is
explicitly partial, are in `analysis/tested.md`.

## Open leads, ranked

1. **Replay the dynamically-constructed candidates a filter bug never reached**
   (hours to days). A 2026-07-28 review found that an appearance-based acceptance
   filter had silently rejected the correct answer shape in 98 of 213 historical
   scripts. A first replay resubmitted 116,043 literal strings from those scripts
   directly (0 match), but the same scripts also built candidates dynamically
   (concatenations, permutations, chained transforms) that this first replay does
   not reach. Confirmed by re-running a script's own generation logic and finding a
   match; killed, stage by stage, by exhausting that logic with none.
2. **Determine whether the 256-symbol object is the right target at all** (an
   afternoon of reasoning, not a sweep). Every negative in row 1 to row 5 of the
   tested table assumes the key comes directly from this object; the AES-blob route
   this folder's oracle implements is a different, untested-at-scale hypothesis.
   Confirmed by a reduction, other than the ones tried, that matches an address;
   redirected by establishing the AES-blob or "Dualite" route is the real one.
3. **Identify the single tool reportedly used to build every phase** (hours). An
   authenticated author statement says one tool built every phase; comparing
   confirmed cipher conventions against one specific public tool's source code
   matches on non-obvious details (no period parameter on its Bifid cipher, a short
   menu of available ciphers). Confirmed by a cipher from that tool's menu
   producing a match on the "Dualite" password or the 256-object reduction; killed
   by exhausting that tool's short menu with no match.
4. **Follow "esrever", the earliest published hint** (minutes to hours). The
   author's first hint, "reverse" spelled backwards, has been applied to the object
   it was originally paired with but not to the current final-gate objects.
   Confirmed by a reversal (string, bit, or reading-order) of one current object
   matching an address; killed by exhausting the small set of reasonable reversals.
5. **Read the 29 dropped letters as their own message** (minutes). Reducing the
   285-letter stream to the 256-symbol object drops exactly 29 letters, never read
   as an object in their own right. Confirmed by a match or a legible fragment;
   killed by exhausting the small set of reasonable reading orders.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | public sources for the puzzle's background and stage order, and the 2 short strings decoded verbatim from the final page's own published content |
| `data/stage-chain.json` | the published stage chain and the two final gates, for the structure figure |
| `data/pipeline-stages.json` | the 6-stage label list for the derivation pipeline figure |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 5 ranked leads |
| `images/01-structure-stages.svg` | the published stage chain forking into the two final gates |
| `images/02-pipeline-derivation.svg` | the final-gate derivation pipeline for the small blob |
| `tools/oracle.py` | candidate checker for the small-blob route, certified in two independent parts |
| `tools/fig_stages.py` | generates images/01-structure-stages.svg from data/stage-chain.json |
| `tools/fig_pipeline.py` | generates images/02-pipeline-derivation.svg from data/pipeline-stages.json |

## Sources

- GSMG.io, platform site: https://www.gsmg.io/
- Escrow first-funding transaction, mempool.space, 2019-04-13: https://mempool.space/tx/73e48ff571a7e9a4387574a50cf2fcb7b21b6ea5702c777a035664df57cbce02
- First transfer to the second address, mempool.space, 2020-05-11: https://mempool.space/tx/2aa9a4a90be819d5122d70c993280785a0508f163521e7b38cebb4db0b071b13
- Second transfer to the second address (public key source), mempool.space, 2024-04-24: https://mempool.space/tx/88cdb3cdca12b471551b1b26188508a14ca5fd8a415223ffb7c190381c9b9df3
- bitcointalk topic 5532424, "Need help Puzzle GSMG.IO 5BTC": https://bitcointalk.org/index.php?topic=5532424.0
- Reddit discussion, r/bitcoinpuzzles: https://www.reddit.com/r/bitcoinpuzzles/comments/bf7siz/gsmgio_5_btc_puzzle_challenge/
- Reddit discussion, r/bitcoinpuzzles: https://www.reddit.com/r/bitcoinpuzzles/comments/dfwcqk/gsmgio_5_btc_puzzle/
- Community-maintained stage documentation: https://github.com/puzzlehunt/gsmgio-5btc-puzzle
