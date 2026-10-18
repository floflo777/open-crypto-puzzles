# Open leads, ranked

## 1. Re-run the grid enumeration at a wider row window, one doubtful hour at a time (hours)

A serif numeral spans about 2 text rows on the published raster, so the true row for some hours
may be 2 rows away from the numeral's centroid, not 1. Opening the window to plus-or-minus 2 on
all 12 hours at once would multiply the space far past what is practical to check, so the right
next step is to widen only the hours whose reads look weakest, starting with the ones clipped at
the image's circular frame edge, one at a time. Confirms: any opened hour turns up a match under
one of the 4 canonical orderings. Kills: widening every doubtful hour individually with no match
closes this specific readout rule (numeral-overlays-word) as the answer.

## 2. Resample at the numeral's bottom pixel instead of its centroid (minutes)

The current model samples each numeral's centroid; because the glyph itself is tall, the
intended word may sit under its lowest pixel rather than its middle. This is a cheap
re-measurement, not a new brute-force pass: re-reading all 12 hours this way changes at most a
few candidates per hour before the same 4-ordering oracle sweep is repeated. Confirms: the new
reads produce a match. Kills: the same 4-ordering sweep on the new reads, run to completion,
with no match.

## 3. Test the sunburst ray length as an alternative per-hour selector (hours)

The 24 sunburst rays on the plot have measurably varying lengths. The current model assumes the
word is chosen by which numeral it sits under; ray length has never been tested as an
alternative or additional selector, and it could also supply an independent ordering signal
apart from the clock position. Confirms: a per-hour selection rule based on ray length, fed
through the oracle, matches. Kills: a systematic pass over ray-length-based selection rules with
no match, though this space is less bounded than the row-window leads above and would need its
own scoping before a run.

Full ledger: [tested.md](tested.md).
