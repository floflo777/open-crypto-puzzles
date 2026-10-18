# Open leads, ranked -- Arweave Puzzle Weave #12

Supersedes the README's "Open leads, ranked" and an earlier draft of this file, as of
2026-08-18 (second pass). Piece 2 remains the blocker, but the shape of the problem is
now much better defined and several once-plausible escapes are closed.

## What is now settled

- **Piece 3 = `2111011`**, independently re-derived (square/diamond/rectangle fix the
  ascender-x-height-descender rule with no free parameter; hexagon follows).
- **Piece 4 is exactly five letters** -- five hatched squares at 88-89px, five orange
  glyphs, stable across thresholds. The six-letter-word idea is refuted. All 120 letter
  orders have been swept, not just the dictionary anagrams.
- **Piece 1's candidate orderings are measured, not guessed.** Three vertical pairs by
  flag x-position; twelve principled reading orders; 144 strings instead of 4,320.
- **The 28+18 split is dead** across all 24 block orders and all 144 orderings. This is
  the split every solver reaches, because `AndreessenHorowitz` is the only investor name
  that closes the budget alone.

## 1. Piece 4's answer may not be the five letters -- WORKED OUT AND DEAD

The hatching on piece 4 is the Petra Sancta heraldic convention -- each square quartered,
each quadrant hatched in the direction that denotes a tincture (see tested.md). Two of
the four clues are therefore about colour, which is unlikely to be a coincidence.

Worked out 2026-08-19 and negative in every form tested (tested.md rows 18 and 19, and
the decoding notes there): as five ASCII bytes at two bits per quadrant, as eight
five-bit letters, and as a literal 20-character sub-answer against all four length
pairings that 58 - 7 - 20 = 31 admits.

The heraldic identification itself stands and is worth keeping -- the hatching is a
recognised colour notation drawn correctly in four directions, not decoration. But it has
no demonstrated role in the answer under any of the three readings now tested:
directional ordering (row 1), heraldic tincture (rows 18 and 19), or line count.

A warning for whoever picks this up: hatch-line counts are **not** reliably measurable
here. Three counting methods give three different answers, and one of them produces a
seductive run of five consecutive integers that is pure artifact.

## 2. Piece 2, without the proper-noun assumption

Every search so far, here and in the community, has assumed piece 2 is a name. Sibling
#5's confirmed sub-answers are `*`, `48`, `GCE` and `Eris`; sibling #3's are
four-character tokens including the chess move `e4d5`. This author uses bare symbols,
numbers and acronyms freely.

So piece 2 may be an acronym (`a16z`, `USV`, `AH`), a bare number, or a date string, at a
length that pairs with a different piece-1 reading. The length algebra in tested.md gives
the pairings; the branches already swept are 28+18, 12+34, 11+35 and 9+37. Unswept and
cheap: piece 2 as `a16z` (4) with piece 1 at 42, and piece 2 as a formatted date
(`16-03-2020` = 10, `16032020` = 8) with piece 1 at 36 or 38.

## 2. Piece 1 as something other than colour names -- AUDITED AND CLOSED

Done, 2026-08-18; see the assumption audit in tested.md. The attributes were measured
(ball on violet/red/green, none on gray/purple/blank; flag side opposing in all three
pairs) and turn out to be scaffolding: the blank flag's attributes are fully determined
by its partner, so they encode the pairing rather than a payload. Reading them as an
18-bit answer is refuted on that principle, no sweep required.

Every colour-derived encoding whose length pairs with a supported piece-2 reading is now
dead: six names (28) with `AndreessenHorowitz`, three primary names (12) with
AH+CoinbaseVentures, six bare hex codes (36) with the date as drawn, and six
`#`-prefixed codes (42) with `a16z`. The two encodings left untested -- a single colour
name (4) and one-letter abbreviations (6) -- are untested because nothing plausible sits
at the 42- and 40-character piece-2 lengths they force.

The audit's own conclusion is that piece 1 is not where the error is.

## 3. All four clues pointing at one answer -- TESTED AND DEAD

Swept 2026-08-19 (row 17): every ordered concatenation of the clue-implied vocabulary
totalling exactly 58 characters, 516,138 candidates, 0 match.

There is also an argument against the model that should have been weighed earlier. Piece
3's answer is a *digit string*, `2111011`, and that is certain: the puzzle prints codes on
three shapes and leaves the hexagon's blank. Four clues cannot jointly name a
natural-language phrase when one of them contributes digits. The concatenation model is
the right one, and it matches sibling #5, whose confirmed sub-answers were a symbol, a
number, an acronym and a name.

So the error is in a sub-answer, not in the model joining them.

## 4. Upstream the fast-reject oracle (tooling)

`tools/oracle.py` decrypts all 198 ciphertext blocks; the `"kty":"RSA"` gate lies wholly
inside block 0. Decrypting one block takes the rate from 2.04 to 40.3 candidates/second
per core, about 20x, with any hit re-checked through the unmodified oracle. Worth shipping
as a `--fast` flag with its scope limit documented (it assumes the keyfile begins with
`{"kty":"RSA"` at offset 0, as sibling #8's does).

## Retired

- **"Confirm piece 1's blank flag as Blue by an oracle hit"** (README rank 2). Not
  independently testable: an oracle hit needs every block correct at once, so no sweep can
  confirm or refute Blue while piece 2 is unknown. The structural case for Blue is
  nonetheless strong -- one additive primary per measured pair -- and the lengths close
  exactly at 28.
- **Co-investor names as piece 2 at length 18.** Length-refuted:
  `UnionSquareVentures` is 19, `CoinbaseVentures` is 16. Both have now been swept in the
  two- and three-name concatenations where their lengths do close the budget.
- **Hatching as an ordering scheme.** Confirmed refuted a second time, by measurement:
  distinct hatch directions per square are 3,2,3,4,3, not a permutation of 1 to 5.
