"""Vérifier le prolongement conditionnel au sein du même paragraphe f75r."""
import gzip,json,re
from ouvrir import ROOT,units
from essayer import HERE,fit

def main():
    views=[]
    for file in ['IT2a-n.txt','ZL3b-n.txt']:
        lines=(ROOT/'voynich_20261028/data'/file).read_text().splitlines()
        prev=next(i for i,l in enumerate(lines) if l.startswith('<f75r.11,+P0>'))
        there=next(i for i,l in enumerate(lines) if l.startswith('<f75r.12,+P0>'))
        assert there==prev+1 and '<$>' not in lines[prev] and '<%>' not in lines[there]
        part=lines[there].split('>',1)[1].strip().split('<->')[0]
        for cut in ('','.'):views.append(part.replace(',',cut).split('.')[:2])
    assert all(v==views[0] for v in views)
    actual=views[0]
    ann=json.loads(gzip.decompress((HERE/'F75-ANNONCES.json.gz').read_bytes()))
    out=[]
    for item in ann['lectures']:
        for r in item['positions']:
            keys=[item['cle']]
            for clear,cipher in zip(r['suite'],actual):
                keys=[solution for k in keys for solution in fit(units(cipher,'blocs'),clear,{},k)]
            out.append({'trio':item['trio'],'suite':r['suite'],'annonce':r['annonces'],
                        'exacts':[w in opts if opts else None for w,opts in zip(actual,r['annonces'])],
                        'nb_extensions':len(keys) if len(r['suite'])==2 else None})
    (HERE/'CHANGEMENT-RESULTATS.json').write_text(json.dumps({'vues':views,'evaluations':out},ensure_ascii=False,indent=1)+'\n')
    print(actual,'extensions',sum(r['nb_extensions'] or 0 for r in out))
if __name__=='__main__':main()
