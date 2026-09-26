#!/usr/bin/env python3
"""
sweep_postword.py -- RO1 with an extra free POST-side word.

Same anchors and same video side as RO1 (4 free video words in reading order,
pool from reading-order-pool.json). Post side: dutch, fiber and fork as in RO1,
but one of the 3 free post words is replaced by a floater from --words, placed
in ANY of the post slots left after fork. The other 2 free post words come from
the pool in reading order, together with fiber.

Prefixes: BIP39 words are unique by their first 4 letters, so --words accepts
a 4-letter prefix and resolves it (mini -> minimum).

USAGE
  python tools/sweep_postword.py --size --words hard
  python tools/sweep_postword.py --selftest --words hard --wordlist bip39_english.txt
  python tools/sweep_postword.py --run --words hard --workers 20 --log hard.tsv --wordlist bip39_english.txt
"""

from __future__ import annotations

import argparse
import itertools
import multiprocessing as mp
import os
import sys
import time
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import sweep_reading_order as ro  # noqa: E402
import sweep_paths as sp  # noqa: E402
import sweep_coins as sc  # noqa: E402

SHIFT, ENT_MASK = ro.SHIFT, ro.ENT_MASK
_W = {}


def resolve(words, wordlist):
    out = []
    for w in [x.strip().lower() for x in words.split(",") if x.strip()]:
        hits = [x for x in wordlist if x.startswith(w[:4])]
        if len(hits) != 1:
            sys.exit("cannot resolve %r to one BIP39 word (%s)" % (w, hits))
        out.append(hits[0])
    return out


def closed_form(n):
    video_pairs = comb(25, 2) * 45 + comb(25, 3) * 2 * 6   # 41,100, as in RO1
    return {"video_pairs": video_pairs, "post_sets": comb(18, 2),
            "arrangements": video_pairs * comb(18, 2) * 5 * 4 * n}


