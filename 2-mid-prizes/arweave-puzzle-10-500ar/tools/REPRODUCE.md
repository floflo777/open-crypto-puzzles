# Reproduce the bounded Genesis 28 checks

Run from the repository root. Python 3.13.3 and Node v25.9.0 were used.
The puzzle oracle, generator and acquisition script use only Python's standard library.
The separate Bitcoin toolchain check needs bip-utils==2.12.2; the root requirements.lock
records the complete environment for this run.

Acquire public source inputs before running any derivation. Keep the input directory
outside the checkout so chapter text and the complete puzzle page cannot be committed.
The following example uses a sibling directory:

```
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/fetch_genesis28_inputs.py ../arweave10-inputs
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/toolchain_selftest.py
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/oracle.py --selftest
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/test_oracle.py
```

The fetcher prints input hashes. Compare them with the recorded result before treating
another run as reproduction of the same source. The original page is required to match
its recorded SHA256 exactly. The two chapter JSON files have these SHA256 values:

- KJV: `903a4a6b413653c54f311a7931c39c1b922c47ce61c2d1c16f0d3e5a62fd1675`
- WEB: `e7bd5d7a6336c95e8d03399e090ba19785d7feb8039940e3a4d6a430c9b980ea`

Now run locally with network access disabled. These commands do not make network calls:

```
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/selftest.json --private-output ../arweave10-private --selftest
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H1.json --private-output ../arweave10-private --hypothesis H1 --plan
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H1.json --private-output ../arweave10-private --hypothesis H1
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H2.json --private-output ../arweave10-private --hypothesis H2 --plan
.venv/bin/python 2-mid-prizes/arweave-puzzle-10-500ar/tools/search_genesis28.py --data-dir ../arweave10-inputs --log ../arweave10-inputs/H2.json --private-output ../arweave10-private --hypothesis H2
```

Each run certifies the oracle, measures the same two-check pipeline with a public solved
vector, prints N, D and N/D, and rejects an estimate above 570 seconds. It stops an actual
run at 590 seconds as incomplete. No negative is recorded unless the complete stream and
all expected witnesses are recovered. Candidate text is never logged.

A deterministic RNG (seed 20260905) chooses one actual candidate for an independently
encrypted fixture. The original page's CryptoJS implementation encrypts the already-solved
#8 wallet with that candidate and a fixed test salt. Every stream item goes through the
same Python check() twice: once for the real target, once for this fixture. Repeating the
fixture candidate at the beginning, middle and end certifies traversal; its original
occurrence must also match. This tests the real input shape without a witness bypass.

Only an exact address match saves an answer and keyfile, in the separate private directory
with directory mode 700 and file mode 600. The script does not construct transactions.
A real match still needs an independent private-key consistency check and a fresh public
address funding check before human handoff. These runs have not produced such a match.

Sources for the separate Bitcoin test vectors:
https://github.com/satoshilabs/slips/blob/master/slip-0132.md and
https://github.com/bitcoin/bips/blob/master/bip-0086.mediawiki.
