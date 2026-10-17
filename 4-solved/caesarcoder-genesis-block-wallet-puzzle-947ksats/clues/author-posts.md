# Author posts and player questions, verbatim

Every message of this puzzle is an OP_RETURN output in a transaction sent to the escrow
`bc1qfkhx02v89u2qyyyljeczw6hu9sr437y44t7ae5yf09thrdukfqesnjg2wj`. The author had no other channel until
the PGP signed message of 2026-10-17. Attribution follows the transaction inputs (rule in
`data/on-chain-dialogue.json`). Encrypted payloads (Electrum ECIES, base64 starting `QklFMQ`) are
readable only by their recipient and are shown as a size. Typographic characters are normalized to
ASCII. All times are UTC block times, fetched 2026-10-17.

**2026-08-22 02:45:22**, block 963,517, `e2aaa928a965ee02b9c9a76227383113a62f350701a18d7792372712ce501ac7`, author, 20,000 sats to the escrow

> (no message)

**2026-08-22 19:45:38**, block 963,629, `b691de3657880d9a1eabd2783b1a9fa8c5313ced338495bf10e85727012d7a77`, author, 5,000 sats to the escrow

> I made a Bitcoin puzzle using information contained in the genesis block created by Satoshi to generate the wallet.
>
> The entropy is extremely low. I didn't even need to back anything up. Everything I needed was already in the genesis block.
>
> Good luck!

**2026-08-23 01:51:20**, block 963,659, `248f690de194372564baa14e1bebf08154e2f2042ed205baa6157fdc0e3f22ea`, author, 5,000 sats to the escrow

> If you have a question, you can include it with a transaction sent directly to this address, and I will reply with a hint.
>
> Larger payments receive better hints. Dust transactions will be ignored.

**2026-08-23 14:41:38**, block 963,739, `3b2f8aef7bb8f56dc939b34465906fd8a7693b2c8718d541ea635f8780313db6`, player, 12,916 sats to the escrow

> Is the witness script a hash lock, a multisig, or something else?

**2026-08-23 15:43:56**, block 963,744, `0fb7a2f175dd7f9b8826cf2923ce4fcb56e4c7bfe252903e6dad1f87f177dfe3`, author, 12,916 sats to the escrow

> The witness script is a multisig.

**2026-08-23 18:19:26**, block 963,758, `268093b9ae56a59d2bb1a6acde588d6763fe859947b098c235031493208d3e22`, author (relayed question from a player), 16,028 sats to the escrow

> How many keys, what threshold, and how are the keys derived from genesis?

**2026-08-23 21:08:58**, block 963,768, `ef63243d374d8eabeac7e17e06cc4b1b672146dc61a8e5180eeac980cec07302`, author, 16,028 sats to the escrow

> Two keys, both required. The rest is for you to derive.

**2026-08-24 06:40:09**, block 963,823, `fe27df994d658e79bea7b4cfe2427341ce024c70c5af21b76186807eebe57072`, author (relayed question from a player), 6,345 sats to the escrow

> Are both keys from the same genesis field, and is the function a hash?

**2026-08-24 07:13:18**, block 963,829, `82a076b02643372769ac676d260ef4d9854c6bf49370ed61875fc63b8241dcfc`, author, 2,000 sats to the escrow

> Yes, both keys use the same Genesis field, and there is no hash.

**2026-08-24 08:58:20**, block 963,837, `2f5bbc7c0d031f54c9b7c8bee73eb2607d04b19019d1deac7f773eafdd1b91f8`, author (relayed question from a player), 12,843 sats to the escrow

> Is the second key derived from the first, or both from genesis independently?

**2026-08-24 14:32:47**, block 963,868, `ff884832e937f972c92c012ba235ff45b549cd1702dfd02691056da6bc1ff913`, author, 2,000 sats to the escrow

> Both keys are derived independently from Genesis.

**2026-08-24 18:01:41**, block 963,888, `69d19cc41b8a5f1e711d46069e301bb4d29223bfcf1128eb6a9236e0d3e9b96c`, player, 12,703 sats to the escrow

> Which genesis field, hash, merkle, nonce, time, headline, or pubkey?

**2026-08-24 21:35:20**, block 963,910, `eb609dfede7f61d3bf9fe79ae48e546c358ebd09c05b3cd64a22433cb784ea86`, author, 2,000 sats to the escrow

> The Genesis Block is public. Which part of it matters is for you to discover.

**2026-08-28 17:38:24**, block 964,465, `51b9f9521ca5bfae851b0f55dc3b151914b95f77eef156078a422396cd30cef2`, player, 2,000 sats to the escrow

> Prize Address?Genesis field 32 bytes or smaller?

**2026-08-28 20:15:31**, block 964,477, `84fc5defe22590a02bbe0025831be110ed6f9e0bc53c3c835a4e42479b0bf050`, player, 3,000 sats to the escrow

> Give a hint at your will!

**2026-08-28 22:45:35**, block 964,486, `610fc4d2ca1a214d99248c8188fd2973f4c51fca319ccf9ab983ac3edf4b1821`, player, 3,500 sats to the escrow

> Can you give any hint about derivation offset/rule?

**2026-08-28 23:15:28**, block 964,491, `6e94cfcbc1350a138242f97310dfd0280371a0020380cb32b2512337470c1077`, author, 5,000 sats to the escrow

> Solve it to find out. Maybe both.
> If you can't check the Genesis block, you can also use The Times newspaper!

**2026-08-28 23:50:52**, block 964,496, `8be479605bc8f2facd2036fd1b7f5cfa3a3f3920eeffee75e0004a2cff4d25d6`, author, 3,500 sats to the escrow

> Derivation rule: root -> multisig -> mainnet -> genesis_data -> script_type

**2026-09-06 15:51:27**, block 965,798, `68e79190221d2b73089b523f7f5af2a11838339a788239f4eee30d6c1d4502e7`, player, 1,000 sats to the escrow

> give another hint

**2026-09-06 19:41:00**, block 965,824, `64385a0cc5c4c712d1d9d8628e1e00364310d9ba50536ccd23c71b49ae66b96b`, author, 1,000 sats to the escrow

