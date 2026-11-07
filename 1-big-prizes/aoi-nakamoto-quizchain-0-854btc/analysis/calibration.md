# Calibration: solved blocks verified end to end

Each entry below was recomputed from its solution string, through the derivation,
to the escrow of the block. Every entry also has a check that does not depend on
the source of the string: the MD5 prefix the author published in 2019, a 2019
confirmation in the block thread, or an on-chain sweep. They are references for
the conventions the author used, not hypotheses about Real Big Block. Re-run them
with `python3 tools/calibration_check.py` from this folder.

All derivations use BIP39 from the raw hash bytes as entropy, then BIP44
`m/44'/0'/0'/0/i`, P2PKH, UTF-8 text with no trailing newline. Every escrow is at
index 0.

## Summary

| Block | Posted | Solution string | Hash | Independent check |
|---|---|---|---|---|
| Run-1 13 | 2019-04-09 | `Second Second Life Second Coming I thought xXJ` | SHA-256 | on-chain sweep 2019-07-23 |
| Run-2 48 | 2019-06-24 | `Think different TOMI Apple slogan` | MD5 | author prefix `2c1` |
| Run-2 56 | 2019-07-02 | `Maybe you were just unlucky to have an exit node without reverse lookup.` | MD5 | author prefix `b9f` |
| Run-2 57 | 2019-07-03 | `https://mobile.twitter.com/halfin/status/1153096538` | MD5 | author prefix `d26` |
| Run-2 58 | 2019-07-04 | `That means a lot coming from you, Hal.` | MD5 | author prefix `a2a` |
| Run-2 60 | 2019-07-06 | `Mayer Multiple` | MD5 | author prefix `e83` |
| Run-2 62 | 2019-07-08 | `Tanabata` | MD5 | author prefix `bf4` |
| Run-2 63 | 2019-07-08 | `I am omnipotent Aoi` | MD5 | puzzleponky, Reddit comment `etgx7js` (2019-07-10) |
| Run-2 66 | 2019-07-12 | `A young woman of Japanese ancestry who is very smart and sincere.` | MD5 | author prefix `dc5` |
| Run-2 67 | 2019-07-12 | `Thomas TOMI Harold Thomas Finney II` | MD5 | puzzleponky, Reddit comment `etn39ar` (2019-07-12) |
| Run-2 69 | 2019-07-15 | `madam TOMI palindrome` | MD5 | author prefix `a8f` |
| Run-2 70 | 2019-07-16 | `Victor/Victoria` | MD5 | author prefix `71a` |
| Run-2 72 | 2019-07-18 | `GND TOMI Green New Deal` | MD5 | author prefix `916` |
| Run-2 73 | 2019-07-19 | `carbon budget TOMI Grycoin solution` | MD5 | author prefix `f13` |
| Run-2 74 | 2019-07-20 | `PETM TOMI second time now` | MD5 | author prefix `c65` |
| Run-2 75 | 2019-07-20 | `reverse Turing test` | MD5 | author prefix `509` |

## Run-1 Block 13

- Reddit post `bb4c7q`, 2019-04-09. Question: "What are the first seven words in
  the hint to block 77?" Format `word1 word2 word3 word4 word5 word6 word7 xXJ.`
- SHA-256 `2a799f952abe95d13bdeea53ba5a9e075178b751bf16ccd75ddbed0aea9afc14`,
  used as 256-bit entropy (24-word mnemonic).
- Escrow `1GJPyUZvBE8MewEZyRx999p5JbVy8wbmWE`. Funding tx
  `3ad89ff0f48bfba17b28dedd5972a69bd3ac8acc73816048ab3ee566b71c1849`
  (0.007 BTC, 2019-04-09). Sweep tx
  `7ec179b405afe98e97c7e6d0d393301bbfeed8d73d445d801c8f9b4af242750e`
  (2019-07-23) to `1ByZvMzApZUUQSkudevtuPq8d6yzS5NtMp`.
- The "hint to block 77" is the "Second" chapter itself. The heading numerals
  `I.` and `1.` are not counted as words. The sweep date equals the chapter's
  modifyDate (2019-07-23).

## Run-2 Blocks 48 and 69

- Block 48 (Reddit `c4ndaa`): MD5 `2c142b58c037bc30c44da6277c2cff91`, escrow
  `19NR1m283F8npNdauDjQgbnEiR5cA2mdcp`. Funding tx
  `0601c2d6b06a9dee4491eeb2123a72bfc132dab3e1bda04fdb79e6fd914b6ccb`
  (2019-06-24), sweep tx
  `930486a0af9addbe3ba73cf337aa3d1c77ffdfada166d0125643c8db231facc6`
  (2019-06-24) to `129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN`.
