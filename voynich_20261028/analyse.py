#!/usr/bin/env python3
"""Traceable Voynich audit. No semantic translations are inferred by this script."""
from __future__ import annotations

import collections
import csv
import hashlib
import json
import math
import pathlib
import random
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / 'data'
OUT = ROOT / 'results'
PROTOCOL = json.loads((ROOT / 'PROTOCOL.json').read_text())
SEED = PROTOCOL['seed']
MAPPING = dict(e='water/purification', o='solar/cycle', k='earth/growth',
               y='termination', q='initiation', d='descent/matter',
               s='life/serpent', h='human', a='air/ascension', r='ray/line',
               i='infinite/plural', l='line/stem', n='nature/plural',
               c='cross/earth', t='time/step', f='fire/initiation')


def write_json(name, data):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def physical_leaf(page):
    m = re.match(r'f(\d+)', page)
    # Rosettes foldout includes panels of the 85/86 sheet. Treat as one group.
    if page == 'fRos' or (m and m.group(1) in {'85', '86'}):
        return 'f85_86_foldout'
    return 'f' + m.group(1) if m else page


def normalize(text, commas='split'):
    text = re.sub(r'<[-~]>', '.', text)
    text = re.sub(r'<[^>]*>', '', text)
    while '[' in text:
        text2 = re.sub(r'\[([^\[\]]+)\]', lambda m: m[1].split(':')[0], text)
        if text2 == text:
            raise ValueError('Unbalanced alternative: ' + text)
        text = text2
    text = re.sub(r'@\d{3};', '?', text)
    text = text.replace('{', '').replace('}', '').lower()
    text = text.replace(',', '.' if commas == 'split' else '')
    text = re.sub(r'\s', '', text)
    # Apostrophe is an EVA modifier, not a letter with the proposed semantics.
    text = text.replace("'", '?')
    bad = set(text) - set('abcdefghijklmnopqrstuvwxyz?.')
    if bad:
        raise ValueError(f'Unparsed text characters {bad}: {text}')
    return [t for t in text.split('.') if t]


def parse(name, commas='split'):
    raw = (DATA / name).read_bytes()
    expected = PROTOCOL['corpora'][name]
    assert hashlib.sha256(raw).hexdigest() == expected['sha256'], 'Changed source bytes'
    lines = raw.decode('utf-8').splitlines()
    assert lines[0].startswith('#=IVTFF Eva') and '2.0' in lines[0]
    records, pages, meta = [], {}, {}
    page = None
    for number, line in enumerate(lines, 1):
        if line.startswith('#') or not line:
            continue
        p = re.match(r'^<([^>.]+)>\s*(.*)$', line)
        if p:
            page = p[1]
            assert page not in pages, f'Duplicate page {page}'
            meta = dict(re.findall(r'\$([A-Z])=([^\s>])', p[2]))
            pages[page] = meta.copy()
            continue
        m = re.match(r'^<([^>]+)>\s*(.*)$', line)
        assert m, f'Unexpected line {number}'
        locus, text = m.groups()
        match = re.fullmatch(r'([^.]+)\.(\d+),(.)([PLCR][a-zA-Z0-9])', locus)
        assert match, f'Invalid locus {locus}'
        assert match[1] == page, f'Wrong page on {locus}'
        for key, val in re.findall(r'<@([A-Z])=([^>])>', text):
            meta[key] = val
        tokens = normalize(text, commas)
        clean = [t for t in tokens if '?' not in t]
        records.append(dict(locus=locus, page=page, leaf=physical_leaf(page),
                            number=int(match[2]), locator=match[3], type=match[4],
                            metadata=meta.copy(), raw=text,
                            tokens=tokens, clean=clean))
    assert len(pages) == expected['page_headers']
    assert len(records) == expected['loci']
    assert len({r['locus'] for r in records}) == len(records)
    assert len({r['page'] for r in records}) >= 220
    assert all(r['metadata'].get('I') for r in records)
    assert records[0]['clean'][:6] == ['fachys','ykal','ar','ataiin','shol','shory']
    assert records[-1]['page'] in {'f116r', 'f116v'}
    return records, pages


def entropy(seq):
    c = collections.Counter(seq)
    n = sum(c.values())
    return -sum(v/n * math.log2(v/n) for v in c.values()) if n else None


def conditional_entropy(tokens, order):
    """Empirical within-word H(next EVA letter | previous order letters).

    No cross-word boundaries or start/end symbols; order 0 includes all letters.
    """
    if order == 0:
        return entropy(''.join(tokens))
    joint, ctx = collections.Counter(), collections.Counter()
    for word in tokens:
        for i in range(order, len(word)):
            key = word[i-order:i]
            joint[(key, word[i])] += 1
            ctx[key] += 1
    n = sum(joint.values())
    return -sum(v/n * math.log2(v/ctx[k]) for (k,c),v in joint.items()) if n else None


