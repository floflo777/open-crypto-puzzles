#!/usr/bin/env python3
"""
verify_solution.py -- reproduce the Genesis Block Wallet Puzzle keys from the raw genesis block.

    python3 tools/verify_solution.py

Reads data/genesis-block.hex, rebuilds both cosigner keys, checks every intermediate
value against the published solution and runs the pair through tools/oracle.py.
Dependencies: stdlib, bip_utils (same as the oracle).
"""
import hashlib
import os
import sys

from bip_utils import Bip32Slip10Secp256k1, Bip39MnemonicGenerator

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oracle  # noqa: E402

FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASSPHRASE = "Satoshi Nakamoto"
PATH = "m/48'/0'/1231006505'/2'/0/0"
COSIGNERS = [  # (PBKDF2 rounds, master fingerprint, public key revealed by the sweep)
    (181505, "0852014c", "027b497b1d82986ebe11bca71108ca43446c00edb069cc839638a0b76529130906"),
    (200913, "040e2791", "033614b02e8e3aeeed9e14ac67839f85d54b694eafd91ca07f1afeb06510832ec1"),
]


def main() -> int:
    block_hex = open(os.path.join(FOLDER, "data", "genesis-block.hex")).read().strip().lower()
    assert len(block_hex) == 570, len(block_hex)
    cut = block_hex[262:400]  # cut -b 263-400 | tr -d '\n'
    assert bytes.fromhex(cut) == b"The Times 03/Jan/2009 Chancellor on brink of second bailout for banks"
    entropy = hashlib.sha256(cut.encode()).digest()[:16]
    assert entropy.hex() == "c020f55f60b8193bd5cac836769dbf76"
    mnemonic = Bip39MnemonicGenerator().FromEntropy(entropy).ToStr()
    assert mnemonic == "scan amateur fit scrap light over fire flip cushion reject hurt ugly"
    print("mnemonic:", mnemonic)
    pubs = []
    for rounds, fingerprint, want in COSIGNERS:
        seed = hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), ("mnemonic" + PASSPHRASE).encode(), rounds, 64)
        root = Bip32Slip10Secp256k1.FromSeed(seed)
        assert root.FingerPrint().ToHex() == fingerprint, root.FingerPrint().ToHex()
        pub = root.DerivePath(PATH).PublicKey().RawCompressed().ToBytes()
        assert pub.hex() == want, pub.hex()
        print(f"rounds {rounds}: fingerprint {fingerprint}, key {pub.hex()}")
        pubs.append(pub)
    order = oracle.check(pubs[0], pubs[1])
    assert order == "AB", order
    assert oracle.bech32_v0(oracle.program(oracle.witness_script(*pubs))) == oracle.TARGET_ADDRESS
    print("MATCH order=AB ->", oracle.TARGET_ADDRESS)
    return 0


if __name__ == "__main__":
    sys.exit(main())
