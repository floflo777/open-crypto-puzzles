# Tested hypotheses, full ledger

Summary table is in the README. This file has the full detail behind each row. All
counts and witness claims below are re-read from the private research folder's own
established-facts register before being written here. A review on 2026-07-28 found
that an appearance-based acceptance filter used in about 46% of the folder's scripts
(98 of 213) had been silently rejecting the correct answer shape for years, because
it required decrypted plaintext to look like printable ASCII when the expected
plaintext is raw key material. The negatives below post-date that fix: nothing here
judges a candidate on how it looks, only on whether it reproduces the target address
exactly.

## 1. Letter-to-bit mask reduction of the 256-symbol object

The final odd-position stream of the puzzle's own Bifid decoding step reduces, after
removing the two Base58-ambiguous letters I and O, to exactly 256 symbols drawn from
a 23-letter alphabet. The most direct hypothesis is that each symbol maps to one bit
of a 256-bit key.

Method: every letter-to-bit mask, tested both in linear reading order and under 20
spatial reading orders (row-major, column-major, spiral, boustrophedon, and their
reverses).

Result: 335,000,000 submissions, 0 match. Witness: yes, two independent
implementations reproduced the same negative and an injected known-good object was
correctly flagged by both. Date: 2026-07-28.

## 2. 16+7 partitions of the 256-symbol object's alphabet

Hypothesis: the 23-letter alphabet splits into a 16-letter and a 7-letter group
(echoing "23 individuals, 16 female, 7 male" from the source text the final page's
prose is adapted from), each group indexing a different half of the key.

Method: all 245,157 possible 16+7 partitions of a 23-symbol alphabet, both
polarities.

Result: 490,314 submissions (245,157 x 2), 0 match. Witness: yes, autotest by
injecting a known-good partition into the same code path. Date: 2026-07-28.

## 3. The 32 target numbers as ASCII codes of a substring

Hypothesis: the 32 numbers the final gate expects are the ASCII codes of 32
consecutive characters taken from one of the puzzle's known decoded objects.

