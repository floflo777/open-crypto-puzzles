# Genesis Block Wallet Puzzle (946,540 sats, [SOLVED])

On 2026-08-22 an anonymous author published a 252-byte OP_RETURN message in block 963,629:
a Bitcoin wallet generated only from data in Satoshi's genesis block, "extremely low"
entropy, nothing backed up. The prize sat in a P2WSH 2-of-2 escrow and grew with every paid
question, from 20,000 sats to 946,540 sats over 118 funding transactions. A reader, Schum-io,
solved it on 2026-10-17 and swept the escrow in block 971,803: both cosigners come from one
12-word mnemonic whose entropy is the first 128 bits of SHA-256 of the coinbase text's hex,
with passphrase `Satoshi Nakamoto` and a non-standard PBKDF2 iteration count per cosigner,
181,505 (18:15:05 UTC) and 200,913 (2009/1/3). Every search in this folder, mine included,
had run at the standard 2,048 rounds.

## At a glance

| | |
|---|---|
| Author | anonymous, on-chain only (every message is an OP_RETURN sent to the escrow) |
| Published | 2026-08-22, OP_RETURN in block 963,629 ([transaction](https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77)) |
| Prize | 946,540 sats at the sweep (about $596 at BTC = $63,000, the 2026-08-16 snapshot); 168,779 sats on 2026-09-12, 142,779 sats on 2026-08-29 |
| Chain | bitcoin |
| Escrow | `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj` ([explorer](https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj)) |
| Last on-chain check | 2026-10-17: swept, 117 outputs spent in block 971,803; one 350-sat output (the author's farewell) arrived after the sweep |
| Status | SOLVED; 935,266 sats paid to the solver after an 11,274-sat fee |
| Puzzle type | multisig, raw-private-key |
| Target format | P2WSH (v0), witness script `OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG`, both keys at `m/48'/0'/1231006505'/2'/0/0` from one BIP39 mnemonic with passphrase and a custom PBKDF2 count |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the BIP-173 P2WSH vector and a real 2-of-2 spent in block 963,629); `tools/verify_solution.py` rebuilds the escrow from the raw block |
| What remains | none |
| Series | none |

## The puzzle as published

The author has no website, no forum thread and no handle. Everything is in OP_RETURN outputs
of transactions paid to the escrow, readable by anyone. Verbatim texts with txids are in
[clues/author-posts.md](clues/author-posts.md); the full ledger of the 119 transactions is in
[data/on-chain-dialogue.json](data/on-chain-dialogue.json).

Announcement, 2026-08-22 19:45:38 UTC, block 963,629,
`b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77`:

> "I made a Bitcoin puzzle using information contained in the genesis block created by
> Satoshi to generate the wallet. The entropy is extremely low. I didn't even need to back
> anything up. Everything I needed was already in the genesis block. Good luck!"

Hint channel, 2026-08-23 01:51 UTC:

> "If you have a question, you can include it with a transaction sent directly to this
> address, and I will reply with a hint. Larger payments receive better hints. Dust
> transactions will be ignored."

Answers given up to the September model (the questions are in the clues file):

| Date (UTC) | Author's answer |
|---|---|
| 2026-08-23 15:43 | "The witness script is a multisig." |
| 2026-08-23 21:08 | "Two keys, both required. The rest is for you to derive." |
| 2026-08-24 07:13 | "Yes, both keys use the same Genesis field, and there is no hash." |
| 2026-08-24 14:32 | "Both keys are derived independently from Genesis." |
| 2026-08-24 21:35 | "The Genesis Block is public. Which part of it matters is for you to discover." |
| 2026-08-28 23:15 | "Solve it to find out. Maybe both. If you can't check the Genesis block, you can also use The Times newspaper!" (asked: "Prize Address? Genesis field 32 bytes or smaller?") |
| 2026-08-28 23:50 | `Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type` (asked: "Can you give any hint about derivation offset/rule?") |
| 2026-09-06 19:41 | "I can't give hints without a question. Low-value transactions get bad hints; dust will be ignored." (a player had sent 1,000 sats with "give another hint") |
| 2026-09-10 21:33 | "root = the master key derived from the BIP39 seed; genesis_data = some data from the genesis block used as the BIP48 account number." (asked, 10,000 sats: "Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account?") |
| 2026-09-11 23:26 | "BIP39: 12 words; Passphrase: Y; Entropy: The data needed to solve it is publicly available in the genesis block." (asked, 10,000 sats: "BIP39 entropy: genesis bytes/puzzle text/img/other? words 12/24? passphrase Y/N?") |

