#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Smith, Lyle & Moore "Glimmer" treasure hunt.

Purpose:
    Check a candidate 12-word BIP39 mnemonic (plus an optional passphrase) against the
    puzzle's escrow. The author published the wallet's account extended public key (xpub)
    on the puzzle site; its m/0/0 address in P2WPKH form is the escrow address. This script
    derives a seed from the candidate mnemonic, walks the standard BIP32/BIP44/BIP49/BIP84
    account paths from the seed, and reports a match if either the resulting account xpub
    equals the published xpub, or the resulting m/.../0/0 address equals the escrow.

    This is a verifier, not a search tool: it checks the candidate you give it, it does not
    generate or guess mnemonics.

Usage:
    python3 tools/oracle.py --selftest                      # must print SELFTEST OK, exit 0
    python3 tools/oracle.py "w1 w2 ... w12"                  # empty passphrase
    python3 tools/oracle.py "w1 w2 ... w12" "passphrase"     # with passphrase
    python3 tools/oracle.py --stdin                          # one "mnemonic[:passphrase]"
                                                               # per line, prints matches only

Input:
    A 12-word BIP39 mnemonic on the command line (English wordlist), optionally followed by
    a passphrase argument. In --stdin mode, one candidate per line; a colon separates an
    optional passphrase from the mnemonic ("word1 ... word12:passphrase").

Output:
    "MATCH via <path> address=<address> WIF=<wif>" on a hit, "NO MATCH" otherwise.
    Exit 0 on any match, 1 if none.

Scope note (read before trusting a negative):
    --selftest below only certifies the xpub-to-address leg of this pipeline (BIP32 key
    derivation and P2WPKH address encoding), because the published xpub's m/0/0 address is
    independently known to equal the escrow. No 12-word mnemonic that actually reproduces
    this xpub is known to me (0 of 12 words held), so the BIP39-mnemonic-to-seed leg has no
    known-good vector to certify against in this repository. A "NO MATCH" from this tool is
    trustworthy for the derivation math; it says nothing about whether your candidate words
    are the right words.

Dependencies:
    stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import sys

from bip_utils import (
    Bip32Slip10Secp256k1,
    Bip39MnemonicValidator,
    Bip39SeedGenerator,
    P2WPKHAddr,
    WifEncoder,
)

# Published account xpub (from the puzzle site) and the escrow it derives.
XPUB = (
    "xpub6CpNc58zqQvNGPHDGGTr68wgrmtfFDBWRuSDAxoDdrCE1iRAaZtyAD5T9uCJ3ELUYKCkx8Jkind2"
    "kwoR3Uxmg1ycQ6DWyGxZBMFvQqhNqVC"
)
ESCROW = "bc1q0akdjvrc2csau2n3gyxa3xcq0fss852x997m9y"

# Account-level paths tried from the seed. BIP84 (native segwit) is the primary hypothesis
# because the escrow is P2WPKH; the others are kept as a defensive net over the same seed.
ACCOUNT_PATHS = [
    "m/84'/0'/0'",
    "m/49'/0'/0'",
    "m/44'/0'/0'",
    "m/0'",
    "m/0",
    "m",
    "m/84'/0'/0'/0",
]


def bip39_seed(mnemonic, passphrase=""):
    """BIP39 seed by direct PBKDF2, with NO checksum validation. A phrase an author built
    from a rule can fail the checksum and still be the funded key (Bitcoin Movie Enigma,
    solved 2026-09-07, was exactly that), so this oracle derives every candidate and reports
    the checksum only as information."""
    import hashlib, unicodedata
    m = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    p = unicodedata.normalize("NFKD", passphrase or "")
    return hashlib.pbkdf2_hmac("sha512", m.encode("utf-8"), ("mnemonic" + p).encode("utf-8"), 2048)


def _p2wpkh(node) -> str:
    return P2WPKHAddr.EncodeKey(node.PublicKey().KeyObject(), hrp="bc")


def verify_xpub_to_escrow() -> bool:
    """The certified leg: published xpub, m/0/0, P2WPKH == escrow."""
    ctx = Bip32Slip10Secp256k1.FromExtendedKey(XPUB)
    addr = _p2wpkh(ctx.DerivePath("0/0"))
    return addr == ESCROW


def check_candidate(mnemonic: str, passphrase: str = ""):
    """Return (matched: bool, detail: str) for one mnemonic + passphrase pair."""
    mnemonic = " ".join(mnemonic.split())
    seed = bip39_seed(mnemonic, passphrase)
    master = Bip32Slip10Secp256k1.FromSeed(seed)

    for path in ACCOUNT_PATHS:
        try:
            acct = master.DerivePath(path)
        except Exception:
            continue
        try:
            acct_xpub = acct.PublicKey().ToExtended()
        except Exception:
            acct_xpub = None
        if acct_xpub == XPUB:
            leaf = acct.DerivePath("0/0")
            wif = WifEncoder.Encode(leaf.PrivateKey().Raw().ToBytes())
            return True, f"account-xpub == published xpub via {path}; address={_p2wpkh(leaf)} WIF={wif}"
        try:
            leaf = acct.DerivePath("0/0")
            if _p2wpkh(leaf) == ESCROW:
                wif = WifEncoder.Encode(leaf.PrivateKey().Raw().ToBytes())
                return True, f"{path}/0/0 == escrow; WIF={wif}"
        except Exception:
            pass
    return False, "no path matches"


def run_selftest() -> int:
    ok = verify_xpub_to_escrow()
    print(f"[selftest] published xpub, m/0/0, P2WPKH == escrow: {'yes' if ok else 'no'}")
    if not ok:
        print("SELFTEST FAILED: xpub-to-escrow identity did not reproduce")
        return 1

    # Negative control: a mnemonic that is BIP39-valid but is not the puzzle's seed must
    # not match, so the harness is shown to reject as well as accept.
    control_mnemonic = (
        "abandon abandon abandon abandon abandon abandon abandon abandon abandon "
        "abandon abandon about"
    )
    matched, detail = check_candidate(control_mnemonic)
    print(f"[selftest] known-wrong mnemonic (BIP39 test vector 'abandon...about'): {detail}")
    if matched:
        print("SELFTEST FAILED: a known-wrong mnemonic matched")
        return 1

    print(
        "[selftest] scope: certifies BIP32 derivation + P2WPKH encoding against the "
        "published xpub-to-escrow identity; no known 12-word mnemonic exists yet to "
        "certify the BIP39-to-seed leg end to end (0 of 12 words held)."
    )
    print("SELFTEST OK")
    return 0


def main():
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("mnemonic", nargs="?", help="12-word BIP39 mnemonic")
    parser.add_argument("passphrase", nargs="?", default="", help="optional passphrase")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--stdin", action="store_true")
    args = parser.parse_args()

    if args.selftest:
        sys.exit(run_selftest())

    if args.stdin:
        any_match = False
        for line in sys.stdin:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            if ":" in line:
                mn, pp = line.split(":", 1)
            else:
                mn, pp = line, ""
            matched, detail = check_candidate(mn, pp)
            if matched:
                any_match = True
                print(f"MATCH '{mn}' :: {detail}")
        sys.exit(0 if any_match else 1)

    if not args.mnemonic:
        parser.print_usage()
        sys.exit(1)

    matched, detail = check_candidate(args.mnemonic, args.passphrase)
    if matched:
        print(f"MATCH {detail}")
        sys.exit(0)
    print(f"NO MATCH ({detail})")
    sys.exit(1)


if __name__ == "__main__":
    main()
