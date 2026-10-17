# GPU bruteforce engines

This directory contains the CUDA engines and Python host drivers I use to
solve the public, author-funded cryptopuzzles catalogued in this repository:
treasure hunts where the puzzle's own author locked a BTC/ETH/AR reward
behind a puzzle, published the address, and publicly invited anyone to
solve it and claim it. Every kernel here does the same three things: derive
a key from a candidate (a passphrase, a mnemonic, a permutation of words),
run the exact same cryptographic pipeline the target wallet used, and
compare the result byte-for-byte to a published target address or key
fingerprint. Nothing here is aimed at a third party's wallet, a leaked key,
or an address that was not deliberately published as a challenge by its own
owner.

Six kernels cover the derivation schemes that show up repeatedly across
these puzzles. All were built and self-tested against a consumer RTX-class
GPU (RTX 5080, 16 GB, Blackwell / sm_120) as part of validating this
directory; the throughput figures below are measured on that card and are
reproducible with the included self-tests and benchmarks.

**A note on the throughput numbers below: they are not comparable to each
other.** What separates them is not kernel quality, it is key-stretching
cost. The brainwallet engine does one SHA-256 per candidate. The BIP39
mnemonic kernel does a 2048-round PBKDF2-HMAC-SHA512 (about 4096 SHA-512
compressions) before it even touches the elliptic curve. Size a search
using the throughput of the specific engine you are running, not the
biggest number in this table.

## The six engines

