# Solved and paid out

The exact solution and confirmed payout are now recorded in the README.
The earlier leads below are preserved as historical community research.

# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.
The gate on this puzzle is entirely cultural (the title-to-word rule and an IMDb
field), not computational: once the 34 words and the intruder rule are both known,
checking a candidate is a single `tools/oracle.py` call.

## Frame-level reconciliation, 2026-08-27

The nine panels that still disagreed between `data/films.csv` (2026-08-04 pass)
and `data/films_community_issue9.csv` were checked against the published stills
at bitcoinmovieenigma.com. Community identifications that the still itself
settles, and that are now merged into `data/films.csv`:

| panel | 2026-08-04 pass | community / still |
|---|---|---|
| 3 | Alien | Aliens (1986): M41A pulse rifle, facehugger jar, Hadley's Hope ops console marked 70 |
| 5 | Star Trek: The Motion Picture | Alien (1979): Ripley in the Narcissus EVA suit; a shelf label reads RIPLEY |
| 14 | Eyes Wide Shut | The Man in the Iron Mask (1998): gold lorgnette masks, Louis XIV court dress; settled 2026-09-03 by deviceio121's frame from MGM's official clip (issue #9) |
| 16 | The 13th Warrior | The Visitors (1993): headless knight standing in a meadow |
| 23 | Valerian | Guardians of the Galaxy (2014): Nova Corps command table over Xandar |
| 27 | The Lost Boys | Terminator 2 (1991): biker-bar boots on wet asphalt at night |

Three panels stay `confirmed-community` rather than `confirmed`, because the still
alone did not give me an independent match and I am relying on the issue #9
sources (YouTube / IMDb / blog stills cited there): panel 9 Spartacus, panel 13
Leon: The Professional, panel 24 Close Encounters of the Third Kind.

Panel 8 (The Goonies) and panel 26 (Sharknado) were already agreed and hold at
the frame: trench-coat men, umbrellas, coloured mailboxes and a cargo ship in
Astoria; John Heard at Fin's bar under the SANTA MIRA BEACH 1986 poster.

## 1. The title-to-word rule, now only The Goonies is wordless

Under a literal substring scan, five community titles yield no English BIP39
word: The Goonies, Leon: The Professional, Sharknado, Raiders of the Lost Ark,
The Shining.

Under the unique 4-letter BIP39 prefix scan of the title with spaces removed,
four of those five resolve: Leon -> `profit`, Sharknado -> `share`, Raiders of
the Lost Ark -> `soft` (the compact string `raidersofthe` contains `soft`),
The Shining -> `shine`. Barry Lyndon is `bar` / `barrel` either way. That leaves
**The Goonies as the only title with no BIP39 reading of either kind**.

What would confirm a Goonies word: a single rule that also produces the 33
already-read words, checked against the escrow with `tools/oracle.py` once the
24-word set is assembled.
What would kill a candidate Goonies word: a full 24-word mnemonic that uses it
and still returns NO MATCH under every remaining intruder rule. That is not a
bounded exhaustion.
Cost: an insight; no compute action available that stays under two hours without
a rule that first shrinks the 10-intruder set.

## 2. The IMDb metadata field that splits 24 keepers from 10 intruders

About 25 to 30 binary IMDb-field criteria were tried against the old film list
and refuted (`analysis/tested.md`). On 2026-08-22, timothy-barus reported three
exhaustive GPU sweeps on the community list (shares-a-year, released-2000-or-later,
ten-shortest-by-runtime), about 1.23 billion checksum-valid seeds, all empty
(his numbers, not reproduced here). SmallCakekoo reported 17 certificate/genre
pairings that select exactly 10 panels, all empty against a fixed word list.

A new certificate reading was tested on 2026-08-27: drop G, PG, and TV-14
(panels 7, 8, 12, 18, 24, 25, 26, 30, 31, 32), keep the rest, and vary the
short per-title word lists. 55,296 raw strings, 227 checksum-valid, 0 match,
uncertified (see `analysis/tested.md`).

What would confirm a field: an IMDb column that splits the reconciled 34-film
set into exactly 24 and 10, tested against the escrow once combined with the
word rule.
Cost: an insight; the Goonies word and this field are coupled, so a rule that
drops panel 8 is cheaper than one that keeps it.

## 3. Kubrick x5 plus Jean Reno x5 at two wildcards

The author's Nostr note names director and actors as the fields to read on IMDb. On
the consensus list exactly 5 films are by Stanley Kubrick (panels 2, 9, 17, 25, 33) and
exactly 5 star Jean Reno (10, 11, 13, 15, 16); together they are 10, and the split needs
panel 14 to be The Man in the Iron Mask rather than a sixth Kubrick, which is now
settled. The 24 keepers then contain three titles with no literal word (The Goonies,
Sharknado, Raiders of the Lost Ark). With panel 8 free over the 2048 words and panels
26 and 32 read as `share`/`tornado` and `soft`, the sweep is negative (3.1e6 raw
candidates, `analysis/tested.md`), and so is the widened-ambiguity version (1.0e9).

What remains is two free positions: (8, 26) with 32 in {`soft`, `ride`}, and (8, 32)
with 26 in {`share`, `tornado`, `ski`}, about 6.4e9 raw candidates and 2.5e7
derivations per pair, about 3 minutes each on one GPU with the shared 24-word engine.
Three free positions is 2048 times more and is not proposed.

What would confirm it: a MATCH on either pair.
What would kill it: both pairs empty with head, middle and tail witnesses recovered.
Cost: minutes of GPU; the enumeration and witness harness already exist.

## 4. Regional IMDb titles and AKAs for the wordless titles (issue #9, couldes)

couldes raised that IMDb pages differ by region, some carrying a subtitle. The word
step reads from the film, so a regional subtitle is not in the search space by default.
For the titles that yield no literal word, an alternate release title is the cheapest
place a word could hide: Sharknado's German title "Dark Skies" gives `ski`, which the
widened sweep already covers; The Goonies and Raiders have no such reading yet. No
confirmed channel to the author exists to ask.

## 5. Panels 9, 13 and 24 as the last identification risk

If any one of Spartacus, Leon: The Professional, or Close Encounters is wrong,
every word list built from this table is underivable. The issue #9 sources are
the next check, not another still-only pass.

## Community identifications, 2026-08 (issues #9 and #3)

Two readers who watched the films posted panel identifications, one with per-scene
notes (issue #9, garrou), one confirming two panels after re-watching (issue #3,
CryptoBlueprint), plus a full 34-title list with IMDb ids in the issue #9 thread.

**They close the two panels this folder had left open.** Panel 11 is Godzilla (1998),
the footprint scene, and panel 34 is The Human Centipede (First Sequence), which
settles the Dead Ringers / Human Centipede dispute in favour of Human Centipede.

**By 2026-08-27 the nine remaining disagreements are settled or narrowed as above.**
The full community list, with IMDb ids and the community's own title-to-word
reading, remains in `data/films_community_issue9.csv` as the alternative fork.
`data/films.csv` is now the merged canonical list.
