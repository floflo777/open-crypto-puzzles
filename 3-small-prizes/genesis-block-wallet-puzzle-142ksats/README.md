# Genesis Block Wallet Puzzle (142,779 sats, [OPEN])

On 2026-08-22 an anonymous author published a 252-byte OP_RETURN message in block 963,629:
a Bitcoin wallet generated only from data in Satoshi's genesis block, "extremely low"
entropy, nothing backed up. The prize sits in the first output of that same transaction, a
P2WSH address, and it grows every time someone pays for a hint: the author answers questions
on chain and relays every payment into the escrow. Eight author messages so far fix the
shape of the lock (a 2-of-2 multisig, both keys from one genesis field, no hash, a field you
can read in The Times, a derivation rule that names the BIP48 levels). The oracle is exact
and offline. Two passes on 2026-08-29 exhausted the mechanical readings of those hints
(611,008 keys, 5.7e11 ordered pairs, 0 match, witnesses re-found); what is left is the exact
meaning of "root" and "genesis_data" in the author's rule, which one paid question would settle.

## At a glance

| | |
|---|---|
| Author | anonymous, on-chain only (every message is an OP_RETURN sent to the escrow) |
| Published | 2026-08-22, OP_RETURN in block 963,629 ([transaction](https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77)) |
| Prize | 142,779 sats (about $90 at BTC = $63,000, 2026-08-16); 125,779 sats on 2026-08-24, growing with each paid question |
| Chain | bitcoin |
| Escrow | `bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj` ([explorer](https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj)) |
| Last on-chain check | 2026-08-29: funded and unspent, 18 outputs, 0 spent, confirmed on mempool.space and blockstream.info |
| Status | OPEN |
| Puzzle type | multisig, raw-private-key |
| Target format | P2WSH (v0), witness script `OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG`, both keys derived from one genesis-block field |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the BIP-173 P2WSH vector and a real 2-of-2 spent in block 963,629) |
| What remains | insight: the meaning of "root" and "genesis_data" in the author's rule (one paid question); the mechanical readings are exhausted |
| Series | none |

## The puzzle as published

The author has no website, no forum thread and no handle. Everything is in OP_RETURN outputs
of transactions paid to the escrow, readable by anyone. Verbatim texts with txids are in
[clues/author-posts.md](clues/author-posts.md); the full ledger of the 18 transactions is in
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

Answers given so far, in order (the questions are in the clues file):

| Date (UTC) | Author's answer |
|---|---|
| 2026-08-23 15:43 | "The witness script is a multisig." |
| 2026-08-23 21:08 | "Two keys, both required. The rest is for you to derive." |
| 2026-08-24 07:13 | "Yes, both keys use the same Genesis field, and there is no hash." |
| 2026-08-24 14:32 | "Both keys are derived independently from Genesis." |
| 2026-08-24 21:35 | "The Genesis Block is public. Which part of it matters is for you to discover." |
| 2026-08-28 23:15 | "Solve it to find out. Maybe both. If you can't check the Genesis block, you can also use The Times newspaper!" (asked: "Prize Address? Genesis field 32 bytes or smaller?") |
| 2026-08-28 23:50 | `Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type` (asked: "Can you give any hint about derivation offset/rule?") |

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

The escrow is a native P2WSH output: the address encodes `sha256(witness script)`. The author
states the witness script is a multisig with two keys, both required, so the script is
`OP_2 <keyA> <keyB> OP_2 OP_CHECKMULTISIG` (71 bytes with compressed keys). The unknown is
the pair of keys and their order in the script (two cases, both checked by the oracle).

Reading of the hints, in the order they constrain the search:

1. "You can also use The Times newspaper" points at the one genesis field a newspaper
   contains: the coinbase text. Its first 32 bytes are exactly
   `The Times 03/Jan/2009 Chancellor`, the size of a private key, which fits "Maybe both"
   as an answer to "32 bytes or smaller": likely one key on 32 bytes, the other on fewer.
