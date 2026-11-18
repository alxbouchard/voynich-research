"""Chercher une légende entière par ligne après l'épreuve visuelle."""
import json
from pathlib import Path
import re
from compter import corpus, labels, tokens

HERE = Path(__file__).resolve().parent


def scan(rows, faces, split):
    target = labels(rows,split)['f88v.4']
    assert target and all(re.fullmatch('[a-z]+',w) for w in target)
    pages = {}
    for loc,(face,kind,_,raw) in rows.items():
        if kind == 'P0' and face in faces:
            pages.setdefault(face,[]).append((loc,tokens(raw,split)))
    variants = {w:[] for w in (*target,'iirody')}
    for loc,seq in pages['f96r']:
        for i,w in enumerate(seq,1):
            if w in variants:
                variants[w].append((loc,i))
    hits = {k:[] for k in ('premiere','seize','entiere')}
    for face,lines in pages.items():
        total = 0
        for num,(loc,seq) in enumerate(lines,1):
            for i in range(len(seq)-len(target)+1):
                if seq[i:i+len(target)] != target:
                    continue
                item = (face,loc,i+1)
                hits['entiere'].append(item)
                if num==1:
                    hits['premiere'].append(item)
                if total+i+len(target)<=16:
                    hits['seize'].append(item)
            total += len(seq)
    return {'legende':target,'f96r_nombre_lignes':len(pages['f96r']),
            'f96r_positions_P0':sum(len(seq) for _,seq in pages['f96r']),
            'f96r_premiere_ligne':pages['f96r'][0],'mots_isoles_f96r':variants,'nombre_faces':len(pages),'occurrences':hits}


def run():
    eds,sections = corpus()
    faces = {f for f,c in sections.items() if c=='H'}
    output = {}
    for split in ('joints','separes'):
        source = {ed:scan(rows,faces,split) for ed,rows in eds.items()}
        common = {}
        for k in ('premiere','seize','entiere'):
            compatible = source['H']['legende'] == source['ZL']['legende']
            where = set.intersection(*({(f,loc) for f,loc,i in s['occurrences'][k]} for s in source.values()))
            shared = sorted(where) if compatible else []
            common[k] = {'meme_legende':compatible,'faces':len({f for f,_ in shared}),
                         'loci':shared,'sur_f96r':[loc for f,loc in shared if f=='f96r']}
        output[split] = {'editions':source,'accord':common}
    (HERE/'voisin.json').write_text(json.dumps(output,ensure_ascii=False,indent=1)+'\n')


if __name__=='__main__':
    run()
