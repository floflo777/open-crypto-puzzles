#!/usr/bin/env python3
"""
sweep_paths.py -- re-run the RO1 reading-order space on other MetaMask-style
derivation paths (lead 3 in analysis/leads.md).

WHAT IT DOES

Enumerates exactly the same 167,688,000 arrangements as sweep_reading_order.py
(it imports that file's enumeration and checksum filter unchanged), keeps the
10.48 million checksum-valid ones, and for each one computes the BIP39 seed ONCE
(the expensive PBKDF2 step) and then derives several addresses from it:

    m/44'/60'/0'/0/0   control, already negative in RO1
    m/44'/60'/0'/0/1   second account of the same wallet
    m/44'/60'/0'/0/2
    m/44'/60'/0'/0/3   (extra, costs about 1 percent)
    m/44'/60'/0'/0/4   (extra)
    m/44'/60'/1'/0/0   Ledger-Live style second account
    m/44'/60'/2'/0/0

A candidate matches if ANY of these equals the target address.

The BIP32 code here is self-contained (coincurve + pycryptodome keccak) so that
the per-candidate cost is dominated by PBKDF2, and it is checked against
tools/oracle.py (bip_utils) in --selftest before any run.

USAGE

  python tools/sweep_paths.py --selftest --wordlist bip39_english.txt
  python tools/sweep_paths.py --bench    --wordlist bip39_english.txt
  python tools/sweep_paths.py --run --workers 20 --log paths.tsv --wordlist bip39_english.txt
  python tools/sweep_paths.py --run --workers 20 --log paths.tsv --resume ...

Dependencies: coincurve, pycryptodome (both wheels on Windows), plus bip_utils
for --selftest only.
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import itertools
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sweep_reading_order as ro  # noqa: E402

from coincurve import PublicKey  # noqa: E402
from Crypto.Hash import keccak  # noqa: E402

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
H = 0x80000000

# (account, [address indexes]) under m/44'/60'/account'/0/index
PATH_SPECS = [(0, (0, 1, 2, 3, 4)), (1, (0,)), (2, (0,))]
PATH_NAMES = ["m/44'/60'/%d'/0/%d" % (a, i) for a, idxs in PATH_SPECS for i in idxs]

LAST_PATH = [None]


def _i512(key, data):
    return hmac.new(key, data, hashlib.sha512).digest()


def _hard(k, c, i):
    d = _i512(c, b"\x00" + k.to_bytes(32, "big") + (i | H).to_bytes(4, "big"))
    return (int.from_bytes(d[:32], "big") + k) % N, d[32:]


def _pub(k):
    return PublicKey.from_secret(k.to_bytes(32, "big")).format(compressed=True)


def _soft(k, kpub, c, i):
    d = _i512(c, kpub + i.to_bytes(4, "big"))
    return (int.from_bytes(d[:32], "big") + k) % N, d[32:]


def _addr(k):
    raw = PublicKey.from_secret(k.to_bytes(32, "big")).format(compressed=False)[1:]
    return "0x" + keccak.new(digest_bits=256, data=raw).digest()[-20:].hex()


def seed_of(mnemonic):
    return hashlib.pbkdf2_hmac("sha512", " ".join(mnemonic.split()).encode(),
                               b"mnemonic", 2048)


def addresses(mnemonic):
    """Returns [(path_name, address)] for every path in PATH_SPECS."""
    d = _i512(b"Bitcoin seed", seed_of(mnemonic))
    k, c = int.from_bytes(d[:32], "big"), d[32:]
    k, c = _hard(k, c, 44)
    k, c = _hard(k, c, 60)
    out = []
    for account, idxs in PATH_SPECS:
        ka, ca = _hard(k, c, account)
        kc, cc = _soft(ka, _pub(ka), ca, 0)          # change = 0
        kcpub = _pub(kc)
        for i in idxs:
            kl, _ = _soft(kc, kcpub, cc, i)
            out.append(("m/44'/60'/%d'/0/%d" % (account, i), _addr(kl)))
    return out


def make_derive(target):
    def derive(mnemonic):
        for name, a in addresses(mnemonic):
            if a == target:
                LAST_PATH[0] = name
                return target
        return "0x" + "0" * 40
    return derive


# ---------------------------------------------------------------- workers
_W = {}


def _init(wordlist, pool_path):
    words, index_of = ro.load_wordlist(wordlist)
    pre, mid, free, order = ro.load_pool(pool_path)
    _W.update(words=words, index_of=index_of, order=order, free=free,
              lay=ro.build_layouts(), vsets=ro.video_sets(pre, mid, index_of),
              derive=make_derive(ro.TARGET_ADDRESS))


def _work(idx):
    bset = _W["units"][idx] if "units" in _W else list(itertools.combinations(_W["free"], 3))[idx]
    t0 = time.time()
    n, d, hit, _ = ro.scan_unit(bset, None, _W["index_of"], _W["words"], _W["lay"],
                                _W["vsets"], _W["order"], _W["derive"],
                                ro.TARGET_ADDRESS, witness_cap=0)
    return idx, n, d, hit, LAST_PATH[0], time.time() - t0


# ---------------------------------------------------------------- commands
def cmd_selftest(args):
    ok = True
    words, index_of = ro.load_wordlist(args.wordlist)
    vector = " ".join(["abandon"] * 11 + ["about"])
    a0 = dict(addresses(vector))["m/44'/60'/0'/0/0"]
    p = a0 == "0x9858effd232b4033e47d90003d41ec34ecaeda94"
    print("canonical vector at m/44'/60'/0'/0/0: %s" % ("OK" if p else "FAIL"))
    ok &= p

    try:
        from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins, Bip44Changes
        import random
        rnd = random.Random(7)
        bad = 0
        for _ in range(5):
            from mnemonic import Mnemonic
            mn = Mnemonic("english").to_mnemonic(bytes(rnd.getrandbits(8) for _ in range(16)))
            seed = Bip39SeedGenerator(mn).Generate()
            for name, a in addresses(mn):
                parts = name.split("/")
                acc, idx = int(parts[3][:-1]), int(parts[-1])
                ref = (Bip44.FromSeed(seed, Bip44Coins.ETHEREUM).Purpose().Coin()
                       .Account(acc).Change(Bip44Changes.CHAIN_EXT)
                       .AddressIndex(idx).PublicKey().ToAddress()).lower()
                if ref != a:
                    bad += 1
        p = bad == 0
        print("all %d paths agree with bip_utils on 5 random phrases: %s"
              % (len(PATH_NAMES), "OK" if p else "FAIL (%d mismatches)" % bad))
        ok &= p
    except ImportError as exc:
        print("bip_utils not available (%s): cross-check SKIPPED, run is UNCERTIFIED" % exc)
        ok = False

    # planted witness on every path, through the real enumeration
    pre, mid, free, order = ro.load_pool(args.pool)
    lay = ro.build_layouts()
    vsets = ro.video_sets(pre, mid, index_of)
    bset = tuple(free[:3])
    seen = {}

    def grab(mn):
        seen.setdefault("mn", mn)
        return "0x" + "0" * 40
    ro.scan_unit(bset, None, index_of, words, lay, vsets, order, grab,
                 "0x" + "f" * 40, witness_cap=0)
    if "mn" not in seen:
        print("no candidate derived: FAIL")
        return 1
    for name, addr in addresses(seen["mn"]):
        LAST_PATH[0] = None
        n, d, hit, _ = ro.scan_unit(bset, None, index_of, words, lay, vsets, order,
                                    make_derive(addr), addr, witness_cap=0)
        p = hit == seen["mn"] and LAST_PATH[0] == name
        print("planted witness recovered at %-20s %s" % (name, "OK" if p else "FAIL"))
        ok &= p
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def cmd_bench(args):
    words, index_of = ro.load_wordlist(args.wordlist)
    pre, mid, free, order = ro.load_pool(args.pool)
    lay = ro.build_layouts()
    vsets = ro.video_sets(pre, mid, index_of)
    derive = make_derive(ro.TARGET_ADDRESS)
    t0 = time.time()
    cnt = [0]

    def counting(mn):
        cnt[0] += 1
        if cnt[0] > 3000:
            raise StopIteration
        return derive(mn)
    try:
        ro.scan_unit(tuple(free[:3]), None, index_of, words, lay, vsets, order,
                     counting, ro.TARGET_ADDRESS, witness_cap=0)
    except StopIteration:
        pass
    dt = time.time() - t0
    per = cnt[0] / dt
    print("single core: %.0f candidates/s (%d paths each)" % (per, len(PATH_NAMES)))
    total = 10484919
    for w in (1, 8, 16, 20, 24):
        print("  %2d workers -> about %.1f minutes for %s candidates"
              % (w, total / (per * w) / 60, format(total, ",")))
    return 0


def cmd_run(args):
    words, index_of = ro.load_wordlist(args.wordlist)
    pre, mid, free, order = ro.load_pool(args.pool)
    units = list(itertools.combinations(free, 3))
    done = set()
    if args.resume and os.path.exists(args.log):
        for line in open(args.log, encoding="utf-8"):
            c = line.rstrip("\n").split("\t")
            if len(c) > 1 and c[0] != "unit":
                done.add(int(c[0]))
    todo = [i for i in range(len(units)) if i not in done]
    print("%d of %d units to run on %d paths with %d workers"
          % (len(todo), len(units), len(PATH_NAMES), args.workers))
    new = not os.path.exists(args.log)
    log = open(args.log, "a", encoding="utf-8")
    if new:
        log.write("unit\tarrangements\tderivations\tseconds\n")
        log.flush()
    t0 = time.time()
    tn = td = 0
    with mp.Pool(args.workers, initializer=_init,
                 initargs=(args.wordlist, args.pool)) as pool:
        for k, (idx, n, d, hit, path, secs) in enumerate(
                pool.imap_unordered(_work, todo), 1):
            tn += n
            td += d
            log.write("%d\t%d\t%d\t%.1f\n" % (idx, n, d, secs))
            log.flush()
            if hit:
                with open(args.hit, "w", encoding="utf-8") as fh:
                    fh.write(hit + "\n" + str(path) + "\n")
                print("MATCH on %s. Phrase written to %s, deliberately not printed. "
                      "Do not share it; move the funds first." % (path, args.hit))
                pool.terminate()
                return 0
            if k % 10 == 0 or k == len(todo):
                el = time.time() - t0
                print("%d/%d units, %s derivations, %.0f/s, eta %.0f min"
                      % (k, len(todo), format(td, ","), td / el,
                         (len(todo) - k) * el / k / 60))
    print("finished: %s arrangements, %s checksum-valid candidates, %d paths each, "
          "no match" % (format(tn, ","), format(td, ","), len(PATH_NAMES)))
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wordlist", default=os.environ.get("BIP39_WORDLIST", "bip39_english.txt"))
    ap.add_argument("--pool", default=os.path.join(os.path.dirname(HERE), "data",
                                                   "reading-order-pool.json"))
    ap.add_argument("--log", default="sweep_paths.tsv")
    ap.add_argument("--hit", default="hit_paths.txt")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--bench", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return cmd_selftest(a)
    if a.bench:
        return cmd_bench(a)
    if a.run:
        return cmd_run(a)
    ap.print_help()
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
