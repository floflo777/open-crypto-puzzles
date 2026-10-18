#!/usr/bin/env python3
"""
oracle.py -- candidate checker for LogicBeach "Powerful Moss" (Base, ETH).

Purpose:
    Given a candidate 12-word BIP39 mnemonic, derive the controlling Ethereum
    address under the standard wallet derivation paths and compare it exactly to
    the winner wallet, the only address the prize contract's withdraw() function
    accepts. This is a verifier, not a search tool: it checks the candidate you
    give it, it does not generate any.

Usage:
    python3 tools/oracle.py --selftest                 # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10 w11 w12"
    python3 tools/oracle.py --stdin                     # one 12-word candidate per line

Input:
    A 12-word, space-separated candidate mnemonic on the command line or one per
    line on stdin.

Output:
    "MATCH <path> <address>" for a hit, "NO MATCH" otherwise. A mnemonic that fails
    the BIP39 checksum is still derived and compared. Exit 0 on a match, 1 otherwise.

Dependencies:
    stdlib, bip_utils.

Format precedent (both verified on-chain from the artist's 2 prior puzzles, which
both paid out): "Bifurcations" (2020) used Bitcoin BIP84; the 2021 ETH puzzle used
Ethereum BIP44 m/44'/60'/0'/0/0. The Powerful Moss winner wallet is an ETH address,
so the primary path here is m/44'/60'/0'/0/0; a small neighbor sweep (3 accounts,
3 indexes) is included to be anti-false-negative against a wallet that used a
non-default account or index.
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
)

TARGET_ADDRESS = "0x635739254bde27d28301f25ad57c3cac3c3468f3"


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def _eth_addresses(seed: bytes, n_accounts: int = 3, n_index: int = 3):
    """Yield (path label, EIP-55 address) for the MetaMask-default family of paths."""
    ctx = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
    for acc in range(n_accounts):
        acc_ctx = ctx.Purpose().Coin().Account(acc).Change(Bip44Changes.CHAIN_EXT)
        for idx in range(n_index):
            a = acc_ctx.AddressIndex(idx)
            yield f"m/44'/60'/{acc}'/0/{idx}", a.PublicKey().ToAddress()


def derive_eth_default(mnemonic: str) -> str:
    """The single canonical address: MetaMask default m/44'/60'/0'/0/0 (EIP-55)."""
    seed = bip39_seed(mnemonic)
    a = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)
         .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0))
    return a.PublicKey().ToAddress()


def check(mnemonic: str, target: str | None = None):
    """Return (path, address) if any swept path matches target exactly, else None."""
    words = mnemonic.split()
    if len(words) != 12:
        return None
    mnemonic = " ".join(words)
    target = (target or TARGET_ADDRESS).lower()
    seed = bip39_seed(mnemonic)
    for label, addr in _eth_addresses(seed):
        if addr.lower() == target:
            return label, addr
    return None


def selftest() -> bool:
    ok = True

    # Public BIP39 test vector (all-zero entropy): standard MetaMask default address.
    kat_mnemonic = ("abandon " * 11 + "about").strip()
    kat_expected = "0x9858EfFD232B4033E47d90003D41EC34EcaEda94"
    kat_addr = derive_eth_default(kat_mnemonic)
    print(f"BIP39 KAT m/44'/60'/0'/0/0 -> {kat_expected}: "
          f"{'OK' if kat_addr.lower() == kat_expected.lower() else 'FAIL'}")
    ok = ok and kat_addr.lower() == kat_expected.lower()

    hit = check(kat_mnemonic, target=kat_expected)
    positive_control = hit is not None and hit[0] == "m/44'/60'/0'/0/0"
    print(f"oracle.check() positive control -> {hit}: {'OK' if positive_control else 'FAIL'}")
    ok = ok and positive_control

    clean = check(kat_mnemonic) is None
    print(f"negative control (KAT phrase vs real winner wallet) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    bad = check("abandon " * 12)
    derived_no_match = bad is None and _eth_addresses(bip39_seed("abandon " * 12))
    print(f"invalid BIP39 checksum -> still derived, no match, no gate: {'OK' if derived_no_match else 'FAIL'}")
    ok = ok and bool(derived_no_match)

    # Independent confirmation the wordlist/seed path matches the artist's prior
    # solved puzzle ("Bifurcations", BTC BIP84), a different coin but the same
    # BIP39 mnemonic-to-seed step this oracle depends on.
    from bip_utils import Bip84, Bip84Coins
    bifurcations_mnemonic = "love sound electric bomb quantum radio silver mountain tree west solve sad"
    bifurcations_expected = "bc1qj7467e7r5pdfpypm03wyvguupdrld0ul2gcutg"
    seed = bip39_seed(bifurcations_mnemonic)
    btc_addr = (Bip84.FromSeed(seed, Bip84Coins.BITCOIN)
                .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT)
                .AddressIndex(0).PublicKey().ToAddress())
    prior_ok = btc_addr == bifurcations_expected
    print(f"prior-puzzle BIP84 vector (Bifurcations) -> {bifurcations_expected}: "
          f"{'OK' if prior_ok else 'FAIL'}")
    ok = ok and prior_ok

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    hit = check(candidate)
    if hit:
        print(f"MATCH {hit[0]} {hit[1]}")
    else:
        print("NO MATCH")
    return hit is not None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="12 space-separated BIP39 words")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.stdin:
        any_match = False
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            if _print_result(line):
                any_match = True
        return 0 if any_match else 1

    if args.candidate:
        return 0 if _print_result(args.candidate) else 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
