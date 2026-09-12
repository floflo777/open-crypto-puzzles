# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts below were re-read from my own private research notes before writing this
folder; most of the work was carried out by autonomous search agents I supervised,
running the certified oracle in `tools/oracle.py` (a slower stdlib-plus-bip_utils
port of the fast internal derivation path used during the original sweeps).

## L-001: all orderings of the 12 dotless tokens

Exactly 12 of the 70 tokens on the card carry no trailing dot: `mad`, `shop`,
`beauty`, `vocal`, `sight` (end of row 2), `upgrade` (end of row 3), `trend`, `zoo`
(end of row 4), `skull` (end of row 5), `steel`, `essence` (end of row 6), plus
`buffalo` (end of row 1). This cardinality matching 12 exactly was the strongest
structural lead in the folder.

Method: enumerate all 12! orderings of this 12-token set, derive each ordering's
BIP84 address, compare to the escrow address.

Result: 479,001,600 orderings enumerated, all exhaustively; 29,943,427 of them pass
the BIP39 checksum (0.0625, exactly 1 in 16, matching the expected rate); 0 exact
address matches. Rate: 13,564 derivations per second on 24 CPU cores, 36.8 minutes
total. Date: 2026-08-02.

Witness: this sweep predates the formal witness protocol adopted later in the same
research folder (a known-good candidate planted at the head, middle, and tail of the
search order). The result is exhaustive and the derivation pipeline is the same
oracle certified elsewhere in this ledger, but under this folder's own house rule a
negative without a planted witness is not called a final negative. I list it here as
uncertified rather than as a closed negative, even though I have no reason to doubt
it. It is corroborated by the author's own statement, "the dots are random, can
ignore" (2024-11-12), which argues against dot status being the selector at all.

## L-002: positional and geometric readings

Method: enumerate whole families of position-based reading rules rather than one
rule at a time: periodic gaps (periods 1 to 4, every starting position, every gap,
with and without wraparound), self-referential jump rules (jump by the letter count,
vowel count, consonant count, initial letter, final letter, or vocabulary rank of
the current token, every offset and starting position), staircase reads across rows
(including negative steps), all contiguous same-length slice pairs, arithmetic and
diagonal reads (free starting point and slope), same-position and mirrored-position
reads across rows, card-digit-based reads (`369369`, the date `6/25/23`, the row
lengths, used both as positions and as jump sizes), and punctuation-based reads
(dot-closed groups, first or last token of a group, the 12 dotless tokens read in
card order).

Result: 669,858 distinct readings enumerated, 41,809 of them actually valid enough
to derive (pass basic structural constraints), 0 matches. Rate and hardware: run on
CPU, elapsed time not separately recorded from L-001. Date: 2026-08-02.

Witness: yes. A known-good reading was planted in the search order and correctly
recovered by the same code path, closing this as a formal negative under this
folder's witness protocol.

## L-003: acrostic (initials spell a word)

The 70 token initials use only 20 distinct letters (missing `g`, `k`, `q`, `w`, `x`,
`y`), which already rules out any 12-letter target word using one of those 6
letters.

Method: for each of 1,723 composable 12-letter English dictionary words (composable
meaning every letter of the word appears among the 70 initials), test whether the
word is realizable as a subsequence of the initials in card order.

Result: 36 selections were realizable as a subsequence, of which 3 pass the BIP39
checksum, 0 address matches. Date: 2026-08-02.

Witness: the acrostic extraction code was self-tested (a known subsequence is
correctly recovered from a synthetic initial-letter sequence), but no witness was
run under the folder's later, stricter protocol with a planted candidate at head,
middle, and tail of this specific search. I list this as uncertified. Note:
concatenations of two dictionary words to spell a longer acrostic were not
enumerated, since that space (about 110 million pairs) was judged too large relative
to its likely payoff and was not run.

## L-004: intrinsic token properties

Method: test 105 criteria based on properties of each token in isolation (character
length, initial letter, final letter, vowel count, position in the official BIP39
word list, digital root of that position, digital root of the position plus 1,
digital root of the sum of letter values, position modulo 9, letter-sum modulo 9,
and every union of the "3, 6, 9" outcomes of these measures) to see whether any of
them partitions the 70 tokens into a group of exactly 12.

Result: none of the 105 criteria produces a partition of exactly 12; the closest are
11 (digital root of vocabulary position plus 1, restricted to values in {6, 9}) and
13 (digital root of the letter sum equal to 9). This is a structural fact about the
token set, not a set of candidates checked against the oracle, since no criterion
reached the required cardinality to test further. Date: 2026-08-02.

Witness: not applicable; this is a direct computation over the 70 known tokens, not
a search that could produce a false negative in the usual sense. I still mark it
uncertified in the summary table because it was not run through the oracle.

An earlier internal note claimed a stronger result from this family (a criterion
that did partition the tokens); that claim was traced to 0 actual submissions to the
oracle and was corrected. The real, verified fact is the structural one above.

## L-005: the "369 clock" theme

Keysa's own book, "The Simplest Bitcoin Book Ever Written," contains a two-page
section titled "Satoshi's Numbers: 369 Clock" (pages 126 to 127) discussing digital
roots and Tesla's reported "3, 6 and 9" quote. This is a real, author-owned anchor
for the escrow amount (369,369 sats), but it does not by itself specify a selector
over the 70 tokens.

The digital-root and modulo-9 criteria from L-004, and the periodic-step-3 or
step-6 or step-9 readings from L-002, already cover the direct mechanical
translations of this theme; all were negative as reported above. This lead remains
open as a source of a selector I have not yet found, not as an untested space.

## L-006: semantic and mnemonic candidate selections

