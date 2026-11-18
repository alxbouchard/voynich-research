"""Rejouer les clés littérales de la légende otaly sur les autres feuillets."""
from collections import Counter, defaultdict
import csv
from functools import reduce
from hashlib import sha256
from itertools import combinations, permutations
import json
from operator import and_
from pathlib import Path
import re
import statistics
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[2]
sys.path.insert(0, str(RESEARCH / '2026-11-18-formes-souterraines/nom/second'))
import transfert as transcription
HEAD = 'otaly'
WORD = re.compile('[otaly]{3,}')
LEXICON = RESEARCH / '2026-11-18-opcheor-paralleles/latin/corpus.json'
HEX = 'c251598bbab3f9f93de40a72d4e039c17f52ce079dd95e86c7322f9a2283893b'


def store_tsv(name, header, rows):
    with (HERE / name).open('w') as file:
        tsv = csv.writer(file, delimiter='\t', lineterminator='\n')
        tsv.writerow(header)
        tsv.writerows(rows)


def parse(raw, cut):
    # Les ruptures physiques et espaces étendus séparent deux groupes.
    raw = re.sub(r'<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>', '.', raw, flags=re.I)
    raw = re.sub(r'\{[^}]*\}', '?', raw)
    return [word for word in transcription.tokens(raw, cut) if WORD.fullmatch(word)]


def gather(editions):
    results = []
    common_lines = Counter()
    for loc in sorted(set.intersection(*(set(ed) for ed in editions.values())), key=natural_locus):
        rows = [ed[loc] for ed in editions.values()]
        page, kind, _, _ = rows[0]
        if any(row[1] != kind for row in rows) or not kind.startswith('P'):
            continue
        if int(re.match(r'f(\d+)', page)[1]) in (88, 99):
            continue
        common_lines[kind] += 1
        versions = [Counter(parse(raw, cut)) for _, _, _, raw in rows for cut in ('joints', 'separes')]
        for word, count in sorted(reduce(and_, versions).items()):
            results.append((loc, kind, word, count))
    return results, common_lines


def adjacent(raw, cut):
    # Une lacune matérielle interrompt tout voisinage, même entre mots lisibles.
    found = Counter()
    chunks = re.split(r'<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>', raw, flags=re.I)
    for chunk in chunks:
        words = transcription.tokens(re.sub(r'\{[^}]*\}', '?', chunk), cut)
        for left, right in zip(words, words[1:]):
            if left != HEAD and right != HEAD and WORD.fullmatch(left) and WORD.fullmatch(right):
                found[left, right] += 1
    return found


def pairs_in_context(editions, chapters):
    attested = {w for words in chapters.values() for w in words}
    phrases = {(a, b) for words in chapters.values() for a, b in zip(words, words[1:])}
    out = []
    source = []
    for loc in sorted(set.intersection(*(set(ed) for ed in editions.values())), key=natural_locus):
        rows = [ed[loc] for ed in editions.values()]
        page, kind, _, _ = rows[0]
        if (not kind.startswith('P') or any(row[1] != kind for row in rows)
                or int(re.match(r'f(\d+)', page)[1]) in (88, 99)):
            continue
        counts = [adjacent(raw, cut) for _, _, _, raw in rows for cut in ('joints', 'separes')]
        for pair, count in sorted(reduce(and_, counts).items()):
            translated = read_forms(tuple('radix'), pair)
            a, b = [translated[w] for w in pair]
            out.append([loc, kind, *pair, a, b, count, int(a in attested and b in attested), int((a, b) in phrases)])
            source.append(pair)
    store_tsv('voisins.tsv', ['lieu','type','eva_gauche','eva_droite','latin_gauche','latin_droite',
                              'multiplicite_minimum','deux_formes_attestees','ordre_atteste'], out)
    return dict(paires_differentes=len(set(source)), occurrences=sum(r[6] for r in out),
                deux_sorties_attestees=sum(r[6]*r[7] for r in out),
                succession_dans_macer=sum(r[6]*r[8] for r in out),
                occurrences_P0=sum(r[6] for r in out if r[1]=='P0'))


def natural_locus(loc):
    num, side, panel, row = re.fullmatch(r'f(\d+)([rv])(\d*)\.(\d+)', loc).groups()
    return int(num), side, int(panel or '0'), int(row)


def keys(target):
    for cuts in combinations(range(1, len(target)), len(HEAD) - 1):
        bounds = (0, *cuts, len(target))
        yield tuple(target[i:j] for i, j in zip(bounds, bounds[1:]))


def read_forms(key, counts):
    trans = dict(zip(HEAD, key))
    return {w: ''.join(trans[c] for c in w) for w in counts}


def score(outputs, counts, known):
    matches = sorted(w for w, translated in outputs.items() if translated in known)
    return len(matches), sum(counts[w] for w in matches), matches


