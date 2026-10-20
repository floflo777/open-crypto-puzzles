# Calibration: solved blocks verified end to end

Each entry below was recomputed from the published solution string, through the
derivation, to an escrow that was funded and later swept on chain. They are
references for the conventions the author used, not hypotheses about Real Big
Block. Re-run them with `python3 tools/calibration_check.py` from this folder.

| Block | Solution string | Hash | Mnemonic | Index | Escrow |
|---|---|---|---|---|---|
| Run-1 Block 13 | `Second Second Life Second Coming I thought xXJ` | SHA-256 | 24 words | 0 | `1GJPyUZvBE8MewEZyRx999p5JbVy8wbmWE` |
| Run-2 Block 48 | `Think different TOMI Apple slogan` | MD5 | 12 words | 0 | `19NR1m283F8npNdauDjQgbnEiR5cA2mdcp` |
| Run-2 Block 69 | `madam TOMI palindrome` | MD5 | 12 words | 0 | `17rkDa7xXHuK1TyzHExcj9e229ooKef8yU` |

All derivations use BIP39 from the raw hash bytes as entropy, then BIP44
`m/44'/0'/0'/0/i`, P2PKH, UTF-8 text with no trailing newline.

## Run-1 Block 13

- Reddit post `bb4c7q`, 2019-04-09. Question: "What are the first seven words in
  the hint to block 77?" Format `word1 word2 word3 word4 word5 word6 word7 xXJ.`
- Solution string `Second Second Life Second Coming I thought xXJ`, first
  published by e1976g in issue #39, independently re-derived here.
- SHA-256 `2a799f952abe95d13bdeea53ba5a9e075178b751bf16ccd75ddbed0aea9afc14`,
  used as 256-bit entropy (24-word mnemonic), address at index 0.
- Funding tx `3ad89ff0f48bfba17b28dedd5972a69bd3ac8acc73816048ab3ee566b71c1849`
  (0.007 BTC, 2019-04-09). Sweep tx
  `7ec179b405afe98e97c7e6d0d393301bbfeed8d73d445d801c8f9b4af242750e`
  (2019-07-23) to `1ByZvMzApZUUQSkudevtuPq8d6yzS5NtMp`.
- The "hint to block 77" is the "Second" chapter itself. The heading numerals
  `I.` and `1.` are not counted as words.
- The sweep date equals the chapter's modifyDate (2019-07-23).

## Run-2 Block 48

- Reddit post `c4ndaa`. Solution string `Think different TOMI Apple slogan`, as
  stated by puzzleponky in the block thread.
- MD5 `2c142b58c037bc30c44da6277c2cff91`, matching the author's published prefix
  `2c1`. Address at index 0.
- Funding tx `0601c2d6b06a9dee4491eeb2123a72bfc132dab3e1bda04fdb79e6fd914b6ccb`
  (0.007 BTC, 2019-06-24). Sweep tx
  `930486a0af9addbe3ba73cf337aa3d1c77ffdfada166d0125643c8db231facc6`
  (2019-06-24) to `129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN`.

## Run-2 Block 69

- Reddit post `cdentq`. Solution string `madam TOMI palindrome`, as stated by
  puzzleponky in the block thread.
- MD5 `a8f7e33a0aaeb16f61a5b09cff038846`, matching the author's published prefix
  `a8f`. Address at index 0.
- Funding tx `2411287307338fd0882d3827319af6574725e5c637396669eeb18242a163add7`
  (0.007 BTC, 2019-07-15). Sweep tx
  `6e56bb4c0df5d645030c67f52fce239e9f0eb2b27f868b344618ee85ffa9031b`
  (2019-07-15) to `129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN`.

## What these establish

- The funded key is at index 0 in both runs. This agrees with the author's note on
  the Real Big Block wallet that "the first one" is the key used.
- The hashed string is the bare solution with single spaces between fields: no
  wrapper, no trailing newline.
- The hash algorithm depends on the period: SHA-256 for Block 13 (April 2019), MD5
  for the run-2 blocks (June and July 2019). The switch to MD5 is described in the
  "Mistakes" part of the Wattpad story.

Credits: moonflightrocket-ops (re-derivation, escrow and sweep data); e1976g
(Block 13 solution string); puzzleponky (Block 48 and 69 solution strings).
