from research_run import setup
P = setup()
from pathlib import Path
source = Path(__file__).resolve().parents[1] / 'clues/arweave-puzzle-11.png'
from pathlib import Path
import sys,time,json,re,os
import numpy as np
from PIL import Image
import zxingcpp as z
from bip_utils import Secp256k1PrivateKey
from Crypto.Hash import keccak
KNOWN=bytes([1])*32;KA='1a642f0e3c3af545e7acbd38b07251b3990914f1';TARGET='ff2142e98e09b5344994f9beb9c56c95506b9f17'
def address(raw):
 pub=Secp256k1PrivateKey.FromBytes(raw).PublicKey().RawUncompressed().ToBytes()[1:]
 return keccak.new(digest_bits=256,data=pub).digest()[-20:].hex()
assert address(KNOWN)==KA
formats=z.BarcodeFormat.Code128|z.BarcodeFormat.ITF
binarizers=[z.Binarizer.LocalAverage,z.Binarizer.GlobalHistogram,z.Binarizer.FixedThreshold]
controls=[]
for fmt in (z.BarcodeFormat.Code128,z.BarcodeFormat.ITF):
 a=np.asarray(z.write_barcode(fmt,KNOWN.hex(),height=80))
 for b in binarizers:
  decoded=z.read_barcodes(a,formats=formats,binarizer=b)
  assert any(r.text==KNOWN.hex() and address(bytes.fromhex(r.text))==KA for r in decoded)
 controls.append((str(fmt),a))
print('SELFTEST OK: official Ethereum key/address vector and two barcode formats across three binarizers',flush=True)
fund={v['id']:v['result'] for v in json.loads((P/'funding.json').read_text())};assert int(fund[1],16)>0 and int(fund[2],16)==0
import hashlib
assert hashlib.sha256(source.read_bytes()).hexdigest()=='c6ba4b50fd75181a325f28b620438f740120925a07a23b889dda597546db87e1'
image=np.asarray(Image.open(source))[:,:,0];samples=[('full',image)]
regions=[('left_vertical_small',(410,178,513,274)),('left_vertical_wide',(500,100,686,274)),('right_vertical_wide',(975,65,1145,275)),('right_vertical_edge',(1510,62,1600,275)),('large_sail',(40,390,540,790)),('all_skyline',(210,15,1600,278))]
for name,(x0,y0,x1,y1) in regions:
 a=image[y0:y1,x0:x1];samples.append((name,a))
 for fraction in (.25,.5,.75):
  y=int(len(a)*fraction);profile=a[max(0,y-4):y+5].mean(axis=0).astype(np.uint8)
  strip=np.tile(profile,(80,1));strip=np.pad(strip,((0,0),(20,20)),constant_values=255)
  samples.append((name+'/profile/'+str(fraction),strip))
jobs=[(name,a,b,False) for name,a in samples for b in binarizers]
for pos in (len(jobs),len(jobs)//2,0):
 for name,a in controls:jobs.insert(pos,('control/'+name,a,binarizers[0],True))
t=time.monotonic()
for b in binarizers:z.read_barcodes(image,formats=formats,binarizer=b)
D=3/(time.monotonic()-t);estimate=len(jobs)/D
print(json.dumps({'jobs':len(jobs),'measured_full_image_jobs_per_second':D,'estimated_seconds':estimate}),flush=True);assert estimate<570
start=time.monotonic();found=[];decoded_meta=[];witness=[]
for i,(name,a,b,iscontrol) in enumerate(jobs):
 if time.monotonic()-start>590:raise RuntimeError('time bound')
 rows=z.read_barcodes(a,formats=formats,binarizer=b)
 if iscontrol:
  assert any(r.text==KNOWN.hex() for r in rows);witness.append(i);continue
 for r in rows:
  decoded_meta.append({'source':name,'binarizer':str(b),'format':str(r.format),'length':len(r.text)})
  if re.fullmatch('[0-9a-fA-F]{64}',r.text):
   raw=bytes.fromhex(r.text)
   try:addr=address(raw)
   except ValueError:continue
   if addr==TARGET:found.append({'key':r.text,'source':name})
assert len(witness)==6
if found:os.umask(0o077);(P/'barcode-hit.json').write_text(json.dumps(found))
result={'status':'match' if found else 'exhausted-no-match','jobs':len(jobs),'puzzle_jobs':len(jobs)-6,'controls':witness,'decoded':decoded_meta,'matches':len(found),'elapsed_seconds':time.monotonic()-start,'rate':D,'estimate':estimate,'library':'zxing-cpp==2.3.0','scope':'Code128 and ITF decoding of original, six object regions and three 9-row profiles per region, three binarizers; no custom stroke-count cipher'}
(P/'barcode-result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
