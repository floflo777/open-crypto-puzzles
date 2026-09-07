# Reproduce the bounded image extractions

Run from the repository root with Python 3.13.3. Install `requirements.lock`, then
`python -m pip install -r 2-mid-prizes/arweave-puzzle-11-1eth/tools/requirements-research.txt`.
The extra barcode dependency is zxing-cpp 2.3.0. No vendor binaries are committed.

The existing source image has SHA256
`c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1`.
Each published script verifies that image hash when reading the original image.
The sixteen-number script uses the public transcription instead.

Set `PUZZLE_RUN_DIR` to a private directory outside the checkout. For an offline
reproduction of these dated runs, copy [funding.json](../analysis/2026-09-05/funding.json)
and [funding-strokes.json](../analysis/2026-09-05/funding-strokes.json) there, preserving
the file names. They are historical preflight snapshots, not live balance guarantees.
Before any new research, run the repository escrow checker and verify current funding.
The scripts perform no network operations. Reports and any hit material go to the
external directory with restrictive permissions; public summaries contain counts only.

Run each script separately:

```sh
python 2-mid-prizes/arweave-puzzle-11-1eth/tools/scan_bits.py
python 2-mid-prizes/arweave-puzzle-11-1eth/tools/scan_top_row.py
python 2-mid-prizes/arweave-puzzle-11-1eth/tools/check_barcodes.py
python 2-mid-prizes/arweave-puzzle-11-1eth/tools/check_sixteen_bars.py
python 2-mid-prizes/arweave-puzzle-11-1eth/tools/scan_compressed.py
```

Each run checks known controls, measures its rate and limits the search to under
10 minutes. A time-limit exit is incomplete, never an exhausted negative. The two
bitstream scripts also support `--selftest` for their synthetic codec controls.

## Recorded results

- [ASCII bitstreams](../analysis/2026-09-05/bits-result.json): 7168 streams, zero payloads.
- [First-row windows](../analysis/2026-09-05/top-row-result.json): 79863 unique valid candidates, zero target matches.
- [Code128/ITF](../analysis/2026-09-05/barcode-result.json): 75 puzzle jobs, zero decoded barcodes.
- [Sixteen-number reading](../analysis/2026-09-05/sixteen-bars-result.json): 60 raw candidates and 1488 HD derivations, zero matches.
- [Compressed bitstreams](../analysis/2026-09-05/compressed-result.json): 7168 streams, zero valid archives.
- [Publication provenance](../analysis/2026-09-05/publication.json): hashes of original and portable scripts, packaging differences.

Synthetic payload controls certify the explicitly tested codecs, not the author's
intended encoding. The barcode tests do not cover QR or custom stroke-count codes.
The two bitstream scans cover different payload representations over the same carriers;
their counts must not be added as independent carrier coverage.

## Sources

- [Ethereum key/address vector](https://raw.githubusercontent.com/ethereum/eth-keys/master/README.md).
- [Public Hardhat test account](https://github.com/NomicFoundation/hardhat/issues/3325).
- [Original discussion and community sixteen-number transcription](https://www.reddit.com/r/ethtrader/comments/g6kefu/there_is_1_eth_hidden_in_this_crypto_puzzle_can/).
- [Drawing discussion and later NFT reference](https://puzzling.stackexchange.com/questions/97537/image-steganography-hidden-message-inside-image-png-8-bit-grayalpha).
- [Original image](https://arweave.net/CzITHnEIlkQw9SbaX5futCzFrKk1qe_NwvWnIBmP2fY).
