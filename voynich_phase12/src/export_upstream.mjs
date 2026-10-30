import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dir=path.join(root,'tmp/vendor/scott');
const source=fs.readFileSync(path.join(dir,'decode.js'),'utf8');
if((source.match(/^main\(\);$/gm)||[]).length!==1)throw Error('Unexpected entry point');
const instrument=path.join(dir,'.phase12_export.mjs');
fs.writeFileSync(instrument,source.replace(/^main\(\);$/m,'export {GLOSS,tokenizeEva,stripGallows,decodeWord,parseTranscription};'));
try{
 const m=await import(pathToFileURL(instrument));
 const folios=m.parseTranscription(path.join(dir,'tools/eva-data/eva_takahashi.txt'));
 const all=Object.values(folios).flatMap(lines=>lines.flatMap(l=>l.words.map(w=>w.replace(/[?*!]/g,'').trim()).filter(Boolean)));
 const entries=Object.fromEntries(Object.keys(m.GLOSS).map(w=>[w,{stripped:m.stripGallows(w),decoded:m.decodeWord(w),after:m.decodeWord(m.stripGallows(w))}]));
 fs.writeFileSync(path.join(root,'tmp/upstream_private.json'),JSON.stringify({gloss:m.GLOSS,entries,
  original_parser:{tokens:all.length,decoded:all.filter(w=>m.decodeWord(w)).length},
  source_parser:folios}));
 console.log(JSON.stringify({glossary_entries:Object.keys(m.GLOSS).length,tokens:all.length}));
}finally{fs.unlinkSync(instrument);}