From 2026-09-14 the channel became busy: a dozen wallets sent some fifty questions, several of
them in Electrum-encrypted form, and four players each paid 50,000 sats for the two public
keys, delivered encrypted. The answers that fixed the construction, in order (the rest,
including the Y/N shape answers and their questions, are in the clues file):

| Date (UTC) | Author's answer |
|---|---|
| 2026-09-14 16:15 | "Passphrase: Who received the first transaction? That's all I've got to say. What built the wallet are the tools that support BIPs 32, 39, and 48." |
| 2026-09-15 03:19 | "No, the passphrase is a name. The entropy isn't the raw 16 bytes." |
| 2026-09-15 15:22 | "Perhaps... but figuring that out is part of the puzzle. The 12 words were generated from entropy." (asked whether both cosigners share the 12 words and the passphrase) |
| 2026-09-16 12:40 | "It's a 128-bit digest." |
| 2026-09-17 23:22 | "The genesis block data can be viewed in binary, hex, decimal, or ASCII. If you figure out which part is being used as the entropy, just try all four forms. Want a valuable hint? Send 50k sats and I'll reveal the public keys for this address." |
| 2026-09-24 02:51 | "First 128 bits of SHA-256 hash of the genesis block's entropy." |
| 2026-09-25 23:37 | "It's a contiguous piece of the genesis block, exactly as a standard tool shows it. I got it by copy-pasting the tool's output." |
| 2026-09-26 16:52 | (declining to give one master fingerprint) "The genesis block is only 2.5E-32 of the 2^128 possibilities. Revealing the seed's master fingerprint without the passphrase is basically giving away the entropy. All the secret pieces have to be cracked at the same time." |
| 2026-09-27 01:39 | "Apps/Tools used to generate the 12 words: bitcoin-cli, cut, jq, tr, sha256sum, iancoleman/bip39, OogaBoogaX/entropylab; Genesis block is extremely small. This will have to be uncovered via brute-force; Pasted from bitcoin-cli and also from an explorer." |
| 2026-09-30 23:11 | "1) hex; 2) substring/cut; 3) N" (hashed form, complete field or cut, trailing newline) and "1) N; 2) Y; 3) Y; 4) Y" (two different pastes for the two seeds, same passphrase, UTF-8 text hashed, first 32 hex of the digest as entropy) |
| 2026-10-03 00:20 | "1) Y; cut -b N-M: it deleted everything outside the selected range. 2) Y. 3) Key question of the passphrase: Who received the first transaction? That's all I've got to say. 4) N." |
| 2026-10-03 21:35 | "1) Y; 2) Y; 3) ¬_¬" (0852014c is the master fingerprint with the passphrase applied; both keys at `m/48'/0'/X'/2'/c/i` with small c and i) |
| 2026-10-05 17:24 | "1) N; 2) d; 3) Y." (the passphrase is exactly two words, given name and surname, one space) |
| 2026-10-07 20:03 | "1) b; 2) b; 3) Y; 4) d. 1) Y; 2) -; 3) c; 4) N." (mempool.space, copied from the page; the cut text is the usual lowercase 570-character raw block hex, the hashed text is 66 characters or longer) |
| 2026-10-14 00:08 | "tr -d '\n'" (asked: "What exact tr command did you use?") |
| 2026-10-16 02:38 | "1) Y; 2) Declined; 3) d; 4) Y." (the account numbers come from the block without hashing, as a named header field's raw value, at least 2^22) |
| 2026-10-16 22:01 | "1) e4caa034; 2) 9fb54bad; 3) e4caa034; 4) e79c9765; 5) 8b9b2fea; 6) 68ab4226; 7) 9290f941." (master fingerprints for `cut -b` 1-1, 2-2, 3-3, 1-4, 1-2000, 263-400, 1-66 with passphrase `Test Example`) |
| 2026-10-17 01:34 | "1) e4caa034; 2) 9fb54bad; 3) 3bc42789." (the same procedure on the literal texts `0`, `1`, `000000000019d6689c08`) |
| 2026-10-17 04:43 | "Shoutout to the player who cracked the puzzle! Thanks to everyone who joined in." (one hour after the sweep) |

The corpus is the genesis block itself, 285 bytes, public since 2009-01-03
([data/genesis-block.hex](data/genesis-block.hex)):

| Field | Value | Size |
|---|---|---|
| version | 1 | 4 bytes |
| previous block hash | 32 zero bytes | 32 bytes |
| merkle root (also the coinbase txid) | `4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b` | 32 bytes |
| time | 1231006505 (2009-01-03 18:15:05 UTC) | 4 bytes |
| bits | 486604799 (`0x1d00ffff`) | 4 bytes |
| nonce | 2083236893 (`0x7c2bac1d`) | 4 bytes |
| block hash | `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f` | 32 bytes |
| coinbase scriptSig | `04ffff001d0104` + `45` + text | 77 bytes |
| coinbase text | `The Times 03/Jan/2009 Chancellor on brink of second bailout for banks` | 69 bytes |
| the newspaper's own headline | `Chancellor on brink of second bailout for banks` | 47 bytes |
| coinbase output public key | `04678afdb0fe5548271967f1a67130b7105cd6a828e03909a67962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5f` | 65 bytes |

## What is understood

### Mechanism

The escrow is a native P2WSH output: the address encodes `sha256(witness script)`, and the
witness script is `OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG` with compressed keys, confirmed
by the sweep's witness. The solution reads the hints as follows:

1. "You can also use The Times newspaper" and "same Genesis field": the coinbase text. In the
   570-character lowercase raw block hex it occupies characters 263 to 400, so `cut -b 263-400`
   extracts exactly the 138 hex characters of the 69-byte text. The text was hashed as ASCII hex,
   not as the decoded bytes.
2. "It's a 128-bit digest" and "no hash" together: the entropy is the first 128 bits of SHA-256 of
   those 138 characters (the author counted the digest as entropy generation, not as a hash of
   a key), turned into 12 English BIP39 words.
3. "Who received the first transaction?": the passphrase is `Satoshi Nakamoto`, the name the author
   gave as the answer. Hal Finney, the recipient of the first Bitcoin transfer, was the obvious
   reading of the question, and the author declined on chain to confirm or deny it on 2026-10-10.
4. "root -> multisig -> mainnet -> genesis_data -> script_type" is BIP48: `m/48'/0'/1231006505'/2'`
   with the genesis timestamp as the account for both cosigners, then `/0/0`.
5. "Derived independently": the two cosigners differ only in the PBKDF2-HMAC-SHA512 iteration
   count that turns mnemonic and passphrase into the seed: 181,505 (the genesis time, 18:15:05
   UTC) and 200,913 (the genesis date, 2009/1/3), where BIP39 fixes 2,048. This is the one setting
   no on-chain question asked about; the author's answers about "the same wallet software" and
   the iancoleman tool, which exposes the count as a custom field, pointed at it only in hindsight.

### Derivation and oracle

```
python3 tools/oracle.py --selftest              # must print SELFTEST OK
python3 tools/oracle.py <keyA hex> <keyB hex>   # 32-byte private keys or 33/65-byte public keys
python3 tools/oracle.py --stdin                 # one "keyA keyB" pair per line
python3 tools/verify_solution.py                # rebuilds both keys from data/genesis-block.hex, must end in MATCH order=AB
```

The oracle rebuilds the 2-of-2 script in both key orders, hashes it, and compares all 32
bytes with the published witness program
`4dae67a9872f1402109f9670276afc2c0758f895aafddcd089795771b7964833`. No network, no false
positive. Measured on one CPU core: about 1,200,000 pairs/s once public keys exist, about
37,000 private-to-public derivations/s in Python.

### Certified against

1. The BIP-173 test vector for a P2WSH program
   (`1863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262` to
   `bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3`).
2. A real 2-of-2 P2WSH spent in the same block as the announcement, transaction
   `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`, input 0: the two
   public keys revealed in its witness, rebuilt into the script, hash to the address of the
   output it spends, `bc1q6vpcc5vdrg0dh0k4edkuvamvn27mwr4crxgl94yva9v9z240vysqr89ddy`.
3. Private key 1 derives the generator point, compressed and uncompressed.
4. Negative control: that revealed pair does not match the escrow.

### Established facts

1. The escrow received 946,890 sats in 118 outputs; 117 of them (946,540 sats) were spent by the
   sweep `1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b` in block 971,803,
   2026-10-17 03:40:20 UTC, paying 935,266 sats to `bc1qdu8mh9qjtjhy89mvhmcgf66ul6ld92rdr6qzad`
   with an 11,274-sat fee. The 118th output (350 sats) carries the author's farewell and arrived
   after the sweep. Confirmed on mempool.space on 2026-10-17.
2. The sweep's witness reveals the script `5221<keyA>21<keyB>52ae` with keyA
   `027b497b1d82986ebe11bca71108ca43446c00edb069cc839638a0b76529130906` and keyB
   `033614b02e8e3aeeed9e14ac67839f85d54b694eafd91ca07f1afeb06510832ec1`; `tools/verify_solution.py`
   rebuilds both from the raw block and the oracle reports `MATCH order=AB`.
3. Every payment sent with a question ended up in the escrow, so the jackpot is the sum of all
   hint payments plus the author's own 30,000 sats. Traced from the transaction inputs in
   `data/on-chain-dialogue.json`.
4. The author used a fresh P2WPKH change address for every message and, from late September,
   paid answers from a batch of 569-sat outputs prepared in a separate transaction. Response
   time to a paid question was between 1 and 10 hours in every case.
5. Three of the author's shape answers do not fit the solution: on 2026-10-01 the hashed hex
   was said to be at most 32 characters (it is 138), and the test vector `cut -b 2-67` with
   passphrase `Test Example` was answered `c85bcea3` on 2026-10-16, which neither 2,048 nor
   181,505 rounds reproduces (the solver reports no count up to 100,000,000 does), while the 2026-10-06 answer `b7f4182b` for the literal
   `000000000019d6689c08` is the 2,048-round value and the 2026-10-17 answer `3bc42789` for the
   same text is the 181,505-round value. The author's "unchanged procedure" was not constant
   across dates; the seven fingerprints of 2026-10-16 22:01 all reproduce at 181,505 rounds.
6. The word "genesis_data" sits exactly where BIP48 puts the account index; the timestamp
   1231006505 is under 2^31 and is the account for both cosigners.
7. The literal readings of hints 7 and 8 do not produce the keys: 447,916 distinct public
   keys built from the coinbase text and the other genesis fields (raw windows, BIP32 seeds
   and BIP39 entropy along 214 paths including every BIP48 path with a genesis integer as
   account), paired every way, give 0 match against the escrow, with the witness pair
   re-found at head, middle and tail. 2.0e11 ordered pairs in 103 s on one RTX 5080,
   2026-08-29 (`analysis/tested.md`).
8. The library-specific root constructions do not produce the keys either: hashed roots,
   a raw 64-byte extended key cut from the text, and a raw key with a zero chain code, along the
   same 214 paths, add 165,064 keys; the union of 611,008 keys paired every way gives 0
   match, witnesses re-found, 3.7e11 ordered pairs in 89 s, 2026-08-29.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md), including the exact list of texts,