> I can't give hints without a question. Low-value transactions get bad hints; dust will be ignored.

**2026-09-10 20:47:36**, block 966,402, `75daa8e824abba4fe1b1a4b12f923b50291fab98743edaa1f03ef8c50bb70552`, player, 10,000 sats to the escrow

> Root = Times text as BIP32 seed? BIP39? raw key? genesis_data = BIP48 account?

**2026-09-10 21:33:46**, block 966,409, `cb47c7a73c1aaa11bfe0edce41c2ef7c9c1fec1478efd15e40b226eb502dcc18`, author, 2,000 sats to the escrow

> root = the master key derived from the BIP39 seed; genesis_data = some data from the genesis block used as the BIP48 account number.

**2026-09-11 21:25:51**, block 966,565, `6497aef4be0d5be68644296d5fcdb709c66bb20db5972f4e53f90836e27862fe`, player, 10,000 sats to the escrow

> BIP39 entropy: genesis bytes/puzzle text/img/other? words 12/24? passphrase Y/N?

**2026-09-11 23:26:17**, block 966,576, `f8f04fc04e2c4f34dc2264f85ff7944c6aa822446bc4cc082e95a52aed5c2a4c`, author, 2,000 sats to the escrow

> BIP39: 12 words; Passphrase: Y; Entropy: The data needed to solve it is publicly available in the genesis block.

**2026-09-14 13:01:13**, block 966,966, `e43647274f672f9b4eb42fff1d15f2afcaa8bfd4650823403a18a76774999169`, player (the address that later received the sweep), 10,000 sats to the escrow

> Passphrase: genesis data or your own word? How long? What built the wallet?

**2026-09-14 16:15:52**, block 966,989, `a137a898ab56180d6e9ebac602377a120511acdec0b4ebe4e806536652d3b32d`, author, 2,000 sats to the escrow

> Passphrase: Who received the first transaction? That's all I've got to say. What built the wallet are the tools that support BIPs 32, 39, and 48.

**2026-09-15 00:56:36**, block 967,045, `65f313fc58ec9bdb62166013bd0ca4f64e8e09739ed576090dfec6b0d24368fb`, player, 10,000 sats to the escrow

> (no message)

**2026-09-15 01:30:16**, block 967,051, `af08a3d048ac44c5888767890532c68b5004e44a2025daf0cbbbb8281a6ee9d9`, player, 4,500 sats to the escrow

> Passphrase sha256 first 8 hex? Entropy: raw 16B slice of Times or sha256?

**2026-09-15 03:19:01**, block 967,064, `a3878ff0c813a726c755e5b1220b69dc3528989fea1095041a8edadefc269fc4`, author, 2,000 sats to the escrow

> No, the passphrase is a name. The entropy isn't the raw 16 bytes.

**2026-09-15 09:34:13**, block 967,106, `b073a2ef7a9a51e8431d48315bfe9f1804a34f5169cae4678af9d92a03860a7b`, player, 10,000 sats to the escrow

> Do both cosigners use the same 12 words and the same passphrase?

**2026-09-15 14:31:15**, block 967,135, `fafdcd55a566ccebe3944b3a4cb3d4d04ced285a4b9aa3da0ccd2279eee57dad`, player, 5,000 sats to the escrow

> Were the 12 words generated from entropy, or chosen directly as words?

**2026-09-15 15:22:43**, block 967,140, `96861335409aa5dd85cc03734191832dfb5e5ff1476d4005ccdb69c286217fcf`, author, 1,784 sats to the escrow

> Perhaps... but figuring that out is part of the puzzle. The 12 words were generated from entropy.

**2026-09-16 09:02:11**, block 967,260, `de3c7aba7b3b8d3650c339041579158125546ff9d3bcfeef02fefe489a73e4d0`, player, 5,000 sats to the escrow

> Is the 128-bit entropy a zero-padded number, a digest, or neither?

**2026-09-16 12:40:51**, block 967,281, `e38caf86a0d304a4d8a10e023e75626387dbce287847d46076a48bf60be82ca2`, author, 1,848 sats to the escrow

> It's a 128-bit digest.

**2026-09-17 07:34:19**, block 967,379, `530490fd94eb76e368a0eff96db87cb1bb74ac1027aa97765a34508d877c4de4`, player, 4,000 sats to the escrow

> Passphrase fmt: first/full/middle name? spaced/joined? lower/UPPER/Capitalized?

**2026-09-17 08:02:14**, block 967,383, `ec08d0014b545776344e84214c82d556e25f11eb91f5764fc2b5b3b18faf4c99`, author, 1,813 sats to the escrow

> Passphrase: You'll have to discover the fmt through brute force. The key question greatly narrows the search space.

**2026-09-17 10:44:14**, block 967,396, `a347081cb74dd40f1a7cbe4a5dcb6f8f8a79d526cd07141c80a85e6ab6eec26e`, player, 3,000 sats to the escrow

> Digest input: typed text, raw block bytes, a file, or something else?

**2026-09-17 23:22:28**, block 967,477, `ed010443963e3601b35266a52108bd1b8dfa58e9e258a041098c05a474513fab`, author, 1,777 sats to the escrow

> The genesis block data can be viewed in binary, hex, decimal, or ASCII. If you figure out which part is being used as the entropy, just try all four forms.
>
> Want a valuable hint? Send 50k sats and I'll reveal the public keys for this address.

**2026-09-18 13:33:23**, block 967,558, `679cfe1e07b15d7cdd2e0200809e37329366dd4b88d7be01f52570e87e935649`, player, 10,000 sats to the escrow

> Is the hashed part a header field, the coinbase text, or the whole block?

**2026-09-19 20:13:07**, block 967,740, `d78593ab6288e2c9792f8c5ad8d020893d1b1dd9631eb5b1ffa5765f13029cd7`, author, 965 sats to the escrow

> Somewhere in the genesis block. The hints reveal the puzzle's shape, not the path to its solution. Brute force will be necessary to uncover it.

