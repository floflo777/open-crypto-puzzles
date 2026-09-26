# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row.
Every sweep below used a witness protocol: candidate lists known in advance to
belong to the swept set (one per corner of the search space, so no quarter of
the space could be silently skipped) were added to the target set before the
run, and their addresses had to be recovered for the negative to count.

## P1 -- full words from the 5 planted sentences (2026-08-15)

Set: full words from the 5 planted sentences only, 6-words-from-video /
6-words-from-post partition, anchors `dutch` at position 1, `parrot` at the
last position, position 5 in {`fog`, `cloud`}, both possible positions of
`fork`, free order otherwise.

2,413,152,000 candidate lists enumerated, 150,822,000 passing the BIP39
checksum (6.25%, matching the expected 1-in-16 rate), derived and compared on
a rented 43-core server. Witness: 4 planted candidates, one per corner of the
space (both `fog`/`cloud` branches crossed with both `fork` positions), all 4
recovered. Rate: 11,807 derivations/second sustained across 40 processes.
Cost: $0.56. Result: 0 match.

## G1 -- same words, `fork` not required as a literal match (2026-08-15)

Set: the P1 word pool without treating `fork` as a required literal word (a
paraphrase reading), 3,500 candidate subsets, 79,391,851 derivations, run on
one rented GPU. Witness: 4 planted candidates, one per corner, all 4
recovered. Rate: 654,436 derivations/second. Duration: 121 seconds. Result: 0
match. This closes the paraphrase reading of `fork` under these anchors: since
`fork` is spoken and spelled letter by letter in the source video, a literal
match is the better-supported reading regardless.

## R1 -- word pool extended with page and video metadata (2026-08-15)

Set: the 5-sentence word pool plus metadata words recovered from the blog
post's own tags (`season`, `market`, `fork`, `round`, from the archived 2020
HTML footer "Tagged... ethereum fork, round") and from the challenge video's
title and hook line ("top", "update", "winter", "finish"), 6/6 partition,
anchors as above, `fork` required, both `fog`/`cloud` branches. 158,670
candidate subsets, 3,384,362,972 derivations, one rented GPU. Witness: 6
planted candidates, all 6 recovered. Rate: 648,936 derivations/second.
Duration: 87 minutes. Result: 0 match.

## R2 minus R1 -- same pools, the 6/6 partition constraint dropped (2026-08-15)

Set: R1's word pools without the 6-words-per-source partition, restricted to
the candidate subsets not already covered by R1 (54,030 of R2's 193,800
total). 1,225,433,776 derivations. Witness: 6 planted candidates, all 6
recovered. Rate: 757,684 derivations/second. Duration: 27 minutes. Result: 0
match. Combined with R1, this makes the full R2 set (metadata-extended pool,
`fork` required, any split between the 2 sources) entirely negative.

## S1 -- blog contributes exactly A1 plus A2, wide video-side pool (2026-08-15)

Set: the post side fixed to exactly the 6 words of sentences A1 and A2 plus
`fiber` (the reading that the post alone supplies exactly 6 words), the video
side drawn from a pool of 56 candidate words (sentences, metadata, natural
inflections, and template text), `parrot` and `fork` anchored, both
`fog`/`cloud` branches. 51,039 candidate subsets, 1,157,541,475 derivations.
Witness: 6 planted candidates, all 6 recovered. Rate: 758,383
derivations/second. Duration: 25 minutes. Result: 0 match.

## R1b -- R1 extended with natural word inflections (2026-08-15)

Set: R1's word pool plus grammatical inflections of already-included words
(for example "hunt" and "health" alongside "hunter" and "healthy"), 6/6
partition, `fork` on the post side, same anchors. 490,776 candidate subsets,
10,752,000,393 derivations, one rented GPU (shared part of the time with
another job). Witness: 6 planted candidates, all 6 recovered. Rate: 668,827
derivations/second. Duration: 4 hours 28 minutes. Result: 0 match.

## Cumulative, metadata-extended era (G1 through R1b, plus P1)

16,749,552,467 candidate derivations across the 6 sweeps above, all negative,
every sweep individually witnessed. This covers: the 5 planted sentences'
words, confirmed metadata words from the blog post's tags and the video's
title and hook line, natural grammatical inflections of those words, both
partition and no-partition readings of the 6-and-6 split, and every free
ordering under the confirmed anchors. It does not cover connecting words
(prepositions, articles), substrings of longer words, or metadata beyond the
tags, title and hook line already identified.

## RO1 -- the complete reading-order model over the full recovered 2020 text (2026-08-20)

