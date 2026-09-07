#!/usr/bin/env python3
"""Offline bounded Genesis 28 readings. Never prints candidate text or key material.

Supply a local directory containing genesis28-kjv.json, genesis28-web.json,
puzzle10.html and original_page_fixture.js. No network APIs are used.
"""
import argparse,hashlib,importlib.util,json,os,pathlib,random,re,subprocess,sys,time

HERE=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('oracle',HERE/'oracle.py')
o=importlib.util.module_from_spec(spec);spec.loader.exec_module(o)

def variants(text):
    raw=' '.join(text.split())
    words=re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",raw)
    clean=' '.join(words)
    return [raw,raw.lower(),raw.upper(),clean,clean.lower(),''.join(words),''.join(words).lower(),''.join(w[:1].upper()+w[1:].lower() for w in words)]

def candidates(data,hypothesis):
    values=[]
    for tr in ('kjv','web'):
        doc=json.loads((data/f'genesis28-{tr}.json').read_text())
        verses=doc['verses']
        assert len(verses)==22 and [v['verse'] for v in verses]==list(range(1,23))
        assert all(v['chapter']==28 and v['book_name']=='Genesis' for v in verses)
        texts=[v['text'] for v in verses]
        bases=texts+[' '.join(texts[a-1:b]) for a,b in [(1,22),(10,22),(10,19),(12,19),(16,19),(18,22)]]
        if hypothesis=='H1':
            for text in bases:values.extend(variants(text))
        else:
            # A different model: numeric clues are extraction instructions on scripture.
            # 6,3,18 select verses, in that order; [0-19] selects first 20 units.
            bases=[' '.join(texts),' '.join(texts[i-1] for i in (6,3,18))]
            for text in bases:
                for v in variants(text):values.append(v[:20])
                words=re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?",text)
                values.extend(variants(' '.join(words[:20])))
                for index_base in (0,1):
                    values.extend(variants(' '.join(words[i-index_base] for i in (6,3,18))))
    return list(dict.fromkeys(values))

def node_fixture(data,witness):
    inp={'ciphertext':o.PZL8_CIPHERTEXT_B64,'answer':o.PZL8_ANSWER,'target':o.PZL8_ADDRESS,'witness':witness}
    p=subprocess.run(['node',str(data/'original_page_fixture.js'),str(data/'puzzle10.html')],input=json.dumps(inp),capture_output=True,text=True,timeout=30)
    if p.returncode:raise RuntimeError('Original-page fixture creation failed; private output suppressed')
    d=json.loads(p.stdout)
    assert d['roundtrip_ok'] and d['address']==o.PZL8_ADDRESS
    return d['ciphertext']

def save_match(candidate,output):
    if '.git' in output.parts or any((p/'.git').exists() for p in [output,*output.parents]):
        raise RuntimeError('Secret output must be outside a repository')
    output.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(output,0o700)
    wallet=json.loads(o.decode_wallet(o.CIPHERTEXT_B64,candidate))
    assert o.jwk_to_address(wallet['n'])==o.ESCROW
    f=output/'matched-wallet.json'
    fd=os.open(f,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as stream:json.dump({'answer':candidate,'wallet':wallet},stream)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data-dir',type=pathlib.Path,required=True)
    ap.add_argument('--hypothesis',choices=['H1','H2'],default='H1')
    ap.add_argument('--log',type=pathlib.Path,required=True)
    ap.add_argument('--private-output',type=pathlib.Path,required=True)
    ap.add_argument('--selftest',action='store_true')
    ap.add_argument('--plan',action='store_true')
    args=ap.parse_args();data=args.data_dir.resolve()
    if not o.selftest():raise RuntimeError('Oracle selftest failed')
    # Measure the same two-check loop with a public solved vector, before target search.
    started=time.monotonic()
    for _ in range(3):
        assert o.check(o.PZL8_ANSWER,ciphertext_b64=o.PZL8_CIPHERTEXT_B64,target=o.PZL8_ADDRESS)==(True,o.PZL8_ADDRESS)
        assert o.check(o.PZL8_ANSWER,ciphertext_b64=o.PZL8_CIPHERTEXT_B64,target=o.ESCROW)==(False,o.PZL8_ADDRESS)
    rate=3/(time.monotonic()-started)
    cs=candidates(data,args.hypothesis)
    witness=random.Random(20260905).choice(cs)
    cipher=node_fixture(data,witness)
    assert o.check(witness,ciphertext_b64=cipher,target=o.PZL8_ADDRESS)==(True,o.PZL8_ADDRESS)
    assert o.check(witness,ciphertext_b64=cipher,target=o.ESCROW)==(False,o.PZL8_ADDRESS)
    if args.selftest:print('SELFTEST OK: original JavaScript fixture and Python exact-address gate');return
    stream=[witness]+cs[:len(cs)//2]+[witness]+cs[len(cs)//2:]+[witness]
    expected=[i for i,c in enumerate(stream) if c==witness]
    report={'hypothesis':args.hypothesis,'unique_candidates':len(cs),'stream_count':len(stream),'rng_seed':20260905,'witness_positions_expected':expected,'measured_candidates_per_second':rate,'estimated_seconds':len(stream)/rate,'target':o.ESCROW,'source_sha256':{n:hashlib.sha256((data/n).read_bytes()).hexdigest() for n in ('genesis28-kjv.json','genesis28-web.json','puzzle10.html')},'oracle_sha256':hashlib.sha256((HERE/'oracle.py').read_bytes()).hexdigest(),'python':sys.version.split()[0],'node':subprocess.check_output(['node','--version'],text=True).strip(),'status':'planned'}
    args.log.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    if args.plan:return
    if report['estimated_seconds']>570:raise RuntimeError('Estimated run exceeds bounded budget; find a smaller constraint')
    start=time.monotonic();found=[];seen=[];processed=0
    for i,c in enumerate(stream):
        if time.monotonic()-start>590:
            report['status']='incomplete-time-limit';break
        match,addr=o.check(c)
        if match:
            assert addr==o.ESCROW;save_match(c,args.private_output.resolve());found.append(addr)
            report['status']='MATCH';break
        hit,_=o.check(c,ciphertext_b64=cipher,target=o.PZL8_ADDRESS)
        if hit:seen.append(i)
        processed+=1
        if processed%50==0:print(json.dumps({'processed':processed,'total':len(stream),'elapsed_seconds':round(time.monotonic()-start,2)}),flush=True)
    else:
        assert seen==expected
        report['status']='exhausted-no-match'
    report.update(processed=processed,witness_positions_found=seen,matches=found,runtime_seconds=time.monotonic()-start)
    args.log.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('RUN FAILED: '+type(exc).__name__+'; no candidate or private output displayed',file=sys.stderr)
        raise SystemExit(2)
