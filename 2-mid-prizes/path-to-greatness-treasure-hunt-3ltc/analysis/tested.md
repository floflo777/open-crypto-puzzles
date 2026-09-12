# Tested (full negatives ledger)

The summary table in the folder's `README.md` shows the highlights; this file is the
complete record. One row per run, in the order tested. Nothing is removed; a hypothesis
retested with a different method gets a new row.

Two things make these negatives cheap and exact.

- Each of the four segments is one AES-256-CBC block holding 8 useful bytes, so its
  plaintext must end with a PKCS7 padding of eight `0x08` bytes. A wrong key passes with
  probability 2^-64. A pair of clue answers is therefore refuted knowing nothing about the
  other six.
- Every answer has a length imposed by the author's own scheme, so a candidate of the wrong
  length is dropped before any AES call. That filter is free and it is what makes some
  families collapse without a run at all.

Two rates are used below. The CPU harness measured 294,000 segment tests per second per
core, about 4,200,000 per second over 22 cores. The GPU engine is a CUDA AES-256-CBC padding
oracle taking a left half and a right half and forming the key as their concatenation; it
peaks near 3,000,000,000 keys per second and the per-run rate in the table is the observed
end-to-end rate, generation of the candidate lists included.

Witness protocol on every GPU run: three synthetic pairs are planted in the candidate
streams, at head, middle and tail, each one encrypted beforehand under the same scheme and
fed through the normal code path. A run counts only if all three are re-found and the engine
reports the space as exhausted. Every reported hit is re-derived on CPU by `tools/oracle.py`
before it would be believed.

## Runs on the GPU engine, 2026-09-09

