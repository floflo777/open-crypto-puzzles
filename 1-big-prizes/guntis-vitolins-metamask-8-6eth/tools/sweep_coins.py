#!/usr/bin/env python3
"""
sweep_coins.py -- lead 1: RO1 with the on-screen coin words as free video words.

MODEL (RO1 plus one floater)

Same anchors (dutch 1, fog 5, parrot 12), same post side as RO1 (fiber and fork
fixed, 3 more post words in reading order, 5 fork slot choices). On the video
side, RO1 filled the 4 free video slots with 4 pool words in reading order. Here
exactly ONE of those 4 slots holds a coin word from the portfolio table
(atom, link, basic, token, dash: written nowhere, so no reading position) in ANY
of the 4 slots; the other 3 slots hold pool words in reading order. The pool
constraint from RO1 stays: at most 2 pool words come from between fog and parrot.

Derives m/44'/60'/0'/0/0 by default (--all-paths adds the other 6 from
sweep_paths.py). Checksum filter as in RO1.

USAGE
  python tools/sweep_coins.py --size
  python tools/sweep_coins.py --selftest --wordlist bip39_english.txt
  python tools/sweep_coins.py --run --workers 20 --log coins.tsv --wordlist bip39_english.txt [--resume]
"""

from __future__ import annotations

import argparse
import itertools
import json
import multiprocessing as mp
import os
import sys
import time
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sweep_reading_order as ro  # noqa: E402
import sweep_paths as sp  # noqa: E402

SHIFT, ENT_MASK = ro.SHIFT, ro.ENT_MASK
DEFAULT_COINS = ["atom", "link", "basic", "token", "dash"]
LAST = [None]
_W = {}


def load_coins(path, override=None):
    if override:
        return [w.strip() for w in override.split(",") if w.strip()]
    try:
        with open(path, encoding="utf-8") as fh:
            v = json.load(fh)["coin_words_from_the_portfolio_table"]
        if isinstance(v, list) and len(v) == 5:
            return v
    except (OSError, KeyError, ValueError):
        pass
    return DEFAULT_COINS


def video_layouts():
    """(free video slots, coin slot, pre pool slots, mid pool slots)."""
    out = []
    for j in range(0, 4):
        for ps in itertools.combinations(ro.PRE_SLOTS, j):
            for ms in itertools.combinations(ro.MID_SLOTS, 4 - j):
                for coin in ps + ms:
                    pp = tuple(s for s in ps if s != coin)
                    mp_ = tuple(s for s in ms if s != coin)
                    if len(mp_) > 2:
                        continue
                    out.append((ps + ms, coin, pp, mp_))
    return out


def closed_form(ncoins=5):
    v = sum(comb(25, len(pp)) * comb(2, len(mm)) for _, _, pp, mm in video_layouts())
    return {"video_per_coin": v, "video_all_coins": v * ncoins,
            "arrangements": v * ncoins * 816 * 5}


