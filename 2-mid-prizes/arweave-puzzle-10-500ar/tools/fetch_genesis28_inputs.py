#!/usr/bin/env python3
"""Fetch public source inputs only; run separately from offline candidate derivation.

Usage: python3 tools/fetch_genesis28_inputs.py <directory-outside-any-repository>
Only fixed public URLs below can be requested. No seed, passphrase or wallet file is read.
"""
import hashlib,json,pathlib,shutil,sys,urllib.request

out=pathlib.Path(sys.argv[1]).resolve()
if any((p/'.git').exists() for p in [out,*out.parents]):
    raise SystemExit('Keep source text outside a repository')
out.mkdir(parents=True,exist_ok=True)
page='https://arweave.net/1fLPMP_smP6ipdIYbYUAZtFPwO4crdYr4kMVf5uTivg'
for name,url in [('puzzle10.html',page),('genesis28-kjv.json','https://bible-api.com/Genesis+28?translation=kjv'),('genesis28-web.json','https://bible-api.com/Genesis+28?translation=web')]:
    with urllib.request.urlopen(url,timeout=30) as response:data=response.read()
    if name.endswith('.json'):data=(json.dumps(json.loads(data),indent=2)+'\n').encode()
    else:
        assert hashlib.sha256(data).hexdigest()=='1c4ba58dc8b65326cc87e7734a52e1c7fa82de61bc51f3db8617fb3a8379517c'
    (out/name).write_bytes(data)
    print(name,hashlib.sha256(data).hexdigest())
shutil.copyfile(pathlib.Path(__file__).with_name('original_page_fixture.js'),out/'original_page_fixture.js')
