const fs=require('fs'),vm=require('vm'),crypto=require('crypto');
const html=fs.readFileSync(process.argv[2],'utf8');
if(crypto.createHash('sha256').update(html).digest('hex')!=='1c4ba58dc8b65326cc87e7734a52e1c7fa82de61bc51f3db8617fb3a8379517c') throw Error('Page hash mismatch');
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]);
const bundle=scripts.find(s=>s.includes('var CryptoJS='));
const ctx=vm.createContext({document:{getElementById:()=>({}),getElementsByClassName:()=>[{}]},window:{},setTimeout:()=>{}});
vm.runInContext(bundle,ctx,{timeout:10000});
const input=JSON.parse(fs.readFileSync(0,'utf8'));
const C=ctx.CryptoJS;
const plain=ctx.decodewallet(input.ciphertext,input.answer);
const wallet=JSON.parse(plain);
const address=crypto.createHash('sha256').update(Buffer.from(wallet.n,'base64url')).digest('base64url');
if(address!==input.target)throw Error('Calibration address mismatch');
let result={address,roundtrip_ok:true};
if(input.witness!==undefined){
 let h=C.SHA512(input.witness);for(let i=0;i<11512;i++)h=C.SHA512(h);
 C.algo.AES.keySize=32;C.algo.EvpKDF.cfg.iterations=10000;C.algo.EvpKDF.cfg.keySize=32;
 result.ciphertext=C.AES.encrypt(plain,h.toString(),{salt:C.enc.Hex.parse('0011223344556677')}).toString();
 result.roundtrip_ok=ctx.decodewallet(result.ciphertext,input.witness)===plain;
 if(!result.roundtrip_ok)throw Error('Fixture round trip failed');
}
process.stdout.write(JSON.stringify(result));
