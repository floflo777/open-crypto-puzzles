"""Replay a private JSON candidate list using the exact-address checker from PR #20."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import random
import sys
import time

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--oracle-dir', type=Path, required=True)
ap.add_argument('--page', type=Path, required=True, help='Original #3 HTML, hash checked by fixture')
ap.add_argument('--candidates', type=Path)
ap.add_argument('--output', type=Path, required=True, help='Private directory outside checkout')
ap.add_argument('--selftest', action='store_true')
args = ap.parse_args()
repo = Path(__file__).resolve().parents[3]
out = args.output.resolve()
if out == repo or repo in out.parents:
    ap.error('--output must be outside the checkout')
os.umask(0o077)
out.mkdir(mode=0o700, parents=True, exist_ok=True)
os.chmod(out, 0o700)
oracle_file = args.oracle_dir / 'oracle.py'
if hashlib.sha256(oracle_file.read_bytes()).hexdigest() != 'ce427963c2fdec08f21e19c1bf764330e375fe76f59e89579d4d70274fddf27a':
    ap.error('Supply the exact-address oracle from PR #20, with its fixture helpers')
sys.path.insert(0, str(args.oracle_dir.resolve()))
import oracle as o
from search_readings import fixture

spec = importlib.util.spec_from_file_location('p12', Path(__file__).with_name('oracle.py'))
p12 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p12)
assert o.selftest()
if args.selftest:
    values = ['public mixed-Case reproduction fixture'.ljust(58, '0')]
else:
    if not args.candidates:
        ap.error('--candidates is required unless --selftest is set')
    values = json.loads(args.candidates.read_text())
    assert isinstance(values, list) and values
    assert all(isinstance(v, str) and len(v) == 58 and v.isascii() for v in values)
    assert len(values) == len(set(values))

control = random.Random(20260905).choice(values)
cipher = fixture(args.page, control)
assert o.check(control, ciphertext_b64=cipher, target=o.PZL8_ADDRESS, lowercase=False)[0]
assert not o.check(control, ciphertext_b64=cipher, target=p12.ESCROW, lowercase=False)[0]
assert not o.check(control+'!', ciphertext_b64=cipher, target=o.PZL8_ADDRESS, lowercase=False)[0]
if args.selftest:
    print('PASS: real solved sibling, exact wrong-target rejection, original JavaScript fixture')
    raise SystemExit
mid = len(values)//2
stream = [control]+values[:mid]+[control]+values[mid:]+[control]
expected = [i for i, v in enumerate(stream) if v == control]
start = time.monotonic()
for _ in range(3):
    o.check(control, ciphertext_b64=p12.CIPHERTEXT_B64, target=p12.ESCROW, lowercase=False)
    assert o.check(control, ciphertext_b64=cipher, target=o.PZL8_ADDRESS, lowercase=False)[0]
rate = 3/(time.monotonic()-start)
report = dict(unique_candidates=len(values), stream_count=len(stream), measured_rate=rate,
              estimated_seconds=len(stream)/rate, target=p12.ESCROW, lowercase=False,
              input_sha256=hashlib.sha256(args.candidates.read_bytes()).hexdigest(),
              witness_positions_expected=expected, status='running')
assert report['estimated_seconds'] < 570
print(json.dumps(report), flush=True)
start = time.monotonic()
seen = []
for i, value in enumerate(stream):
    assert time.monotonic()-start < 590
    if o.check(value, ciphertext_b64=p12.CIPHERTEXT_B64, target=p12.ESCROW, lowercase=False)[0]:
        fd = os.open(out/'matched-wallet.json', os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600)
        with os.fdopen(fd, 'w') as f:
            json.dump({'answer': value, 'wallet': json.loads(o.decode_wallet(p12.CIPHERTEXT_B64, value))}, f)
        report['status'] = 'match'
        break
    if o.check(value, ciphertext_b64=cipher, target=o.PZL8_ADDRESS, lowercase=False)[0]:
        seen.append(i)
else:
    assert seen == expected
    report['status'] = 'exhausted-no-match'
report.update(processed=i+1, witness_positions_found=seen, runtime_seconds=time.monotonic()-start)
(out/'replay-result.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps(report))
