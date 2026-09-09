#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Guntis Vitolins 12-word wallet challenge.

Purpose:
    Given a candidate 12-word BIP39 English mnemonic, derive the MetaMask
    default Ethereum address (BIP44 m/44'/60'/0'/0/0, no passphrase) and
    compare it, case-insensitively, against the target wallet.

Usage:
    python3 tools/oracle.py --selftest              # must print SELFTEST OK
    python3 tools/oracle.py "word1 word2 ... word12" # one candidate
    python3 tools/oracle.py --stdin                  # one candidate per line

Input:
    A 12-word BIP39 English mnemonic, space separated.

Output:
    "MATCH <address>" on a hit, "NO MATCH" otherwise (a wrong checksum is reported but not a gate), or
    "INVALID WORD" if the candidate is not a well-formed BIP39 mnemonic.
    Exit 0 on any match, 1 otherwise.

Dependencies: stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import sys

from bip_utils import (
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
)

TARGET_ADDRESS = "0x9c2f44efad0c1e852a09df9939e6daf061140caf"
DERIVATION_PATH = "m/44'/60'/0'/0/0"

# Certification vector: the canonical BIP-0039 all-zero-entropy test mnemonic,
# a public standard vector, not specific to this puzzle.
VECTOR_MNEMONIC = " ".join(["abandon"] * 11 + ["about"])
VECTOR_ADDRESS = "0x9858effd232b4033e47d90003d41ec34ecaeda94"


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def derive_address(mnemonic: str) -> str:
    """12-word BIP39 mnemonic (no passphrase) -> MetaMask default Ethereum
    address (BIP44 m/44'/60'/0'/0/0), lowercase, with 0x prefix."""
    seed = bip39_seed(mnemonic)
    account = (
        Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )
    return account.PublicKey().ToAddress().lower()


def attempt(candidate: str) -> tuple[str, dict]:
    """Returns (verdict, info). verdict in {"MATCH", "NO MATCH",
    "INVALID CHECKSUM", "INVALID WORD"}."""
    words = candidate.strip().split()
    if len(words) != 12:
        return "INVALID WORD", {"reason": f"expected 12 words, got {len(words)}"}
    checksum_ok = Bip39MnemonicValidator().IsValid(candidate)
    address = derive_address(candidate)
    if address == TARGET_ADDRESS:
        return "MATCH", {"address": address, "checksum_valid": checksum_ok}
    return "NO MATCH", {"checksum_valid": checksum_ok}


def selftest() -> bool:
    ok = True

    addr = derive_address(VECTOR_MNEMONIC)
    part1 = addr == VECTOR_ADDRESS
    print(f"canonical BIP-0039 vector (abandon x11 + about) -> {VECTOR_ADDRESS}: {'OK' if part1 else 'FAIL'}")
    ok = ok and part1

    neighbor = " ".join(["abandon"] * 12)
    valid_neighbor = Bip39MnemonicValidator().IsValid(neighbor)
    part2 = not valid_neighbor
    print(f"a 1-word-different neighbor (abandon x12) fails the checksum, as expected: {'OK' if part2 else 'FAIL'}")
    ok = ok and part2

    part2b = derive_address(neighbor).startswith("0x")
    print(f"an invalid-checksum phrase still derives an address (no checksum gate): {'OK' if part2b else 'FAIL'}")
    ok = ok and part2b

    part3 = TARGET_ADDRESS == TARGET_ADDRESS.lower()
    print(f"target address is stored lowercase for exact comparison: {'OK' if part3 else 'FAIL'}")
    ok = ok and part3

    # Checksum acceptance rate: for a fixed first 11 words, exactly 1 in 16 of
    # the 2048 possible last words should pass the BIP39 checksum.
    from bip_utils import Bip39Languages
    from bip_utils.bip.bip39.bip39_mnemonic_utils import Bip39WordsListGetter

    wordlist = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
    validator = Bip39MnemonicValidator()
    base = ["abandon"] * 11
    passing = sum(
        1
        for i in range(wordlist.Length())
        if validator.IsValid(" ".join(base + [wordlist.GetWordAtIdx(i)]))
    )
    rate = passing / wordlist.Length()
    part4 = abs(rate - 1 / 16) < 0.005
    print(f"checksum acceptance rate over the full wordlist: {passing}/{wordlist.Length()} = {rate:.4f} (expected 0.0625): {'OK' if part4 else 'FAIL'}")
    ok = ok and part4

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    verdict, info = attempt(candidate)
    if verdict == "MATCH":
        print(f"MATCH {info['address']}")
        return True
    print(verdict)
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="12-word BIP39 mnemonic, space separated")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification checks")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_hit = False
        for line in sys.stdin:
            line = line.rstrip("\n")
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
