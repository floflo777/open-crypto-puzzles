# CaesarCoder: Genesis Block Wallet Puzzle (947,620 sats, [SOLVED])

On 2026-08-22 an author who at first stayed anonymous published a 252-byte OP_RETURN message in
block 963,629: a Bitcoin wallet generated only from data in Satoshi's genesis block, "extremely
low" entropy, nothing backed up. The prize was the first output of that same transaction, a 2-of-2
P2WSH address, and it grew every time someone paid for a hint: the author answered questions on
chain and relayed every payment into the escrow, from 25,000 sats to 947,620 sats in eight weeks
and 123 transactions. On 2026-10-17 at 03:40 UTC a player swept all 117 outputs (935,266 sats net)
and the author then signed a message with PGP: CaesarCoder, github.com/caesrcd. The solution was
contributed by [Schum-io](https://github.com/Schum-io) (PR #44) and is replayed in
`tools/verify_solution.py`: the coinbase text's hex, passphrase `Satoshi Nakamoto`, and one
setting nobody searched, the PBKDF2 round count (181,505 and 200,913 instead of 2,048).

## At a glance

| | |
|---|---|
| Author | CaesarCoder ([github.com/caesrcd](https://github.com/caesrcd)), PGP fingerprint `E2A0 BF0D 72D7 4483 064D 4FF9 3049 5240 7A6E 5C38`, revealed on chain on 2026-10-17 |
| Published | 2026-08-22, OP_RETURN in block 963,629 ([transaction](https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77)) |
| Prize | 947,620 sats at the end (about $597 at BTC = $63,000, the 2026-08-16 snapshot); it started at 25,000 sats and grew with each paid question |
| Chain | bitcoin |
| Escrow | `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj` ([explorer](https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj)) |
| Last on-chain check | 2026-10-17: 120 outputs funded, 120 spent, balance 0 |
| Status | SOLVED; swept 2026-10-17, solution in this folder (contributed by Schum-io, PR #44) |
| Puzzle type | multisig, bip39-seed |
| Target format | P2WSH 2-of-2 (`OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG`), each key from its own 12-word BIP39 seed plus a passphrase, BIP48 path `m/48'/0'/account'/2'/<0;1>/*` |
| Certified oracle | yes (`tools/oracle.py --selftest`); `tools/verify_solution.py` rebuilds both keys and reports MATCH |
| What remains | nothing |
| Series | none |

## The puzzle as published

The author had no website, no forum thread and no handle until the end. Every message is an
OP_RETURN in a transaction paid to the escrow. All 123 transactions, with every question and
answer verbatim, are in [clues/author-posts.md](clues/author-posts.md) and
[data/on-chain-dialogue.json](data/on-chain-dialogue.json).

Announcement, 2026-08-22 19:45:38 UTC, block 963,629:

> "I made a Bitcoin puzzle using information contained in the genesis block created by
> Satoshi to generate the wallet. The entropy is extremely low. I didn't even need to back
> anything up. Everything I needed was already in the genesis block. Good luck!"

Hint channel, 2026-08-23 01:51 UTC:

> "If you have a question, you can include it with a transaction sent directly to this
> address, and I will reply with a hint. Larger payments receive better hints. Dust
> transactions will be ignored."

The answers that shaped the solution, in order (questions paraphrased, answers verbatim):

| Date (UTC) | Question | Author's answer |
|---|---|---|
| 2026-08-23 | script type? | "The witness script is a multisig." |
| 2026-08-23 | how many keys? | "Two keys, both required. The rest is for you to derive." |
| 2026-08-28 | derivation rule? | `root -> multisig -> mainnet -> genesis_data -> script_type` (the BIP48 levels) |
| 2026-09-10 | what is root? | "root = the master key derived from the BIP39 seed; genesis_data = some data from the genesis block used as the BIP48 account number." |
| 2026-09-11 | words, passphrase? | "BIP39: 12 words; Passphrase: Y" |
| 2026-09-14 | passphrase? | "Who received the first transaction?" |
| 2026-09-15 | passphrase and entropy | "No, the passphrase is a name." and, on 2026-09-16, "It's a 128-bit digest." |
| 2026-09-24 | both key origins (encrypted reply, decrypted by the buyer) | two different seeds, master fingerprints `0852014c` and `040e2791`, path `m/48'/0'/<account>'/2'` |
| 2026-09-25 | what is hashed? | "It's a contiguous piece of the genesis block, exactly as a standard tool displays it" |
| 2026-09-27 | which tools? | "bitcoin-cli, cut, jq, tr, sha256sum, iancoleman/bip39, OogaBoogaX/entropylab" |
| 2026-09-30 to 10-03 | shape of the text | hex text, `cut -b N-M`, same length for both keys, passphrase letters and spaces only, same passphrase for both seeds |
| 2026-10-05 | passphrase words | exactly two words, one space, each a given name or surname of the recipient |
| 2026-10-06 | where the cut comes from | the raw block hex, copied from an explorer, the cut does not start at byte 1 |
| 2026-10-07 | which explorer and length | mempool.space, the usual lowercase 570-character raw hex, hashed text of even length 66 or more |
| 2026-10-09 | passphrase shape | the first word is shorter than the second; no word has exactly 3 letters |
| 2026-10-10 | the "2^23" count of 2026-09-26 | cut ranges times passphrase forms |
| 2026-10-14 | exact `tr` command | `tr -d '\n'` |
| 2026-10-16 | counts | 1 to 32 passphrase forms, more than 2^17 cut ranges, no typo; both BIP48 accounts are the raw value of a named header field, one of them at least 2^22 |
| 2026-10-16 and 17 | test vectors with "your own procedure and settings unchanged", passphrase `Test Example` | see "What is understood" |

## What is understood

### Mechanism

1. Take the raw genesis block as hex (570 characters, as served by mempool.space or
   `bitcoin-cli getblock <hash> 0`), cut a contiguous range with `cut -b N-M`, strip the newline
   with `tr -d '\n'`, and hash it with `sha256sum`.
2. The first 32 hex digits of the digest are pasted into Ian Coleman's BIP39 tool as Hex entropy,
   which gives 12 words. Two different cuts give the two cosigner seeds.
3. A two-word name is the passphrase, the same for both seeds.
4. Each seed gives a BIP48 account key `m/48'/0'/account'/2'`, the account being the raw value
   of a header field (time 1231006505 or nonce 2083236893 are the fields above 2^22), and the
   two account keys form `wsh(sortedmulti(2, ...))`.

### The step everyone missed

On 2026-10-06 a player asked for a test vector: the text `000000000019d6689c08`, passphrase
`Test Example`, "same wallet software as the puzzle". The author answered first word `host`,
fingerprint `b7f4182b`, which is exactly the standard BIP39 result (PBKDF2-HMAC-SHA512, 2048
rounds, salt `"mnemonic" + passphrase`). Searches were then run on that standard pipeline.

On 2026-10-16 and 17 other players asked for vectors computed with "your own procedure and
settings unchanged". For the same text and passphrase the author answered `3bc42789`, not
`b7f4182b`. So the puzzle's own seed step differs from standard BIP39. Two hours after the last
vector, the escrow was swept. The transaction that sent "My GPU searched everywhere except the
PBKDF2 settings. Well played!" spends escrow outputs, so it comes from someone who held the keys.

Author vectors for cosigner `0852014c`, passphrase `Test Example`, all computed with the puzzle
settings:

| Text fed to the pipeline | Master fingerprint |
|---|---|
| `cut -b 1-1` of the raw hex, or the literal text `0` | `e4caa034` |
| `cut -b 2-2`, or the literal text `1` | `9fb54bad` |
| `cut -b 3-3` | `e4caa034` |
| `cut -b 1-4` | `e79c9765` |
| `cut -b 1-66` | `9290f941` |
| `cut -b 263-400` | `68ab4226` |
| `cut -b 1-2000` | `8b9b2fea` |
| `cut -b 2-67` | `c85bcea3` |
| the literal text `000000000019d6689c08` | `3bc42789` (the 2026-10-06 standard answer was `b7f4182b`) |

The missing setting is the PBKDF2 round count: 181,505 for cosigner `0852014c` (see
"Solution"). With it, 8 of the 9 vectors above reproduce exactly, `3bc42789` included (2,048
rounds gives `b7f4182b`). The one that does not is `c85bcea3` for `cut -b 2-67`: 181,505 rounds
give `d463151e` (with a final newline `f1f02043`), so that answer looks like an author error. My
earlier search had stopped at 30,000 rounds.

### Derivation and oracle

```
python3 tools/oracle.py --selftest              # must print SELFTEST OK
python3 tools/oracle.py <keyA hex> <keyB hex>   # 32-byte private keys or 33/65-byte public keys
```

The oracle rebuilds the 2-of-2 script in both key orders, hashes it, and compares all 32 bytes
with the witness program `4dae67a9872f1402109f9670276afc2c0758f895aafddcd089795771b7964833`.
Certified against the BIP-173 P2WSH vector and a real 2-of-2 spent in block 963,629
(tx `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`).

### Established facts

1. The escrow received 120 outputs, 947,620 sats in total, every one of them spent on
   2026-10-17 (mempool.space, checked the same day).
2. The sweep, `1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b` in block
   971,803, spends 117 outputs and pays 935,266 sats to
   `bc1qdu8mh9qjtjhy89mvhmcgf66ul6ld92rdr6qzad`. Two later transactions spend the last outputs:
   `4b2d29ec` (with the PBKDF2 message) and `d25aa1b7`.
3. The receiving address had asked two paid questions before: 10,000 sats on 2026-09-14 and
   51,000 sats on 2026-09-24 for the two public keys. From that address alone the solver spent
   about 62,000 sats including fees; it may have used other addresses too. On 2026-10-17 it sent
   10,000 sats to the author's address and a thank-you note to the escrow.
4. The author's PGP message (`473a314b`, 2026-10-17 17:01 UTC) names CaesarCoder and
   github.com/caesrcd, whose public repositories are Bitcoin node tools.
5. Several paid answers were encrypted to the asker and are unreadable to anyone else: the public
   keys (three buyers), the BIP48 accounts (two buyers, likely declined: the author refused
   every request for a value that isolates one secret), and one exchange with the solver on
   2026-10-16.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Every negative below assumed the
standard BIP39 seed step (2,048 rounds). The last two rows did contain the right cut and the
right passphrase, so the round count alone hid the answer from them.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Passes 1 and 2: literal readings of the August hints (raw keys, BIP32 seeds, BIP39 entropy, hashed roots, 214 paths), every ordered pair | 611,008 keys, 3.7e11 ordered pairs | CPU keys, GPU pairing, exact compare | 0 match | yes, 9 of 9 | 2026-08-29 |
| Pass 3: 329 entropies from 16-byte windows times 53 passphrases times BIP48 accounts | 1.57e6 keys, 2.46e12 pairs | same | 0 match | yes, 9 of 9 | 2026-09-12 |
| Seed fingerprints: every substring of every bitcoin-cli and explorer output line, as is or uppercase, with or without a newline, times up to 7.3 million name spellings (Hal Finney and Satoshi Nakamoto, case variants, hashcat rules) | 8.32e10 seeds over 28 runs (sum of the per-run reports) | GPU master fingerprint against `0852014c` and `040e2791` | 0 seed | yes, 3 of 3 per run | 2026-09-24 to 10-05 |
| Every substring of the 570-character raw hex times 20 two-word names that fit the 2026-10-09 shape, 8 case forms each | 2.5e7 seeds | same | 0 seed | yes, 3 of 3 | 2026-10-11 |

## Open leads, ranked

None: the puzzle is solved and the solution is reproduced below.

## Solution

Contributed by [Schum-io](https://github.com/Schum-io) in PR #44, opened 2026-10-17 06:18 UTC,
under three hours after the sweep, when no other source had the answer. The author acknowledged
the solve on chain ("Shoutout to the player who cracked the puzzle!").

| | |
|---|---|
| Date | 2026-10-17 03:40:20 UTC, block 971,803 |
| Payout | 935,266 sats to `bc1qdu8mh9qjtjhy89mvhmcgf66ul6ld92rdr6qzad` ([transaction](https://mempool.space/tx/1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b)) |
| Answer | mnemonic from `cut -b 263-400` of the raw hex, passphrase `Satoshi Nakamoto`, PBKDF2 rounds 181,505 and 200,913, both keys at `m/48'/0'/1231006505'/2'/0/0` |
| Key material disclosed | yes (the escrow is empty) |

1. Take the raw genesis block as one lowercase hex line of 570 characters
   ([data/genesis-block.hex](data/genesis-block.hex), the same bytes mempool.space serves at
   `/api/block/<hash>/raw`).
2. `cut -b 263-400 | tr -d '\n'`: the 138 hex characters of the coinbase text,
   `5468652054696d6573...62616e6b73`, which decode to
   `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks`.
3. `sha256sum` of those 138 ASCII characters; the first 32 hex digits of the digest are the
   128-bit entropy `c020f55f60b8193bd5cac836769dbf76`.
4. The entropy as 12 English BIP39 words:

```
scan amateur fit scrap light over fire flip cushion reject hurt ugly
```

5. BIP39 passphrase `Satoshi Nakamoto` (capital initials, one space), the same for both cosigners.
6. Seed = PBKDF2-HMAC-SHA512(mnemonic, "mnemonic" + passphrase, rounds, 64 bytes) with a
   non-standard round count per cosigner; the two cosigners share one mnemonic:

| Cosigner | PBKDF2 rounds | Reading | Master fingerprint | Public key at `m/48'/0'/1231006505'/2'/0/0` |
|---|---|---|---|---|
| A | 181505 | 18:15:05 UTC, the genesis time | `0852014c` | `027b497b1d82986ebe11bca71108ca43446c00edb069cc839638a0b76529130906` |
| B | 200913 | 2009/1/3, the genesis date | `040e2791` | `033614b02e8e3aeeed9e14ac67839f85d54b694eafd91ca07f1afeb06510832ec1` |

7. Witness script `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG`; its SHA-256 is the escrow's witness
   program, so `tools/oracle.py` reports `MATCH order=AB`.

```
python3 tools/verify_solution.py   # replays steps 1 to 7 and asserts every intermediate value
```

Checked independently on 2026-10-18: both public keys give a MATCH with a separate oracle, and
the round count reproduces the author's published test vectors (see "The step everyone missed").

What it teaches: the one parameter nobody searched is one that a BIP39 tool exposes as a custom
field. Several passes here had the right cut and the right passphrase; the round count was never
asked about. When an author names the tools, enumerate every setting those tools let a user
change, not only the ones the BIPs fix. And a test vector certifies a setting only when it is
computed with the puzzle's own settings: the 2026-10-06 vector was standard, the 2026-10-16
vectors were not.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | all 123 escrow transactions with their OP_RETURN text, verbatim |
| `data/on-chain-dialogue.json` | the same ledger as data: attribution, amounts, inputs, text, fetched 2026-10-17 |
| `data/genesis-block.hex` | the raw genesis block, 285 bytes |
| `analysis/tested.md` | the negatives ledger with exact scope |
| `analysis/leads.md` | notes behind the leads, kept as written while the puzzle was open |
| `tools/oracle.py` | two keys to 2-of-2 P2WSH, both orders, exact match; `--selftest` |
| `tools/verify_solution.py` | rebuilds both keys from `data/genesis-block.hex` and checks them with the oracle (by Schum-io, PR #44) |
| `tools/candidates.py` and the `check_*.py` scripts | key generators for passes 1 to 3 and the contributed constructions |

## Sources

- Announcement transaction, block 963,629, 2026-08-22: https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77
- Escrow address and full dialogue: https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj
- Sweep transaction, 2026-10-17: https://mempool.space/tx/1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b
- Author's signed message, 2026-10-17: https://mempool.space/tx/473a314bcb3f5abc8dc4500e8d0ab80525ff65a846d55406c1e1e10fa8c8e46c
- Author on GitHub: https://github.com/caesrcd
- Galaxy Research, first public report, X, 2026-08-23: https://x.com/glxyresearch/status/2091349771952742566
- crypto.news, 2026-08-23: https://crypto.news/bitcoin-puzzle-hides-wallet-key-in-genesis-block-data/
- Tools named by the author: https://iancoleman.io/bip39/ and https://github.com/OogaBoogaX/entropylab

Credits: @Schum-io (PR #44) for the solution and `tools/verify_solution.py`; @BorisLoveDev (PR #21) for the six 2026-09-05 bounded constructions; the players who
paid for the questions quoted above.
