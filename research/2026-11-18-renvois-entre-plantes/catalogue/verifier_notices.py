"""Contrôler les renvois de retour, les termes de description et les seuls en-têtes IVTFF."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
from extraire import HERE, BLOCK, clean

ROOT = HERE.parents[2]
CORPUS = ROOT / 'voynich_20261028/data'


def verify(pattern):
    inventory = json.loads((HERE/'RENVOIS.json').read_bytes())
    all_faces = set(inventory['panneaux']) | {r['plante'] for r in inventory['liens']}
    p0 = {}
    for file in ('IT2a-n.txt','ZL3b-n.txt'):
        # La recherche s'arrête au > final du localisateur et ne consulte aucun signe.
        rows = re.findall(rb'^<(f\d+[rv]\d*)\.\d+,.P0>', (CORPUS/file).read_bytes(), re.M)
        counts = Counter(p.decode() for p in rows)
        p0[file] = {p:counts[p] for p in sorted(all_faces)}
    cache, fingerprints, rows = {}, {}, []
    for row in inventory['liens']:
        q = int(re.search(r'/q(\d+)/', row['cible_source'])[1])
        if q not in cache:
            data=Path(pattern.format(q=q)).read_bytes()
            cache[q] = dict(BLOCK.findall(data.decode()))
            fingerprints[q] = sha256(data).hexdigest()
        text=cache[q][row['plante']]
        ill=clean(re.search(r'<h4>Illustration\(s\)</h4>(.*?)<h4>Text</h4>',text,re.S|re.I)[1]).split('Herbal drawing characterisation')[0]
        reciprocal = bool(re.search(r'(?:fragment|item) #?'+str(row['fragment'])+r'\b',clean(text),re.I))
        berry_words=sorted(set(re.findall(r'\b(?:berry|berries|currant|currants)\b',ill,re.I)))
        rows.append(dict(fragment=row['fragment'],panneau=row['panneau'],plante=row['plante'],numero_repris=reciprocal,
                         termes_de_baies=berry_words))
    out=dict(empreintes_html=fingerprints, P0_en_tetes=p0, verification=rows)
    (HERE/'VERIFICATION.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
    assert all(n>0 for edition in p0.values() for n in edition.values())
    assert sum(r['numero_repris'] for r in rows)==31


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('fichiers',help='exemple : /tmp/notice-{q}.html')
    verify(p.parse_args().fichiers)
