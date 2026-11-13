#!/usr/bin/env python3
"""
calibration_check.py -- re-derive the solved blocks listed in analysis/calibration.md.

Purpose:
    For each solution string, hash it (SHA-256 or MD5 as stated), use the raw
    digest as BIP39 entropy, derive BIP44 m/44'/0'/0'/0/0 and compare the P2PKH
    address with the block escrow. Where the author published the first hex
    digits of the hash in 2019, those are checked too.

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

# (block, solution string, hash algorithm, 2019 published prefix or None, escrow)
CASES = [
    ('run-1 Block 13', 'Second Second Life Second Coming I thought xXJ', 'sha256', None,
     '1GJPyUZvBE8MewEZyRx999p5JbVy8wbmWE'),
    ('run-2 Block 48', 'Think different TOMI Apple slogan', 'md5', '2c1',
     '19NR1m283F8npNdauDjQgbnEiR5cA2mdcp'),
    ('run-2 Block 56', 'Maybe you were just unlucky to have an exit node without reverse lookup.', 'md5', 'b9f',
     '14tuS6dG5BXd1usDTUJduEDafFAuET74P5'),
    ('run-2 Block 57', 'https://mobile.twitter.com/halfin/status/1153096538', 'md5', 'd26',
     '128cmgWEf3Cbor5ftazjtisNAfaiRhDgyk'),
    ('run-2 Block 58', 'That means a lot coming from you, Hal.', 'md5', 'a2a',
     '1ExTyMrA43mFJukabSCicdjdgG5ZJ2y2R9'),
    ('run-2 Block 60', 'Mayer Multiple', 'md5', 'e83',
     '1Gz9gHf4VyPorCDkpXtPg1xakQwGsJ7TP3'),
    ('run-2 Block 62', 'Tanabata', 'md5', 'bf4',
     '1FPi8gMKZLD61dU3Zeb9vrwDc6yXpg4Ff7'),
    ('run-2 Block 63', 'I am omnipotent Aoi', 'md5', None,
     '1MnL2VeHEX3wE2dvUWfJ3H3tb1AqRhxSWK'),
    ('run-2 Block 66', 'A young woman of Japanese ancestry who is very smart and sincere.', 'md5', 'dc5',
     '1Lrh5pgaaKXdWC9u5bzp9ogsNktjPWJMij'),
    ('run-2 Block 67', 'Thomas TOMI Harold Thomas Finney II', 'md5', None,
     '18o7TyCU1zkXCiC5sZSyxBFAn3Nntb4MAw'),
    ('run-2 Block 69', 'madam TOMI palindrome', 'md5', 'a8f',
     '17rkDa7xXHuK1TyzHExcj9e229ooKef8yU'),
    ('run-2 Block 70', 'Victor/Victoria', 'md5', '71a',
     '19PShGAWvbs3LCvhhBUZFt2czPzEdQ17iX'),
    ('run-2 Block 72', 'GND TOMI Green New Deal', 'md5', '916',
     '147dHipPd9eF7UTWrsxQhGDDySAmDUhXeG'),
    ('run-2 Block 73', 'carbon budget TOMI Grycoin solution', 'md5', 'f13',
     '1dG3cAWeKx67hnTVvpDCpUFwPiuqCn68X'),
    ('run-2 Block 74', 'PETM TOMI second time now', 'md5', 'c65',
     '1P1BFMU7vnpzsaUtQCAvArVKQyeMgYtmPY'),
    ('run-2 Block 75', 'reverse Turing test', 'md5', '509',
     '15pmBkzmSyXg2KhYHMmauF3EjYNEvyiABS'),
]


def address_at(entropy: bytes, index: int) -> str:
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy)
    seed = Bip39SeedGenerator(mnemonic).Generate()
    node = (Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
            .Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT))
    return node.AddressIndex(index).PublicKey().ToAddress()


def main() -> int:
    failed = 0
    for name, text, algo, prefix, escrow in CASES:
        digest = hashlib.new(algo, text.encode("utf-8")).digest()
        ok_prefix = prefix is None or digest.hex().startswith(prefix)
        ok_addr = address_at(digest, 0) == escrow
        status = "PASS" if ok_prefix and ok_addr else "FAIL"
        failed += status == "FAIL"
        note = f"prefix {prefix}" if prefix else "no published prefix"
        print(f"{status} {name}: {algo} {digest.hex()[:12]}... ({note}) "
              f"index 0 -> {escrow}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