The selection rule may be based on meaning rather than position: a phrase, a story,
or a category that picks out 12 of the 70 words without following a positional
pattern. This kind of rule is not enumerable the way a positional rule is, so it
cannot be closed by sweeping every case.

Method: a supervised wave of independent search agents, each working from the same
neutral framing and the same sealed oracle, proposed and tested candidate selections
under 114 separately labeled hypothesis families (thematic groupings such as
travel, calendars, and story structure).

Result: 572,368 valid 12-word selections tested, 439,773 of them distinct sets of
12 tokens, 0 matches. Date: 2026-08-02.

Witness: the oracle used for these tests is the same one certified elsewhere in this
ledger. No single planted witness applies to this family, since it is not a single
enumerated space with one search order; I mark it uncertified in the summary table
on that basis, while noting the volume of testing.

## L-009: every known candidate set under "reading order, all but two words"

Keysa wrote on 2023-06-27, in a sub-thread under her original post, "In this example,
all the words but two, are in order ;)" and, 8 minutes earlier, that one "still
wouldn't know which of all those words are the 12" (`clues/author-posts.md`). The
order of the seed is therefore the card's reading order of the 12 selected tokens,
except for two words. Two order models cover that sentence: reading order plus one
transposition of two words (66 transpositions plus the identity, 67 orders per set),
and reading order with up to two words moved anywhere (about 6,100 orders per set).
None of the sweeps in L-001 to L-006 tested a transposition: they used the card
order, its reverse, the reading order and its reverse only.

Method: replay every candidate set the folder had produced under those two order
models: 196,000 sets from the positional rules, 1,170,000 sets from 8 further
positional families (row-by-column sub-grids, per-row 3-6-9 digit and mirror rules,
arithmetic progressions plus a free token, multiple takes of 3, 3 and 6, 12 groups
of 5 to 7 tokens, circular walks from every start, key-token initials, removal
rounds), the 31,088 natural sets (rows of 12, row edges, dotless tokens, windows,
left and right column pairs, sub-grids, progressions) and all 877,000 sets from the
L-006 agent wave: 2,084,778 distinct sets. Derivation BIP84 `m/84'/0'/0'/0/0` and
`0/1`, checksum filter first, then the certified oracle.

| Campaign | Sets | Order model | Sequences | Checksum-valid derivations | Result |
|---|---|---|---|---|---|
| 1 | 2,084,778 | reading order plus one transposition | 139,680,327 | 8,730,698 | 0 match |
| 2 | 31,088 natural sets | reading order, up to two words moved | 188,500,763 | 11,775,450 | 0 match |
| 3 | 2,084,778 | reversed reading order plus one transposition | 139,680,327 | 8,729,064 | 0 match |

Witness: 3 synthetic sets, each with a target address derived in advance from one
order of the same model, planted at the head, middle and tail of each run and
recovered by the normal path. The first reversed-order pass planted a witness built
on the direct reading and recovered 0 of 3, which is what the witness is for; it was
re-run with witnesses on the normal path. Rate: CPU only, elapsed time not recorded.
Date: 2026-08-16.

What this closes: under the author's own order statement, no candidate set this
folder has produced is the seed. What it leaves open is the selection rule itself,
which is not an enumerable space. As a scale reference, all C(70,12) sets in reading
order are about 1e13, or 6.6e11 derivations after the checksum filter, and the two
words out of order multiply that by 67; that is not a sweep, it is the reason the
next step is information from the author.

## Contributed (fork, not a pull request): ordered readings of the typed rows, 2026-08-17

A fork by ebreen (branch `cursor/keysa-spoken-cipher-9cc6`) records four families of
ordered readings run through this folder's oracle on 2026-08-17: every-k walks for
k = 5 to 12, a 69-token stream that drops `mad`, 3-6-9 take-then-skip, two-column
reads of the padded 6x12 grid and keyword-mapped columns (9,513 sequences, 643
checksum-valid); self-referential and keyed jump walks (5,808 sequences, 388 valid);
speakable row-block readings, first, last or middle n tokens of m rows, column takes
on row groups, half-card concatenations (7,560 sequences, 466 valid); and per-row
pairs of 13 types under every row permutation and per-row flip (5,203,141 sequences,
312,753 valid). All 0 match. Recorded as reported, not re-run here; the fork describes
constructed sequences re-found in its own candidate set as the witness for the first
and third families and marks the jump family uncertified. Under the 2023-06-27 order
statement most of these orders are no longer candidates. The same fork read, on the
2024 Nostr repost of the card, the note's title "369369 Sats Guessing Game" and the
BlueWallet header "Crack the Seed Game HD SegWit", a second confirmation of BIP84.

## Typographic measurement (not a hypothesis test)

A pixel-level measurement on the binarized card image found that the gap after the
first token, `mad`, is about 20 pixels wide, while every other inter-word gap on the
card measures 9 to 13 pixels. This is the single typographic anomaly on the entire
card, and it falls on the very first token. It is not itself a tested hypothesis,
since no selection rule based on it has been derived and checked; it remains an open
observation (see the README's open leads).

## Row-structure measurement (not a hypothesis test)

An initial reading concluded that the 6-row wrapping (12/12/11/12/12/11) was a
rendering artifact of the display width, since a greedy line-wrap algorithm
reproduced the same row lengths for a range of column widths. This conclusion was
wrong: it showed the wrapping was compatible with an automatic reflow, not that it
was caused by one. A narrower-column screenshot of the same note, found later,
settled the question: at that width, the note's rows visibly wrap onto extra display
lines, and at 5 of those wrap points the leftover horizontal space (309 to 422
pixels) is far larger than the next word would have needed (129 to 196 pixels). An
automatic reflow never leaves that much room unused, so the 6 logical rows are
typed line breaks, not a rendering side effect. This supports treating row-based
rules (two words per row, columns, diagonals) as legitimate rather than coincidental.
