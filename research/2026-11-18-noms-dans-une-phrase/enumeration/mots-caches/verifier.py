"""Dévoiler la prose aux numéros déjà publiés et comparer les prédictions."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True
from predire import HERE, PAGES, corpus, sequence, MODES, digest, write

SHA_ANNONCES = 'a6a92c76b7d12da70fcad6546c93a8755f3b1a1c57c8b2340a3398a4ded74a6b'
SHA_MASQUE = 'ea988b3bdb025f4b7da77ca85d2633eb82f5770ce935eed78a28194005378a8b'


def reveal(data,masked,source):
    pages = {}
    for page in PAGES:
        path = source/(page+'.json')
        assert digest(path)==masked[page]['carte_sha256']
        words,boxes = json.loads(path.read_text())
        index = 0
        for loc,row in data['H'].items():
            if row[0]!=page: continue
            original = list(masked[page]['lignes'][loc.rsplit('.',1)[1]]['boites'])
            assert [b[1:5] for b in boxes[index:index+len(original)]]==original
            js = [words[b[0]][0] for b in boxes[index:index+len(original)]]
            index += len(original)
            if row[1]!='P0': continue
            readings = {e+'_'+c:[w for _,w in sequence(entries[loc][3],c)] for e,entries in data.items() for c in MODES}
            pages[loc] = {'points':js, 'lectures':readings}
        assert index==len(boxes)
    return pages


def slot(line,rank):
    found = {k:ws[rank-1] if rank<=len(ws) else None for k,ws in line['lectures'].items()}
    viewer = line['points'][rank-1]
    h = found['H_joints']
    h_ok = h==viewer and bool(re.fullmatch('[a-z]+',h or ''))
    joint = h_ok and set(found.values())=={h}
    return {'rang':rank, 'visualiseur':viewer, 'lectures':found,
            'commun':h if joint else None, 'h_visualiseur':h if h_ok else None}


def judge(predictions, pages):
    out = []
    for prediction in predictions:
        if not prediction['annonce']: continue
        v=prediction['annonce']
        page=prediction['page']
        loc=prediction['cible']
        line=pages[loc]
        size=len(line['points'])
        actual=slot(line,v['rang'])
        control=slot(line,v['rang']%size+1)
        all_slots=[slot(line,i)['commun'] for i in range(1,size+1)]
        available=[w for w in all_slots if w]
        out.append({'feuillet':re.match('f[0-9]+',page)[0], 'page':page,'cote':prediction['cote'],
                    'legende':prediction['legende'], 'cible':loc,'annonce':v, 'observe':actual, 'decale':control,
                    'hasard_justes':available.count(v['mot']), 'hasard_recevables':len(available), 'taille_H':size,
                    'dans_ligne_apres_coup':{k:ws.count(v['mot']) for k,ws in {**line['lectures'],'visualiseur':line['points']}.items()},
                    'comptes_transcriptions':{k:len(ws) for k,ws in line['lectures'].items()}})
    return out


def summary(rows):
    s=Counter({'paires_recevables':0,'paires_position_juste':0,'paires_decalage_juste':0,'hasard_comparables':0})
    expectation=Fraction(0)
    for r in rows:
        mot=r['annonce']['mot']
        s['annonces']+=1
        for label,key in [('position_predite','observe'),('decalage','decale')]:
            for form in ['commun','h_visualiseur']:
                actual=r[key][form]
                s[label+'_'+form+'_recevables']+=bool(actual)
                s[label+'_'+form+'_justes']+=actual==mot
        if r['observe']['commun'] and r['decale']['commun']:
            s['paires_recevables']+=1
            s['paires_position_juste']+=r['observe']['commun']==mot
            s['paires_decalage_juste']+=r['decale']['commun']==mot
        if r['hasard_recevables']:
            expectation+=Fraction(r['hasard_justes'],r['hasard_recevables'])
            s['hasard_comparables']+=1
    sites={(r['cible'],r['annonce']['rang']) for r in rows}
    return {**s,'cases_distinctes':len(sites),'nombre_attendu_hasard':str(expectation),
            'taux_attendu_hasard':str(expectation/s['hasard_comparables']) if s['hasard_comparables'] else None}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('sources',type=Path)
    args=parser.parse_args()
    pred=HERE/'PREDICTIONS.json'
    geom=HERE/'GEOMETRIE-MASQUEE.json'
    assert digest(pred)==SHA_ANNONCES and digest(geom)==SHA_MASQUE
    data,_=corpus()
    pages=reveal(data,json.loads(geom.read_text()),args.sources)
    rows=judge(json.loads(pred.read_text()),pages)
    groups={'tous':summary(rows)}
    for side in ('haut','bas'):
        groups[side]=summary([r for r in rows if r['cote']==side])
        for f in ['f88','f89']:
            groups[f+'_'+side]=summary([r for r in rows if r['cote']==side and r['feuillet']==f])
    write('RESULTATS.json',{'bilans':groups,'annonces':rows})