| # | Engine | Transform | Output | Measured throughput |
|---|---|---|---|---|
| 1 | `secp256k1_hash160_engine.cu` | passphrase -> SHA256 -> secp256k1 -> hash160 -> compare | standalone binary | 9.3 M keys/s free GPU |
| 2 | `bip39_passphrase_engine.cu` | BIP39 mnemonic -> PBKDF2-HMAC-SHA512 (2048 rounds) -> BIP32 -> secp256k1 -> hash160/keccak -> compare | `libbip39pass.so` | 220-790 k/s depending on mode (below) |
| 3 | `electrum_v1_engine.cu` | 16-byte entropy -> SHA256 stretch (100000 rounds) -> master key -> per-(change,index) child -> hash160 -> compare | standalone binary | 58.8 k candidates/s (11.75 GH/s of the underlying SHA-256 stretch, about 88% of hashcat `-m 1400 -O`'s SOTA) |
| 4 | `pzl3_arweave_engine.cu` | fixed 32-byte passphrase (8 x 4-char tokens) -> SHA-512 chained 11513x -> EvpKDF(MD5, 10000 rounds) -> Rijndael(Nk=32, Nr=38) CBC decrypt -> test JWK prefix | `libpzl3.so` | about 251 k attempts/s |
| 5 | `arweave_var_engine.cu` | variable-length passphrase (<= 111 bytes) through the identical SHA-512/EvpKDF/Rijndael chain as #4 | `libarv.so` | same pipeline as #4, same order of throughput |
| 6 | `p2wsh_2of2_pairs.cu` | N public keys -> every ordered pair (i, j) -> witness script `OP_2 <Ki> <Kj> OP_2 OP_CHECKMULTISIG` -> SHA-256 -> compare with up to 8 P2WSH witness programs | standalone binary | 1.95e9 ordered pairs/s (447,922 keys, 2.0e11 pairs in 103 s) |

### 1. Brainwallet: `secp256k1_hash160_engine.cu`

A free-form string, hashed once with SHA-256 to get a private key, then
carried through a windowed scalar multiplication on secp256k1 (single
modular inversion, addition-chain field inverse) to get both the
compressed and uncompressed public key, then RIPEMD160(SHA256(pubkey)) and
a base58check comparison against one or more target addresses. This is the
"SHA256(passphrase) -> P2PKH" scheme used by RushWallet-era brainwallet
puzzles and by anyone who rolled their own from a memorable phrase.

Also doubles as a general-purpose stream cracker: `--stream` reads
newline-delimited candidate passphrases from stdin (so it can sit behind
`hashcat --stdout`, a PRINCE generator, or a combinator) and reports the
first exact match. Running with no flags builds a small built-in corpus of
clue-derived candidates (used originally against a specific brainwallet
puzzle whose clues are baked into `build_corpus()`) and can additionally
load `wordlist.txt` / `whitepaper_phrases.txt` from the current directory
if present, or extra files via repeated `-f <path>`.

```
./secp256k1_hash160_engine --selftest                     # 2 public oracles, must PASS
./secp256k1_hash160_engine --bench 20000000                # throughput probe
./secp256k1_hash160_engine --stream --target-hash160 <40hex> < candidates.txt
```

### 2. BIP39 mnemonic / passphrase family: `bip39_passphrase_engine.cu`

One shared PBKDF2-HMAC-SHA512 + BIP32 + secp256k1/keccak core, exposed
through several kernels for the different ways a BIP39-based puzzle locks
its answer:

- **Fixed mnemonic, unknown passphrase** (the "25th word" scheme):
  `check_passphrases` / `corey_init` / `corey_run_batch`, aliased as
  `bip39pass_init` / `bip39pass_run_batch` / `bip39pass_set_path`. The
  mnemonic is fixed, the passphrase (BIP39's optional 25th word) is
  unknown, the BIP32 path is configurable (default BIP84
  `m/84'/0'/0'/0/0`). About 220 k/s on a contended GPU, 319 k/s free; this
  mode is bound by PBKDF2, not by the curve arithmetic. Host driver:
  `bip39pass_stream.py`, oracle: `bip39pass_oracle.py`.
- **Unknown 12-word mnemonic, ETH output**: `check_mnemonics_eth` /
  `check_mnemonics_eth_multi` (up to 16 simultaneous targets so synthetic
  witnesses can travel the exact same code path as the real target inside
  one run). PBKDF2-SHA512 -> BIP32 (default ETH `m/44'/60'/0'/0/0`) ->
  uncompressed pubkey -> keccak256 -> last 20 bytes. Host: `bip39pass_eth.py`.
- **Unknown 12-word mnemonic, BTC output, multi-target**:
  `check_mnemonics_btc_multi`, the BTC mirror of the ETH multi-target
  kernel (PBKDF2 with an empty passphrase -> configurable BIP32 path ->
  hash160 of the compressed pubkey).
- **Word-position brute force with a checksum-aware kernel**:
  `check_mnemonics_btc` filters an on-device BIP39 checksum per candidate;
  `check_mnemonics_btc_ck` is the same search restructured so the last
  word is *computed* from the checksum instead of enumerated, which keeps
  every thread in a warp doing useful work instead of 15 of 16 threads
  diverging away on a bad checksum. Measured about 6.5x faster than the
  filtering kernel, at roughly 790 k/s. Never filter a checksum inside a
  GPU kernel if you can instead enumerate directly into the valid
  subspace: on a 32-wide warp, if only 1 candidate in 16 survives the
  filter, the other 31 threads still pay for the full PBKDF2 anyway.
- **Order search over a locked 11-word set**: `check_perm11_eth` /
  `bip39pass_run_perm11_eth`. When 11 of 12 BIP39 words are known but their
  order is not, the space is 11! orders x 128 checksum-valid twelfth words
  = 5,108,300,800. Passing every candidate's 12 word indices from the host
  would cost about 245 GB of PCIe transfer for the full space, so the
  kernel generates each candidate's word order and checksum-valid last
  word on-device from a single 64-bit global index (Lehmer / factorial
  number system decode), and only the resulting ETH address crosses back
  to the host. Measured 792 k derivations/s. Host driver:
  `perm11_eth_host.py`, which also carries a from-scratch Python
  implementation of the permutation math (no external permutation
  enumerator needed).

```
nvcc ...                                    # see build.sh
python3 bip39pass_stream.py --selftest      # oracle: empty passphrase -> a known public "sister" address
python3 bip39pass_oracle.py                 # same oracle, no sweep machinery
python3 perm11_eth_host.py selftest         # 6 witnesses + 3 negative controls
```

### 3. Electrum v1 ("old seed"): `electrum_v1_engine.cu`

Electrum's original 2011-era wallet format: 16 bytes of entropy (decoded
from a 12-word old-Electrum mnemonic on the host) are stretched with
100,000 rounds of `h = SHA256(h || entropy_hex)`, each round being exactly
one 64-byte SHA-256 block, fully unrolled in registers. The result is the
master private key; for each `(change, index)` pair the child key is
`(master + SHA256d("idx:change:" || master_pubkey)) mod n`, and both the
compressed and uncompressed hash160 are compared to the target(s).
Validated bit-exact against `bip_utils.ElectrumV1` and an independent CPU
reference. Measured 11.75 GH/s of the underlying SHA-256 stretch, which
works out to 58.8 k full candidates/s (16-byte entropy through 3
change/index pairs) freely running -- about 88% of `hashcat -m 1400 -O`'s
own throughput on the same class of card.

```
./electrum_v1_engine --bench 2000000
echo <32-hex-char-entropy> | ./electrum_v1_engine --target-hash160 <40hex> --idx-max 2 --change-max 1
```

There is no separate host driver for this one; it is used directly from
the CLI (stdin mode reads one 16-byte entropy value per line, hex-encoded).

### 4 and 5. Arweave puzzle series: `pzl3_arweave_engine.cu` / `arweave_var_engine.cu`

Several Arweave puzzles encrypt a JWK keyfile client-side with a scheme
built from primitives found in typical browser crypto libraries: the
passphrase is hashed with SHA-512, then that hash is re-hashed 11,512 more
times (11,513 rounds total) to get a 128-character hex "key string"; that
string is run through an OpenSSL/CryptoJS-style `EvpKDF` (MD5, 10,000
iterations, with the per-block re-hash quirk some CryptoJS versions have)
to get a 144-byte key+IV; then a generalised Rijndael with a 32-word key
schedule and 38 rounds (CryptoJS's `keySize: 32` "quirk" -- most AES
libraries only go up to Nk=8/Nr=14 and cannot do this natively) decrypts
the ciphertext in CBC mode. Success is detected by checking whether the
first decrypted block starts with `{"kty` (the start of a JSON Web Key).

Two variants exist because the passphrase shape differs across puzzles in
the series, and that shape changes the SHA-512 padding on the very first
block:

- **`pzl3_arweave_engine.cu` -> `libpzl3.so`**: the passphrase is always
  exactly 32 bytes, built from 8 fixed-length 4-character tokens (one
  puzzle in the series used this shape). One slot can optionally be
  generated from a charset instead of a wordlist (`--free-slot`). Host:
  `pzl3_host.py`.
- **`arweave_var_engine.cu` -> `libarv.so`**: the passphrase is the
  concatenation of 1 to 6 slot tokens of arbitrary length, up to 111 bytes
  total (other puzzles in the series used this shape). Host:
  `arweave_var_host.py`, plus `arv_candfile.py` for streaming an arbitrary
  precomputed candidate list (any structural hypothesis you can enumerate
  on the CPU -- sliced strings, reordered tokens, mixed separators --
  rather than only a mixed-radix product of per-slot wordlists).

Both engines share the same SHA-512 device core as engine #2
(`bip39_passphrase_engine.cu`), specialised for a fixed 64-byte-in/
64-byte-out hot loop that skips repeated padding computation across the
11,513-round chain.

Neither host script launches a brute-force by default; both run their
self-test and refuse to sweep without an explicit
`--i-understand-this-bruteforces` flag. Because encrypting real puzzle
data into a redistributable self-test vector was not appropriate for a
public repository, both self-tests are fully synthetic: they build known
`(salt, ciphertext-block-0, expected-plaintext-block-0)` triples on the
CPU with the same scheme, hand only the salt and ciphertext block to the
GPU, and check the recovered plaintext byte-for-byte. `pzl3_host.py` also
includes a mixed-radix index-decode check independent of the GPU.

```
python3 pzl3_host.py --selftest
python3 arweave_var_host.py                 # no flags = selftest
python3 arv_candfile.py --page <puzzle.html> --cands cands.txt --target <address>
```

## The shared host driver pattern

Every host driver in this directory follows the same shape, because it is
the shape that makes a negative result trustworthy:

1. **Load the `.so`** with `ctypes.CDLL` and bind the handful of exported
   `extern "C"` functions (`*_init`, `*_set_*`, `*_run_*`, `*_selftest`).
2. **Run the self-test before anything else, unconditionally.** Every
   script either runs it automatically or refuses to sweep without it
   having passed. A self-test failure means "do not trust any result from
   this build," full stop.
3. **Run candidates in batches**, keeping the passphrase/mnemonic bytes on
   the host and only sending compact indices or packed strings across
   PCIe.
4. **Re-derive every GPU hit on the CPU** with an independent
   implementation (`coincurve`, `bip_utils`, `ecdsa`, or the pure-Python
   reference code inlined in the host script itself) before declaring a
   solution. A GPU hit that does not survive CPU re-derivation is reported
   as a false positive, not a solution.
5. **Multi-target kernels carry synthetic witnesses alongside the real
   target** in the same run wherever practical, so a "no hit" result is
   backed by proof the harness would have found something if it were
   there, not just an absence of output.

## Building

```
cd engines
bash build.sh
```

`build.sh` compiles to `compute_80`/`compute_90` PTX and lets the CUDA
driver JIT it to whatever GPU is actually installed. This is the portable
path: it works with a stock `nvcc` (tested with CUDA 12.0) even though it
predates newer GPU architectures by name, and does not require a
native/per-architecture build. It produces:

- `secp256k1_hash160_engine`, `electrum_v1_engine` -- standalone binaries
- `libbip39pass.so`, `libpzl3.so`, `libarv.so` -- shared libraries loaded
  by their respective Python host drivers via `ctypes`

None of the build outputs are checked in; `.gitignore` in this directory
excludes them. Run `build.sh` once after cloning.

## CPU reference libraries: `lib/`

- `lib/btc_p2pkh.py` -- private key -> P2PKH address, compressed and
  uncompressed.
- `lib/bip39_multipath.py` -- BIP39 seed -> the P2PKH address set across a
  small bank of common derivation paths (master key plus a few BIP44-style
  depths, compressed and uncompressed at each), for checking a candidate
  mnemonic against a target without committing to one derivation path
  ahead of time. Self-test: `python3 lib/bip39_multipath.py` (the standard
  `abandon abandon ... about` BIP39 test vector, checked against the
  well-known `m/44'/0'/0'/0/0` address for that seed).
- `lib/rushwallet_derive.py` -- `SHA256(passphrase) -> P2PKH`
  (RushWallet-style brainwallets), validated against 3 independent public
  oracles. Self-test: `python3 lib/rushwallet_derive.py`.
- `lib/bip39_english.txt` -- the standard 2048-word BIP-39 English wordlist
  (the fixed index table the BIP-39 spec defines, not a password-guessing
  dictionary). `bip39pass_eth.py` and `perm11_eth_host.py` load this file
  to map word indices to words and back; without it those two host
  drivers cannot run.

None of these three modules use package-relative imports, so they can be
imported either as `from lib import btc_p2pkh` or by adding `lib/` to
`sys.path` directly.

## What is not here

- No password/attack wordlists (rockyou, xato, probable, skullsecurity,
  and the like). If a sweep in this directory's tooling needs one, get it
  from its usual public source and point `--wordlists` at it; none are
  bundled here.
- No compiled artifacts (`.so`, the two standalone binaries) -- build them
  locally with `build.sh`.
- No secrets, API keys, private keys, seeds, or `.env` files.
- No puzzle-specific input data (page HTML, salts, ciphertexts). Those are
  the puzzle's own published material, not part of the engine; pass them
  in with the appropriate flag (`--page`, `--wordlists`, `--target*`) when
  you point one of these drivers at a specific puzzle.

### 6. P2WSH 2-of-2 pair enumerator: `p2wsh_2of2_pairs.cu`

For puzzles whose escrow is a native P2WSH output holding a 2-of-2 multisig, the unknown is a
pair of keys and their order in the script. This engine takes a file of N candidate public keys
(66-byte records: one length byte, then the SEC key zero-padded to 65 bytes), forms every
ordered pair, rebuilds the witness script, hashes it once with SHA-256 and compares the 32
bytes with up to 8 target programs. Ordered pairs mean both key orders are covered, so a
BIP-67 sorted script needs no special case. Key derivation is not done here: the host
generates and labels the candidates on the CPU (see
`4-solved/caesarcoder-genesis-block-wallet-puzzle-947ksats/tools/candidates.py` for a complete
example with head, middle and tail witnesses), the GPU only pairs and hashes.

```
p2wsh_2of2_pairs --bench 20000                                   # 4e8 pairs, prints the rate
p2wsh_2of2_pairs --keys keys.bin --targets targets.hex --out hits.txt
```

Output lines are `HIT i j t` (key indexes and target index) and a final `DONE ... exhausted=yes`
line. Every hit is re-derived on the CPU by the host before it counts; the witness pair placed
at the head, middle and tail of the key file must produce its 9 ordered hits, otherwise the
run is not a negative. Measured on the RTX 5080: 1.95e9 ordered pairs/s, so N = 1e6 keys
(1e12 pairs) takes about 9 minutes.