def stats(tokens, label):
    letters = ''.join(tokens)
    text = ' '.join(tokens)
    freq = collections.Counter(tokens)
    cf = collections.Counter(letters)
    y = sum(w.count('y') for w in tokens)
    q = sum(w.count('q') for w in tokens)
    fib = {1, 2, 3, 5, 8, 13, 21}
    return dict(label=label, tokens=len(tokens), characters_no_spaces=len(letters),
                characters_with_spaces=len(text), types=len(freq),
                qokeedy=freq['qokeedy'], e_count=cf['e'],
                e_percent=100*cf['e']/len(letters),
                H0_no_spaces=entropy(letters), H0_with_spaces=entropy(text),
                H_within_word=[conditional_entropy(tokens,n) for n in range(4)],
                top_words=freq.most_common(10),
                top_trigrams_with_spaces=collections.Counter(text[i:i+3] for i in range(len(text)-2)).most_common(10),
                character_counts=dict(cf), length_histogram=dict(sorted(collections.Counter(map(len,tokens)).items())),
                fibonacci_5_8_13_percent=100*sum(len(w) in {5,8,13} for w in tokens)/len(tokens),
                fibonacci_any_percent=100*sum(len(w) in fib for w in tokens)/len(tokens),
                q_at_start_percent=100*sum(w.startswith('q') for w in tokens)/q if q else None,
                y_at_end_percent=100*sum(w.endswith('y') for w in tokens)/y if y else None,
                words_ending_y_percent=100*sum(w.endswith('y') for w in tokens)/len(tokens),
                unassigned_letters={k:v for k,v in cf.items() if k not in MAPPING},
                mapping_character_coverage_percent=100*sum(v for k,v in cf.items() if k in MAPPING)/len(letters),
                mapping_token_coverage_percent=100*sum(set(w)<=set(MAPPING) for w in tokens)/len(tokens))


def page_table(records):
    groups = {}
    for rec in records:
        if not rec['type'].startswith('P'):
            continue
        m=rec['metadata']
        key=(rec['page'],m.get('I','?'),m.get('L','?'),m.get('H','?'))
        g=groups.setdefault(key,dict(page=rec['page'],leaf=rec['leaf'],section=m.get('I','?'),
                                      currier=m.get('L','?'),hand=m.get('H','?'),quire=m.get('Q','?'),tokens=[]))
        g['tokens'].extend(rec['clean'])
    result=[]
    for g in groups.values():
        letters=''.join(g.pop('tokens'))
        g['chars']=len(letters)
        if len(letters)>=100:
            for c in 'eko':g[c]=letters.count(c)/len(letters)
            result.append(g)
    return result


def matched_test(table, symbol, positive, negative):
    pos=set(positive) if not isinstance(positive,str) else {positive}
    neg={negative}
    # Cluster all same-class panels/sides of a physical leaf; drop mixed-class
    # leaves rather than permuting their correlated parts independently.
    tmp=collections.defaultdict(list)
    for r in table:
        if r['section'] in pos|neg:
            tmp[(r['currier'],r['hand'],r['leaf'])].append(r)
    strata=collections.defaultdict(list)
    dropped=[]
    for (currier,hand,leaf), rows in tmp.items():
        labels={int(r['section'] in pos) for r in rows}
        if len(labels)!=1:
            dropped.append(leaf);continue
        strata[(currier,hand)].append((leaf,labels.pop(),sum(r[symbol] for r in rows)/len(rows)))
    strata={k:v for k,v in strata.items() if len({x[1] for x in v})==2}
    if not strata:
        return dict(symbol=symbol,estimable=False,p=1.0,strata=[],dropped_mixed_leaves=dropped)
    def effect(parts):
        numerator=denominator=0
        for rows, labs in parts:
            a=[row[2] for row,lab in zip(rows,labs) if lab]
            b=[row[2] for row,lab in zip(rows,labs) if not lab]
            weight=min(len(a),len(b))
            numerator+=weight*(sum(a)/len(a)-sum(b)/len(b));denominator+=weight
        return numerator/denominator
    parts=[(v,[x[1] for x in v]) for v in strata.values()]
    obs=effect(parts)
    rng=random.Random(SEED)
    greater=0
    for _ in range(1999):
        null=[]
        for rows,labs in parts:
            perm=labs.copy();rng.shuffle(perm);null.append((rows,perm))
        greater+=effect(null)>=obs-1e-15
    return dict(symbol=symbol,estimable=True,effect_percentage_points=100*obs,
                p=(1+greater)/2000,permutations=1999,dropped_mixed_leaves=dropped,
                strata=[dict(currier=k[0],hand=k[1],positive_leaves=sum(x[1] for x in v),
                             negative_leaves=sum(not x[1] for x in v),leaves=[x[0] for x in v]) for k,v in strata.items()])


