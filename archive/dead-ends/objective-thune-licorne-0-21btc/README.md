# Objective Thune: Le Secret de la Licorne (0.21021 BTC, [DEAD END])

"Objective Thune" is a French satirical essay pairing Tintin with Bitcoin, written by
Jacques Favier and Philippe Ratte, illustrated by Pamina Calisti, and published by PVH
editions in Switzerland in late 2019. The publisher hid 3 real private keys inside 3 of
210 numbered collector copies, then shuffled the copies so thoroughly that not even the
publisher knows which 3 hold them. The 3 public keys form a multisig redeem script whose
hash matches the escrow, a P2SH address funded with 0.21021 BTC since 2020 and still
untouched. The mechanism is fully understood and I have a certified oracle ready; what
is missing is not a computation, it is which 3 of 210 physical books hold the keys.

## At a glance

| | |
|---|---|
| Author | Jacques Favier and Philippe Ratte, published by [PVH editions](https://pvh-editions.com) |
| Published | 2020-03-01, [bitcoin.fr](https://bitcoin.fr/le-secret-de-la-licorne/) |
| Prize | 0.21021 BTC (about $13,243 at BTC = $63,000, 2026-08-16) |
| Chain | bitcoin |
| Escrow | `3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ` ([mempool.space](https://mempool.space/address/3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ)) |
| Last on-chain check | 2026-08-16: funded and unspent, 2 funding transactions, 21,021,000 sats, 0 spent |
| Status | DEAD END |
| Puzzle type | multisig, physical-object, book |
| Target format | 3 private keys hidden in 3 of 210 book copies; public keys form a P2SH multisig redeem script (M-of-3, Bitcoin Core 0.18.1 semantics, key order not sorted) |
| Certified oracle | yes: `tools/oracle.py --selftest` (certified against a real, already-spent 2-of-3 P2SH multisig found on-chain; it checks candidate public keys, it does not search for private keys) |
| What remains | which 3 of 210 physical book copies hold the keys (human action, not computation) |
| Series | none |

## Why this is a dead end

The escrow is real and still funded, but the material needed to solve it cannot be
obtained. The three private keys are split across 3 of only 210 numbered collector
copies of the book, and the publisher halted the print run over copyright on the
Tintin-derived artwork, so those copies were never widely distributed. Reason:
unobtainable material. Verified funded and unspent on 2026-08-16
(`3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ`). It would reopen if one of the three
key-bearing collector copies surfaces, or the authors or publisher release the keys.

## The puzzle as published

The publisher wrote on bitcoin.fr, 2020-03-01: "Trois ouvrages parmi deux-cent-dix
collectors contiennent des cles privees qui, une fois reunies, donnent acces a un tresor
de 21 millions de satoshis actuellement enfoui a cette adresse: `3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ`."
("Three books among two hundred and ten collector copies contain private keys that, once
reunited, give access to a treasure of 21 million satoshis buried at this address.") The
collector-edition product page adds: "Ils sont numerotes de 1 a 210 et parmi eux il y a
trois licornes qui cachent un secret" ("They are numbered 1 to 210 and among them are
three unicorns that hide a secret"). A journalducoin.com feature co-written with the
publisher, 2020-02-29, is the most explicit: the publisher "insera au hasard les cles
privees au coeur de trois ouvrages de collection qui furent soigneusement melanges afin
que meme lui ignore quels sont les trois Licornes" ("inserted the private keys at random
into three collector copies, then shuffled them so thoroughly that even he does not know
which three are the Unicorns"). Full quotes with links in
[clues/author-posts.md](clues/author-posts.md).

## What is understood

### Mechanism

The escrow is P2SH, and the publisher's own header illustration for the announcement
reads, in part, "Trois pairs unys ... codant sous Bitcoin Core 0.18.1 ... le # de
l'Hydre" ("three pairs united ... coding under Bitcoin Core 0.18.1 ... the hash of the
Hydra"): 3 key pairs, hashed. Bitcoin Core 0.18.x builds a P2SH multisig redeem script as
`OP_M <pk1> <pk2> <pk3> OP_N OP_CHECKMULTISIG` and does not sort the keys (BIP67 key
sorting is not applied by default in that version), so the order the 3 public keys were
entered in matters for reproducing the exact `hash160`. This is confirmed, in the
publisher's own words, to not be a cryptographic puzzle at all: 3 genuine, complete
private keys were physically inserted into 3 of 210 printed books, at random, and the
books were then shuffled. No computation, decryption, or text analysis reveals them; the
book's own narrative even winks at this, with a line about a fortune-teller: "Devinerait-
elle les cles privees? Nous ne le saurons jamais" ("Would she guess the private keys? We
will never know").

### Derivation and oracle

```
python3 tools/oracle.py --selftest
python3 tools/oracle.py "<pk1_hex> <pk2_hex> <pk3_hex>"
python3 tools/oracle.py --stdin
```

Given 2 or 3 candidate compressed public keys, the oracle rebuilds the multisig redeem
script under every key order and every M from 2 to the key count, hashes each one, and
compares the resulting P2SH address to the escrow, printing `MATCH <m>-of-<n>
<redeem_script_hex>` or `NO MATCH`. For 3 candidate keys this is 12 cheap tries over
public data already in hand, not a search for private keys.

### Certified against

`tools/oracle.py --selftest` reproduces a real, already-spent 2-of-3 P2SH multisig I
found by scanning historical blocks: transaction
[`de5af572e195ecbd7ce715be0464f79cd720b1c540c23c07a9d4e23dd24f8e47`](https://mempool.space/tx/de5af572e195ecbd7ce715be0464f79cd720b1c540c23c07a9d4e23dd24f8e47)
(block 360000, 2015-06-08) spends `3MirgPA7x9hAmRzFcERXwj1nNnBjy894sT`; I read its 3
public keys directly from the spending `scriptSig` and rebuilt the exact redeem script
and address from them. The self-test also confirms that the same 3 keys in a different
order do not reproduce the address, which is the reason key order matters for this
puzzle. Reproduced 2026-08-16.

### Established facts

1. The escrow holds 0.21021 BTC across 2 funding transactions (21,000,000 sats on
   2020-01-03, block 611139; 21,000 sats on 2020-06-19, block 635472), 0 spent,
   confirmed 2026-08-16.
2. The full text of the book (133,416 characters) contains 0 occurrences of the escrow
   address or any explicit mention of the mechanism.
3. A drawn "private key" in one panel, transcribed and tested against 4,308,174
   edit-distance-2 variants, produced 0 valid checksums; it is a fictional prop, not a
   real key (`data/` and `analysis/tested.md`, section 3).
4. A different contest by the same publisher on the same domain
   (`bc1qnqpfydv9amqewthfjmskh03t2aunafv2wvpmm6`, "Utopie p2p") is fully spent
   (6,694,793 sats funded and spent, confirmed again 2026-08-16), showing the publisher
   pays real winners and that this escrow staying untouched is not a bookkeeping
   artifact.
5. About 128 of the 210 collector copies had sold by 2021-01-16
   (`data/print_run_stock.csv`); no registry of which buyer received which copy number
   has surfaced.
6. The publisher announced a CC BY-SA release of the print files on 2025-05-02; the
   linked zip file returns HTTP 404 today and is not captured by the Wayback Machine or
   archive.today.

## What has been tested

Full ledger in [analysis/tested.md](analysis/tested.md). Summary:

| Hypothesis | Space | Method | Result | Witness | Date |
|---|---|---|---|---|---|
| the address or mechanism is spelled out in the book text | 133,416 characters | plain-text search for the address and 5 keyword variants | 0 occurrences | yes: witness terms found elsewhere in the same text | 2026-08-03 |
| the cover's hex-looking band encodes a secret | 1 image | direct visual decode | decodes to the public genesis block hash, not a secret | yes: matches the known genesis hash exactly | 2026-08-03 |
| the drawn "private key" panel is a real WIF | 4,308,174 edit-distance-2 variants | checksum validation | 0 valid checksums | yes: known-good WIF accepted, 1-character variant rejected | 2026-08-03 |
| the publisher does not pay real winners | 1 sibling contest | on-chain balance check | refuted: the sibling contest is fully spent | yes: mempool.space, rechecked 2026-08-16 | 2026-08-16 |
| library and marketplace registries name a marked copy | 12 registries queried | direct query, witness query proven first | 2 registries returned data (1 library copy, 1 unmarked standard copy for sale), the rest unconfirmed (client-side or anti-bot blocks) | mixed: 4 confirmed empty, 8 unconfirmed | 2026-08-03 |

## Open leads, ranked

None while the reason above holds. It reopens only if the three key-bearing collector
copies surface, or the authors or the publisher release the keys.

## Files in this folder

| Path | What it is |
|---|---|
| `clues/author-posts.md` | short verbatim quotes from the publisher and press, with dates and links |
| `data/funding.csv` | the 2 funding transactions, full txids, from mempool.space |
| `data/print_run_stock.csv` | remaining collector-edition stock over time, from archived product-page JSON |
| `analysis/tested.md` | full negatives ledger |
| `analysis/leads.md` | full lead notes |
| `tools/oracle.py` | P2SH multisig checker: candidate public keys to a derived address |

## Sources

- ["Le secret de la Licorne"](https://bitcoin.fr/le-secret-de-la-licorne/), bitcoin.fr, 2020-03-01
- Objective Thune, collector edition product page, `plaisirvaleurdhistoire.com` (archived: [web.archive.org, 2021-01-16](https://web.archive.org/web/20210116213114/https://www.plaisirvaleurdhistoire.com/shop/objective-thune/222-soutien-licorne-financement-participatif-d-une-collection-bitcoin.html))
- journalducoin.com, interview with the publisher, 2020-02-29
- [PVH editions](https://pvh-editions.com), publisher site, checked 2026-08-16
- [mempool.space](https://mempool.space/address/3Jf995GANG4EmFBK89byNNyZdtB3ELXJsZ), escrow address, checked 2026-08-16