**2026-09-22 18:45:08**, block 968,172, `0499b89a88b5ff98569fecf404afae878ea78b2442e7b698a4ee24409f9c0661`, player, 9,000 sats to the escrow

> Which block part + which hash gives the 128-bit entropy? One line.

**2026-09-23 21:31:42**, block 968,323, `ac8c1244d4c7042102741236d580ed5ca9e3827a3412a0005b4a8581774c7036`, player, 3,000 sats to the escrow

> Can I pay 50k for the pubkeys encrypted to this tx's input pubkey (Electrum)?

**2026-09-24 02:51:06**, block 968,343, `ae906bdebdf7cd2e9b2490a727d5d91eaa203c2ae68f8461ea62e07ffe3b9b1c`, author, 448 sats to the escrow

> First 128 bits of SHA-256 hash of the genesis block's entropy.
>
> Encrypted pubkey: 50k sats output + 1k input.
>

**2026-09-24 04:33:39**, block 968,351, `040cca803909ca782fe3ba4d197740afc4ff3b353af1c5cbe06de52cfbb99792`, player (the address that later received the sweep), 50,000 sats to the escrow

> 50k+1k: please send the 2 pubkeys Electrum-encrypted to this tx's input pubkey

**2026-09-24 04:59:42**, block 968,357, `5ee1f8e2e5c7eaf571b6bbac6dc89263206d4db2c44ce71df94bb6d10924b81c`, author, 777 sats to the escrow

> [encrypted payload, 229 bytes]

**2026-09-24 09:36:20**, block 968,379, `e0f06c05c392ba186aca39eb10f5b1b7cf14c24c6a7a30e839b5ff40255a4797`, player, 50,000 sats to the escrow

> 50k+1k: please send the 2 pubkeys Electrum-encrypted to this tx's input pubkey

**2026-09-24 15:07:14**, block 968,411, `b767eb9fd162854b875e69253fe2b26464136cf2548ad0d009c69317adac1271`, author, 777 sats to the escrow

> [encrypted payload, 229 bytes]

**2026-09-24 16:37:50**, block 968,424, `5a5b5404ff410f7487b7e04c38cb0f77d3b7506304a6cf92ea23c5c1aafa89ef`, player, 20,000 sats to the escrow

> Encrypted Q to bc1qyas2 key: [encrypted payload, 357 bytes]

**2026-09-24 18:30:04**, block 968,435, `acda5891499731f5cf33afbf8a50a1a76a5e459c681ecc0253f606f68288ff66`, player, 5,000 sats to the escrow

> (a player describing their own search method; text omitted)

**2026-09-24 18:50:37**, block 968,440, `b94ae65f3f683f927f210619631991094f4c5c36a444dfc616f90f5fa0f3f571`, author, 830 sats to the escrow

> I'm curious: Are you using an LLM and brute-force attempts?
>
> Encrypted Q to bc1qax0h key: [encrypted payload, 181 bytes]

**2026-09-24 22:54:51**, block 968,461, `11856ad1037f2b3e04cddbd3ae1c0669fe66bb1f83d56e3f9f17a36be1153ad5`, player, 30,000 sats to the escrow

> Encrypted Q to bc1qyas2 key: [encrypted payload, 325 bytes]

**2026-09-24 23:26:26**, block 968,466, `39a8b5c4435df8ac703e58493102b5dba4904745c4442702d82e8c34206641ed`, author, 433 sats to the escrow

> Encrypted Q to bc1qax0h key: [encrypted payload, 725 bytes]

**2026-09-25 01:37:22**, block 968,479, `8f3c64e4f66ad662a20cddea3cb3d2ce73632f29a06494890d117a50ab122da6`, player, 330 sats to the escrow

> Only the keys may go encrypted; the rest should be public. Why not swap emails?

**2026-09-25 07:14:16**, block 968,519, `7bcd93d02f9e9e9e27f136fb25e76f5a2eeb3724dd3053c7d7373a8dbd2c40ca`, player, 1,000 sats to the escrow

> Fair enough, I understand. I might ask another one today for 30k, feel free to decline if it gives too much away. I've seen someone complaining about encrypted conversations and they are right, I benefited from public hints too and will from now on ask everything publicly. For transparency, my last question asked for the master fingerprint of one seed without the passphrase. Author declined as it would have been too easy to solve afterwards. Also, my previous encrypted question asked for the key origins (master fingerprints and derivation paths) of both cosigners. I'll keep that one private as it's strongly related to the 50k public keys question. The author is free to confirm or publish any of his replies.

**2026-09-25 15:14:12**, block 968,561, `c5f4c7ca2959b3c166f4941bcaf9debb2174017b49909a05d0a7e8a584e0e4a6`, player, 10,000 sats to the escrow

> Two quick shape questions. 1) Is the hashed input a contiguous piece of the genesis block exactly as a standard tool shows it (explorer, bitcoin-cli), or did you combine or edit parts yourself? 2) Did you get it by copy-pasting a tool's output, or by typing it yourself? Here's 10k. Let me know if my declined 30k plus this is enough, or if you'd like me to top up.

**2026-09-25 23:37:19**, block 968,601, `b1343918e8357ce355f1d7a1d71e41f79d0b17f58fa1201b294f7f8007fbc44c`, player, 20,000 sats to the escrow

> 0xflorent agreed publicly: please publish the derivation paths you sent him, or just the two BIP48 account numbers. I paid the 50k+1k for the pubkeys too.

**2026-09-25 23:37:19**, block 968,601, `e3ab67c0ad72980678f6da4e0751d765cd73c1457656232ac878cfcfec8ae882`, author, 844 sats to the escrow

> It's a contiguous piece of the genesis block, exactly as a standard tool shows it. I got it by copy-pasting the tool's output.

**2026-09-25 23:44:49**, block 968,603, `65491a02b537f727094cf9c5ea49a5b44140301929355dff132a3ef97fbcae9b`, author, 644 sats to the escrow

