#!/usr/bin/env python3
"""
oracle.py -- candidate checker for Exitonly "Bitcoin Challenge 14".

A candidate is a 12-word BIP39 English mnemonic (space-separated). 7 of the 12
words are published by the author in clear: dad, butter, wink, follow, trophy,
mixed, erosion. This checker does not assume their positions; it takes any
full 12-word candidate (checksum valid or not), derives it to a Bitcoin address
under BIP84 (m/84'/0'/0'/0/0, no passphrase), and compares it to the escrow
address. BIP49 and BIP44 first addresses are also checked as a fallback, since
the video never states the derivation path.

Usage:
    python3 oracle.py --selftest              # certifies the derivation, prints SELFTEST OK
    python3 oracle.py "w1 w2 w3 ... w12"       # MATCH / NO MATCH, exit 0/1
    python3 oracle.py --stdin                  # one 12-word candidate per line, matches only
"""
import sys

from bip_utils import (
    Bip39MnemonicValidator, Bip39SeedGenerator,
    Bip84, Bip84Coins, Bip49, Bip49Coins, Bip44, Bip44Coins,
    Bip44Changes,
)

TARGET = "bc1q5rjy2cdfy4n4dkk4r6pxtwqlm8tgjcc2dj0ee9"

SELFTEST_MNEMONIC = (
    "abandon abandon abandon abandon abandon abandon "
    "abandon abandon abandon abandon abandon about"
)
SELFTEST_BIP84 = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"

PATHS = (
    (Bip84, Bip84Coins.BITCOIN, "bip84"),
    (Bip49, Bip49Coins.BITCOIN, "bip49"),
    (Bip44, Bip44Coins.BITCOIN, "bip44"),
)


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def derive_addresses(mnemonic):
    seed = bip39_seed(mnemonic)
    addrs = []
    for cls, coin, name in PATHS:
        try:
            addr = (
                cls.FromSeed(seed, coin).Purpose().Coin().Account(0)
                .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0)
                .PublicKey().ToAddress()
            )
            addrs.append((name, addr))
        except Exception:
            continue
    return addrs


def check(mnemonic):
    for name, addr in derive_addresses(mnemonic):
        if addr == TARGET:
            return name, addr
    return None


def selftest():
    addrs = dict(derive_addresses(SELFTEST_MNEMONIC))
    got = addrs.get("bip84")
    assert got == SELFTEST_BIP84, f"BIP84 mismatch: {got} != {SELFTEST_BIP84}"
    print("SELFTEST OK")


def main():
    args = sys.argv[1:]
    if not args:
        print('usage: oracle.py --selftest | "w1 w2 ... w12" | --stdin')
        sys.exit(2)

    if args[0] == "--selftest":
        selftest()
        sys.exit(0)

    if args[0] == "--stdin":
        matched = False
        for line in sys.stdin:
            mnemonic = line.strip()
            if not mnemonic:
                continue
            hit = check(mnemonic)
            if hit:
                print(f"MATCH {mnemonic} via {hit[0]} -> {hit[1]}")
                matched = True
        sys.exit(0 if matched else 1)

    hit = check(args[0])
    if hit:
        print(f"MATCH via {hit[0]} -> {hit[1]}")
        sys.exit(0)
    print("NO MATCH")
    sys.exit(1)


if __name__ == "__main__":
    main()
