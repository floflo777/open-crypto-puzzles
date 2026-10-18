# Recorded dated-address readings

All three runs finished on 2026-09-05 without an exact target-address match:
[W1](../analysis/2026-09-05/w1-result.json),
[W2](../analysis/2026-09-05/w2-result.json),
[Q1](../analysis/2026-09-05/q1-result.json).
The reports preserve the exact local input fingerprints and original runner hashes.
Only a local source-note label was removed from Q1's published `sources` array.

The exact 58-character candidate lists stay outside Git. A public checkout alone
cannot reconstruct those input files. The ledger describes the bounded constructions
and their sources; this is finite coverage, not elimination of the whole clue family.
The new `replay_readings.py` reproduces the comparison stream from an available private
JSON list, without publishing or regenerating the candidate strings.

## Checker dependency

These runs used the exact-address oracle from
[PR #20](https://github.com/floflo777/open-crypto-puzzles/pull/20), not this folder's
historical RSA-substring checker. Supply the #3 tools directory from that PR using
`--oracle-dir`. The runner checks the oracle SHA256 before import:
`ce427963c2fdec08f21e19c1bf764330e375fe76f59e89579d4d70274fddf27a`.
That directory must also contain `search_readings.py` and `original_page_fixture.js`.
The change is intentionally not duplicated here; both PRs can be reviewed separately.

Use Python 3.13.3 and Node v25.9.0. Obtain the
[original #3 HTML](https://arweave.net/VLJIGuTJewofKx8ad4JYQs93nEuGnkgjrIt_Sd2QPYw)
outside Git. Its SHA256 must be
`e22da5925990914204fb9b3c5b18e7ac510fc260be568ddbb256762f3c7181bc`.
The fixture enforces that hash. The #12 archived page had SHA256
`9c5739094149cc321ea194f22254b7c3ddaa20bbd30ee30cd58dc88096660077`;
its ciphertext matched this folder's constant, and its cryptographic script was
byte-identical to #3's. The archive is linked rather than copied:
[original-page archive](https://github.com/HomelessPhD/AR_Puzzles/blob/main/PZL12/Puzzle_Weave_12.html).

From the repository root, set the following shell variables to your local paths:
`CHECKER_DIR`, `ORIGINAL_PAGE`, `PRIVATE_INPUT`, and `PRIVATE_OUTPUT`.
Output must be outside this checkout. Candidate lists are JSON arrays of unique
58-character ASCII strings, in the original order.

```sh
python 2-mid-prizes/arweave-puzzle-12-400ar/tools/replay_readings.py --oracle-dir "$CHECKER_DIR" --page "$ORIGINAL_PAGE" --output "$PRIVATE_OUTPUT" --selftest
python 2-mid-prizes/arweave-puzzle-12-400ar/tools/replay_readings.py --oracle-dir "$CHECKER_DIR" --page "$ORIGINAL_PAGE" --output "$PRIVATE_OUTPUT" --candidates "$PRIVATE_INPUT"
```

The self-test covers the real solved sibling, wrong-target and mutated-answer rejection,
and a mixed-case original-JavaScript fixture. Full replay measures N/rate before the
loop and inserts the deterministic control at head/middle/tail, plus its natural
occurrence. The output includes counts and positions, never candidate text.
A matching wallet would be written only to the private output directory, mode 600.

[Recorded funding](../analysis/2026-09-05/funding.json): 400.00248121 AR and no outgoing
transactions at 2026-09-05 00:12:55 UTC. Recheck before any new search. The replay tool
is offline; no transactions are constructed, signed or sent.
