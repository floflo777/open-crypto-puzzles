from research_run import setup
P = setup()
import sys,hashlib,time,json,os,itertools
from pathlib import Path
import candidates as c
import oracle as o
from bip_utils import Bip32Slip10Secp256k1
assert o.selftest()
fund=json.loads((P/'funding.json').read_text());assert fund['chain_stats']['funded_txo_sum']>fund['chain_stats']['spent_txo_sum']
start=time.monotonic();oldpaths=set(c.PATHS);groups=[]
roots={name:Bip32Slip10Secp256k1.FromSeed(c.TEXTS[name]) for name in ('T','Tl','Tu','J','Jl','Ju')}
for mask in itertools.product((False,True),repeat=4):
 rows={}
 for name,root in roots.items():
  for account in c.G:
   for script in (0,1,2):
    path='m/'+ '/'.join(str(v)+("'" if hard else '') for v,hard in zip((48,0,account,script),mask))
    for suffix in ('','/0/0','/0/1','/1/0'):
     full=path+suffix;pub=root.DerivePath(full).PublicKey().RawCompressed().ToBytes()
     rows.setdefault(pub,{'new':full not in oldpaths,'labels':[]})['labels'].append((name,full))
 keys=list(rows);old=sum(not rows[k]['new'] for k in keys)
 N=len(keys)**2-old**2
 if N:groups.append((mask,keys,rows,N))
N=sum(g[3] for g in groups);control=o.program(o.witness_script(o.REVEALED_A,o.REVEALED_B))
def digest(a,b):return hashlib.sha256(b'\x52\x21'+a+b'\x21'+b+b'\x52\xae').digest()
t=time.monotonic()
for i in range(10000):digest(o.REVEALED_A,o.REVEALED_B)
rate=10000/(time.monotonic()-t);assert (N+3)/rate<570
print(json.dumps({'groups':len(groups),'new_pairs':N,'rate':rate,'estimated_seconds':(N+3)/rate}),flush=True)
k=0;count=0;controls=[];found=[];positions={0,N//2,N}
def test(a,b,label):
 global count
 h=digest(a,b)
 if h==control:controls.append(count)
 if h==o.TARGET_PROGRAM:found.append(label)
 count+=1
for mask,keys,rows,n in groups:
 for a in keys:
  if time.monotonic()-start>590:raise RuntimeError('time bound')
  for b in keys:
   if not rows[a]['new'] and not rows[b]['new']:continue
   if k in positions:test(o.REVEALED_A,o.REVEALED_B,'control');positions.remove(k)
   test(a,b,(rows[a]['labels'],rows[b]['labels']));k+=1
if N in positions:test(o.REVEALED_A,o.REVEALED_B,'control')
assert k==N and len(controls)==3 and count==N+3
result={'status':'match' if found else 'exhausted-no-match','family':'six canonical T/J raw BIP32 seeds, 16 hardening patterns over 48/0/account/script, 12 prior genesis accounts, script 0/1/2, suffix empty or 0/0 0/1 1/0, pairs within same hardening pattern; old-old pairs excluded','new_ordered_pairs':N,'stream_records':count,'groups':[{'mask':m,'keys':len(ks),'pairs':n} for m,ks,r,n in groups],'controls':controls,'elapsed_seconds':time.monotonic()-start,'rate':rate,'estimate':(N+3)/rate,'matches':len(found)}
if found:os.umask(0o077);(P/'hardening-hit.json').write_text(json.dumps(found))
(P/'hardening-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