> Decrypted message: Offer 20k+1k (paid in this tx) for both key origins [fingerprint/48h/0h/acct'/2h], or at least both master fingerprints. Reply encrypted to this tx's input pubkey. Also: I'm really enjoying your puzzle, thank you. Let me know if encrypting ruins the game for you and I'll conform.
>
> Encrypted Q to bc1qdu8m key: [encrypted payload, 181 bytes]

**2026-09-26 16:52:17**, block 968,713, `88fc7fd69dc89b2d716814d2a1ccdc8bdf419f158c7028b37c1cb83230cda4da`, author, 500 sats to the escrow

> Decrypted message: Offer 30k+1k (paid in this tx): the master fingerprint of one cosigner's 12-word seed with an empty passphrase (not <fingerprint>/<fingerprint>, which include it). Your choice of cosigner; both if you're willing. Reply encrypted to this tx's input pubkey. Thanks!
>
> Reason for decline: The genesis block is only 2.5E-32 of the 2^128 possibilities. Revealing the seed's master fingerprint without the passphrase is basically giving away the entropy. All the secret pieces have to be cracked at the same time.

**2026-09-26 21:29:22**, block 968,745, `5216126176a1e4917f32f0a0aedc403cb23591919eb56520d43f0132a0c2aa5c`, player, 50,000 sats to the escrow

> 50k+1k: please send the 2 pubkeys Electrum-encrypted to this tx's input pubkey

**2026-09-26 22:17:53**, block 968,748, `0774617b6bf04ba6723a1ddf1f77d4103a829117d972f4a98032420aa6159102`, player, 10,000 sats to the escrow

> 10k: Y/N only. 1) Digest input = ONLY genesis coinbase Times/ASCII text (not whole block/header)? 2) Exactly tool copy-paste ASCII (bitcoin-cli/explorer)?

**2026-09-26 22:17:53**, block 968,748, `f055ffaafd001b95fae78ee9b2746efb2e76be7ce57b2cfb3657a6278770dfbb`, player, 30,000 sats to the escrow

> 30k+1k: both BIP48 account numbers (m/48'/0'/acct'/2') for both cosigners, or both full key origins. Electrum-encrypt to this tx's input pubkey.

**2026-09-26 23:36:22**, block 968,754, `e9a17ac9c9ccc8129075b1f2bfe81a3511ede9c227692fda080deef5f10f05db`, author, 810 sats to the escrow

> Encrypted Q to bc1qrzqq key: [encrypted payload, 229 bytes]

**2026-09-26 23:36:22**, block 968,754, `f1ad8d19a70c657b8438bb6fabe43dd3ab3d2df494960016dab838e897857634`, author, 836 sats to the escrow

> Encrypted Q to bc1qlahu key: [encrypted payload, 181 bytes]

**2026-09-27 00:19:30**, block 968,759, `68171cd7aa964213998ac8960940fc20df9a25d5ed6c06ca6de4e16442cf6886`, player, 20,000 sats to the escrow

> 20k+1k, structure only: 1) App that made the 12 words: iancoleman.io Entropy box, Sparrow, other? 2) Entropy Type + Event Count it showed (else char count hashed)? 3) Pasted from bitcoin-cli/explorer/hex editor?

**2026-09-27 01:39:37**, block 968,768, `457fc560caded5b020ba8d1c3543ceec0269880e1ff88bdbda14008de4079023`, author, 928 sats to the escrow

> 1) N;
> 2) N.

**2026-09-27 01:39:37**, block 968,768, `dcd7d3990e9bc4407f2146fa77fff583c26b66c12eef7e0e0832fbbed062df51`, author, 800 sats to the escrow

> 1) Apps/Tools used to generate the 12 words: bitcoin-cli, cut, jq, tr, sha256sum, iancoleman/bip39, OogaBoogaX/entropylab;
> 2) Genesis block is extremely small. This will have to be uncovered via brute-force;
> 3) Pasted from bitcoin-cli and also from an explorer.

**2026-09-27 20:18:46**, block 968,885, `67c1b1e4b8c3a220ffbe46fadb484685db7471ee74b3883146ed5b8df3ecb196`, player, 50,000 sats to the escrow

> 50k+1k: please send first8hex(sha256(passphrase UTF-8 noNL))+first8hex(sha256(12 words lowercase single-spaces)) Electrum-encrypted to this tx's input pubkey

**2026-09-28 00:10:09**, block 968,906, `d2758a2b6e2d01cb2ab5007f6340b88aa6d3b0ee31009c4c4df71be775e7ae3d`, author, 762 sats to the escrow

> Declined for the same reason as before.
>
> The puzzle wallet was built using secret components that are extremely weak on their own. Those components won't be disclosed or reduced to a searchable checksum. Revealing any one of them independently would turn part of the puzzle into an oracle for solving the others. So you'll have to recover the actual secret pieces and test them together. I won't provide any derived value that isolates any individual secret.

**2026-09-28 10:32:39**, block 968,981, `4c6ef4099a2a4263e28bae8abf17246c6b26315e2b3a9da1e5b5e646d3cb7e8c`, player, 10,000 sats to the escrow

> Shape only, one letter each. 1) jq/cut/tr changed: a) the text before sha256sum b) only sha256sum's output (e.g. cut -c1-32). 2) Words: a) Coleman "12 words" on that text b) first 32 hex as raw entropy

**2026-09-28 12:36:48**, block 968,996, `9da63c9f600f8a91b9ef90327f71422e66da22c8900f9df1491b4e78b06f56a1`, author, 947 sats to the escrow

> 1) a;
> 2) b.

**2026-09-30 21:13:21**, block 969,350, `33736aa78237fe96f94edcf48f14fb3841ff0bf42bedc3688cb5803ee42315a3`, player, 15,000 sats to the escrow

> 15k Y/N only: 1) Two different pastes for the two 12-word seeds (one cli, one explorer)? 2) Same passphrase both cosigners? 3) sha256sum input = UTF-8 text of paste (not hex-decoded binary)? 4) Ian Entropy Type = Hex (first 32 hex chars of sha256sum)?

**2026-09-30 21:13:21**, block 969,350, `faf44a9e7d572e65f0dfa96c4f32e7393e3fab600da3cdfdd5c758c9fe493218`, player, 10,000 sats to the escrow

