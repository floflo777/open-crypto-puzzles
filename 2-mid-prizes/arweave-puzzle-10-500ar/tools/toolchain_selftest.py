from bip_utils import Bip39SeedGenerator,Bip44,Bip44Coins,Bip49,Bip49Coins,Bip84,Bip84Coins,Bip86,Bip86Coins,Bip44Changes
v=' '.join(['abandon']*11+['about'])
s=Bip39SeedGenerator(v).Generate()
for cls,coins,want,path in [
 (Bip44,Bip44Coins.BITCOIN,'1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA',44),
 (Bip49,Bip49Coins.BITCOIN,'37VucYSaXLCAsxYyAPfbSi9eh4iEcbShgf',49),
 (Bip84,Bip84Coins.BITCOIN,'bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu',84),
 (Bip86,Bip86Coins.BITCOIN,'bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr',86)]:
 got=cls.FromSeed(s,coins).Purpose().Coin().Account(0).Change(Bip44Changes.CHAIN_EXT).AddressIndex(0).PublicKey().ToAddress()
 assert got==want
 print(f"SELFTEST OK m/{path}'/0'/0'/0/0 {got}")