def bench(counts, known, kind):
    main, null = [], []
    for target in ('radix', 'foliis', 'flos'):
        for key in keys(target):
            direct = read_forms(key, counts)
            ntypes, ntokens, hits = score(direct, counts, known)
            comparators = []
            for perm in sorted(set(permutations(key))):
                values = read_forms(perm, counts)
                nty, nto, _ = score(values, counts, known)
                comparators.append((nty, nto))
                null.append([kind, target, '/'.join(key), '/'.join(perm), int(key == perm), nty, nto])
            ref = [{'eva': w, 'lecture': direct[w], 'occurrences': counts[w]} for w in hits]
            main.append(dict(cible=target, valeurs=key, types=ntypes, occurrences=ntokens, rencontres=ref,
                             nombre_permutations=len(comparators),
                             au_moins_autant_types=sum(a >= ntypes for a, _ in comparators),
                             au_moins_autant_occurrences=sum(b >= ntokens for _, b in comparators),
                             au_moins_autant_les_deux=sum(a >= ntypes and b >= ntokens for a, b in comparators)))
    return main, null


def coverage(chapters):
    document_frequency = Counter(w for words in chapters.values() for w in set(words))
    scores = []
    for name, words in chapters.items():
        types = set(words)
        seen = sum(document_frequency[w] > 1 for w in words)
        seen_types = sum(document_frequency[w] > 1 for w in types)
        scores.append([name, len(words), seen, len(types), seen_types])
    store_tsv('couverture.tsv', ['notice', 'mots', 'mots_vus_ailleurs', 'types', 'types_vus_ailleurs'], scores)
    restricted = Counter(w for words in chapters.values() for w in words
                         if len(w) >= 3 and w != 'radix' and set(w) <= set('radix'))
    return dict(sensibilite_alphabet_radix_et_sans_radix=dict(effectifs=restricted,
                retrouves=sum(n for w, n in restricted.items() if document_frequency[w] > 1)),
                mots=sum(row[1] for row in scores), retrouves=sum(row[2] for row in scores),
                types_compte_par_notice=sum(row[3] for row in scores),
                types_par_notice_retrouves=sum(row[4] for row in scores),
                moyenne_des_taux=statistics.mean(row[2] / row[1] for row in scores),
                min_des_taux=min(row[2] / row[1] for row in scores),
                max_des_taux=max(row[2] / row[1] for row in scores))


def main():
    assert parse('otal.{ty}.o[ta:o]l.oto?l.oty<??>.otol<!gap>tyl<->ytal.%', 'joints') == ['otal', 'otol', 'tyl','ytal']
    assert parse('otal,y','joints') == ['otaly'] and parse('otal,y','separes') == ['otal']
    assert sha256(LEXICON.read_bytes()).hexdigest() == HEX
    chapters = json.loads(LEXICON.read_bytes())
    lexicon = {w for words in chapters.values() for w in words}
    editions, _ = transcription.corpus()
    allrows, nlines = gather(editions)
    removed_head = sum(n for _, _, w, n in allrows if w == HEAD)
    rows = [row for row in allrows if row[2] != HEAD]
    store_tsv('lignes.tsv', ['lieu', 'type', 'eva', 'multiplicite_minimum'], rows)
    results = {'cle_ordre': HEAD, 'editions': transcription.langage.HASH, 'macer_sha256': HEX, 'lexique_types': len(lexicon),
               'lignes_communes': nlines, 'occurrences_otaly_ecartees': removed_head, 'controle_couverture': coverage(chapters),
               'temoin_flos_nombre_tables': len(list(keys('flos'))), 'domaines': {}}
    assert adjacent('alol.lol.dol.alol<->lol.otaly.lol', 'joints') == {('alol','lol'): 1}
    results['paires'] = pairs_in_context(editions, chapters)
    all_null = []
    for category in ['tous_P', 'P0']:
        frequencies = Counter()
        occurrences = defaultdict(list)
        for loc, kind, word, n in rows:
            if category == 'P0' and kind != 'P0':
                continue
            frequencies[word] += n
            occurrences[word].append([loc, n])
        actual, null = bench(frequencies, lexicon, category)
        all_null.extend(null)
        results['domaines'][category] = dict(types=len(frequencies), occurrences=frequencies.total(), tables=actual)
        if category == 'tous_P':
            translations = read_forms(tuple('radix'), frequencies)
            store_tsv('radix.tsv', ['eva','latin','occurrences','dans_macer','premiers_lieux'],
                      ([w,translations[w],n,int(translations[w] in lexicon),','.join(pair[0] for pair in occurrences[w][:5])]
                       for w,n in sorted(frequencies.items(), key=lambda kv:(-kv[1], kv[0]))))
    store_tsv('permutations.tsv', ['domaine','cible','valeurs_initiales','valeurs_permutes','predite','types','mots'], all_null)
    (HERE/'resultats.json').write_text(json.dumps(results, ensure_ascii=False, indent=1)+'\n')


if __name__ == '__main__':
    main()