windows, readings and derivation paths. Every pass below used the standard 2,048 PBKDF2 rounds,
so none of them could reach the keys; pass 3 even contained the right entropy and the right
account and missed on the passphrase and the round count. Reproduce with
`tools/candidates.py --write --pass 2` (about 17 s on 22 cores) and `engines/p2wsh_2of2_pairs`
(about 90 s on one RTX 5080), then `tools/candidates.py --verify` on the hits file.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Pass 1, families A to D: literal readings of hints 7 and 8 (raw keys, BIP32 seeds, BIP39 entropy from the coinbase text and the other fields, 214 paths), every ordered pair | 447,916 keys, 200,634,118,084 ordered pairs | CPU key generation (`tools/candidates.py`), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`), exact 32-byte compare, every hit re-derived on CPU | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-08-29 |
| Pass 2, A to D plus E (hashed roots), F (raw 64-byte extended key from the text), G (raw key with zero chain code), same 214 paths, every ordered pair of the union | 611,008 keys, 373,338,108,196 ordered pairs | same pipeline, `tools/candidates.py --pass 2` | 0 match | yes: same witness protocol, 9 of 9 re-found, `exhausted=yes` | 2026-08-29 |
| Six further constructions by @BorisLoveDev (PR #21): the texts directly as BIP39 sentences, the newspaper date as an integer seed, a date-prefix mnemonic, text bytes as derivation-path indices, zero roots, and 15 hardening patterns over m/48'/0'/account/script | about 42 million new ordered pairs across the six families (1,648,656 + 26,378,496 + 2,060,820 + 576 + 732,736 + 11,150,784) | CPU pairing on the same 2-of-2 program, exact 32-byte compare | 0 match | yes: revealed pair at head, middle and tail; I replayed all six locally with identical counts | 2026-09-05 |
| Pass 3, the September model (2026-09-12): 12-word BIP39 mnemonic whose entropy is a 16-byte window of genesis data (every window of the raw 285-byte block, of the merkle root and block hash in both byte orders, of the coinbase text, headline, scriptSig, header and coinbase public key, plus the header integers zero-padded and as decimal strings: 329 entropies), 53 passphrases (empty as control, the coinbase text, the headline, The Times, Satoshi, genesis, bitcoin, the header integers, the hashes in hex and a dozen short words from the author's messages), BIP48 `m/48'/0'/a'/s'` with a in {0, 1, 2, 3, 50, 2009, 285, bits, time, nonce} and s in {0', 1', 2'}, suffix empty, /0/0 or /0/1; every ordered pair | 1,569,330 keys, 2.463e12 ordered pairs | CPU BIP39/BIP32 generation (25 s on 22 cores), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`, 4.18e9 pairs/s, 589 s), exact 32-byte compare | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-09-12 |

