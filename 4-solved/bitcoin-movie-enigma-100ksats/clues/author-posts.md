# Author posts and quotes

Short, dated material published by "klems" (Nostr
`npub10q5dpm5p05a0g3vtgcl76wv0pc4t820f5fj8qmpfaa4umv6404xqvwzvp0`) about this puzzle,
on the puzzle's own site, on X, on Instagram, and on Nostr.

## /rules page, bitcoinmovieenigma.com

Read live 2026-08-16 at https://bitcoinmovieenigma.com/rules. Verbatim (the "IMBD"
spelling is the author's, not a transcription error):

> "Guess all the 34 movie titles, from the provided movie frames. There was an
> alternative release, as a single image."

> "Transform 'somehow' each movie title into an English BIP-0039 seed word."

> "The seedphrase you have is 34 words long, but we should have a 24 words
> seedphrase instead. Some movies should not be in the sequence, and should be
> considered intruders, but which ones? You will need additional informations
> about each movie to detect those intruders 'somehow'. Every information you need
> can be found on IMBD, on each movie's page. Organize your findings in an excel
> table, unless you have a giga brain."

> "Once you got rid of the intruders, you can restore the Bitcoin wallet using the
> 24 words passphrase with any compatible software."

## /about page, bitcoinmovieenigma.com

> "I initially published this enigma on Twitter, Instagram, and Nostr. Some
> platforms compressed the movie frames poorly, therefore, I decided to set up a
> small website for it."

## /wallet page, bitcoinmovieenigma.com

The page names the escrow address directly and lists a donation ledger entry in the
author's own hand: "npub10q5dpm5p05a0g3vtgcl76wv0pc4t820f5fj8qmpfaa4umv6404xqvwzvp0
| 100000 | 4/08/2022," which matches the escrow's on-chain funding date. This
explains the gap between the 2022-04-08 funding and the January 2024 public
launch: the escrow was pre-funded by the author as a donation entry well before the
puzzle was announced, not funded at launch.

## Nostr launch note, 2024-01-03

Event `48fbbff9845680b463784d5ddfdc5907a953b3f4df9e0e49a97d6eb123d52145`
([njump](https://njump.me/48fbbff9845680b463784d5ddfdc5907a953b3f4df9e0e49a97d6eb123d52145)),
posted 2024-01-03 23:33 UTC, 518 days after the funding. It states the rules more
precisely than the site does:

> "34 movies screenshot will be posted in the proper order."

> "Each movie equals a word from the [BIP39 English] list. You need to find the trick
> to match a movie name with a word on that list."

> "Since you need 24 words, 10 screenshots from the sequence are perfectly useless
> ... but which ones :) ? I suggest that, for every movie, you go see its IMDB page,
> and find additional informations about each movie. things like Director / Year of
> release / Length / Actors starring in it / etc ...) nothing outside the first page
> of IMDB."

> "All you need is cinematic knowledge, no fancy cryptic enigma or complex
> calculations on this one."

> "This enigma was posted on Instagram and Twitter and is still ongoing, never been
> found."

The author's last Nostr event is dated 2026-08-31 (246 events read on 2026-09-01);
none after 2024 mentions the puzzle.

## X account @cryptop1r4t3, first launch 2022-04-08

Every published panel's XMP names `@cryptop1r4t3` as creator. That X account
([x.com/cryptop1r4t3](https://x.com/cryptop1r4t3)) posted the same 34 stills, in the
same order, on 2022-04-08, the day the escrow was funded, with "80% movie quiz and
20% reflexion" and "i might add clues"; no clue followed. Read on 2026-09-01; the
account's earlier hunts (February 2022) were physical caches whose passphrases were
BIP39 words.

## The 34 movie panels

Each panel is a single still from one film, published as its own numbered post
("Movie Frame #1" through "Movie Frame #34," one panel per day from 2024-01-03 to
2024-02-05 by display date) at
[bitcoinmovieenigma.com/blog/NN](https://bitcoinmovieenigma.com) and cross-posted to
X, Instagram, and Nostr in 2024-01-03/04. I do not reproduce these stills here:
each one is a frame from a third-party film, not original photography by the
author, and the site itself is still live, so I link to it rather than
redistribute the frames. An "alternative release" of the same 34 stills as a single
combined image is also linked from the rules page; I confirmed it is byte-for-byte
identical to the individual panels (34 of 34 match by MD5), so it carries no
additional information.