Totals: 37 runs, 5,690,021,893,966 ordered pairs, 0 match, 4.12 hours elapsed on one
RTX 5080, witnesses 3 of 3 on every run.

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Segment 3: `ship` is one of 12 strong strings taken from the film scene (`isamathematicalcertainty`, `jonathanhydevictorgarber` and 10 others), `wasd` is any 8-digit string | 12 x 100,000,000 = 1,200,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 1.18 G/s, 1.0 s | 2026-09-09 |
| Segment 3: `ship` is a name or role of at most 4 tokens, `wasd` is one of 1,134 structural readings of the grid | 839,858 x 1,134 = 952,398,972 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.73 G/s, 1.3 s | 2026-09-09 |
| Segment 3: `ship` is a word window of the IMSDb screenplay, Wikiquote, Wikipedia or the site poems, `wasd` structural | 72,865 x 1,134 = 82,628,910 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.65 G/s, 0.1 s | 2026-09-09 |
| Segment 3: `ship` is any 24-character window of the film transcript, all positions, `wasd` structural | 54,998 x 1,134 = 62,367,732 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.63 G/s, 0.1 s | 2026-09-09 |
| Segment 3: `ship` is a name or role of at most 4 tokens, `wasd` is any of the 65,536 strings over `{w,a,s,d}` | 839,858 x 65,536 = 55,040,933,888 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.76 G/s, 72.0 s | 2026-09-09 |
| Segment 3: `ship` is one of 625 deck names of the ship, `wasd` is any 8-digit string | 625 x 100,000,000 = 62,500,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.56 G/s, 112.2 s | 2026-09-09 |
| Segment 3: `ship` is a concatenation of 5 deck names, `wasd` structural | 3,173,842 x 1,134 = 3,599,136,828 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.75 G/s, 4.8 s | 2026-09-09 |
| Segment 3: `ship` comes from the stanza 2 riddle, at most 4 tokens, `wasd` structural | 3,209,764 x 1,134 = 3,639,872,376 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.74 G/s, 4.9 s | 2026-09-09 |
| Segment 3: same stanza 2 family, `wasd` over `{w,a,s,d}^8` | 3,209,764 x 65,536 = 210,355,093,504 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.77 G/s, 274.5 s | 2026-09-09 |
| Segment 4: `scramble` from 5 mechanical readings of the 41-character string, `sky` from 4 families | 198,508 x 741 = 147,094,428 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.08 G/s, 1.8 s | 2026-09-09 |
| Segment 1: `imagine` is an 8-digit block written twice, `beach` from the earlier candidate lists | 100,000,000 x 2,479 = 247,900,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.37 G/s, 665.6 s | 2026-09-09 |
| Segment 3: `ship` is a 24-character window starting on a word, over the whole film transcript, `wasd` is any 8-digit string | 14,706 x 100,000,000 = 1,470,600,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.67 G/s, 2,190.0 s | 2026-09-09 |
| Segment 1: `imagine` is two December 7 or 8 dates, years 1800 to 2100, in 4 formats, `beach` from the earlier lists | 5,796,056 x 2,479 = 14,368,422,824 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.39 G/s, 36.4 s | 2026-09-09 |
| Segment 1: `imagine` is one date written in two different formats, years 1 to 2100, `beach` from the earlier lists | 7,124,619 x 2,479 = 17,661,930,501 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.38 G/s, 47.0 s | 2026-09-09 |
| Segment 4: `scramble` 5 families, `sky` with its capitals pinned by the certified rule | 198,508 x 3,599,533 = 714,536,096,764 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.59 G/s, 1,217.7 s | 2026-09-09 |
| Segment 1: two December dates, `beach` from the YouTube melody, first reading (389 variants) | 5,796,056 x 389 = 2,254,665,784 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.21 G/s, 10.5 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` from the YouTube melody, first reading | 7,124,619 x 389 = 2,771,476,791 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.18 G/s, 15.3 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` from the YouTube melody, first reading | 100,000,000 x 389 = 38,900,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.56 G/s, 69.3 s | 2026-09-09 |
| Segment 1: `imagine` is `19410712` followed by any 8 digits, `beach` from the lists plus the melody | 100,000,000 x 2,868 = 286,800,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.55 G/s, 519.3 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` from the melody, second reading (1,177 variants) | 7,124,619 x 1,177 = 8,385,676,563 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.29 G/s, 28.6 s | 2026-09-09 |
| Segment 1: two December dates, `beach` melody second reading | 5,796,056 x 1,177 = 6,821,957,912 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.32 G/s, 21.4 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` melody second reading | 100,000,000 x 1,177 = 117,700,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.37 G/s, 315.4 s | 2026-09-09 |
| Segment 1: `imagine` is any 8 digits followed by `19410712`, `beach` from the lists plus the melody | 100,000,000 x 2,868 = 286,800,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.42 G/s, 680.9 s | 2026-09-09 |
| Segment 1: `imagine` is a number or a word spelled out, twice, `beach` from the lists plus the melody, third reading | 15,262 x 6,243 = 95,280,666 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.27 G/s, 0.4 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` melody fourth reading (3,804 variants, sixth note read as D# or as E) | 7,124,619 x 3,804 = 27,102,050,676 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.32 G/s, 84.0 s | 2026-09-09 |
| Segment 1: two December dates, `beach` melody fourth reading | 5,796,056 x 3,804 = 22,048,197,024 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.33 G/s, 66.2 s | 2026-09-09 |
| Segment 1: `imagine` spelled out in words, `beach` melody fourth reading | 15,262 x 3,804 = 58,056,648 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.23 G/s, 0.2 s | 2026-09-09 |
| Segment 1: `imagine` is a date written in letters, month abbreviated or full, twice, `beach` from the widest melody family | 319,545 x 13,215 = 4,222,787,175 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.28 G/s, 14.9 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` melody third reading with one extra character (43 encodings) | 100,000,000 x 3,764 = 376,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.33 G/s, 1,149.5 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` written as note names or solfege syllables | 100,000,000 x 560 = 56,000,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.23 G/s, 242.8 s | 2026-09-09 |
| Segment 1: one date in two formats, `beach` as note names | 7,124,619 x 560 = 3,989,786,640 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.18 G/s, 22.2 s | 2026-09-09 |
| Segment 1: date in letters twice, `beach` as note names | 319,545 x 560 = 178,945,200 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.12 G/s, 1.4 s | 2026-09-09 |
| Segment 1: `imagine` is `1941`, any 8 digits, then `0712`, `beach` from the lists plus the melody | 100,000,000 x 6,243 = 624,300,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.25 G/s, 2,453.7 s | 2026-09-09 |
| Segment 1: `19410712` then any 8 digits, `beach` melody fourth reading | 100,000,000 x 3,804 = 380,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.21 G/s, 1,796.5 s | 2026-09-09 |
| Segment 1: 8-digit block twice, `beach` read from degree 0 and chromatically | 100,000,000 x 2,617 = 261,700,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.20 G/s, 1,340.3 s | 2026-09-09 |
| Segment 2: `chess` is 4 pieces in algebraic notation, `wonders` from the earlier structured encodings | 360 x 130,656 = 47,036,160 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.22 G/s, 0.2 s | 2026-09-09 |
| Segment 1: any 8 digits then `19410712`, `beach` melody fourth reading | 100,000,000 x 3,804 = 380,400,000,000 | GPU padding oracle | 0 match | yes: 3 of 3 | 0.28 G/s, 1,382.0 s | 2026-09-09 |

## Earlier passes on the CPU harness, 2026-09-08

| Hypothesis | Space (N) | Method | Result | Witness | Rate | Date |
|---|---|---|---|---|---|---|
| Segment 3: `wasd` is the four movement letters, `ship` is the first family built from the image (174 tokens concatenated 1 to 3 deep) | 10,900,000,000 ordered pairs, `{w,a,s,d}^8` exhaustive | CPU harness on 22 cores | 0 match | yes: head, middle, tail | 4,200,000/s | 2026-09-08 |
| Segment 2: `chess` is the 14 pieces minus exactly 2, in 6 notations and about 18 orders, case inversion included, against the structured `wonders` encodings | 861,000,000 ordered pairs | CPU harness, exhaustive over the reduction | 0 match | yes | 4,200,000/s | 2026-09-08 |
| Segment 1: `imagine` is a pair of calendar dates (188,276 dates, 4 formats, 36 anchor days, each written twice) | 63,330,856 candidates | CPU harness | 0 match | yes | 294,000/s per core | 2026-09-08 |
| Segment 4: `sky` under the capital pinning `n = v - 4`, unique solution under `1 <= n <= len(title)` | 3,599,533 values, exhaustive over the pinned space | CPU enumeration, then GPU crossing above | space exhausted, 0 match in the crossing | yes | n/a | 2026-09-08 |

## Families excluded without running anything

These cost nothing because the author fixed the answer lengths.

| Hypothesis | Why it is excluded | Date |
|---|---|---|
| The clue 6 melody is Do-Re-Mi, the Lost theme, Zelda, Mario, Tetris, Star Wars or 14 other well-known tunes | 18 of the 20 cannot produce 16 characters for 15 notes under any of the 840 encodings tried. Arithmetic only, no oracle call | 2026-09-08 |
| Solfege syllables written out, or bare initials, or all degrees 1 to 7 at one digit | minimum 30 characters, or exactly 15, never 16 | 2026-09-08 |
| Any transcription of a segment ciphertext whose 22nd base64 character is not `A`, `Q`, `g` or `w` | a 16-byte ciphertext leaves only 2 useful bits in that character. This caught one real misreading of segment 3 (`O` against `Q`) | 2026-09-09 |
| Reading each value of clue 8 as a single letter index | two of the values need a track title of 18 letters or more, and only one of the 13 titles is that long. Splitting into digits is forced | 2026-09-08 |

## Observations that closed a channel

| Claim | Scope of the negative | Witness | Date |
|---|---|---|---|
| `ship` is a string written inside the hidden image of `Ship.png` | 24 characters planted at the real size and the real contrast are re-read, even at 61 percent of that contrast; nothing comparable is in the image. The payload is a picture | yes, legibility witness | 2026-09-08 |
| The hidden image comes from a texture of the game | 198 textures extracted from the build, SSIM and correlation, mirrored and not: best real score 0.106 against a planted copy at 1.000 | yes | 2026-09-08 |
| The two faces are real 1912 passengers or crew | about 700 targeted photographs, including the 206 portrait plates of the 1911 source volume: best real score 0.76 against witnesses at 0.92 to 0.99. They are actors in the 1997 film | yes | 2026-09-09 |
| `Beach.png` carries image steganography | 24 bit planes in 2 scan directions, local contrast at 6, 12 and 25 times, and 0 bytes after the IEND chunk. The sand grain co-varies across the three channels, which is a drawn texture | yes | 2026-09-08 |
| The three numbers of clue 5 are great-circle distances between monuments | haversine over the New7Wonders plus Giza plus 21 monuments, both units, tolerance 60: no coincidence under 6 miles. 12,772 miles is also more than half the Earth's circumference | yes | 2026-09-09 |
| Clue 4 is a chess problem | Stockfish 17, 20 seconds, multipv 4: no forced mate, no unique move, and the position is in no database. It encodes the position, it does not ask a question about it | yes | 2026-09-08 |
| The game demo hides a positional music player, so "the first fifteen you hear" depends on where the player stands | the level has one AudioSource playing the whole album from t = 0 on loop; the `PositionMusicPlayer` and `Phonograph` classes exist in the assembly but no instance is present, checked over all 2,174 MonoBehaviours of the level | yes | 2026-09-09 |

## Uncertified, does not count

| Hypothesis | Space (N) | What went wrong | Status |
|---|---|---|---|
| Segment 4, wave F | 6,110,000,000 ordered pairs | the process exited 0 but wrote no verdict line, so there is no evidence the sweep reached the end | to be replayed; it is not counted in any total above |
