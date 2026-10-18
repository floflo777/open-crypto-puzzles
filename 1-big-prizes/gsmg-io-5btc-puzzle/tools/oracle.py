#!/usr/bin/env python3
"""
oracle.py -- final-gate candidate checker for the GSMG.io puzzle.

Purpose:
    The puzzle's last published page names an OpenSSL AES blob and tells the solver
    to find the password. This script reproduces that specific, publicly documented
    half of the final gate: given a candidate answer string X, it computes
    password = sha256(X).hexdigest(), decrypts the blob printed on the last page
    (OpenSSL legacy "Salted__" format, AES-256-CBC, MD5 key derivation) with that
    password, reduces the resulting plaintext to a 32-byte value with a small set of
    standard readings, derives the uncompressed secp256k1 public key, and compares
    its HASH160 to the escrow address.

    This is NOT the puzzle's own sealed answer-checker (an unpublished tool some
    solvers reference informally); that tool is not public and this repository has
    no access to it, so it is not shipped here. What is shipped is the AES-blob
    pipeline itself, which is fully reproducible from the puzzle's own published
    material and the escrow's on-chain public key.

Usage:
    python3 tools/oracle.py --selftest              # see "Certified against" below
    python3 tools/oracle.py "<candidate answer>"     # try one candidate
    python3 tools/oracle.py --stdin                  # one candidate per line

Input:
    A candidate answer string X.

Output:
    "MATCH <address> reading=<name> priv_hex=<hex> wif=<wif>" on a hit,
    "NO MATCH" otherwise. Exit 0 on any match, 1 if none matched.

Dependencies: stdlib, pycryptodome, ecdsa, base58.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys

import base58
from Crypto.Cipher import AES
from ecdsa import SECP256k1, SigningKey

# The blob printed on the puzzle's last published page (128 base64 characters,
# decodes to 96 bytes: "Salted__" + 8-byte salt + 80 bytes of ciphertext).
BLOB_B64 = (
    "U2FsdGVkX186tYU0hVJBXXUnBUO7C0+X4KUWnWkCvoZSxbRD3wNsGWVHefvdrd9z"
    "QvX0t8v3jPB4okpspxebRi6sE1BMl5HI8Rku+KejUqTvdWOX6nQjSpepXwGuN/jJ"
)

TARGET_ADDRESS = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# The escrow's public key, recovered from its 2024 spending transaction on chain
# (block 840725, txid 88cdb3cd...). Used only by the selftest, to certify the
# address-derivation half of the pipeline against a real, independently checkable
# fact: this pubkey's HASH160 must equal TARGET_ADDRESS.
KNOWN_PUBKEY_HEX = (
    "04f4d1bbd91e65e2a019566a17574e97dae908b784b388891848007e4f55d5a464"
    "9c73d25fc5ed8fd7227cab0be4e576c0c6404db5aa546286563e4be12bf33559"
)


# Certification vector: the puzzle's own phase-2 blob, published on
# gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithoutaveryspecial
# dessertiwroteitmyself, whose password is the known stage answer sha256("causality").
# This is a real end-to-end vector for the key-derivation and AES half of the pipeline,
# which a self-made round trip cannot provide: a self-made blob is encrypted with the
# same derivation it is then decrypted with, so it cannot detect a wrong digest.
PHASE2_BLOB_B64 = (
    "U2FsdGVkX18GKGYS1D7X7VjxWz6uUyPFszr8dVvtOIrJqioWHgT69JJnzJGDVOvF"
    "QYWh5BEZxFPXmMq1cbyy3dVVDgLhF050xlDy2J5grtKw9jUOO4oFNRgoD+1dlukX"
    "pd8ccg++kkXgE9mGBP6lQbukDiSjY4mnR2Mv6ydIncrRqacQNVEmEgM4fGTi1ANz"
    "nHsGn7mP+P3UyrJCRbuFmpZJc4CNdPj6YuxwR4HkHkqcfxh0L5CaEu4VbY70+fmk"
    "qgZQyMJqiUlaV9KC4UPuRVj0r7MYbVRazkhsjeIcogmdJGEeBwD47lEB7X9PNKWm"
    "ojTvRZg6R+sZzRZE26VLaF+s9cpTo4Y8PZUxKvQ86HXC8QIavUgDfw7HxIxkTatv"
    "CW2yq3ZOXl5naR6oSNxdX9alyhTzB+/2623oGdlWev5Oo8xHJqUi7QjVP+mNC8BA"
    "+Cg0DJwcOFGO5K7g8Rm06+sLogwntdIgTo70X3FegAtipHboeUNKefiAguvkDoIf"
    "8iMPc+83PygvlZPDNQCOKugwDEUimhHwQrMsmalRNoFEQEb+ZIC+na15cPoRAlOD"
    "NJfXIJ96ihAy9wWis39mQW6JFqZmUags4xoP3lJ35bCrXsNOPFZ4WH+f4YC/Ov8C"
    "QW5bjtxno8GG4b/wBWevhcRVMK6KmRJj8NBCssnrlz0sQ70rMNkiN2wiSPcwX3Ad"
    "JgLs8vQAUM59x9fkKFFzD4+Sc1sJztUTB7CMGGfpZOA8W33VZnEdmGcoaHlDsR8G"
    "vAkZ+jg+QJs9ZNHqWE1+1zgm/6NsWWgWH8OI2PPCfXHxDbfDk8uD/Zibr/yjSKvu"
    "Sb8OecflOT2hw37WL49uADgeWgnp2bzkfGIq7EYS7OImjZZwY5h4sfcPfhvQ9kOV"
)
PHASE2_MARKER = b"keymakers"


def sha256(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()


def evp_bytes_to_key(password: bytes, salt: bytes, key_len: int, iv_len: int,
                     digest: str = "sha256") -> tuple[bytes, bytes]:
    """OpenSSL's EVP_BytesToKey, with the digest selectable.

    This puzzle uses BOTH digests, so neither can be assumed:

      phase 2, phase 3   SHA-256 (the `openssl enc` default since OpenSSL 1.1.0);
                         MD5 yields invalid padding and garbage on both.
      Cosmic Duality     MD5; SHA-256 fails on it.

    An earlier version of this file hardcoded MD5 and described it as the scheme used
    throughout, which is wrong for phases 2 and 3. Hardcoding SHA-256 instead would be
    equally wrong for Cosmic Duality. Since the small blob's password is unknown, its
    digest cannot be determined, so `attempt` tries both."""
    H = hashlib.sha256 if digest == "sha256" else hashlib.md5
    derived, prev = b"", b""
    while len(derived) < key_len + iv_len:
        prev = H(prev + password + salt).digest()
        derived += prev
    return derived[:key_len], derived[key_len:key_len + iv_len]


def unpad_pkcs7(data: bytes) -> bytes | None:
    if not data:
        return None
    n = data[-1]
    if n < 1 or n > 16 or n > len(data):
        return None
    if data[-n:] != bytes([n]) * n:
        return None
    return data[:-n]


def decrypt_blob(blob_b64: str, password: str, digest: str = "sha256") -> bytes | None:
    """Decrypt an OpenSSL "Salted__" AES-256-CBC blob. Returns the unpadded
    plaintext, or None if the header is malformed or padding does not validate."""
    raw = base64.b64decode(blob_b64)
    if raw[:8] != b"Salted__":
        return None
    salt, ciphertext = raw[8:16], raw[16:]
    key, iv = evp_bytes_to_key(password.encode("utf-8"), salt, 32, 16, digest)
    plain = AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext)
    return unpad_pkcs7(plain)


def readings(plain: bytes) -> list[tuple[str, bytes]]:
    """Standard ways to reduce a decrypted plaintext to a 32-byte private key
    candidate, with no judgment on how the bytes look (binary key material is
    expected, not printable text)."""
    out = [("sha256(plaintext)", sha256(plain))]
    if len(plain) >= 32:
        out.append(("first32", plain[:32]))
        out.append(("last32", plain[-32:]))
    if len(plain) >= 64:
        out.append(("sha256(first64)", sha256(plain[:64])))
    # Hex-encoded key material: strip whitespace and an optional 0x, then
    # hex-decode when the result is 32 or 64 bytes (reported by my314team /
    # 314.run in issue #46: a 64-char ASCII hex key is 80 bytes of ciphertext
    # and was scored NO MATCH because none of the readings above decode hex).
    stripped = b"".join(plain.split())
    if stripped[:2] in (b"0x", b"0X"):
        stripped = stripped[2:]
    if len(stripped) in (64, 128) and all(c in b"0123456789abcdefABCDEF" for c in stripped):
        try:
            dec = bytes.fromhex(stripped.decode("ascii"))
            if len(dec) == 32:
                out.append(("hex->32", dec))
            elif len(dec) == 64:
                out.append(("hex->first32", dec[:32]))
                out.append(("hex->last32", dec[-32:]))
        except ValueError:
            pass
    # WIF-shaped tokens: Base58Check that decodes to 0x80 + 32 (+ optional 0x01).
    token = b"".join(plain.split())
    if 50 <= len(token) <= 53:
        try:
            raw = base58.b58decode_check(token.decode("ascii"))
            if raw[:1] == b"\x80" and len(raw) in (33, 34):
                out.append(("wif", raw[1:33]))
        except Exception:
            pass
    return out


def priv_to_address(priv_bytes: bytes) -> tuple[str, str]:
    """Uncompressed secp256k1 public key -> HASH160 -> P2PKH address. Returns
    (address, uncompressed_pubkey_hex)."""
    sk = SigningKey.from_string(priv_bytes, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pub = b"\x04" + vk.to_string()
    h160 = hashlib.new("ripemd160", sha256(pub)).digest()
    address = base58.b58encode_check(b"\x00" + h160).decode()
    return address, pub.hex()


def wif_uncompressed(priv_bytes: bytes) -> str:
    return base58.b58encode_check(b"\x80" + priv_bytes).decode()


def attempt(candidate: str) -> tuple[bool, dict]:
    password = hashlib.sha256(candidate.encode("utf-8")).hexdigest()
    # The puzzle uses both digests on different blobs, and this blob's password is
    # unknown, so neither can be ruled out. Try both.
    plains = [(d, decrypt_blob(BLOB_B64, password, d)) for d in ("sha256", "md5")]
    plains = [(d, p) for d, p in plains if p is not None]
    if not plains:
        return False, {"reason": "PKCS7 padding did not validate under either digest"}
    for digest, plain in plains:
      for name, key_bytes in readings(plain):
        if len(key_bytes) != 32:
            continue
        try:
            address, pub_hex = priv_to_address(key_bytes)
        except Exception:  # noqa: BLE001  out-of-range scalar, etc.
            continue
        if address == TARGET_ADDRESS:
            return True, {
                "digest": digest,
                "reading": name,
                "address": address,
                "priv_hex": key_bytes.hex(),
                "wif": wif_uncompressed(key_bytes),
            }
    return False, {"reason": "padding valid, no reading matched the address"}


def selftest() -> bool:
    ok = True

    # Part 1: the address-derivation half of the pipeline, certified against a
    # real, independently checkable fact: the escrow's own on-chain public key
    # (recovered from its 2024 spending transaction) must hash to its address.
    pub = bytes.fromhex(KNOWN_PUBKEY_HEX)
    h160 = hashlib.new("ripemd160", sha256(pub)).digest()
    address_from_known_pubkey = base58.b58encode_check(b"\x00" + h160).decode()
    part1 = address_from_known_pubkey == TARGET_ADDRESS
    print(f"HASH160(known on-chain pubkey) -> {TARGET_ADDRESS}: {'OK' if part1 else 'FAIL'}")
    ok = ok and part1

    # Part 2: the AES decrypt implementation, certified against a real puzzle blob.
    # The phase-2 blob's password is a known stage answer, so this exercises
    # evp_bytes_to_key + AES-256-CBC + PKCS7 unpadding end to end against material
    # the puzzle itself published, rather than against a self-made vector.
    phase2_password = sha256(b"causality").hex()
    recovered = decrypt_blob(PHASE2_BLOB_B64, phase2_password)
    part2 = recovered is not None and PHASE2_MARKER in recovered
    print(f"phase-2 blob decrypts under sha256(\"causality\"): {'OK' if part2 else 'FAIL'}")
    ok = ok and part2

    # Part 2b: a wrong password must not validate (no false positive from a
    # coincidentally-valid PKCS7 padding byte).
    wrong = decrypt_blob(PHASE2_BLOB_B64, "definitely the wrong password")
    part2b = wrong is None
    print(f"wrong password on the same blob -> no valid padding: {'OK' if part2b else 'FAIL'}")
    ok = ok and part2b

    # Part 2c: MD5 must fail on the phase-2 blob specifically. This does NOT mean MD5
    # is unused in the puzzle: the Cosmic Duality blob uses MD5 (verified against its
    # published plaintext hash). The two digests appear on different blobs, which is
    # why attempt() tries both rather than assuming either.
    def _md5_derive(password, salt, key_len, iv_len):
        derived, prev = b"", b""
        while len(derived) < key_len + iv_len:
            prev = hashlib.md5(prev + password + salt).digest()
            derived += prev
        return derived[:key_len], derived[key_len:key_len + iv_len]

    raw2 = base64.b64decode(PHASE2_BLOB_B64)
    k2, iv2 = _md5_derive(phase2_password.encode("utf-8"), raw2[8:16], 32, 16)
    md5_plain = AES.new(k2, AES.MODE_CBC, iv2).decrypt(raw2[16:])
    part2c = unpad_pkcs7(md5_plain) is None
    print(f"MD5 fails on the phase-2 blob specifically: {'OK' if part2c else 'FAIL'}")
    ok = ok and part2c

    # Part 3: the real blob decodes to the documented shape (96 bytes total,
    # 8-byte salt, 80 bytes ciphertext = 5 AES blocks), independent of password.
    raw = base64.b64decode(BLOB_B64)
    part3 = raw[:8] == b"Salted__" and len(raw) == 96 and raw[8:16].hex() == "3ab585348552415d"
    print(f"published blob shape (96 bytes, salt 3ab585348552415d): {'OK' if part3 else 'FAIL'}")
    ok = ok and part3

    if ok:
        print("SELFTEST OK")
        print(
            "Note: part 1 certifies the address half against on-chain data; parts 2, "
            "2b and 2c certify the key-derivation and AES half against a real puzzle "
            "blob whose password is known. The puzzle uses SHA-256 on phases 2 and 3 "
            "and MD5 on Cosmic Duality, so attempt() tries both. X remains unsolved."
        )
    return ok


def _print_result(candidate: str) -> bool:
    matched, info = attempt(candidate)
    if matched:
        print(f"MATCH {info['address']} reading={info['reading']} priv_hex={info['priv_hex']} wif={info['wif']}")
    else:
        print("NO MATCH")
    return matched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidate", nargs="?", help="candidate answer string X")
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
