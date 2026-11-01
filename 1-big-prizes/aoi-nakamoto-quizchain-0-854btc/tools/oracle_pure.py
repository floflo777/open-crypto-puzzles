#!/usr/bin/env python3
"""
Pure-Python Aoi Nakamoto oracle — no bip_utils, no native deps.

Pipeline (per repo spec):
  candidate text → MD5(UTF-8 bytes) → 128-bit entropy → BIP39 mnemonic
  → PBKDF2-HMAC-SHA512 seed → BIP32 master → BIP44 m/44'/0'/0'/0/i
  → P2PKH address

Verified against author's calibration vector:
  entropy 2941774a2abec9f30c7d6777d1d53d91 → WIF L5Z66qPm… at index 1 ✓
"""
import hmac, hashlib, base58, sys
from mnemonic import Mnemonic
from ecdsa import SigningKey, SECP256k1

# --- BIP39 ---
MNEMO = Mnemonic('english')

def md5_bytes(text: str) -> bytes:
    return hashlib.md5(text.encode('utf-8')).digest()

def mnemonic_from_entropy(entropy: bytes) -> str:
    return MNEMO.to_mnemonic(entropy)

def seed_from_mnemonic(phrase: str, passphrase: str = '') -> bytes:
    return MNEMO.to_seed(phrase, passphrase=passphrase)

# --- BIP32 (pure stdlib + ecdsa) ---
N = SECP256k1.order

def _hmac_sha512(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha512).digest()

def bip32_master(seed: bytes):
    I = _hmac_sha512(b'Bitcoin seed', seed)
    priv = int.from_bytes(I[:32], 'big') % N
    chain = I[32:]
    return priv, chain

def _hardened_child(priv, chain, idx):
    data = b'\x00' + priv.to_bytes(32, 'big') + idx.to_bytes(4, 'big')
    I = _hmac_sha512(chain, data)
    child_priv = (priv + int.from_bytes(I[:32], 'big')) % N
    child_chain = I[32:]
    return child_priv, child_chain

def _nonhardened_child(priv, chain, idx):
    sk = SigningKey.from_secret_exponent(priv, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pub = (b'\x02' if (vk.pubkey.point.y() % 2 == 0) else b'\x03') + vk.pubkey.point.x().to_bytes(32, 'big')
    data = pub + idx.to_bytes(4, 'big')
    I = _hmac_sha512(chain, data)
    child_priv = (priv + int.from_bytes(I[:32], 'big')) % N
    child_chain = I[32:]
    return child_priv, child_chain

def bip44_address(seed: bytes, account: int = 0, change: int = 0, idx: int = 0) -> tuple[str, str]:
    """Derive P2PKH address at m/44'/0'/account'/change/idx."""
    priv, chain = bip32_master(seed)
    for level in (0x8000002c, 0x80000000, 0x80000000 | account):
        priv, chain = _hardened_child(priv, chain, level)
    priv, chain = _nonhardened_child(priv, chain, change)
    priv, chain = _nonhardened_child(priv, chain, idx)
    wif = base58.b58encode_check(b'\x80' + priv.to_bytes(32, 'big') + b'\x01').decode()
    sk = SigningKey.from_secret_exponent(priv, curve=SECP256k1)
    vk = sk.get_verifying_key()
    pub = (b'\x02' if (vk.pubkey.point.y() % 2 == 0) else b'\x03') + vk.pubkey.point.x().to_bytes(32, 'big')
    h160 = hashlib.new('ripemd160', hashlib.sha256(pub).digest()).digest()
    addr = base58.b58encode_check(b'\x00' + h160).decode()
    return addr, wif

def check_text(text: str, escrows: list[str]) -> tuple[bool, str | None, str | None]:
    """Check a candidate text against escrow addresses. Returns (hit, addr, wif)."""
    entropy = md5_bytes(text)
    phrase = mnemonic_from_entropy(entropy)
    seed = seed_from_mnemonic(phrase)
    for i in range(6):
        addr, wif = bip44_address(seed, idx=i)
        if addr in escrows:
            return True, addr, wif
    return False, None, None

def selftest():
    """Run calibration vector and BIP39 test vector."""
    print("=== Selftest ===")

    # Calibration vector (author's published test)
    entropy = bytes.fromhex("2941774a2abec9f30c7d6777d1d53d91")
    phrase = mnemonic_from_entropy(entropy)
    seed = seed_from_mnemonic(phrase)
    _, wif1 = bip44_address(seed, idx=1)
    expected_wif = "L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex"
    print(f"Calibration WIF index 1: {wif1}")
    print(f"Expected:               {expected_wif}")
    print(f"Calibration pass: {wif1 == expected_wif}")
    assert wif1 == expected_wif, "CALIBRATION FAILED"

    # BIP39 test vector 1
    phrase2 = MNEMO.to_mnemonic(bytes(16))
    assert phrase2 == "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about", "BIP39 test failed"
    print("BIP39 test vector 1 pass")

    # BIP32 test vector 1 (master)
    I = _hmac_sha512(b'Bitcoin seed', bytes.fromhex('000102030405060708090a0b0c0d0e0f'))
    assert I[:32].hex() == "e8f32e723decf4051aefac8e2c93c9c5b214313817cdb01a1494b917c8436b35", "BIP32 HMAC failed"
    print("BIP32 test vector 1 pass")

    print("All selftests passed ✓")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--selftest':
        selftest()
    elif len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
        hit, addr, wif = check_text(text, ["14zMkTgaVXJcxdh4JdWi29MLRR44iUSG9W", "13Cv6SXUnzGDT8JHqzzJ8xMPtsSdhJA4wd"])
        print(f"Hit: {hit}, addr={addr}, wif={wif}")
    else:
        print("Usage: oracle_pure.py [--selftest] | <candidate text>")
