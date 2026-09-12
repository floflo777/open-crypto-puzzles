# Leads (full notes)

The "Open leads, ranked" section of the folder's `README.md` shows the ranked list; this file
carries the full notes. Leads are ordered by cost to test, then by expected value.

One remark applies to all of them. Because the four segments are independent and each has an
exact test, a lead here is never "run more of something". It is always one precise reading of
one clue, and the run that settles it lasts seconds. The right question to ask of any idea
below is: what 16, or 8, or 24 characters exactly does it produce.

## 1. Segment 1: the 16th character of `beach`, and how `imagine` is written

- **Cost**: minutes per new convention. One convention against all 10^8 repeated 8-digit
  blocks is 0.2 seconds on the GPU engine.
- **What it is**: clue 6 says "Our counting starts with a deer" (doe, so `do` = 1), "Our
  pattern starts with the sun" (`sol`, so the melody begins on the fifth degree), and "Note
  the first fifteen you hear". The melody is the opening of the author's own YouTube video
  "Seconds of Dream - Path to Greatness Soundtrack" (2019), which is monophonic, unlike the
  album version embedded in the game. Measured by FFT to within 1 cent, the first fifteen
  notes are A#5 F#5 B5 A#5 F#5 D#5 F5 C#5 B4 C#5 A#4 A#5 F#5 B5 A#5, and the key is F# major
  or D# minor, so the first note A# is the fifth degree and the poem's witness passes. The
  answer is 16 characters for 15 notes, so exactly one note costs two characters. The sixth
  note bends between D#5 and E5, which is the natural candidate for that extra character
  (`1#` if it is read as E in D# minor). Written that way the sequence is
  `536531#276755365`, 16 characters.
- **Why it ranks here**: it is the only segment where both halves are read rather than
  guessed, and the remaining ambiguity is a writing convention, which is a finite list.
- **What would confirm it**: a match on segment 1 from `tools/oracle.py --segment 1`.
- **What would kill it**: listening to the first 20 seconds of the video and counting a
  number of notes other than 15, or hearing the sixth note clearly as one pitch and not a
  bend. Either would mean the pitch track, not the convention, is what is wrong.
- **Status**: open. Refuted so far against this melody family, in all its readings from 389
  to 13,215 variants: an 8-digit block repeated over the whole 10^8 space, one date in two
  formats, two December dates, `19410712` with 8 free digits on either side and in the
  middle, numbers and dates spelled out. See `tested.md`.

## 2. Segment 1, the other half: `imagine` may not be a date

- **Cost**: minutes.
- **What it is**: the clue 1 poem rewrites Lennon. Where the song has "living life in peace",
  the poem has "Livin' life today", and the poem then says "Left a number in its place". The
  usual reading is that the number printed under it, `19410712`, is December 7 1941 written
  with day and month swapped, that "the infamous way" points at the American `MMDDYYYY`
  format, and that "written twice" means 2 times 8 characters. Every calendar date pair under
  that reading has now been swept. The reading that has not been tried is the literal one:
  a word of the song was replaced by a number, and it is that word, or the count attached to
  it, that the poem wants written twice.
- **Why it ranks here**: same cost as lead 1, and it is the complement of it. If lead 1 is
  right about `beach`, then `imagine` is what is wrong, and this is the largest untested
  reading of `imagine`.
- **What would confirm it**: a match on segment 1.
- **What would kill it**: a match on segment 1 from lead 1 instead.
- **Status**: open.

## 3. Segment 3: what the author would write to describe his own montage

- **Cost**: minutes per family. The left half of this segment is fully enumerable, so one
  `ship` hypothesis is tested on its own: `{0-9}^8` is 19 seconds on CPU and about 1.5
  seconds on the GPU engine, and `{0-9wasd}^8` (1,480,000,000 strings) is also within
  seconds there.
- **What it is**: the hidden picture in the red low bit plane of `Ship.png` is a montage of
  frames from the 1997 film "Titanic", the "will founder" scene: Ismay played by Jonathan
  Hyde on the left, Andrews played by Victor Garber on the right, the deck plans in the
  middle. What is missing is the 24-character string the author drew out of it. Quotations
  from the scene, character names, actor names, deck names and the stanza 2 riddle are all
  refuted against an enumerable left half, 1.8e12 ordered pairs with witnesses. What has not
  been built is a description family: what the montage shows rather than what is said in it.
- **Why it ranks here**: same near-zero cost per hypothesis as leads 1 and 2, but the target
  is looser, so the number of families to try is larger.
- **What would confirm it**: a match on segment 3.
- **What would kill it**: nothing cleanly. Treat it as a family to exhaust rather than a
  claim to refute, and record the scope of each family.
- **Status**: open. Note that the poem's own phrases, "the great undertaker" and "moves
  towards its maker", may be paraphrases of lines in the original screenplay; finding the
  lines they paraphrase would point at the register the author was writing in.

## 4. Segment 4: the pairing rule between the 17 digits and the 13 tracks

- **Cost**: hours, because the rule has to be found before it can be tested.
- **What it is**: clue 8 states its own rule with two worked examples, `4 -> Exit Light -> T`
  and `8 -> Ghost March -> R`, that is, a number picks a letter out of a track title with
  spaces removed. Both titles are tracks of the author's album "Seconds of Dream", which has
  13 tracks, and the clue's string `ehk-bqNEFRUn-` has 13 cells, so the pairing looks 1 to 1.
  The 11 letters give the 17 digits `58112171456182114` through their alphabet positions.
  A lowercase form `n = len - v` reproduces the author's own witness and closes the count at
  17 characters, whose first letters read `e n t ? r`, which is ENTER; "Exit light, enter
  night" is the Metallica lyric the two example titles are quoting. The part that does not
  work is that track 7, `allartmustdie`, contains neither `h` nor `n`, so `enterthenight`
  cannot come out of a strictly positional 1 to 13 pairing.
- **Why it ranks here**: more of the mechanism is certified here than anywhere else, but the
  missing piece is a rule and not a string, so it cannot be swept.
- **What would confirm it**: a pairing that is not positional, still reproduces
  `4 -> Exit Light -> T`, and produces 17 characters.
- **What would kill it**: showing that the 17 digits are not letter indexes at all, for
  example by finding a different reading of the 13 cells that also lands on 17.
- **Status**: open. 714,683,191,192 pairs already refuted under the mechanical readings of
  `scramble` crossed with the pinned-capital `sky` space.

## 5. Segment 2: identify the six pictograms of clue 5

- **Cost**: needs a person. Someone who recognises the drawings settles it in a minute.
- **What it is**: clue 5 has three rows, each ending in a Roman numeral written with a
  vinculum: 12,772 then 5,210 then 12,061. The two torches framing the panel in the game
  level carry 64 by 64 textures reading `km` and `mi`, and each row's pennant points at one
  of them, so the numbers are presented as distances. That reading does not survive
  measurement: 12,772 miles is more than half the Earth's circumference, and a haversine
  sweep over the New7Wonders plus Giza plus 21 other monuments, both units, tolerance 60,
  produced no coincidence under 6 miles. If the numbers are instead pairs of (track number,
  letter position), which is the rule certified on clue 8, then naming the six icons is what
  gives the reading its dictionary.
- **Why it ranks here**: the cheapest step is recognition by a human eye, and no sweep
  replaces it.
- **What would confirm it**: an identification of the icons that makes the three numbers
  decompose the same way in all three rows.
- **What would kill it**: an identification that makes the distance reading work after all,
  which would send the segment back to geography.
- **Status**: open. `chess`, the other half of this segment, is the only answer that keeps
  its case, and the reduction from 14 pieces on the board to 12 characters is not solved
  either; the two lines "A period of madness / From a symbol that's flown" are the ones that
  have to do that work, and "a symbol that's flown" in a maritime puzzle suggests the
  international code of signals, where each flag stands for a letter. Untested.

## Closed, kept here so they are not retried

- **The author will provide a hint.** He wrote on the old rules page, in 2021, "The first and
  last steps are the only steps I will ever provide." Nothing here should wait on him.
- **The game objectives carry something.** Same page: "The green orbs, timer, and lava have no
  connection to the treasure hunt."
- **`CrimsonGrid`, the object in the game whose name matches the red channel.** 198 textures
  compared, best real SSIM 0.106 against a planted copy at 1.000.
- **The two men in the hidden image are real Titanic figures.** About 700 photographs, best
  score 0.76 against witnesses at 0.92 to 0.99. They are actors.
- **The melody is a well-known tune.** 18 of 20 candidates cannot produce 16 characters for 15
  notes under any encoding tried.
- **`colors_on_leaves` names a track to be found.** It is on neither of the author's two
  albums and is not published anywhere, which is consistent with clue 7 being an image rather
  than audio. The other three IVs are tracks.
