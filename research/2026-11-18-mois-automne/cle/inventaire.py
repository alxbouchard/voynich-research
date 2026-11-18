"""Inventorie les graphies rencontrées et vérifie leur sélection contre le déchiffreur."""
from collections import defaultdict
import json
import re

from dechiffrer import DATA, FILES, HERE, LINE, PANELS, SCOPES, read_pages, tokens, vocab


def readings():
    rows = defaultdict(dict)
    for edition, filename in FILES.items():
        for line in (DATA / filename).read_text().splitlines():
            match = LINE.match(line)
            if not match or match[1] not in PANELS:
                continue
            page, rank, _, kind, raw = match.groups()
            versions = rows[page, kind, page + '.' + rank]
            for cut in ('joints', 'separes'):
                assert (edition, cut) not in versions
                versions[edition, cut] = tokens(raw, cut)
    return rows


def status(word, parts, kind):
    if word not in parts:
        return '.'
    if not re.fullmatch('[a-z]+', word):
        return '?'
    if kind == 'Lz' and len(parts) != 1:
        return 'm'
    return '+'


def inventory():
    views = SCOPES['accord']
    rows = readings()
    dataset = read_pages(PANELS)
    result = {'ordre_des_lectures': ['/'.join(v) for v in views], 'panneaux': {}}
    for page in PANELS:
        result['panneaux'][page] = panel = {}
        for kind in ('Lz', 'Cc'):
            places = {}
            count = {'loci': 0, 'loci_avec_accord': 0, 'graphies_locus_utilisables': 0,
                     'graphies_locus_exclues': 0}
            accepted = defaultdict(list)
            for (p, k, loc), versions in rows.items():
                if (p, k) != (page, kind):
                    continue
                by_status = defaultdict(list)
                for word in sorted(set().union(*versions.values())):
                    code = ''.join(status(word, versions.get(v, ()), kind) for v in views)
                    by_status[code].append(word)
                common = by_status.pop('+' * len(views), [])
                places[loc] = {'utilisables': common, 'exclues': dict(sorted(by_status.items()))}
                missing = ['/'.join(v) for v in views if v not in versions]
                if missing:
                    places[loc]['lectures_absentes'] = missing
                for word in common:
                    accepted[word].append(loc)
                count['loci'] += 1
                count['loci_avec_accord'] += bool(common)
                count['graphies_locus_utilisables'] += len(common)
                count['graphies_locus_exclues'] += sum(map(len, by_status.values()))
            reference, loci = vocab(dataset, 'accord', page, kind)
            assert count['loci'] == loci
            assert {w: sorted(locs) for w, locs in accepted.items()} == {
                ''.join(w): locs for w, locs in reference.items()}
            count['graphies_utilisables_distinctes_du_panneau'] = len(accepted)
            panel[kind] = {'effectifs': count, 'loci': places}
    return result


if __name__ == '__main__':
    output = json.dumps(inventory(), ensure_ascii=False, separators=(',', ':'))
    (HERE / 'INVENTAIRE.json').write_text(output + '\n')
