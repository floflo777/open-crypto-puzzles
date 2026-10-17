#!/usr/bin/env python3
"""
candidates.py -- candidate key generator for the Genesis Block Wallet Puzzle (pass 1, families A to D).

Purpose:
    Turn the literal readings of the author's hints into an explicit, labeled set of public
    keys, so that every ordered pair can be checked against the escrow's witness program with
    the GPU engine `engines/p2wsh_2of2_pairs.cu`. Every key carries a label saying exactly how
    it was built (source bytes, window, reading, derivation path), so a hit is explainable and
    a negative has an exact scope. The known 2-of-2 pair from block 963,629 is inserted at the
    head, the middle and the tail of the key file as the witness; its own witness program is
    written as the second target.

Usage:
    python3 tools/candidates.py --count [--pass 2]            # exact sizes, no derivation
    python3 tools/candidates.py --write keys.bin labels.tsv targets.hex [--procs 22] [--pass 2]
    ../../engines/p2wsh_2of2_pairs --keys keys.bin --targets targets.hex --out hits.txt
    python3 tools/candidates.py --verify keys.bin labels.tsv hits.txt   # re-derive every hit on CPU

Pass 2 (--pass 2) adds three families on top of A to D:
    E  hashed roots: SHA-256, double SHA-256, hash160 and SHA-512 of each text, used as a raw
       private key, as a BIP32 seed and as BIP39 entropy (32 and 16 bytes, empty passphrase).
    F  raw extended key: 32 key bytes and 32 chain-code bytes taken directly from the text
       (X[:32] with X[32:64], and swapped) for T, S, their case forms and their reversed forms,
       plus T[:32] with T[37:69].
    G  raw private key with a zero chain code (the way some libraries import a bare key into an
       HD object): every 16/20/24/28/32-byte window of T (big-endian, little-endian, right
       padded), the texts modulo n, the genesis integers, the fields of at most 32 bytes.
    All three along the same 214 paths.

Families (see README, "Open leads"):
    A  raw private keys: every 1 to 32-byte window of the coinbase text T (69 bytes), the
       headline J (47), the scriptSig S (77) and their lower/upper-case forms, read big-endian,
       little-endian and right-padded; windows longer than 32 bytes reduced modulo n; the
       genesis integers; the other genesis fields. Compressed keys, plus uncompressed for the
       three canonical texts, the integers and the fields.
    B  BIP32 seeds: the whole texts, their 16/20/24/28/32/64-byte windows, the fields of at
       least 16 bytes, each derived along 214 paths (BIP48 hardened and unhardened with the
       account set to each genesis integer and script type 0'/1'/2', the root, m/0, m/0/0,
       BIP44/49/84/86, BIP45).
    C  BIP39 entropy: 16/20/24/28/32-byte windows of the same texts and prefixes of the fields,
       English mnemonic, seed with an empty passphrase and with T as passphrase, same 214 paths.
    D  the other fields (merkle root, block hash, coinbase public key and its coordinates,
       header, coinbase transaction, nonce, time, bits, version) as raw keys, seeds and entropy.

Dependencies:
    stdlib, bip_utils. Reuses oracle.py from the same directory for the script and key helpers.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import struct
import sys
import time
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle as o  # noqa: E402

from bip_utils import (  # noqa: E402
    Bip32ChainCode, Bip32KeyData, Bip32Slip10Secp256k1, Bip39Languages, Bip39MnemonicGenerator,
    Bip39SeedGenerator,
)

# The raw genesis block, 285 bytes, as served by any node or explorer (data/genesis-block.hex).
GENESIS_HEX = (
    "0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e"
    "67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c01010000000100000000000000000000"
    "00000000000000000000000000000000000000000000ffffffff4d04ffff001d0104455468652054696d65732030332f"
    "4a616e2f32303039204368616e63656c6c6f72206f6e206272696e6b206f66207365636f6e64206261696c6f75742066"
    "6f722062616e6b73ffffffff0100f2052a01000000434104678afdb0fe5548271967f1a67130b7105cd6a828e03909a6"
    "7962e0ea1f61deb649f6bc3f4cef38c4f35504e51ec112de5c384df7ba0b8d578a4c702b6bf11d5fac00000000"
)
RAW = bytes.fromhex(GENESIS_HEX)
HEADER = RAW[:80]
MERKLE_LE = HEADER[36:68]
MERKLE_BE = MERKLE_LE[::-1]
TIME, BITS, NONCE = struct.unpack("<III", HEADER[68:80])
BLOCK_HASH_BE = hashlib.sha256(hashlib.sha256(HEADER).digest()).digest()[::-1]
COINBASE = RAW[81:]
SCRIPTSIG = COINBASE[42:42 + 77]
T = SCRIPTSIG[8:]
J = T[22:]
S = SCRIPTSIG
PUBKEY = COINBASE[-70:-5]
assert T == b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
assert PUBKEY[0] == 4 and len(PUBKEY) == 65 and NONCE == 2083236893

TEXTS = {"T": T, "J": J, "S": S, "Tl": T.lower(), "Tu": T.upper(), "Jl": J.lower(), "Ju": J.upper()}
G = [0, 1, 2, 3, 9, 50, 2009, 3012009, 20090103, TIME, NONCE, BITS]
FIELDS = {
    "merkle_le": MERKLE_LE, "merkle_be": MERKLE_BE, "hash_be": BLOCK_HASH_BE, "hash_le": BLOCK_HASH_BE[::-1],
    "pubkey": PUBKEY, "pubkey_x": PUBKEY[1:33], "pubkey_y": PUBKEY[33:65], "header": HEADER, "coinbase": COINBASE,
    "nonce_le": struct.pack("<I", NONCE), "nonce_be": struct.pack(">I", NONCE),
    "time_le": struct.pack("<I", TIME), "time_be": struct.pack(">I", TIME),
    "bits_le": struct.pack("<I", BITS), "bits_be": struct.pack(">I", BITS), "version": struct.pack("<I", 1),
}
N_SECP = o.N_SECP

WITNESS_A = o.REVEALED_A
WITNESS_B = o.REVEALED_B
WITNESS_PROGRAM = o.program(o.witness_script(WITNESS_A, WITNESS_B))


def windows(x: bytes, lengths):
    for L in lengths:
        if L > len(x):
            continue
        for s in range(len(x) - L + 1):
            yield s, L, x[s:s + L]


def paths() -> list[str]:
    out = []
    for a in G:
        out.append(f"m/48'/0'/{a}'")
        for s in (0, 1, 2):
            base = f"m/48'/0'/{a}'/{s}'"
            out += [base, base + "/0/0", base + "/0/1", base + "/1/0"]
            out.append(f"m/48/0/{a}/{s}/0/0")
    out += ["m", "m/0", "m/0/0", "m/0/1", "m/1/0", "m/0'", "m/0'/0", "m/0'/0'", "m/0'/0'/0'",
            "m/44'/0'/0'/0/0", "m/44'/0'/0'/0/1", "m/44'/0'/0'", "m/49'/0'/0'/0/0",
            "m/84'/0'/0'/0/0", "m/84'/0'/0'/0/1", "m/86'/0'/0'/0/0",
            "m/45'", "m/45'/0/0", "m/45'/0/0/0", "m/45'/1/0/0", "m/48'", "m/48'/0'"]
    return out


PATHS = paths()


def family_A_ints():
    for name, x in TEXTS.items():
        for s, L, c in windows(x, range(1, len(x) + 1)):
            if L <= 32:
                yield f"A:{name}[{s}:{s+L}]:BE", int.from_bytes(c, "big")
                if L > 1:
                    yield f"A:{name}[{s}:{s+L}]:LE", int.from_bytes(c, "little")
                if L < 32:
                    yield f"A:{name}[{s}:{s+L}]:BEpadR", int.from_bytes(c + b"\0" * (32 - L), "big")
            else:
                yield f"A:{name}[{s}:{s+L}]:BEmodn", int.from_bytes(c, "big") % N_SECP
                yield f"A:{name}[{s}:{s+L}]:LEmodn", int.from_bytes(c, "little") % N_SECP
    for a in G:
        yield f"A:G:{a}", a
    for name, c in FIELDS.items():
        if len(c) <= 32:
            yield f"D:{name}:BE", int.from_bytes(c, "big")
            yield f"D:{name}:LE", int.from_bytes(c, "little")
            if len(c) < 32:
                yield f"D:{name}:BEpadR", int.from_bytes(c + b"\0" * (32 - len(c)), "big")
        else:
            yield f"D:{name}:BEmodn", int.from_bytes(c, "big") % N_SECP
            yield f"D:{name}:LEmodn", int.from_bytes(c, "little") % N_SECP
            yield f"D:{name}[:32]:BE", int.from_bytes(c[:32], "big")
            yield f"D:{name}[-32:]:BE", int.from_bytes(c[-32:], "big")


def _work_A(item):
    label, d = item
    pk = o.pubkey_from_priv(d)
    if pk is None:
        return []
    out = [(label, pk)]
    if label.startswith(("A:T[", "A:J[", "A:S[", "A:G", "D:")):
        out.append((label + ":U", o.pubkey_from_priv(d, compressed=False)))
    return out


def seeds_B():
    for name, x in TEXTS.items():
        yield f"B:{name}", x
        for s, L, c in windows(x, (16, 20, 24, 28, 32, 64)):
            if (s, L) != (0, len(x)):
                yield f"B:{name}[{s}:{s+L}]", c
    yield "B:T[32:69]", T[32:]
    yield "B:T[22:69]", T[22:]
    for name, c in FIELDS.items():
        if len(c) >= 16:
            yield f"B:D:{name}", c


def entropies_C():
    for name, x in TEXTS.items():
        for s, L, c in windows(x, (16, 20, 24, 28, 32)):
            yield f"C:{name}[{s}:{s+L}]", c
    for name, c in FIELDS.items():
        if len(c) >= 16:
            for L in (16, 20, 24, 28, 32):
                if L <= len(c):
                    yield f"C:D:{name}[:{L}]", c[:L]


def seeds_C():
    for label, ent in entropies_C():
        mn = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromEntropy(ent)
        for pname, pp in (("", ""), ("ppT", T.decode())):
            seed = Bip39SeedGenerator(mn, Bip39Languages.ENGLISH).Generate(pp)
            yield f"{label}:{pname}" if pname else label, seed


def _work_BC(item):
    label, seed = item
    out = []
    try:
        root = Bip32Slip10Secp256k1.FromSeed(seed)
    except Exception as exc:  # noqa: BLE001
        return [(f"{label}:ERROR:{type(exc).__name__}", None)]
    for p in PATHS:
        try:
            node = root if p == "m" else root.DerivePath(p)
            out.append((f"{label}:{p}", node.PublicKey().RawCompressed().ToBytes()))
        except Exception as exc:  # noqa: BLE001
            out.append((f"{label}:{p}:ERROR:{type(exc).__name__}", None))
    return out


def _hash160(b: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()


HASHES = {
    "sha256": lambda b: hashlib.sha256(b).digest(),
    "sha256d": lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest(),
    "hash160": _hash160,
    "sha512": lambda b: hashlib.sha512(b).digest(),
}


def family_E_ints():
    for name, x in TEXTS.items():
        for hn, hf in HASHES.items():
            h = hf(x)
            yield f"E:{hn}({name}):BE", int.from_bytes(h[:32], "big")
            yield f"E:{hn}({name}):LE", int.from_bytes(h[:32][::-1], "big")
            if len(h) == 64:
                yield f"E:{hn}({name})[32:]:BE", int.from_bytes(h[32:], "big")
                yield f"E:{hn}({name}):modn", int.from_bytes(h, "big") % N_SECP


def seeds_E():
    for name, x in TEXTS.items():
        for hn, hf in HASHES.items():
            h = hf(x)
            yield f"E:{hn}({name}):seed", h
            for L in (32, 16):
                if L <= len(h):
                    mn = Bip39MnemonicGenerator(Bip39Languages.ENGLISH).FromEntropy(h[:L])
                    yield f"E:{hn}({name})[:{L}]:bip39", Bip39SeedGenerator(mn, Bip39Languages.ENGLISH).Generate("")


def roots_F():
    sources = {"T": T, "S": S, "Tl": T.lower(), "Tu": T.upper(), "Trev": T[::-1], "Srev": S[::-1]}
    for name, x in sources.items():
        yield f"F:{name}[:32]|{name}[32:64]", x[:32], x[32:64]
        yield f"F:{name}[32:64]|{name}[:32]", x[32:64], x[:32]
    yield "F:T[:32]|T[37:69]", T[:32], T[37:69]
    yield "F:T[37:69]|T[:32]", T[37:69], T[:32]


def roots_G():
    zero = b"\0" * 32
    for s, L, c in windows(T, (16, 20, 24, 28, 32)):
        yield f"G:T[{s}:{s+L}]:BE|cc0", int.from_bytes(c, "big").to_bytes(32, "big"), zero
        yield f"G:T[{s}:{s+L}]:LE|cc0", int.from_bytes(c, "little").to_bytes(32, "big"), zero
        if L < 32:
            yield f"G:T[{s}:{s+L}]:BEpadR|cc0", c + b"\0" * (32 - L), zero
    for name, x in (("T", T), ("J", J), ("S", S)):
        yield f"G:{name}:modn|cc0", (int.from_bytes(x, "big") % N_SECP).to_bytes(32, "big"), zero
    for a in G:
        yield f"G:G:{a}|cc0", a.to_bytes(32, "big"), zero
    for name, c in FIELDS.items():
        if len(c) <= 32:
            yield f"G:D:{name}:BE|cc0", int.from_bytes(c, "big").to_bytes(32, "big"), zero


def _work_root(item):
    label, priv, cc = item
    d = int.from_bytes(priv, "big")
    if not 1 <= d < N_SECP:
        return []
    out = []
    try:
        root = Bip32Slip10Secp256k1.FromPrivateKey(priv, Bip32KeyData(chain_code=Bip32ChainCode(cc)))
    except Exception as exc:  # noqa: BLE001
        return [(f"{label}:ERROR:{type(exc).__name__}", None)]
    for p in PATHS:
        try:
            node = root if p == "m" else root.DerivePath(p)
            out.append((f"{label}:{p}", node.PublicKey().RawCompressed().ToBytes()))
        except Exception as exc:  # noqa: BLE001
            out.append((f"{label}:{p}:ERROR:{type(exc).__name__}", None))
    return out


def count(pass_no: int = 1) -> dict:
    nA = sum(1 for _ in family_A_ints())
    nB = sum(1 for _ in seeds_B())
    nC = sum(1 for _ in seeds_C())
    out = {"A_integers": nA, "B_seeds": nB, "C_seeds": nC, "paths": len(PATHS),
           "B_keys": nB * len(PATHS), "C_keys": nC * len(PATHS)}
    if pass_no >= 2:
        nE, nEs, nF, nG = (sum(1 for _ in family_E_ints()), sum(1 for _ in seeds_E()),
                           sum(1 for _ in roots_F()), sum(1 for _ in roots_G()))
        out.update({"E_integers": nE, "E_seeds": nEs, "F_roots": nF, "G_roots": nG,
                    "EFG_keys": nE + (nEs + nF + nG) * len(PATHS)})
    return out


def generate(procs: int, pass_no: int = 1):
    t0 = time.time()
    with Pool(procs) as pool:
        A = [kv for lst in pool.imap_unordered(_work_A, list(family_A_ints()), chunksize=256) for kv in lst]
        B = [kv for lst in pool.imap_unordered(_work_BC, list(seeds_B()), chunksize=4) for kv in lst]
        C = [kv for lst in pool.imap_unordered(_work_BC, list(seeds_C()), chunksize=4) for kv in lst]
        EFG = []
        if pass_no >= 2:
            EFG += [kv for lst in pool.imap_unordered(_work_A, list(family_E_ints()), chunksize=8) for kv in lst]
            EFG += [kv for lst in pool.imap_unordered(_work_BC, list(seeds_E()), chunksize=2) for kv in lst]
            EFG += [kv for lst in pool.imap_unordered(_work_root, list(roots_F()) + list(roots_G()), chunksize=2) for kv in lst]
    keys: dict[bytes, list[str]] = {}
    errors = 0
    for label, pk in A + B + C + EFG:
        if pk is None:
            errors += 1
            continue
        keys.setdefault(pk, []).append(label)
    return keys, errors, time.time() - t0


def write(keys: dict, kbin: Path, ltsv: Path, thex: Path) -> tuple[int, str]:
    items = list(keys.items())
    half = len(items) // 2
    order = [("WITNESS_A_head", WITNESS_A), ("WITNESS_B_head", WITNESS_B)]
    order += [(" | ".join(v), k) for k, v in items[:half]]
    order += [("WITNESS_A_middle", WITNESS_A), ("WITNESS_B_middle", WITNESS_B)]
    order += [(" | ".join(v), k) for k, v in items[half:]]
    order += [("WITNESS_A_tail", WITNESS_A), ("WITNESS_B_tail", WITNESS_B)]
    with open(kbin, "wb") as fk, open(ltsv, "w") as fl:
        for i, (label, pk) in enumerate(order):
            fk.write(bytes([len(pk)]) + pk + b"\0" * (65 - len(pk)))
            fl.write(f"{i}\t{label}\n")
    thex.write_text(o.TARGET_PROGRAM.hex() + "\n" + WITNESS_PROGRAM.hex() + "\n")
    return len(order), hashlib.sha256(kbin.read_bytes()).hexdigest()


def read_key(kbin: Path, idx: int) -> bytes:
    with open(kbin, "rb") as f:
        f.seek(idx * 66)
        rec = f.read(66)
    return rec[1:1 + rec[0]]


def verify(kbin: Path, ltsv: Path, hits: Path) -> int:
    labels = dict(line.rstrip("\n").split("\t", 1) for line in ltsv.read_text().splitlines())
    n_target = n_witness = n_bad = 0
    for line in hits.read_text().splitlines():
        parts = line.split()
        if len(parts) != 4 or parts[0] != "HIT":
            continue
        i, j, t = map(int, parts[1:])
        target = o.TARGET_PROGRAM if t == 0 else WITNESS_PROGRAM
        order = o.check(read_key(kbin, i), read_key(kbin, j), target)
        if order is None:
            n_bad += 1
            print(f"GPU hit not confirmed on CPU: i={i} j={j} t={t}")
        elif t == 0:
            n_target += 1
            print(f"MATCH on the escrow: i={i} ({labels.get(str(i))}) j={j} ({labels.get(str(j))}) order={order}")
        else:
            n_witness += 1
    print(f"escrow matches: {n_target}; witness hits: {n_witness} (9 expected); unconfirmed: {n_bad}")
    return 0 if n_bad == 0 else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--count", action="store_true")
    ap.add_argument("--write", nargs=3, metavar=("keys.bin", "labels.tsv", "targets.hex"))
    ap.add_argument("--verify", nargs=3, metavar=("keys.bin", "labels.tsv", "hits.txt"))
    ap.add_argument("--procs", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--pass", dest="pass_no", type=int, default=1, help="1 = families A to D, 2 = plus E, F, G")
    a = ap.parse_args()
    if a.count:
        for k, v in count(a.pass_no).items():
            print(f"{k:12} {v:,}")
    if a.write:
        keys, errors, secs = generate(a.procs, a.pass_no)
        n, digest = write(keys, Path(a.write[0]), Path(a.write[1]), Path(a.write[2]))
        print(f"{len(keys):,} distinct keys in {secs:.1f} s ({errors} derivation errors); "
              f"{n:,} records written incl. 6 witness copies; sha256 {digest}")
    if a.verify:
        return verify(Path(a.verify[0]), Path(a.verify[1]), Path(a.verify[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