def cmd_size(args):
    cf = closed_form(len(load_coins(args.coins, args.words)))
    for k, v in cf.items():
        print("%-16s %s" % (k, format(v, ",")))
    print("expected checksum-valid derivations: about %s"
          % format(cf["arrangements"] // 16, ","))
    return 0


def build_rows(pre, mid, index_of):
    """Per layout: list of word-index tuples for the 3 pool slots, in slot order."""
    lays = []
    for vpos, coin, pp, mm in video_layouts():
        rows = [tuple(index_of[w] for w in a + b)
                for a in itertools.combinations(pre, len(pp))
                for b in itertools.combinations(mid, len(mm))]
        lays.append((vpos, coin, pp + mm, rows))
    return lays


def make_derive_default(target):
    def derive(mn):
        d = sp._i512(b"Bitcoin seed", sp.seed_of(mn))
        k, c = int.from_bytes(d[:32], "big"), d[32:]
        k, c = sp._hard(k, c, 44)
        k, c = sp._hard(k, c, 60)
        k, c = sp._hard(k, c, 0)
        k, c = sp._soft(k, sp._pub(k), c, 0)
        k, _ = sp._soft(k, sp._pub(k), c, 0)
        a = sp._addr(k)
        if a == target:
            LAST[0] = "m/44'/60'/0'/0/0"
            return target
        return "0x" + "0" * 40
    return derive


def scan_unit(bset, index_of, words, lays, coins_i, order, derive, target):
    ordered4 = [index_of[w] for w in
                sorted(list(bset) + ["fiber"], key=lambda w: order[w])]
    fork_i = index_of["fork"]
    anchor = ((index_of["dutch"] << SHIFT[ro.DUTCH]) + (index_of["fog"] << SHIFT[ro.FOG])
              + (index_of["parrot"] << SHIFT[ro.PARROT]))
    sha = ro.hashlib.sha256
    n = d = 0
    for vpos, coin_slot, pool_slots, rows in lays:
        used = set(vpos) | {ro.DUTCH, ro.FOG, ro.PARROT}
        post = [p for p in range(12) if p not in used]
        sh = [SHIFT[s] for s in pool_slots]
        for fslot in post:
            others = [p for p in post if p != fslot]
            base0 = anchor + (fork_i << SHIFT[fslot])
            for w4, p in zip(ordered4, others):
                base0 += w4 << SHIFT[p]
            for ci in coins_i:
                base = base0 + (ci << SHIFT[coin_slot])
                for v in rows:
                    acc = base
                    for wi, s in zip(v, sh):
                        acc += wi << s
                    n += 1
                    ent = ((acc >> 4) & ENT_MASK).to_bytes(16, "big")
                    if (sha(ent).digest()[0] >> 4) != (acc & 0xF):
                        continue
                    d += 1
                    mn = " ".join(words[(acc >> SHIFT[p]) & 0x7FF] for p in range(12))
                    if derive(mn) == target:
                        return n, d, mn
    return n, d, None


def _setup(wordlist, pool_path, coins_path, allp, extra=None):
    words, index_of = ro.load_wordlist(wordlist)
    pre, mid, free, order = ro.load_pool(pool_path)
    coins = load_coins(coins_path, extra)
    for w in coins:
        if w not in index_of:
            sys.exit("coin word %s not in wordlist" % w)
    return dict(words=words, index_of=index_of, order=order, free=free,
                lays=build_rows(pre, mid, index_of),
                coins_i=[index_of[w] for w in coins], coins=coins,
                mk=(sp.make_derive if allp else make_derive_default))


def _init(*a):
    _W.update(_setup(*a))
    _W["derive"] = _W["mk"](ro.TARGET_ADDRESS)


def _work(idx):
    bset = list(itertools.combinations(_W["free"], 3))[idx]
    t0 = time.time()
    n, d, hit = scan_unit(bset, _W["index_of"], _W["words"], _W["lays"],
                          _W["coins_i"], _W["order"], _W["derive"], ro.TARGET_ADDRESS)
    return idx, n, d, hit, time.time() - t0


def cmd_selftest(args):
    ok = True
    S = _setup(args.wordlist, args.pool, args.coins, False, args.words)
    cf = closed_form(len(S["coins"]))
    p = cf["arrangements"] == 85350 * len(S["coins"]) * 816 * 5
    print("closed form %s arrangements: %s" % (format(cf["arrangements"], ","), "OK" if p else "FAIL"))
    ok &= p
    print("coin words: %s" % S["coins"])
    bset = tuple(S["free"][:3])
    # 1 unit count and checksum rate
    seen = []

    def grab(mn):
        seen.append(mn)
        return "0x" + "0" * 40
    n, d, _ = scan_unit(bset, S["index_of"], S["words"], S["lays"], S["coins_i"],
                        S["order"], grab, "0x" + "f" * 40)
    want = cf["arrangements"] // 816
    p = n == want and abs(d / n - 1 / 16) < 0.004
    print("1 unit: %s arrangements (expect %s), %d checksum-valid, rate %.4f: %s"
          % (format(n, ","), format(want, ","), d, d / n, "OK" if p else "FAIL"))
    ok &= p
    # every candidate has exactly one coin word, anchors in place, no duplicates
    bad = 0
    for mn in seen[:20000]:
        w = mn.split()
        if not (w[0] == "dutch" and w[4] == "fog" and w[11] == "parrot"):
            bad += 1
        if sum(x in S["coins"] for x in w) != 1:
            bad += 1
    p = bad == 0
    print("anchors fixed and exactly one coin word in 20,000 candidates: %s"
          % ("OK" if p else "FAIL"))
    ok &= p
    p = len(set(seen)) == len(seen)
    print("no duplicate candidates in 1 unit: %s" % ("OK" if p else "FAIL"))
    ok &= p
    # planted witness on a candidate holding each coin word
    derive_real = sp.make_derive
    for cw in S["coins"]:
        mn = next(m for m in seen if cw in m.split())
        tgt = sp.addresses(mn)[0][1]
        LAST[0] = None
        n2, d2, hit = scan_unit(bset, S["index_of"], S["words"], S["lays"],
                                S["coins_i"], S["order"], make_derive_default(tgt), tgt)
        p = hit == mn
        print("planted witness containing %-6s recovered: %s" % (cw, "OK" if p else "FAIL"))
        ok &= p
    vector = sp.addresses(" ".join(["abandon"] * 11 + ["about"]))[0][1]
    p = vector == "0x9858effd232b4033e47d90003d41ec34ecaeda94"
    print("canonical vector: %s" % ("OK" if p else "FAIL"))
    ok &= p
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def cmd_run(args):
    S = _setup(args.wordlist, args.pool, args.coins, args.all_paths, args.words)
    units = list(itertools.combinations(S["free"], 3))
    done = set()
    if args.resume and os.path.exists(args.log):
        for line in open(args.log, encoding="utf-8"):
            c = line.rstrip("\n").split("\t")
            if len(c) > 1 and c[0] != "unit":
                done.add(int(c[0]))
    todo = [i for i in range(len(units)) if i not in done]
    print("%d of %d units, coins %s, %s, %d workers"
          % (len(todo), len(units), S["coins"],
             "7 paths" if args.all_paths else "default path", args.workers))
    new = not os.path.exists(args.log)
    log = open(args.log, "a", encoding="utf-8")
    if new:
        log.write("unit\tarrangements\tderivations\tseconds\n")
    t0 = time.time()
    tn = td = 0
    with mp.Pool(args.workers, initializer=_init,
                 initargs=(args.wordlist, args.pool, args.coins, args.all_paths, args.words)) as pool:
        for k, (idx, n, d, hit, secs) in enumerate(pool.imap_unordered(_work, todo), 1):
            tn += n
            td += d
            log.write("%d\t%d\t%d\t%.1f\n" % (idx, n, d, secs))
            log.flush()
            if hit:
                with open(args.hit, "w", encoding="utf-8") as fh:
                    fh.write(hit + "\n")
                print("MATCH. Phrase written to %s, deliberately not printed. "
                      "Do not share it; move the funds first." % args.hit)
                pool.terminate()
                return 0
            if k % 10 == 0 or k == len(todo):
                el = time.time() - t0
                print("%d/%d units, %s derivations, %.0f/s, eta %.0f min"
                      % (k, len(todo), format(td, ","), td / el,
                         (len(todo) - k) * el / k / 60))
    print("finished: %s arrangements, %s checksum-valid candidates, no match"
          % (format(tn, ","), format(td, ",")))
    return 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--wordlist", default=os.environ.get("BIP39_WORDLIST", "bip39_english.txt"))
    ap.add_argument("--pool", default=os.path.join(os.path.dirname(HERE), "data",
                                                   "reading-order-pool.json"))
    ap.add_argument("--coins", default=os.path.join(os.path.dirname(HERE), "data",
                                                    "video-onscreen-words.json"))
    ap.add_argument("--words", default=None,
                    help="comma-separated free video words, replaces the default 5 coin words")
    ap.add_argument("--log", default="sweep_coins.tsv")
    ap.add_argument("--hit", default="hit_coins.txt")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--all-paths", action="store_true")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--size", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    if a.size:
        return cmd_size(a)
    if a.selftest:
        return cmd_selftest(a)
    if a.run:
        return cmd_run(a)
    ap.print_help()
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    sys.exit(main())
