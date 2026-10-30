"""Conservative EVA label/prose pilot. No words are assigned a meaning."""
from pathlib import Path
from collections import Counter, defaultdict
import hashlib, json, re
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
N_PERM = 10000
SEED = 20261029

def parse(path):
    meta, rows = {}, []
    for line in path.read_text().splitlines():
        h = re.match(r'^<(f[^.>]+)>\s+<! (.+)>', line)
        if h:
            meta[h[1]] = dict(re.findall(r'\$(\w)=(\S+)', h[2]))
        m = re.match(r'^<(f[^.>]+)\.(\d+),([^>]+)>\s+(.+)', line)
        if not m:
            continue
        page, num, kind, raw = m.groups()
        # A drawing break is a delimiter, never concatenated away.
        clean = re.sub(r'<[^>]*>', '', raw.replace('<->', '.')).strip()
        rows.append(dict(page=page, num=int(num), locus=f'{page}.{num}',
                         kind=kind, raw=raw, clean=clean,
                         tokens=[s for s in clean.split('.') if re.fullmatch('[a-z]+', s)],
                         metadata=meta[page]))
    assert len({r['locus'] for r in rows}) == len(rows), 'Duplicate locus'
    return meta, rows

def single_label(r):
    return r['kind'][0] != '!' and r['kind'][1:2] == 'L' and re.fullmatch('[a-z]{3,}', r['clean']) is not None

def stats_matrix(blocks, texts, dedup=False):
    return np.array([[sum(w in text for w in (set(b) if dedup else b)) for text in texts]
                     for b in blocks], dtype=float)

def permutations(matrix, denominators, groups=None, seed=SEED):
    n = matrix.shape[0]
    rng = np.random.default_rng(seed)
    ids = np.arange(n)
    perms = []
    for _ in range(N_PERM):
        if groups is None:
            p = rng.permutation(n)
        else:
            p = ids.copy()
            for group in groups:
                p[group] = rng.permutation(group)
        perms.append(p)
    perms = np.asarray(perms)
    values = matrix[ids[None, :], perms]
    samples = values.sum(axis=1)
    normalized = (values / np.asarray(denominators)[None, :]).mean(axis=1)
    def result(obs, null):
        return dict(observed=float(obs), null_mean=float(null.mean()),
                    null_sd=float(null.std(ddof=1)), null_q025=float(np.quantile(null,.025)),
                    null_q975=float(np.quantile(null,.975)),
                    p_upper=float((1 + np.count_nonzero(null >= obs)) / (N_PERM + 1)),
                    permutations=N_PERM, seed=seed)
    return dict(count=result(np.trace(matrix), samples),
                page_normalized=result(np.mean(matrix.diagonal()/denominators), normalized))

def label_test(rows):
    bypage = defaultdict(list)
    for r in rows:
        if r['metadata'].get('I') == 'P' and r['kind'][0] != '!':
            bypage[r['page']].append(r)
    pages, blocks, texts, detail = [], [], [], []
    for page, rr in bypage.items():
        labels = [r for r in rr if r['kind'][1:] in ('Lf','Lc') and single_label(r)]
        prose = [w for r in rr if r['kind'][1:2] == 'P' for w in r['tokens']]
        if not labels or not prose:
            continue
        pages.append(page); blocks.append([r['clean'] for r in labels]); texts.append(set(prose))
        detail.append(dict(page=page, metadata=rr[0]['metadata'], n_labels=len(labels),
                           n_prose_tokens=len(prose), n_prose_types=len(set(prose)),
                           hits=[dict(locus=r['locus'], word=r['clean'], kind=r['kind'])
                                 for r in labels if r['clean'] in set(prose)],
                           labels=[dict(locus=r['locus'], word=r['clean'],kind=r['kind']) for r in labels]))
    matrix = stats_matrix(blocks, texts)
    denom = [len(b) for b in blocks]
    result = dict(pages=detail, n_pages=len(pages), n_labels=sum(denom),
                  n_page_label_types=sum(len(set(b)) for b in blocks),
                  primary=permutations(matrix, denom))
    groups = [[i for i,d in enumerate(detail) if d['metadata']['Q'] == q]
              for q in sorted({d['metadata']['Q'] for d in detail})]
    result['within_quire_sensitivity'] = permutations(matrix, denom, groups)
    result['deduplicated_within_page_sensitivity'] = permutations(stats_matrix(blocks,texts,True), [len(set(b)) for b in blocks])
    # Permuting rows and columns yields the same diagonal total. An independently
    # written list-of-sets count verifies the primary observed statistic.
    direct = sum(sum(label in text for label in labels) for labels,text in zip(blocks,texts))
    assert direct == result['primary']['count']['observed']
    assert sum(len(d['hits']) for d in detail) == direct
    result['score_matrix'] = matrix.astype(int).tolist()
    return result

