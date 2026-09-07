# Open leads, full notes

Ranked summary is in the README. This file has the reasoning behind the ranking.

I harvested the author's public X timeline covering the Season 2 clue window
(2025-05-19 launch through the author's own "last clue from me" on 2025-06-15,
plus the remaining promotional posts that month). On 2025-06-05 the author posted
a screenshot of the hosting dashboard's "Enable Attack Challenge Mode" button and
said they were turning it on because dictionary probing of page names was running
up the request bill. A datacenter curl and a headed browser on this host both
failed that checkpoint (Code 11). A later fetch on 2026-08-27 did get through:
the eleven listed games, the extras, `home.html`, `wordorder.html`, `new.html`,
`check.html`, and the Season 4 hint-mapping page all returned HTTP 200. The
hashed Game 12 URL, whose preimage is still the sentence spelled by the eleven
page names, now returns Vercel `404 NOT_FOUND`. 0 of 12 seed words are confirmed
by the oracle. Three games now have a single-list-word reading from a closed
mechanic; those are working readings, not a MATCH.

I am quoting visible strings and describing images. City names that are not on
the English BIP39 list are clues, not seeds. Image captions that merely
neighbour a list word are not seeds either.

## Working readings, 2026-08-27 (not a MATCH)

Each line is one game, one list word, one mechanic. None of these has been
run as a 12-word set. A reading is not a solution.

1. **Game 9 = `can`**. Title `1211920` groups as 12, 1, 19, 20 = LAST, which
   is the Game 2 page-name preimage and is the witness that this page uses
   A1Z26 with mixed 1-digit and 2-digit groups. Body `3114` has three such
   partitions; only 3, 1, 14 is an English BIP39 word: `can`. Scrabble maps
   here. N was 3 partitions; D is instant.
2. **Game 11 = `airport`**. Title `44 . C`. Season 4 says "standard" applies
   in most games; Game 7's title names that standard as zero-based indexing.
   English list index 44 (0-based) is `airport`. Index 43 (1-based 44) is
   `air`. The leftover `. C` is not used. N = 2; I am ranking the 0-based
   reading first.
3. **Game 7 = `nice`**. The X clue "If I were a city I would be ?" maps here.
   The seed must be an English BIP39 word. The English list contains two
   ordinary city names: `nice` and `buffalo`. Game 7 is the French city
   page (Paris and Dakar on the couplets, French-twice maps here). `nice`
   is the French one. Paris, Dakar, and the IBIZA acrostic on Game 10 are
   city-clues, not list words. The author called Game 7 too vague; a riddle
   whose answer is a city-word fits that. N = 2.

