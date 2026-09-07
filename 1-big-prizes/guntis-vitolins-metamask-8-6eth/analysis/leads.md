# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the
ranking.

## Why the ranking changed (2026-08-21)

The previous ranking put the 2 pool-extension sweeps first and re-reading the
sources third. Sweep RO1 in `analysis/tested.md` closed the complete
reading-order model over the full recovered 2020 text, 167,688,000
arrangements and 10,484,919 derivations, witnessed, 0 match. That result makes
the sweep leads look smaller than they did:

```
free ordering over the same pool and anchors
  = C(38,4) * C(82,3) * 9!
  = 73,815 * 88,560 * 362,880
  = 2.3722x10^15 arrangements
  = 1.4826x10^14 checksum-valid derivations
  = 5.9 years at 792,000 derivations/second
```

The liaison and substring leads together are about 0.2 percent of that. They
are still worth running, because they are hours rather than years, but they are
no longer plausibly where the answer is hiding. The remaining 99.8 percent is
not purchasable at any budget this challenge justifies. So the binding
constraint is not search, it is word identification, and the first lead below
is now a reading task rather than a sweep.

## 1. Read the text shown on screen in the challenge video

Executed by @cjmcdaniel on 2026-09-04 (issue #18): 720p download, 1 frame per
second (431 frames), OCR of every frame, intersection with the BIP-0039 list,
diff against `data/reading-order-pool.json`. Result: 122 dictionary words are
legible on screen, 109 of them in no written surface of the pool, so the pool
every sweep below used was incomplete. Most of the 109 are browser chrome. The
words that match the portfolio-table prediction are `atom`, `link`, `basic`,
`token` and `dash`; `cash`, `icon`, `wave`, `gas`, `ocean`, `fetch` and
`ripple` are not legible at that resolution and not spoken. `cloud` is not on
screen, which supports `fog`. A second channel no sweep has used: the spoken
words of the video (129 dictionary words in the auto captions, 110 not in the
pool). Both lists are in `data/video-onscreen-words.json`. I checked all 219
words against the list and spot-checked `link`, `token`, `atom` and `reveal` on
my own frames. The RO1 model extended with the five coin words as free video
words is the natural next sweep; @cjmcdaniel said they are running it.

Original lead text, kept for the reasoning:

The author states in the spoken rules of the challenge video,
https://www.youtube.com/watch?v=w4mpiuBP_aY at 5:22 to 5:38, that the words
"could be you know written in the video on the screen so read carefully". The
written rules in the hint 5 description agree, listing "description, tags,
title, video basically could be anywhere in this video". Quoted in
`clues/author-posts.md`.

Every sweep in `analysis/tested.md` draws its pool from the description, the
title, the tags and the post body. None has read a single frame of the video
image. That makes on-screen text the only author-named channel that has never
been examined at all, which is a different class of gap from an unswept corner
of a pool that has been read.

There is independent reason to expect payload there. The video shows a
portfolio table of coin holdings. Ten coin names visible or audible in that
segment are BIP-0039 dictionary words: `atom`, `link`, `dash`, `cash`, `icon`,
`wave`, `gas`, `ocean`, `fetch`, `ripple`. Checked against the wordlist, none
of the 10 appears in any 2020 written surface recovered so far. If even one is
a list element, every sweep in this folder was drawing from an incomplete pool
and its negative result says nothing about the phrase.

Method, for anyone with the video and a normal desktop: download it, sample
frames at 1 per second, read the text in each frame, intersect the result with
the BIP-0039 English wordlist, and add anything new to the pool before
re-running RO1. Optical character recognition on 1 frame per second is enough;
a person watching once and writing down the visible tickers gets most of it.
Check explicitly for `cloud`, which decides established fact 3 in the README,
and for the 10 coin words above.

What would confirm it: a dictionary word legible on screen that appears in no
written surface, which then completes a phrase through `tools/oracle.py`.
What would kill it: a complete frame read yielding no dictionary word absent
from the already-known pool. That is a real exhaustion point, unlike a
re-read of prose.
Cost: about an hour of directed work, no compute budget.

## 2. Extend the swept word pool with connecting words (liaisons)

Unchanged in substance from the previous lead 1, still open, now second because
lead 1 is cheaper and can invalidate the pool this lead extends.

Every completed sweep draws its non-anchor words from full words in the
recovered text. None includes the short connecting words from the same
sentences: prepositions, articles and conjunctions such as "there", "will",
"also", "you", "more", "can", "then" on the video side, or "only", "because",
"there", "like" on the post side. Sized at 15 and 14 words per side,
1.36x10^10 derivations, about 4.8 hours at 792,000 derivations/second.

Note the interaction with RO1: "also" is one of only 2 dictionary words lying
between `fog` and `parrot` in the video text, and RO1 already covered every
reading-order arrangement containing it. So the part of this lead that overlaps
the reading-order model is closed; what is open is the free-order remainder.

What would confirm it: a match within the extended set.
What would kill it: exhausting the extended set with 0 match, under the same
witness protocol as every prior sweep.
Cost: hours on one rented GPU.

## 3. Re-check the already-enumerated survivors on other derivation paths

Cheap, decisive, and never run. Every sweep in this folder derives only
`m/44'/60'/0'/0/0`, the MetaMask default first account. The escrow is stated to
be a MetaMask wallet, so that is the correct first guess, but if the author
funded the challenge from the second account in the same wallet, or from a
second wallet in the same application, then every negative in
`analysis/tested.md` is a negative about the wrong address and says nothing
about the phrase.

Paths worth checking: `m/44'/60'/0'/0/1`, `m/44'/60'/0'/0/2`,
`m/44'/60'/1'/0/0`, `m/44'/60'/2'/0/0`.

The cost is low because the expensive half of the work is already done. The
PBKDF2 seed stretch dominates a BIP39 derivation; changing the path only
repeats the child key derivation and the address hash. Re-running the 10,484,919
RO1 survivors on 4 extra paths costs about 28 percent of the original run, not
400 percent.

What would confirm it: a match on any of the 4 paths.
What would kill it: 0 match across all 4, which upgrades every existing
negative in this folder from "negative at the default path" to "negative across
the plausible MetaMask path family".
Cost: about 4 hours on 2 CPU cores, seconds on a GPU. This is the best value
experiment currently available in this folder.

## 4. Substrings of longer written words

Demoted from lead 2, with a correction to the reason it was ranked so high.

**The correction.** This lead used to say that the author, asked whether a list
word could be hidden inside a longer written word, "answered yes and gave
"possible" inside its own negation, formed with the prefix "im-", as his own
example". Reading the comment thread directly shows the nesting example belongs
to the reader who asked the question, not to the author. The author's reply is
"1. Yes for example usa could be united states in hints , but wikk have corect
word in text at chalange." His own example is an abbreviation, it is offered
about hints, and he contrasts it with the challenge text, which "wikk have corect
word". A second thread has the same shape: asked how the first word can be
"Netherlands" when that is not in the wordlist, he answers that the exact word
is in the post. Read together, the 2 replies describe hints that gloss a word,
not text that conceals one inside another. Both are quoted in full in
`clues/author-posts.md`.

So "yes" is real but its subject is contested. The substring mechanism is now a
reader's hypothesis that the author did not contradict, which is weaker
evidence than an author-stated mechanism.

**A second argument against it.** All 5 confirmed list words appear as whole
tokens: `dutch` and `fiber` in the post body, `fog` and `parrot` in the video
description, `fork` in the post's tags. Not one of the 5 is a substring of a
longer word. If the author had used a substring mechanism across 12 elements,
seeing 5 of 5 come out as whole tokens has probability roughly 0.065 under a
simple model where each element is independently whole or nested. That is weak
evidence against the mechanism rather than proof, and it should be red-teamed:
the 5 known words are exactly the ones the author chose to write hints for, and
a hint is easier to write for a whole word, so the sample is not drawn at
random from the 12. The argument survives that objection only in weakened form.

If the mechanism is real, substrings already identified include "cat" (cattle),
"ill" (will), "hen" (then), "like" (likely), "cause" and "use" (because),
"health" (healthy), "hunt" (hunter) and "inner" (dinner). Sized at 21 and 20
words per side, 2.78x10^11 derivations, about 4.1 days at 792,000
derivations/second. Sweep RO2 in `analysis/tested.md` has already covered the
reading-order corner of this space, 582,725 derivations, 0 match; that leaves
the free-order remainder, which is the bulk of it.

What would confirm it: a match within the substring-extended set.
What would kill it: exhausting it with 0 match. Re-price before running, since
throughput changes the estimate directly.
Cost: on the order of a day on one rented GPU.

## Retired: position 5 is settled

An earlier open question asked whether position 5 holds `fog` or `cloud`. Treat
it as `fog`. Hint 3 describes condensed water droplets; 3 BIP-0039 words fit
that description, `fog`, `cloud` and `vapor`, and of the 3 only `fog` appears in
any recovered 2020 written surface, at index 25 of the video description. The
author's own reply that the challenge text carries the exact word points the
same way: a hint may gloss, the text does not. `cloud` remains worth a glance
during lead 1, because on-screen text is the one channel that could still
produce it, and if it does appear there this retirement should be reopened.

## Community corrections: R1 pool provenance (issue #10)

HPreziosa (issue #10) grepped the 2020 Wayback captures of the video and blog
and found three R1 pool words mis-sourced: `top` and `finish` are in the blog
body and video description, not the video title as the ledger's "title and hook
line" row said (`finish` only as the inflection `finished`), and `cloud` appears
in no authored 2020 surface. Verified against the archives on 2026-08-21
(Wayback `20200626184951` of the video, `20201026062858` of the blog). Result:
`top` and `finish` stay in the pool but are re-sourced, and `cloud` is dropped as
a candidate because only `fog` appears in a written 2020 surface. This is what
settles position 5 as `fog` (see "Retired: position 5 is settled" above) and it
is the basis for `cloud` being dropped in sweep C1.
