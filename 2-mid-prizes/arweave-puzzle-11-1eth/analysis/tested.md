# Tested (full negatives ledger)

No certified oracle exists for this puzzle: the target is a raw 256-bit private key with no
intermediate checksum, so every candidate below was checked by deriving its ETH address
(`eth_keys`, compressed public key) and comparing it byte-exact (case-insensitive on the hex)
against `0xFF2142E98E09b5344994F9bEB9C56C95506B9F17`. The derivation code itself (SHA-256,
Keccak-256, and secp256k1 point multiplication) is standard and was checked against public
test vectors, but I have no known-answer candidate specific to this puzzle to certify the
mapping from image to key, so every row below is "uncertified" in the sense that a clean run
proves the tested candidates are wrong, not that the harness would have caught every possible
right answer. I also flag near-misses (an ETH address starting with the same 2 bytes, `ff21`)
as an extra check; none occurred in any family below.

## Geometry-derived candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Building height/width/roof-y/x0 sequences (raw, sorted ascending, sorted descending, interleaved), joined with 5 separator styles, padded left/right to 32 bytes, first/last 32 bytes, 2-hex-digit encoding per value | about 460 candidates total across this and the next 3 rows | SHA-256, double SHA-256, Keccak-256, compared to target address | 0 match, 0 near-miss (no derived address even starts with `ff21`) | uncertified (no known-answer vector for this puzzle) | 2026-06-13 |
| Raw pixel hashes: grayscale channel, alpha channel, full PNG file, first/last 32 bytes of the flat grayscale array | included above | SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| cHRM chunk (32 bytes) and its byte-reversed form, raw and hashed | included above | direct, SHA-256, Keccak-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Object counts (12 buildings, 1 large sail, 5 small sails, 2 clusters, left/right counts) as a byte sequence | included above | SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Matrix reshape of the grayscale channel at 7 column widths, first/last row and column strips | 56 strips | first 32 bytes, SHA-256 | 0 match, 0 near-miss | uncertified | 2026-06-13 |
| Value-band pixel masks (bands including 240 to 245, 235 to 254, 248 to 254, 1 to 30) | 4 bands | SHA-256, first 32 bytes | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Metadata-derived candidates (the date:create / date:modify anomaly)

The PNG's own `tEXt` chunks (confirmed present in `clues/arweave-puzzle-11.png`, reproduced
2026-08-16) read `date:create 2020-03-30T11:38:07+03:00` and
`date:modify 2020-03-30T11:34:44+03:00`: the modify timestamp precedes the create timestamp,
an anomaly present only in this puzzle and its sibling puzzle #9.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| ISO date strings, digit strings, Unix epochs, and their difference/sum/XOR, in decimal and big/little-endian 4 and 8-byte encodings, alone and concatenated or XORed with the address and the cHRM bytes | dozens of encodings times {SHA-256, double SHA-256, Keccak-256, BLAKE2s, first 32 bytes, last 32 bytes} | direct address comparison | 0 match, 0 near-miss | uncertified | 2026-06-13 |

## Alpha channel and sibling-puzzle-calibrated candidates

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| 260 near-white pixels from the sibling puzzle #9's own 8-level image, tested as a carrier under many bit orders (raster, polar, radial), bit widths (1 to 3 bits per pixel, MSB and LSB first), and symbol mappings, plus several passphrase guesses hashed with SHA-256, double SHA-256, and Keccak-256 | several hundred combinations | address comparison, calibrated against puzzle #9's real (and already spent) address as a positive control | 0 match, 0 near-miss on #9 itself (so the method is confirmed not to reproduce the known #9 answer either) | yes, on the #9 positive control only | 2026-06-13 |
| Container-level myths (embedded executable or filesystem inside the PNG) | full file | binwalk, manual chunk inspection | refuted: file is a clean, valid PNG (IHDR, gAMA, cHRM, bKGD, pHYs, 22 IDAT, 3 tEXt, IEND chunks), 0 bytes after IEND; the "executable" reports from other solvers are binwalk false positives on near-random decompressed pixel bytes | yes (direct chunk inspection) | 2026-06-13 |
| Alpha channel as a data carrier | full channel | direct pixel inspection | 434 pixels have alpha under 255, all clustered on the large sailboat's outline (an anti-aliasing halo from a copy-paste), values 1 to 30, consistent with a smoothed edge rather than structured data | yes | 2026-06-13 |

## What the ~460-candidate geometry sweep and the metadata sweep together rule out

Between the two families above, on the order of 1,000 candidates were checked, all through the
same address-comparison harness, with 0 matches and 0 near-misses anywhere. This rules out
every direct, single-transform reading of the measured geometry and the metadata anomaly that I
was able to enumerate. It does not rule out a reading that depends on information outside this
image, such as the promised but never-delivered "$100" hint (see "Open leads, ranked").


