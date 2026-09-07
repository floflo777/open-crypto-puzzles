# Arweave Puzzle #11 (1 ETH, [OPEN])

Tiamat (@arweavep), an Arweave project Discord member and early investor, announced this
puzzle on Twitter on 2020-04-22: a single grayscale PNG sketch of a harbor, uploaded to
Arweave, with 1 ETH locked at an address the author said is "also included somewhere in the
image." Unlike the rest of the series, this puzzle has no password-protected decryption page:
the author's own hint is "MEW: Access by Private Key," meaning the answer is a raw 64-hex
private key read directly out of the image, not a mnemonic or a keystore file. The address
printed in clear text inside the file's metadata is a confirmed decoy. I measured the image's
geometry precisely (12 buildings, 1 large sailboat, 5 small sails) and its metadata (a
create-before-modify timestamp anomaly shared only with a sibling puzzle), and tested close to
1,000 direct encodings of both against the target address, all negative. The exact pixel-level
encoding the author used is still unknown, and no certified oracle exists for this puzzle since
no known-answer candidate is available to test the harness against.

## At a glance

| | |
|---|---|
| Author | Tiamat, [@arweavep on Twitter](https://twitter.com/arweavep) |
| Published | 2020-04-22, Twitter ([original announcement, now deleted](https://twitter.com/arweavep/status/1252961944807641090)) |
| Prize | 1 ETH (about $1,880 at ETH = $1,880, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0xFF2142E98E09b5344994F9bEB9C56C95506B9F17` ([explorer](https://etherscan.io/address/0xFF2142E98E09b5344994F9bEB9C56C95506B9F17)) |
| Last on-chain check | 2026-08-16: funded and unspent (balance exactly 1.000000000000000000 ETH, outgoing transaction count 0) |
| Status | OPEN |
| Puzzle type | image-stego, pixel-code, raw-private-key |
| Target format | raw 32-byte / 64-hex secp256k1 private key, standard ETH address derivation, no mnemonic, no keystore |
| Certified oracle | no: the derivation code (SHA-256, Keccak-256, secp256k1) is checked against public test vectors, but no known-answer candidate exists for this specific puzzle to certify the image-to-key mapping against |
| What remains | the exact pixel-level encoding (which channel, what order, what quantization) that turns the image into 256 bits |
| Series | Arweave Puzzles (this folder covers puzzle #11 only) |

## The puzzle as published

The puzzle is a single PNG, `clues/arweave-puzzle-11.png` (1600x1105, 8-bit grayscale with
alpha, published as-is): a pencil-style sketch of a harbor, with a skyline of 12 buildings, one
large sailboat, a jetty carrying 5 small sails, and a watermark reading
`twitter.com/ArweaveP`. The image is stored on Arweave at transaction
`CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY`
([viewblock](https://viewblock.io/arweave/tx/CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY)),
uploaded 2020-04-22, and its sha256 (`c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1`)
matches the copy in this folder exactly. The full set of the author's own quotes, each sourced
and dated where a date is recoverable, is in `clues/author-posts.md`.

![Automated silhouette measurements over the published sketch: 12 building bounding boxes and the large sailboat bounding box](images/01-annotated-geometry.png)
*Figure 1. The measured geometry fed into the negative candidate sweep, drawn over the published image (source: data/geometry.json, script tools/fig_geometry.py), 2026-08-16.*

## What is understood

### Mechanism

The expected output is a raw 256-bit ECDSA private key on the secp256k1 curve, which derives
the escrow address directly under the standard Ethereum address scheme
(Keccak-256 of the uncompressed public key, last 20 bytes). The author's "format does not
matter" reply, given when someone asked about the file type, reads as a statement that the
payload survives re-encoding: it lives in the visual pixel content, not in PNG-specific
container structures. The address printed inside a `tEXt` metadata chunk is a confirmed decoy,
not the key: the author separately said the key is "hidden in the image," and a plaintext
address inside the file would defeat the point of a puzzle.

### Derivation and oracle

No certified oracle is shipped for this folder. A candidate is checked by treating it as a
32-byte private key, deriving its Ethereum address, and comparing the result to the target
case-insensitively:

```python
from eth_keys import keys
candidate_privkey = bytes.fromhex("...")  # 32 bytes
address = keys.PrivateKey(candidate_privkey).public_key.to_checksum_address().lower()
match = address == "0xff2142e98e09b5344994f9beb9c56c95506b9f17"
```

This comparison code is standard and was checked against public secp256k1 and EIP-55 test
vectors, so a "no match" on any candidate below is reliable. What is not certified is the step
before it, the mapping from image content to a 32-byte candidate: no known-answer image and key
pair exists for this puzzle to test that mapping against, so every negative in this folder
carries an "uncertified" mark rather than a witness.

### Certified against

Not applicable in the usual sense: there is no solved sibling and no author-published example
for this specific puzzle. The derivation primitives (SHA-256, Keccak-256, secp256k1 point
multiplication) were checked against the standard EIP-55 checksum test vectors and against
puzzle #9's own real, already-spent address as a positive control when its geometry was used to
calibrate carrier hypotheses (see `analysis/tested.md`); neither of these certifies a specific
image-to-key scheme for puzzle #11 itself.

### Established facts

1. The escrow holds exactly 1.000000000000000000 ETH and has an outgoing transaction count of
   0, checked via `eth_getBalance` and `eth_getTransactionCount` against a public Ethereum RPC
   endpoint on 2026-08-16.
2. The puzzle image's `tEXt` metadata chunks read `comment 0xFF2142E98E09b5344994F9bEB9C56C95506B9F17`,
   `date:create 2020-03-30T11:38:07+03:00`, and `date:modify 2020-03-30T11:34:44+03:00`: the
   modify timestamp precedes the create timestamp, an anomaly shared only with sibling puzzle
   #9, confirmed by reading the file's own chunks on 2026-08-16.
3. The file is a clean, valid PNG with 0 bytes after the IEND marker: IHDR, gAMA, cHRM, bKGD,
   pHYs, 22 IDAT, 3 tEXt, and IEND chunks, checked with binwalk and direct chunk inspection.
   Community reports of an embedded executable or filesystem are binwalk false positives on
   near-random decompressed pixel bytes, not real container structure.
4. The alpha channel has 434 pixels with a value under 255, all clustered on the large
   sailboat's outline with values from 1 to 30, consistent with an anti-aliasing halo from a
   copy-paste rather than structured data.
5. Automated silhouette measurement (thresholded at gray value 110) found 12 buildings, 1 large
   sailboat (bounding box x 44 to 359, y 320 to 599), and 5 small sails with widths 27, 53, 79,
   83, and 51 pixels left to right; full coordinates in `data/geometry.json`.
6. No public write-up describes a working encoding scheme for this puzzle: the community repository
   `HomelessPhD/AR_Puzzles` marks its own PZL11 entry as not solved, and a full local archive of
   the community Telegram group (55,002 messages, November 2021 to May 2026) contains no
   message from the author and no later hint beyond the ones quoted in `clues/author-posts.md`.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Geometry-derived candidates (building sequences, raw pixel hashes, cHRM bytes, object counts, matrix reshapes, value-band masks) | about 460 candidates | SHA-256, double SHA-256, Keccak-256, address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Metadata date anomaly (create/modify timestamps, several encodings and combinations) | dozens of encodings times 6 hash functions | address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Sibling-puzzle-#9-calibrated alpha channel carrier hypotheses | several hundred combinations | address comparison, calibrated against #9's real address | 0 match, 0 near-miss, and does not reproduce #9's known answer either | yes, on the #9 positive control only | 2026-06-13 |
| Container-structure myths (embedded executable or filesystem) | full file | binwalk, chunk inspection | refuted: clean valid PNG | yes | 2026-06-13 |

Cumulative: on the order of 1,000 candidates tested across geometry and metadata families,
0 matches, 0 near-misses under the `ff21` address-prefix check.

Added 2026-09-05 by @BorisLoveDev (PR #21), all with synthetic-carrier witnesses and an
exact-address compare: isolated ASCII hex and zlib/gzip payloads in 7,168 pixel
bitstreams, 79,863 raw 256-bit windows in the anomalous first row, Code128/ITF barcodes
on 75 crops, and one community sixteen-number skyline transcription through 1,488 HD
derivations. 0 match. I replayed the four non-barcode scans locally with identical
counts. Details in [analysis/tested.md](analysis/tested.md).

## Open leads, ranked

1. **A systematic LSB scan of the continuous grayscale and alpha channels** (hours). Every
   candidate so far reads geometry or metadata as a whole value; a bit-level scan with a tool
   built for this (`zsteg -a`, `stegoveritas`) has not yet been run to exhaustion. Confirmed if
   an extracted 64-hex string derives the target exactly; killed once the sweep is exhaustive
   across bit order and bit width with no match.
2. **Join the community Telegram group and search first-hand for the promised hint** (needs a
   person). I already searched the full archived window (November 2021 to May 2026) and found
   nothing; what remains untested is anything from before the archive starts or outside its
   coverage.
3. **Puzzle #9's real solving method, if it ever surfaces** (needs new information). #9 was
   swept in 2020 by an anonymous solver who never published a method; a future write-up would
   give this folder its first certified, puzzle-specific oracle.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/arweave-puzzle-11.png` | the published puzzle image, byte-exact, sha256 recorded in puzzle.json |
| `clues/author-posts.md` | the author's dated Twitter quotes, as reproduced by the community repository |
| `data/geometry.json` | the 12 building bounding boxes, the sailboat bounding box, and the 5 small sail widths |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 3 ranked leads |
| `images/01-annotated-geometry.png` | the annotated geometry figure |
| `tools/fig_geometry.py` | generates images/01-annotated-geometry.png from data/geometry.json |

## Sources

- Tiamat, original announcement, Twitter, 2020-04-22 (deleted): https://twitter.com/arweavep/status/1252961944807641090
- Tiamat, "Next set of hints when AR reaches $100 :)", Twitter, 2021-08-23: https://twitter.com/arweavep/status/1429846914028158977
- Puzzle image, Arweave transaction CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY: https://viewblock.io/arweave/tx/CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY
- HomelessPhD, "AR_Puzzles" community repository, PZL11 entry, checked 2026-08-16: https://github.com/HomelessPhD/AR_Puzzles/tree/main/PZL11
- Escrow address, Etherscan: https://etherscan.io/address/0xFF2142E98E09b5344994F9bEB9C56C95506B9F17

Credits: @BorisLoveDev (PR #21): the 2026-09-05 bounded extraction tests and their scripts.
