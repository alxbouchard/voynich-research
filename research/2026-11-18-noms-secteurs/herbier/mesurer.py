"""Contrôles à 8 et 16 mots sur deux herbiers, Python standard."""
import csv
import gzip
import hashlib
import json
import re
import unicodedata
from pathlib import Path
from statistics import mean, median

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent.parent
GART = RESEARCH / '2026-11-18-mots-et-dessins/herbier_1485/corpus.json'
MACER = RESEARCH / '2026-11-18-noms-dans-les-notices/historique/source.wiki.gz'
HEADING = re.compile(r'^==\s*([IVXLCDM]+)\.\s*(.*?)\.\s*==\s*$', re.M | re.I)
WINDOWS = (8, 16)
GART_HASH = 'b53eca69ec48df84864d79d97eee4baaa7e67a89ac4c5c74f425724a3038e730'
MACER_HASH = '41ca63622e4fbcc4f52c40d7c9261541c5b6d24ee59ebb2964ece69cee480e26'


def checked(data, expected):
    if hashlib.sha256(data).hexdigest() != expected:
        raise ValueError('Empreinte de la source inattendue')
    return data.decode('utf-8')


def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if not unicodedata.combining(c))


def words(text):
    return re.findall(r'[^\W\d_]+', norm(text))


def macer_source():
    source = checked(gzip.decompress(MACER.read_bytes()), MACER_HASH)
    headers = list(HEADING.finditer(source))
    assert len(headers) == 77
    entries = []
    for i, header in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(source)
        poem = re.fullmatch(r'\s*<poem>\s*(.*?)\s*</poem>\s*', source[header.end():end], re.S)
        if poem is None:
            raise ValueError(f'Bloc sans délimitation au chapitre {i+1}')
        clean = re.sub(r'\{\{Versus\|\d+\}\}', ' ', poem[1])
        assert not any(c in clean for c in '<>{}[]')
        entries.append((header[2], words(clean)))
    return entries


def pattern(word):
    code = {}
    return tuple(code.setdefault(c, len(code)) for c in word)


def inflections(label):
    endings = {'a': 'a ae am as arum is', 'us': 'us i o um e os orum is',
               'um': 'um i o a orum is'}
    for ending, variants in endings.items():
        if label.endswith(ending):
            return {label[:-len(ending)] + form for form in variants.split()}
    return {label}


def rank(scores, target):
    own = scores[target]
    best = max(scores)
    lo = 1 + sum(score > own for score in scores)
    hi = sum(score >= own for score in scores)
    ids = [i + 1 for i, score in enumerate(scores) if score == best]
    return {'score': own, 'rang_min': lo, 'rang_max': hi, 'premier_unique': int(own > 0 and lo == 1 and hi == 1),
            'credit_premier': 1 / hi if lo == 1 else 0, 'meilleur_score': best,
            'meilleures_notices': ','.join(map(str, ids)) if best else 'toutes (aucun indice)'}


def macer_rank(entries):
    rows = []
    for i in range(40, len(entries)):
        title, target = entries[i]
        label = words(title)[0]
        forms = inflections(label)
        for width in WINDOWS:
            for mode in ('longueur', 'patron', 'exact', 'flexion'):
                def score(word):
                    if mode == 'longueur':
                        return int(len(word) == len(label))
                    if mode == 'patron':
                        return int(pattern(word) == pattern(label))
                    if mode == 'exact':
                        return int(word == label)
                    return 2 if word == label else int(word in forms)
                scores = [max(map(score, body[:width])) for _, body in entries]
                matches = [f'{j}/{w}/{len(w)}/{score(w)}' for j, w in enumerate(target[:width], 1) if score(w)]
                rows.append({'chapitre': i + 1, 'titre': title, 'cle': label, 'longueur_cle': len(label),
                             'fenetre': width, 'mots_disponibles': min(width, len(target)), 'mode': mode,
                             'occurrences_cible_position_forme_longueur_score': ' '.join(matches),
                             **rank(scores, i)})
    return rows


