# Author posts and quotes

The puzzle's author posts as "Jrk Bgrt" (handle `@SoWut`) inside a puzzle-specific
Telegram group; the group is not indexed at a stable public URL, so this file does
not quote it. What follows is the material that is verifiable at a public URL.

## GSMG.io, platform site

https://www.gsmg.io/

The platform presents itself as an automated crypto-trading service. The puzzle is
a separate, unpaid challenge hosted on the same domain; the escrow address was
first funded on 2019-04-13.

## bitcointalk topic 5532424, "Need help Puzzle GSMG.IO 5BTC"

https://bitcointalk.org/index.php?topic=5532424.0

Community discussion thread, active since 2025-02-18, including several solvers'
notes on the stage chain. Used here only to corroborate the public stage order, not
quoted directly.

## Reddit, r/bitcoinpuzzles

https://www.reddit.com/r/bitcoinpuzzles/comments/bf7siz/gsmgio_5_btc_puzzle_challenge/

https://www.reddit.com/r/bitcoinpuzzles/comments/dfwcqk/gsmgio_5_btc_puzzle/

Two community discussion threads, also linked from the community repository below.

## Community repository

https://github.com/puzzlehunt/gsmgio-5btc-puzzle

A community-maintained repository documenting the solved stages, referenced here
for the public stage-chain order (see `data/stage-chain.json`). Not mirrored in
this folder; consult it directly for the community's own write-ups.

## The puzzle's own published page content

The final page (reached after "the Architect Choice" stage) publishes its content
directly in the page body: a sequence of 1075 single-character tokens, an
image, and a base64-encoded block. This folder quotes only the two short strings
that are the deterministic decoding of that published content, not an
interpretation: `matrixsumlist` and `ourfirsthintisyourlastcommand` (see
"What is understood / Mechanism" in the README for how each is decoded). The
128-character base64 blob is reproduced in `tools/oracle.py` because it is itself
the object the final gate is built on.
