#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the School of Bitcoin "1 Million Sats In This Image" puzzle.

Purpose:
    Given a candidate 12-word BIP39 mnemonic (with an optional passphrase), derive the
    first receiving address under the three standard script types, BIP44, BIP49 and
    BIP84, account 0, and compare each to the escrow address. This is the "Path B"
    check: assembling the seed words directly and deriving an address, which bypasses
    the puzzle's KeePass file (whose Argon2d key derivation is memory-hard and not
    meant to be brute-forced; a correct candidate must be reasoned out, not searched
    for). The known first word, "abstract", is not hardcoded: pass it as part of the
    12-word candidate.

Usage:
    python3 tools/oracle.py --selftest                         # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 ... w12"                     # empty passphrase
    python3 tools/oracle.py "w1 w2 ... w12" --passphrase "..."
    python3 tools/oracle.py --stdin                             # one 12-word candidate per line

Input:
    A 12-word, space-separated candidate mnemonic, and an optional passphrase.

Output:
    "MATCH <path> <address>" on a hit, "NO MATCH" otherwise. A mnemonic that fails
    the BIP39 checksum is still derived and compared. Exit 0 on any match, 1 if none.

Dependencies:
    stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import sys

from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Changes,
    Bip44Coins,
    Bip49,
    Bip49Coins,
    Bip84,
    Bip84Coins,
)

TARGET_ADDRESS = "bc1qcsdfkaqgy9ux668vmzflzqsyg0qtspncymt5ed"

_SCHEMES = (
    ("BIP84", Bip84, Bip84Coins.BITCOIN),
    ("BIP44", Bip44, Bip44Coins.BITCOIN),
    ("BIP49", Bip49, Bip49Coins.BITCOIN),
)

# Public BIP39/BIP84 test vector (12 words, all-zero entropy), the standard vector used
# across the BIP39/BIP44/BIP84 test suites. No solved sibling exists for this puzzle,
# so this certifies the derivation path instead.
SELFTEST_VECTOR = " ".join(["abandon"] * 11 + ["about"])
SELFTEST_EXPECTED_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def check(mnemonic: str, passphrase: str = "") -> tuple[str, str] | None:
    """Return (scheme, address) for the scheme that reproduces the target, or None."""
    words = mnemonic.split()
    if len(words) != 12:
        return None
    seed = bip39_seed(mnemonic, passphrase)
    for name, cls, coin in _SCHEMES:
        ctx = cls.FromSeed(seed, coin)
        addr = (
            ctx.Purpose().Coin().Account(0)
            .Change(Bip44Changes.CHAIN_EXT)
            .AddressIndex(0)
            .PublicKey()
            .ToAddress()
        )
        if addr == TARGET_ADDRESS:
            return (name, addr)
    return None


def selftest() -> bool:
    ok = True

    got = check(SELFTEST_VECTOR)
    print(f"public BIP39/BIP84 test vector against the puzzle target: {got}")
    not_target = got is None
    print(f"  {'OK' if not_target else 'FAIL'}  test vector does not match the puzzle target")
    ok = ok and not_target

    seed = bip39_seed(SELFTEST_VECTOR, "")
    addr = (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0)
        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    )
    match = addr == SELFTEST_EXPECTED_ADDRESS
    print(f"  {'OK' if match else 'FAIL'}  BIP84 derivation reproduces the public test vector")
    print(f"        {addr}")
    ok = ok and match

    if ok:
        print("SELFTEST OK")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate 12-word mnemonic")
    parser.add_argument("--passphrase", default="", help="BIP39 passphrase (default: empty)")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vector")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            cand = line.strip()
            if not cand:
                continue
            hit = check(cand, args.passphrase)
            if hit:
                any_hit = True
                name, addr = hit
                print(f"MATCH {name} {addr}  candidate={cand!r}")
        return 0 if any_hit else 1

    if args.candidate is None:
        parser.print_help()
        return 0

    hit = check(args.candidate, args.passphrase)
    if hit:
        name, addr = hit
        print(f"MATCH {name} {addr}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
