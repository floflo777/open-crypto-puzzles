# Open leads, ranked

## 1. Log the 3 already-launched btcrecover runs (minutes, free)

Runs 1 to 3 (499,000,000 raw candidates; 274,000,000 close-word and typo variants of the 4
refuted anchors; 880,000 candidates crossed with 50 thematic passphrases) were prepared and
launched against a pipeline whose own known-answer test passes, but the result of each run was
never written down. This is the fastest possible action: rerun each and record whether the
tool printed a match. Confirms: any match ends the puzzle. Kills: a clean run on all 3
confirms these particular candidate sets carry no signal, without spending new compute.

## 2. Re-derive the word inventory from the image itself, not from community claims (hours)

Every large campaign to date, including the 3.75-million-seed anchor-free sweep, still forces
a fixed pool of "obviously visible" words rather than a pool built by a fresh, systematic pass
over the full image. The high-resolution crops needed for this already exist; what has not
been done is a first-principles relisting of every candidate word on the collage, independent
of the word lists used in past runs (several of which trace back to the 2 unconfirmed Reddit
accounts). Confirms: a word not present in any prior candidate pool turns up and, combined with
the others, derives the target. Kills: a systematic relisting reproduces the same pool already
tested, closing this as a source of new candidates.

Contributed 2026-11-04: a clue-by-clue reading of the image, with crops and what each reading
was searched against, is in [Desalzes/bnw-0.2btc-analysis](https://github.com/Desalzes/bnw-0.2btc-analysis#the-clues). It ranks words
by visible hiding devices (tiny labels, case and colour changes) rather than by the community
pool, so it answers part of this lead; it does not close it.

## 3. Cross the rune transcription against the Russian-prose cipher key (closed 2026-11-04, contributed)

@Desalzes decoded all three inscriptions with one key, a one-to-one substitution over Russian
([readings](https://github.com/Desalzes/bnw-0.2btc-analysis#1-the-borders-the-address-and-the-rune-cipher)). A key rebuilt from the right
border and the dial strip alone predicted every group length of the held-out top rows
(reported). The decoded text reads coherently start to finish:

| Where | Plaintext | English |
|---|---|---|
| Right border | Здесь зашифрованы биткоины на чёрный день номер X | here are encrypted bitcoins for a rainy day, number X |
| Top border, 3 rows | Я надеюсь, что сюда будут присылать много биткоинов | I hope that many bitcoins will be sent here |
| Dial strip | СУММА ДВУХ ЧИСЕЛ | sum of two numbers |

"Чёрный день" is literally "black day". The glyph after "номер" (number) is a stave with one
diagonal, read as the rune Nauthiz, the 10th rune of the Elder Futhark, so "number 10"; it is the
one glyph not cross-checked. The channel names no seed word, but it states that bitcoins are
encrypted in the image, gives a number, and gives an arithmetic rule next to the dial.

Original note:


The 85-glyph positioned transcription of the geometric rune script (3 locations on the image)
was completed on 2026-08-02. The hypothesis that this script decodes as Russian-language prose
was developed earlier and independently. The two have never been directly cross-checked against
each other, because the positioned transcription did not exist until the later pass. Either the
decoded prose reads coherently start to finish, which would settle the rune channel as
non-seed-bearing with certainty rather than high confidence, or a mismatch would reopen the
cipher as a candidate word source. The image's pedestal and bottom band remain untranscribed, so
even a coherent result would not close the glyph inventory completely.

## 4. Settle BIP39 versus old-Electrum from a source, not from more derivation (needs new
information)

The format fork is the single choice that would cut the remaining search space roughly in half.
The puzzle author posted once, in 2020, and has not been heard from since; no known-answer
message signature exists. The only path I have not exhausted is a further pass over 2025 to
2026 Reddit and BitcoinTalk activity for any post that quotes or references a hint from the
author directly, as opposed to a poster's own guess.
