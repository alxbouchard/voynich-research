"""Recalcule les occurrences et les dénominateurs par classe L hors feuillet 102."""
import csv
import re
from collections import Counter
from hashlib import sha256
from pathlib import Path

ICI = Path(__file__).resolve().parent
DATA = ICI.parents[3] / 'voynich_20261028' / 'data'
SOURCES = {
    'H': ('IT2a-n.txt', '7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5'),
    'ZL': ('ZL3b-n.txt', 'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc'),
}
MOTS = ('opchy', 'otol')
CLASSES = ('Lf', 'L0', 'La', 'Lc', 'Ln', 'Lp', 'Ls', 'Lt', 'Lx', 'Lz')
LOCUS = re.compile(r'^<([^.,>]+)\.(\d+),(.)(L[a-z0-9])>\s*(.*)$')

def lire(nom, empreinte):
    blob = (DATA / nom).read_bytes()
    assert sha256(blob).hexdigest() == empreinte
    resultat = {}
    for ligne in blob.decode().splitlines():
        m = LOCUS.match(ligne)
        if not m:
            continue
        page, num, position, classe, texte = m.groups()
        if re.fullmatch(r'f102[rv]\d*', page) or position == '!':
            continue
        texte = re.sub(r'<![^>]*>', '', texte).strip().replace('{', '').replace('}', '')
        resultat[f'{page}.{num}'] = (classe, texte)
    return resultat

def ecrire(nom, en_tete, donnees):
    with (ICI / nom).open('w', newline='') as flux:
        table = csv.writer(flux, delimiter='\t', lineterminator='\n')
        table.writerow(en_tete)
        table.writerows(donnees)

corpus = {temoin: lire(*source) for temoin, source in SOURCES.items()}
comptes = []
for temoin, loci in corpus.items():
    for classe in CLASSES:
        formes = Counter(texte for c, texte in loci.values() if c == classe)
        # Le seul Lf sur deux loci est f99r.6+7 (objet 72). Aucun des deux loci ne donne un mot cible.
        if classe == 'Lf':
            assert all(loci['f99r.'+str(n)][1] not in MOTS for n in (6, 7))
        comptes.append([temoin, classe, sum(formes.values()), *(formes[mot] for mot in MOTS)])
ecrire('comptes.tsv', ['temoin', 'classe', 'loci_examines', 'opchy_locus_entier', 'otol_locus_entier'], comptes)

occurrences = []
for lieu in sorted(set().union(*(r.keys() for r in corpus.values()))):
    lectures = [corpus[t].get(lieu, ('', '')) for t in SOURCES]
    if any(texte in MOTS for _, texte in lectures):
        classe = next(c for c, texte in lectures if texte in MOTS)
        entier = 'non_etabli_groupe_II_lignes_149_a_151' if lieu == 'fRos.149' else 'oui'
        occurrences.append((lieu, classe, lectures[0][1], lectures[1][1], entier))
ecrire('occurrences.tsv', ['locus', 'classe', 'H', 'ZL', 'inscription_entiere'], occurrences)