def cmd_size(args):
    n = len(args.words.split(","))
    cf = closed_form(n)
    for k, v in cf.items():
        print("%-14s %s" % (k, format(v, ",")))
    print("expected checksum-valid: about %s" % format(cf["arrangements"] // 16, ","))
    return 0


def scan_unit(bset, extras_i, index_of, words, lay, vsets, order, derive, target):
    ordered3 = [index_of[w] for w in
                sorted(list(bset) + ["fiber"], key=lambda w: order[w])]
    fork_i = index_of["fork"]
    anchor = ((index_of["dutch"] << SHIFT[ro.DUTCH]) + (index_of["fog"] << SHIFT[ro.FOG])
              + (index_of["parrot"] << SHIFT[ro.PARROT]))
    sha = ro.hashlib.sha256
    n = d = 0
    for (k, m), rows in vsets.items():
        for vpos, forks in lay[(k, m)]:
            free_slots = [SHIFT[p] for p in vpos[:k] + vpos[k + 1:-1]]
            for fslot, others in forks:
                for eslot in others:
                    rest = [p for p in others if p != eslot]
                    base0 = anchor + (fork_i << SHIFT[fslot])
                    for w3, p in zip(ordered3, rest):
                        base0 += w3 << SHIFT[p]
                    for ei in extras_i:
                        base = base0 + (ei << SHIFT[eslot])
                        for v in rows:
                            acc = base
                            for wi, sh in zip(v, free_slots):
                                acc += wi << sh
                            n += 1
                            ent = ((acc >> 4) & ENT_MASK).to_bytes(16, "big")
                            if (sha(ent).digest()[0] >> 4) != (acc & 0xF):
                                continue
                            d += 1
                            mn = " ".join(words[(acc >> SHIFT[q]) & 0x7FF] for q in range(12))
                            if derive(mn) == target:
                                return n, d, mn
    return n, d, None


def _setup(wordlist, pool_path, extra):
    words, index_of = ro.load_wordlist(wordlist)
    pre, mid, free, order = ro.load_pool(pool_path)
    ex = resolve(extra, words)
    return dict(words=words, index_of=index_of, order=order, ex=ex,
                free=[w for w in free if w not in ex] if False else free,
                lay=ro.build_layouts(), vsets=ro.video_sets(pre, mid, index_of),
                extras_i=[index_of[w] for w in ex])


def _init(*a):
    _W.update(_setup(*a))
    _W["derive"] = sc.make_derive_default(ro.TARGET_ADDRESS)


def _work(idx):
    bset = list(itertools.combinations(_W["free"], 2))[idx]
    t0 = time.time()
    n, d, hit = scan_unit(bset, _W["extras_i"], _W["index_of"], _W["words"], _W["lay"],
                          _W["vsets"], _W["order"], _W["derive"], ro.TARGET_ADDRESS)
    return idx, n, d, hit, time.time() - t0


def cmd_selftest(args):
    ok = True
    S = _setup(args.wordlist, args.pool, args.words)
    print("extra post words: %s" % S["ex"])
    cf = closed_form(len(S["ex"]))
    bset = tuple(S["free"][:2])
    seen = []

    def grab(mn):
        seen.append(mn)
        return "0x" + "0" * 40
    n, d, _ = scan_unit(bset, S["extras_i"], S["index_of"], S["words"], S["lay"],
                        S["vsets"], S["order"], grab, "0x" + "f" * 40)
    want = cf["arrangements"] // comb(18, 2)
    p = n == want and abs(d / n - 1 / 16) < 0.004
    print("1 unit: %s arrangements (expect %s), %d valid, rate %.4f: %s"
          % (format(n, ","), format(want, ","), d, d / n, "OK" if p else "FAIL"))
    ok &= p
    bad = 0
    for mn in seen[:20000]:
        w = mn.split()
        if not (w[0] == "dutch" and w[4] == "fog" and w[11] == "parrot"):
            bad += 1
        if "fork" not in w or "fiber" not in w or not any(e in w for e in S["ex"]):
            bad += 1
    p = bad == 0
    print("anchors, fork, fiber and the extra word present in 20,000 candidates: %s"
          % ("OK" if p else "FAIL"))
    ok &= p
    p = len(set(seen)) == len(seen)
    print("no duplicates in 1 unit: %s" % ("OK" if p else "FAIL"))
    ok &= p
    for e in S["ex"]:
        mn = next(m for m in seen if e in m.split())
        tgt = sp.addresses(mn)[0][1]
        n2, d2, hit = scan_unit(bset, S["extras_i"], S["index_of"], S["words"], S["lay"],
                                S["vsets"], S["order"], sc.make_derive_default(tgt), tgt)
        p = hit == mn
        print("planted witness containing %-8s recovered: %s" % (e, "OK" if p else "FAIL"))
        ok &= p
    vec = sp.addresses(" ".join(["abandon"] * 11 + ["about"]))[0][1]
    p = vec == "0x9858effd232b4033e47d90003d41ec34ecaeda94"
    print("canonical vector: %s" % ("OK" if p else "FAIL"))
    ok &= p
    print("SELFTEST OK" if ok else "SELFTEST FAILED")
    return 0 if ok else 1


def cmd_run(args):
    S = _setup(args.wordlist, args.pool, args.words)
    units = list(itertools.combinations(S["free"], 2))
    done = set()
    if args.resume and os.path.exists(args.log):
        for line in open(args.log, encoding="utf-8"):
            c = line.rstrip("\n").split("\t")
            if len(c) > 1 and c[0] != "unit":
                done.add(int(c[0]))
    todo = [i for i in range(len(units)) if i not in done]
    print("%d of %d units, extra post words %s, default path, %d workers"
          % (len(todo), len(units), S["ex"], args.workers))
    new = not os.path.exists(args.log)
    log = open(args.log, "a", encoding="utf-8")
    if new:
        log.write("unit\tarrangements\tderivations\tseconds\n")
    t0 = time.time()
    tn = td = 0
    with mp.Pool(args.workers, initializer=_init,
                 initargs=(args.wordlist, args.pool, args.words)) as pool:
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
    ap.add_argument("--words", required=True, help="comma-separated words or 4-letter prefixes")
    ap.add_argument("--log", default="sweep_postword.tsv")
    ap.add_argument("--hit", default="hit_postword.txt")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
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
