# Negatives ledger, in full

All page-password candidates below were checked directly against the live site (a password
either opens the gated page or the site returns its "wrong password" response; there is no
partial credit and no ambiguity in the result). None of them reached the seed-derivation
oracle, since none opened a lock.

I flag a family "uncertified" when I have no known-good candidate for that specific locked
page to prove the guess space was covered as intended (case, spacing, digits). The three
insight locks are unsolved, so by construction no such positive control exists for them yet;
this is a real limitation of these particular negatives, not a formality, and it is why I do
not present them as proof the answer is not in the tested set.

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| West (`wt1jy`): the riddle's named pirates (Blackbeard, Shawn Fanning, Lars Ulrich, Ross Ulbricht, Gottfrid Svartholm, Fredrik Neij) share a single-word connection | about 2,100 candidates cumulative, overwhelmingly lowercase | direct page-password submission | 0 match | uncertified: no known-good candidate exists for this locked page | 2026-07-25 |
| East (`c2ozw`): a diving/near-death/pop-culture term answers "is this the end?" | about 2,030 candidates cumulative, including 943 recorded in a single late pass | direct page-password submission | 0 match | uncertified: no known-good candidate exists for this locked page | 2026-07-25 |
| South (`b3vye`): the sixth Gilligan's Island castaway (the Professor) named by the full canon (radio pilot, opening/closing credits, reunion films, animated spinoffs, comics) | about 775 candidates cumulative, Title Case single tokens | direct page-password submission | 0 match | uncertified: no known-good candidate exists for this locked page; the show's enumerable canon is exhausted, so a hit here is more likely an off-canon wordplay on the author's own pun ("having fun with the url, I loved this show as a kid") than a direct character name | 2026-07-25 |
| A single puzzle-wide password rule (assumed all lowercase) | 2 known passwords retested in 3 case variants each | direct page-password submission on already-open gates | refuted: `Gilligan` and `Ginger` (Title Case) succeed, `gilligan`/`GILLIGAN` and `ginger`/`GINGER` both fail | yes: both known-good passwords reproduced their real accept/reject outcome | 2026-07-25 |
| Cover art trailer-byte channel (word 1) | 1,585 cover images scanned across Bandcamp, Apple Music, Deezer, ToneDen, and the site's own assets | byte-level scan for data appended after the image's EOF marker, the exact channel used by the solved Hunt #1 cover | 0 match on any Hunt #2 image; the technique itself reproduces on the known Hunt #1 cover | yes: the same scan finds the real trailer on the Hunt #1 cover used as a positive control | 2026-07-14 |
| Audio steganography on the public Glimmer master (Morse, reversed playback, LSB, spectrogram) | 1 audio file (48kHz/24-bit FLAC), 4 techniques | direct signal analysis | 0 match; audio matches the official master with no alternate mix found anywhere | not applicable (no known-good alternate-mix vector exists to test the harness against) | 2026-07-10 |
| Instagram captions and post dates as page-password candidates | 80 posts plus story highlights | direct page-password submission of caption puns and dates | 0 match on any of the 3 locks | uncertified: same reason as the 3 locks above | 2026-07-18 |
| North branch (`mwfaz` and the whale-themed pages) carries hidden words | full content of every page on the branch | direct read of page text, images, and buttons | confirmed 0 of 12 words; the branch ends on a static "coming soon" page | not applicable (a direct content read, not a guess) | 2026-07-20 |
| Contributed (@Neopram, issue #48): 15 South candidates in Title Case (`AndTheRest`, `TheRest`, `Rest`, `Andtherest`, `Roy`, `Professor`, `Hinkley`, `RoyHinkley`, `TheProfessor`, `professor`, `PROFESSOR`, `Proffesor`, `Profesor`, `MaryAnn`, `Willy`), 8 East in lowercase (`resurface`, `no`, `nottheend`, `whiteshores`, `anotherpath`, `death`, `wakeup`, `hallucinations`), 8 West in lowercase (`roberts`, `dreadpirateroberts`, `piracy`, `teach`, `royle`, `smithlylemoore`, `metallica`, `napster`) | 31 candidates | direct page-password submission | 0 match | contributed: the method opened `/name-1` to `/name5` with the known-good passwords; no known-good candidate exists for the 3 locks | 2026-10-19 |
| Contributed (@Neopram, issue #48): the `/latitude` page password as a rendering of the EXIF latitude | about 40 variants (`27`, `27.132481`, `270756`, `27075693` and others) | direct page-password submission | 0 match; the accepted format is not recorded in this folder | contributed, uncertified | 2026-10-19 |

Cumulative candidate count across the 3 open locks: about 5,000, 0 hits, all uncertified in
the sense above. The site's gated-page mechanism itself is server-side (a real browser cannot
bypass it by reading the page body before entering the password), which I confirmed directly
rather than assumed.
