# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. Add one row per hypothesis family tested, in the order tested. Never remove
a row; if a hypothesis is retested with a different method, add a new row rather than editing
the old one.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Pass 1, families A to D: the literal readings of the two 2026-08-28 hints (raw keys from windows of the coinbase text, BIP32 seeds and BIP39 entropy from the same text along 214 paths including every BIP48 path with a genesis integer as account, the other genesis fields), every ordered pair of the union | 447,916 distinct public keys (447,922 records with 6 witness copies), 200,634,118,084 ordered pairs | keys generated on the CPU by `tools/candidates.py` (22 processes, 15 s), pairs formed and hashed on the GPU by `engines/p2wsh_2of2_pairs.cu`, exact 32-byte compare with the escrow program; every GPU hit re-derived on the CPU with `tools/oracle.py` | 0 match | yes: the 2-of-2 pair revealed in block 963,629 placed at head, middle and tail of the key file, all 9 ordered combinations re-found, engine reported `exhausted=yes` | 1.95e9 ordered pairs/s on one RTX 5080, 103 s | 2026-08-29 |
| Pass 2, families A to D plus E (hashed roots: SHA-256, double SHA-256, hash160, SHA-512 of each text as raw key, BIP32 seed and BIP39 entropy), F (raw extended key: 32 key bytes plus 32 chain-code bytes taken from the text, swapped and reversed forms), G (raw key with a zero chain code for the 16 to 32-byte windows of the text, the texts modulo n, the genesis integers and the fields), all along the same 214 paths, every ordered pair of the union | 611,008 distinct public keys (611,014 records with 6 witness copies), 373,338,108,196 ordered pairs | same pipeline as pass 1 with `tools/candidates.py --pass 2` (22 processes, 17 s) | 0 match | yes: same witness pair at head, middle and tail, all 9 ordered combinations re-found, `exhausted=yes` | 4.18e9 ordered pairs/s on one RTX 5080, 89 s | 2026-08-29 |

## Pass 2 in full

373,338,108,196 ordered pairs tested, 0 match. Method: the pass 1 key set plus 165,064 keys
from three more families (16,548 E, 2,996 F, 145,306 G before deduplication), 611,008 distinct
public keys in total, every ordered pair rebuilt as the 2-of-2 witness script, hashed on the GPU
and compared byte for byte with the escrow's witness program. Witness: same protocol as pass 1,
9 of 9 ordered head/middle/tail combinations re-found and confirmed on the CPU, no other hit.
Rate: 4.18e9 ordered pairs/s on one RTX 5080, 89 s elapsed. Date: 2026-08-29.

Scope added by pass 2 (labels E:, F:, G: in `labels.tsv`):

- E, hashed roots despite "no hash": SHA-256, double SHA-256, hash160 and SHA-512 of each of
  the 7 texts, each used (1) as a raw private key (first 32 bytes big-endian and reversed; for
  SHA-512 also the second half and the whole digest modulo n), (2) as a BIP32 seed, (3) as
  BIP39 entropy of 32 and 16 bytes with an empty passphrase, then the 214 paths. 70 integers,
  77 seeds.
- F, raw extended key: master private key = X[:32] and chain code = X[32:64] for X in T, S,
  the lower and upper-case forms of T, and the byte-reversed T and S, plus the two halves
  swapped, plus T[:32] with T[37:69] and its swap, then the 214 paths. 14 roots.
- G, raw private key imported with a zero chain code: every 16/20/24/28/32-byte window of T
  read big-endian, little-endian and right-padded, T, J and S modulo n, the 12 genesis
  integers, and the fields of at most 32 bytes, then the 214 paths. 680 roots.

After pass 2 the mechanical readings of "root -> multisig -> mainnet -> genesis_data ->
script_type" with the coinbase text as the source are closed on this list of paths. Still not
covered: SLIP-39, BIP85, a passphrase other than empty or T, paths outside the 214, and a
witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with compressed keys.

## Pass 1 in full

200,634,118,084 ordered pairs tested, 0 match. Method: 447,916 distinct public keys built on
the CPU from four families, then every ordered pair (i, j) rebuilt as
`OP_2 <Ki> <Kj> OP_2 OP_CHECKMULTISIG`, hashed with SHA-256 on the GPU and compared byte for
byte with the escrow's witness program. Witness: the real 2-of-2 pair spent in block 963,629
(transaction `47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a`) inserted at
the head, the middle and the tail of the key file with its own program as a second target; all
9 ordered head/middle/tail combinations were re-found and confirmed on the CPU, and no other
hit appeared. Rate: 1.95e9 ordered pairs/s on one RTX 5080, 103 s elapsed. Date: 2026-08-29.

