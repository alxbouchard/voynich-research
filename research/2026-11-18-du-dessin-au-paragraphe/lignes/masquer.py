"""Aligner les boîtes sur H dans une étape séparée, sans exporter le texte des cibles."""
from pathlib import Path
from collections import Counter
import re
import sys
from fichiers import PASSAGES, save, digest
sys.path.insert(0,str(PASSAGES))
from preparer import MODES, corpus, make, sequence, units
from predire import inclination


def lectures(loc,editions,n):
    views=[[w for _,w in sequence(rows[loc][3],cut)] for rows in editions.values() for cut in MODES]
    assert len(views)==4 and len(views[0])==n
    same=[]
    for i in range(n):
        options={v[i] if i<len(v) else None for v in views}
        w=next(iter(options)) if len(options)==1 else None
        same.append(w if w is not None and re.fullmatch('[a-z]+',w) else None)
    return same


def lot(page,section):
    if section=='P' and page!='f101r':return 'pharmaceutique'
    m=re.fullmatch(r'f(\d+)[rv]',page)
    if m and 1<=int(m[1])<=16:return 'f1-16'
    if m and 103<=int(m[1])<=116:return 'f103-116'


def main(cache):
    editions,sections=corpus()
    both=set.intersection(*({p for p,k,_,_ in ed.values() if k=='P0'} for ed in editions.values()))
    masked={};sources={}
    for page in sorted(both):
        group=lot(page,sections.get(page));
        if not group:continue
        path=cache/(page+'.json')
        material=make(page,path.read_bytes(),editions)
        name='f101v2' if page=='f101v' else page
        sources[page]=dict(lot=group,url=f'https://www.voynichese.com/2/data/folio/script/{name}.js',sha256=digest(path),couverture=material['couverture'])
        pairs=[]
        for para in material['paragraphes']['strict']:
            for above,below in zip(para[::2],para[1::2]):
                up,down=(material['lignes'][loc] for loc in (above,below))
                upper=lectures(above,editions,len(up))
                given=[w if 0<i<len(up)-1 and w and len(units(w,False))>=3 else None for i,w in enumerate(upper)]
                pairs.append(dict(haut=above,bas=below,boites_haut=up,boites_bas=down,mots_haut=given))
        assert len({p['haut'] for p in pairs}|{p['bas'] for p in pairs})==2*len(pairs)
        masked[page]=dict(lot=group,pente=inclination(material['lignes']),paires=pairs)
    counts=Counter(source['lot'] for source in sources.values())
    assert counts['pharmaceutique']==15
    save('SOURCES.json',sources);save('CARTE-MASQUEE.json.gz',masked)


if __name__=='__main__': main(Path(sys.argv[1]))
