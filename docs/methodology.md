# Methodology

This is how I worked through these puzzles. It is the reusable part: the rules that kept
months of work from producing false positives or wasted compute. If you contribute a
negative, a lead, or a solve, follow the same rules so the catalogue stays trustworthy.

## Oracle first

Before searching anything, I write a small program, the oracle, that takes a candidate answer
and says MATCH or NO MATCH against the target address or value. Then I run the oracle's own
self-test: feed it a known-good input (a solved sibling puzzle, the author's own published
example, or a public test vector such as the standard BIP39/BIP32 vectors) and confirm it
reports MATCH. An oracle that has never matched anything is not trustworthy yet, no matter
how obviously correct its code looks. Every folder's `tools/oracle.py --selftest` runs this
check and must print `SELFTEST OK` before any search using it counts for anything.

## Witnesses: head, middle, tail

A search that reports "zero matches" is not evidence of anything by itself; it might just
mean the search never actually ran the candidates through the real pipeline, or stopped
early, or hit a filter that silently rejects everything including the true answer. Before
believing a negative, I plant three witnesses of the exact shape being searched for, one near
the start of the search, one in the middle, and one at the end, and confirm the search finds
all three. If the tail witness is missed, the search did not go all the way through and the
whole run is void, not just the untested part. A witness only counts if the tool would treat
it exactly like a real candidate; a witness that takes a special code path proves nothing.

## Zero false positives

A candidate counts as a solution only when the derived value is exactly equal, character for
character or byte for byte, to the target. A valid checksum is not a match. Plausible-looking
plaintext is not a match. A near miss (one character off, one word swapped) is not a match
and is not reported as one, even as a curiosity, because it invites a reader to mistake it for
progress.

## Scope travels with the number

A negative result is only meaningful together with what exactly was tested. "0 match" alone
says nothing; "0 match under BIP84 derivation with an empty passphrase, English wordlist,
12-word candidates built from the 20 printed words" is checkable and falsifiable. Every
negative in this repository states the count of candidates, the method in one line, whether
it carries a witness or is labeled uncertified, the rate achieved, and the date.

## Bounded search arithmetic

Compute is verification, not discovery. A properly bounded search finishes in seconds or
minutes; if a plan needs hours, the constraint that would shrink the space has not been found
yet, and I look for that constraint before asking for more hardware.

The most common free filter for seed-phrase puzzles is the BIP39 checksum: the final bits of
a mnemonic are a checksum over the entropy, so only a fraction of word sequences are valid at
all. For a 12-word mnemonic (128 bits of entropy, 4 checksum bits), 1 in 16 sequences is
valid; for 24 words (256 bits, 8 checksum bits), 1 in 256 is valid. Checking the checksum
costs one hash; deriving a full address costs a password-stretching function (PBKDF2 with
2048 rounds) followed by elliptic-curve multiplication, several orders of magnitude more
expensive. Applying the cheap filter before the expensive derivation is the single biggest
lever available on these puzzles: permuting 12 known words is not 12! = 479,001,600
candidates but roughly 479,001,600 / 16 = 29.9 million once the checksum filter is applied
first.

Use this filter only when the puzzle requires a checksum-valid mnemonic. PBKDF2
can derive a seed from an invalid-checksum phrase, and some wallet import paths
accept one. Bitcoin Movie Enigma was solved with exactly such a 24-word phrase;
its old checksum filter rejected the real answer. A public valid-mnemonic test
vector alone does not detect that mistake. For a puzzle built from an extracted
word sequence, retain an unfiltered derivation path and test it explicitly.

Other filters, in rough order of value: compare derived hashes as raw bytes rather than as
encoded strings; check length and character set before deriving anything; only lock a
candidate word or position to a specific value when it is proven by a structural constraint,
never on a hunch, since a wrong lock guarantees the search will never find the answer; when
many candidates share an expensive prefix, compute the prefix once.

Rates I quote are always for one particular derivation on one particular machine, stated as
an order of magnitude rather than a precise promise, for example "on the order of 10^5 to
10^6 derivations per second on a rented GPU for a BIP39-to-address pipeline". Different
derivations cost wildly different amounts (a single SHA-256 versus a 2048-round PBKDF2
followed by curve multiplication), so a rate measured for one puzzle should never be reused
to size another without re-measuring.

## Amount fingerprint

Several escrow addresses were never announced directly by the author; I found them by
matching the exact prize amount stated in the announcement (in sats, ETH, or AR) against a
public balance listing. When an amount is unusual enough (369,369 sats, not a round number),
it acts as a fingerprint that narrows a search for the actual address.

## Funder trace

Once one puzzle in a series is solved, its funding transaction sometimes reveals the same
wallet funding sibling puzzles in the series, even before those siblings are publicly linked
to the same author. Following the funding wallet, not just the announcement text, has
surfaced escrows that were otherwise easy to miss.

## Check on-chain first, always

A press article describing a puzzle as "solved" or "still open" is not chain state. Before
allocating any effort, I check the address directly: the chain does not go stale between
reprints of an old article, and it does not get details wrong. An article's account of an
event should always be checked against the transaction it claims happened.

## Custodial versus permissionless

A prize is only as real as the mechanism that pays it out. An address anyone can verify and
that pays automatically to whoever produces a valid signature is permissionless. A prize that
depends on a person or a platform manually verifying a solution and sending funds by hand is
custodial: the balance you can see is not a guarantee, only a promise. Promised is not
funded. Puzzles in this state are treated differently and usually land in dead ends, not
because the effort of solving them is different but because the payout is not something the
chain alone can confirm.

## Zero-cost actions run immediately

If checking an already-known fact costs nothing (a public announcement window closing, a
free API call, a single command), the action to capture it runs right away rather than being
queued behind lower-priority work. A missed zero-cost window is a pure loss with no offsetting
benefit.

## Read the existing negatives first

Before running anything, I read `analysis/tested.md` for that puzzle. Re-running a search
that has already been logged with its witness and its exhausted range wastes time and compute
for no new information. This file exists specifically so that nobody, including me on a later
day, repeats work that has already produced a certified answer of "no match here".