> 10k Y/N+choice: 1) Hashed form = binary, hex, or decimal (pick one)? 2) Complete tool field value vs substring/cut? 3) Trailing newline on sha256sum input?

**2026-09-30 23:11:40**, block 969,361, `1f0f0af2aef408c25c3c813476a130cae171af2190498754c695f8d8e7b43bc2`, author, 918 sats to the escrow

> 1) N; 2) Y; 3) Y; 4) Y

**2026-09-30 23:11:40**, block 969,361, `3678a0e393de3e664f5470580d7a504b981809d35f029f4bc592b8126a133446`, author, 933 sats to the escrow

> 1) hex; 2) substring/cut; 3) N

**2026-10-01 02:26:39**, block 969,383, `734da7fc7a60f741074688d55344b70a1dbc5dc42a47e67a6353c5f2de49e770`, player, 10,000 sats to the escrow

> 10k Y/N+pick, shape only (no values): 1) Is FP 0852014c the cosigner whose iancoleman Entropy Type = Hex? 2) Is that cosigner's hashed hex copied from bitcoin-cli (vs explorer)? 3) Is the hex cut <=32 chars? 4) <=16?

**2026-10-01 02:26:39**, block 969,383, `759663153ca23f956b1f2b354550f9df547481df5b121a2a229e77d255685cef`, player, 10,000 sats to the escrow

> 10k Y/N+pick shape only: 1) Hex cut from getblock 0 raw hex (not a JSON text field)? 2) Source = header 80B / coinbase tx hex / other (pick)? 3) Cut length multiple of 2? 4) Same cut length both cosigners?

**2026-10-01 03:43:21**, block 969,390, `41a68f4a564a4fc52a25dd52c3169aaa549dcbd9310e945a06114ea934752cda`, author, 936 sats to the escrow

> 1) N; 2) genesis block; 3) Y; 4) Y

**2026-10-01 03:43:21**, block 969,390, `b050d6450f7d12eef41fae3179791c572499b653ee24665ae25adb9fe46dfd49`, author, 929 sats to the escrow

> 1) Y; 2) N (bitcoin-cli/explorer); 3) Y; 4) N

**2026-10-02 10:39:41**, block 969,576, `d98ac606deeb8f2d9efdb11abafaabc505d8fccc7a026f0e876bda68f47429a4`, player, 10,000 sats to the escrow

> Shape only, no secret values requested. For cosigner 0852014c (the one you confirmed used Coleman Hex): 1) Before sha256sum, did any command delete, translate or squeeze hex digits, beyond letter-case conversion and whitespace removal? Y/N; if Y, which operation? 2) Procedure = one SHA-256 of the UTF-8 hex text, first 32 hex digits of the digest as raw entropy, standard English BIP39, 12 words? Y/N; if N, which step differs? 3) Your hint 'first transaction' = a) genesis coinbase b) the 10 BTC payment in block 170 c) other: which block/tx? 4) Does the passphrase contain any character other than ASCII letters A-Z/a-z or a space (any digit, punctuation, accent, non-Latin letter)? Y/N

**2026-10-03 00:20:10**, block 969,650, `719623a4f2c94413b3f954e0864685aa5b7e6aead664b4f5b9efd868b7dcd7c7`, author, 874 sats to the escrow

> 1) Y; cut -b N-M: it deleted everything outside the selected range.
> 2) Y.
> 3) Key question of the passphrase: Who received the first transaction? That's all I've got to say.
> 4) N.

**2026-10-03 09:31:40**, block 969,708, `8c1e0c1b1e70d70c00142310a89240f2669f349e62673bcc3b92f0ca9d7dc29c`, player, 10,000 sats to the escrow

> 1) Is 0852014c the fingerprint of the depth-0 BIP32 master public key derived from the 12-word mnemonic with the BIP39 passphrase applied? Y/N. If N, which node does it identify (no account number needed)?
> 2) Are both escrow public keys at the complete path m/48h/0h/Xh/2h/c/i (any X), with either c=0 and i=0..9, or c=1 and i=0..4? Y/N. If N: a larger index, or a different path?
> 3) How many space characters does the passphrase contain, counting any leading or trailing space: 0, 1, 2, or 3+?

**2026-10-03 21:35:56**, block 969,766, `d2ae17e2e91a18c78bcc9d9b99c153c5d6ff55dea217f925d438745c29e11042`, author, 942 sats to the escrow

> 1) Y; 2) Y; 3) ¬_¬

**2026-10-05 09:14:09**, block 969,987, `44444289a6d96b35e0ae50a4f8b7b99acedb1e2fabcad23ae3b20258d4e43ed8`, player, 10,000 sats to the escrow

> Shape only, for 0852014c:
> 1) Is the exact text you hashed 18-32 hex digits, nothing else (no line break, CR, space, quote), that appear uninterrupted, in either letter case, inside one of: the raw block hex (it holds the header, coinbase tx, scriptSig, Times text, pubkey), block hash, merkle root, chainwork, nextblockhash, target, address hash160 - whatever tool or field you copied it from? Y/N
> 2) If N, pick: a) it has a non-hex character; b) hex digits from 2+ places joined (e.g. cut over several lines); c) hex of a value not listed; d) listed, but length/case/ending differ from item 1.
> 3) Is the passphrase exactly two words with one blank between them, each word a name of the recipient (given name or surname)? Y/N
> P.S. My memory's not that great either: youtube.com/shorts/e_8s8fn93Ww

**2026-10-05 17:24:32**, block 970,056, `221021e681efd10dad0d0988a9e27b937ef1ad1c1f90133f04866746874f4e3b`, author, 955 sats to the escrow

> 1) N; 2) d; 3) Y.

**2026-10-06 14:37:38**, block 970,185, `10edb8315de15c0aae216198e5128c0a0a28712edde8767d2ca74d0b3d1480af`, player, 10,000 sats to the escrow

