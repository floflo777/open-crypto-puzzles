from research_run import setup
P = setup()
from pathlib import Path
source = Path(__file__).resolve().parents[1] / 'clues/arweave-puzzle-11.png'
from pathlib import Path
import hashlib,json,time,os
from bip_utils import Secp256k1PrivateKey,Bip39SeedGenerator,Bip39MnemonicGenerator,Bip39MnemonicDecoder,Bip32Slip10Secp256k1
from Crypto.Hash import keccak
TARGET='ff2142e98e09b5344994f9beb9c56c95506b9f17';KNOWN=bytes([1])*32;KA='1a642f0e3c3af545e7acbd38b07251b3990914f1'
ORDER=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
M=' '.join(['test']*11+['junk']);MA='f39fd6e51aad88f6f4ce6ab8827279cfffb92266'
def address(raw):
 if not 0<int.from_bytes(raw,'big')<ORDER:return None
 pub=Secp256k1PrivateKey.FromBytes(raw).PublicKey().RawUncompressed().ToBytes()[1:]
 return keccak.new(digest_bits=256,data=pub).digest()[-20:].hex()
assert address(KNOWN)==KA
r=Bip32Slip10Secp256k1.FromSeed(Bip39SeedGenerator(M).Generate()).DerivePath("m/44'/60'/0'/0/0")
assert address(r.PrivateKey().Raw().ToBytes())==MA
E=Bip39MnemonicDecoder().Decode(M)
assert str(Bip39MnemonicGenerator().FromEntropy(E))==M
print('SELFTEST OK: raw Ethereum key/address vector and known Hardhat mnemonic/address vector',flush=True)
fund={v['id']:v['result'] for v in json.loads((P/'funding-strokes.json').read_text())};assert int(fund[1],16)>0 and int(fund[2],16)==0
# Public unconfirmed sixteen-bar transcription from ColdDevil, Reddit g6kefu.
# These are clue measurements, not generated secret key material.
bars=[0,0,4,7,3,6,6,9,0,2,7,6,3,6,3,7]
entropies={}
for backwards in (False,True):
 seq=bars[::-1] if backwards else bars;s=''.join(map(str,seq));packed=bytes.fromhex(s)
 variants={'ascii':s.encode(),'one-byte-per-height':bytes(seq),'hex-leftpad':packed.rjust(16,b'\0'),'hex-rightpad':packed.ljust(16,b'\0'),'decimal-big':int(s).to_bytes(16,'big'),'decimal-little':int(s).to_bytes(16,'little')}
 for name,e in variants.items():entropies.setdefault(e,[]).append((backwards,name))
rawkeys={}
for e,label in entropies.items():
 for name,key in [('leftpad',e.rjust(32,b'\0')),('rightpad',e.ljust(32,b'\0')),('sha256',hashlib.sha256(e).digest()),('sha256d',hashlib.sha256(hashlib.sha256(e).digest()).digest()),('keccak256',keccak.new(digest_bits=256,data=e).digest())]:
  if 0<int.from_bytes(key,'big')<ORDER:rawkeys.setdefault(key,[]).append((label,name))
paths=sorted({path for i in range(21) for path in (f"m/44'/60'/0'/0/{i}",f"m/44'/60'/0'/{i}",f"m/44'/60'/{i}'/0/0")})
def derive(e):
 for method in ('bip39','bip32'):
  seed=Bip39SeedGenerator(Bip39MnemonicGenerator().FromEntropy(e)).Generate() if method=='bip39' else e
  root=Bip32Slip10Secp256k1.FromSeed(seed)
  for path in paths:yield method,path,root.DerivePath(path).PrivateKey().Raw().ToBytes()
start=time.monotonic();list(derive(E));d_entropy=1/(time.monotonic()-start)
start=time.monotonic()
for i in range(1000):address(KNOWN)
d_raw=1000/(time.monotonic()-start)
rawitems=list(rawkeys);entropyitems=list(entropies)
for pos in (len(rawitems),len(rawitems)//2,0):rawitems.insert(pos,KNOWN)
for pos in (len(entropyitems),len(entropyitems)//2,0):entropyitems.insert(pos,E)
estimate=len(entropyitems)/d_entropy+(len(rawitems)+len(entropyitems)*len(paths)*2)/d_raw
print(json.dumps({'raw_candidates':len(rawkeys),'entropy_candidates':len(entropies),'paths':len(paths),'seed_methods':2,'candidate_HD_derivations':len(entropies)*len(paths)*2,'estimated_seconds':estimate}),flush=True);assert estimate<570
start=time.monotonic();found=[];rawcontrols=[];hdcontrols=[];checks=0
for i,key in enumerate(rawitems):
 addr=address(key);checks+=1
 if addr==KA:rawcontrols.append(i)
 if addr==TARGET:found.append({'private_key':key.hex(),'construction':rawkeys.get(key)})
for i,e in enumerate(entropyitems):
 for method,path,key in derive(e):
  if time.monotonic()-start>590:raise RuntimeError('time bound')
  addr=address(key);checks+=1
  if addr==MA:hdcontrols.append((i,method,path))
  if addr==TARGET:found.append({'private_key':key.hex(),'entropy_hex':e.hex(),'construction':entropies.get(e),'method':method,'path':path})
assert len(rawcontrols)==3 and len(hdcontrols)==3
if found:os.umask(0o077);(P/'sixteen-bars-hit.json').write_text(json.dumps(found))
result={'status':'match' if found else 'exhausted-no-match','raw_candidates':len(rawkeys),'entropy_candidates':len(entropies),'paths':paths,'seed_methods':['bip39-empty-passphrase','bip32-direct-seed'],'candidate_HD_derivations':len(entropies)*len(paths)*2,'total_address_checks_with_controls':checks,'raw_controls':rawcontrols,'HD_controls':hdcontrols,'matches':len(found),'elapsed_seconds':time.monotonic()-start,'estimate':estimate,'scope':'one published unconfirmed sixteen-number skyline transcription, forwards/backwards; ASCII, byte heights, packed-hex zero padding, decimal integer encodings; raw scalar padding/hash or BIP39 entropy/direct BIP32 seed'}
(P/'sixteen-bars-result.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='paths'}))
