# Guntis Vitolins: 10 ETH Challenge (8.61254155425694462 ETH, [OPEN])

Guntis Vitolins, managing director of mining-hardware retailer mineshop.eu,
published a 10 ETH challenge on 2020-02-12: a YouTube video and a blog post,
each hiding 6 words of a 12-word BIP39 seed phrase for a wallet he funded that
same day. Six years later the wallet is still not empty; the author himself
has withdrawn from it 7 times since 2021, most recently in June 2024, leaving
8.61254155425694462 ETH. Three of the 12 words are confirmed and placed
(positions 1, 5 and 12), 2 more are confirmed as list members with unknown
positions, and every combination tried against the confirmed word pool has
failed. The blocking gap, found only in August 2026, is that part of the word
pool hides in page metadata (HTML tags), not in the visible text.

## At a glance

| | |
|---|---|
| Author | Guntis Vitolins, [#GuntisVitolins on YouTube](https://www.youtube.com/channel/UCkYCnjVcFJDN6Cp_uP0pv_A), [mineshop.eu](https://mineshop.eu/) |
| Published | 2020-02-12, [YouTube video](https://www.youtube.com/watch?v=w4mpiuBP_aY) and [mineshop.eu blog post](https://mineshop.eu/2020/02/12/crypto-pumping-hardcore-research-portfolio-update-how-are-we-doing/) |
| Prize | 8.61254155425694462 ETH (about $16,192 at ETH = $1,880, 2026-08-16) |
| Chain | ethereum |
| Escrow | `0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF` ([explorer](https://etherscan.io/address/0x9C2F44EFAd0c1E852a09dF9939e6DaF061140CaF)) |
| Last on-chain check | 2026-08-16: balance 8.61254155425694462 ETH, nonce 7 (see "Established facts" for what the nonce means here) |
| Status | OPEN |
| Puzzle type | bip39-seed, word-selection, video-series |
| Target format | 12-word BIP39 English mnemonic, no passphrase, MetaMask default path `m/44'/60'/0'/0/0` |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against the public canonical BIP-0039 test vector) |
| What remains | the full 12-word list; 3 positions and 2 more list members are confirmed, but the word pool the remaining candidates are drawn from is not yet complete (part of it hides in page metadata, confirmed only in August 2026) |
| Series | none |

## The puzzle as published

Guntis Vitolins posted "10 ETH challenge | Ethereum Parabolic | Bitcoin
generator portfolio update !?" on YouTube and a companion blog post on
mineshop.eu, both on 2020-02-12, the same day he funded the target wallet with
10 ETH from an exchange hot wallet. He states the challenge needs the complete
12-word list, submitted in the right order, to a reference wallet tool (he
confirms this is MetaMask, with no special import setting), and that 6 words
hide in the video and 6 in the blog post.

The video description carries 2 sentences with no connection to its finance
topic:

> "Don't expect anything easy there will be dark fog on the lake."

The same sentence continues with a short assurance that the challenge can, in
fact, be solved.

> "Do you think its more likely for parrot can sing a song then for a goat to
> whistle?"

The blog post carries 3 more, mid-paragraph, also unrelated to its subject:

> "Round dutch cattle is living in the forest and eating wood."

> "Only because there is a lot of healthy fiber."

> "Hunter like the rib roast dinner fresh."

That these 5 sentences are deliberately inserted, not incidental, is
confirmed statistically: their language departs from the author's other posts
at z = 3.71 against a control corpus of his 4 other blog entries. The 5 planted
sentences, the video title and the post's tags are confirmed unchanged since
2020, checked against a 2020-05-28 web archive capture. That claim is
deliberately narrower than "both pages are unchanged byte for byte", which is
not true: the video description's contact address was later edited from an
"info@" form to a "guntis@" form, and its rules block accreted more text as
each new hint was published. Those edits sit outside the planted sentences, but
anyone diffing the live page against the archive should expect to see them and
should not read them as tampering with the payload.

Across roughly 40 of his later video descriptions, the author published 5
hints, the last 2 of which are spoken rather than written: the final word is a
tropical bird; word 1 names the Netherlands; word 5 is made of condensed
water droplets; a fourth hint, spoken at 15:26 in
[youtube.com/watch?v=03wXiMczCXk](https://www.youtube.com/watch?v=03wXiMczCXk),
resolves to "fiber"; a fifth, spoken and spelled letter by letter at 17:28 in
[youtube.com/watch?v=ZjBJKooVmuE](https://www.youtube.com/watch?v=ZjBJKooVmuE),
gives "fork" directly. Full quotes and links: [clues/author-posts.md](clues/author-posts.md).

![The 12-word seed, colored by what is confirmed at each position](images/01-seed-slot-grid.svg)
*Figure 1. Confirmed positions, confirmed-but-unplaced words, and unknowns (source: data/seed-slots.json, script tools/fig_slots.py), 2026-08-16.*

## What is understood

### Mechanism

The 12 words go directly into a standard BIP39 English mnemonic, no
passphrase, MetaMask's default derivation path `m/44'/60'/0'/0/0`. A correct
12-word list must pass the BIP39 checksum (encoded in the choice of the 12th
word) before it can even be tested: for any fixed first 11 words, only 1 in 16
possible last words passes, so anchoring the last word first is the single
most valuable constraint.

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "word1 word2 word3 ... word12"
python3 tools/oracle.py --stdin
```

Given a 12-word candidate, the oracle validates the BIP39 checksum, derives
the MetaMask default Ethereum address, and compares it case-insensitively
against the target. `MATCH <address>` on a hit; otherwise `NO MATCH`,
`INVALID CHECKSUM`, or `INVALID WORD`, exit code 0 or 1.

### Certified against

`tools/oracle.py --selftest` reproduces the public, canonical BIP-0039 test
vector: the mnemonic "abandon" repeated 11 times plus "about" derives address
`0x9858effd232b4033e47d90003d41ec34ecaeda94` exactly at
`m/44'/60'/0'/0/0`, and a 1-word-different neighbor ("abandon" x12) correctly
fails the checksum rather than silently deriving something else. The
selftest also confirms the checksum acceptance rate over the full 2048-word
English wordlist is exactly 1 in 16, as the format requires. Reproduced
2026-08-16.

### Established facts

1. Position 1 is `dutch`: of the BIP39 dictionary's 4 words that could match
   hint 2 ("designates the Netherlands"), only `dutch` appears anywhere in
   the source texts.
2. The last position is `parrot`: of 14 BIP39 dictionary words naming birds,
   only `parrot` is tropical, matching hint 1.
3. Position 5 is `fog`. Narrowing hint 3 from "related to water" to its actual
   wording, condensed water droplets, leaves exactly 3 BIP39 dictionary words:
   `fog`, `cloud` and `vapor`. `vapor` is the gas phase, not condensed
   droplets, which leaves `fog` and `cloud`, and of those 2 only `fog` appears
   in any recovered 2020 written surface, at index 25 of the video description.
   `lake` appears there too but a lake is not made of condensed droplets. The
   author's own reply in a comment thread, that a hint may gloss a word while
   the challenge text carries the exact one, points the same way. Treat this as
   settled with 1 reservation: `cloud` becomes live again if it turns out to be
   legible in the video image, which nobody has read yet. See "Open leads,
   ranked", lead 1.
4. `fiber` and `fork` are confirmed list members with unconfirmed positions,
   from hints 4 and 5, each verified against both YouTube's official captions
   and an independent local transcription.
5. `fork` is written in the blog post's own HTML metadata: the archived 2020
   page carries the tags "ethereum fork" and "round" in its footer and in
   `article:tag` meta elements; a tag named "round" exists on no other post on
   the site. The live, current version of the page no longer carries these
   tags, since a later site redesign removed them; this was not found until
   2026-08-15, and for years before that, exhaustive searches of the visible
   text (64 files, including OCR of 216 images) found no occurrence of `fork`
   anywhere, which was mistakenly treated as ruling `fork` out rather than as
   a sign the search needed to include metadata.
6. The wallet was funded with exactly 10 ETH on 2020-02-12 from an exchange
   hot wallet, and the author has since sent 7 outgoing transactions from it,
   between 2021-05 and 2024-06-04, totaling approximately 1.377 ETH, leaving
   the balance checked above. He still holds and periodically uses this
   private key; a future balance change would not by itself mean anyone
   solved the puzzle.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| Full words from the 5 planted sentences only, 6/6 partition, confirmed anchors | 150,822,000 derivations (of 2.41 billion enumerated) | BIP39 checksum then address compare | 0 match | yes: 4 planted candidates recovered | 2026-08-15 |
| Same pool, `fork` read as a paraphrase rather than a literal word | 79,391,851 derivations | same | 0 match | yes: 4/4 | 2026-08-15 |
| Pool extended with confirmed page and video metadata words, 6/6 partition | 3,384,362,972 derivations | same | 0 match | yes: 6/6 | 2026-08-15 |
| Same extended pool, the 6/6 partition dropped | 1,225,433,776 derivations | same | 0 match | yes: 6/6 | 2026-08-15 |
| Post fixed to exactly 2 of its 3 planted sentences, wide video-side pool | 1,157,541,475 derivations | same | 0 match | yes: 6/6 | 2026-08-15 |
| Extended pool plus natural grammatical inflections | 10,752,000,393 derivations | same | 0 match | yes: 6/6 | 2026-08-15 |
| Text reading order, contiguous halves, interleavings, full internal orderings | approximately 5.5 million candidates | same | 0 match | not individually recorded per row | before 2026-08-15 |
| Likelihood-ratio closure of the 6-plus-6 word budget | 91,865 candidates | same | 0 match | not recorded | before 2026-08-15 |
| Complete reading-order model over the full recovered 2020 text and metadata, 3 anchors fixed, `fork` free | 10,484,919 derivations (of 167,688,000 arrangements, matching a closed form) | closed-form count, then checksum, then address compare | 0 match | yes: 1,062 planted and recovered, 0 disagreements between 2 engines | 2026-08-20 |
| The same reading-order model extended to substrings of longer words | 582,725 derivations (of 9,334,500 arrangements) | same | 0 match | yes | 2026-08-20 |
| Pool extended with short connecting words from the planted texts, fog-only, `fiber`+`fork` required | 18,657,475,200 derivations (of 298.5 billion enumerated) | checksum-aware CUDA engine (`engines/`) on a rented L40S, per-chunk witness protocol | 0 match | yes: 2 planted candidates recovered in every one of 412 chunks | 2026-08-23 |

Cumulative: approximately 35.4 billion candidate derivations tested across
the metadata-era sweeps, all negative and individually witnessed, plus
roughly 5.6 million candidates from earlier, smaller sweeps, plus the 11.07
million derivations of the 2 reading-order sweeps above. Full method notes are
in `analysis/tested.md`.

The reading-order sweep matters out of proportion to its size. It is the first
sweep here whose space is stated as a closed form and then enumerated to that
exact count, so its coverage claim is checkable. Reading order was also the
assumption that made this challenge searchable at all: dropping it, over the
same pool and the same 3 anchors, gives `C(38,4) * C(82,3) * 9!` =
2.3722x10^15 arrangements and 1.4826x10^14 derivations, which is 5.9 years on 1
GPU at 792,000 derivations/second. That assumption is now closed and negative
over 100 percent of its space, which moves the binding constraint from search to
word identification and re-orders the leads below.

## Open leads, ranked

1. **Read the text shown on screen in the challenge video** (about an hour, no
   compute). The author names on-screen text as a channel in his own spoken
   rules, at 5:22 to 5:38 of the challenge video: the words "could be you know
   written in the video on the screen so read carefully". Every sweep in
   `analysis/tested.md` draws its pool from the description, title, tags and
   post body; not 1 frame of the video image has been read. The video shows a
   portfolio table, and 10 coin names visible or audible in that segment are
   BIP39 dictionary words (`atom`, `link`, `dash`, `cash`, `icon`, `wave`,
   `gas`, `ocean`, `fetch`, `ripple`), none of which appears in any recovered
   written surface. Confirmed by a legible dictionary word absent from the known
   pool; killed by a complete frame read yielding nothing new, which unlike a
   prose re-read is a real exhaustion point.
2. **KILLED 2026-08-23: extend the word pool with connecting words.** Every
   sweep before this drew non-anchor words from full content words; short
   connecting words from the same sentences ("there", "will", "also", "only",
   "because", "like", and similar) were not included. Executed as sweep C1
   (`analysis/tested.md`): 18,657,475,200 checksum-valid derivations, fog-only,
   per-chunk witness protocol, 0 match. This lead is closed.
3. **Re-check the already-enumerated survivors on other derivation paths**
   (about 4 hours on 2 CPU cores, seconds on a GPU). Every sweep here derives
   only `m/44'/60'/0'/0/0`. If the escrow is the second account of the same
   wallet, every negative in this folder is a negative about the wrong address.
   Re-checking `m/44'/60'/0'/0/1`, `m/44'/60'/0'/0/2`, `m/44'/60'/1'/0/0` and
   `m/44'/60'/2'/0/0` costs about 28 percent of the original derivation work,
   because the seed stretch is already done and only the child derivation
   repeats. Killed by 0 match across all 4, which upgrades every existing
   negative here from "negative at the default path" to "negative across the
   plausible path family". Best value experiment currently available.
4. **Substrings of longer words** (about a day on 1 rented GPU). Demoted, with
   a correction. This lead used to credit the author with an example of a list
   word nested inside its own negation. Reading the thread directly shows that
   example came from the reader asking the question; the author's own example is
   "usa" for "united states", he offers it about hints, and he adds that the
   challenge text "wikk have corect word". So the mechanism is a reader's
   hypothesis the author did not contradict, not an author-stated rule. All 5
   confirmed list words are whole tokens, which is weak further evidence
   against it. About 2.78x10^11 derivations; the reading-order corner is
   already swept.

Full notes: [analysis/leads.md](analysis/leads.md).

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | the 5 planted sentences, the 5 hints, the author's comment replies quoted verbatim, and his spoken statement of the channels, with dates and links |
| `data/seed-slots.json` | the 12-position grid state, for the seed slot figure |
| `data/reading-order-pool.json` | the derived reading-order index the sweep script consumes: which dictionary words appear in which source range, in written order |
| `analysis/tested.md` | the complete negatives ledger |
| `analysis/leads.md` | full notes behind the 4 ranked leads |
| `images/01-seed-slot-grid.svg` | the 12-word seed grid, confirmed vs unknown |
| `tools/oracle.py` | candidate checker, certified against the canonical BIP-0039 vector |
| `tools/fig_slots.py` | generates images/01-seed-slot-grid.svg from data/seed-slots.json |
| `tools/sweep_reading_order.py` | the reading-order sweep of `analysis/tested.md`; `--size` prints the closed form, `--selftest` plants and recovers a witness, `--run` is resumable |

## Sources

- Challenge video, YouTube, 2020-02-12: https://www.youtube.com/watch?v=w4mpiuBP_aY
- Challenge blog post, mineshop.eu, 2020-02-12: https://mineshop.eu/2020/02/12/crypto-pumping-hardcore-research-portfolio-update-how-are-we-doing/
- Blog post, archived (tags visible in footer), Wayback Machine, 2020-05-28: https://web.archive.org/web/20200528000000*/mineshop.eu/2020/02/12/crypto-pumping-hardcore-research-portfolio-update-how-are-we-doing/
- Challenge video, spoken statement of the channels including on-screen text, at 5:22 to 5:38: https://www.youtube.com/watch?v=w4mpiuBP_aY
- Hint 4 video: https://www.youtube.com/watch?v=03wXiMczCXk
- Hint 5 video: https://www.youtube.com/watch?v=ZjBJKooVmuE
- #GuntisVitolins, YouTube channel: https://www.youtube.com/channel/UCkYCnjVcFJDN6Cp_uP0pv_A

Credits: @cjmcdaniel (issue #18): on-screen and spoken word channels of the challenge video read, 219 new dictionary words.
