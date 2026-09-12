# Dead ends

Puzzles that are not workable for a reason other than difficulty: unfunded, custodial, swept
by a third party, solved by someone else, suspected fake, a contract with no exit path, an
author who died before publishing the rest of the material, or a window that closed. Every
entry states its reason as one of a fixed set of words, the date it was verified, and what
would reopen it. Kept here rather than deleted, because a documented dead end saves the next
reader from re-running the same dead-end research.

<!-- generated:start -->
| Puzzle | Announced | Why | Verified | Lesson |
|---|---|---|---|---|
| [Commander U Riddle for 8.5 BTC](commander-u-puzzle-8-5btc/) | 8.50099081 BTC | suspected-fake | 2026-08-16 | 4 of 6 fragments are unrecovered; one has no published checksum at all, and 3 do not match the MD5 of any base58 string of the stated length under any of 28 standard transforms tried; the missing piece is the original 2019 channel with the sub-riddle answers, which I could not find, and which may never have existed as a real puzzle in the first place |
| Phemex Dorian Nakamoto 2.1 BTC puzzle | 1.1 BTC | swept-by-third-party | 2026-08-16 | Swept 2020-03-21; the sweep transaction exposed the public key. The chain, not the press, is the source of truth: a 2024 article calling it unclaimed was wrong by four years. |
| [ONFO / Dr. J.R. Forsyth Bitcoin Treasure Hunt](onfo-forsyth-1btc/) | 1 BTC | author-deceased-unfinished | 2026-08-16 | half of the announced material (segments 6 to 10) was never published, and the sole self-declared key holder died in 2023; no known method applies to an incomplete corpus |
| [Objective Thune: Le Secret de la Licorne](objective-thune-licorne-0-21btc/) | 0.21021 BTC | unobtainable-material | 2026-08-16 | the mechanism is fully specified and the oracle is ready; what is missing is which 3 of the 210 physical book copies hold the keys, a physical fact, not a computation |
| The Game of Satoshi (Season 1) | 0.21 BTC | custodial | 2026-08-16 | Custodial: the 24 words are a game answer submitted to a server, not a mnemonic controlling a wallet. Ask first: custodial or permissionless? If the answer goes to a server, there is no key to derive. |
| De Mint: Bitcoin Evangelism book puzzle | 3,146,386 sats | solved-by-others | 2026-08-16 | Puzzle 1 was cashed by a reader around October 2022 (author confirmed on camera); the escrow was never published. A podcast publish date is not an event date, and a coincidental amount match in a balance dump is not the escrow. |
| [Keysa: Crack the Seed Game](keysa-crack-the-seed-369ksats/) | 369,369 sats | swept-by-third-party | 2026-09-12 | swept on 2026-09-08 (block 966,260, 369,150 sats to bc1q82gz5dnpxnqmvzrkusm8yc0nt4dcqp8gd3y59j); the author confirmed the crack on X on 2026-09-10 without naming the solver; neither the 12 words nor the selection rule has been published; the negatives ledger stays as a record of what the selection rule is not |
| [Zodomo 11x11 Pixel Puzzles](zodomo-11x11-pixel-puzzles-0-05eth/) | 0.05 ETH | unfunded | 2026-08-16 | the active puzzle's escrow does not exist on Ethereum mainnet as of the last check; even once it does, its encoding scheme is not yet identified, and the strongest lead is a set of author-distributed hints in a gated community chat |
| BAM x AskABitcoiner 42k Seed Cipher | 42,100 sats | swept-by-third-party | 2026-08-16 | Swept 2026-06-05 by another solver; passphrase was an artwork title. Reusable: this maker's series uses BIP49 m/49'/0'/0'/0/0 and a passphrase equal to an artwork title, not a block height. |
| Wares Wallets (Solana video series) | 0.1 SOL | swept-by-third-party | 2026-08-16 | Checked escrows at 0 SOL; channel inactive since 2025-07-04. Reusable: Solana path m/44'/501'/0' (solana-cli/Solflare), not Phantom's .../0'/0'. Measure the real prize before the marketing number. |
| ZK Guess #31 (chainhackers, Base) | 0.0025 ETH | window-closed | 2026-08-16 | Secret 149 was identified, but a third party guessed it about 40 hours later and the puzzle forfeited. A zero-cost, positive-value action runs immediately. |
| Aenigma Shards (AESH NFT cryptogram) | 34 ETH | unfunded | 2026-08-16 | A promised total is not a funded prize: mint stalled at 72 of 100, contract holds 0 ETH, no puzzle ever released beyond a demo. Check the contract balance, not the marketing. |
<!-- generated:end -->

## Dead ends without a folder

Some dead ends never had enough live research to justify a folder of their own: one paragraph
in `rows.json` and in this section is the whole record. Each entry states what the puzzle
was, why it is dead, when that was verified, and one lesson.

## Excluded without research

Puzzles or promotions I chose not to onboard at all, in one sentence each:

- **Max Keiser 20 BTC**: matches a known scam pattern; not onboarded.
- **The Trading Handbook**: matches a known scam pattern; not onboarded.
- **DarthCoin and Phineas Fisher**: no author invitation to solve and claim a reward; out of
  scope by principle, regardless of any technical interest.
