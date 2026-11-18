"""Compte les légendes entières concordantes portant les finales du test visuel."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
INVENTORY = HERE.parents[2] / '2026-11-18-mois-automne' / 'cle' / 'INVENTAIRE.json'


def counts(loci):
    labels = {loc: record['utilisables'][0] for loc, record in loci.items() if record['utilisables']}
    assert all(len(record['utilisables']) <= 1 for record in loci.values())
    return {
        'emplacements': len(loci),
        'legendes_entieres_concordantes': len(labels),
        'avec_finale_y': sum(word.endswith('y') for word in labels.values()),
        'lieux_par_forme': {
            target: sorted(loc for loc, word in labels.items() if word == target)
            for target in ('okal', 'okaly', 'otedy')
        },
    }


def main():
    pages = json.loads(INVENTORY.read_text())['panneaux']
    gemini = pages['f72r2']['Lz']['loci']
    outer = {f'f72r2.{i}': gemini[f'f72r2.{i}'] for i in range(7, 22)}
    all_labels = {loc: row for page in pages.values() for loc, row in page['Lz']['loci'].items()}
    output = {
        'gemeaux_couronne_complete_exterieure': counts(outer),
        'gemeaux_tout_le_panneau': counts(gemini),
        'douze_panneaux': counts(all_labels),
    }
    (HERE / 'contexte.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    main()