def semantic_tests(table):
    tests=[matched_test(table,'e','B','H'),matched_test(table,'k','H','B'),matched_test(table,'o',{'A','Z'},'H')]
    order=sorted(range(len(tests)),key=lambda i:tests[i]['p'])
    previous=0
    for rank,index in enumerate(order):
        previous=max(previous,min(1,tests[index]['p']*(len(tests)-rank)))
        tests[index]['holm_p']=previous
    return tests


def main():
    OUT.mkdir(exist_ok=True)
    parsed={}
    integrity=[]
    # The gate checks both entire corpora before any statistical study starts.
    for name,expected in PROTOCOL['corpora'].items():
        records,pages=parse(name)
        parsed[name]=(records,pages)
        integrity.append(dict(file=name,sha256=expected['sha256'],loci=len(records),
                              pages_with_headers=len(pages),pages_with_loci=len({r['page'] for r in records}),
                              physical_leaf_groups=len({r['leaf'] for r in records}),
                              all_tokens=sum(len(r['tokens']) for r in records),
                              clean_tokens=sum(len(r['clean']) for r in records),
                              unknown_tokens_excluded=sum(len(r['tokens'])-len(r['clean']) for r in records),
                              data_real=True,gate_pass=True))
    write_json('integrity.json',integrity)
    print('DATA INTEGRITY GATE PASSED FOR BOTH CORPORA',flush=True)

    result={}
    sample=(DATA/'submitted_sample.txt').read_text().strip().split()
    result['submitted_sample']=stats(sample,'Exact sample submitted in the conversation')
    result['corpora']={}
    for name,(records,pages) in parsed.items():
        tokens=[w for r in records for w in r['clean']]
        f1=[w for r in records if r['page']=='f1r' for w in r['clean']]
        alts,_=parse(name,commas='join')
        record=dict(full=stats(tokens,name),f1r=stats(f1,name+' f1r'),
                    f1r_raw_lines=[dict(locus=r['locus'],raw=r['raw']) for r in records if r['page']=='f1r'],
                    full_with_uncertain_spaces_joined=stats([w for r in alts for w in r['clean']],name+' commas joined'),
                    page_metadata_for_claimed_examples={p:m for p,m in pages.items() if p in {'f1r','f75r','f87r','f103r','f116v','fRos'} or p.startswith('f68r')},
                    section_tests=semantic_tests(page_table(records)))
        # Explicit check of all cited strings; whitespace normalized identically.
        examples={'f1r':'fachys ykal ar ataiin shol shory cthres ykor sheedy',
                  'f68r':'oteol dain otaiin sheol', 'f75r':'sheor chedy qokeey',
                  'f86v':'daiin chol daiir shey','f87r':'chedy qotol',
                  'f103r':'qotedy chedy qotedy'}
        checks=[]
        for page,excerpt in examples.items():
            candidates=[r for r in records if r['page']==page or r['page'].startswith(page) and r['page'][len(page):].isdigit()]
            checks.append(dict(claimed_page=page,excerpt=excerpt,page_ids=[p for p in pages if p==page or p.startswith(page) and p[len(page):].isdigit()],
                               found_in_any_line=any(excerpt in ' '.join(r['tokens']) for r in candidates),
                               found_in_concatenated_loci=excerpt in ' '.join(w for r in candidates for w in r['tokens'])))
        record['quoted_excerpt_checks']=checks
        result['corpora'][name]=record
        write_json(name.replace('.txt','')+'_records.json',records)
        table=page_table(records)
        with (OUT/(name.replace('.txt','')+'_pages.csv')).open('w') as f:
            writer=csv.DictWriter(f,fieldnames=list(table[0]));writer.writeheader();writer.writerows(table)
        print(name, 'f1r qokeedy:',record['f1r']['qokeedy'],'full words:',len(tokens),flush=True)

    result['semantic_label_invariance']={
        'explanation':'A bijective permutation of assigned meaning labels leaves every text-based likelihood, frequency, entropy and n-gram score exactly unchanged.',
        'original_qokeedy':[MAPPING[c] for c in 'qokeedy'],
        'alternative_qokeedy':['unverified-label-'+str(i) for i in range(7)],
        'semantic_translation_accuracy':None,
        'reason':'No independently readable target text or fixed compositional grammar exists.'}
    write_json('audit.json',result)
    for title,item in [('submitted',result['submitted_sample'])]+[(name+' f1r',r['f1r']) for name,r in result['corpora'].items()]:
        print(title,{k:item[k] for k in ['tokens','characters_no_spaces','qokeedy','e_percent','H0_no_spaces','H0_with_spaces']},flush=True)
    print('AUDIT COMPLETE',flush=True)


if __name__=='__main__':
    main()