Method: 10 candidate source objects x 2 letter cases x 2 reading directions x every
window of 32 consecutive characters x 2 value conventions (direct ASCII, or the
letter's rank in the reduced alphabet).

Result: 34,000 candidates, 0 match. Witness: yes. Date: 2026-07-28.

## 4. The 256-symbol object read as a single Base58 number

Hypothesis: the object, or the string it derives from, is a private key written
directly in Base58 (matching the object's own alphabet, which happens to exclude
the two Base58-ambiguous letters I and O).

Method: windows of 43, 44 and 45 characters (the length of a Base58-encoded 32-byte
value), every position, both reading directions, 2 extraction conventions, plus the
object read whole.

Result: 17,304 candidates, 0 match. Witness: yes. Date: 2026-07-28.

## 5. A substring of the object is Base58 to decode

A related but distinct hypothesis: some substring of the 256-symbol object, or of
the 570-character string it derives from with I and O removed, is a Base58Check
string with a valid checksum, rather than a raw private key encoding.

Method: every substring of length 21 to 64 characters, both reading directions, on
both source objects.

Result: 123,728 submissions, 0 match, and separately: zero valid Base58Check
checksum found anywhere in this space. That checksum observation is reported as a
fact, not used as a filter ahead of the address-comparison step. Witness: yes.
Date: 2026-07-28.

## 6. Direct readings of the large "Dualite" blob without a password

Hypothesis: the second, larger OpenSSL-format blob on the final page (titled
"Dualite" in the page's own markup) might be plain bits to read directly, rather
than something requiring a password.

Method: every 256-bit window (step 1 bit) of the decoded blob, submitted directly
to the address comparison, no key involved.

Result: 59,269 submissions, 0 match. A companion entropy measurement (byte
histogram, autocorrelation) on the same blob shows it is indistinguishable from
well-formed AES-CBC ciphertext, not from noise or a decorative filler value.
Witness: yes, on both the submission sweep and the entropy measurement.
Date: 2026-07-30. This narrows the interpretation (it is encrypted data with an
unknown key, not noise to read directly) without narrowing the space of possible
passwords, which has not been swept for this blob: see the README's mechanism
section for why this repository does not ship an oracle for it.

## 7. Taijitu (yin-yang) antisymmetry reading of the 256-symbol object

Hypothesis: the object, read as a binary image under some letter-to-bit mask, forms
a taijitu (rotationally antisymmetric) pattern, echoing a creator hint about a
"ying yang".

Method: analytic check, not a search: for every one of the 128 possible letter
pairings needed to test 180-degree rotational antisymmetry under any mask, checked
whether at least one pair of positions is forced to carry the same letter twice.

Result: every one of the 128 pairings fails this check, so no letter-to-bit mask can
produce a taijitu from this object. Refuted analytically; no submissions needed.
Date: 2026-07-28.

## 8. A partial replay of literal candidate strings from the folder's own history

Hypothesis: among literal password guesses tried by scripts written over several
years, some were built correctly but never reached a real address comparison,
because of the appearance-based filter bug described above.

Method: 13,090 literal strings harvested from 1,017 archived scripts that contain
password-guessing logic, submitted directly to an address comparison with zero
rejection ahead of that comparison; separately, the single most-repeated candidate
family across the same archive (69,454 variants).

Result: 46,589 plus 69,454 submissions, 0 match. Witness: yes, head, middle and
tail witnesses recovered. Date: 2026-07-28. This is explicitly a partial replay,
not a completed one: it covers literal strings only, not the patterns those same
scripts constructed dynamically at run time (concatenations, permutations, chained
derivations). Those dynamic patterns are the subject of the open lead ranked first
in the README; this row is why that lead is ranked first rather than closed.

## 9. The small-blob pipeline, first sweeps

The rows above test the 256-symbol object and the large blob. None of them tests the
small-blob pipeline `tools/oracle.py` implements (candidate answer to sha256 password to
AES decrypt to 32-byte key to address). These rows are the first sweeps of it.

Every sweep below was first run against the shipped oracle, which derived the AES key with
EVP_BytesToKey/MD5. That derivation is wrong for this puzzle (see section 10). The counts
and results here are from the re-run under EVP_BytesToKey/SHA-256; the earlier results are
void rather than negative, and are not reported.

Method: candidates pushed through the corrected oracle with no filter ahead of the address
comparison. PKCS7 padding rejects about 255 of every 256 wrong passwords before any
elliptic-curve work, measured at 0.35 percent of random passwords producing valid padding
against 0.39 percent expected, which is what makes this pipeline cheap to sweep. Measured
rate 76,803 candidates per second per core.

| Configuration | Candidates | Result |
|---|---|---|
| Puzzle vocabulary and stage names, each in four cases and reversed | 273 | 0 match |
| Ordered pairs of that vocabulary | 74,256 | 0 match |
| Suffixes and prefixes of the Architect message | 4,174 | 0 match |
| Every contiguous word window up to 14 words of the Architect message, the VIC plaintext, and the phase-2 and phase-3 decryptions | 49,808 | 0 match |
| Last-N-word readings of every stage text, in the conventions the pages state | 5,608 | 0 match |
| Live-page prose re-fetched from the site, SalPhaseIon and Cosmic Duality terms | 17,125 | 0 match |
| The system word list, each entry in four cases and reversed | 1,194,789 | 0 match |
| Confirmed stage passwords and their pairwise concatenations, including the phase-1 form password recovered from the hidden POST form on the theseedisplanted page | 12,544 | 0 match |

Result: 1,358,577 submissions, 0 match. Witness: yes, the corrected oracle reproduces two
real puzzle blobs from their known passwords (section 10). Date: 2026-08-19.

## 10. Key derivation: the shipped oracle used the wrong digest

Not a candidate sweep. `tools/oracle.py` derived the AES key with EVP_BytesToKey/MD5, and
its docstring described MD5 as "the scheme used throughout this puzzle's earlier stages".
That is false, and it is checkable against the puzzle's own material.

Method: the phase-2 and phase-3 blobs were re-fetched from the live page and decrypted
with their known stage passwords under both digests.

| blob | password | MD5 | SHA-256 |
|---|---|---|---|
| phase 2 | sha256 of the stage answer | padding invalid, 35 percent printable | padding valid, 100 percent printable, known plaintext |
| phase 3 | sha256 of the concatenated parts 1 to 7 | padding invalid, 38 percent printable | padding valid, 100 percent printable, known plaintext |

The phase-3 password digest was recomputed independently and reproduces the digest the
community published, which confirms the password string as well as the digest choice.

Why the old selftest passed anyway: its part 2 encrypted a self-made blob with the same
derivation it then decrypted with. A round trip certifies self-consistency, not the digest
choice, and cannot fail on a wrong constant used on both sides. `tools/oracle.py` now
certifies against the phase-2 blob instead, and asserts that MD5 fails on it.

Scope, corrected 2026-08-19: it is proven that MD5 fails on the phase-2 and phase-3
blobs, which is enough to establish that the shipped oracle's hardcoded MD5 was wrong.
It is NOT true that MD5 is unused in this puzzle. The Cosmic Duality blob decrypts only
under EVP_BytesToKey with MD5, verified by reproducing its published plaintext hash
4f7a1e4e...c081 at 1327 bytes from the live page (see section 11). The author therefore
used both digests on different blobs, and nothing determines which the small blob uses,
because its password is unknown. Hardcoding either digest is an error; `tools/oracle.py`
now tries both.

Consequence: any negative previously obtained through the shipped oracle is uncertified
and needs re-running. Date: 2026-08-19.


## 11. Cosmic Duality is decryptable, and it uses MD5

Not a candidate sweep, and a correction to this folder's account of the large blob. Row 6
and the README describe the "Dualite" / Cosmic Duality blob as never successfully
decrypted under any tested password. It has been decrypted, publicly, and the result
reproduces here from primary sources.

Method: the key is the XOR chain of the SHA-256 digests of seven tokens, in order --
matrixsumlist, enter, lastwordsbeforearchichoice, thispassword, matrixsumlist,
yourlastcommand, secondanswer -- giving
a795de117e472590e572dc193130c763e3fb555ee5db9d34494e156152e50735. Those 32 raw bytes are
then used as the password to EVP_BytesToKey with MD5 against the blob published on the
SalPhaseIon page.

Result: 1327 bytes of high-entropy output, SHA-256
4f7a1e4efe4bf6c5581e32505c019657cb7b030e90232d33f011aca6a5e9c081. Both the key and the
plaintext hash were reproduced independently here from the live page, matching the
published values exactly. Witness: yes, the reproduction is the witness. Date: 2026-08-19.

Note that four of the seven tokens are the strings this folder already documents from the
SalPhaseIon page. They are ingredients in a key derivation, not the answer string the
small blob's password is built from; reading `lastwordsbeforearchichoice` and
`thispassword` as an instruction naming the small blob's password (section 9's last-words
sweeps) is therefore probably the wrong reading of them.

Consequence for the small blob: since the puzzle demonstrably mixes digests, sweeps that
assume one digest cover only half the space. Section 9's sweeps assumed SHA-256 and are
negative only for SHA-256.


## 12. The Half / Better Half derivation, reproduced end to end

Not a candidate sweep. The Cosmic Duality plaintext from section 11 carries the rest of
the chain, and the whole of it reproduces here from primary sources.

Method, applied to the 1327-byte plaintext:

1. Read as a bitstream, row-major, into a 103 x 103 binary matrix. 1327 bytes is 10,616
   bits and 103 x 103 is 10,609, leaving 7 padding bits; the fit is exact.
2. Take row_sums[i] (ones per row) and col_sums[i] (ones per column).
3. secondary[i] = chr((row_sums[i] + col_sums[(i + 7) mod 103]) and 0xFF), giving 103
   characters whose ordinals lie in 80..117, i.e. exactly 38 distinct symbols.
4. Decode those 103 characters as a base-38 number with digit = ord(ch) - 80, giving 68
   bytes: 32 for "Half", 32 for "Better half", and 4 trailing.

Result: the 103-character secondary string reproduces the value published in
puzzlehunt/gsmgio-5btc-puzzle#72 exactly, and the two 32-byte values reproduce the keys
published in that repository's issue #79, which derive to:

| | compressed | uncompressed |
|---|---|---|
| Half | 1JG648yaB7Wp2dpUfcZoRSD4q35oq47vCu | 15E3pcDDXSKhvi3CLVhRTHEgd8dbVKvSZg |
| Better half | 145ZQ9siLrsXBKf465wjdyQYAP5dRwhRhQ | 1FhbJnrdq1FmeiXrpTqnpQ8jvYV7naze96 |

The private keys are already public in that issue and are not repeated here; the four
addresses above are enough to check the derivation. All four were empty when checked on
2026-08-19. Witness: yes, the reproduction from the live page is the witness.
Date: 2026-08-19.

## 13. The trailing 4 bytes complete the phase-2 variable table

The 4 bytes left over from section 12's base-38 decode are `fc0c1b02`. Read as signed
bytes they are -4, 12, 27, 2.

Those are the four unknowns in the table the phase-2 page prints as
`# X 2 S H 4 Y 0 Q B 15 #`. Two of its variables were already public: S = 32, from the
Klingon arithmetic the page gives (cha' + vagh x jav = 2 + 5 x 6), and B = -16, from the
Intel processor model number the page gives ((4i)^2). X, H, Y and Q had no published
values. With the trailing bytes supplying X = -4, H = 12, Y = 27 and Q = 2, the table
resolves in full to:

    -4, 2, 32, 12, 4, 27, 0, 2, -16, 15

This closes an object that had been partially solved since 2019 and connects two stages
that were previously unrelated in this folder's account: the phase-2 riddle table and the
tail of the Cosmic Duality decode.

Tested as password material for the small blob (decimal joins with several separators,
absolute values, hex forms, the raw byte string, the concatenated and XORed key material,
each under both key-derivation digests): 32 forms, 0 match.

Provenance note: the same reading appears in puzzlehunt/gsmgio-5btc-puzzle#88. That issue
also asserts a hidden "Salted__" blob at offset 158 of the Cosmic Duality plaintext with
salt 5bbd88ac32481bca, which is false: there is no such marker anywhere in the 1327 bytes
and those eight salt bytes occur at no offset, checked against a file whose SHA-256
matches the one that issue itself publishes. The table reading is recorded here because it
was independently verified, not because it was posted.


## 14. The "decrypted Cosmic Duality" is a padding accident

Not a candidate sweep, and a correction to sections 11 to 13. The community key (the
XOR of seven SHA-256 digests, two of the seven tokens invented) reproduces the
1327-byte reference file only under a convention the puzzle never uses: the 32 raw key
bytes passed as the password to EVP_BytesToKey with MD5. The creator's own convention,
written on the archived Phase 2 and Phase 3 page, is the hex SHA-256 of the answer as
the password with a SHA-256 key derivation, and every blob whose password is known
opens under that and no other (section 10).

Method: decrypt the large blob with 20,000 random 32-byte keys under the community's
convention and count the plaintexts with valid PKCS7 padding; measure the byte
distribution of the reference plaintext.

Result: 93 of 20,000 random keys give a valid padding (78 expected at 1 in 256), 92 of
them with exactly one byte of padding, which is the precise signature of the reference
file (1328 minus 1 = 1327 bytes). The reference plaintext's bytes are uniform. So the
community decrypt is one of the roughly 1 in 256 keys that pass padding by chance, and
its "plaintext" is noise; the 103 x 103 matrix, the row and column sums in the 80 to
117 range (which is what sums of about 51 random bits plus 51 random bits give), the
base-38 decode and the four trailing bytes of sections 12 and 13 are readings of that
noise. The two derived keys pay nothing and the phase 2 variables they "complete" had
no published values to check against. Witness: the theoretical padding rate is the
witness. Date: 2026-09-01.

Consequence: the large blob is closed, with an unknown key, as section 6 first said.
Section 11's statement that the puzzle mixes digests is withdrawn: the only digest the
creator documents is SHA-256, and `tools/oracle.py` trying both is harmless but not
evidence of a second one.

## 15. Word sequences of every text as the password of both locks

Hypothesis: "lastwordsbeforearchichoice" and "thispassword" name a run of words from a
text the solver holds, used as the OpenSSL password of the small blob; and the same
password may open the phase 3.2.2 blob, which has the same shape.

Method: every contiguous window of 1 to 20 words, every suffix and every prefix of the
Architect's monologue, the 91-letter phrase, the phase 3.2 introduction, the
checkerboard riddle, the January 2020 poem, the 2023 meta-hint, the page footer and
the complete Architect scene of the film, in 3 forms (lowercase joined, lowercase
spaced, uppercase joined) and 7 password forms, under both key derivations, against
both locks; then every window of 1 to 15 words of the transcripts of the three Matrix
films, of the Architect scene, of the page, the poem and the riddle, as password and
as text answer.

Result: 84,043 plus 321,244 candidates, 2,353,204 plus 22,487,080 decryptions,
88,675 valid paddings, 0 match. Witness: 3 synthetic blobs encrypted under the SHA
form of the first, median and last candidate, recovered by the normal path. Date:
2026-09-01. This closes the literal reading of the two directives on every text this
folder holds, including the film scene.

## 16. Stage answers, digests, matrices and visible strings

Hypothesis: the password of a lock is an earlier answer, a digest, or the literal
`matrixsumlist` applied to a matrix nobody had summed.

Method: the answers and digests of every solved stage, single (3 cases), in ordered
pairs concatenated and interleaved, answer plus digest, the 5,040 permutations of the
7 parts, round-robin interleavings and digest chains; the 14 x 14 image under 9 colour
valuations (rows, columns, diagonals, transposed), `seg3` and `seg1` as digits (a=1,
a=0, primality, prime and non-prime values) on every rectangular grid, and the page's
visible strings in exact case with spaces. 7 password forms, 2 derivations, both
locks.

Result: 15,134 plus 4,096 candidates, 423,752 plus 344,064 decryptions, 0 match.
Witness: synthetic head, middle and tail blobs recovered. Date: 2026-09-01.

## 17. Interleavings, iterated hashes, digit strings, the poem, nested layers

Hypothesis, in four parts: (a) the password is the six planted preimages, or the
stage passwords, interleaved character by character or concatenated in some order, or
a hash iterated up to 64 times; (b) the creator plants raw digit strings (the 149
digits are a planted preimage), so the page's digit strings in every convention might
be a password or a preimage; (c) the phases are named after the song "The Warning",
whose third phase asks "which flower would you be? The red rose or the black?", and
the creator's poem answers it; (d) "sixteen encryptions" means nested OpenSSL layers
inside the large blob.

Method: (a) permutations of 3 to 6 of the stage passwords and of 2 to 6 of the six
planted preimages, concatenated and interleaved, raw and hashed, and SHA-256 iterated
1 to 64 times over 20 bases; (b) the digit strings of `seg1`, `seg3`, both z-sections
and the whole stream, a=1 and a=0, both directions, as integers to bytes; (c) 60 short
answers to the flower question and the Whiterose lines, 3 cases; the exact forms of
the poem and of every authenticated hint; (d) 9,252 passwords against the large blob,
every valid plaintext checked for a `Salted__` or `U2FsdGVk` prefix. All to both locks
under 7 forms and 2 derivations, and to the planted addresses.

Result: 227,852 plus 205 plus 94 plus 9,252 candidates, 357,679 decryptions, 506
valid paddings on the large blob, none starting with a container, 0 match. Witness:
synthetic blobs at head, middle and tail in every family. Dates: 2026-09-01 and
2026-09-02.

## 18. Every substring of every object against the planted addresses

Hypothesis: the third door's preimage, or another stage's, is a substring of an
object the solver already holds.

Method: every contiguous substring of length 2 or more of `seg1`, `seg3`, both
`abba` runs, the 256-symbol object, the even stream, the 1075 and 765 token streams,
the 91-letter phrase, the large blob, the monologue, the 570-letter Bifid output, the
odd and even 285 streams, the two small blobs in base64 and the Vigenere key, in 6
forms (raw, lowercase, uppercase, each reversed), hashed with SHA-256 into a key,
compressed and uncompressed addresses compared to the planted list and the prize;
then substrings of 2 to 300 characters of the phase 3.2 plaintext, its Beaufort
block, the phase 2 and 3 plaintexts, the 149 digits, the two checkerboards, the two
FEN strings, the coordinates and the song's lyrics; then substrings of 1 to 32
characters of the digit objects under the raw and bit-reversed constructions.

Result: 25,091,219 plus 8,397,734 plus 2,992,383 candidates, 0 match on the prize or
the third door. The second pass found that the whole 149-digit string is the
preimage of "GSMG.io: part of the cipher", an attribution, not a prize hit; the third
found nothing. Witness: 4 known preimages (phase 3.2, causality, the hashed prize
address, the flower sentence) injected into the normal stream and recovered. Rate:
about 176,000 keys/s per core. Dates: 2026-09-01 and 2026-09-02.

## 19. The third door under six key constructions

Hypothesis: the unmessaged address of 2020-04-07 has a short preimage under one of
the creator's constructions: raw bytes padded on the left or on the right, bits
reversed, bytes reversed, SHA-256, SHA-256 of the reversed bits.

Method: the puzzle's vocabulary (texts, the creator's corpus, page tokens), the
system dictionary, every window of 2 to 6 words of at most 32 bytes from the puzzle
texts and the three films, pairs, and `gsmg.io/` paths built from all of these
(2,766,049 candidates, 16,596,294 keys); permutations of 1 to 5 of the words on the
image with 6 separators and 4 cases, and the image's numbers (the 24 yellow and blue
bits in both polarities, spiral ranks, the 15 and 9 counts, the index of the
off-white cell) (1,736,097); 12 colour masks of the 14 x 14 grid in 5 reading orders
as 196 or 192 bits, reversed, as raw key, SHA-256 and SHA-256 of the bit string,
plus the yellow and blue cells' indices, sums and counts and the characters at prime
ranks (1,300); the 8 image texts in every permutation, 6 transcriptions, 6 joins and 3
cases, the colour values in hex, decimal and RGB with pairs and arithmetic, and "hash
the text" of every page (1,408,731 candidates, 2,870,000 keys); the phase 2.1 riddle's
substitutions and the coordinates near the named company in 13 notations (50,501
candidates, 189,860 keys); and the prime-rank and non-prime-rank characters of every
digit object, with the prime ranks zeroed out, all substrings of at most 32 bytes
(19,542,003).