> We tested 1.8M distinct passphrases of the form "name name", 2.7e11 (text, passphrase) roots in all, against both master fingerprints: 0. To tell a wrong name from a wrong algorithm, please run YOUR exact steps on this already-cut text: 000000000019d6689c08 (20 lowercase hex). sha256sum -> first 32 hex -> Coleman Entropy box, Hex, raw -> 12 words; BIP39 passphrase: Test Example; same wallet software as the puzzle. 1) First of the 12 words? 2) Master fingerprint (8 hex)?

**2026-10-06 14:37:38**, block 970,185, `8f9e8dd494fd0f51f2ff192d13c57241a2f2b24702ed405e24316943f64fdb80`, player, 10,000 sats to the escrow

> 10k+1k, shape only for 0852014c (letters/Y-N/pick; no paste, no cut indices, no PP spelling). Reply like: 1) b; 2) Y; 3) a; 4) c.
>
> 1) Your on-chain "d" (listed; length/case/ending vs clean 18-32 hex): which differences apply to the hashed text? Pick all that apply: a) length not in 18-32 b) letter case differs from the tool's usual form c) extra or missing char at one end - if c: LF, CR, space, quote, comma, or other?
> 2) Does your cut -b N-M start at byte 1 of the line/string you cut? Y/N
> 3) That line/string came from: a) bitcoin-cli piped to jq -r b) bitcoin-cli without jq c) explorer page or API
> 4) Which listed place: a) raw block hex b) block hash c) merkle root d) chainwork e) nextblockhash f) target g) address hash160

**2026-10-06 15:22:05**, block 970,190, `05ab6e90b0aea14b7a24d0a41d54c4aa3eb17239cc033d1c70f15c0259f1aa01`, author, 939 sats to the escrow

> 1) host; 2) b7f4182b

**2026-10-06 16:14:20**, block 970,198, `3e53ba380eabacce422e278a0916627e42408f4dc11e192c61039647f694b1e1`, author, 938 sats to the escrow

> 1) a; 2) N; 3) c; 4) a.

**2026-10-07 16:03:58**, block 970,358, `e6fd1907568e6afadddc6946837be741b88876d9fcb5fb39e703ba21c4de0270`, player, 10,000 sats to the escrow

> 10k+1k, shape only for 0852014c (letters/Y-N/pick; no paste, no cut indices, no PP spelling). Reply like: 1) b; 2) Y; 3) a; 4) c.
>
> 1) The explorer that supplied the raw-block hex you cut: a) blockchain.info / blockchain.com b) mempool.space c) blockstream.info d) btcscan.org e) other
> 2) That raw-block hex view was: a) compact API or raw endpoint (one continuous hex string) b) browser HTML page you copied c) a downloaded file d) other
> 3) Before cut -b, was that hex one continuous unbroken run with no newline inside the hex digits? Y/N
> 4) Reconciling Ask A (cut <=32, not <=16) with Ask E (hashed length not in 18-32), pick one: a) Ask A = cut -b range width; Ask E = resulting hashed text length (they differ if the line ends before the range end) b) both mean hashed text length; use Ask E (length not in 18-32) c) both mean hashed text length; use Ask A (still even 18-32) d) other

**2026-10-07 18:27:04**, block 970,376, `b94390c4f3da104ad344fe29b40b04e37efb578b3589bb84189d5f102ff33ada`, player, 9,000 sats to the escrow

> 9k no tip, shape only for 0852014c (letters/Y-N/pick; no paste, no cut indices, no PP spelling). Reply like: 1) Y; 2) a; 3) b; 4) N.
>
> 1) Is the continuous hex you cut the usual lowercase genesis raw-block hex of length 570 (same bytes as mempool.space /api/block/.../raw)? Y/N
> 2) If N: which? a) header hex length 160 b) coinbase/raw tx hex c) block hash d) merkle root e) other mempool continuous hex field f) not pure hex-only / not continuous after all. If Y to 1): reply "-"
> 3) After cut -b, the hashed text length was: a) even, 2-16 b) even, 34-64 c) even, 66 or more d) odd
> 4) Did your cut -b range extend past the end of the string (hashed text shorter than the range width)? Y/N

**2026-10-07 20:03:29**, block 970,385, `9750cd4ab471da045914e964c7c9100bc6d975426a6e07c22a3194c69fe67e52`, author, 881 sats to the escrow

> 1) b; 2) b; 3) Y; 4) d.
>
> 1) Y; 2) -; 3) c; 4) N.

**2026-10-08 23:41:06**, block 970,545, `9cd66237c00c5c3f3236e623d6ab258e8f2933a6662b28d63a98b8277d7a78c4`, player, 10,000 sats to the escrow

> 10k escrow, no tip. Previous ask was sent to the wrong address (tip tx 4a197e9b...). Please answer THIS ask on escrow. Shape only for FP 040e2791 (B) + PP shape. No paste, no cut indices, no PP spelling. Reply like: 1) Y; 2) Y; 3) c; 4) N; 5) Y; 6) N.
>
> 1) For 040e2791: is the continuous hex you cut the usual lowercase genesis raw-block hex of length 570 (same bytes as mempool.space /api/block/.../raw)? Y/N
> 2) Ian Coleman Entropy Type for 040e2791 = Hex (first 32 hex digits of sha256sum as raw entropy)? Y/N; if N: a) Binary b) Base 10 c) Dice d) other
> 3) After cut -b, the hashed text length was: a) even, 2-16 b) even, 34-64 c) even, 66 or more d) odd
> 4) Did your cut -b range extend past the end of the string (hashed text shorter than the range width)? Y/N
> 5) Ignoring case and spelling: is the word before the space shorter (fewer letters) than the word after? Y/N
> 6) Ignoring case and spelling: is either of the two words exactly 3 letters long? Y/N

**2026-10-09 00:18:21**, block 970,551, `9d789e14f440e38e131848948ca86af1451969f57450f39d8840ca7920df0135`, author, 1,000 sats to the escrow

> 1) Y; 2) Y; 3) c; 4) N; 5) Y; 6) N.

**2026-10-10 17:56:15**, block 970,801, `d1bd1dccbe5f7b31a9f7ffe171f0a73df996db5cf4943be615c689d349a69f4e`, player, 5,000 sats to the escrow

