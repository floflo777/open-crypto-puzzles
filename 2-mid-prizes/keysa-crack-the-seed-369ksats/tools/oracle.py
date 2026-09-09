#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Keysa "Crack the Seed Game!" puzzle.

Purpose:
    Given 12 candidate BIP39 words in a candidate order, derive the BIP84 first
    receiving address (m/84'/0'/0'/0/0, empty passphrase) and compare it byte-exact
    to the escrow address. This matches the escrow's own script type (v0_p2wpkh) and
    the BlueWallet default HD path used for the balance-proof screenshot the author
    published. This is a verifier, not a search tool: it checks the candidate you
    give it, it does not generate any.

Usage:
    python3 tools/oracle.py --selftest                 # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12"
    python3 tools/oracle.py --stdin                     # one 12-word candidate per line

Input:
    A 12-word, space-separated candidate mnemonic on the command line or one per
    line on stdin.

Output:
    "MATCH <address>" for a hit, "NO MATCH" otherwise. A mnemonic that fails the BIP39
    checksum is still derived and compared; the checksum is not a gate. Exit 0 on any
    match, 1 if none.

Dependencies:
    stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import sys

from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44Changes,
    Bip84,
    Bip84Coins,
)

TARGET_ADDRESS = "bc1qcv84707v4sglaj306qezkcrun4eejh77k8cyjr"

# Public BIP39/BIP84 test vector (not specific to this puzzle): "abandon" x11 + "about",
# the standard all-zero-entropy mnemonic used across the BIP39/BIP44/BIP84 test suites.
# No solved sibling exists for this puzzle, so this vector certifies the derivation path.
SELFTEST_VECTOR = ("abandon " * 11 + "about").strip()
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


def derive_address(mnemonic: str) -> str | None:
    """Return the BIP84 m/84'/0'/0'/0/0 address for a 12-word mnemonic, or None if
    the word count is not 12. A bad checksum is NOT a rejection: the seed is derived
    by direct PBKDF2 (see bip39_seed)."""
    words = mnemonic.split()
    if len(words) != 12:
        return None
    seed = bip39_seed(mnemonic)
    acc = (
        Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
    )
    return acc.AddressIndex(0).PublicKey().ToAddress()


def check(mnemonic: str) -> tuple[bool, str | None]:
    addr = derive_address(mnemonic)
    if addr is None:
        return False, None
    return addr == TARGET_ADDRESS, addr


def selftest() -> bool:
    ok = True

    addr = derive_address(SELFTEST_VECTOR)
    found = addr == SELFTEST_EXPECTED_ADDRESS
    print(f"public BIP84 test vector -> {SELFTEST_EXPECTED_ADDRESS}: {'OK' if found else 'FAIL'}")
    ok = ok and found

    bad = derive_address(SELFTEST_VECTOR.replace("about", "zoo"))
    derived = bad is not None and bad != SELFTEST_EXPECTED_ADDRESS
    print(f"bad checksum (last word swapped) -> still derived, different address, no gate: {'OK' if derived else 'FAIL'}")
    ok = ok and derived

    wrong_len = derive_address("abandon " * 10 + "about")
    rejected_len = wrong_len is None
    print(f"wrong word count (11 words) -> rejected: {'OK' if rejected_len else 'FAIL'}")
    ok = ok and rejected_len

    matched, addr = check(SELFTEST_VECTOR)
    clean = not matched
    print(f"negative control (public vector vs escrow) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    matched, addr = check(candidate)
    if matched:
        print(f"MATCH {addr}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="12 space-separated BIP39 words")
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