Contributed. This is the first sweep to define its space by a closed form and
then enumerate exactly that count, so the coverage claim is checkable rather
than asserted.

Hypothesis: all 12 elements are whole words appearing in the recovered 2020
written surfaces, 6 from the video side and 6 from the post side, and the
elements keep the order in which they are written. The 3 anchors are fixed as
already established: `dutch` at position 1, `fog` at position 5, `parrot` at
position 12. `fork` appears only in the post's tag "ethereum fork", which has
no position in running prose, so it is given a free slot among the post's 6.

Word pool, built from the archived 2020 text and its metadata, not from the 5
planted sentences alone: 39 dictionary words on the video side, 83 on the post
side, 106 distinct across both.

Space, closed form. All counts are exact integers, no rounding:

```
video word sets   = C(25,2)*C(2,2) + C(25,3)*C(2,1) = 300 + 4,600 = 4,900
templates         = C(3,2)*C(6,2) = 45  for the (2 before fog, 2 after) shape
                    C(3,3)*C(6,1) = 6   for the (3 before fog, 1 after) shape
video pairs       = 300*45 + 4,600*6 = 13,500 + 27,600 = 41,100
post word sets    = C(18,3) = 816
fork slot choices = 5
arrangements      = 41,100 * 816 * 5 = 167,688,000
checksum-valid    = 10,484,919
```

Method: enumerate all 167,688,000 arrangements in 3,264 units, filter by the
BIP39 checksum in stdlib, derive every survivor at `m/44'/60'/0'/0/0` and
compare against the escrow address.

Script: `tools/sweep_reading_order.py`, which re-enumerates the identical space
in 816 larger units (1 per post word set) without the novelty banding the
original run used to order its units. `--size` prints the closed form and
checks that the layout enumeration reproduces it. `--selftest` verifies the
wordlist digest, measures the checksum acceptance rate on a real unit, and
plants a candidate then requires the pipeline to recover it. Enumeration and
the checksum filter are stdlib, so both of those run without `bip_utils`;
derivation is delegated to `tools/oracle.py`. On a hit the phrase is written to
a file and deliberately not printed to the log.

Certification. The enumerated arrangement count equals the closed form to the
unit, in all 7 novelty bands separately and in total. Duplicate arrangements
across units: 0. The observed checksum pass rate is 6.254 percent against a
predicted 6.25 percent, which is the independent check that the enumeration and
the checksum filter agree. A known-answer test was run on the derivation engine
before and after: `abandon` 11 times plus `about` derives
`0x9858EfFD232B4033E47d90003D41EC34EcaEda94`, on both the fast engine and a
separate reference engine, with 0 disagreements between the two over the whole
run. A synthetic witness was planted in each unit that could hold one and
recovered through the identical pipeline: OK 1,062, SKIP 2,202 (units whose
shape admits no witness), NONE 0.

Result: 10,484,919 derivations, **0 match**.

Rate: measured 207 to 497 derivations/second on 2 CPU cores, so about 14 hours
of elapsed time here. The same space is about 13 seconds at the 792,000
derivations/second rate this repository's earlier sweeps were run at. The space
is small; the point of this sweep is that it is now closed and witnessed, not
that it was expensive.

## RO2 -- the same reading-order model extended to substrings (2026-08-20)

Contributed. A bounded probe of lead 2, not a closure of it.

Hypothesis: as RO1, but the pool also admits substrings of longer written words
where the substring is itself a dictionary word.

Space: 9,334,500 arrangements, 582,725 checksum-valid derivations. Same
anchors, same order constraint, same witness protocol.

Result: 0 match.

This does **not** close lead 2. It covers only the substrings already listed in
`analysis/leads.md` under the reading-order constraint. The free-order
substring space named in that lead is about 2.8x10^11 derivations and remains
open.

## What RO1 changes about the remaining space

Reading order was the assumption that made any of this searchable. With it
dropped, the same pool and the same 3 anchors give:

```
C(38,4) = 73,815          free choice of the 4 unplaced video words
C(82,3) = 88,560          free choice of the 3 unplaced post words
9!      = 362,880         free arrangement of the 9 unanchored positions
arrangements   = 73,815 * 88,560 * 362,880 = 2.3722x10^15
checksum-valid = 1.4826x10^14
```

At 792,000 derivations/second that is 5.9 years on one GPU. At 12,600
derivations/second, the rate 64 rented CPU cores would give, it is 373 years.
Both figures are quoted so that nobody prices this the way an earlier private
estimate did, which put the same space at 9.1x10^9 arrangements and concluded
that a weekend of rented CPU would cover it. That estimate was low by a factor
of about 2.6x10^5.

