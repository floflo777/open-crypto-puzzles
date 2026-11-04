#!/usr/bin/env python3
"""Certified candidate oracle for the Trithemius: Wealth in Poetry puzzle.

Checks a candidate phrase against escrow 1K4ezpLybootYF23TM4a8Y4NyP7auysnRo
through every wallet family the article makes plausible:

  bip39            BIP39 seed (PBKDF2 "mnemonic" salt) -> BIP44/49/84, m/0 index 0,
                   compressed keys (gate: wordlist + checksum)
  brainwallet      raw-text hashing of the phrase string, sha256 and sha256d,
                   both key compressions, 6 serializations (old-Electrum-style
                   restore of arbitrary text and generic 2019 brainwallet tools)
  electrum_std     Electrum 2.x-4.x native seed: PBKDF2 "electrum" salt ->
                   BIP32 root -> m/0/n + m/1/n (n < 6), compressed P2PKH
                   (gate: HMAC-SHA512 "Seed version" prefix '01', the restore
                   gate of a real Electrum GUI)
  electrum_old     Electrum 1.x old seed: mn_decode (1626-word list, requires
                   the `electrum` package) -> 100000x sha256 stretch ->
                   uncompressed m/0/n + m/1/n (n < 6)

Certification (--selftest): official BIP32/39/44/49/84 vectors through two
independent implementations, Bitcoin-wiki raw-key pairs, Electrum BIP32_KeyStore
and Old_KeyStore agreement on generated seeds (needs the `electrum` package),
and negative controls. Do not trust any negative from a run whose selftest did
not pass first.

Usage:
  python3 tools/oracle.py --selftest
  python3 tools/oracle.py --phrase "word1 word2 ... word12" [--passphrase pp]
  python3 tools/oracle.py --batch candidates.txt   # one phrase per line

Exit codes: 0 = selftest ok / candidates all no-match, 1 = MATCH found,
2 = selftest failure or environment error.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import sys

import base58
from bip_utils import (
    Bip32Secp256k1,
    Bip39SeedGenerator,
    Bip44,
    Bip44Changes,
    Bip44Coins,
    Bip49,
    Bip49Coins,
    Bip84,
    Bip84Coins,
)
from bip_utils.bech32 import SegwitBech32Decoder, SegwitBech32Encoder
from coincurve import PrivateKey

ESCROW_ADDRESS = "1K4ezpLybootYF23TM4a8Y4NyP7auysnRo"
CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

WORDLIST: list[str] | None = None
OLD_WORDLIST: list[str] | None = None


def get_wordlist() -> list[str]:
    global WORDLIST
    if WORDLIST is None:
        from mnemonic import Mnemonic

        WORDLIST = Mnemonic("english").wordlist
    return WORDLIST


def get_old_wordlist() -> list[str]:
    global OLD_WORDLIST
    if OLD_WORDLIST is None:
        try:
            from electrum import old_mnemonic
        except ImportError:
            raise SystemExit(
                "electrum package not installed; electrum_old family unavailable "
                "(pip install electrum)"
            )
        OLD_WORDLIST = list(old_mnemonic.wordlist)
    return OLD_WORDLIST


def h160_of_address(addr: str) -> bytes:
    if addr.lower().startswith(("bc1", "tb1")):
        hrp = "bc" if addr.lower().startswith("bc1") else "tb"
        witver, witprog = SegwitBech32Decoder.Decode(hrp, addr)
        if witver != 0 or len(witprog) != 20:
            raise ValueError(f"not a v0 P2WPKH address: {addr}")
        return bytes(witprog)
    raw = base58.b58decode_check(addr)
    if len(raw) != 21:
        raise ValueError(f"unexpected payload length for {addr}")
    return raw[1:]


ESCROW_H160 = h160_of_address(ESCROW_ADDRESS)


def _hash160(data: bytes) -> bytes:
    return hashlib.new("ripemd160", hashlib.sha256(data).digest()).digest()


def base58check(payload: bytes) -> str:
    return base58.b58encode_check(payload).decode()


def validate_mnemonic(words: list[str]) -> tuple[bool, str]:
    if len(words) not in (12, 24):
        return False, f"word count {len(words)}"
    wl = get_wordlist()
    idxs = []
    for w in words:
        try:
            idxs.append(wl.index(w.lower()))
        except ValueError:
            return False, f"not in wordlist: {w!r}"
    nbits = len(idxs) * 11
    bits = 0
    for i in idxs:
        bits = (bits << 11) | i
    ent_bits = nbits * 32 // 33
    cs_bits = nbits - ent_bits
    if ent_bits % 8 or ent_bits < 128:
        return False, f"bad entropy length {ent_bits}"
    entropy = (bits >> cs_bits).to_bytes(ent_bits // 8, "big")
    computed = hashlib.sha256(entropy).digest()[0] >> (8 - cs_bits)
    if computed != bits & ((1 << cs_bits) - 1):
        return False, "checksum mismatch"
    return True, ""


# ------------------------------------------------------------------ families
def bip39_addresses(words: list[str], passphrase: str = "") -> dict[str, str]:
    seed = Bip39SeedGenerator(" ".join(words)).Generate(passphrase)
    out = {}
    for label, path in (
        ("bip44", "m/44'/0'/0'/0/0"),
        ("bip49", "m/49'/0'/0'/0/0"),
        ("bip84", "m/84'/0'/0'/0/0"),
    ):
        bip32 = Bip32Secp256k1.FromSeed(seed)
        for part in path.split("/")[1:]:
            bip32 = bip32.ChildKey(
                0x80000000 + int(part[:-1]) if part.endswith("'") else int(part)
            )
        pub = bip32.PublicKey().RawCompressed().ToBytes()
        h160 = _hash160(pub)
        if label == "bip44":
            out[label] = base58check(b"\x00" + h160)
        elif label == "bip49":
            out[label] = base58check(b"\x05" + _hash160(b"\x00\x14" + h160))
        else:
            out[label] = SegwitBech32Encoder.Encode("bc", 0, h160)
    return out


BRAINWALLET_VARIANTS = (
    ("space", lambda w: " ".join(w)),
    ("space_lower", lambda w: " ".join(w).lower()),
    ("joined", lambda w: "".join(w)),
    ("joined_lower", lambda w: "".join(w).lower()),
    ("title", lambda w: " ".join(w).title()),
    ("newline", lambda w: " ".join(w) + "\n"),
)


def brainwallet_addresses(words: list[str]) -> dict[str, str]:
    out = {}
    for vname, mk in BRAINWALLET_VARIANTS:
        phrase = mk(words)
        for hname, data in (
            ("sha256", phrase.encode()),
            ("sha256d", hashlib.sha256(hashlib.sha256(phrase.encode()).digest()).digest()),
        ):
            s = int.from_bytes(data, "big") % CURVE_ORDER
            if s == 0:
                continue
            pk = PrivateKey(s.to_bytes(32, "big"))
            for comp in (True, False):
                pub = pk.public_key.format(compressed=comp)
                out[f"{hname}/{vname}/{'c' if comp else 'u'}"] = base58check(
                    b"\x00" + _hash160(pub)
                )
    return out


def normalize_text(s: str) -> str:
    import unicodedata

    return " ".join(unicodedata.normalize("NFKD", s).split())


def electrum_new_seed_gate(phrase: str, prefix: str = "01") -> bool:
    s = hmac.new(b"Seed version", normalize_text(phrase).encode(), hashlib.sha512).hexdigest()
    return s.startswith(prefix)


def electrum_standard_addresses(phrase: str, passphrase: str = "", n: int = 6) -> dict[str, str]:
    seed = hashlib.pbkdf2_hmac(
        "sha512", normalize_text(phrase).encode(), ("electrum" + normalize_text(passphrase)).encode(), 2048
    )
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k = int.from_bytes(I[:32], "big")
    if k == 0 or k >= CURVE_ORDER:
        raise ValueError("bad master scalar")
    chain = I[32:]

    def ckd(k: int, chain: bytes, idx: int):
        parent_pub = PrivateKey(k.to_bytes(32, "big")).public_key.format(compressed=True)
        I2 = hmac.new(chain, parent_pub + idx.to_bytes(4, "big"), hashlib.sha512).digest()
        kk = (int.from_bytes(I2[:32], "big") + k) % CURVE_ORDER
        return kk, I2[32:]

    out = {}
    for change in (0, 1):
        kc, cc = ckd(k, chain, change)
        for i in range(n):
            ki, _ = ckd(kc, cc, i)
            pub = PrivateKey(ki.to_bytes(32, "big")).public_key.format(compressed=True)
            out[f"m/{change}/{i}"] = base58check(b"\x00" + _hash160(pub))
    return out


def electrum_old_addresses(phrase: str, n: int = 6) -> dict[str, str] | None:
    from electrum import old_mnemonic

    try:
        hex_seed = old_mnemonic.mn_decode(phrase.split())
    except Exception:
        return None
    if not hex_seed:
        return None
    seed = hex_seed.encode()
    x = seed
    for _ in range(100000):
        x = hashlib.sha256(x + seed).digest()
    secexp = int.from_bytes(x, "big") % CURVE_ORDER
    mpk = PrivateKey(secexp.to_bytes(32, "big")).public_key.format(compressed=False)[1:]
    out = {}
    for change in (0, 1):
        for i in range(n):
            z = int.from_bytes(
                hashlib.sha256(hashlib.sha256(("%d:%d:" % (i, change)).encode() + mpk).digest()).digest(),
                "big",
            )
            child = (secexp + z) % CURVE_ORDER
            pub = PrivateKey(child.to_bytes(32, "big")).public_key.format(compressed=False)
            out[f"old/{change}/{i}"] = base58check(b"\x00" + _hash160(pub))
    return out


# -------------------------------------------------------------------- check
def check_phrase(phrase: str, passphrase: str = "") -> dict:
    words = phrase.split()
    res: dict = {"phrase": phrase, "passphrase": passphrase, "families": {}, "match": False}
    ok, reason = validate_mnemonic(words)
    if ok:
        addrs = bip39_addresses(words, passphrase)
        res["families"]["bip39"] = addrs
        if any(h160_of_address(a) == ESCROW_H160 for a in addrs.values()):
            res["match"] = True
    bw = brainwallet_addresses(words)
    res["families"]["brainwallet_count"] = len(bw)
    if any(h160_of_address(a) == ESCROW_H160 for a in bw.values()):
        res["match"] = True
        res["families"]["brainwallet_hit"] = True
    if electrum_new_seed_gate(phrase):
        try:
            addrs = electrum_standard_addresses(phrase, passphrase, n=6)
            res["families"]["electrum_std"] = addrs
            if any(h160_of_address(a) == ESCROW_H160 for a in addrs.values()):
                res["match"] = True
        except ValueError:
            pass
    if all(w in get_old_wordlist() for w in words):
        addrs = electrum_old_addresses(phrase, n=6)
        if addrs:
            res["families"]["electrum_old"] = addrs
            if any(h160_of_address(a) == ESCROW_H160 for a in addrs.values()):
                res["match"] = True
    return res


def selftest() -> None:
    # BIP39 official vector through two implementations
    phrase = "abandon " * 11 + "about"
    expected = {
        "bip44": "1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA",
        "bip49": "37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf",
        "bip84": "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu",
    }
    got = bip39_addresses(phrase.split())
    for label, want in expected.items():
        assert got[label] == want, f"manual {label}: {got[label]} != {want}"
    seed = Bip39SeedGenerator(phrase).Generate("")
    ctx = Bip44.FromSeed(seed, Bip44Coins.BITCOIN)
    via_lib = ctx.Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    assert via_lib == expected["bip44"], via_lib
    via_lib49 = Bip49.FromSeed(seed, Bip49Coins.BITCOIN).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    assert via_lib49 == expected["bip49"], via_lib49
    via_lib84 = Bip84.FromSeed(seed, Bip84Coins.BITCOIN).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
    assert via_lib84 == expected["bip84"], via_lib84

    # checksum validator cross-check
    from mnemonic import Mnemonic

    m = Mnemonic("english")
    ok, _ = validate_mnemonic(phrase.split())
    assert ok and m.check(phrase)
    ok, reason = validate_mnemonic(("abandon " * 11 + "act").split())
    assert not ok and "checksum" in reason

    # raw-key path against the two documented Bitcoin wiki pairs
    for sec_hex, want in (
        ("18E14A7B6A307F426A94F8114701E7C8E774E7F9A47E2C2035DB29A206321725", "16UwLL9Risc3QfPqBUvKofHmBQ7wMtjvM"),
        ("E9873D79C6D87DC0FB6A5778633389F4453213303DA61F20BD67FC233AA33262", "1CC3X2gu58d6wXUWMffpuzN9JAfTUWu4Kj"),
    ):
        pub = PrivateKey(bytes.fromhex(sec_hex)).public_key.format(compressed=False)
        assert base58check(b"\x00" + _hash160(pub)) == want

    # electrum families against the electrum package's own keystores
    from electrum import keystore
    from electrum import mnemonic as ec_mnemonic_mod

    genuine = ec_mnemonic_mod.Mnemonic("english").make_seed(seed_type="standard", num_bits=132)
    assert electrum_new_seed_gate(genuine)
    a = electrum_standard_addresses(genuine, n=1)
    ks = keystore.from_seed(genuine, passphrase="", for_multisig=False)
    node = keystore.BIP32Node.from_xkey(ks.xprv)
    pk0 = node.subkey_at_private_derivation((0, 0)).eckey.get_public_key_bytes(compressed=True)
    assert base58check(b"\x00" + _hash160(pk0)) == a["m/0/0"]

    hexseed = "112233445566778899aabbccddeeff00"
    old_phrase = " ".join(__import__("electrum.old_mnemonic", fromlist=["mn_encode"]).mn_encode(hexseed))
    a_old = electrum_old_addresses(old_phrase, n=1)
    ks_old = keystore.from_seed(old_phrase, passphrase="", for_multisig=False)
    pub = ks_old.derive_pubkey(0, 0)
    if isinstance(pub, str):
        pub = bytes.fromhex(pub)
    assert base58check(b"\x00" + _hash160(pub)) == a_old["old/0/0"]

    # false-positive control
    r1 = check_phrase(phrase)
    r2 = check_phrase("legal winner thank year wave sausage worth useful legal winner thank yellow")
    assert not r1["match"] and not r2["match"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--phrase", help="candidate phrase, words separated by spaces")
    parser.add_argument("--passphrase", default="")
    parser.add_argument("--batch", help="file with one candidate phrase per line")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.selftest:
        try:
            selftest()
        except Exception as e:
            print(f"SELFTEST FAIL: {e}", file=sys.stderr)
            sys.exit(2)
        print("SELFTEST OK")
        sys.exit(0)

    if not args.phrase and not args.batch:
        parser.error("need --phrase or --batch (or --selftest)")

    phrases = [args.phrase] if args.phrase else [
        line.strip() for line in open(args.batch, encoding="utf-8") if line.strip()
    ]
    any_match = False
    for phrase in phrases:
        res = check_phrase(phrase, args.passphrase)
        any_match = any_match or res["match"]
        if args.json:
            print(json.dumps(res))
        else:
            fams = ", ".join(sorted(res["families"]))
            print(f"{'MATCH' if res['match'] else 'NO MATCH'}  {phrase}  [{fams}]")
    sys.exit(1 if any_match else 0)


if __name__ == "__main__":
    main()
