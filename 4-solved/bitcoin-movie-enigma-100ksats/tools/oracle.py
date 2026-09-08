#!/usr/bin/env python3
"""
oracle.py -- candidate checker for the Bitcoin Movie Enigma puzzle.

Purpose:
    The puzzle's own rules say the wallet is restored from a 24-word BIP39 mnemonic,
    obtained by dropping 10 "intruder" words from a 34-word sequence (one word per
    movie panel, in panel order). The author does not state the derivation path, so
    this oracle checks a 24-word candidate against BIP84, BIP49 and BIP44 (2
    accounts, 3 address indices each) plus 3 raw derivation paths some simple
    wallets use. This is a verifier, not a search tool: it checks the 24-word
    candidate you give it, it does not generate the C(34,10) ways to pick it.

    The funded address was reproduced locally on 2026-09-07. Its phrase has
    an invalid BIP39 checksum. Searches that prefilter on that checksum do not
    cover the solution, even when their address derivation tests pass.

Usage:
    python3 tools/oracle.py --selftest                # must print SELFTEST OK
    python3 tools/oracle.py "w1 w2 ... w24"            # 24 space-separated BIP39 words
    python3 tools/oracle.py --stdin                    # one 24-word candidate per line

Input:
    A 24-word, space-separated candidate mnemonic on the command line or one per
    line on stdin.

Output:
    "MATCH <address> via <path>" on a hit, "NO MATCH" otherwise. The puzzle's
    actual phrase uses BIP39-listed words but has an invalid checksum, so the
    checker must derive it without the usual mnemonic-validation filter.
    Exit 0 on any match, 1 if none.

Dependencies:
    stdlib, bip_utils.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
import unicodedata

from bip_utils import (
    Bip32Slip10Secp256k1,
    Bip39MnemonicValidator,
    Bip39Languages,
    Bip44,
    Bip44Changes,
    Bip44Coins,
    Bip49,
    Bip49Coins,
    Bip84,
    Bip84Coins,
    P2WPKHAddrEncoder,
)
from bip_utils.bip.bip39.bip39_mnemonic_utils import Bip39WordsListGetter

TARGET_ADDRESS = "bc1q94ecsn0qk8lap2gefrycnms3ruepy889z969a6"
_WORDLIST = Bip39WordsListGetter().GetByLanguage(Bip39Languages.ENGLISH)
ENGLISH_WORDS = frozenset(_WORDLIST.GetWordAtIdx(i) for i in range(2048))

# Public BIP39/BIP84 test vectors (not specific to this puzzle). No solved sibling
# exists for this puzzle, so these certify the derivation path.
SELFTEST_12 = ("abandon " * 11 + "about").strip()
SELFTEST_12_ADDRESS = "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"
SELFTEST_24_GOOD = ("abandon " * 23 + "art").strip()
SELFTEST_24_BAD = ("abandon " * 23 + "about").strip()  # wrong checksum for 24 words
SELFTEST_24_ADDRESS = "bc1qzmtrqsfuaf6l6kkcsseumq26ukaphfj9skkug6"
SELFTEST_24_BAD_ADDRESS = "bc1q6qrpr2qv7xm9td5v4skfwlmwsvu40kg79zg7ya"
SOLVED_PHRASE = (
    "path mad alien apology escape spare miss goddess leopard crime visit clock "
    "start first blade guard close barrel term screen matrix toy ghost shine"
)


def addresses(mnemonic: str, passphrase: str = "") -> dict[str, str]:
    """Every plausible address for a mnemonic: BIP84/49/44, 2 accounts x 3 indices,
    plus 3 raw paths some simple wallets use. The author does not state a path."""
    # PBKDF2 is defined for arbitrary strings. Mnemonic checksums are a wallet
    # import safeguard, not a requirement of the seed-to-address mathematics.
    normalized = unicodedata.normalize("NFKD", " ".join(mnemonic.split()))
    salt = "mnemonic" + unicodedata.normalize("NFKD", passphrase)
    seed = hashlib.pbkdf2_hmac("sha512", normalized.encode(), salt.encode(), 2048, 64)
    out = {}
    for name, cls, coin in (
        ("bip84", Bip84, Bip84Coins.BITCOIN),
        ("bip49", Bip49, Bip49Coins.BITCOIN),
        ("bip44", Bip44, Bip44Coins.BITCOIN),
    ):
        try:
            ctx = cls.FromSeed(seed, coin)
            for acct in range(2):
                for i in range(3):
                    node = (
                        ctx.Purpose().Coin().Account(acct)
                        .Change(Bip44Changes.CHAIN_EXT).AddressIndex(i)
                    )
                    out[f"{name} account {acct} index {i}"] = node.PublicKey().ToAddress()
        except Exception:  # noqa: BLE001
            pass
    try:
        root = Bip32Slip10Secp256k1.FromSeed(seed)
        for path in ("m/0/0", "m/0'/0'", "m/44'/0'/0'/0/0"):
            k = root.DerivePath(path).PublicKey().RawCompressed().ToBytes()
            out[f"raw {path} (p2wpkh)"] = P2WPKHAddrEncoder.EncodeKey(k, hrp="bc")
    except Exception:  # noqa: BLE001
        pass
    return out


def check(mnemonic: str) -> tuple[bool, str | None, str | None]:
    """Return (matched, address, path) for a 24-word candidate."""
    words = mnemonic.split()
    if len(words) != 24 or any(word not in ENGLISH_WORDS for word in words):
        return False, None, None
    for path, addr in addresses(mnemonic).items():
        if addr == TARGET_ADDRESS:
            return True, addr, path
    return False, None, None


def selftest() -> bool:
    ok = True

    addr = addresses(SELFTEST_12).get("bip84 account 0 index 0")
    found = addr == SELFTEST_12_ADDRESS
    print(f"public BIP84 test vector (12 words) -> {SELFTEST_12_ADDRESS}: {'OK' if found else 'FAIL'}")
    ok = ok and found

    valid_24 = Bip39MnemonicValidator().IsValid(SELFTEST_24_GOOD)
    addr24 = addresses(SELFTEST_24_GOOD).get("bip84 account 0 index 0")
    found24 = valid_24 and addr24 == SELFTEST_24_ADDRESS
    print(f"24-word chain derives independently verified address: {'OK' if found24 else 'FAIL'}")
    ok = ok and found24

    invalid_but_derivable = (
        not Bip39MnemonicValidator().IsValid(SELFTEST_24_BAD)
        and addresses(SELFTEST_24_BAD).get("bip84 account 0 index 0") == SELFTEST_24_BAD_ADDRESS
    )
    print(f"invalid-checksum regression derives independently verified address: {'OK' if invalid_but_derivable else 'FAIL'}")
    ok = ok and invalid_but_derivable

    # Exercise check() itself so a future checksum prefilter cannot silently
    # discard this puzzle's class of solution. No funded phrase is embedded.
    global TARGET_ADDRESS
    original_target = TARGET_ADDRESS
    try:
        TARGET_ADDRESS = SELFTEST_24_BAD_ADDRESS
        accepts_invalid = check(SELFTEST_24_BAD)[0]
    finally:
        TARGET_ADDRESS = original_target
    print(f"checker accepts invalid-checksum 24-word regression: {'OK' if accepts_invalid else 'FAIL'}")
    ok = ok and accepts_invalid

    matched, _, _ = check(SELFTEST_24_GOOD)
    clean = not matched
    print(f"negative control (public vector vs escrow) -> no match: {'OK' if clean else 'FAIL'}")
    ok = ok and clean

    solved = not Bip39MnemonicValidator().IsValid(SOLVED_PHRASE) and check(SOLVED_PHRASE)[0]
    print(f"confirmed puzzle solution despite invalid checksum: {'OK' if solved else 'FAIL'}")
    ok = ok and solved

    if ok:
        print("SELFTEST OK")
    return ok


def _print_result(candidate: str) -> bool:
    matched, addr, path = check(candidate)
    if matched:
        print(f"MATCH {addr} via {path}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="24 space-separated BIP39 words")
    parser.add_argument("--stdin", action="store_true", help="read candidates, one per line")
    parser.add_argument("--selftest", action="store_true", help="run the certification vectors")
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