> Two short items, reply like: 1) b; 2) Y. 1) Your 09-26 "2.5E-32 of the 2^128 possibilities" looks like 2^23/2^128. What does your 2^23 count? a) cut -b ranges only; b) cut -b ranges x passphrase forms; c) cut -b ranges x something else about the text (case, ending, source, edits); d) a rough guess, not a count. 2) Is the passphrase a form of Hal Finney's name? Y/N

**2026-10-10 20:12:20**, block 970,820, `c41a5e9c9ccc9e16d52cf25789217dfc057a5b2e8801794854db1c136485a419`, author, 1,000 sats to the escrow

> 1) b; 2) Declined: no confirmation of candidates.

**2026-10-12 23:20:04**, block 971,153, `7bd0b87bf1e69ae6e36df004e8c2d9a7abb6cbda7eeb6ccd92bca5f47786e359`, player, 50,000 sats to the escrow

> 50k+1k: please send the 2 pubkeys Electrum-encrypted to this tx's input pubkey

**2026-10-13 00:00:33**, block 971,158, `5d8490b39fb3aa21f4b00c0608af23d9a4fe1b78984722afd56934c784d76d73`, author, 823 sats to the escrow

> Encrypted Q to bc1q7x7y key: [encrypted payload, 229 bytes]

**2026-10-13 16:51:20**, block 971,276, `5a5919bb8ffa82ba67bd81d72809985213371754397360e1ab68467bd6daac50`, player, 30,000 sats to the escrow

> 30k+1k: both BIP48 account numbers (m/48'/0'/acct'/2') for both cosigners, or both full key origins. Electrum-encrypt to this tx's input pubkey (also love the puzzle <3)

**2026-10-13 18:33:23**, block 971,283, `44834b212b60b5df2703cd1aaff654c1d85e966b9b15870e82c83846f6480a74`, player, 30,000 sats to the escrow

> 30k: both BIP48 account indices (or full key origins). Encrypt to input pubkey.

**2026-10-13 19:05:02**, block 971,287, `e067545b8eb57268555b3d4e8881f6df765fdd7a4bdf92d9d1cb7f5446e74a98`, author, 500 sats to the escrow

> Encrypted Q to bc1qpcmr key: [encrypted payload, 181 bytes]

**2026-10-13 22:50:33**, block 971,315, `6f9fe0aa1f929006de61fd29c67648260b0d5c4feba3416b45362e10fda46363`, player, 5,000 sats to the escrow

> 5k: What exact tr command did you use? Include options and operands, or NONE.

**2026-10-14 00:08:03**, block 971,322, `d416a2765ab1a61dfed4d8acb6becb52b8e890db4de6eca9452468c4fa6ca915`, author, 440 sats to the escrow

> tr -d '\n'

**2026-10-15 19:17:38**, block 971,616, `b50873ca31a944c0fbf781ebabe6ce6160569b4ff97a52c1b41b6aed8ad1df59`, player, 7,500 sats to the escrow

> Follow up on your 10-10 answer: 2^23 = cut ranges x passphrase forms Shape only, no name or values. Decline if needed, some might be too revealing :3
> 1) Number of passphrase forms counted: a) 1-32 b) 33-256 c) 257-4096 d) more
> 2) Number of cut ranges counted: a) under 2^15 b) 2^15 to 2^17 c) more than 2^17
> 3) Is each word's letter case one of: all lower, Capitalized, ALL UPPER? (y/n)
> 4) Typo in password?: (y/n)

**2026-10-16 00:21:48**, block 971,639, `a4db429eadc17e54e73385e0bd06720e8fb91c2d2b0569cef518dde43d0dd8db`, author, 500 sats to the escrow

> 1) a; 2) c; 3) Declined; 4) n.

**2026-10-16 01:16:24**, block 971,642, `ec831a9d72108dc8f844231cf106ce2029ca648f133a2f5fb4fe6c2c753e7b80`, player, 7,500 sats to the escrow

> 7.5k+1k, shape only about the two BIP48 account numbers. No values, no indices, no paste, no PP spelling. Reply like: 1) Y; 2) a; 3) b; 4) N.
> 1) Were both account numbers obtained from the genesis block data WITHOUT any hashing? Y/N
> 2) The two account numbers come from: a) the SAME contiguous piece of genesis data b) two DIFFERENT pieces of genesis data c) one from genesis data, one chosen freely d) other
> 3) How were the genesis bytes turned into the account integer? a) hex digits read as a number b) decimal digits read as a number c) a byte offset or position d) a named field's raw value (version/time/bits/nonce) e) other
> 4) Is either of the two account numbers >= 4194304 (2^22)? Y/N

**2026-10-16 02:38:46**, block 971,653, `3fee7cef9f6ec7b212368e2be38cf71bcb256441f88a3473a99af07182ba43b1`, author (by content and timing), 517 sats to the escrow

> 1) Y; 2) Declined; 3) d; 4) Y.

**2026-10-16 05:41:24**, block 971,671, `58d3b7d8a5ea665ff2d4c2f12ff253f4516a2511e25293a1acbb9a04c3a7a233`, player, 10,000 sats to the escrow

> Encrypted Q to bc1qyas2 key: [encrypted payload, 1333 bytes]

**2026-10-16 07:51:50**, block 971,685, `2dd4e0e492c132c374d76d13b81d7b2ae6389839e6a56c6c81734507d59eabd2`, author (by content and timing), 432 sats to the escrow

> Encrypted Q to bc1qdu8m key: [encrypted payload, 85 bytes]

**2026-10-16 14:12:48**, block 971,719, `29d4e3fefd5e9f57b3e50dc3c7121899e1ebf77575418624b67b022f6c7ccb21`, player, 10,000 sats to the escrow

> 10k prize + 1k reply. Small test vector for the procedure only for cosigner 0852014c Using the same data source and processing steps, but substituting 'cut -b 2-67' and BIP39 passphrase 'Test Example', what are 1) the first mnemonic word and 2) the resulting BIP32 master fingerprint? These are arbitrary test inputs; no actual puzzle cut, passphrase, seed, or account numbers are requested. Feel free to decline either part if needed.

