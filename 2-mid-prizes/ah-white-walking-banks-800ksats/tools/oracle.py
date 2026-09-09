#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the AH White "Walking Banks" seed puzzle.

Purpose:
    The author published the account-level extended public key (xpub) of the wallet
    holding the prize, not the addresses directly. Given a candidate 24-word BIP39
    mnemonic, this script derives the account-0 extended public key under BIP84,
    BIP44, BIP49 and BIP86 (empty passphrase) and compares the compressed public key
    and chain code, byte for byte, to the published xpub. The version prefix
    (xpub/ypub/zpub) is ignored: it encodes the script type the reader chose when
    exporting, not the key itself.

    A match at the account level guarantees a match on every child address, so this
    is equivalent to comparing derived addresses one by one, without needing to
    enumerate an address index.

Usage:
    python3 tools/oracle.py --selftest                  # must print SELFTEST OK
    python3 tools/oracle.py "word1 word2 ... word24"     # 24-word candidate
    python3 tools/oracle.py --stdin                       # one 24-word candidate per line

Input:
    A 24-word, space-separated BIP39 mnemonic (English wordlist), on the command
    line or one per line on stdin.

Output:
    "MATCH <path>" naming which derivation (BIP84/BIP44/BIP49/BIP86) reproduces the
    published xpub, "NO MATCH" otherwise. A mnemonic that fails the BIP39 checksum
    is still derived and compared; the checksum is not a gate.
    Exit 0 on any match, 1 if none.

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
    Bip44,
    Bip44Coins,
    Bip49,
    Bip49Coins,
    Bip84,
    Bip84Coins,
    Bip86,
    Bip86Coins,
    P2WPKHAddrEncoder,
)

# Published on walkingbanks.com, "Find the Treasure" section ("Wallet Info on Blockchain.com").
XPUB = (
    "xpub6DWcZA9sqNapeBk9oUtd6Vj1PPAMARX1c6qMeX7VpUWeLZQ93UGDi6G1aSCX5"
    "FKt92XrEB5CcUmDHJjUeTTT9cJxV88wZ2vdhNnuY3PSdsV"
)

TREASURE_ADDRESSES = {
    "bc1qxy4tf0s4n7x9w24rawf9qsxh2hyljrmvyrhwzt": 100000,
    "bc1q4qc24xk5cehc4t7vr264zldsms2kmxf86jqjau": 700000,
}

_ctx = Bip32Slip10Secp256k1.FromExtendedKey(XPUB)
_TARGET = (_ctx.PublicKey().RawCompressed().ToBytes(), _ctx.ChainCode().ToBytes())

_PURPOSES = (
    ("BIP84", Bip84, Bip84Coins.BITCOIN),
    ("BIP44", Bip44, Bip44Coins.BITCOIN),
    ("BIP49", Bip49, Bip49Coins.BITCOIN),
    ("BIP86", Bip86, Bip86Coins.BITCOIN),
)

# Public BIP39 test vector (24 words, all-zero entropy plus checksum word "art"), used to
# certify the derivation and comparison logic since no solved sibling exists for this puzzle.
SELFTEST_VECTOR = " ".join(["abandon"] * 23 + ["art"])
SELFTEST_EXPECTED_PUBKEY_HEX = (
    "039cbf6a0c2a0c3a287103018396f12602ec7f6547cb378d941f2c263a472522b5"
)
SELFTEST_EXPECTED_CHAINCODE_HEX = (
    "9220117c4fa030015437ab195732bd1dd2d0f0f07f4dcaaf51350b25bc5a3c82"
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


def check(mnemonic: str) -> str | None:
    """Return the derivation name (e.g. "BIP84") that reproduces the published xpub,
    or None."""
    words = mnemonic.split()
    if len(words) != 24:
        return None
    seed = bip39_seed(mnemonic)
    for name, cls, coin in _PURPOSES:
        acc = cls.FromSeed(seed, coin).Purpose().Coin().Account(0).Bip32Object()
        key = (acc.PublicKey().RawCompressed().ToBytes(), acc.ChainCode().ToBytes())
        if key == _TARGET:
            return name
    return None


def selftest() -> bool:
    ok = True

    print("-> the published xpub derives the two known treasure addresses (P2WPKH)")
    found = {}
    for i in range(2):
        pub = _ctx.ChildKey(0).ChildKey(i).PublicKey()
        bech = P2WPKHAddrEncoder.EncodeKey(pub.KeyObject(), hrp="bc")
        found[bech] = i
    for addr, sats in TREASURE_ADDRESSES.items():
        match = addr in found
        print(f'  {"OK" if match else "FAIL"}  {addr} ({sats:,} sats) derives at 0/{found.get(addr)}')
        ok = ok and match

    print("-> public BIP39 test vector (24 words, all-zero entropy) derives a known account key")
    seed = bip39_seed(SELFTEST_VECTOR)
    acc = Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0).Bip32Object()
    got_pub = acc.PublicKey().RawCompressed().ToBytes().hex()
    got_cc = acc.ChainCode().ToBytes().hex()
    match_pub = got_pub == SELFTEST_EXPECTED_PUBKEY_HEX
    match_cc = got_cc == SELFTEST_EXPECTED_CHAINCODE_HEX
    print(f'  {"OK" if match_pub else "FAIL"}  BIP84 account pubkey matches the recorded vector')
    print(f'  {"OK" if match_cc else "FAIL"}  BIP84 account chain code matches the recorded vector')
    ok = ok and match_pub and match_cc

    print("-> negative control: the test vector does not match the puzzle target")
    not_target = check(SELFTEST_VECTOR) is None
    print(f'  {"OK" if not_target else "FAIL"}  test vector does not derive the published xpub')
    ok = ok and not_target

    if ok:
        print("SELFTEST OK")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate 24-word BIP39 mnemonic")
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
            path = check(cand)
            if path:
                any_hit = True
                print(f"MATCH {path}  candidate={cand!r}")
        return 0 if any_hit else 1

    if args.candidate is None:
        parser.print_help()
        return 0

    path = check(args.candidate)
    if path:
        print(f"MATCH {path}")
        return 0
    print("NO MATCH")
    return 1


if __name__ == "__main__":
    sys.exit(main())
