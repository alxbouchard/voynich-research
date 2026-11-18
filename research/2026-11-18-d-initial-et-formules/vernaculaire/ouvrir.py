"""Vérifier les annonces historiques dans les deux transcriptions de f43."""
from collections import Counter
from hashlib import sha256
from itertools import product
import gzip
import json
import re
from essayer import HERE,fit

ROOT=HERE.parents[2]
LOCI={'recto':'f43r.9','verso':'f43v.13'}
UNITS=r'ckh|cth|cph|cfh|ch|sh|[a-z]'


def reveal():
    answers={}
    for side,loc in LOCI.items():
        versions=[]
        for file in ['IT2a-n.txt','ZL3b-n.txt']:
            line=next(l for l in (ROOT/'voynich_20261028/data'/file).read_text().splitlines() if l.startswith('<'+loc+','))
            raw=re.sub(r'<[^>]*>|!','',line).strip()
            for cut in ['','.']:
                words=raw.replace(',',cut).strip('.').split('.')
                versions.append(words[:3])
        assert all(v==versions[0] for v in versions)
        answers[side]=versions[0]
    return answers

def units(word,mode):
    pattern=UNITS
    if mode=='blocs':pattern='edy|qo|'+pattern
    elif mode.startswith('qo_lie'):pattern='qo|'+pattern
    return tuple(re.findall(pattern,word))

def main():
    source=HERE/'ANNONCES.json.gz'
    text=json.loads(gzip.decompress(source.read_bytes()))
    answers=reveal()
    results={}
    for name,v in text.items():
        checks=Counter()
        exact={'recto':set(),'verso':set()}
        singles={'recto':set(),'verso':set()}
        fitting=[]
        for row in v['resultats']['deux_faces']:
            key=row['cle']
            poss={}
            for side in LOCI:
                cy=answers[side][-1]
                poss[side]=[]
                for ref in row[side]:
                    clear=ref['troisieme']
                    exact[side].update(ref['annonces'])
                    if clear:
                        for k in fit(units(cy,row['mode']),clear,{},key):
                            poss[side].append((ref,k))
            checks['compatibles_recto']+=bool(poss['recto'])
            checks['compatibles_verso']+=bool(poss['verso'])
            both=[]
            for (a,k),(b,other) in product(poss['recto'],poss['verso']):
                if any(k[s]!=other[s] for s in k.keys()&other):continue
                merge={**k,**other}
                if len(set(merge.values()))!=len(merge):continue
                both.append({'recto':a,'verso':b,'cle_completee':merge})
            if both:fitting.append({'ajustement':row['premiers'],'mode':row['mode'],'paires':both})
            checked=[(a['troisieme'],b['troisieme']) for a,b in product(row['recto'],row['verso']) if a['troisieme'] and b['troisieme']]
            checks['paires_de_contextes_comparables']+=len(checked)
            checks['paires_du_meme_troisieme']+=sum(a==b for a,b in checked)
        for row in v['resultats']['une_face']:
            for pos in row['lieux']:singles[row['face']].update(pos['annonces'])
        extras=[]
        for row in v['resultats']['une_face']:
            side=row['face']
            for hit in row['lieux']:
                clear=hit['troisieme']
                if clear:
                    for k in fit(units(answers[side][-1],row['mode']),clear,{},row['cle']):
                        extras.append({'face':side,'premiers':row['premiers'],'mode':row['mode'],'lieu':hit,'table':k})
        results[name]={'annonces_deux_faces':{s:sorted(ws) for s,ws in exact.items()},
                       'annonces_une_face':{s:sorted(ws) for s,ws in singles.items()},
                       'controles':dict(checks), 'trois_mots_compatibles_des_deux_cotes':fitting,
                       'trois_mots_compatibles_apres_apprentissage_sur_une_face':extras}
    out={'premiers_groupes_par_face':answers,'empreinte_annonces':sha256(source.read_bytes()).hexdigest(),'comparaisons':results}
    (HERE/'OUVERTURE.json').write_text(json.dumps(out,indent=1,sort_keys=True,ensure_ascii=False)+'\n')
    for name,d in results.items(): print(name,d['controles'],len(d['trois_mots_compatibles_des_deux_cotes']),len(d['trois_mots_compatibles_apres_apprentissage_sur_une_face']))
if __name__=='__main__':main()