Exact scope of the key set (labels in `labels.tsv` produced by `tools/candidates.py --write`):

- A, raw private keys: every 1 to 32-byte window of the 69-byte coinbase text T, the 47-byte
  headline J, the 77-byte scriptSig S and the lower and upper-case forms of T and J, read as a
  big-endian integer, a little-endian integer and right-padded to 32 bytes; windows longer
  than 32 bytes reduced modulo the curve order (big and little-endian); the 12 genesis
  integers {0, 1, 2, 3, 9, 50, 2009, 3012009, 20090103, 1231006505, 2083236893, 486604799};
  the other fields (D). Compressed keys, plus uncompressed keys for T, J, S, the integers and
  the fields. 36,816 integers, 54,264 keys before deduplication.
- B, BIP32 seeds: each whole text, its 16/20/24/28/32/64-byte windows, T[32:], T[22:] and the
  fields of at least 16 bytes (1,370 seeds), each derived along 214 paths: `m/48'/0'/a'`,
  `m/48'/0'/a'/s'`, `m/48'/0'/a'/s'/0/0`, `/0/1`, `/1/0` and `m/48/0/a/s/0/0` for every
  genesis integer a and script type s in {0, 1, 2}; `m`, `m/0`, `m/0/0`, `m/0/1`, `m/1/0`,
  `m/0'`, `m/0'/0`, `m/0'/0'`, `m/0'/0'/0'`, `m/44'/0'/0'/0/0`, `m/44'/0'/0'/0/1`,
  `m/44'/0'/0'`, `m/49'/0'/0'/0/0`, `m/84'/0'/0'/0/0`, `m/84'/0'/0'/0/1`, `m/86'/0'/0'/0/0`,
  `m/45'`, `m/45'/0/0`, `m/45'/0/0/0`, `m/45'/1/0/0`, `m/48'`, `m/48'/0'`. 293,180 keys.
- C, BIP39 entropy: the 16/20/24/28/32-byte windows of the same texts and the prefixes of the
  32-byte fields, English mnemonic, seed with an empty passphrase and with T as passphrase
  (2,730 seeds), same 214 paths. 584,220 keys.
- D, other fields as raw keys: merkle root (both byte orders), block hash (both), coinbase
  public key and its x and y coordinates, header, coinbase transaction, nonce, time, bits and
  version (both byte orders). 90 keys.

The union deduplicates to 447,916 keys because J is a suffix of T, T is a suffix of S, and the
case-changed forms share every window without a letter.

What this negative does not cover: a root built by a library step not modeled here (a raw
private key with a zero chain code, a raw extended key made of 32 key bytes plus 32 chain-code
bytes, BIP85, SLIP-39), hashed roots (the author said "no hash", but a SHA-256 of the text as
seed or key costs nothing to add), paths outside the list above, a passphrase other than empty
or T, and any witness script other than `OP_2 <A> <B> OP_2 OP_CHECKMULTISIG` with 33-byte keys
(uncompressed keys were only tried for family A and D).


## Additional bounded constructions, 2026-09-05 (contributed by @BorisLoveDev, PR #21)

