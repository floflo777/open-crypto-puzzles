# Reproduce the #3 oracle audit and finite reading searches

Run from the repository root with Python 3.13.3 and Node v25.9.0. The new checker,
fixture helper and search runner use standard libraries only; the workspace's
`requirements.lock` pins the shared environment.

Obtain the author's original HTML page from
https://arweave.net/VLJIGuTJewofKx8ad4JYQs93nEuGnkgjrIt_Sd2QPYw
and save it outside the repository. Expected SHA256:
`e22da5925990914204fb9b3c5b18e7ac510fc260be568ddbb256762f3c7181bc`.
The helper enforces this hash and executes only the embedded cryptographic script
inside a Node VM with no network facilities, not the page's analytics scripts.

## Regression checks

```sh
.venv/bin/python 2-mid-prizes/arweave-puzzle-3-1000ar/tools/oracle.py --selftest
ARWEAVE3_SOURCE=../run-2026-09-05/all-puzzles-review/ar3-page.txt .venv/bin/python 2-mid-prizes/arweave-puzzle-3-1000ar/tools/test_oracle.py
```

All three tests passed with `ARWEAVE3_SOURCE` present. Without that environment variable,
the two original-page tests are skipped; such a run is not the full audit.

## H1 exact local invocation

```sh
.venv/bin/python 2-mid-prizes/arweave-puzzle-3-1000ar/tools/search_readings.py --readings ../run-2026-09-05/arweave3/h1-readings.json --page ../run-2026-09-05/all-puzzles-review/ar3-page.txt --log ../run-2026-09-05/arweave3/h1-result.json --private-output ../run-2026-09-05/arweave3/private
```

The readings document contains `hypothesis`, `sources`, and eight arrays under `slots`.
Each element is four ASCII characters. Concatenate, lowercase, deduplicate while
preserving order. H1 pool sizes are `[1,4,1,2,4,2,3,2]`. The exact local input has SHA256
`c2e85f8370913b800bbe2b449934a743203ff176629401b1e6a2196b9edf8dda`.
The input stays outside Git with permissions 600, and candidate strings are suppressed
from logs. Consequently, a fresh public checkout alone cannot reconstruct this exact
search: it needs the recorded local readings file. The oracle tests are independently
reproducible without that file.

The runner first checks the solved sibling, creates an original-JavaScript fixture,
measures the two-check loop and records N, rate and estimated runtime before searching.
It refuses estimates over 570 seconds and ends incomplete after 590 seconds. A planned
or incomplete report is not an exhausted negative.

[Recorded H1 output](../analysis/h1-result.json): 384 unique candidates, 387 stream
elements, four expected and observed fixture hits, zero target matches, 225.966 seconds.
No seed, candidate string, wallet key or decrypted JSON is included in that report.

## Public source snapshots

- Community Discord: `https://raw.githubusercontent.com/HomelessPhD/AR_Puzzles/main/PZL3/EXTRA_materials/ARweave_Discord.txt`;
  SHA256 `5da120305ce1a5f7e6402b105d1e95d8bb5dc6647c9fd7f1c110e2bd79503eba`.
- Author tweet workbook: `https://raw.githubusercontent.com/HomelessPhD/AR_Puzzles/main/ArweaveP_user_tweets.xlsx`;
  SHA256 `d60658b4f1e292a47d6c43a9c927fc80c4211af5f809244d4aff47ad9fbdaab0`.
- Reply-parent checks: `https://api.fxtwitter.com/status/<tweet_id>`;
  inspect `tweet.replying_to_status` and follow the referenced original tweet.

No transcripts, workbook copies or sourced wordlists are shipped in the repository.

## H2-H4

Use the same command with `h2`, `h3` or `h4` in place of `h1` in all file names.
Add `--allow-short-slots` for H2 only; it permits one through four ASCII characters
per reading. Candidate lengths and slot sizes are recorded in each report.
The default still requires exactly four characters in every slot.

The reports retain the SHA256 of the exact local inputs and executed runner.
Only local source-note labels were omitted from the published H3/H4 `sources`
arrays; numerical results and input fingerprints are unchanged. No full candidate
strings or decrypted wallet material are published.
