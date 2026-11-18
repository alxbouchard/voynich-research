"""Tester les formes fléchies et la table imposant au signe o une valeur vide."""
import itertools
import json
import re
from lire import CLUSTER, DIR, SRC, UNITS, checksum, consensus, decoded, latin, tables

FORMS = {
    'stella':'stella stellae stellam stellarum stellis stellas'.split(),
    'sidus':'sidus sideris sideri sidere sidera siderum sideribus'.split(),
    'astrum':'astrum astri astro astra astrorum astris'.split()
}


def regular():
    result = {}
    for lemma, forms in FORMS.items():
        result[lemma] = {}
        for word in forms:
            ok = []
            for a,b,c in itertools.combinations(range(1,len(word)),3):
                if word[:a]==word[b:c]:
                    ok.append([word[:a],word[a:b],word[b:c],word[c:]])
            result[lemma][word] = {
                'rangs_de_la_lettre_initiale': [i+1 for i,ch in enumerate(word) if ch == word[0]],
                'segmentations':ok}
    return result


def get_labels(path):
    result = {}
    for line in path.read_text().splitlines():
        hit = re.fullmatch(r'<(f68r[23]\.\d+),[@=+*]Ls>\s*(.*)',line)
        if hit:
            cleaned = re.sub(r'<![^>]*>', '', hit[2]).translate(str.maketrans('','','{}! '))
            result[hit[1]] = cleaned
    return result


def run():
    h, zl = [get_labels(SRC[s]) for s in ('IT','ZL')]
    assert h.keys()==zl.keys() and len(h)==35 and h['f68r3.11']==zl['f68r3.11']=='doaro'
    eligible = {k:v for k,v in h.items() if k!='f68r3.11' and v==zl[k] and re.fullmatch('[a-z]+',v)}
    excluded = {k:(h[k],zl[k]) for k in h if k!='f68r3.11' and k not in eligible}
    words,_ = consensus()
    anchor = list(tables(['t','r'],'stella',3,{'o':''}))
    tests=[]
    for table in anchor:
        def read(basis):
            readings = {}
            for loc,w in basis:
                value = decoded(UNITS.findall(w),table)
                if value is not None:
                    readings[loc] = {'EVA':w,'lecture':value,'retour_ancre':w=='otor'}
            return readings
        # With o silent, the fixed non-empty sequence on the cluster is d·a·r.
        cluster = {w:list(tables(['d','a','r'],latin(w)[0],3,table)) for w in CLUSTER}
        tests.append({'table':table,'prose':read(words),'legendes_reservees':read(eligible.items()),
                      'amas':{'lecture_partielle':[table.get(s) for s in 'doaro'],'completions':cluster}})
    result = {'protocole_sha256': checksum(DIR/'SUITE-PROTOCOLE.md'), 'flexions':regular(),
              'legendes_reservees_admissibles':eligible,'legendes_reservees_exclues':excluded, 'o_muet':tests}
    (DIR/'SUITE.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    run()
