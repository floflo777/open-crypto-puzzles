# Mechanism, in full

## The site

The puzzle lives on an approximately 70-page Wix site, almost all of it password-protected
page by page. The entry page (`/treasure-hunt`) carries an image whose EXIF metadata encodes
GPS coordinates; entering the latitude and then the longitude as consecutive page passwords
opens a compass page, which displays four branch passwords in clear text: `north64`,
`south64`, `east64`, and `west64`. From there the site forks into four branches.

Everything up to and including the branch fork is solved: I hold every password from the
entry page through the compass page and through every page each branch passes before its
final locked gate.

## The four branches

North is a decorative dead end: its chain of pages (ending in a "coming soon" page) carries
none of the 12 words. I confirmed this by reading the full content of every page on the
branch; no word-bearing artifact of any kind is present.

West, East, and South each end in one password-gated page I have not opened. I call these
the three insight locks. Opening any of them requires guessing a short, unenumerable string
that answers the riddle text quoted in [clues/author-posts.md](../clues/author-posts.md), not
decoding anything hidden in an image or audio file: no steganographic payload was found on
any page along the way (see analysis/tested.md).

The South branch is a chain of six pages named after five Gilligan's Island castaways in
sequence (Gilligan, the Skipper, Thurston Howell III, Lovey Howell, Ginger), each password a
single Title Case name, before ending on a sixth page titled "Name 6" that asks for the
sixth castaway, the Professor. This last page is the one I have not opened; solving it opens
the entire South branch's downstream chain (a further set of "escape the island" pages) in
one step, since password to `b3vye` is also the key to everything after it.

The exact South passwords, contributed by @Neopram (issue #48) and taken as given: `/name-1`
`Gilligan`, `/name2` `Jonas`, `/name3` `Thurston`, `/name4` `Lovey`, `/name5` `Ginger`.
`Skipper` does not open `/name2` and `Eunice` does not open `/name4`: the author uses the
character's first or common name. By that pattern Name 6 should be `Roy` or `Professor`, and
neither opens it.

## Direct URLs of the three locks

The site's route table is embedded in the page HTML (`pagesMap`, 78 pages on 2026-11-25), so
each lock can be reached without walking the chain. Reported by @Neopram (issue #48); I
checked the three entries below against the live page.

| Lock | Page id | URL slug | Page title |
|---|---|---|---|
| West | `wt1jy` | `/message` | a message |
| East | `c2ozw` | `/take-a-big-breath` | resurface |
| South | `b3vye` | `/havingfunwiththeurl-ilovedthisshowasakid-sosomuch` | Name 6 |

The titles and slugs are the author's own and may hint at the answers. The table also lists
`/ross-u` (title "the library"), `/key-checker` and `/end-of-treasure-hunt`. The entry image's
EXIF GPS block reads 27 07 56.93 N, 73 05 11.57 W, date stamp 2077:07:29, time 11:59:19.

## Case sensitivity and format, established by direct test

Passwords on this site are case sensitive. I confirmed this on two already-open gates on the
South chain: the page password `Gilligan` succeeds where `gilligan` and `GILLIGAN` both fail,
and `Ginger` succeeds where `ginger` and `GINGER` both fail. Combined with the passwords
already known for every other open gate, the format of the three remaining locks is:

- South (`b3vye`): Title Case, a single token, no digits, no spaces (matches the naming
  pattern of the five prior South pages).
- West (`wt1jy`) and East (`c2ozw`): lowercase, a single token with no spaces (matches every
  other open West/East page password, e.g. `albatross`, `semaphore`, `20000leagues`).

No password anywhere on the site I have opened carries a numeric suffix that is not directly
derivable from the page's own content (a number visible in an image on that same page); no
guess should add an arbitrary digit string.

## The 12-word carrier channels

The site's predecessor, "Born to Be Wild" (2021, Apollo/moon theme), was solved and swept by
an unidentified third party; I used its known solution purely as a template for how this
author hides seed words, not as part of the live puzzle. Its seed was
`fortune all man kind one giant step into digital tomorrow virtual moon` with passphrase
`supernova`, assembled from 7 carrier channels. Mapping the same 7 channels onto this hunt:

| # | words | Hunt #1 channel | Hunt #2 equivalent | status here |
|---|---|---|---|---|
| 1 | word 1 | bytes appended after the cover image's EOF marker | Glimmer cover art | refuted: every Hunt #2 cover image I found (Bandcamp, Apple Music, Deezer, ToneDen, and the site's own PNG) is clean; a collage image that looked like a second Hunt #2 cover turned out to be a Hunt #1 teaser predating this hunt |
| 2-4 | words 2-4 | museum gold frames pictured in the book/site | not located outside a gated page | not found on any open page |
| 5-7 | words 5-7 | a forced cultural quotation naming a BIP39 word | pop-culture reference on the East branch | behind the locked `c2ozw` gate |
| 8-9 | words 8-9 | Morse code in an alternate audio mix | West branch "computer" theme or a hypothetical alternate mix | refuted for the public master: the only public 48kHz/24-bit Glimmer audio matches its own official master with no Morse signal; no alternate mix has been found distributed anywhere |
| 10 | word 10 | binary encoding | not located | the only binary string found anywhere on the site is an EXIF comment reading "nope lol", which does not decode to anything |
| 11-12 | words 11-12 | a "future song" ticket prop | inherited endgame page, already open | present, but this is Hunt #1's own endgame carried over, already read, and not new information |
| passphrase | "in the song" | the closing track's title | the Glimmer track title or lyric | not testable without the 12 words |

The practical conclusion: every carrier channel that is reachable without solving one of the
three insight locks has been checked and is either empty (refuted) or inherited scaffolding
from Hunt #1 that carries no new word. All 12 words are behind West, East, and South.