## Open leads, ranked

None; the solution is verified and the sweep is confirmed.

## Solution

Solved and swept by [Schum-io](https://github.com/Schum-io) on 2026-10-17. The author
acknowledged the solve on chain one hour later ("Shoutout to the player who cracked the puzzle!").

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

5. BIP39 passphrase `Satoshi Nakamoto` (capital initials, one space).
6. Seed = PBKDF2-HMAC-SHA512(mnemonic, "mnemonic" + passphrase, rounds, 64 bytes) with a
   non-standard round count per cosigner:

| Cosigner | PBKDF2 rounds | Reading | Master fingerprint | Public key at `m/48'/0'/1231006505'/2'/0/0` |
|---|---|---|---|---|
| A | 181505 | 18:15:05 UTC, the genesis time | `0852014c` | `027b497b1d82986ebe11bca71108ca43446c00edb069cc839638a0b76529130906` |
| B | 200913 | 2009/1/3, the genesis date | `040e2791` | `033614b02e8e3aeeed9e14ac67839f85d54b694eafd91ca07f1afeb06510832ec1` |

7. Witness script `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG`; its SHA-256 is the published witness
   program, so `tools/oracle.py` reports `MATCH order=AB`. `tools/verify_solution.py` replays
   steps 1 to 7 from the hex file and asserts every intermediate value.

The sweep, `1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b`
([explorer](https://mempool.space/tx/1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b)),
spends all 117 escrow outputs (946,540 sats) in one transaction and pays 935,266 sats to
`bc1qdu8mh9qjtjhy89mvhmcgf66ul6ld92rdr6qzad`; fee 11,274 sats for 11,245 vB. Its witnesses carry
the two public keys above in script order.

What it teaches: the one parameter nobody searches is the one a wallet generator exposes as an
innocuous "custom" field. Three passes here had the right entropy family, the right account and
the right path shape, and the passphrase question was asked on chain within days; the PBKDF2
count was never a question. When an author says "the tools that support BIPs 32, 39 and 48"
and names iancoleman/bip39, enumerate every setting that page lets a user change, not only
the ones the BIPs name. The author's answers also show that paid Y/N hints can be wrong or
drift over time (fact 5), so no single shape answer should prune a search on its own.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | every OP_RETURN of the dialogue, verbatim, with txid, block and time |
| `data/genesis-block.hex` | the raw genesis block, 285 bytes, as served by any node or explorer |
| `data/on-chain-dialogue.json` | the 119 escrow transactions: sender attribution, amounts, decoded OP_RETURN, fetched 2026-10-17 |
| `analysis/tested.md` | the negatives ledger: passes 1 to 3 in full, all at 2,048 PBKDF2 rounds |
| `analysis/leads.md` | historical notes behind the leads that were open before the solve |
| `tools/oracle.py` | candidate checker: two keys to 2-of-2 P2WSH, both orders, exact match; `--selftest` |
| `tools/verify_solution.py` | rebuilds both cosigner keys from the raw block and runs them through the oracle |
| `tools/candidates.py` | key generator for passes 1 and 2 (families A to G, labeled), witness insertion, targets file, CPU re-derivation of GPU hits |

## Sources

- Announcement transaction, block 963,629, 2026-08-22: https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77
- Escrow address and full dialogue: https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj
- Sweep transaction, block 971,803, 2026-10-17: https://mempool.space/tx/1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b
- Galaxy Research, first public report, X, 2026-08-23: https://x.com/glxyresearch/status/2091349771952742566
- crypto.news, "Bitcoin puzzle hides wallet key in Genesis Block data", 2026-08-23: https://crypto.news/bitcoin-puzzle-hides-wallet-key-in-genesis-block-data/
- U.Today, 2026-08-23: https://u.today/satoshis-code-reopened-someone-just-deciphered-bitcoin-puzzle-into-genesis-block-data
- Blockmedia (Korean), 2026-08-23: https://www.blockmedia.co.kr/archives/1131026
- Genesis block, Bitcoin Wiki: https://en.bitcoin.it/wiki/Genesis_block

Credits: Schum-io, the solve and the sweep of 2026-10-17. @BorisLoveDev (PR #21): the six
2026-09-05 bounded constructions and their scripts.
