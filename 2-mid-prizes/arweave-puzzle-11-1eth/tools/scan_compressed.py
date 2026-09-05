from research_run import setup
P = setup()
from pathlib import Path
source = Path(__file__).resolve().parents[1] / 'clues/arweave-puzzle-11.png'
from pathlib import Path
import numpy as np, hashlib,re,time,json,os,sys,zlib,gzip
from PIL import Image
from bip_utils import Secp256k1PrivateKey
from Crypto.Hash import keccak
TARGET='ff2142e98e09b5344994f9beb9c56c95506b9f17'
NSECP=0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
KNOWN=bytes([1])*32;KNOWN_ADDR='1a642f0e3c3af545e7acbd38b07251b3990914f1'
def address(raw):
 if len(raw)!=32 or not 0<int.from_bytes(raw,'big')<NSECP:return None
 pub=Secp256k1PrivateKey.FromBytes(raw).PublicKey().RawUncompressed().ToBytes()[1:]
 return keccak.new(digest_bits=256,data=pub).digest()[-20:].hex()
assert address(KNOWN)==KNOWN_ADDR
assert address(bytes(32)) is None
HEX=re.compile(rb'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])')
MAGIC=re.compile(rb'\x78[\x01\x5e\x9c\xda]|\x1f\x8b\x08')
valid_archives=0
real_scan=False
saved_payloads=0
def candidates(data):
 global valid_archives,saved_payloads
 for marker in MAGIC.finditer(data):
  pos=marker.start();view=memoryview(data)[pos:pos+1048576]
  try:
   dec=zlib.decompressobj(31 if data[pos:pos+3]==b'\x1f\x8b\x08' else 15)
   payload=dec.decompress(view,1048576)
   if not dec.eof:continue
  except zlib.error:continue
  valid_archives+=1
  if real_scan and payload and saved_payloads<20:
   folder=P/'decompressed-private';folder.mkdir(mode=0o700,exist_ok=True)
   fd=os.open(folder/(str(saved_payloads)+'.bin'),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
   with os.fdopen(fd,'wb') as f:f.write(payload)
   saved_payloads+=1
  if len(payload)==32:yield pos,payload
  for m in HEX.finditer(payload):yield pos,bytes.fromhex(m.group().decode())
# Independent scalar bit encoder for controlled grayscale arrays. All expected keys are public vector data.
def extract(flat,planes,reverse=False,offset=0):
 bits=np.stack([(flat>>p)&1 for p in planes],axis=1).ravel()
 return np.packbits(bits[offset:],bitorder='little' if reverse else 'big').tobytes()
controls=0
for planes in [(0,),(7,),(0,1),(3,2,1,0)]:
 for rev in (False,True):
  for offset in (0,3,7):
   payload=b'\0'+zlib.compress(KNOWN.hex().encode())+b'\0'+gzip.compress(KNOWN,mtime=0)+b'\0';width=len(planes)
   values=[0]*((offset+len(payload)*8+width-1)//width)
   for k in range(len(payload)*8):
    bit=(payload[k//8]>>(k%8 if rev else 7-k%8))&1
    i,sub=divmod(k+offset,width);values[i]|=bit<<planes[sub]
   output=extract(np.array(values,dtype=np.uint8),planes,rev,offset)
   assert sum(address(raw)==KNOWN_ADDR for pos,raw in candidates(output))==2;controls+=2
print(json.dumps({'selftest':'passed','public_key_vector':'ethereum eth-keys README 01*32','codec_witnesses':controls}),flush=True)
if '--selftest' in sys.argv:raise SystemExit
fund={v['id']:v['result'] for v in json.loads((P/'funding.json').read_text())}
assert int(fund[1],16)>0 and int(fund[2],16)==0
assert hashlib.sha256(source.read_bytes()).hexdigest()=='c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1'
a=np.array(Image.open(source));assert a.shape==(1105,1600,2)
selections=[(i,) for i in range(8)]+[tuple(range(n)) for n in (2,3,4)]+[tuple(reversed(range(n))) for n in (2,3,4)]
# Eight raster directions: original/transposed, both horizontal and vertical directions.
N=8*4*len(selections)*2*8
probe=a[:,:,0].ravel();t=time.monotonic()
for planes in selections:
 bits=np.stack([(probe>>p)&1 for p in planes],axis=1).ravel()
 for rev in (False,True):
  for offset in range(8):list(candidates(np.packbits(bits[offset:],bitorder='little' if rev else 'big').tobytes()))
probe_time=time.monotonic()-t;D=(len(selections)*16)/probe_time;estimate=N/D*1.5
print(json.dumps({'streams':N,'measured_streams_per_second':D,'estimated_seconds_including_interleave_factor':estimate}),flush=True)
assert estimate<570
valid_archives=0;real_scan=True
start=time.monotonic();done=0;seen=set();occurrences=0;hits=[]
for transpose in (False,True):
 base=a.transpose(1,0,2) if transpose else a
 for fy in (False,True):
  for fx in (False,True):
   oriented=base[::-1 if fy else 1,::-1 if fx else 1,:]
   for channel in ('L','A','LA','AL'):
    flat=oriented[:,:,0].ravel() if channel=='L' else oriented[:,:,1].ravel() if channel=='A' else oriented[:,:,::(-1 if channel=='AL' else 1)].ravel()
    for planes in selections:
     bits=np.stack([(flat>>p)&1 for p in planes],axis=1).ravel()
     for reverse in (False,True):
      for offset in range(8):
       if time.monotonic()-start>590:raise RuntimeError('time bound')
       output=np.packbits(bits[offset:],bitorder='little' if reverse else 'big').tobytes();done+=1
       for pos,raw in candidates(output):
        occurrences+=1
        if raw in seen:continue
        seen.add(raw);addr=address(raw)
        if addr==TARGET:hits.append({'key':raw.hex(),'transpose':transpose,'fy':fy,'fx':fx,'channel':channel,'planes':planes,'reverse':reverse,'offset':offset,'position':pos})
assert done==N
if hits:os.umask(0o077);(P/'compressed-hit.json').write_text(json.dumps(hits))
result={'status':'match' if hits else 'exhausted-no-match','streams':done,'decompressed_key_occurrences':occurrences,'valid_archives':valid_archives,'saved_private_payloads':saved_payloads,'unique_keys':len(seen),'matches':len(hits),'codec_witnesses':controls,'elapsed_seconds':time.monotonic()-start,'measured_streams_per_second':D,'estimated_seconds':estimate,'planes':selections,'scope':'zlib headers 7801/785e/789c/78da and gzip magic in 7168 pixel bitstreams, checksum/EOF required, at most 1MiB compressed/decompressed per stream; isolated hex64 or exactly32 raw bytes in decompressed payload'}
(P/'compressed-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
