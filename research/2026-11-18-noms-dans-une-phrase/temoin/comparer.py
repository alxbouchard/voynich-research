"""Prédire qu'un mot reprend le titre à partir des seuls voisins du mot masqué."""
import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
from itertools import product
import json
from pathlib import Path
import re
import unicodedata


ICI = Path(__file__).resolve().parent
SOURCE = ICI.parent.parent / '2026-11-18-noms-dans-les-notices/historique/source.wiki.gz'
DIGEST = '41ca63622e4fbcc4f52c40d7c9261541c5b6d24ee59ebb2964ece69cee480e26'
TITRE = re.compile(r'^==\s*([IVXLCDM]+)\.\s*(.*?)\.\s*==\s*$', re.I | re.M)


def mots(s):
    return re.findall(r'[^\W\d_]+', ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if not unicodedata.combining(c)))


def corpus(debut, fin):
    src = gzip.decompress(SOURCE.read_bytes())
    assert hashlib.sha256(src).hexdigest() == DIGEST
    s = src.decode()
    rub = list(TITRE.finditer(s))
    notices = {}
    for n in range(debut, fin + 1):
        bloc = s[rub[n-1].end():rub[n].start()]
        vers = re.search(r'<poem>\s*(.*?)\s*</poem>', bloc, re.S).group(1)
        vers = re.sub(r'\{\{Versus\|\d+\}\}', '', vers)
        assert not any(c in vers for c in '<>{}[]')
        notices[n] = (rub[n-1][2], [v.strip() for v in vers.splitlines() if v.strip()])
    return notices


def est_nom(a, b):
    if a == b:
        return True
    i = 0
    for x, y in zip(a, b):
        if x != y:
            break
        i += 1
    return i >= 4 and max(len(a), len(b)) - i <= 2


def indices(v, i):
    voisins = [(d, v[i+d]) for d in (-2, -1, 1, 2) if 0 <= i+d < len(v)]
    return [(x,) for x in voisins] + [(l, r) for l, r in product(voisins, repeat=2) if l[0] < 0 < r[0]]


def positions(lot):
    for n, (titre, vers) in lot.items():
        for j, ligne in enumerate(vers, 1):
            v = mots(ligne)
            for i in range(len(v)):
                yield n, titre, j, ligne, v, i


def apprendre():
    compte, bons, notices = Counter(), Counter(), defaultdict(set)
    for n, titre, _, _, v, i in positions(corpus(45, 60)):
        for k in indices(v, i):
            compte[k] += 1
            if est_nom(mots(titre)[0], v[i]):
                bons[k] += 1
                notices[k].add(n)
    return [{'indice': k, 'occurrences': compte[k], 'noms': bons[k], 'chapitres': sorted(notices[k])}
            for k in sorted(bons) if len(notices[k]) >= 2 and bons[k] * 20 >= compte[k]]


def lire(nom):
    return json.loads((ICI / nom).read_text())


def ecrire(nom, contenu):
    (ICI / nom).write_text(json.dumps(contenu, ensure_ascii=False, indent=2) + '\n')


def predire():
    cles = {tuple(tuple(x) for x in regle['indice']): j
            for j, regle in enumerate(lire('INDICES.json'), 1)}
    annonces = []
    for n, titre, j, _, v, i in positions(corpus(61, 76)):
        regles = [cles[k] for k in indices(v, i) if k in cles]
        if regles:
            annonces.append({'chapitre': n, 'rubrique': titre, 'vers': j, 'position': i+1, 'indices': regles})
    return annonces


def verifier():
    lot = corpus(61, 76)
    annonces = {(a['chapitre'], a['vers'], a['position']): a for a in lire('PREDICTIONS.json')}
    lignes, bilans = [], defaultdict(Counter)
    for n, titre, j, ligne, v, i in positions(lot):
        t = mots(titre)[0]
        suivant = mots(lot[61 if n == 76 else n+1][0])[0]
        bon = est_nom(t, v[i])
        annonce = (n,j,i+1) in annonces
        decale = (n,j,(i-1) % len(v)+1) in annonces
        if bon or annonce or decale:
            lignes.append({'chapitre': n, 'rubrique': titre, 'vers': j, 'position': i+1,
                           'mot': v[i], 'ligne': ligne, 'reprise': bon, 'annonce': annonce,
                           'annonce_decalee': decale, 'titre_suivant': suivant,
                           'reprise_du_suivant': est_nom(suivant,v[i])})
        for g in ['tous', 'vers_1_et_2' if j <= 2 else 'vers_3_et_suivants', str(n)]:
            b = bilans[g]
            b.update(places=1, reprises=int(bon), annonces=int(annonce), justes=int(bon and annonce),
                     decalees=int(decale), justes_decalees=int(bon and decale),
                     rubrique_suivante_justes=int(annonce and est_nom(suivant, v[i])))
    return {'bilans': bilans, 'detail': lignes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('etape', choices=['apprendre', 'predire', 'verifier'])
    etape = parser.parse_args().etape
    if etape == 'apprendre':
        ecrire('INDICES.json', apprendre())
    elif etape == 'predire':
        ecrire('PREDICTIONS.json', predire())
    else:
        ecrire('RESULTATS.json', verifier())