Recorded escrow check on 2026-09-05: 142,779 sats, 18 funded outputs, none spent; no pending transactions. No newer message at the escrow or the last author change address. All tests below passed the existing oracle self-test before generation and compared the exact 32-byte target witness program. Candidate material stayed local; no transactions were constructed or sent.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| T and J exact/lower/upper directly as BIP39 mnemonic sentences, PBKDF2 with empty passphrase, existing 214 paths | 1,284 unique compressed keys; 1,648,656 candidate ordered pairs; 1,664,100 stream pairs including witness-key cross-pairs | CPU SHA256 of standard 2-of-2 script, exact target-program comparison | 0 match, exhausted | real revealed pair at head/middle/tail of key records, all 9 combinations recovered; BIP39 PBKDF2 also checked against a valid mnemonic vector | 2.62M hashes/s calibration; 0.873 s total | 2026-09-05 |
| Newspaper date as decimal YYYYMMDD/DDMMYYYY/MMDDYYYY integer, BE/LE padded to 16/32 bytes, BIP32 seed or BIP39 entropy with empty passphrase, existing 214 paths | 5,136 unique keys; 26,378,496 candidate ordered pairs; 26,440,164 stream pairs including witness-key cross-pairs | same exact CPU checker | 0 match, exhausted | same real pair inserted head/middle/tail, all 9 combinations recovered | 2.72M hashes/s calibration; 11.548 s total | 2026-09-05 |
| T[:21] exact/lower/upper directly as BIP39 mnemonic, empty passphrase, 214 paths; paired with itself and prior direct-mnemonic keys | 642 new keys plus 1,284 old keys; 2,060,820 new ordered pairs, old-old pairs excluded | exact CPU checker; 3 additional witness pair records | 0 match, exhausted | real pair recovered at stream head/middle/tail | 2.48M hashes/s calibration; 2.366 s total | 2026-09-05 |
| T/J/T[:21] as hardened byte indices or 4-byte BE chunk indices inside m/48'/0'/text/2', optional /0/0; seed T or 32 zero bytes | 24 keys, 576 ordered pairs | exact CPU checker; final chunk padded right with zero, chunks masked to 31 bits; 3 additional witness records | 0 match, exhausted | real pair recovered at stream head/middle/tail | 2.90M hashes/s calibration; 0.027 s total | 2026-09-05 |

These negatives cover only the stated constructions and paths. They do not establish that any natural-language clue has a unique interpretation.


| Additional hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Zero-filled 16/32 bytes as BIP32 seed or BIP39 entropy, empty passphrase, prior 214 paths | 856 keys; 732736 candidate ordered pairs, 743044 stream pairs including witness-key cross-pairs | standard 2-of-2 script, exact target SHA256 compare | 0 match, exhausted | public real pair at head/middle/tail, all 9 combinations recovered; oracle self-test passed | 2.83M hashes/s calibration; 0.434 s total | 2026-09-05 |
| Six canonical T/J raw BIP32 seeds, all hardening combinations for 48/0/account/script, prior 12 genesis accounts, script 0/1/2, suffix empty or /0/0 /0/1 /1/0; pairs share a hardening pattern | 11150784 new ordered pairs in 15 patterns; all prior old-old pairs excluded; standard all-hardened group had no new pairs and was skipped | exact CPU target-program compare | 0 match, exhausted | public real pair at stream head/middle/tail, all 3 recovered; oracle self-test passed | 2.47M hashes/s calibration; 8.625 s total | 2026-09-05 |


[Scripts and per-run reports](../tools/REPRODUCE.md) preserve the six bounded
constructions. The pair counts above are per-family coverage, not a claim that
all families are mutually disjoint. No solution was obtained.

## Pass 3, the September model (2026-09-12)

After the author's answers of 2026-09-10 and 2026-09-11 (12 words, a passphrase, entropy from the genesis block, a genesis value as the BIP48 account), one bounded pass over that model.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Pass 3, the September model (2026-09-12): 12-word BIP39 mnemonic whose entropy is a 16-byte window of genesis data (every window of the raw 285-byte block, of the merkle root and block hash in both byte orders, of the coinbase text, headline, scriptSig, header and coinbase public key, plus the header integers zero-padded and as decimal strings: 329 entropies), 53 passphrases (empty as control, the coinbase text, the headline, The Times, Satoshi, genesis, bitcoin, the header integers, the hashes in hex and a dozen short words from the author's messages), BIP48 `m/48'/0'/a'/s'` with a in {0, 1, 2, 3, 50, 2009, 285, bits, time, nonce} and s in {0', 1', 2'}, suffix empty, /0/0 or /0/1; every ordered pair | 1,569,330 keys, 2.463e12 ordered pairs | CPU BIP39/BIP32 generation (25 s on 22 cores), GPU pairing and SHA-256 (`engines/p2wsh_2of2_pairs.cu`, 4.18e9 pairs/s, 589 s), exact 32-byte compare | 0 match | yes: revealed 2-of-2 pair at head, middle and tail, 9 of 9 ordered combinations re-found, `exhausted=yes` | 2026-09-12 |

Scope: only 12-word mnemonics, only the listed entropy windows, only the 53 listed passphrases, only the listed accounts and script types, compressed keys. Under that model the passphrase is not among the obvious readings of the block. Not covered: a passphrase outside the list (the one thing the author has not described), 24 words, other accounts, non-BIP48 paths.