The consequence for this folder's ranking: the 2 open sweep leads, liaisons and
substrings, are together about 0.2 percent of the free-order space. They are
worth running because they are cheap, not because covering them would leave
much behind. If the phrase is not in them, no amount of rented compute reaches
the rest. What remains after them is a reading problem, so the leads have been
re-ordered to put reading first.

One sharper result from inside the reading-order model, offered as evidence
rather than as a conclusion. With `fog` at 5 and `parrot` at 12 and order
preserved, the 4 free video words must split k of them before `fog` and m of
them between `fog` and `parrot`, with k+m=4 and k at most 3. Only 2 dictionary
words lie between `fog` and `parrot` in the video text, `lake` and `also`, so m
is at most 2, which forces (k,m) to be (2,2) or (3,1) and therefore forces at
least one of `lake` or `also` into the phrase. RO1 covers 100 percent of that
space and is negative. So either the pool is incomplete on the video side, or
order is not preserved. Those are the only 2 options left inside this model,
and lead 1 is the cheaper of the 2 to test.

## Earlier, smaller sweeps (pre-metadata, dates not individually re-timestamped
in the source record, all prior to 2026-08-15)

- Text reading order (in-source order, contiguous halves, on a strict then a
  widened word pool): 99,335 lists across 36 reading paths. Result: 0 match.
- Every interleaving of the 2 source word sets on the strict pool: 5.4 million
  candidates, only 3 possible reading paths tested. Result: 0 match.
- All 5 candidate word sets with every internal ordering allowed: tested,
  result 0 match, count not separately recorded.
- A posteriori likelihood-ordered search: started, interrupted before
  completion (not a negative, an abandoned run).
- Closing the 6-plus-6 budget by a likelihood-ratio rule, 4 candidate sets:
  91,865 lists, 0 match. This method's 2 strongest supporting words
  ("whisper", "impose") were later found to come from an unconfirmed prefix
  rule, not a validated one, so this negative's supporting logic is weaker
  than it looked at the time.
- A uniformity test of whether the hint words are unusually common in the
  BIP39 dictionary: statistical power 0.023, too low to support any
  conclusion.
- A test for planted list words hidden in the ordinary, non-absurd prose of
  the 2 texts: z = +0.52, p = 0.34, no signal detected.

## What none of this has tested

1. Text shown on screen in the challenge video. The author names this as a
   channel in his own spoken rules for the challenge, at 5:22 to 5:38 of
   .../w4mpiuBP_aY: the words "could be you know written in the video on the
   screen so read carefully". Every sweep in this file, including RO1 and RO2,
   draws its pool from the description, title, tags and post body only. No
   frame of the video image has been read. This is the largest untested channel
   and it is not a sweep, it is a reading task.

2. Free ordering over the full recovered pool. Sized above at 1.4826x10^14
   derivations. Open and not purchasable.

3. Substrings under free ordering, about 2.8x10^11 derivations. The liaison
   free-order sweep, about 1.9x10^10 derivations, was executed as sweep C1
   below (0 match), so the connecting-words part of this is now closed and only
   the substring part remains.

4. Derivation paths other than `m/44'/60'/0'/0/0`. Every sweep in this file
   uses the MetaMask default first account. The escrow is stated to be a
   MetaMask wallet, so this is the right first guess, but a phrase already
   enumerated and rejected at index 0 would also have been rejected at index 1.
   Re-checking the already-enumerated survivors at
   `m/44'/60'/0'/0/1`, `m/44'/60'/0'/0/2`, `m/44'/60'/1'/0/0` and
   `m/44'/60'/2'/0/0` costs about 28 percent of the original derivation work,
   because the seed is already computed and only the child key derivation
   repeats.

5. Material outside the 2 published texts and their metadata.

A correction to what this section used to say. It attributed to the author an
example of a list word hidden inside a longer written word, specifically a word
nested inside its own negation formed with the prefix "im-". Reading the comment
thread directly shows that example was written by the reader asking the
question, not by the author. The author's own example in that reply is "usa" for
"united states", an abbreviation in a hint, and he adds that the challenge text
"wikk have corect word". See `clues/author-posts.md` for both replies in full.
The substring mechanism is still possible; it is just not author-stated, and the
lead resting on it has been demoted accordingly.

## C1 -- pool extended with short connecting words, fog-only, GPU (2026-08-23)

