#!/usr/bin/env python3
"""Oracle for FTPK Season 2 ("Never-Ending").

Purpose: check whether a 12-word BIP39 mnemonic derives the escrow's Ethereum address
under the standard BIP44 path m/44'/60'/0'/0/0.

Usage:
  python3 oracle.py --selftest              # reproduces the author's own published worked example (Game 11)
  python3 oracle.py "word1 word2 ... word12" # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin                  # one 12-word candidate per line

Input: 12 space-separated English BIP39 words, in the order to derive with.
Expected output: "SELFTEST OK" (exit 0) or "SELFTEST FAILED" (exit 1) for --selftest;
"MATCH <address>" or "NO MATCH" per candidate otherwise. A checksum-invalid candidate is
still derived (PBKDF2 does not need a valid checksum); the checksum state is only reported.

Requires: mnemonic, bip_utils (both pure-Python, no network).
"""
import sys

from mnemonic import Mnemonic
from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes, Bip39MnemonicValidator

ESCROW = "0xb5fe4f1b6cb2bbe6a327f8c68f370da7df18b2dc".lower()
DERIVATION_PATH = "m/44'/60'/0'/0/0"

SELFTEST_MNEMONIC = "claim cycle staff clump domain judge boy session razor tiny shoulder coconut"
SELFTEST_ADDRESS = "0x50D7e097e61121140c19871F06eA6FeB6d14105b"

MNEMO = Mnemonic("english")
VALIDATOR = Bip39MnemonicValidator()


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def derive_eth(mnemonic, passphrase=""):
    seed = bip39_seed(mnemonic, passphrase)
    acc = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
           .Purpose().Coin().Account(0)
           .Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
    return acc.PublicKey().ToAddress()


def check(candidate):
    """Returns (ok, address_or_none, reason)."""
    words = candidate.split()
    if len(words) != 12:
        return False, None, "need exactly 12 words, got %d" % len(words)
    checksum_ok = VALIDATOR.IsValid(" ".join(words))
    addr = derive_eth(" ".join(words))
    if addr.lower() == ESCROW:
        return True, addr, "match" + ("" if checksum_ok else " (invalid BIP39 checksum)")
    return False, None, "no match" + ("" if checksum_ok else " (invalid BIP39 checksum)")


def selftest():
    got = derive_eth(SELFTEST_MNEMONIC)
    ok = got.lower() == SELFTEST_ADDRESS.lower()
    print("selftest mnemonic -> %s" % got)
    print("expected              %s" % SELFTEST_ADDRESS)
    print("SELFTEST %s: the author's own published worked example (Game 11)" % ("OK" if ok else "FAILED"))
    return ok


def main():
    if len(sys.argv) < 2:
        print('usage: oracle.py --selftest | "12 words" | --stdin', file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if sys.argv[1] == "--stdin":
        found = False
        for line in sys.stdin:
            cand = line.strip()
            if not cand:
                continue
            ok, addr, reason = check(cand)
            if ok:
                print("MATCH %s <- %r" % (addr, cand))
                found = True
        sys.exit(0 if found else 1)
    ok, addr, reason = check(sys.argv[1])
    if ok:
        print("MATCH %s" % addr)
        sys.exit(0)
    print("NO MATCH (%s)" % reason)
    sys.exit(1)


if __name__ == "__main__":
    main()
