"""Lire le corpus.json du Gart et reproduire le codage des titres et des ouvertures."""
import argparse
import hashlib
import json
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('corpus', type=Path)
args = parser.parse_args()
doc = json.loads(args.corpus.read_bytes())
assert [item['number'] for item in doc['items']] == list(range(1, 13))

# Vérification visuelle des pages portant le titre, sur les douze scans du lot.
sans_image_sur_page_titre = {3, 9}
# Formes autonomes susceptibles d'exprimer les notions testées. Toutes les
# formes effectivement rencontrées dans ces 12 titres figurent dans la sortie.
generiques = set('planta plante plantae plantas plantam plantarum pflanze pflanzen herba erba herbae herbas herbam herbis herbarum kraut kraute krut krude crut crute krute radix radices radicis radicem radicibus radicum wurz wurzel wurzeln wurtz wortz wurtzel wortzel'.split())
rows = []
for item in doc['items']:
    words = item['title'].casefold().split()
    body = item['body'].casefold().split()
    assert len(body) == 24
    rows.append({
        'chapitre': item['number'], 'vue': item['view'], 'source': item['url'],
        'titre': item['title'], 'image_sur_la_page_du_titre': item['number'] not in sans_image_sur_page_titre,
        'titres_generiques': [w for w in words if w in generiques],
        'composes_en_wortz': [w for w in words if w.endswith('wortz') and w != 'wortz'],
        'debut_prose_generiques': [{'mot': w, 'position': j, 'lecture_incertaine': j in item['uncertain_word_positions']} for j, w in enumerate(body, 1) if w in generiques]
    })
print(json.dumps({'sha256_corpus': hashlib.sha256(args.corpus.read_bytes()).hexdigest(), 'notices': rows}, ensure_ascii=False, indent=2))
