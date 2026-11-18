"""Lectures conditionnelles de arol et transferts sans réajuster la clé."""
from collections import Counter,defaultdict
from hashlib import sha256
from pathlib import Path
from random import Random
import json
import re
import sys
import gzip
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/'2026-11-18-du-dessin-au-paragraphe/cressons'))
from ajuster import canon,solve,readbacks,corpus,sequence,MODES

FAMILLES={
 'latin':('bifida',['bifidi','bifido'],'lacertis',['et']),
 'normand_nom':('furche',['furc','furches'],'une',['de']),
 'normand_arbre':('furc',['furche','furches'],'el',['d','dun']),
 'anglais':('forked',[],'a',['berd'])}
SITES={'f40v.18':6,'f106r.16':5,'f113v.45':2}


def save(name,x): (HERE/name).write_text(json.dumps(x,ensure_ascii=False,indent=1)+'\n')
def load(name):return json.loads((HERE/name).read_text())
def predicted(key,w):return sorted({''.join(v) for v in readbacks(key,w)})
def models(eqs):
    return [dict(t) for t in solve([(canon(s),w) for s,w in eqs],2) if len(set(dict(t).values()))==len(t)]


def site_word(ed,loc,delta):
    idx=SITES[loc]-1
    forms=[]
    for e in ed.values():
        for cut in MODES:
            words=sequence(e[loc][3],cut)
            assert words[idx][1]=='arol'
            j=idx+delta
            forms.append(words[j][1] if 0<=j<len(words) and words[j][0]==words[idx][0] else None)
    return forms[0] if len(set(forms))==1 and forms[0] and re.fullmatch('[a-z]+',forms[0]) else None


def freeze():
    ed,_=corpus(); first='f40v.18';left=site_word(ed,first,-1)
    out={}
    for name,(seed,deriv,prev,after) in FAMILLES.items():
        keys=models([('arol',seed)])
        extra=models([('arol',seed),(left,prev)]) if left else []
        def goals(keys,ws):return {w:sorted(set(v for k in keys for v in predicted(k,w))) for w in ws}
        out[name]=dict(ancre=seed,cles=keys,formes=goals(keys,deriv),gauche=goals(keys,[prev]),droite=goals(keys,after),
          double_ancre=dict(apprentissage=first,voisin_gauche=left,cles=extra,annonces_droite=goals(extra,after)))
    save('PREDICTIONS.json',out)


def controls():
    abc=sorted(set('bifida'+'bifidi'+'bifido')); hidden=list('uvwxyz')[:len(abc)]; Random(398).shuffle(hidden)
    enc=dict(zip(abc,hidden));code=lambda word: ''.join(enc[c] for c in word)
    seen=dict(zip('bifida',code('bifida')))
    def transfer(w): return ''.join(seen[c] for c in w) if all(c in seen for c in w) else None
    ref={'seme':'bifida','code':code('bifida'),'cibles':{w:{'annonce':transfer(w),'reel':code(w)} for w in ('bifidi','bifido')}}
    test=models([('wxyz','furche')]);guesses=sorted({w for k in test for w in predicted(k,'furc')})
    return {'latin':ref,'anglo_normand':dict(ancre='wxyz',segments_experimentaux=['fu','r','c','he'],
        tables=len(test),annonces=guesses,graphie_reelle='wxy',correct='wxy' in guesses)}


def labels():
    ed,_=corpus(); out={}
    for loc in sorted(set.union(*(set(e) for e in ed.values()))):
        src=[e.get(loc) for e in ed.values()]
        if not any(r and r[1]=='Lf' for r in src) or loc.startswith(('f99r.','f99v.')):continue
        if not all(r and r[1]=='Lf' for r in src):out[loc]=None;continue
        # The only P-section multifragment joining in the inventory occurs on f99r, excluded here.
        rows=[tuple(w for _,w in sequence(r[3],cut)) for r in src for cut in MODES]
        v=rows[0];out[loc]=list(v) if len(set(rows))==1 and all(re.fullmatch('[a-z]+',w) for w in v) and v else None
    return out


def verify():
    ed,_=corpus();pred=load('PREDICTIONS.json');forms={'arol'}
    for t in pred.values():forms.update(f for fs in t['formes'].values() for f in fs)
    def matches(w,guess):return {k:(w in forms if w is not None and forms else None) for k,forms in guess.items()}
    neighbors={}
    for loc in SITES:
        before=site_word(ed,loc,-1);after=site_word(ed,loc,1)
        neighbors[loc]=dict(gauche=before,droite=after,essais={n:{'avant':matches(before,m['gauche']),
            'apres':matches(after,m['droite']),'ancre_double_apres':matches(after,m['double_ancre']['annonces_droite'])} for n,m in pred.items()})
    records=labels();flat=Counter(w for ws in records.values() if ws for w in ws)
    counts={w:dict(lieux=[loc for loc,ws in records.items() if ws and w in ws],positions=flat[w],
           autres_types_meme_longueur=sum(v!=w and len(canon(v))==len(canon(w)) for v in flat),
           tous_mots_meme_longueur=sum(n for v,n in flat.items() if len(canon(v))==len(canon(w)))) for w in sorted(forms)}
    save('VERIFICATION.json',dict(empreinte=sha256((HERE/'PREDICTIONS.json').read_bytes()).hexdigest(),calibration=controls(),
         voisins=neighbors,legendes_hors_f99=len(records),legendes_lisibles=sum(v is not None for v in records.values()),
         positions_lisibles=flat.total(),inventaire=counts))


if __name__=='__main__':{'annoncer':freeze,'verifier':verify}[sys.argv[1]]()
