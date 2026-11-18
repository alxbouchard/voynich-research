"""Ajuster et transférer toutes les tables littérales admissibles pour le nom proposé."""
from collections import Counter, defaultdict
from functools import lru_cache
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import langage

FACES = ('f6r','f52r','f56v')
WITNESSES = ('aristologia','aristologie','aristologe')
ALL = WITNESSES + ('aristolochia',)


@lru_cache(maxsize=None)
def units(w, unit):
    return tuple(w) if unit=='caracteres' else tuple(langage.UNIT.findall(w))


def windows(tokens, limit, unit):
    selected = tokens if limit is None else tokens[:limit]
    for i,(loc,w) in enumerate(selected):
        if w is None:
            continue
        yield loc, w, units(w,unit)
        if i+1 < len(selected):
            loc2,w2 = selected[i+1]
            if w2 is not None and loc.split('/')[0]==loc2.split('/')[0]:
                yield loc+'–'+loc2, w+'.'+w2, units(w,unit)+units(w2,unit)


def mapping(cipher,plain,injective):
    if len(cipher)!=len(plain):
        return None
    key=dict(zip(cipher,plain))
    if any(key[c]!=p for c,p in zip(cipher,plain)):
        return None
    if injective and len(set(key.values()))!=len(key):
        return None
    return key


def fits(windows_, names, inj):
    out=[]
    by_size=defaultdict(list)
    for name in names:
        by_size[len(name)].append(name)
    for loc,w,seq in windows_:
        for name in by_size[len(seq)]:
            key=mapping(seq,name,inj)
            if key:
                out.append({'loc':loc,'eva':w,'nom':name,'cle':key})
    return out


def decode(rows, keys, names):
    result=[]
    sizes={len(n) for n in names}
    for loc,w,seq in rows:
        if len(seq) not in sizes:
            continue
        for ref,k in enumerate(keys):
            value=''.join(k.get(s,'?') for s in seq)
            if value in names:
                result.append({'loc':loc,'eva':w,'lecture':value,'cle_numero':ref+1})
    return result


def label_slots(stem,where,split):
    lines = (langage.DATA/(stem+'-n.txt')).read_text().splitlines()
    result={}
    for loc in where:
        matching=[s.split('>',1)[1] for s in lines if re.match(r'^<'+re.escape(loc)+r',[^!]Lf>',s)]
        assert len(matching)==1,(stem,loc)
        raw=re.sub('<![^>]*>|<[%$]>|!', '', matching[0].strip())
        raw=re.sub(r'<[-~]>', '.', raw).replace(',', '.' if split=='separes' else '')
        result[loc]=[(loc+'/'+str(i), w if re.fullmatch('[a-z]+',w) else None)
                     for i,w in enumerate(filter(None,raw.split('.')),1)]
    return result


def run(label_ids):
    qs=langage.eligible()
    result={}
    for split in langage.SPLITS:
        eds=langage.tokens(qs,split)
        for ed,raw in eds.items():
            labels=label_slots(langage.EDITIONS[ed],label_ids,split)
            for unit in ('unites','caracteres'):
                main_windows={f:list(windows(seq,16,unit)) for f,seq in raw.items()}
                corpus={**main_windows,**{loc:list(windows(seq,None,unit)) for loc,seq in labels.items()}}
                three = [{w for _,w in raw[f][:16] if w and len(units(w,unit))>=3} for f in FACES]
                shared = sorted(set.intersection(*three))
                data = {'mots_communs':{w:{f:[loc for loc,x in raw[f][:16] if x==w] for f in FACES} for w in shared},
                        'ouvertures': {f:raw[f][0] for f in FACES}, 'petits_dessins':labels,
                        'lectures':{}}
                for tag,names in [('temoins_XVe',WITNESSES),('variante_latine',('aristolochia',))]:
                    for model,inj in [('simple',True),('homophones',False)]:
                        learn=fits(main_windows['f6r'],names,inj)
                        keys=[dict(t) for t in sorted({tuple(sorted(row['cle'].items())) for row in learn})]
                        local={}
                        for f,seq in {**{f:raw[f] for f in FACES},**labels}.items():
                            local[f]={}
                            limits = [('premier',1),('seize',16),('page',None)] if f in raw else [('etiquette',None)]
                            for title,limit in limits:
                                samples=list(windows(seq,limit,unit))
                                local[f][title]={'fenetres':len(samples),'longueur_compatible':sum(len(s) in {len(n) for n in names} for _,_,s in samples),
                                                      'lectures':fits(samples,names,inj)}
                        hits = {f:decode(ws,keys,names) for f,ws in corpus.items()} if keys else {}
                        data['lectures'][tag+'_'+model]={'apprentissage':learn,'cles':keys,'ajustements_locaux':local,
                                'transfert_par_face':{f:rows for f,rows in hits.items() if f!='f6r' and rows},
                                'nombre_temoins_grandes_faces':len(qs)-len(FACES)}
                result[split+'_'+ed+'_'+unit]=data
    return result


def calibration():
    # Un chiffrement témoin commun aux deux graphies « Aristologia » attestées.
    # Le système simple utilise une seule graphie par lettre ; le second deux pour a.
    known='aristologia'
    alphabet={p:chr(65+i) for i,p in enumerate(sorted(set(known)))}
    cipher=[alphabet[p] for p in known]
    another=cipher.copy()
    another[-1]='Z'
    positive=mapping(another,known,False)
    assert positive and mapping(another,known,True) is None
    reads=decode([('tenu_cache', ''.join(cipher), tuple(cipher))],[positive],WITNESSES)
    assert reads and reads[0]['lecture']==known
    return {'nom_atteste':known,'simple':mapping(cipher,known,True),'homophones':positive,
            'cipher_avec_homophone':''.join(another),'cipher_reserve':''.join(cipher),'lecture_reserve':reads,
            'table_simple_rejette_seconde_graphie_pour_a':True}


if __name__=='__main__':
    spec=json.loads((HERE/'emplacements.json').read_text())
    out={'calibration':calibration(),'emplacements':spec,'variantes':run(spec['loci'])}
    (HERE/'lectures.json').write_text(json.dumps(out,ensure_ascii=False,indent=1,sort_keys=True)+'\n')