def gart_rank():
    items = json.loads(checked(GART.read_bytes(), GART_HASH))['items']
    assert [entry['number'] for entry in items] == list(range(1, 13))
    rows = []
    for i, item in enumerate(items):
        latin_words = 2 if 7 <= i+1 <= 11 else 1
        for language, tokens in [('latin', item['keys'][:latin_words]), ('allemand', item['keys'][latin_words:])]:
            name = list(map(norm, tokens))
            for mode in ('diplomatique', 'initiale_restituee'):
                for width in WINDOWS:
                    places = []
                    for entry in items:
                        body = entry['body' if mode == 'diplomatique' else 'body_expanded_initial'].split()
                        assert len(body) == 24 and entry['missing_initial'] == [1]
                        masked = set(entry['uncertain_word_positions'])
                        if mode == 'initiale_restituee':
                            masked.discard(1)
                        visible = [None if j in masked else norm(w) for j,w in enumerate(body[:width],1)]
                        places.append([j+1 for j in range(len(visible)-len(name)+1) if visible[j:j+len(name)] == name])
                    rows.append({'chapitre': i+1, 'titre': item['title'], 'cle': ' '.join(name),
                                 'longueurs_cle': ','.join(str(len(word)) for word in name),
                                 'langue': language, 'fenetre': width, 'mode': mode,
                                 'positions_cible': ','.join(map(str, places[i])),
                                 **rank([int(bool(p)) for p in places], i)})
    return rows


def summarize(rows, grouping, n):
    groups = {}
    for row in rows:
        groups.setdefault(tuple(row[key] for key in grouping), []).append(row)
    summaries = []
    for group, selected in groups.items():
        unique_issued = sum(r['meilleur_score'] > 0 and ',' not in r['meilleures_notices'] for r in selected)
        summaries.append({**dict(zip(grouping, group)), 'notices':len(selected), 'candidates':n,
                          'indices_sur_la_bonne': sum(r['score'] > 0 for r in selected),
                          'premiers_uniques_corrects':sum(r['premier_unique'] for r in selected),
                          'premiers_uniques_proposes': unique_issued,
                          'attente_corrects_uniques_hasard': round(unique_issued / n, 5),
                          'credit_moyen_premier':round(mean(r['credit_premier'] for r in selected), 6),
                          'credit_hasard': round(1/n, 6),
                          'rang_moyen_ex_aequo':round(mean((r['rang_min']+r['rang_max'])/2 for r in selected), 3),
                          'rang_moyen_hasard': (n+1)/2})
    return summaries


def tsv(filename, rows):
    with (HERE / filename).open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter='\t', lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def audit_reading(entries):
    # Adjudication de la première reprise du nom de rubrique dans le passage.
    # Transcrite après lecture. Elle est tenue hors du score prédictif.
    with (HERE/'lecture_macer.tsv').open(encoding='utf-8') as handle:
        annotated = list(csv.DictReader(handle, delimiter='\t'))
    assert [int(a['chapitre']) for a in annotated] == list(range(41,78))
    rows = []
    for a in annotated:
        chapter = int(a['chapitre'])
        title, body = entries[chapter-1]
        label = words(title)[0]
        position = body.index(a['premiere_forme']) + 1
        rows.append({**a, 'titre':title, 'position_premiere_forme':position, 'longueur_cle':len(label),
                     'longueur_forme':len(a['premiere_forme']), 'debut_16':' '.join(body[:16])})
    return rows


if __name__ == '__main__':
    entries = macer_source()
    # Vérifier la visibilité des seuls invariants testés sous un alphabet permuté.
    for _, body in entries:
        for word in body[:16]:
            translated = ''.join(chr(ord('A')+(ord(c)-ord('a')+13)%26) for c in word)
            assert len(translated) == len(word) and pattern(translated) == pattern(word)
    macer = macer_rank(entries)
    gart = gart_rank()
    tsv('rangs_macer.tsv', macer)
    tsv('rangs_gart.tsv', gart)
    readings = audit_reading(entries)
    tsv('positions_macer.tsv', readings)
    out = {'Macer':summarize(macer, ['fenetre','mode'],77),
           'Gart':summarize(gart, ['fenetre','mode','langue'],12),
           'lecture_macer':{'effectif': len(readings),
                            'position_mediane':median(r['position_premiere_forme'] for r in readings),
                            'position_max':max(r['position_premiere_forme'] for r in readings),
                            'presences':{w:sum(r['position_premiere_forme']<=w for r in readings) for w in WINDOWS}}}
    (HERE/'resultats.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
