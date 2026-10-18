#!/usr/bin/env python3
"""Oracle for Arweave Puzzle Weave #12 (400.00 AR).

Purpose: check whether a candidate answer string decrypts the puzzle's on-page AES
ciphertext to a valid Arweave RSA wallet keyfile (a JSON blob containing "kty":"RSA")
whose derived address equals the escrow address XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg.

Mechanism (reversed from the live puzzle page, an unmodified CryptoJS bundle shared by
several puzzles in this author's series):
  1. key_hex = SHA-512 applied 11,513 times to the candidate string (the page passes the single free-text field through unmodified: case-sensitive, no trimming).
  2. The page ciphertext is OpenSSL-format ("Salted__" + 8-byte salt + AES-CBC body).
     key_hex is used as an EvpKDF (MD5, 10,000 iterations) password to derive a
     128-byte key and 16-byte IV -- CryptoJS's own non-standard AES.keySize=32 override
     (crypto-js issue #293), which makes this a 1024-bit-key, 38-round Rijndael
     variant, not textbook AES-256. That variant is reimplemented here in pure Python,
     since no dependency available to this repository supports a non-standard Rijndael
     key size; the round function and key schedule were checked to reproduce
     pycryptodome's output exactly at the standard AES-256 parameters (Nk=8, Nr=14)
     before being trusted at this puzzle's Nk=32/Nr=38.
  3. PKCS7-unpad, then truncate at the first null byte (matches the page's own hex2a()).
  4. Success iff the plaintext contains the literal substring "kty":"RSA".
  5. On success, the wallet address is base64url(SHA-256(raw bytes of the JWK's
     modulus "n")).

Usage:
  python3 oracle.py --selftest        # reproduces the solved sibling Arweave #8
  python3 oracle.py "<candidate>"     # MATCH / NO MATCH, exit 0 / 1
  python3 oracle.py --stdin           # one candidate per line, prints MATCH lines only

Input: a single answer string on the command line, or one per line on stdin.
Expected output: "SELFTEST OK" (exit 0) or "SELFTEST FAILED" (exit 1) for --selftest;
"MATCH <address>" or "NO MATCH" per candidate otherwise.
"""
import base64
import hashlib
import json
import sys

# ---------------------------------------------------------------------- puzzle constants
ESCROW = "XRGEfkMbCMHeTY9mZI9Lh6hf8EmA8RstmBFUjDm40fg"
CIPHERTEXT_B64 = "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"
LOWERCASE_INPUT = False
STRETCH_ROUNDS = 11513

# Calibration vector: the solved sibling Arweave Puzzle Weave #8 (solved 2020-03-07,
# escrow already spent, checked 2026-08-16). Reproducing it byte-for-byte certifies
# every stage of this pipeline before any candidate for THIS puzzle is trusted.
PZL8_CIPHERTEXT_B64 = "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"
PZL8_ANSWER = "RasputinWilhelmAlekhine"
PZL8_ADDRESS = "ayJQH1S6Fi52OEokLVi2tl5kr_y39LSfhJcNV0z9Ny4"

GATE = '"kty":"RSA"'

# ---------------------------------------------------------------------- Rijndael (Nk, Nr generalized)
# Standard FIPS-197 S-box / round structure, generalized only in key length (Nk words)
# and round count (Nr = Nk + 6). At Nk=8 this is textbook AES-256 (Nr=14); at Nk=32
# (this puzzle's non-standard 1024-bit key) it is Nr=38.
SBOX = [
    0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,
    0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,
    0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,
    0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,
    0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,
    0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,
    0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,
    0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,
    0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,
    0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,
    0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,
    0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,
    0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,
    0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,
    0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,
    0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16,
]
INV_SBOX = [0] * 256
for _i, _v in enumerate(SBOX):
    INV_SBOX[_v] = _i
RCON = [0x00,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36,0x6C,0xD8,0xAB,0x4D]


def _sub_word(w):
    return ((SBOX[(w >> 24) & 0xFF] << 24) | (SBOX[(w >> 16) & 0xFF] << 16)
             | (SBOX[(w >> 8) & 0xFF] << 8) | SBOX[w & 0xFF])


def _rot_word(w):
    return ((w << 8) | (w >> 24)) & 0xFFFFFFFF


