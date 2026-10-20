#!/usr/bin/env python3
"""
calibration_check.py -- re-derive the solved blocks listed in analysis/calibration.md.

Purpose:
    For each published solution string, hash it (SHA-256 or MD5 as stated), use the
    raw digest as BIP39 entropy, derive BIP44 m/44'/0'/0'/0/0 and compare the P2PKH
    address with the escrow that was funded and swept on chain.

Usage (run from this puzzle folder):
    python3 tools/calibration_check.py

Output:
    One PASS/FAIL line per block. Exit code 1 if any block fails.
    No network access, no keys printed.
"""

import hashlib
import sys

from bip_utils import (Bip39MnemonicGenerator, Bip39SeedGenerator,
                       Bip44, Bip44Coins, Bip44Changes)

CASES = [
    ("run-1 Block 13", "Second Second Life Second Coming I thought xXJ", "sha256",
     "2a799f952abe95d13bdeea53ba5a9e075178b751bf16ccd75ddbed0aea9afc14",
     "1GJPyUZvBE8MewEZyRx999p5JbVy8wbmWE"),
    ("run-2 Block 48", "Think different TOMI Apple slogan", "md5",
     "2c142b58c037bc30c44da6277c2cff91",
     "19NR1m283F8npNdauDjQgbnEiR5cA2mdcp"),
    ("run-2 Block 69", "madam TOMI palindrome", "md5",
     "a8f7e33a0aaeb16f61a5b09cff038846",
     "17rkDa7xXHuK1TyzHExcj9e229ooKef8yU"),
]


def address_at(entropy: bytes, index: int) -> str:
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    node = (Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
            .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT))
    return node.AddressIndex(index).PublicKey().ToAddress()


def main() -> int:
    failed = 0
    for name, text, algo, expected_hash, escrow in CASES:
        digest = hashlib.new(algo, text.encode("utf-8")).digest()
        ok_hash = digest.hex() == expected_hash
        ok_addr = address_at(digest, 0) == escrow
        status = "PASS" if ok_hash and ok_addr else "FAIL"
        failed += status == "FAIL"
        print(f"{status} {name}: {algo} {digest.hex()[:12]}... index 0 -> {escrow}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
