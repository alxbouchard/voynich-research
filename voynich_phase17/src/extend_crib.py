from pathlib import Path
import json
from crib_scan import blocks,rows,units,PLAIN

ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'results/crib_scan.json').read_text())
out={'post_hoc':True,'extension':'maria','gap_units':list(range(9)),'runs':[]}
for run in r['runs']:
    bs=blocks(rows(ROOT/'data'/('ZL3b-n.txt' if run['corpus']=='ZL' else 'IT2a-n.txt')),run['spacing'])
    attempts=0;survivors=[]
    for match in run['matches']:
        b=bs[match['block']]
        uw=[units(w['text'],run['tokenization']) for w in b]
        flat=[u for w in uw for u in w]
        start=sum(map(len,uw[:match['start_word']]))+match['start_unit']
        end=sum(map(len,uw[:match['end_word']]))+match['end_unit']+1
        seq=flat[start:end]
        if match['direction']=='reverse':seq=seq[::-1];continuation=flat[:start][::-1]
        else:continuation=flat[end:]
        assert seq==match['cipher_units']
        for gap in range(9):
            sample=continuation[gap:gap+5]
            if len(sample)<5:continue
            attempts+=1;key=match['key'].copy();ok=True
            for c,p in zip(sample,'maria'):
                if c in key and key[c]!=p:ok=False;break
                key[c]=p
            if ok:survivors.append({'initial_match':match,'gap':gap,'extension_units':sample,'extended_key':key})
    out['runs'].append({k:run[k] for k in ['corpus','spacing','tokenization']}|{'initial_candidates':len(run['matches']),'extension_tests':attempts,'survivors':survivors})
(ROOT/'results/crib_extension.json').write_text(json.dumps(out,indent=2))
for q in out['runs']: print({k:(len(v) if k=='survivors' else v) for k,v in q.items()})