Game 4's sentence points at `simple` and Game 3's `1881` as a 0-based index
points at `twenty`. Both have leftovers (the hidden E; the letters SW), so
I am not putting them in the list above. Game 2's yellow discriminator hits
two thumbnails (slot banana; car's yellow UK plate) and I will not pick
one.

Game 2's four thumbnails neighbour several list words. I am not taking
`seven`, `bar`, `slot`, `clock`, `time`, or `car` from a caption. The yellow
discriminator is a real mechanic and is recorded under Game 2; it still hits
two pictures, so it is not a fourth working reading yet.

## 1. Read the twelve game pages (done for text; Game 12 is live at the no-spaces hash)

The derivation is certified and the page-naming scheme is already broken. On
2026-08-27 I fetched every listed hashed URL, the four Game 10 text pages, both
50-letter extras, the Game 1 `.psd` link, `wordorder.html`, `new.html`,
`check.html`, and the Season 4 hint page. Source HTML (F12) is in the notes
below. What remains of this lead is visual work the HTML does not settle:
Photopea on `/image1.psd`, Game 2's two yellow thumbnails, Game 3's grids,
Game 5's stage-2 block, Game 8, Game 10's four-city cluster, and Game 12's audio
(the Drive link is on the live page, see the Game 12 note below).

What would confirm it: a 12-word MATCH on `tools/oracle.py`.
What would kill it: an on-chain sweep, or the author taking the season down.
Cost: insight against the transcriptions below; Game 12 still needs the audio.

Known hashed URLs, in the order the 11 listed-game preimages spell, with game 12
named by the whole sentence. Each path is
`https://findtheprivatekeys2.vercel.app/<hex>.html`.

| Game | Page-name preimage | sha256 |
|---|---|---|
| 1 | the | `b9776d7ddf459c9ad5b0e1d6ac61e27befb5e99fd62446677600d7cacef544d0` |
| 2 | last | `3547cb112ac4489af2310c0626cdba6f3097a2ad5a3b42ddd3b59c76c7a079a3` |
| 3 | game | `6ca5cab77e702c787b4c14b3d3bf26bad43da606be6eed04ab0b9720120ae081` |
| 4 | has | `9150c74c5f92d51a92857f4b9678105ba5a676d308339a353b20bd38cd669ce7` |
| 5 | for | `10c22bcf4c768b515be4e94bcafc71bf3e8fb5f70b2584bcc8c7533217f2e7f9` |
| 6 | url | `28e5ebabd9d8f6e237df63da2b503785093f0229241bc7021198f63c43b93269` |
| 7 | this | `1eb79602411ef02cf6fe117897015fff89f80face4eccd50425c45149b148408` |
| 8 | sentence | `821119d79af8b9fcf86d782863d55861708cc4040673f905f9e3b616cfb71199` |
| 9 | that | `8e7fc0236af43df9340685fc16f1efe36543cc1707051220a103ad99cf69a2df` |
| 10 | is | `fa51fd49abf67705d6a35d18218c115ff5633aec1f9ebfdc9d5d4956416f57f6` |
| 11 | hashed | `1a06df824ed741b53c785079a6347f00eec5af82f9850775409ca69dff4068a6` |
| 12 | the last game has for url this sentence that is hashed | `2d80326b034b1aa616625ecb0febf8e9f58b125c5c43bc65f5d8ab6bd6cc1d36` |

Extra hosted paths transcribed by @N4Khjir from the live site in May 2025, still
behind the same checkpoint. These are not `sha256` hex names.

| Path | What N4 reported | Tweet |
|---|---|---|
| `/image1.psd` | Photoshop file linked from Game 1 | https://x.com/N4Khjir/status/1927619197695082629 |
| `/gdjztvzuojmmsmuwrsudjhzdvvlkftfehnxxkbpilscjfljyyg.html` | second extra Game 1 page | https://x.com/N4Khjir/status/1927619197695082629 |
| `/hdvpvgyqxzplxefvngacfsdsljxajfhtweksvlkihugghszomf.html` | Game 6 page titled "Simplicity Must Be Rewarded I" | https://x.com/N4Khjir/status/1929061582220276150 |

Wayback has none of these three. A browser PSD editor is still the reading the
author gave for `/image1.psd`. I word-broke both 50-letter names against the
English BIP39 list: 0 reconstructions of any length (`analysis/tested.md`).
They are not the order-helper named by concatenating the 12 seed words. Game 10
adds four more 50-letter text pages, listed in the live notes below.

## Live pages, 2026-08-27

Quoted strings are the site's. I am not claiming a seed word.

### Home, helpers, Season 4

`home.html` lists games 1-11 and Word order. It does not list Game 12. The
footer has `new.html` ("New (2/3)") and `check.html`. `wordorder.html` says to
visit `https://findtheprivatekeys2.vercel.app/(words in game order without
spaces).html`.

`new.html` and the top of `check.html` add an author offer: if a player using
the paid word check has at least 8 of 12 words correct, each on the right game,
the author will share the missing four. That does not change the on-chain
oracle, which still needs a full valid mnemonic. `check.html` is optional, asks
for $2 to the escrow plus an email or X handle, and says no hints live on that
page. Contact named there: `alexandredescartes77@gmail.com` and `@ftpkgame`.

The Season 4 bonus page maps the 2025 X clues to Season 2 game numbers:

| Clue | Games |
|---|---|
| Photopea | 1 |
| F12 | 1, 3, 4, 6, 7, 11, 12 |
| History | 7 |
| Library image | 2 |
| Rabbit wallet image | 11 |
| Optional hint bad vibes | 5 |
| Red image | 2 |
| World map image | 3 |
| SHA256 | 12 |
| Tetris piece | 5 |
| 10 hidden cities | 3, 7, 10 |
| Scrabble board | 9 |
| CCZA | 1 |
| History in Arabic | 7 |
| Colorful painter | 6 |
| If I were a city I would be | 7 |
| Work of art | 11 |
| 4 cities 1 word | 3, 10 |
| Bip | 11 |
| Microphone | 7 |
| Standard (broad sense) | most games |
| French twice | 7, 10 |
| Knight | 1, 5 |

Extra line, quoted: game number 7 is the weakest, too vague and poorly designed,
and a good candidate if one word had to be left unconstrained.

### Game 1

`lang=fr`. Cipher block matches N4. Invisible 1x1 download link to
`/image1.psd`. Hidden 100x100 hit-target, bottom right, to
`/gdjztvzuojmmsmuwrsudjhzdvvlkftfehnxxkbpilscjfljyyg.html`, whose body is only
`image2.bmp`. CSS defines `.background-image` with no `url()`, so the old
`image2.jpg` layer is gone (author: development error). Photopea on the PSD is
still the unread step. CCZA and knight also map here.

### Game 2

Solid red page, four 150px thumbnails in a 2x2 grid:

- slot machine: 7, BAR, cherry, plum, yellow banana
- music: 4/4, quarter = 120, a rest, then a held note
- analog clock, hands at about 10 and 2 (the usual catalogue pose)
- light-blue Ford GT, UK yellow rear plate `SXC`, police lights on

The author's uniform-red PNG and "a little yellow in all this red" both map
here. Yellow pixels sit on two thumbnails: the banana, and the car plate.
Library image also maps here. Not a working reading until one of those two
wins.

### Game 3

Three 4x4 addition grids (fifth row and column are sums) on a background image
`image7.jfif`: a low sun on a horizon, coloured streaks, a small standing
figure. Caption `SW 1881`. The middle grid has an empty CSS `::before` at
`top: 39.57px; left: 107.53px`. Unique fill of the blanks from the sums:

```
4 20 7 8     19 14 5 3     6 4 15 12
20 5 1 17    9 12 7 26     14 17 26 32
3 12 11 3    10 13 5 8     18 12 25 13
9 19 4 18    21 17 5 4     7 19 8 9
```

World map, F12, 10 hidden cities, and "4 cities 1 word" all map here. `SW 1881`
is also the catalog name of an 1881 "Map of the Southwest" (Texas State
Archives Map 1592) and the flight code WN1881. I have not taken either as the
word.

### Game 4

No photographs in the current HTML (N4's two photos are gone). Body:
`simplicity must be rewarded` plus a black-on-black `<span class="hidden-letter">E</span>`
that appears when selected. F12 maps here.

### Game 5

Instruction: find the 13-digit number, then visit
`/?????????????.html`. Thirteen rows of 25 digits (325 digits, factors
1, 5, 13, 25, 65, 325), then a lone `Z`. Tetris and "optional hint bad vibes"
and knight map here. N4 wrote `Z = 2 ?`. Five matrix readings of this grid
(both main diagonals of the 13x25 layout, both of the 25x13 layout, and column
0 of 13x25) all return Vercel 404 (`analysis/tested.md`). The reading that works is
the visual diagonal of the block as rendered in monospace (25 characters are about
240 px wide and 13 lines about 478 px tall, so the corner-to-corner line crosses row
i at column 2i): `5509589357423`. That page returned 200 on 2026-07-26 and
@CyberCalculus reported it live again on 2026-09-07 (issue #23); the 2026-08-27
"not there now" note was wrong because that batch never probed this number. The
stage-2 page repeats the "find the 13-digit number below" wording, carries a hidden
`simplicity must be rewarded C`, and shows this 12x12 block:

```
123456789013
453219876540
950110148630
084002017891
370123456789
002345678912
606015100003
072345678907
060123456781
303005007292
046000001126
978030456783
```

Its visual diagonal is only 12 digits (`150025176223`). That string, its reverse,
the anti-diagonal and reverse, all 12 columns, the row sums (`4048777668667`),
column sums (`5482599826360`), their sum, and 13-digit wrap variants all 404 on
2026-07-26. Rows 0, 4, 5, 7, 8 and 11 hold ascending `123456789` runs at varying
offsets and row 1 a descending run, which reads as camouflage; rows 2, 3, 6, 9 and
10 are zero-heavy. Zero/non-zero bitmaps draw no glyph. Hidden letters collected so
far across chain pages: E (Game 4), I (Game 6 hub), T (Game 12), C (Game 5 stage 2).

### Game 6

Fake events site branded as a French-looking company name, hero in `#c90a64`,
further CSS variables `#660a00`, `#660000`, `#650ac8`, `#640000`. Contact block
is empty (author removed a fake email; the empty field is part of the game).
Nav link to `/hdvpvgyqxzplxefvngacfsdsljxajfhtweksvlkihugghszomf.html`, title
`Simplicity Must Be Rewarded I`. Colorful painter maps here.

### Game 7

Title `Zero-based indexing`. Visible couplets:

```
With ifs, we put Paris in a bottle
Directed toward gold, my bootlegs will be adorned

With ifs, we put Dakar in a can
Decorated by gold will be marked my mock-ups
```

Hidden `<h1 class="hidden">Dyor</h1>`. History, Arabic history, "If I were a
city I would be", microphone, French-twice, and 10 hidden cities all map here.
Paris and Dakar are city-clues, not list words. Working reading: `nice` (see
the list at the top). This is the page the author called the weakest.

### Game 8

`lang=fr`. Body is the five-character string `A9759`. No title. No other
markup.

### Game 9

Title `1211920`, body `3114`, `lang=fr`, huge type. Scrabble maps here. As a
single BIP39 index both numbers are out of range. Working reading: `can` (see
the list at the top). The title grouping 12, 1, 19, 20 is the witness.

### Game 10

`lang=fr`. Four buttons, Text 1 to Text 4. French-twice, 10 hidden cities, and
"4 cities 1 word" map here. The two sub-poem acrostics already fail
(`analysis/tested.md`); there are now four texts, not two.

- Text 1: nine-line dark poem. Line 1 quotes `bro`. First letters do not spell
  a list word.
- Text 2: ocean poem, last two lines `i feel good` and `still alone at sea`.
- Text 3: title `+33` (map metadata). Grade-1 Braille of the five-line French
  poem N4 had pasted under Game 11. First letters I, B, I, Z, A: a city name,
  not an English BIP39 word. N4's Game 11 second pane was this Game 10 page.
- Text 4: monoalphabetic cipher. Unique substitution with `QHO` = `THE`
  decrypts to:

  > IN THE LAND WHERE RIVERS GENTLY MEET,
  > A CITY STANDS, BOTH GRAND AND DISCREET.
  > MARBLE PILLARS RISE TO TOUCH THE SKY,
  > WHERE ECHOES OF THE PAST STILL LIE.
  > BENEATH THE WATCHFUL EAGLE'S GATE,
  > A SILENT SENTINEL THROUGH ENDLESS DAYS.
  > THE AIR IS FILLED WITH WHISPERED LORE,
  > OF BATTLES FOUGHT, OF FREEDOM'S CORE.

  That describes a city. A well-known Eagle Gate monument stands in Salt Lake
  City; other cities sit where rivers meet under an eagle. I am not treating
  any of those names as the seed word.

### Game 11

Title `44 . C`. Visible: the teaching address
`0x50D7e097e61121140c19871F06eA6FeB6d14105b`. Hidden black-on-black mnemonic,
the selftest example, not the Season 2 seed. No second pane. Rabbit wallet,
work of art, bip, and F12 map here. Working reading: `airport` (see the list
at the top). The leftover `. C` is unused.

### Game 12

`sha256("the last game has for url this sentence that is hashed")` is still
`2d80326b034b1aa616625ecb0febf8e9f58b125c5c43bc65f5d8ab6bd6cc1d36`. Fetching
that `.html` on 2026-08-27 returns Vercel `404 NOT_FOUND`. A site map of the
host does not list it. SHA256 and F12 still map here. The Drive file is not on
the tweet screenshot. Notes-to-digits waits on that file.

## 2. Cross-reference the Season 4 hidden page

Done. The table is under Live pages above. It does not name any seed word. It
does name which games hold the ten cities (3, 7, 10), which two games share
"4 cities 1 word" (3 and 10, not 7), and that French helps on 7 and 10, not 11.
The Game 11 Braille attribution in N4's thread is therefore the wrong game.

What would confirm it: using that map plus the live pages to build a 12-word
MATCH.
What would kill it: a full reading that never needs the map.
Cost: insight; the page is transcribed.

## 3. Game 12 as notes-to-digits, not song identification

Already ranked in the README. The page itself is live, not gone: the 11 known
preimages spell "the last game has for url this sentence that is hashed", and the
hosted name is the sha256 of that sentence with the spaces removed,
`913170fd2a64507ceb9cedcd29961f63c03888a2207d4bd8f5e55729c5d67a39.html` (200 on
2026-07-26 and 2026-09-07 through a real browser; 38 other spellings 404, including
the spaced sentence and the tail `this sentence that is hashed` that @deviceio121
proposed in issue #17, whose content description of the page is otherwise right).
The page shows `C1094` bottom right, a black-on-black `simplicity must be rewarded T`,
and a Google Drive link (`drive.google.com/file/d/1WlYvf9JMGlbhJIe3Xnah6ZOHDb0M1IUO`)
to `FTPK.wav`: 43.636 s, 48 kHz, 24-bit stereo PCM, RIFF `fmt` and `data` only, no
LIST/INFO/ID3, L and R genuinely different (correlation 0.974), all 24 bits used, about
89 BPM, key near D minor, flat RMS across the whole track. The audio is not shipped here. The X posts add two facts. On 2025-05-27 the
author posted "Screenshot of game 12" showing the Google Drive placeholder
"Click here to view the file", then replied to themselves "F12 of course". On
2025-06-03 they said someone had found an email address on that Drive link, that
the address is useless, and that they would not open the attachments. Season 1's
hidden `kplo.html` page ("M Prez can help you") is the grammar: keypad digits
play fixed notes (1=D4 293.66 Hz through 0=C4 261.63 Hz) and the instruction is
to visit `https://findtheprivatekey.vercel.app/(the number).html`. A spectrogram
of the S2 track as an image was already refuted (`analysis/tested.md`); the
remaining reading is note names or MIDI numbers to a digit string, then that
string as a BIP39 word or as a page name.

The author's 2025-05-27 "Screenshot of game 12" image is still served as tweet
media: 329x188 pixels, black rectangle, white text "Click here to view the
file". No Google Drive id is visible at that resolution. F12 of the hashed
Season 2 page is no longer available: that URL is 404. The Drive id has to come
from an old mirror, a player paste, or the tweet thread.

@thedragon8383 asked for a hint "through the Jungle" under the author's one-word
post "photopea"
(https://x.com/FTPKgame/status/1926763058266767552,
https://x.com/thedragon8383/status/1926814830620459249). Two days later the same
player identified "the Jungle" as Game 12's sound, with the game found and the
audio unread (https://x.com/thedragon8383/status/1927546235486871920). Photopea
is the browser editor for the Game 1 `.psd`; the Jungle is the Game 12 track.

What would confirm it: a digit string that is a BIP39 word or that names a page
whose body is the word, then the full 12-word mnemonic matching the escrow.
What would kill it: exhausting the note-to-digit maps against the oracle once
the other 11 words are held.
Cost: the audio file itself, which is not on the hashed URL any more.

## 4. The cities cluster

The Season 4 map puts the ten cities in games 3, 7, and 10, and "4 cities 1
word" in games 3 and 10 only (not 7). Live pages now supply named cities and
city-clues, none of them a printed seed word:

- Game 7: Paris, Dakar, in the "with ifs" couplets. S4 also maps "If I were a
  city I would be" here.
- Game 10 Text 3: first letters of the French poem, I B I Z A, a city, and the
  page title is `+33`.
- Game 10 Text 4: the decrypted city poem (eagle's gate, rivers meeting).
- Game 10 Texts 1 and 2: not yet read as city names.
- Game 3: no city string in the HTML; the grids, `SW 1881`, and `image7.jfif`
  are the remaining source.

The word fixed by four cities is not required to be a city name. Game 11 is not
on S4's city list; the IBIZA acrostic is Game 10. Game 7's seed reading is
`nice`; Paris and Dakar stay in the set of ten hidden cities.

What would confirm it: four cities on games 3 and 10 that share one BIP39 word,
then a 12-word MATCH.
What would kill it: a reading of games 3 and 10 that never uses four cities.
Cost: insight; the pages are transcribed.

## 5. The rest of the 2025-05-19 to 2025-06-15 clue posts

Posted in order, skipping pure advertisements. Each URL is the author's own
post; I am describing the attached image rather than reproducing it.

- 2025-05-27 "Screenshot of game 12" then "F12 of course": Drive file
  placeholder, see lead 3.
  https://x.com/FTPKgame/status/1927326950692941869
- 2025-05-28 "History": text only.
  https://x.com/FTPKgame/status/1927680981399457854
  A reply asking "Is this a hint?" got "It's up to you ;) For me, yes :)"
- 2025-05-29 a dark wood library interior, candles, herringbone floor, one
  open book on an armchair. https://x.com/FTPKgame/status/1928053987237925220
- 2025-05-30 a leaping white rabbit on a lavender ground.
  https://x.com/FTPKgame/status/1928392074086285478
- 2025-05-31 a Google Maps view of the Pacific with the International Date
  Line drawn as a dashed zig-zag. https://x.com/FTPKgame/status/1928791004858945750
- 2025-06-02 "In one of the games, there is an optional clue that doesn't have
  very good vibes". Text only.
- 2025-06-03 a uniform #FF0000 rectangle, then the reply "What could it make
  you think of? (several attempts will probably be necessary, but you will
  find)". Pixel check: 624x402, every pixel RGB(255,0,0), no yellow, no EXIF
  payload (`analysis/tested.md`). Three days later: "Just a little yellow in
  all this red will help you find the right one." The yellow is therefore not
  in this PNG; it is on a game page.
  https://x.com/FTPKgame/status/1929833486514278892
- 2025-06-04 "SHA256": names the page-naming scheme, already broken.
- 2025-06-05 "5" attached to a blue Tetris J-piece (four squares).
  https://x.com/FTPKgame/status/1930573400700833946
  Game 5 is independently a digit grid whose corrected diagonal already
  returned HTTP 200 as a number URL; this image may be that game's theme, or
  the number five, or both.
- 2025-06-06 screenshot of a player asking whether Game 6's contact-info
  section is meant to be empty, and the author answering that they removed
  a fake email to avoid contact with a fake address, that "collusion,
  false leads, human error can happen", and that the empty field is now
  part of the game. https://x.com/FTPKgame/status/1931005550558371927
  The same post tells readers to look at comments from @N4Khjir and
  @thedragon8383.
- 2025-06-07 an empty 15x15 Scrabble board, standard colouring, centre star,
  no tiles. https://x.com/FTPKgame/status/1931313249644859692
- 2025-06-08 "ccza". Four letters, no image. Unread.
- 2025-06-09 the Arabic word for date/history. Pairs with "History" and with
  the International Date Line map, but that is a grouping, not a word.
  https://x.com/FTPKgame/status/1931993663816548769
- 2025-06-09 a painter at an easel working a blocky colour canvas (posted as
  a wink, then "work of art" two days later).
  https://x.com/FTPKgame/status/1932181950292525147
  https://x.com/FTPKgame/status/1932844034503868830
- 2025-06-10 a Fall Guys bean in the Ninja skin, captioned "The fall guys
  level is very hard and normally requires two players". One of the twelve
  Season 2 games is a Fall Guys Creative level. This is weeks before Season 3
  ("Fall Guys") launched.
  https://x.com/FTPKgame/status/1932394053368238137
- 2025-06-12 "bip". Confirms the target is a BIP39 word, which the oracle
  already assumes.
- 2025-06-13 a Shure SM58, then the one-word post "standards".
  https://x.com/FTPKgame/status/1933439628868014452
- 2025-06-14 "2 times throughout the game, French will help you". The author
  is in Paris; Season 1 already used French song titles as hashtags. Two of
  the twelve games, not all twelve.
- 2025-06-15 "last clue from me": a black chess knight on a grey ground.
  https://x.com/FTPKgame/status/1934183762079666297

After 2025-06-15 the author said they would only promote, not clue. I have not
treated later posts as S2 clues.

What would confirm any one of these: the matching game page, a single BIP39
word, and a 12-word MATCH against the escrow.
What would kill any one of these: the matching game page showing the image was
flavour, plus the word coming from a different mechanic on that page.
Cost: insight against the live pages; I will not sweep the English wordlist
against the escrow on the strength of an image caption.

## 6. Player comments the author pointed at

On 2025-06-06 the author named @N4Khjir and @thedragon8383 as having left
comments "that could interest you", in the same thread as the Game 6 contact-info
answer (https://x.com/FTPKgame/status/1931006963740979489). I pulled both
timelines for the Season 2 clue window (2025-05-19 through the author's
2025-06-15 last clue). The threads are not social only. N4 pasted live page
text. The dragon posted progress reports the author answered. None of this is a
seed word. Every 12-word set still has to go through `tools/oracle.py`.

### @N4Khjir page transcriptions (2025-05-28 to 2025-06-06)

Posted as replies to the author, with the live titles and body text. I am
quoting the puzzle strings, not claiming a BIP39 word.

- Game 1 (https://x.com/N4Khjir/status/1927619197695082629): Vigenere block
  `ZROQV / JVVW EHFOZV TILV XDB. / OROLV LJNH ZRX DDQ'U VTFJR IRZ / UR GFW TIH
  MFVVAHH QVLFK`; Cicada 3301; the Cold War barrier image already named a decoy
  in `analysis/tested.md`; extra paths `/image1.psd` and
  `/gdjztvzuojmmsmuwrsudjhzdvvlkftfehnxxkbpilscjfljyyg.html`.
- Game 4 (https://x.com/N4Khjir/status/1927620248426913890): two photographs.
  The attached files are no longer served. The live Game 4 page has no photos;
  it has the sentence with a hidden final E.
- Game 6 (https://x.com/N4Khjir/status/1929061582220276150): page
  `hdvpvgyqxzplxefvngacfsdsljxajfhtweksvlkihugghszomf.html`, title
  "Simplicity Must Be Rewarded I". Season 1 used the same sentence as a hashtag
  and as a clue, with a different final letter.
- Game 7 (https://x.com/N4Khjir/status/1927621189503005053): title
  "Zero-based indexing", plus a screenshot that is no longer served. This is
  the game the Season 4 hint page calls the weakest. The title names the
  convention for reading a number as a list position (0-based versus 1-based).
  I am not treating the title-word as a candidate.
- Game 9 (https://x.com/N4Khjir/status/1927621634828939664): title `1211920`,
  body `3114`. Digit strings. As a single BIP39 index, both numbers are out of
  range (max 2048). A1Z26 partitions of the title: 8 letter strings, 0 English
  BIP39 words. A1Z26 of the body: 3 letter strings, 1 English BIP39 word, not
  printed. One title grouping (12, 1, 19, 20) yields the Game 2 page-name
  preimage already in the hash table above, which is a naming-scheme word, not
  a seed word. The live page still has to show how the digits are grouped.
- Game 11, teaching pane (https://x.com/N4Khjir/status/1927616681964126429):
  title `44 . C`, plus the mnemonic and address that `tools/oracle.py
  --selftest` already reproduces. Teaching example, not the Season 2 seed.
  The live Game 11 page is only this pane.
- Game 11, second pane (https://x.com/N4Khjir/status/1927623047076282678):
  title `+33`, heading "Transcription from Braille", then a five-line French
  poem. The live site puts that title and Braille on Game 10 Text 3, not on
  Game 11. S4 maps French to games 7 and 10. Accents omitted here; they do
  not change the first letters I, B, I, Z, A (lead 4):

  > Infinie est la lumiere du matin.
  > Berce doucement, le vent dans le jardin.
  > Il murmurait des secrets aux fleurs endormies.
  > Zephyr danse, leger sur l'eau de la vie.
  > Au loin, l'horizon veille, plein de magie.
- Game 5 (https://x.com/N4Khjir/status/1931017991170183383): "Z = 2 ?". Pairs
  with the author's 2025-06-05 Tetris J-piece captioned "5" and with the digit
  grid already in `analysis/tested.md`.
- Game 1 follow-up (https://x.com/N4Khjir/status/1931020117774668115): "The
  file image2.jpg does not exist." The author confirmed it
  (https://x.com/FTPKgame/status/1931024956046909798): the file was a
  development error, and they said they would delete that part of the code.
  Not a puzzle step.
- White-rabbit clue (https://x.com/N4Khjir/status/1928535519022948673): N4
  read it as a wallet with no native ETH. The escrow's ETH balance is 0; the
  prize is the USDT token. I am not treating a thematically neighbouring
  BIP39 word as a candidate.

The author told N4 "you did some good research... nice to share it with
others" (https://x.com/FTPKgame/status/1927681391833051513). N4's later
2025-06-07 to 2025-06-15 posts in the Wayback capture are unrelated retweets,
except a no-text reply to the Shure SM58 clue.

### @thedragon8383 progress reports

- Game 11 teaching wallet empty?
  (https://x.com/thedragon8383/status/1925711495020560598). It is the
  teaching example, 0 ETH / 0 USDT, not the escrow.
- "not sure if I C what is going on"
  (https://x.com/thedragon8383/status/1925723116078080077). Author: "This
  game seems okay" (https://x.com/FTPKgame/status/1925716299876896917).
  Pairs with Game 11's `44 . C` title, or with the letter C, or with neither.
- "I think I got game 10"
  (https://x.com/thedragon8383/status/1926386081076826598). Unverified. Game
  10's two sub-poem acrostics already fail (`analysis/tested.md`); if the
  player was right, the word is not in those acrostics.
- Jungle / Photopea / Game 12 sound: see lead 3.
- "cold German cicada", stuck on Game 1 part 2
  (https://x.com/thedragon8383/status/1929260937292267742). Author: the
  optional bad-vibes clue is not required to reach Game 1
  (https://x.com/FTPKgame/status/1929299848991244698). Later recap: the
  player's first reply was cicada, the second a GPS coordinate site
  (https://x.com/FTPKgame/status/1929903388839350590). The GPS site the
  player linked was https://www.itilog.com/
  (https://x.com/thedragon8383/status/1929895434689941876).
- Solid-red PNG: "Game 2... but why?"
  (https://x.com/thedragon8383/status/1929885806606372961).
- Game 5: asked for a hint; author said a first one had already been posted,
  then the Tetris-J image. Player: "More of these two part puzzles"
  (https://x.com/thedragon8383/status/1930789907376594980).
- International Date Line map: "stuck in Colorado, USA"
  (https://x.com/thedragon8383/status/1930426198095515915).
- Empty Scrabble board: guessed Game 1 or Game 5, "did not seem to get me
  anywhere with either game"
  (https://x.com/thedragon8383/status/1931419058877968771).
- Arabic تاريخ: asked whether the word was Sindhi or Arabic
  (https://x.com/thedragon8383/status/1932077123491053972).

What would confirm any transcription: the matching live page, a single BIP39
word from that page's mechanic, and a 12-word MATCH against the escrow.
What would kill any transcription: the live page showing the pasted text was
flavour, plus the word coming from a different mechanic on that page.
Cost: the harvest itself is done. Two bounded readings of those strings are
now in `analysis/tested.md` (the extra 50-letter names are not the
concatenation oracle; Game 9 as a lone index is out of range; Game 9 title
A1Z26 is 0 list words). The live pages from 2026-08-27 supersede N4 on Game 10
versus Game 11 and on Game 4's missing photos. I will not sweep the English
wordlist against the escrow on the strength of a title or an acrostic.
