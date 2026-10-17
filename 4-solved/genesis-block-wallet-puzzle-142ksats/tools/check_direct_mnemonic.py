from research_run import setup
P = setup()
import sys,hashlib,time,json,unicodedata,os,contextlib,io
from pathlib import Path
import candidates as c
import oracle as o
from bip_utils import Bip39SeedGenerator,Bip32Slip10Secp256k1
assert o.selftest()
def seed(s):
 return hashlib.pbkdf2_hmac('sha512',unicodedata.normalize('NFKD',s).encode(),b'mnemonic',2048)
vector='abandon '*11+'about'
assert seed(vector)==Bip39SeedGenerator(vector).Generate()
fund=json.loads((P/'funding.json').read_text())
assert fund['chain_stats']['funded_txo_sum']-fund['chain_stats']['spent_txo_sum']>0
start=time.monotonic(); keys={}
for name in ('T','Tl','Tu','J','Jl','Ju'):
 root=Bip32Slip10Secp256k1.FromSeed(seed(c.TEXTS[name].decode()))
 for path in c.PATHS:
  node=root if path=='m' else root.DerivePath(path)
  pub=node.PublicKey().RawCompressed().ToBytes()
  keys.setdefault(pub,[]).append((name,path))
records=list(keys)
control=o.program(o.witness_script(o.REVEALED_A,o.REVEALED_B))
for pos in (len(records),len(records)//2,0): records[pos:pos]=[o.REVEALED_A,o.REVEALED_B]
n=len(records); hashes=0; controls=[]; found=[]
prefixes=[b'\x52\x21'+x+b'\x21' for x in records]
suffixes=[x+b'\x52\xae' for x in records]
def digest(i,j): return hashlib.sha256(prefixes[i]+suffixes[j]).digest()
t=time.monotonic()
for i in range(10000): digest(i%n,(i*17)%n)
rate=10000/(time.monotonic()-t); est=n*n/rate
print(json.dumps({'unique_keys':len(keys),'records':n,'ordered_pairs':n*n,'hashes_per_second':rate,'estimated_seconds':est}),flush=True)
assert est<570
for i in range(n):
 if time.monotonic()-start>590: raise RuntimeError('time bound')
 for j in range(n):
  h=digest(i,j);hashes+=1
  if h==control: controls.append([i,j])
  if h==o.TARGET_PROGRAM: found.append([i,j])
assert len(controls)==9
result={'status':'match' if found else 'exhausted-no-match','family':'direct BIP39 sentence PBKDF2, six canonical text/case variants, empty passphrase, prior 214 paths, ordered compressed-key pairs','unique_keys':len(keys),'ordered_pairs':hashes,'control_hits':controls,'matches':len(found),'elapsed_seconds':time.monotonic()-start,'benchmark_hashes_per_second':rate,'estimated_seconds':est}
if found:
 os.umask(0o077)
 (P/'direct-mnemonic-hit.json').write_text(json.dumps([{'a':keys.get(records[i]),'b':keys.get(records[j])} for i,j in found]))
(P/'direct-mnemonic-result.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
