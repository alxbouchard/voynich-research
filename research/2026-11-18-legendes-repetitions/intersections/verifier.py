"""Localiser les deux mots dans les deux éditions et les deux conventions du blanc."""
from pathlib import Path
import json
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / '2026-11-18-opcheor-paralleles' / 'variantes'))
from compter import corpus, tokens

MOTS = ('otoky', 'otaly')

def relever(editions, mot):
    communs = set.intersection(*(set(rows) for rows in editions.values()))
    lieux = {}
    for lieu in sorted(communs):
        lignes = {edition: rows[lieu] for edition, rows in editions.items()}
        variantes = [tokens(row[3], coupe) for row in lignes.values()
                     for coupe in ('joints', 'separes')]
        if all(mot in lecture for lecture in variantes):
            lieux[lieu] = {
                'type': lignes['ZL'][1],
                'seul': all(len(lecture) == 1 for lecture in variantes),
                'ZL': lignes['ZL'][3],
                'IT': lignes['H'][3],
            }
    return lieux

def main():
    editions, _ = corpus()
    inventaire = RESEARCH / '2026-11-18-deux-legendes-botaniques/lecture/tucker/prefixe/resultats.json'
    anciennes_classes = json.loads(inventaire.read_text())['par_code']
    bilan = {}
    for mot in MOTS:
        lieux = relever(editions, mot)
        bilan[mot] = {'nombre_de_lieux': len(lieux),
                      'lieux_a_un_mot': sum(row['seul'] for row in lieux.values()),
                      'lieux': lieux,
                      'dans_les_six_classes': {code: sorted(loc for loc, value in data['mots_par_locus'].items()
                                                            if value == mot)
                                               for code, data in anciennes_classes.items()}}
    (HERE/'lieux.json').write_text(json.dumps(bilan, ensure_ascii=False, indent=2)+'\n')

if __name__ == '__main__':
    main()
