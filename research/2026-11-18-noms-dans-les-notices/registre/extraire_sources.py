"""Extraire uniquement les champs documentaires autorisés du dépôt de recherche."""
import argparse
import hashlib
import json
from pathlib import Path

V = 'research/2026-11-17-plantes-repetees'
N = 'research/2026-11-17-verso-premiere-ligne'
K = N + '/knowles'
P = 'voynich_phase45/PAIRS.json'
F25 = 'research/2026-11-18-mots-des-images/racines/fragment25/PREDICTION.md'


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def extract(root, publication):
    sources, facts = {}, {}

    def path_for(path):
        return (root / path) if (root / path).exists() else publication / path

    def load(path):
        raw = path_for(path).read_bytes()
        sources[path] = hashlib.sha256(raw).hexdigest()
        return json.loads(raw)

    def keep(path, keys, array=None):
        data = load(path)
        if array:
            data = data[array]
        facts[path] = [{k: row[k] for k in keys} for row in data]

    for path in [
        V + '/visuel/INVENTAIRE.json', V + '/visuel/DECISIONS.json',
        V + '/visuel/INDEX_CARTES.json', V + '/visuel/CORRECTION.json',
        V + '/visuel/lectures/A.json', V + '/visuel/lectures/B.json',
        V + '/visuel/IMAGES_SOURCES.json',
        N + '/sources/Q15.json', N + '/sources/Q19.json',
        N + '/sources/INVENTAIRE_EXTERNE.json', N + '/sources/PILOTE_KNOWLES.json',
        N + '/visuel/VIGNETTES.json', K + '/CONTRE_LECTURE.json',
        K + '/ATTACHES_Q19.json', K + '/DECISIONS_KNOWLES.json',
    ]:
        facts[path] = load(path)
    for base in [N, K]:
        for tail in ['/visuel/CLE_CARTES.json', '/lectures/A.json', '/lectures/B.json']:
            path = base + tail
            facts[path] = load(path)
        keep(base + '/PREDICTIONS.json', ['fragment','source','labels','targets','destinations'], 'lignes')
        keep(base + '/RESULTATS.json', ['fragment','locus','page','evaluable'], 'cas')
    keep(N + '/VARIANTES.json', ['fragment','locus','dessin'])
    keep(V + '/RESULTATS.json', ['fragment','locus','page','motif_exclusion_texte'], 'lignes')
    path = V + '/verso/audit.json'
    data = load(path)
    facts[path] = [{k: x[k] for k in ['locus','reference','opposees']}
                   for x in data['editions']['IT']['preuves']]
    keep(P, ['fragment','locus','source_page','target','visual_note'], 'pairs')
    # Le document daté fixe le fragment, le lieu et la cible du test exact de f57r.
    # Son contenu textuel et le résultat ne sont pas utilisés par le registre.
    source = path_for(F25)
    if source.exists():
        sources[F25] = hashlib.sha256(source.read_bytes()).hexdigest()
        facts[F25] = {'fragment':25, 'source_page':'f89r1', 'locus':'f89r1.4','target':'f57r'}
    return {'sha256_sources_integrales':sources,'donnees_documentaires':facts}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('depot', type=Path)
    cli.add_argument('--publication', type=Path, default=Path('.'))
    cli.add_argument('--out', type=Path, default=Path(__file__).with_name('sources.json'))
    args = cli.parse_args()
    write(args.out, extract(args.depot, args.publication))
