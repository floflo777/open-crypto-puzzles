# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

## 1. Write to the author

Keysa is active (her most recent Nostr event at the time of my last check was
2026-08-01) and has twice invited exactly this kind of contact in her own posts:
"I would love to know if this method is solid" and "Open to comments." Her stated
interest is in an audit of her method, not in protecting a secret. This is a near
zero cost action with the highest plausible payoff, since the selection rule is, by
her own description, short, memorable, and meant to be spoken aloud to a trusted
person, which is exactly the kind of fact that a mechanical sweep cannot recover but
a direct question can.

What would confirm it: a reply describing the selection rule, or enough of it to
narrow the remaining candidates to something `tools/oracle.py` can check directly.
What would kill it: no reply, or a reply that does not narrow anything (she has
stated before that she does not want to spoil the puzzle for others).
Cost: needs a person; no compute cost.

## 2. A new selection family, replayed under the two-words-out-of-order model

The earlier version of this lead read the puzzle as "order, not selection", on the
strength of Keysa engaging with a reader's permutation count. Her own replies two
levels down in the same thread say the opposite (`clues/author-posts.md`,
2023-06-27): "one still wouldn't know which of all those words are the 12", and "all
the words but two, are in order". So the order is the card's reading order up to two
words, and the lock is the selection.

Under that model every candidate set this folder has ever produced is negative
(L-009 in `analysis/tested.md`: 2,084,778 distinct sets under reading order plus one
transposition, 31,088 natural sets under up to two moved words, and the reversed
reading order). Replaying a set costs milliseconds, so a new family of sets is cheap
to test and the whole cost is in proposing it. What such a family would be built on:
the card's typed rows, the 20-pixel gap after `mad` (the first token), and the 3-6-9
theme of her book, none of which has produced a selector yet.

What would confirm it: any new 12-token set whose 67 (or about 6,100) orders,
run through `tools/oracle.py --stdin`, return a MATCH.
What would kill it: nothing bounded; the lead stays open until a family is proposed.
Cost: minutes per family on a CPU; the 12! GPU sweeps of the earlier reading are no
longer useful.

## 3. Two tokens per row, under the corrected order model

The 6 rows are typed line breaks (see the row-structure measurement in
`analysis/tested.md`), so a rule that picks 2 tokens from each row is a legitimate
family. Under the old "arbitrary order" reading it cost about 76 minutes on one GPU
(3.6e9 candidates after the checksum filter). Under reading order plus one
transposition it costs 67 times more: about 2.4e11 derivations after the checksum
filter, about 3.5 days at 790,000 derivations/s on one GPU. The per-row-pair readings
already run (the left and right column pairs among the natural sets in L-009, and
the 13 pair types in the ebreen fork's L-010) are negative.

What would confirm it: a MATCH from `tools/oracle.py` on a candidate from this space.
What would kill it: the full space with witnesses at head, middle and tail, 0 match.
Cost: days of rented GPU; not proposed without a row rule that narrows which pair.

## 4. The double-width gap after "mad", and the "369 clock" theme

Two weaker, unresolved observations, neither of which is itself an actionable next
step:

- The gap after the first token, `mad`, measures about 20 pixels, against 9 to 13
  pixels for every other inter-word gap on the card (`analysis/tested.md`). This is
  the only typographic anomaly on the card. It may mark a deliberate starting point,
  or it may be an unrelated formatting choice; I have not derived a selection rule
  from it to test.
- Keysa's own book anchors the 369 theme in a real, author-owned passage (pages 126
  to 127, "Satoshi's Numbers: 369 Clock"), which rules out the amount being purely
  decorative, but no digital-root or modulo-9 based selector derived from this theme
  has produced a match (L-004, L-005 in `analysis/tested.md`).

What would confirm either: a specific selection rule derived from one of these
observations that `tools/oracle.py` confirms.
What would kill either: this is not a bounded space to exhaust; both stay open until
a rule is proposed and tested, or until new information (most likely from lead 1)
explains them.
Cost: needs a new insight; no compute action is available on either today.
