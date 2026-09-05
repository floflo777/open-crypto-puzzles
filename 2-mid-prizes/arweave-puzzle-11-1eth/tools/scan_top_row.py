from research_run import setup
P = setup()
from pathlib import Path
source = Path(__file__).resolve().parents[1] / 'clues/arweave-puzzle-11.png'
from pathlib import Path
import numpy as np,hashlib,time,json,os
from PIL import Image
from bip_utils import Secp256k1PrivateKey
from Crypto.Hash import keccak
TARGET='ff2142e98e09b5344994f9beb9c56c95506b9f17';KNOWN=bytes([1])*32;KA='1a642f0e3c3af545e7acbd38b07251b3990914f1'
ORDER=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
def address(raw):
 if not 0<int.from_bytes(raw,'big')<ORDER:return None
 pub=Secp256k1PrivateKey.FromBytes(raw).PublicKey().RawUncompressed().ToBytes()[1:]
 return keccak.new(digest_bits=256,data=pub).digest()[-20:].hex()
assert address(KNOWN)==KA and address(bytes(32)) is None
planes=[(i,) for i in range(8)]+[tuple(range(n)) for n in (2,3,4)]+[tuple(reversed(range(n))) for n in (2,3,4)]
def windows(flat,selected,byteorder):
 bits=np.stack([(flat>>p)&1 for p in selected],axis=1).ravel()
 for off in range(8):
  length=(len(bits)-off)//8
  data=np.packbits(bits[off:],bitorder=byteorder).tobytes()[:length]
  for i in range(max(0,len(data)-31)):yield off+i*8,data[i:i+32]
# Known raw private key independently encoded at head, middle and tail of a synthetic carrier.
fixture=np.full(1600,254,dtype=np.uint8)
for start in (0,672,1344):
 for k in range(256):fixture[start+k]|=(KNOWN[k//8]>>(7-k%8))&1
found=[pos for pos,raw in windows(fixture,(0,),'big') if raw==KNOWN]
assert all(pos in found for pos in (0,672,1344))
print(json.dumps({'selftest':'passed','raw_carrier_witness_offsets':[0,672,1344]}),flush=True)
fund={v['id']:v['result'] for v in json.loads((P/'funding.json').read_text())};assert int(fund[1],16)>0 and int(fund[2],16)==0
assert hashlib.sha256(source.read_bytes()).hexdigest()=='c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1'
a=np.array(Image.open(source))[0,:,0]
# Previous raw flat-array endpoint candidates are explicitly excluded.
whole=np.array(Image.open(source))[:,:,0].ravel().tobytes();excluded={whole[:32],whole[-32:]}
keys={};raw_count=0
for selection,flat in [('all',a),('nonwhite',a[a<255])]:
 for backwards in (False,True):
  ordered=flat[::-1] if backwards else flat
  for invert in (False,True):
   data=255-ordered if invert else ordered
   for selected in planes:
    for byteorder in ('big','little'):
     for pos,raw in windows(data,selected,byteorder):
      for little in (False,True):
       key=raw[::-1] if little else raw;raw_count+=1
       if key not in excluded and 0<int.from_bytes(key,'big')<ORDER:keys.setdefault(key,(selection,backwards,invert,selected,byteorder,pos,little))
items=list(keys);N=len(items)
for pos in (N,N//2,0):items.insert(pos,KNOWN)
t=time.monotonic()
for i in range(1000):address(KNOWN)
D=1000/(time.monotonic()-t);estimate=len(items)/D
print(json.dumps({'raw_windows_with_variants':raw_count,'unique_candidate_keys':N,'records':len(items),'rate':D,'estimate':estimate}),flush=True);assert estimate<570
start=time.monotonic();controls=[];hits=[]
for i,key in enumerate(items):
 if time.monotonic()-start>590:raise RuntimeError('time bound')
 addr=address(key)
 if addr==KA:controls.append(i)
 if addr==TARGET:hits.append({'key':key.hex(),'construction':keys.get(key)})
assert len(controls)>=3
if hits:os.umask(0o077);(P/'top-row-hit.json').write_text(json.dumps(hits))
result={'status':'match' if hits else 'exhausted-no-match','raw_windows_with_variants':raw_count,'unique_candidate_keys':N,'stream_records':len(items),'controls':controls,'carrier_witness_offsets':[0,672,1344],'elapsed_seconds':time.monotonic()-start,'rate':D,'estimate':estimate,'matches':len(hits),'scope':'first image row, all pixels or nonwhite pixels, forward/backward, original/inverted grayscale, 14 bit selections, both byte bit orders and private-scalar endian orders, every 256-bit window; raw full-image endpoints excluded'}
(P/'top-row-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
