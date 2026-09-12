#!/usr/bin/env python3
"""
oracle.py -- candidate checker for "Path to Greatness: Treasure Hunt" (jpatt94).

Purpose:
    The author published his own encryption scheme on the fake desktop screenshot
    served as clue "computer_screen.jpg". A Litecoin WIF is encrypted with AES-256-CBC
    under a 32-byte super_key; that super_key is cut into four 8-byte segments, and each
    segment is encrypted separately under its own 16-character IV (an album track title)
    with a key made of two clue answers concatenated as raw ASCII.

    Because each segment is one AES block holding 8 useful bytes, its plaintext must end
    with a PKCS7 padding of eight 0x08 bytes. That is an exact per-segment oracle with a
    false positive rate of 2^-64, and it needs nothing from the other six answers. One
    pair of clue answers can therefore be refuted on its own, in microseconds.

    Three layers, each with its own verdict:
      L1  segment_oracle(i, key32)  -> the 8 super_key bytes, or None
      L2  superkey_to_wif(key32)    -> the WIF string, or None
      L3  address_from_wif(wif)     -> compared character by character with the escrow

    A solution is declared only on exact equality at L3. A valid padding at L1 is a
    filter, not an answer.

Usage:
    python3 tools/oracle.py --selftest                      # must print SELFTEST OK
    python3 tools/oracle.py --segment 1 <answer1> <answer6> # one pair, MATCH / NO MATCH
    python3 tools/oracle.py --answers <a1> <a2> ... <a8>    # all eight, in clue order
    python3 tools/oracle.py --stdin-segment 1               # one "a b" pair per line

Input:
    Clue answers as written. Normalisation is applied here exactly as the author's
    fix_clues.script states it: spaces removed everywhere, lowercased except clue 4.

Output:
    "MATCH ..." or "NO MATCH ...". Exit 0 on a match, 1 otherwise. --selftest exits 0
    after printing SELFTEST OK.

Dependencies:
    stdlib, pycryptodome (AES, RIPEMD160 fallback), coincurve, ecdsa.
    No network access, no files read.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import sys

from Crypto.Cipher import AES

TARGET_ADDRESS = "LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS"
LTC_P2PKH_VERSION = 0x30          # 48, addresses start with 'L'
LTC_WIF_VERSION = 0xB0            # 176 = 48 + 128, WIF starts with 'T' or '6'

# ----------------------------------------------------------------- author's scheme
# Transcribed from the author's own clue image clues/computer_screen.jpg.
# Window 1, litecoin_wallet.txt: the encrypted WIF and its IV.
WIF_BLOB_B64 = ("dxIx52zhnXodWi36dEx/kJV59Udj4xh3vR5vmeuoyXTNCE8VOaTmVkVctDpK"
                "0XNHYJA6G+m/jT4fSU9VejXYgg==")
WIF_IV = b"goodluck_havefun"       # 16 characters exactly

# Window 2, super_key_segments.sheet, plus window 3, clues.sheet:
# segment id -> (ciphertext base64, super_key byte range, IV, (left clue, right clue))
SEGMENTS = {
    1: ("I2c6TXU/Z1oCKnEQTWZUvg==", (0, 7),   b"few_n_far_btween", (1, 6)),
    2: ("RWaBo4ChEOM/i+MLy2NUpg==", (8, 15),  b"nocturnal_sugars", (4, 5)),
    3: ("16GmtUINaYuN7f1RlBO5sQ==", (16, 23), b"colors_on_leaves", (3, 7)),
    4: ("7CZlZjwCMGUb/TZm07b9dg==", (24, 31), b"seconds_of_dream", (2, 8)),
}

# clue id -> (name, segment it feeds, byte range inside that segment's AES key).
# The range is what fixes each answer's exact length, which is the free filter.
CLUES = {
    1: ("imagine",  1, (0, 15)),
    2: ("scramble", 4, (0, 14)),
    3: ("wasd",     3, (0, 7)),
    4: ("chess",    2, (0, 11)),
    5: ("wonders",  2, (12, 31)),
    6: ("beach",    1, (16, 31)),
    7: ("ship",     3, (8, 31)),
    8: ("sky",      4, (15, 31)),
}
ANSWER_LEN = {i: hi - lo + 1 for i, (_, _, (lo, hi)) in CLUES.items()}

_SEG_CT = {i: base64.b64decode(v[0]) for i, v in SEGMENTS.items()}


def normalise_answer(clue_id: int, raw: str) -> str:
    """fix_clues.script: remove_spaces() everywhere, to_lowercase() except clue 4."""
    s = raw.replace(" ", "")
    if clue_id != 4:
        s = s.lower()
    return s


# ------------------------------------------------------------------- primitives
def _ripemd160(data: bytes) -> bytes:
    try:
        h = hashlib.new("ripemd160")
        h.update(data)
        return h.digest()
    except Exception:
        from Crypto.Hash import RIPEMD160
        return RIPEMD160.new(data).digest()


def hash160(data: bytes) -> bytes:
    return _ripemd160(hashlib.sha256(data).digest())


_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check_encode(payload: bytes) -> str:
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    raw = payload + chk
    n = int.from_bytes(raw, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = _B58[r] + out
    return "1" * (len(raw) - len(raw.lstrip(b"\x00"))) + out


def b58check_decode(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + _B58.index(c)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    raw = b"\x00" * (len(s) - len(s.lstrip("1"))) + raw
    payload, chk = raw[:-4], raw[-4:]
    if hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4] != chk:
        raise ValueError("base58 checksum invalid: " + s)
    return payload


def pubkey_from_priv(priv32: bytes, compressed: bool = True) -> bytes:
    from coincurve import PublicKey
    return PublicKey.from_valid_secret(priv32).format(compressed=compressed)


def address_from_priv(priv32: bytes, compressed: bool = True,
                      version: int = LTC_P2PKH_VERSION) -> str:
    return b58check_encode(bytes([version]) + hash160(pubkey_from_priv(priv32, compressed)))


def wif_encode(priv32: bytes, compressed: bool = True,
               version: int = LTC_WIF_VERSION) -> str:
    body = bytes([version]) + priv32 + (b"\x01" if compressed else b"")
    return b58check_encode(body)


def wif_decode(wif: str):
    """-> (priv32, compressed, version). Raises ValueError when malformed."""
    p = b58check_decode(wif)
    version, body = p[0], p[1:]
    if len(body) == 33 and body[-1] == 0x01:
        return body[:32], True, version
    if len(body) == 32:
        return body, False, version
    raise ValueError("unexpected WIF body length: %d" % len(body))


def address_from_wif(wif: str) -> str:
    priv, compressed, _ = wif_decode(wif)
    return address_from_priv(priv, compressed)


# ------------------------------------------------------------------------- L3
def is_solution(candidate_wif: str) -> bool:
    """Final verdict. True only on exact, character by character equality."""
    try:
        return address_from_wif(candidate_wif) == TARGET_ADDRESS
    except Exception:
        return False


# ------------------------------------------------------------------------- L1
def segment_oracle(seg_id: int, key32: bytes):
    """AES-256-CBC decrypt of one segment. Returns its 8 super_key bytes, or None."""
    if len(key32) != 32:
        return None
    pt = AES.new(key32, AES.MODE_CBC, SEGMENTS[seg_id][2]).decrypt(_SEG_CT[seg_id])
    if pt[8:] != b"\x08" * 8:
        return None
    return pt[:8]


def segment_key(seg_id: int, answers: dict):
    """Concatenate the two answers of a segment. Returns 32 bytes, or None."""
    a, b = SEGMENTS[seg_id][3]
    ka, kb = answers.get(a), answers.get(b)
    if ka is None or kb is None:
        return None
    key = (ka + kb).encode()
    return key if len(key) == 32 else None


# ------------------------------------------------------------------------- L2
def superkey_to_wif(key32: bytes):
    """Decrypt the WIF blob. Returns the WIF string if the padding is coherent."""
    if len(key32) != 32:
        return None
    pt = AES.new(key32, AES.MODE_CBC, WIF_IV).decrypt(base64.b64decode(WIF_BLOB_B64))
    pad = pt[-1]
    if not (1 <= pad <= 16) or pt[-pad:] != bytes([pad]) * pad:
        return None
    try:
        return pt[:-pad].decode("ascii")
    except UnicodeDecodeError:
        return None


def solve_from_answers(answers: dict):
    """answers = {clue_id: normalised answer}. Returns (wif, address) or None."""
    super_key = bytearray(32)
    for seg_id in (1, 2, 3, 4):
        key = segment_key(seg_id, answers)
        if key is None:
            return None
        eight = segment_oracle(seg_id, key)
        if eight is None:
            return None
        lo, hi = SEGMENTS[seg_id][1]
        super_key[lo:hi + 1] = eight
    wif = superkey_to_wif(bytes(super_key))
    if wif is None:
        return None
    try:
        return wif, address_from_wif(wif)
    except Exception:
        return wif, None


# --------------------------------------------------------------------- selftest
def selftest(verbose: bool = True) -> bool:
    ok = True

    def say(*a):
        if verbose:
            print(*a)

    say("=" * 72)
    say("SELFTEST -- witnesses at head, middle and tail")
    say("=" * 72)

    # T1: the escrow decodes as a Litecoin P2PKH address.
    payload = b58check_decode(TARGET_ADDRESS)
    t1 = payload[0] == LTC_P2PKH_VERSION and len(payload) == 21
    say("T1  escrow base58check version=0x%02x len=%d hash160=%s  -> %s"
        % (payload[0], len(payload), payload[1:].hex(), "OK" if t1 else "FAIL"))
    ok &= t1

    # T2: the EC and hash160 pipeline against the canonical Bitcoin vectors for key 1.
    k1 = b"\x00" * 31 + b"\x01"
    vectors = {True: "1BgGZ9tcN4rm9KBzDn7KprQz87SZ26SAMH",
               False: "1EHNa6Q4Jz2uvNExL497mE43ikXhwF6kZm"}
    t2 = True
    for compressed, want in vectors.items():
        got = b58check_encode(bytes([0x00]) + hash160(pubkey_from_priv(k1, compressed)))
        t2 &= got == want
        say("T2  privkey=1 %-14s -> %s  -> %s"
            % ("compressed" if compressed else "uncompressed", got,
               "OK" if got == want else "FAIL"))
    ok &= t2

    # T3: cross-check the curve against a second, independent implementation.
    import ecdsa as _ecdsa

    def pub_ecdsa(k, compressed):
        sk = _ecdsa.SigningKey.from_string(k, curve=_ecdsa.SECP256k1)
        point = sk.get_verifying_key().pubkey.point
        x, y = point.x(), point.y()
        if compressed:
            return bytes([2 + (y & 1)]) + x.to_bytes(32, "big")
        return b"\x04" + x.to_bytes(32, "big") + y.to_bytes(32, "big")

    t3 = True
    n_cross = 0
    for compressed in (True, False):
        for tag in (b"head", b"middle", b"tail", b"p2g"):
            k = hashlib.sha256(tag).digest()
            if pubkey_from_priv(k, compressed) != pub_ecdsa(k, compressed):
                t3 = False
                say("    disagreement coincurve vs ecdsa, compressed=%s tag=%s"
                    % (compressed, tag.decode()))
            n_cross += 1
    say("T3  %d keys cross-checked on 2 independent curve implementations  -> %s"
        % (n_cross, "OK" if t3 else "FAIL"))
    ok &= t3

    # T3b: optional third opinion on the Litecoin version bytes and the WIF encoder.
    try:
        from bip_utils import (P2PKHAddrEncoder, Secp256k1PublicKey, WifEncoder,
                               P2PKHPubKeyModes)
        from bip_utils.coin_conf import CoinsConf
        ltc_ver = CoinsConf.LitecoinMainNet.ParamByKey("p2pkh_std_net_ver")
        ltc_wif = CoinsConf.LitecoinMainNet.ParamByKey("wif_net_ver")
        t3b = ltc_ver[0] == LTC_P2PKH_VERSION and ltc_wif[0] == LTC_WIF_VERSION
        k = hashlib.sha256(b"p2g-version-check").digest()
        theirs = P2PKHAddrEncoder.EncodeKey(
            Secp256k1PublicKey.FromBytes(pubkey_from_priv(k, True)),
            net_ver=ltc_ver, pub_key_mode=P2PKHPubKeyModes.COMPRESSED)
        t3b &= theirs == address_from_priv(k, True)
        t3b &= WifEncoder.Encode(k, net_ver=ltc_wif,
                                 pub_key_mode=P2PKHPubKeyModes.COMPRESSED) == wif_encode(k, True)
        say("T3b Litecoin version bytes and WIF encoder agree with a third library  -> %s"
            % ("OK" if t3b else "FAIL"))
        ok &= t3b
    except ImportError:
        say("T3b third library not installed, skipped (not required)")

    # T4: WIF round trip, both compression modes. Litecoin WIF starts with T or 6.
    t4 = True
    for compressed in (True, False):
        k = hashlib.sha256(b"p2g-wif-%d" % compressed).digest()
        w = wif_encode(k, compressed)
        if wif_decode(w) != (k, compressed, LTC_WIF_VERSION):
            t4 = False
        say("    WIF compressed=%-5s %s  len=%d  prefix=%s  -> address %s"
            % (compressed, w, len(w), w[0], address_from_wif(w)))
    say("T4  WIF round trip, compressed and uncompressed  -> %s" % ("OK" if t4 else "FAIL"))
    ok &= t4

    # T5: three control negatives must be rejected.
    bad = wif_encode(hashlib.sha256(b"definitely-not-the-key").digest(), True)
    t5 = (not is_solution(bad)) and (not is_solution("not-even-base58")) \
        and (not is_solution(TARGET_ADDRESS))
    say("T5  3 control negatives rejected  -> %s" % ("OK" if t5 else "FAIL"))
    ok &= t5

    # T6: the segment oracle itself, with a synthetic witness taking the normal path.
    known_key = hashlib.sha256(b"witness-key").digest()
    known_eight = b"ABCDEFGH"
    ct = AES.new(known_key, AES.MODE_CBC, SEGMENTS[1][2]).encrypt(known_eight + b"\x08" * 8)
    saved = _SEG_CT[1]
    _SEG_CT[1] = ct
    hit = segment_oracle(1, known_key)
    false_positives = sum(1 for i in range(1024)
                          if segment_oracle(1, hashlib.sha256(b"wrong-%d" % i).digest())
                          is not None)
    _SEG_CT[1] = saved
    t6 = hit == known_eight and false_positives == 0
    say("T6  segment oracle: witness re-found=%r, false positives on 1024 keys=%d  -> %s"
        % (hit, false_positives, "OK" if t6 else "FAIL"))
    ok &= t6

    # T7: the WIF layer, with a synthetic witness wallet.
    global WIF_BLOB_B64
    real_wif = wif_encode(hashlib.sha256(b"witness-wallet").digest(), True)
    sk = hashlib.sha256(b"witness-superkey").digest()
    pad = 16 - (len(real_wif) % 16)
    blob = AES.new(sk, AES.MODE_CBC, WIF_IV).encrypt(real_wif.encode() + bytes([pad]) * pad)
    saved_blob = WIF_BLOB_B64
    WIF_BLOB_B64 = base64.b64encode(blob).decode()
    got = superkey_to_wif(sk)
    non_rejects = sum(1 for i in range(1024)
                      if superkey_to_wif(hashlib.sha256(b"nope-%d" % i).digest()) is not None)
    WIF_BLOB_B64 = saved_blob
    t7 = got == real_wif
    say("T7  WIF layer: witness WIF re-found=%s, non-rejects on 1024 keys=%d  -> %s"
        % (got == real_wif, non_rejects, "OK" if t7 else "FAIL"))
    say("    (a non-reject at this layer is not a false positive: the address decides)")
    ok &= t7

    # T8: the author's composition scheme has to add up, character for character.
    say("-" * 72)
    say("T8  composition scheme published by the author")
    t8 = True
    for seg_id, (ct_b64, (lo, hi), iv, (a, b)) in sorted(SEGMENTS.items()):
        la, lb = ANSWER_LEN[a], ANSWER_LEN[b]
        good = (la + lb == 32) and len(iv) == 16 and (hi - lo + 1) == 8 \
            and len(base64.b64decode(ct_b64)) == 16
        t8 &= good
        say("    seg %d  bytes %2d-%2d  IV %-16s  clue %d (%2d) + clue %d (%2d) = %2d  %s"
            % (seg_id, lo, hi, iv.decode(), a, la, b, lb, la + lb, "OK" if good else "FAIL"))
    total = sum(ANSWER_LEN.values())
    blob_len = len(base64.b64decode(WIF_BLOB_B64))
    say("    8 answers = %d characters; 4 AES-256 keys = 128 bytes  -> %s"
        % (total, "OK" if total == 128 else "FAIL"))
    say("    WIF blob = %d bytes = %d AES blocks; a WIF is 51 or 52 characters  -> %s"
        % (blob_len, blob_len // 16, "OK" if blob_len == 64 else "FAIL"))
    t8 &= total == 128 and blob_len == 64
    ok &= t8

    # T9: base64 canonicity. A 16-byte ciphertext ends in "==" and its 22nd character
    # carries only 2 useful bits, so it can only be A, Q, g or w. Any transcription that
    # breaks this is wrong without calling the oracle at all.
    t9 = True
    for seg_id, (ct_b64, _r, _iv, _c) in sorted(SEGMENTS.items()):
        c22 = ct_b64[21]
        good = c22 in "AQgw" and ct_b64.endswith("==") and len(ct_b64) == 24
        t9 &= good
        say("T9  segment %d ciphertext 22nd character = %r  -> %s"
            % (seg_id, c22, "OK" if good else "FAIL"))
    ok &= t9

    say("=" * 72)
    if ok:
        say("SELFTEST OK")
    else:
        say("SELFTEST FAILED, conclude nothing")
    return ok


# -------------------------------------------------------------------------- CLI
def _check_segment(seg_id: int, raw_left: str, raw_right: str, quiet: bool = False) -> bool:
    clue_a, clue_b = SEGMENTS[seg_id][3]
    left = normalise_answer(clue_a, raw_left)
    right = normalise_answer(clue_b, raw_right)
    for clue_id, value in ((clue_a, left), (clue_b, right)):
        if len(value) != ANSWER_LEN[clue_id]:
            if not quiet:
                print("NO MATCH (clue %d '%s' is %d characters after normalisation, "
                      "the author's scheme requires %d)"
                      % (clue_id, CLUES[clue_id][0], len(value), ANSWER_LEN[clue_id]))
            return False
    eight = segment_oracle(seg_id, (left + right).encode())
    if eight is None:
        if not quiet:
            print("NO MATCH segment %d" % seg_id)
        return False
    lo, hi = SEGMENTS[seg_id][1]
    print("MATCH segment %d: super_key bytes %d-%d = %s"
          % (seg_id, lo, hi, eight.hex()))
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Candidate checker for Path to Greatness: Treasure Hunt.")
    parser.add_argument("--selftest", action="store_true",
                        help="reproduce the author's scheme and the witness protocol")
    parser.add_argument("--segment", nargs=3, metavar=("N", "LEFT", "RIGHT"),
                        help="check one pair of clue answers against segment N (1 to 4)")
    parser.add_argument("--stdin-segment", type=int, metavar="N",
                        help="read 'left right' pairs for segment N, one per line")
    parser.add_argument("--answers", nargs=8, metavar="A",
                        help="the eight clue answers, in clue order 1 to 8")
    args = parser.parse_args()

    if args.selftest:
        return 0 if selftest() else 1

    if args.segment:
        seg_id = int(args.segment[0])
        if seg_id not in SEGMENTS:
            print("segment must be 1, 2, 3 or 4")
            return 2
        return 0 if _check_segment(seg_id, args.segment[1], args.segment[2]) else 1

    if args.stdin_segment:
        seg_id = args.stdin_segment
        if seg_id not in SEGMENTS:
            print("segment must be 1, 2, 3 or 4")
            return 2
        found = False
        for line in sys.stdin:
            parts = line.split()
            if len(parts) != 2:
                continue
            if _check_segment(seg_id, parts[0], parts[1], quiet=True):
                found = True
        if not found:
            print("NO MATCH segment %d" % seg_id)
        return 0 if found else 1

    if args.answers:
        answers = {i + 1: normalise_answer(i + 1, a) for i, a in enumerate(args.answers)}
        for clue_id, value in sorted(answers.items()):
            if len(value) != ANSWER_LEN[clue_id]:
                print("NO MATCH (clue %d '%s' is %d characters after normalisation, "
                      "the author's scheme requires %d)"
                      % (clue_id, CLUES[clue_id][0], len(value), ANSWER_LEN[clue_id]))
                return 1
        result = solve_from_answers(answers)
        if result is None:
            print("NO MATCH (at least one segment fails its padding oracle)")
            return 1
        wif, address = result
        if address == TARGET_ADDRESS:
            print("MATCH %s" % TARGET_ADDRESS)
            print("WIF %s" % wif)
            return 0
        print("NO MATCH (the four segments passed but the address is %r, not %s)"
              % (address, TARGET_ADDRESS))
        return 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
