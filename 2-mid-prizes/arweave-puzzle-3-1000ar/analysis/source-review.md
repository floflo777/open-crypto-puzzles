# Source review, 2026-09-05

The puzzle remains unsolved. One bounded reading has been exhausted with planted
controls; no recovered address matched the escrow.

## Mechanism and evidence corrections

The page has 32 one-character inputs. It concatenates their values in DOM order and
lowercases the result. It inserts no spaces and performs no trimming. The embedded
ciphertext equals the constant in `tools/oracle.py`. The original page's success marker
is weaker than a solution: my oracle now requires the derived address to equal the
published escrow, with a wrong-target regression using the real solved #8 wallet.

Two regression tests cover the solved sibling and a 32-character calibration answer
encrypted by the original #3 JavaScript. The latter covers case normalization,
significant whitespace and CLI output that does not disclose the candidate.

Historical B1-B16 rows have no per-run witness evidence. Their approximate 330 million
total remains uncertified. In particular, the claimed free-slot negatives do not prove
that at least two of the current readings are wrong.

## Author and chronology

The official [October 2019 interview](https://arweave.medium.com/community-spotlight-meeting-tiamat-e484655b25e0)
describes Tiamat as a community member and Chronobot developer. It does not identify him
as an Arweave employee. He described an interest in physical puzzles and said the
permaweb's permanence and project awareness motivated the series.

The [May 2019 newsletter](https://arweave.medium.com/arweave-newsletter-may-9de22fa3700e)
documents ArweaveID and links directly to its immutable application. That establishes
that the identity service existed when #3 appeared; it does not establish a rebus answer.

I inspected the community Discord export, bounded before 2019-05-28, and extracted
683 messages from `tiamat#9131`. The later six-month, tree and image-four quotations in
the community README cannot be independently recovered from that cutoff archive.
They remain secondary-source quotations, not newly verified primary messages.

## Keep clues attached to their actual puzzle

The public tweet archive contains 403 tweet rows but no reply-parent column. I checked
parent IDs separately using the public FxTwitter response fields. Relevant chains:

| Tweet | Parent chain | Applies to |
|---|---|---|
| [Count the dots](https://twitter.com/ArweaveP/status/1152887601529073665) | 1152887601529073665 -> 1132936723162378240 | #3 |
| [Third picture obsolete](https://twitter.com/ArweaveP/status/1177235139035836417) | 1177235139035836417 -> 1152887601529073665 -> #3 announcement | #3 |
| [Tree and GoT](https://twitter.com/ArweaveP/status/1210259404806918146) | 1210259404806918146 -> 1135460147881529344 | #5 |
| [Unidentified solver / suspected brute force](https://twitter.com/ArweaveP/status/1433836440765468683) | 1433836440765468683 -> 1433779044835803152 -> 1215166354707439621 | #9 |
| [More hints at AR $100](https://twitter.com/ArweaveP/status/1429846914028158977) | 1429846914028158977 -> 1253658421162844160 -> 1252961944807641090 | #11 |

The earlier README's suggestion that an unidentified solver brute-forced #3 was
unsupported. The located 2021 statement concerns #9. None of these reply chains is a
new cryptographic negative for #3.

## H1 result and limits

I tested an ArweaveID reading of the first distorted-letter drawing, keeping the mining
reading fixed and using bounded alternatives for the other images. The eight pool sizes
were 1, 4, 1, 2, 4, 2, 3, 2: 384 unique, normalized 32-character candidates.
This was not a repeat of a historical B1-B16 configuration; overlap with their missing
candidate lists cannot be measured.

An answer selected with RNG seed 20260905 was used to re-encrypt the real solved #8
wallet using the original #3 CryptoJS bundle. The same candidate stream was checked
against both the actual ciphertext/escrow and that control ciphertext/address. Extra
copies at the head, middle and tail were found, as was its natural occurrence.

The 387-element stream finished in 225.966 seconds with no target match. Expected and
observed control positions were both `[0, 193, 302, 386]`. Calibration measured 1.7498
stream elements/second and predicted 221.168 seconds. This excludes only the exact H1
set; ArweaveID as a concept and all eight individual readings remain unproved.

Source and reproducibility details: [tools/REPRODUCE.md](../tools/REPRODUCE.md).

## Next constraint to seek

The numeric second image and letter-like first/seventh images still need an extraction
rule supported by the drawing and dated sources. More synonyms alone would only expand
uncertainty. One clean negative has been recorded; after a second, return to the source
model before starting another search. Each search must remain below ten minutes.
