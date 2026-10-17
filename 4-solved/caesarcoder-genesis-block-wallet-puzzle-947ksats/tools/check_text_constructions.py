from research_run import setup
P = setup()
import sys,hashlib,time,json,os,unicodedata
from pathlib import Path
import candidates as c
import oracle as o
from bip_utils import Bip32Slip10Secp256k1
assert o.selftest()
fund=json.loads((P/'funding.json').read_text());assert fund['chain_stats']['funded_txo_sum']>fund['chain_stats']['spent_txo_sum']
mode=sys.argv[1];assert mode in ('prefix','path');old={};new={};start=time.monotonic()
def derive(text,path):
 seed=hashlib.pbkdf2_hmac('sha512',unicodedata.normalize('NFKD',text.decode()).encode(),b'mnemonic',2048)
 return Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path).PublicKey().RawCompressed().ToBytes()
if mode=='prefix':
 for name in ('T','Tl','Tu','J','Jl','Ju'):
  for path in c.PATHS:old[derive(c.TEXTS[name],path)]=(name,path)
 for name,text in [('prefix',c.T[:21]),('prefix_lower',c.T[:21].lower()),('prefix_upper',c.T[:21].upper())]:
  for path in c.PATHS:new[derive(text,path)]=(name,path)
else:
 for seedname,seed in [('T',c.T),('zero32',bytes(32))]:
  for name,text in [('T',c.T),('J',c.J),('prefix',c.T[:21])]:
   for encoding in ('bytes','chunks4'):
    indices=list(text) if encoding=='bytes' else [int.from_bytes(text[i:i+4].ljust(4,b'\0'),'big')&0x7fffffff for i in range(0,len(text),4)]
    path="m/48'/0'/"+'/'.join(str(x)+"'" for x in indices)+"/2'"
    for suffix in ('','/0/0'):
     node=Bip32Slip10Secp256k1.FromSeed(seed).DerivePath(path+suffix)
     new[node.PublicKey().RawCompressed().ToBytes()]=(seedname,name,encoding,suffix)
new={k:v for k,v in new.items() if k not in old}
keys=list(old)+list(new);split=len(old);n=len(keys)
N=n*n-split*split
control=o.program(o.witness_script(o.REVEALED_A,o.REVEALED_B))
def digest(a,b):return hashlib.sha256(b'\x52\x21'+a+b'\x21'+b+b'\x52\xae').digest()
t=time.monotonic()
for i in range(10000):digest(o.REVEALED_A,o.REVEALED_B)
rate=10000/(time.monotonic()-t);assert (N+3)/rate<570
print(json.dumps({'family':mode,'old_keys':split,'new_keys':len(new),'new_ordered_pairs':N,'rate':rate,'estimated_seconds':(N+3)/rate}),flush=True)
controls=[];found=[];count=0
positions={0,N//2,N}
def test(a,b,label):
 global count
 h=digest(a,b)
 if h==control:controls.append(count)
 if h==o.TARGET_PROGRAM:found.append(label)
 count+=1
k=0
for i,a in enumerate(keys):
 if time.monotonic()-start>590:raise RuntimeError('time bound')
 for j in range(split if i<split else 0,n):
  if k in positions:
   test(o.REVEALED_A,o.REVEALED_B,('control',k));positions.remove(k)
  test(a,keys[j],(old.get(a,new.get(a)),old.get(keys[j],new.get(keys[j]))));k+=1
if N in positions:test(o.REVEALED_A,o.REVEALED_B,('control',N))
assert k==N and count==N+3 and len(controls)==3
result={'family':mode,'status':'match' if found else 'exhausted-no-match','old_keys':split,'new_keys':len(new),'new_ordered_pairs':N,'stream_records':count,'controls':controls,'elapsed_seconds':time.monotonic()-start,'rate':rate,'estimate':(N+3)/rate,'matches':len(found)}
if found:
 os.umask(0o077);(P/(mode+'-hit.json')).write_text(json.dumps(found))
(P/(mode+'-result.json')).write_text(json.dumps(result,indent=2));print(json.dumps(result))