**2026-10-16 16:23:20**, block 971,734, `f1027314f59377f908384fcf1d232c7d724a70e240adcc3c4d0f122a2a129873`, player, 10,000 sats to the escrow

> 10k, public test inputs only, no secrets. Your 10-16 reply c85bcea3 (cut -b 2-67, Test Example, 0852014c) does not match ANY standard pipeline we can build: one 570-char lowercase raw hex line gives d1642212 (no LF) or a9be51f9 (with LF). So one step differs. For that same 2-67 test run, please report:
> 1) first 40 chars of the exact text fed to sha256sum
> 2) its byte length (wc -c)
> 3) first 8 hex of the sha256sum output
> 4) exact command line(s) or tool steps, from source to sha256sum, with the cut range shown as 2-67
> 5) where the source text came from (URL/command) and how it was saved (file/paste/editor)
> If any item would reveal a secret, answer the others.

**2026-10-16 16:37:27**, block 971,736, `439cc93022c7cefda8f9eb43e4f3ad25120ef78c0bb390012a744a7de69627d1`, author (by content and timing), 514 sats to the escrow

> 1) Declined; 2) c85bcea3.

**2026-10-16 17:40:02**, block 971,743, `3de07be481e97c9ae57e38fcfd52ad40a0c0629d05603c286f47faebd3c462ec`, author (by content and timing), 447 sats to the escrow

> Declined. For a test vector with predefined inputs, I can only provide the final result. Step-level answers would be the same as uncovering the individual secrets one by one.

**2026-10-16 18:34:22**, block 971,753, `f1aeed6d1fb79335f62427da1e64f20b9f71030ca1996c2968086fae0f5b5429`, player, 10,000 sats to the escrow

> 10k+1k. Test vectors with predefined inputs, final result only, as you offered. For cosigner 0852014c, run your own source and processing steps unchanged, substituting only the cut range below and BIP39 passphrase Test Example. Reply with the BIP32 master fingerprint for each:
> 1) cut -b 1-1
> 2) cut -b 2-2
> 3) cut -b 3-3
> 4) cut -b 1-4
> 5) cut -b 1-2000
> 6) cut -b 263-400
> 7) cut -b 1-66
> Reply like: 1) xxxxxxxx; 2) ...

**2026-10-16 22:01:10**, block 971,770, `39a7dd0c74a15d11c2cc301167bcee243f458bdc54f2aa3e6a1426df44d868d6`, author (by content and timing), 490 sats to the escrow

> 1) e4caa034; 2) 9fb54bad; 3) e4caa034; 4) e79c9765; 5) 8b9b2fea; 6) 68ab4226; 7) 9290f941.

**2026-10-16 22:01:10**, block 971,770, `5b7ff44c779abced7889d70dce5299d3680140bc77f6d54e200c1c55b33ee472`, player, 10,000 sats to the escrow

> 10k+1k. Test vectors with predefined inputs, final result only, same as your last answer. For cosigner 0852014c, use your own procedure and settings unchanged, except that the cut output is the literal text given below instead of a cut of the block, with BIP39 passphrase Test Example. Reply with the master fingerprint for each:
> 1) 0
> 2) 1
> 3) 000000000019d6689c08
> Reply like: 1) xxxxxxxx; 2) ...; 3) ...

**2026-10-17 01:34:27**, block 971,789, `484fef192e43bd6c72407ad4382037f6ff3c6df985df165b3a78713bc50aa4d8`, author (by content and timing), 500 sats to the escrow

> 1) e4caa034; 2) 9fb54bad; 3) 3bc42789.

**2026-10-17 03:40:20**, block 971,803, `1c70c4745fad5bf891b9ee2a9f8b0b5cd3f328eb847eb09c9bebb92f5f7e900b`, solver, 0 sats to the escrow

> (no message; spends escrow outputs)

**2026-10-17 04:43:33**, block 971,810, `bcfc8cbeb5498d803dc1b1384233eb5e9f2da79c2077b9a0907bc0187e2e4465`, player, 350 sats to the escrow

> Shoutout to the player who cracked the puzzle!
>
> Thanks to everyone who joined in.

**2026-10-17 05:43:52**, block 971,814, `3367997d30d4b0363ff96e9fb587c28622a691044ab3ea9ce5c30c5d730b422f`, solver, 330 sats to the escrow

> (a thank-you note to the author; text omitted)

**2026-10-17 10:29:04**, block 971,840, `4b2d29ec21e2c9a37dae5ca7ddc49d6f34b0efbf4b0aa1afed6405dec8067b78`, solver, 0 sats to the escrow

> My GPU searched everywhere except the PBKDF2 settings. Well played!

**2026-10-17 17:01:47**, block 971,886, `473a314bcb3f5abc8dc4500e8d0ab80525ff65a846d55406c1e1e10fa8c8e46c`, author, 400 sats to the escrow

> -----BEGIN PGP SIGNED MESSAGE-----
> Hash: SHA512
>
>               [ PUZZLE AUTHOR ]
>
>   Handle : CaesarCoder
>   GitHub : github.com/caesrcd
>
>   PGP Fingerprint:
>   E2A0 BF0D 72D7 4483 064D
>   4FF9 3049 5240 7A6E 5C38
>
>   "Every cipher tells a story.
>    Every puzzle bears its creator's mark."
>
>               -- CaesarCoder
>
> -----BEGIN PGP SIGNATURE-----
>
> iHUEARYKAB0WIQS/k451MIi8XIQFhUUt5kqVkMnuzwUCatOdRQAKCRAt5kqVkMnu
> z9wFAP46H2ajFiutbOQFwrJEZ34BKhzYeURvKES1XR/SRctyywD9GXCc+OTV2325
> PMaeDBJCyz0dixlLWzQsncNpCPsU5gY=
> =bm1s
> -----END PGP SIGNATURE-----
>

**2026-10-17 18:03:12**, block 971,896, `d25aa1b7ada019b01ee3228f667d2881f47d7b53492d7b46b836743c1d7062f5`, solver, 0 sats to the escrow

> (no message; spends escrow outputs)
