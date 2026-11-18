"""Compare exact autonomous labels in two IVTFF readings. Standard library only."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
PAGES = {'f68r1': 'Ls', 'f68r2': 'Ls', 'f99r': 'Lf', 'f100r': 'Lf'}
EXPECTED = {'f68r1': 29, 'f68r2': 24, 'f99r': 29, 'f100r': 17}
SHA = {'H': 'ab6f89c1e33352c030e9c9a81ff494b1743e9af3a3a59b95e37c979e39267f21',
       'ZL': 'bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc'}
LINE = re.compile(r'<(f68r1|f68r2|f99r|f100r)\.(\d+),([@+])(L[fs])(?:;([^>]+))?>\s*(.*)')


def extract(path, source):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA[source]:
        raise ValueError(f'Wrong source file for {source}')
    result = {}
    for line in raw.decode('latin-1').splitlines():
        match = LINE.fullmatch(line)
        if not match:
            continue
        page, num, locator, kind, transcriber, text = match.groups()
        if PAGES[page] != kind or transcriber != ('H' if source == 'H' else None):
            continue
        key = (page, int(num), locator)
        if key in result:
            raise ValueError(f'Duplicate locus: {key}')
        result[key] = text.strip()
    return result


def save_extract(h, zl):
    if h.keys() != zl.keys() or len(h) != 100:
        raise ValueError('Different coverage or missing raw loci')
    with (BASE / 'sources.tsv').open('w', newline='') as stream:
        writer = csv.writer(stream, delimiter='\t', lineterminator='\n')
        writer.writerow(['page', 'num', 'locator', 'H', 'ZL'])
        for key in sorted(h, key=lambda k: (list(PAGES).index(k[0]), k[1])):
            writer.writerow([*key, h[key], zl[key]])


def labels():
    pages = {p: [] for p in PAGES}
    with (BASE / 'sources.tsv').open() as stream:
        for row in csv.DictReader(stream, delimiter='\t'):
            page = row['page']
            if row['locator'] == '+':
                # Both ZL scribal lines have fragment number 72; one object label.
                assert (page, row['num'], pages[page][-1]['locus']) == ('f99r', '7', 'f99r.6')
                row0 = pages[page][-1]
                row0['locus'] += '+7'
                for src in SHA:
                    row0[src] += '.' + row[src]
            else:
                pages[page].append({'locus': page + '.' + row['num'], 'H': row['H'], 'ZL': row['ZL']})
    assert {page:len(rows) for page,rows in pages.items()} == EXPECTED
    return pages


def read_label(text):
    text = re.sub(r'<![^>]*>', '', text).replace('<->', '.')
    text = text.translate(str.maketrans('', '', '!{} ')).strip('.')
    if any(c in text for c in '[?,'):
        return None
    words = text.split('.')
    if not all(re.fullmatch(r'(?:[a-z]|@[0-9]{3};)+', word) for word in words):
        raise ValueError(f'Unhandled notation {text}')
    return words


def summary(rows, src):
    readings = [read_label(row[src]) for row in rows]
    counts = Counter(w[0] for w in readings if w is not None and len(w) == 1)
    readable = sum(w is not None for w in readings)
    high = max(counts.values(), default=0)
    return {'positions': len(rows), 'readable': readable, 'single': sum(counts.values()),
            'distinct_single':len(counts), 'max':high,
            'repeated': dict(sorted((k, v) for k, v in counts.items() if v > 1)),
            'frequency': dict(sorted(counts.items()))}


def compare(pages):
    output = {}
    for name, selected in [('full', pages), ('matched', {p:[v[i*(len(v)-1)//5] for i in range(6)] for p,v in pages.items()})]:
        groups = {'stars':selected['f68r1']+selected['f68r2'], 'plants':selected['f99r']+selected['f100r']}
        results = {s:{} for s in SHA}
        for src in SHA:
            stats = {p:summary(v,src) for p,v in {**selected,**groups}.items()}
            def common(a,b):
                ac = stats[a]['frequency']; bc = stats[b]['frequency']
                return {k: [ac[k],bc[k]] for k in sorted(ac.keys() & bc.keys())}
            results[src] = {'stats':stats, 'between_star_panels':common('f68r1','f68r2'),
                            'between_plant_pages':common('f99r','f100r'), 'between_classes':common('stars','plants')}
        agreement = {}
        for cls, rows in groups.items():
            pairs = [(read_label(r['H']), read_label(r['ZL'])) for r in rows]
            comparable = [(h,z) for h,z in pairs if h is not None and z is not None]
            agreement[cls] = {'positions':len(rows), 'comparable':len(comparable),
                              'agree':sum(h==z for h,z in comparable),
                              'agree_single':sum(h==z and len(h)==1 for h,z in comparable)}
        winners = []
        for src in SHA:
            stats = results[src]['stats']
            frequent = []
            for page in ['f68r1', 'f68r2']:
                page_stats = stats[page]
                limit = page_stats['readable'] / 2
                frequent.append({word for word, n in page_stats['frequency'].items() if n > limit})
            candidates = frequent[0] & frequent[1]
            star_counts = stats['stars']['frequency']
            plant_counts = stats['plants']['frequency']
            winners.append({word for word in candidates
                            if star_counts[word] / stats['stars']['readable'] >
                            plant_counts.get(word, 0) / stats['plants']['readable']})
        majority = sorted(winners[0] & winners[1])
        output[name] = {'positions':{p:[r['locus'] for r in v] for p,v in selected.items()}, 'readings':results,
                        'positional_agreement':agreement,'majority_hits':majority}
    return output


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extract', nargs=2, type=Path, metavar=('H_LSI','ZL_IVTFF'))
    args=p.parse_args()
    if args.extract:
        save_extract(extract(args.extract[0],'H'),extract(args.extract[1],'ZL'))
    data=compare(labels())
    (BASE/'resultats.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    for name,d in data.items():
        print(name, 'hits',d['majority_hits'], 'agreement',d['positional_agreement'])
        for s,r in d['readings'].items():
            for key,v in r['stats'].items():
                print(s,key,*(v[k] for k in ['positions','readable','single','distinct_single','max']),v['repeated'])
            print('shared',s,r['between_star_panels'],r['between_plant_pages'],r['between_classes'])

if __name__ == '__main__':
    main()