2. "root -> multisig -> mainnet -> genesis_data -> script_type" is, word for word, the level
   order of BIP48: `m / 48' / 0' / account' / script_type'`, with a genesis value in the
   account slot. The nonce (2083236893), the timestamp and the bits value all fit under
   2^31, so all three are valid hardened indexes. Script type 2' is native P2WSH.
3. "Same field", "no hash", "derived independently": two roots built from the same text
   without an explicit SHA-256 step (raw bytes, a BIP32 seed, or BIP39 entropy), then the
   same BIP48 path; or one root and two accounts.

### Derivation and oracle

```
python3 tools/oracle.py --selftest              # must print SELFTEST OK
python3 tools/oracle.py <keyA hex> <keyB hex>   # 32-byte private keys or 33/65-byte public keys
python3 tools/oracle.py --stdin                 # one "keyA keyB" pair per line
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

1. The escrow holds 142,779 sats in 18 unspent outputs as of 2026-08-29, checked on
   mempool.space and blockstream.info. The first funding (20,000 sats) confirmed in block
   963,517 on 2026-08-22 02:45 UTC, 17 hours before the announcement.
2. Every payment sent with a question ends up in the escrow. Four questions were paid
   directly to the author's change addresses (12,909, 32,357, 6,465 and 12,963 sats); the
   author re-posted each question to the escrow with the same amount minus fees, then
   posted the answer. So the jackpot is the sum of all hint payments plus the author's
   own 30,000 sats. Traced from the transaction inputs in `data/on-chain-dialogue.json`.
3. The author uses a fresh P2WPKH change address for every message and keeps a separate
   1,000,000 sats output untouched (`bc1qw8uecdjvuedtkg4s2kku4s2ak9r2cm59khclfr`, funded
   2026-08-22 from the same source as the escrow). Response time to a paid question was
   between 1 and 10 hours in every case so far.
4. Only two wallets have asked questions: one asked 5 questions on 2026-08-23 and
   2026-08-24 (about 77,000 sats paid in total), the other asked 3 on 2026-08-28. The
   first one had split its coins into 5 equal outputs of 66,020 sats on 2026-08-06, 16
   days before the puzzle existed. I record this as an observation only.
5. The two 2026-08-28 answers ("The Times newspaper", the derivation rule) are absent from
   every press article I found; the articles cover the announcement and the first two
   answers, and report the jackpot at 125,779 sats, its value on 2026-08-24.
6. The word "genesis_data" sits exactly where BIP48 puts the account index; the nonce is
   the only genesis integer that lands under 2^31 by chance (time and bits do so by
   construction).
7. The literal readings of hints 7 and 8 do not produce the keys: 447,916 distinct public
   keys built from the coinbase text and the other genesis fields (raw windows, BIP32 seeds
   and BIP39 entropy along 214 paths including every BIP48 path with a genesis integer as
   account), paired every way, give 0 match against the escrow, with the witness pair
   re-found at head, middle and tail. 2.0e11 ordered pairs in 103 s on one RTX 5080,
   2026-08-29 (`analysis/tested.md`). The two 2026-08-28 hints therefore describe a
   construction with at least one step I have not modeled, most likely how "root" is built.
8. The library-specific root constructions do not produce the keys either: hashed roots
   (SHA-256, double SHA-256, hash160, SHA-512 of the text as key, seed or entropy), a raw
   64-byte extended key cut from the text, and a raw key with a zero chain code, along the
   same 214 paths, add 165,064 keys; the union of 611,008 keys paired every way gives 0
   match, witnesses re-found, 3.7e11 ordered pairs in 89 s, 2026-08-29. "root" is therefore
   not any standard function of the coinbase text on these paths.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md), including the exact list of texts,
windows, readings and derivation paths. Reproduce with `tools/candidates.py --write --pass 2`
(about 17 s on 22 cores) and `engines/p2wsh_2of2_pairs` (about 90 s on one RTX 5080), then
`tools/candidates.py --verify` on the hits file.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Pass 1, families A to D: literal readings of hints 7 and 8 (raw keys, BIP32 seeds, BIP39 entropy from the coinbase text and the other fields, 214 paths), every ordered pair | 447,916 keys, 200,634,118,084 ordered pairs | CPU key generation (`tools/candidates.py`), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`), exact 32-byte compare, every hit re-derived on CPU | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-08-29 |
| Pass 2, A to D plus E (hashed roots), F (raw 64-byte extended key from the text), G (raw key with zero chain code), same 214 paths, every ordered pair of the union | 611,008 keys, 373,338,108,196 ordered pairs | same pipeline, `tools/candidates.py --pass 2` | 0 match | yes: same witness protocol, 9 of 9 re-found, `exhausted=yes` | 2026-08-29 |
| Six further constructions by @BorisLoveDev (PR #21): the texts directly as BIP39 sentences, the newspaper date as an integer seed, a date-prefix mnemonic, text bytes as derivation-path indices, zero roots, and 15 hardening patterns over m/48'/0'/account/script | about 42 million new ordered pairs across the six families (1,648,656 + 26,378,496 + 2,060,820 + 576 + 732,736 + 11,150,784) | CPU pairing on the same 2-of-2 program, exact 32-byte compare | 0 match | yes: revealed pair at head, middle and tail; I replayed all six locally with identical counts | 2026-09-05 |

## Open leads, ranked

1. **Ask the author one precise question on chain** (needs a person, about 5,000 to
   10,000 sats, answer within hours). A transaction with an output to the escrow and an
   OP_RETURN of at most 80 bytes, for example
   `Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account?`
   (78 bytes). The two 2026-08-28 hints cost 3,000 and 3,500 sats each. Passes 1 and 2
   show that no standard reading of "root" works, so this is the only lead left that can
   move the puzzle. What confirms it: any answer, since each one is checked against the
   oracle in seconds. What kills it: the author stops answering; the last answer was on
   2026-08-28.
2. **Watch the channel** (minutes). Re-read the escrow's transactions before any work:
   a new OP_RETURN from the author's change chain is a new constraint; a spend closes the
   puzzle. The author's current change address (17,200 sats, unspent) is
   `bc1qktf2wdszlsg4fes6mlzjxkcnhp63wnhct6gkgh`; it moves with every message.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | every OP_RETURN of the dialogue, verbatim, with txid, block and time |
| `data/genesis-block.hex` | the raw genesis block, 285 bytes, as served by any node or explorer |
| `data/on-chain-dialogue.json` | the 18 escrow transactions: sender attribution, amounts, decoded OP_RETURN, fetched 2026-08-29 |
| `analysis/tested.md` | the negatives ledger: passes 1 and 2 in full, with their exact scope |
| `analysis/leads.md` | full notes behind the ranked leads, with family sizes and the two killed passes |
| `tools/oracle.py` | candidate checker: two keys to 2-of-2 P2WSH, both orders, exact match; `--selftest` |
| `tools/candidates.py` | key generator for passes 1 and 2 (families A to G, labeled), witness insertion, targets file, CPU re-derivation of GPU hits |

## Sources

- Announcement transaction, block 963,629, 2026-08-22: https://mempool.space/tx/b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77
- Escrow address and full dialogue: https://mempool.space/address/bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj
- Galaxy Research, first public report, X, 2026-08-23: https://x.com/glxyresearch/status/2091349771952742566
- crypto.news, "Bitcoin puzzle hides wallet key in Genesis Block data", 2026-08-23: https://crypto.news/bitcoin-puzzle-hides-wallet-key-in-genesis-block-data/
- U.Today, 2026-08-23: https://u.today/satoshis-code-reopened-someone-just-deciphered-bitcoin-puzzle-into-genesis-block-data
- Blockmedia (Korean), 2026-08-23: https://www.blockmedia.co.kr/archives/1131026
- Genesis block, Bitcoin Wiki: https://en.bitcoin.it/wiki/Genesis_block

Credits: @BorisLoveDev (PR #21): the six 2026-09-05 bounded constructions and their scripts.
