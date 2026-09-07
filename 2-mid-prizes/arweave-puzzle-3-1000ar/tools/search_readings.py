#!/usr/bin/env python3
"""Bounded offline eight-slot search with original-page planted controls.

Input is a local JSON document with hypothesis, sources and eight lists in slots.
Candidate text and decrypted wallet material are never printed.
"""
import argparse
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time

import oracle as o

HERE = Path(__file__).resolve().parent


def fixture(page, candidate):
    request = dict(ciphertext=o.PZL8_CIPHERTEXT_B64, answer=o.PZL8_ANSWER,
                   target=o.PZL8_ADDRESS, witness=candidate)
    result = subprocess.run(['node', str(HERE/'original_page_fixture.js'), str(page)],
                            input=json.dumps(request), text=True, capture_output=True,
                            timeout=30)
    if result.returncode:
        raise RuntimeError('Original-page fixture failed')
    result = json.loads(result.stdout)
    assert result['roundtrip_ok'] and result['address'] == o.PZL8_ADDRESS
    return result['ciphertext']


def save_match(candidate, output):
    output = output.resolve()
    if any((p/'.git').exists() for p in [output, *output.parents]):
        raise RuntimeError('Private output must be outside a repository')
    output.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(output, 0o700)
    wallet = json.loads(o.decode_wallet(o.CIPHERTEXT_B64, candidate))
    assert o.jwk_to_address(wallet['n']) == o.ESCROW
    fd = os.open(output/'matched-wallet.json', os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as stream:
        json.dump({'answer': candidate, 'wallet': wallet}, stream)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--readings', type=Path, required=True)
    ap.add_argument('--page', type=Path, required=True)
    ap.add_argument('--log', type=Path, required=True)
    ap.add_argument('--private-output', type=Path, required=True)
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--allow-short-slots', action='store_true',
                    help='Allow 1-4 characters per slot; empty DOM cells contribute no padding')
    args = ap.parse_args()
    assert o.selftest()
    doc = json.loads(args.readings.read_text())
    slots = doc['slots']
    assert len(slots) == 8 and all(slot for slot in slots)
    minimum = 1 if args.allow_short_slots else 4
    assert all(isinstance(s, str) and minimum <= len(s) <= 4 and s.isascii()
               for slot in slots for s in slot)
    count = 1
    for slot in slots:
        count *= len(slot)
    assert count <= 10000, 'Find a tighter constraint'
    candidates = list(dict.fromkeys(''.join(parts).lower() for parts in itertools.product(*slots)))
    witness = random.Random(20260905).choice(candidates)
    cipher = fixture(args.page, witness)
    start = time.monotonic()
    for _ in range(3):
        assert o.check(witness, ciphertext_b64=cipher, target=o.PZL8_ADDRESS) == (True, o.PZL8_ADDRESS)
        assert o.check(witness, ciphertext_b64=cipher, target=o.ESCROW) == (False, o.PZL8_ADDRESS)
    rate = 3/(time.monotonic()-start)
    midpoint = len(candidates)//2
    stream = [witness] + candidates[:midpoint] + [witness] + candidates[midpoint:] + [witness]
    expected = [i for i, c in enumerate(stream) if c == witness]
    report = dict(hypothesis=doc['hypothesis'], sources=doc['sources'],
                  allow_short_slots=args.allow_short_slots,
                  candidate_lengths=sorted(set(map(len, candidates))),
                  slot_counts=[len(s) for s in slots], unique_candidates=len(candidates),
                  stream_count=len(stream), rng_seed=20260905, target=o.ESCROW,
                  witness_positions_expected=expected, measured_candidates_per_second=rate,
                  estimated_seconds=len(stream)/rate, python=sys.version.split()[0],
                  status='planned', input_sha256=hashlib.sha256(args.readings.read_bytes()).hexdigest(),
                  page_sha256=hashlib.sha256(args.page.read_bytes()).hexdigest(),
                  oracle_sha256=hashlib.sha256((HERE/'oracle.py').read_bytes()).hexdigest(),
                  runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.log.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)
    if args.plan:
        return
    assert report['estimated_seconds'] < 570, 'Run exceeds bounded budget'
    start = time.monotonic()
    seen = []
    processed = 0
    for i, candidate in enumerate(stream):
        if time.monotonic()-start > 590:
            report['status'] = 'incomplete-time-limit'
            break
        match, address = o.check(candidate)
        if match:
            save_match(candidate, args.private_output)
            report.update(status='MATCH', address=address)
            break
        hit, _ = o.check(candidate, ciphertext_b64=cipher, target=o.PZL8_ADDRESS)
        if hit:
            seen.append(i)
        processed += 1
        if processed % 50 == 0:
            print(json.dumps(dict(processed=processed, total=len(stream),
                                  elapsed_seconds=round(time.monotonic()-start, 2))), flush=True)
    else:
        assert seen == expected
        report['status'] = 'exhausted-no-match'
    report.update(processed=processed, witness_positions_found=seen,
                  runtime_seconds=time.monotonic()-start)
    args.log.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('RUN FAILED: '+type(error).__name__+'; private output suppressed', file=sys.stderr)
        raise SystemExit(2)
