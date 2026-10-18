# Author posts and quotes

Guntis Vitolins (Managing Director, mineshop.eu) published this challenge as a
YouTube video and a blog post, both dated 2020-02-12. All quotes below are his
own published text, reproduced short and verbatim, with source and date.

## The challenge video

https://www.youtube.com/watch?v=w4mpiuBP_aY
"10 ETH challenge | Ethereum Parabolic | Bitcoin generator portfolio update !?"
(2020-02-12)

Two sentences planted in the video description, unrelated to the video's
finance topic:

> V1: "Don't expect anything easy there will be dark fog on the lake."

The same sentence continues with a short assurance that the challenge can, in
fact, be solved.

> V2: "Do you think its more likely for parrot can sing a song then for a goat
> to whistle?"

## The blog post

https://mineshop.eu/2020/02/12/crypto-pumping-hardcore-research-portfolio-update-how-are-we-doing/

Three sentences planted mid-paragraph, unrelated to the post's market
discussion:

> A1: "Round dutch cattle is living in the forest and eating wood."

> A2: "Only because there is a lot of healthy fiber."

> A3: "Hunter like the rib roast dinner fresh."

The archived HTML of this post (Wayback Machine capture, 2020-05-28) carries,
in its footer: "Posted in Blog. Tagged altcoin season, altcoins, bitcoin, bull
market, crypto pumping, ethereum, ethereum fork, round." The current live page
no longer carries these tags; the site redesign removed them.

## The 5 hints, published later in other video descriptions

Hint 1: the last word is a tropical bird.
Hint 2: word 1 names the Netherlands (also spelled "Netherland" in some of his
later descriptions).
Hint 3: word 5 is made of condensed water droplets.
Hint 4, spoken in [youtube.com/watch?v=03wXiMczCXk](https://www.youtube.com/watch?v=03wXiMczCXk)
at 15:26: a plant-based food the body cannot digest, also said to be good for
digestion. Resolves to "fiber".
Hint 5, spoken and spelled letter by letter in
[youtube.com/watch?v=ZjBJKooVmuE](https://www.youtube.com/watch?v=ZjBJKooVmuE)
at 17:28: "the keyword is fork, f-o-r-k. It's not necessarily in its place in
the order." Both official captions and an independent transcription agree on
the spelling despite both hearing "keyboard" for "keyword".

## What the author has said in comments, verbatim

Recovered 2026-08-21 by reading the comment threads under the hint 5 video
directly. This section replaces an earlier paraphrase of the same threads. The
paraphrase was right on two points and wrong on a third, so the exact wording is
reproduced here: the nesting lead in `analysis/leads.md` rests on the first
reply below.

**Thread 1.** A reader (`@nokiasixdotone1273`) asked three questions in one
comment: whether a list word can be hidden inside a longer written word, giving
as his own example a word nested inside its own negation formed with the prefix
"im-"; whether a word appearing in both the video and the post is invalidated;
and whether hint 4's word, like hint 5's, has an unconfirmed position. The
author's reply, in full, spelling his:

> "1. Yes for example usa could be united states in hints , but wikk have corect
> word in text at chalange. 2 no it doeesnt. 3 it coukd be in any positon from 12
> seed"

**Thread 2.** Asked by `@mirosomething` how the first word can be "Netherlands"
when "Netherlands" is not in the English wordlist:

> "It not necceseraly need to be exact word if you would read a post you would
> figure it our exact word."

**The correction this forces.** The example inside reply 1 is the author's own
and it is "usa" for "united states". That is an abbreviation, not a word nested
inside a longer word. The nesting example belongs to the reader who asked the
question. The earlier paraphrase of this thread, and the lead built on it,
attributed the nesting example to the author; on this evidence that attribution
is wrong. What he actually wrote is contrastive: that looser form is allowed "in
hints", but the challenge text "wikk have corect word". Thread 2 has the same
shape, with the hint saying "Netherlands" and the text carrying `dutch`. Read
together the two replies describe hints that gloss a word, not text that hides
one inside another. `analysis/leads.md` has been re-ranked accordingly.

Two other points in reply 1 confirm what the earlier paraphrase already said: a
word may appear in both sources and stay valid, and hint 4's word has no
confirmed position.

**Thread 3, unanswered.** On 2026-08-19 a reader (`@9PashaE6ashu`) argued that
the challenge is not worth searching by volume, and said of hint 5: "From where
fork was taken? It isn't mentioned anywhere (not in blog, neither in video). It
just a random word." There is no author reply as of 2026-08-21. The premise is
answerable from this file: `fork` is written, as the blog tag "ethereum fork"
quoted in the footer above. Anyone reading only the visible prose, and not the
page metadata, would reach exactly that reader's conclusion.

## The author on text shown on screen

Spoken audio of the challenge video, https://www.youtube.com/watch?v=w4mpiuBP_aY,
at 5:22 to 5:38, transcribed 2026-08-20:

> "there will be six seed phrase words from the wallet address, totally 12 seed
> phrase words. It could be anywhere in the description, with your description
> title, it could be you know written in the video on the screen so read
> carefully."

This names four video side channels: description, title, tags, and text shown on
screen. It does not say the words are in the spoken audio. The written rules in
the hint 5 video description agree, listing "description, tags, title, video
basically could be anywhere in this video".

The description, the title and the tags have all been read. The video image has
not. See `analysis/leads.md` lead 1.

## Written challenge rules

Quoted from the hint 5 video description as archived by the Wayback Machine on
2022-12-08. This is the author's own statement of the format:

> "12 wallet seed words- 6 are hidden in video .../w4mpiuBP_aY (description,
> tags, title, video basically could be anywhere in this video) 6.words are
> hidden in original post"

The 6 and 6 split is therefore the author's own, not an inference. The escrow
address given in the same rules block matches the address in `puzzle.json` and
in `tools/oracle.py`.


## Reported by profesor1234 (issue #38, 2026-10-18), not independently verified here

Author reply that retires the spoken-audio channel of lead 1, on the challenge video
https://www.youtube.com/watch?v=w4mpiuBP_aY :

- @ZeIronDucK: "I really can't hear what's the last word you saying in video ... and I guess Im needing it"
- @GuntisVitolins: "Youll need only written words."

Hint-5 verbatim, https://www.youtube.com/watch?v=ZjBJKooVmuE at 17:25:

> "so the last hint we are giving out is a keyboard fork so it's f o r k that's a keyword it's not
> necessarily uh in order um it's one of the keywords from the seed wallet"

This is the primary support for treating `fork` as a literal list member at a free position. Minor
timestamp corrections on the current uploads: hint 4 at 15:15 (not 15:26), hint 5 at 17:25 (not 17:28).