def _key_expansion(key_bytes):
    nk = len(key_bytes) // 4
    nr = nk + 6
    total_words = 4 * (nr + 1)
    w = [int.from_bytes(key_bytes[4 * i:4 * i + 4], "big") for i in range(nk)]
    for o in range(nk, total_words):
        s = w[o - 1]
        if o % nk == 0:
            s = _sub_word(_rot_word(s)) ^ (RCON[o // nk] << 24)
        elif nk > 6 and o % nk == 4:
            s = _sub_word(s)
        w.append((w[o - nk] ^ s) & 0xFFFFFFFF)
    return w, nr


def _gmul(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p & 0xFF


def _inv_shift_rows(state):
    out = bytearray(16)
    for r in range(4):
        for c in range(4):
            out[r + 4 * c] = state[r + 4 * ((c - r) % 4)]
    return bytes(out)


def _inv_mix_columns(state):
    out = bytearray(16)
    for c in range(4):
        s0, s1, s2, s3 = state[4 * c:4 * c + 4]
        out[4 * c + 0] = _gmul(s0, 14) ^ _gmul(s1, 11) ^ _gmul(s2, 13) ^ _gmul(s3, 9)
        out[4 * c + 1] = _gmul(s0, 9) ^ _gmul(s1, 14) ^ _gmul(s2, 11) ^ _gmul(s3, 13)
        out[4 * c + 2] = _gmul(s0, 13) ^ _gmul(s1, 9) ^ _gmul(s2, 14) ^ _gmul(s3, 11)
        out[4 * c + 3] = _gmul(s0, 11) ^ _gmul(s1, 13) ^ _gmul(s2, 9) ^ _gmul(s3, 14)
    return bytes(out)


def _add_round_key(state, words, round_idx):
    out = bytearray(state)
    for c in range(4):
        wb = words[round_idx * 4 + c].to_bytes(4, "big")
        for r in range(4):
            out[r + 4 * c] ^= wb[r]
    return bytes(out)


def _decrypt_block(ct_block, w, nr):
    state = _add_round_key(ct_block, w, nr)
    for rnd in range(nr - 1, 0, -1):
        state = _inv_shift_rows(state)
        state = bytes(INV_SBOX[b] for b in state)
        state = _add_round_key(state, w, rnd)
        state = _inv_mix_columns(state)
    state = _inv_shift_rows(state)
    state = bytes(INV_SBOX[b] for b in state)
    state = _add_round_key(state, w, 0)
    return state


def _cbc_decrypt(ciphertext, key, iv):
    w, nr = _key_expansion(key)
    prev = iv
    out = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i + 16]
        out += bytes(a ^ b for a, b in zip(_decrypt_block(block, w, nr), prev))
        prev = block
    return bytes(out)


# ---------------------------------------------------------------------- KDF and pipeline
def _stretch(passphrase):
    buf = hashlib.sha512(passphrase.encode("utf-8")).digest()
    for _ in range(STRETCH_ROUNDS - 1):
        buf = hashlib.sha512(buf).digest()
    return buf.hex()


def _evp_bytes_to_key(password, salt, key_len, iv_len, iterations):
    total = key_len + iv_len
    derived = b""
    prev = b""
    while len(derived) < total:
        block = hashlib.md5(prev + password + salt).digest()
        for _ in range(iterations - 1):
            block = hashlib.md5(block).digest()
        derived += block
        prev = block
    return derived[:key_len], derived[key_len:key_len + iv_len]


def _pkcs7_unpad(data):
    if not data:
        return data
    pad = data[-1]
    if 1 <= pad <= 16 and pad <= len(data):
        return data[:-pad]
    return data


def _b64url_decode(s):
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def jwk_to_address(n_b64url):
    digest = hashlib.sha256(_b64url_decode(n_b64url)).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


def decode_wallet(ciphertext_b64, passphrase):
    """Returns the decrypted plaintext string (empty/garbage on a wrong passphrase)."""
    key_hex = _stretch(passphrase)
    raw = base64.b64decode(ciphertext_b64)
    if raw[:8] != b"Salted__":
        return ""
    salt, body = raw[8:16], raw[16:]
    key, iv = _evp_bytes_to_key(key_hex.encode("ascii"), salt, 128, 16, 10000)
    plain = _pkcs7_unpad(_cbc_decrypt(body, key, iv))
    nul = plain.find(b"\x00")
    if nul != -1:
        plain = plain[:nul]
    return plain.decode("latin-1", errors="replace")


def check(candidate):
    """Returns (ok, address_or_none)."""
    if LOWERCASE_INPUT:
        candidate = candidate.lower()
    out = decode_wallet(CIPHERTEXT_B64, candidate)
    if GATE not in out:
        return False, None
    try:
        addr = jwk_to_address(json.loads(out)["n"])
    except Exception:
        return False, None
    return True, addr


# ---------------------------------------------------------------------- selftest / CLI
def selftest():
    out = decode_wallet(PZL8_CIPHERTEXT_B64, PZL8_ANSWER)
    if GATE not in out:
        print("SELFTEST FAILED: solved-sibling Arweave #8 vector did not decrypt")
        return False
    try:
        addr = jwk_to_address(json.loads(out)["n"])
    except Exception as exc:
        print("SELFTEST FAILED: could not parse recovered JWK (%s)" % exc)
        return False
    if addr != PZL8_ADDRESS:
        print("SELFTEST FAILED: address %s != expected %s" % (addr, PZL8_ADDRESS))
        return False
    if GATE in decode_wallet(PZL8_CIPHERTEXT_B64, PZL8_ANSWER.lower()):
        print("SELFTEST FAILED: lowercased answer incorrectly matched (gate is not case-sensitive)")
        return False
    print("SELFTEST OK: solved sibling Arweave #8, answer %r -> %s" % (PZL8_ANSWER, addr))
    return True


def main():
    if len(sys.argv) < 2:
        print('usage: oracle.py --selftest | "<candidate>" | --stdin', file=sys.stderr)
        sys.exit(2)
    if sys.argv[1] == "--selftest":
        sys.exit(0 if selftest() else 1)
    if sys.argv[1] == "--stdin":
        found = False
        for line in sys.stdin:
            cand = line.rstrip("\n")
            if not cand:
                continue
            ok, addr = check(cand)
            if ok:
                print("MATCH %s <- %r" % (addr, cand))
                found = True
        sys.exit(0 if found else 1)
    candidate = sys.argv[1]
    ok, addr = check(candidate)
    if ok:
        print("MATCH %s" % addr)
        sys.exit(0)
    print("NO MATCH")
    sys.exit(1)


if __name__ == "__main__":
    main()
