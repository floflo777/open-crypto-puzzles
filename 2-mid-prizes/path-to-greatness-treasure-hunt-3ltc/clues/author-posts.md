# Author posts and quotes

Short, dated material published by Justin Patterson (`jpatt94`) about this treasure hunt:
the announcement, the two versions of the rules page, and the lines of his own clue poems
that carry an instruction. The clue images themselves are the JPEG and PNG files next to
this one, served from `p2gtreasure.com/Clues/` since 2021-05-15.

## Announcement, r/ARG, 2021-07-25 18:00:56 UTC

Post `orgh1k`, 23 upvotes, 4 comments:
https://reddit.com/r/ARG/comments/orgh1k/i_made_a_treasure_hunt_with_a_crypto_prize/

> "There's a Litecoin wallet with 3 LTC (~$375 at the time of writing this), and the
> private key can be discovered using the clues. Once solved, you can freely transfer the
> balance to your own Litecoin wallet."

> "The clues can be found at https://p2gtreasure.com/"

> "I'm very proud of the puzzles I designed in this treasure hunt, and I know there's a
> community out there somewhere that would enjoy solving them, but I'm having a hard time
> finding them. I hope this is a good place to share it. Good luck and happy solving!"

On 2021-08-25, in the same thread, the author reports only "a few private efforts through
DMs" and no public solving community.

## Rules, p2gtreasure.com, read 2026-09-09

https://p2gtreasure.com/ (Wayback capture 2021-12-20:
https://web.archive.org/web/20211220074516/http://p2gtreasure.com/)

> "The clues above will lead to a Litecoin wallet's private key."

> "Once solved, you must send the Litecoins from the treasure hunt Litecoin wallet to a
> separate Litecoin wallet that only you own."

> "If the prize value shown above becomes zero (or close to zero), it means that someone
> has won and the treasure hunt is over."

> "It is not necessary to make a donation in order to win."

The same page names the escrow directly, under "Donate Litecoin (LTC)":

> "Litecoin address: LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS"
> "Your donation will be added directly to the Litecoin wallet prize."

## Rules, the older site at p2gtreasure.com/old/, still served

https://p2gtreasure.com/old/index.html (Wayback capture 2022-03-23:
https://web.archive.org/web/20220323235950/http://p2gtreasure.com/old/index.html)

> "It is not necessary to make a donation in order to win."
> "The first step is to download and play the demo."
> "Clues are found in the demo, and will lead to a Litecoin wallet's private key."
> "The last step is to send the Litecoins from the treasure hunt Litecoin wallet to a
> separate Litecoin wallet that only you own."
> "The first and last steps are the only steps I will ever provide."
> "If the prize value shown on the main page becomes zero (or close to zero), it means
> that someone has won and the treasure hunt is over."
> "The green orbs, timer, and lava have no connection to the treasure hunt. They are meant
> only to be fun objectives."

Two of these matter for method. The fifth line says in advance that the author will never
publish another hint, so nothing here waits on him. The seventh is a negative he gives away
for free: the game objectives of the demo carry nothing.

The old home page also states who he is and what the demo is for:

> "It is currently being developed by just me, Justin Patterson"

## The composition scheme, clue image `computer_screen.jpg`

This is the author's own drawing of his encryption, staged as four windows of a fake
desktop. Transcribed here character for character from the lossless texture that ships
inside the game demo; the JPEG in this folder is the same image, one generation down.

Window 1, `litecoin_wallet.txt`:

```
Public address:
LUtL7qnm3gzxKjHcfVLSjydqhhinTVmTmS

Private key (WIF, encrypted with super_key):
dxIx52zhnXodWi36dEx/kJV59Udj4xh3vR5vmeuoyXTNCE8VOaTmVkVctDpK0XNHYJA6G+m/jT4fSU9VejXYgg==

AES 256-bit, CBC, IV: goodluck_havefun
```

Window 2, `super_key_segments.sheet`: the 32-byte `super_key` cut into four 8-byte pieces,
each encrypted on its own.

```
id  segment (base64, encrypted)  bytes   IV                 key
1   I2c6TXU/Z1oCKnEQTWZUvg==     0-7     few_n_far_btween   clue 1 + clue 6
2   RWaBo4ChEOM/i+MLy2NUpg==     8-15    nocturnal_sugars   clue 4 + clue 5
3   16GmtUINaYuN7f1RlBO5sQ==     16-23   colors_on_leaves   clue 3 + clue 7
4   7CZlZjwCMGUb/TZm07b9dg==     24-31   seconds_of_dream   clue 2 + clue 8
```