Result: 25,504,681 candidates, 0 match. Witness: the "black plus blue" mask of the
image and its reversal reproduce the two "Good job, Neo!" addresses by the normal
path, and the door-1 URL injected into the prime-rank run is recovered under both
constructions. Rate: single core, 488 s for the largest family. Dates: 2026-09-01 and
2026-09-02.

What this closes: the third door is not a word of the puzzle, a dictionary word, a
short run of words from its texts or films, a `gsmg.io/` path made of those, a reading
of the image's colours or numbers, or any page's text hashed, under any of the six
constructions.

## Cumulative

Across the 7 completed hypothesis families above (rows 1 to 7), 335,724,615
candidate submissions were made against the real address-comparison logic used in
the private research, all negative. Sections 15 to 19 add 62,647,937 candidates on
2026-09-01 and 2026-09-02 against both locks and the planted addresses, all negative
with witnesses; a `rockyou.txt` pass on both locks and the third door was still
running when that session closed and is not counted. Row 8's 116,043 submissions are reported
separately because that replay is explicitly partial. Section 9's 1,358,577 submissions
are reported separately again, because they sweep a different half of the final gate (the
small blob) and because they postdate the key-derivation correction in section 10. Rows 1 to 5 test the
hypothesis that the 256-symbol object reduces directly to a 32-byte key, bypassing
the AES blob entirely; row 6 tests the large blob without a password. Rows 1 to 8 do not
test the small-blob pipeline that `tools/oracle.py` in this folder implements
(candidate answer to sha256 password to AES decrypt); as of the private research's last
update that publicly reproducible half of the final gate had not been isolated and swept
on its own. Section 9 is the first sweep of it, and section 10 records why every result
obtained through the shipped oracle before that point has to be discarded.