## Bounded extraction tests, 2026-09-05 (contributed by @BorisLoveDev, PR #21)

The exact standard Ethereum address verifier was calibrated with the public Ethereum
eth-keys README vector (private bytes 01 repeated 32 times -> address
0x1a642f0E3c3aF545E7AcBD38b07251B3990914F1). Synthetic carrier controls below test each
specified decoder; they do not establish that it is the author's intended encoding.
Recorded prize checks at blocks 0x18b51dc and 0x18b5222: 1 ETH, outgoing nonce zero.

| Hypothesis | Space | Method | Result | Witness | Runtime | Date |
|---|---|---|---|---|---|---|
| Isolated ASCII hex64 in L/A/LA/AL bitstreams: eight raster orientations, eight single planes plus low 2/3/4 bits in both pixel-bit orders, both byte-bit orders, offsets 0..7 | 7168 streams | regex extraction, any extracted scalar compared by exact ETH address | 0 hex64 occurrences; exhausted for this scope | 24 independently encoded synthetic carriers recover the known scalar and expected address | 46.493 s; estimate 46.563 s | 2026-09-05 |
| Raw 256-bit windows in the anomalous first image row, whole row or nonwhite-only; 14 bit selections, both raster directions, grayscale inversion, both byte-bit and scalar-byte orders | 626336 windows with variants, 79863 unique valid scalars; prior raw full-image endpoint keys excluded | exact ETH address compare; 79866 stream records including controls | 0 match; exhausted | raw synthetic first-row carrier recovers key at bit offsets 0/672/1344; actual comparison stream recovers controls at head/middle/tail | 1.515 s; estimate 1.478 s | 2026-09-05 |
| Standard Code128/ITF in original image, six visible object crops, and three 9-row profiles per crop, three binarizers | 75 puzzle decoding jobs + 6 controls | zxing-cpp 2.3.0, full hex64 payloads eligible for exact ETH compare | 0 barcodes decoded | both barcode formats recover public key vector across all three binarizers before search; six controls recovered within run | 0.045 s; conservative estimate 0.553 s | 2026-09-05 |

The ASCII scan does not cover spaced, encrypted, compressed, or raw binary payloads.
The first-row test does not cover arbitrary positions across the full canvas. The barcode
negative does not rule out a custom stroke-count code. No transaction was constructed or sent.

| Further hypothesis | Space | Method | Result | Witness | Runtime | Date |
|---|---|---|---|---|---|---|
| One unconfirmed sixteen-number skyline transcription from the original Reddit discussion, forwards/backwards, six entropy encodings per direction | 60 raw candidates; 12 entropy inputs x 2 seed methods x 62 ETH paths = 1488 HD derivations; 1923 checks with controls | raw padding/SHA256/double-SHA256/Keccak; BIP39 empty-passphrase entropy or direct BIP32 seed; exact ETH address | 0 match; exhausted for this transcription | 3 raw-key controls, 3 public Hardhat account controls, all recovered in-stream | 0.276 s; estimate 0.293 s | 2026-09-05 |
| Zlib or gzip payload in the same 7168 pixel bitstreams as the ASCII scan | 7168 streams; zlib headers 7801/785e/789c/78da or gzip magic, EOF and checksum required, max 1 MiB input/output per trial | exact 32-byte raw scalar or isolated ASCII hex64 from a valid decompressed payload | 0 valid archives, 0 candidates | 48 synthetic compressed-payload controls, all recover the public key/address vector | 14.514 s; 752.170 streams/s calibration; estimate 14.295 s including interleave margin | 2026-09-05 |

The sixteen-number row is one community transcription, not an author-supplied key
format. Its 62 paths are the union of m/44'/60'/0'/0/i, m/44'/60'/0'/i and
m/44'/60'/i'/0/0 for i=0..20. The six entropy encodings are ASCII digits, one byte per
height, packed hexadecimal left/right padded to 16 bytes, and decimal integer in
16-byte big/little endian form. The negative does not exclude other segmentations.

A separate stroke-group measurement produced 26 groups with a fixed threshold and
changed with the threshold. It supplied no justified key sequence and is not counted
as a witnessed key-search negative. The later NFT copy links back to the original
puzzle post; it did not provide an earlier drawing source or an extra author hint.

[Recorded reports and execution notes](../tools/REPRODUCE.md) preserve the scopes,
controls and runtime measurements. Raw-key and HD negatives do not establish the
absence of arbitrary image encodings, passphrases or other derivation paths.