Window 3, `clues.sheet`: which clue feeds which segment, and which bytes of the AES key it
occupies. That byte range is what fixes each answer's exact length.

```
id  clue      segment  bytes in the key   answer length
1   imagine   1        0-15               16
2   scramble  4        0-14               15
3   wasd      3        0-7                8
4   chess     2        0-11               12
5   wonders   2        12-31              20
6   beach     1        16-31              16
7   ship      3        8-31               24
8   sky       4        15-31              17
```

Window 4, `fix_clues.script`: the normalisation, given explicitly.

```
foreach clue:
    clue.answer.remove_spaces()
    if clue.id != 4:
        clue.answer.to_lowercase()

// A monkey on a typewriter wrote this
// at some point in time.
```

## The clue poems, quoted where they carry an instruction

Each clue image pairs a picture with a short poem. Transcribed from the lossless textures.

**Clue 1, `imagine`, 16 characters.** The poem rewrites the Lennon lyric ("living life in
peace" becomes "Livin' life today"), and prints one number under it.

> "Imagine all the people / Livin' life today / Imagine life was taken / Left a number in
> its place / Imagine that number of years / Past that fateful day / Imagine it written
> twice / The infamous way"
>
> "19410712"

**Clue 2, `scramble`, 15 characters.** Eight anagrams above one mixed-case string. The
anagrams read "With your capital, addition. To the lower, subtract." The string, transcribed
on a monospace grid, is `s-bcBPEFfJDfeFmksmPOkChDhrgBqjD-i---ffeNB`, 41 cells with dashes at
positions 2, 32, 34, 35 and 36, and 15 capitals.

**Clue 3, `wasd`, 8 characters.** A 10 by 10 grid of number plus direction pairs (up, down,
left, right), with four cells carrying a star numbered 1 to 4 instead of an arrow.

**Clue 4, `chess`, 12 characters.** A board with 14 pieces, and the only clue whose answer
keeps its case.

> "A period of madness / From a symbol that's flown / Order in the court / From the front
> lines to the throne"

**Clue 5, `wonders`, 20 characters.** Three rows of pictograms, each row ending in a Roman
numeral written with a vinculum: 12,772 then 5,210 then 12,061.

> "A thousand maps drawn with blood"
>
> "A bit of help from each line"
>
> "To shelter my ship on the flood"
>
> "With the stars in the sky our guide"

**Clue 6, `beach`, 16 characters.** Delivered by the QR code `qr1.jpg`, which points at a
Google Drive copy of `Beach.png`. The whole poem is the instruction:

> "This time we change the channel / And traverse to lost dimensions / Here we find a
> pattern / That demands our full attentions / Our counting starts with a deer / Our
> pattern starts with the sun / Note the first fifteen you hear / Write them up and this
> step's done"

**Clue 7, `ship`, 24 characters.** Delivered by the QR code `qr2.jpg`, which points at a
Google Drive copy of `Ship.png`.

> "A red sky at night / Not the least bit significant / A channel for light / And a ship so
> magnificent"
>
> "The cold, dark night / Moves towards its maker / The vast, frigid ocean / The great
> undertaker"

**Clue 8, `sky`, 17 characters.** File name `00111111.jpg`, which is 63, the ASCII code of a
question mark. A panel inside the room states the rule with two worked examples, then a row of 13
question marks above the string `ehk-bqNEFRUn-`.

```
4 -> Exit Light  -> T
8 -> Ghost March -> R
```

## The author's other published material

- Game demo, 134,238,633 bytes, Unity Windows x64, built 2021-02-04, linked from the old
  download page: https://drive.google.com/file/d/15B7i1EU7OUpc1SXYmSccRLDku4199cSB/view
- Demo trailer, YouTube: https://www.youtube.com/watch?v=T98D6Otefgs
- Album "Seconds of Dream", Justin Patterson, released 2021-01-07, 13 tracks, 57:06, the
  exact audio embedded in the demo: https://open.spotify.com/album/1pGpPWw8Dl0Uq7n77s4koK
  and https://music.apple.com/us/album/seconds-of-dream/1548289299
- YouTube video "Seconds of Dream - Path to Greatness Soundtrack", posted 2019-03-18,
  641 s: https://www.youtube.com/watch?v=EojQgdZeTyM
- Second album "Archaic Reveries", 2018, 8 tracks.