def main():
    sources = {k:parse(ROOT/'data'/f)[1] for k,f in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]}
    maps = {k:{r['locus']:r for r in rows} for k,rows in sources.items()}
    label_stats = {}
    for k,rr in sources.items():
        labs = [r for r in rr if r['kind'][1:2] == 'L' and r['kind'][0] != '!']
        label_stats[k] = dict(all_label_loci=len(labs), clean_single_ge3=sum(single_label(r) for r in labs))
    agreeing = [r for r in sources['ZL'] if single_label(r) and r['locus'] in maps['IT']
                and single_label(maps['IT'][r['locus']])
                and r['clean'] == maps['IT'][r['locus']]['clean']]
    grouped = defaultdict(list)
    for r in agreeing: grouped[r['clean']].append(r)
    candidates = sorted([w for w,rr in grouped.items() if len({r['page'] for r in rr})>=2], key=lambda w:(-len(grouped[w]),w))[:10]
    candrows=[]
    for word in candidates:
        candrows.append(dict(eva=word, n_agreeing_labels=len(grouped[word]), n_pages=len({r['page'] for r in grouped[word]}),
            contexts=sorted({r['kind'][1:] for r in grouped[word]}),
            loci=[dict(locus=r['locus'],kind=r['kind']) for r in grouped[word]],
            prose_occurrences={k:sum(r['tokens'].count(word) for r in rr if r['kind'][0]!='!' and r['kind'][1:2]=='P') for k,rr in sources.items()}))
    results = dict(date='2026-10-29', method='Exact EVA matching; no semantic mapping',
                   label_stats=label_stats, n_exact_agreeing_labels=len(agreeing),
                   candidates=candrows, tests={k:label_test(rr) for k,rr in sources.items()},
                   limitations=['Two transcriptions of the same physical source are sensitivity checks, not independent replications.',
                   'No assertion that a label denotes the nearest object.',
                   'Non-random pages, shared leaves, label type and prose length can affect exchangeability.',
                   'Exact matching can miss inflection, compound splitting and transcription uncertainty.',
                   'An association would not identify a language; non-significance does not prove no relation.'])
    # Positive and negative executable controls of the statistic and permutation path.
    positive = stats_matrix([[f'unique{i}'] for i in range(16)], [{f'unique{i}'} for i in range(16)])
    negative = stats_matrix([['absent'] for _ in range(16)], [{f'unique{i}'} for i in range(16)])
    assert np.trace(positive)==16 and np.trace(negative)==0
    results['controls'] = dict(positive=permutations(positive,[1]*16), negative=permutations(negative,[1]*16))
    assert results['controls']['positive']['count']['p_upper'] < .001
    assert results['controls']['negative']['count']['p_upper'] == 1
    (ROOT/'results/labels.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    (ROOT/'results/parsed_loci.json').write_text(json.dumps(sources,ensure_ascii=False))
    summary={k:dict(n_pages=v['n_pages'], n_labels=v['n_labels'], primary=v['primary'], within_quire=v['within_quire_sensitivity'],dedup=v['deduplicated_within_page_sensitivity']) for k,v in results['tests'].items()}
    print(json.dumps(dict(label_stats=label_stats,n_agree=len(agreeing),candidates=candrows,tests=summary,controls=results['controls']),ensure_ascii=False,indent=2))

if __name__ == '__main__': main()
