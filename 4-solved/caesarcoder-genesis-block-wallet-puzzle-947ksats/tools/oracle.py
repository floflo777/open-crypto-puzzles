#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Genesis Block Wallet Puzzle.

Purpose:
    The escrow is a native P2WSH output, so its address encodes sha256(witness script).
    The author states the witness script is a 2-of-2 multisig. A candidate pair of keys is
    therefore checked offline and exactly: rebuild OP_2 <A> <B> OP_2 OP_CHECKMULTISIG in
    both key orders, sha256 each script, compare all 32 bytes with the published witness
    program. This is a verifier, not a search tool: it checks the pair you give it.

Usage:
    python3 tools/oracle.py --selftest                 # must print SELFTEST OK
    python3 tools/oracle.py <keyA hex> <keyB hex>      # 32-byte private keys or 33/65-byte public keys
    python3 tools/oracle.py --stdin                    # one "keyA keyB" pair per line

Input:
    Two hex strings. A 64-hex-digit value is a private key (big-endian integer in [1, n-1]);
    a 66 or 130-hex-digit value is a SEC public key and is used as given.

Output:
    "MATCH order=<AB|BA>" on a hit, "NO MATCH" otherwise. Exit 0 on any match, 1 if none.

Dependencies:
    stdlib, bip_utils (for the private-to-public step only).
"""

from __future__ import annotations

import argparse
import hashlib
import sys

from bip_utils import Secp256k1PrivateKey

TARGET_ADDRESS = "bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj"
TARGET_PROGRAM = bytes.fromhex("4dae67a9872f1402109f9670276afc2c0758f895aafddcd089795771b7964833")
N_SECP = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Certification vectors (not specific to this puzzle).
# 1. BIP-173 test vector for a P2WSH program.
BIP173_PROGRAM = bytes.fromhex("1863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262")
BIP173_ADDRESS = "bc1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3qccfmv3"
# 2. A real 2-of-2 P2WSH spent in block 963629 (the announcement's block), transaction
#    47ded3504e855ce418e46eeca4694b55a623d1e23a8e3c83292abbcf9cee9f7a, input 0: the two
#    public keys in script order, and the address of the output it spends.
REVEALED_A = bytes.fromhex("02d6a21e190325448946e7ef986863113131ed6ea2dc2397e447994140d0553cf2")
REVEALED_B = bytes.fromhex("027f48ee90a45bc408c2d4aa6004d1c06827881f691ce810c713fc1b2be8d12de8")
REVEALED_ADDRESS = "bc1q6vpcc5vdrg0dh0k4edkuvamvn27mwr4crxgl94yva9v9z240vysqr89ddy"
# 3. Private key 1 is the generator point.
G_COMPRESSED = "0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798"

_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = (0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3)
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            chk ^= gen[i] if (b >> i) & 1 else 0
    return chk


def _convertbits(data, frombits, tobits):
    acc = bits = 0
    out = []
    maxv = (1 << tobits) - 1
    for value in data:
        acc = (acc << frombits) | value
        bits += frombits
        while bits >= tobits:
            bits -= tobits
            out.append((acc >> bits) & maxv)
    if bits:
        out.append((acc << (tobits - bits)) & maxv)
    return out


def bech32_v0(program: bytes, hrp: str = "bc") -> str:
    data = [0] + _convertbits(program, 8, 5)
    hrp_exp = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
    pm = _polymod(hrp_exp + data + [0] * 6) ^ 1
    chk = [(pm >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(_CHARSET[d] for d in data + chk)


def pubkey_from_priv(d: int | bytes, compressed: bool = True) -> bytes | None:
    if isinstance(d, (bytes, bytearray)):
        d = int.from_bytes(bytes(d), "big")
    if not 1 <= d < N_SECP:
        return None
    pub = Secp256k1PrivateKey.FromBytes(d.to_bytes(32, "big")).PublicKey()
    return pub.RawCompressed().ToBytes() if compressed else pub.RawUncompressed().ToBytes()


def witness_script(a: bytes, b: bytes) -> bytes:
    return b"\x52" + bytes([len(a)]) + a + bytes([len(b)]) + b + b"\x52\xae"


def program(script: bytes) -> bytes:
    return hashlib.sha256(script).digest()


def check(a: bytes, b: bytes, target: bytes = TARGET_PROGRAM) -> str | None:
    """Return 'AB' or 'BA' when one key order reproduces the target program exactly."""
    if program(witness_script(a, b)) == target:
        return "AB"
    if program(witness_script(b, a)) == target:
        return "BA"
    return None


def parse_key(h: str) -> bytes:
    raw = bytes.fromhex(h.strip())
    if len(raw) == 32:
        pub = pubkey_from_priv(raw)
        if pub is None:
            raise ValueError("private key out of range")
        return pub
    if len(raw) in (33, 65):
        return raw
    raise ValueError(f"unexpected key length {len(raw)} bytes")


def selftest() -> bool:
    ok = True

    got = bech32_v0(BIP173_PROGRAM)
    r = got == BIP173_ADDRESS
    print(f"BIP-173 P2WSH vector -> {BIP173_ADDRESS}: {'OK' if r else 'FAIL'}")
    ok = ok and r

    script = witness_script(REVEALED_A, REVEALED_B)
    r = len(script) == 71 and bech32_v0(program(script)) == REVEALED_ADDRESS
    print(f"real 2-of-2 from block 963629 rebuilds to {REVEALED_ADDRESS}: {'OK' if r else 'FAIL'}")
    ok = ok and r

    r = check(REVEALED_A, REVEALED_B, program(script)) == "AB" and check(REVEALED_B, REVEALED_A, program(script)) == "BA"
    print(f"both key orders are checked: {'OK' if r else 'FAIL'}")
    ok = ok and r

    r = pubkey_from_priv(1).hex() == G_COMPRESSED and pubkey_from_priv(0) is None and pubkey_from_priv(N_SECP) is None
    print(f"private key 1 -> G, 0 and n rejected: {'OK' if r else 'FAIL'}")
    ok = ok and r

    r = bech32_v0(TARGET_PROGRAM) == TARGET_ADDRESS
    print(f"target program -> escrow address: {'OK' if r else 'FAIL'}")
    ok = ok and r

    r = check(REVEALED_A, REVEALED_B) is None
    print(f"negative control (revealed pair vs escrow) -> no match: {'OK' if r else 'FAIL'}")
    ok = ok and r

    if ok:
        print("SELFTEST OK")
    return ok


def _report(a: bytes, b: bytes) -> bool:
    order = check(a, b)
    print(f"MATCH order={order}" if order else "NO MATCH")
    return order is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("keys", nargs="*", help="two hex keys: 32-byte private or 33/65-byte public")
    parser.add_argument("--stdin", action="store_true", help="read 'keyA keyB' pairs, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vectors")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        hit = False
        for line in sys.stdin:
            parts = line.split()
            if len(parts) != 2:
                continue
            try:
                hit = _report(parse_key(parts[0]), parse_key(parts[1])) or hit
            except ValueError as exc:
                print(f"skip: {exc}")
        return 0 if hit else 1

    if len(args.keys) != 2:
        parser.print_help()
        return 0
    return 0 if _report(parse_key(args.keys[0]), parse_key(args.keys[1])) else 1


if __name__ == "__main__":
    sys.exit(main())