- Block 69 (Reddit `cdentq`): MD5 `a8f7e33a0aaeb16f61a5b09cff038846`, escrow
  `17rkDa7xXHuK1TyzHExcj9e229ooKef8yU`. Funding tx
  `2411287307338fd0882d3827319af6574725e5c637396669eeb18242a163add7`
  (2019-07-15), sweep tx
  `6e56bb4c0df5d645030c67f52fce239e9f0eb2b27f868b344618ee85ffa9031b`
  (2019-07-15) to `129jw1GUGwiJbf4rL7qEANPbxvSRC5zfHN`.

## Run-2 blocks from July 2019

Escrows and funding transactions (the transaction id is the one linked in the
block post):

| Block | Reddit post | Escrow | Funding tx |
|---|---|---|---|
| 56 | `c88x4w` | `14tuS6dG5BXd1usDTUJduEDafFAuET74P5` | `f4bcd3b94827d049362e075d1122a9aeae4983a66debe92957b2c5069a2c4d68` |
| 57 | `c8lcsr` | `128cmgWEf3Cbor5ftazjtisNAfaiRhDgyk` | `5d2ba35d75f5f87276141aa73eb71b5790e33d0d602d2e03fd166ee3e64f958a` |
| 58 | `c8xwgt` | `1ExTyMrA43mFJukabSCicdjdgG5ZJ2y2R9` | `a926226f9861bc18c0e9361f194f0b0d7345591f7cbe015c5eb0f57316f39766` |
| 60 | `c9tbo0` | `1Gz9gHf4VyPorCDkpXtPg1xakQwGsJ7TP3` | `c21bd6238a66318a27b5bf54d7e3bdbd16f41c707336c8189f983199f0069bb9` |
| 62 | `cag7u1` | `1FPi8gMKZLD61dU3Zeb9vrwDc6yXpg4Ff7` | `1789a6b33846d93c8d0859377cd659d8196e2a6c10b4db816c83fe76e516557f` |
| 63 | `casci2` | `1MnL2VeHEX3wE2dvUWfJ3H3tb1AqRhxSWK` | `7de43ce4ae06ac4c2c7de9b8f9466af1a2f8fd6c3595310516b23a0584f5c983` |
| 66 | `cc5uka` | `1Lrh5pgaaKXdWC9u5bzp9ogsNktjPWJMij` | `58b9cb448f10f76d49f1db501ebb0ef49df2cbab3df402a20416eb524116ea70` |
| 67 | `cchy6l` | `18o7TyCU1zkXCiC5sZSyxBFAn3Nntb4MAw` | `4385d66a41d92939005b5767fb0c77b44f89e30a7d379f4d61d3e0fc9ac6b6f2` |
| 70 | `cds16v` | `19PShGAWvbs3LCvhhBUZFt2czPzEdQ17iX` | `a87465e396ac4502402d063269c2c518ab094bea07d26a8fe74c15b349fd4ad6` |
| 72 | `ces4vi` | `147dHipPd9eF7UTWrsxQhGDDySAmDUhXeG` | `8eca76a4b7793b6f8a0aed3b4f79d66d63846abde4c6590b8d0861694a572c3d` |
| 73 | `cf4rnd` | `1dG3cAWeKx67hnTVvpDCpUFwPiuqCn68X` | `e7f8fef0258cd5e76bec5846257cd9129d39cd5324765099c392a93950b8666e` |
| 74 | `cfhi1e` | `1P1BFMU7vnpzsaUtQCAvArVKQyeMgYtmPY` | `f2623d2b4679277ed587c6031ebd3662bc4b72387828b62c8975d14860cf1854` |
| 75 | `cfs3ld` | `15pmBkzmSyXg2KhYHMmauF3EjYNEvyiABS` | `c52c46d2831e8372393af09f66541647b6d1bda80694d87886ed7bd6cc5298be` |

## What these establish

- The funded key is at index 0 in every block listed (16 of 16, both runs).
- The hashed string is the bare solution: no wrapper, no trailing newline,
  single spaces between fields (`[solution] TOMI [TOMI]` becomes for example
  `GND TOMI Green New Deal`).
- Final punctuation is part of the string when it is part of the sentence
  (Blocks 56, 58, 66).
- Brackets in a `Format:` line are placeholders, not literal: Block 63 has
  `Format: (solution).` and hashes `I am omnipotent Aoi`.
- The hash algorithm depends on the period: SHA-256 for run-1 Block 13 (April
  2019), MD5 for the run-2 blocks (June and July 2019). The switch to MD5 is
  described in the "Mistakes" part of the Wattpad story.

Credits: BTCxanter (formerly e1976g) for the Block 13 string and the thirteen
July 2019 strings (issues #39 and #43); puzzleponky for the Block 48 and 69
strings and the 2019 confirmations of 63 and 67; hulkisliky22 for the escrow list
of Blocks 72 to 75; moonflightrocket-ops for the independent re-derivation and
the escrow and sweep data.
