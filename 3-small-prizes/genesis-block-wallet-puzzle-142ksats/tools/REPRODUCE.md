# Reproduce the six bounded constructions

Use Python 3.13.3 and the repository `requirements.lock` (bip-utils 2.12.2).
Run from the repository root. These scripts reuse this folder's existing `oracle.py`
and `candidates.py`; T/J, the 214 paths and the 12 genesis integers come from that
existing generator. No new downloaded wordlist or transcript is required.

Set `PUZZLE_RUN_DIR` to a private directory outside this checkout. Copy the dated
[funding.json](../analysis/2026-09-05/funding.json) there for offline reproduction.
This snapshot records the preflight state on 2026-09-05; it is not a current balance
claim. Run the escrow checker again before new research. Output stays in that external
directory with restrictive permissions. These scripts have no network operations.

```sh
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_direct_mnemonic.py
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_numeric_date.py
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_text_constructions.py prefix
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_text_constructions.py path
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_zero_root.py
python 3-small-prizes/genesis-block-wallet-puzzle-142ksats/tools/check_hardening.py
```

The scripts run the existing oracle self-test, calibrate the exact SHA256 pair checker
and inject the public, revealed two-key witness into the actual stream. They reject
estimates above 570 seconds and stop incomplete if the time bound is exceeded.
The checks compare the full 32-byte witness program, not an address prefix.

## Recorded reports

- [Direct mnemonic](../analysis/2026-09-05/direct-mnemonic-result.json).
- [Numeric date](../analysis/2026-09-05/numeric-date-result.json).
- [Date-prefix mnemonic](../analysis/2026-09-05/prefix-result.json).
- [Text in derivation path](../analysis/2026-09-05/path-result.json).
- [Zero root](../analysis/2026-09-05/zero-root-result.json).
- [Hardening combinations](../analysis/2026-09-05/hardening-result.json).
- [Original and portable source hashes](../analysis/2026-09-05/publication.json).

Counts in `ordered_pairs` include cross-pairs with inserted witness-key records.
The ledger separates candidate-only pairs from those stream counts. The prefix and
hardening scripts explicitly omit their defined old-old pairs. These six families
are not asserted to be mutually disjoint. Controls certify the comparison harness;
they do not establish that the root/path interpretation matches the author's intent.