Contributed by salikkhann (PR #13). Executes and closes the connecting-words
lead (README lead 2).

Set: anchors `dutch`/1, `fog`/5 (`cloud` dropped per the R1 sourcing
correction, issue #10), `parrot`/12; `fiber` and `fork` required members on
the post side; 6/6 video/post partition; free words drawn from the full
content-word pools PLUS the short connecting words from the planted
sentences and metadata ("there", "will", "also", "you", "more", "can",
"then", "only", "because", "like"); all 12 words distinct, 9! free orders,
1-in-16 BIP39 checksum filter.

822,640 set-pairs x 9! = 298,519,603,200 lists enumerated; 18,657,475,200
passing the checksum, derived and compared via the repo's own
`engines/bip39_passphrase_engine.cu` (PBKDF2-HMAC-SHA512 -> BIP32
m/44'/60'/0'/0/0 -> keccak256) on a rented Modal L40S. Overlap with the
prior metadata-era sweeps reconstructed at 571.5 million derivations
(3.06%), so roughly 96.9 percent of this space had never been tested.

Rate: 986,965 derivations/second sustained, measured row-fed through the
full sweep path before the run. Witness: per-chunk protocol -- every
2,000-set-pair chunk carried the real escrow plus 2 planted candidates
(first valid row of set-pair 0 and of set-pair 822,639) as simultaneous
targets; a chunk whose planted witnesses were not recovered aborts the run
with exit 3 rather than reporting a negative. The generator was validated
against the folder oracle (40/40 canonical, zero invalid-checksum rejects)
and the engine's known-answer tests before any measurement; the validation
protocol caught and fixed one real generator bug (a wrong 128-of-132-bit
checksum slice) pre-run. Cost: about 11 dollars across three resumable
segments (one segment interrupted by a local network loss and resumed from
its volume checkpoint, repeating only one partial chunk). Result: 0 match
across all 822,640 set-pairs -- 18,657,475,200 derivations.

## RO1 on alternative paths and extra-word variants (issue #18, Bayols, 2026-09-26)

Six sweeps contributed by Bayols in
[issue #18](https://github.com/floflo777/open-crypto-puzzles/issues/18), all no match. Same
anchors and pools as `data/reading-order-pool.json` (dutch at 1, fog at 5, parrot at 12). Every
run passed a self-test first: the canonical `abandon ... about` vector, agreement with
bip_utils, and a planted witness recovered through the real enumeration. The scripts
(`tools/sweep_paths.py`, `tools/sweep_coins.py`, `tools/sweep_postword.py`) import the
enumeration from `tools/sweep_reading_order.py` unchanged; their `--selftest` was re-run
here on 2026-09-26 (all OK, witnesses recovered on every path and every extra word).

| Hypothesis | Space | Method | Result | Witness | Date |
| --- | --- | --- | --- | --- | --- |
| RO1 on 7 paths: `/0/0` to `/0/4`, `1'/0/0`, `2'/0/0` (lead 3) | 167,688,000 arrangements, 10,484,919 checksum-valid, all 7 paths | `sweep_paths.py`, one PBKDF2 per candidate then 7 derivations | 0 match | yes, planted witness on each path | 2026-09-26 |
| RO1 plus one free video-side slot from atom, link, basic, token, dash (lead 1) | 1,741,140,000 arrangements, 108,817,960 valid | `sweep_coins.py`, default path | 0 match | yes | 2026-09-26 |
| RO1 plus one free video-side slot from build, ready | 696,456,000 arrangements, 43,524,282 valid | `sweep_coins.py`, default path | 0 match | yes | 2026-09-26 |
| RO1 plus one free video-side slot from donor, stay, until, win | 1,392,912,000 arrangements, 87,064,878 valid | `sweep_coins.py`, default path | 0 match | yes | 2026-09-26 |
| RO1 plus a free post-side floater "hard" | 125,766,000 arrangements, 7,863,418 valid | `sweep_postword.py`, default path | 0 match | yes | 2026-09-26 |
| RO1 plus a free post-side floater "minimum" | 348,228,000 arrangements, 21,763,738 valid | `sweep_postword.py`, default path | 0 match | yes | 2026-09-26 |

What this rules out: the RO1 space on the alternative derivation paths (lead 3), and the
extra-word variants above at `m/44'/60'/0'/0/0`. What it does not rule out: anything outside
the RO1 reading-order model, checksum-invalid phrases (only valid candidates were derived),
and the other paths for the extra-word sweeps. Speed was about 1,000 derivations per second
per core; the paths sweep took about 13 minutes on 22 workers. The connecting-words lead
(about 1.36e10 derivations) needs a GPU PBKDF2 implementation.