## 11. Oracle fix: hex-encoded and WIF keys now read (issue #46, my314team / 314.run, 2026-10-18)

my314team reported, with a reproducible synthetic witness, that `tools/oracle.py`'s
`readings()` scored a correct password as NO MATCH when the decrypted plaintext is a
64-character ASCII hex key: none of sha256(plaintext), first32, last32 or sha256(first64)
hex-decodes, so the 32 real bytes were never recovered. They also noted that both 80-byte
locks (the SalPhaseIon small blob and the phase 3.2.2 blob) rule out a single raw 32-byte key
(which encrypts to 48 bytes under PKCS7) and fit 64 to 79 bytes: two raw keys (exactly 64,
matching "half and better half"), a 64-char hex key, a hex key with a short suffix, or text.

Reproduced here on 2026-10-18 against the shipped oracle (synthetic keys only): raw and
two-key plaintexts MATCH, a 64-char hex plaintext returned NO MATCH. `readings()` now strips
whitespace and an optional `0x`, hex-decodes 64- and 128-char hex to 32 or 64 bytes (then reads
the whole and its first and last 32), and Base58Check-decodes WIF-shaped tokens. After the fix
all five shapes (raw, two keys, hex, `0x`+hex, WIF) MATCH and `--selftest` stays green.

Open follow-up, not yet done: re-read the 11,473 valid-padding plaintexts from lead 2 through
the extended readings, and flag any decrypt that is entirely printable over 64+ bytes (a wrong
password gives that with probability about (95/256)^64, so such a plaintext is near-certain
evidence of the right password even if no reading matches an address).
