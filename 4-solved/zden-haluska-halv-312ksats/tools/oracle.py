#!/usr/bin/env python3
"""
oracle.py -- candidate checker for Zden's Level HALV.

Purpose:
    Given a candidate 256-bit private key as 64 hex characters, derive both the
    compressed and uncompressed P2PKH addresses and compare each byte-exact to the
    escrow address.

    This oracle certifies the general secp256k1 / hash160 / base58check pipeline
    against a standard public vector. It does NOT certify the reading of the
    waveform image itself: how the 59 lobe shapes (and any other channel) turn
    into 32 key bytes is the open part of this puzzle (see the README's "What is
    understood" section). Treat every reported negative from that reading as
    uncertified for that reason, even when this oracle's own derivation is correct.

Usage:
    python3 tools/oracle.py --selftest                 # must print SELFTEST OK
    python3 tools/oracle.py "<64 hex chars>"
    python3 tools/oracle.py --stdin                     # one candidate per line

Input:
    A single candidate as 64 hex characters (a 32-byte private key) on the command
    line, or one per line on stdin.

Output:
    "MATCH <address> (<compressed|uncompressed>)" for a hit, "NO MATCH" otherwise.
    Exit 0 on any match, 1 if none.

Dependencies:
    stdlib, ecdsa, base58.
"""

from __future__ import annotations

import argparse
import hashlib
import sys

import base58
import ecdsa

TARGET_ADDRESS = "1crypto24HCr178iMcKd5iUi5D4rsg1nK"

# Public, puzzle-independent test vector: the private key 1 (the generator point
# itself), a standard example reproduced in Bitcoin educational material. Used only
# to certify the derivation pipeline in this file, not anything specific to HALV.
SELFTEST_PRIV_HEX = "0000000000000000000000000000000000000000000000000000000000000001"
assert len(SELFTEST_PRIV_HEX) == 64
SELFTEST_UNCOMPRESSED_ADDRESS = "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm"
SELFTEST_COMPRESSED_ADDRESS = "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH"


def _p2pkh(pub: bytes) -> str:
    h160 = hashlib.new("ripemd160", hashlib.sha256(pub).digest()).digest()
    return base58.b58encode_check(b"\x00" + h160).decode()


def priv_to_addresses(priv: bytes) -> tuple[str, str] | tuple[None, None]:
    """Return (compressed_addr, uncompressed_addr) for a 32-byte private key, or (None, None)."""
    if len(priv) != 32:
        return (None, None)
    n = int.from_bytes(priv, "big")
    if n == 0 or n >= ecdsa.SECP256k1.order:
        return (None, None)
    vk = ecdsa.SigningKey.from_string(priv, curve=ecdsa.SECP256k1).get_verifying_key()
    xy = vk.to_string()
    x, y = xy[:32], xy[32:]
    uncompressed = _p2pkh(b"\x04" + xy)
    compressed_prefix = b"\x03" if y[-1] & 1 else b"\x02"
    compressed = _p2pkh(compressed_prefix + x)
    return compressed, uncompressed


def check(candidate: str) -> tuple[bool, str | None, str | None]:
    candidate = candidate.strip()
    if len(candidate) != 64:
        return False, None, None
    try:
        priv = bytes.fromhex(candidate)
    except ValueError:
        return False, None, None
    compressed, uncompressed = priv_to_addresses(priv)
    if compressed is None:
        return False, None, None
    if compressed == TARGET_ADDRESS:
        return True, compressed, "compressed"
    if uncompressed == TARGET_ADDRESS:
        return True, uncompressed, "uncompressed"
    return False, None, None


def selftest() -> bool:
    ok = True

    priv = bytes.fromhex(SELFTEST_PRIV_HEX)
    compressed, uncompressed = priv_to_addresses(priv)
    found_u = uncompressed == SELFTEST_UNCOMPRESSED_ADDRESS
    print(f"private key 1 -> uncompressed {SELFTEST_UNCOMPRESSED_ADDRESS}: {'OK' if found_u else 'FAIL'}")
    ok = ok and found_u
    found_c = compressed == SELFTEST_COMPRESSED_ADDRESS
    print(f"private key 1 -> compressed {SELFTEST_COMPRESSED_ADDRESS}: {'OK' if found_c else 'FAIL'}")
    ok = ok and found_c

    matched, addr, form = check(SELFTEST_PRIV_HEX)
    clean = not matched
    print(f"negative control (public vector vs HALV's escrow) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    matched, addr, form = check(candidate)
    if matched:
        print(f"MATCH {addr} ({form})")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="64 hex characters (32-byte private key)")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vector")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            any_hit = _print_result(line) or any_hit
        return 0 if any_hit else 1

    if not args.candidate:
        parser.print_help()
        return 0

    return 0 if _print_result(args.candidate) else 1


if __name__ == "__main__":
    sys.exit(main())
