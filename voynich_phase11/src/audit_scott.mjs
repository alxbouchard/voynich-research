import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';
import crypto from 'node:crypto';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const vendor=path.join(root,'tmp/vendor/scott');
fs.mkdirSync(path.join(root,'results'),{recursive:true});
const original=execFileSync('node',['decode.js'],{cwd:vendor,encoding:'utf8'});
fs.writeFileSync(path.join(root,'tmp/scott_original_stdout.txt'),original);
const code=fs.readFileSync(path.join(vendor,'decode.js'),'utf8');
if((code.match(/^main\(\);$/gm)||[]).length!==1)throw Error('Unexpected main entry');
const instrument=path.join(vendor,'.phase11_audit_module.mjs');
fs.writeFileSync(instrument,code.replace(/^main\(\);$/m,'export {GLOSS, parseTranscription, decodeFolios, decodeWord};'));
const hash=x=>crypto.createHash('sha256').update(JSON.stringify(x)).digest('hex');
function rng(seed){let a=seed>>>0;return()=>{a=(Math.imul(a,1664525)+1013904223)>>>0;return a/4294967296;};}
function shuffle(a,r){for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;}
try{
 const {GLOSS,parseTranscription,decodeFolios,decodeWord}=await import(pathToFileURL(instrument));
 const originalGloss={...GLOSS};
 const folios=parseTranscription(path.join(vendor,'tools/eva-data/eva_takahashi.txt'));
 const base=decodeFolios(folios);
 const words=Object.values(folios).flatMap(lines=>lines.flatMap(l=>l.words.map(w=>w.replace(/[?*!]/g,'').trim()).filter(Boolean)));
 const baseOutput=words.map(decodeWord);
 const freqs=out=>{const m=new Map();for(const x of out)if(x)m.set(x,(m.get(x)||0)+1);return [...m.values()].sort((a,b)=>a-b);};
 const values=[...new Set(Object.values(originalGloss))];
 const baseFreq=hash(freqs(baseOutput)), trials=[];
 for(let n=0;n<100;n++){
  const seed=110000+n, order=shuffle([...values],rng(seed));
  const perm=new Map(order.map((v,i)=>[v,order[(i+1)%order.length]]));
  for(const [k,v]of Object.entries(originalGloss))GLOSS[k]=perm.get(v);
  const now=decodeFolios(folios), output=words.map(decodeWord);
  trials.push({seed,total:now.totalWords,decoded:now.totalDecoded,
   changed_decoded_tokens:output.filter((v,i)=>v&&v!==baseOutput[i]).length,
   sorted_frequency_profile_unchanged:hash(freqs(output))===baseFreq,
   output_vocabulary_set_unchanged:hash([...new Set(Object.values(GLOSS))].sort())===hash([...values].sort()),
   section_coverage_unchanged:JSON.stringify(now.sectionStats)===JSON.stringify(base.sectionStats),
   glossary_sha256:hash(GLOSS)});
 }
 Object.assign(GLOSS,originalGloss);
 const result={repository:'scott-schechter/voynich-decoded',
  baseline:{folios:Object.keys(folios).length,glossary_keys:Object.keys(GLOSS).length,distinct_values:values.length,total:base.totalWords,decoded:base.totalDecoded,coverage:base.totalDecoded/base.totalWords,sections:base.sectionStats},
  instrumentation:'Only final main() call replaced by exports in temporary copy.',
  permutation:'Random cyclic derangement of distinct output values; homophonies preserved.',
  trials};
 fs.writeFileSync(path.join(root,'results/scott_audit.json'),JSON.stringify(result,null,2)+'\n');
 console.log(JSON.stringify({baseline:result.baseline,permutations:trials.length,allCoverageIdentical:trials.every(t=>t.decoded===base.totalDecoded),allDecodedChanged:trials.every(t=>t.changed_decoded_tokens===base.totalDecoded),allFrequencyProfilesIdentical:trials.every(t=>t.sorted_frequency_profile_unchanged)}));
}finally{fs.unlinkSync(instrument);}
