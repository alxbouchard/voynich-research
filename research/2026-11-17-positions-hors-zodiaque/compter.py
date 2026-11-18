"""Score preregistered glyph predictions using circle sectors identified on Yale images."""
from collections import Counter
from itertools import product
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
QUARTS = ('HG', 'HD', 'BD', 'BG')
EDITIONS = ('ZL','IT')
WORD = ('oteos','oteey')


def read(name):
    return json.loads((HERE/name).read_text())


def save(name,data):
    (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')


def transcriptions(axes):
    corpus = {}
    for ed in EDITIONS:
        rows = {}
        for line in (HERE/'sources'/(ed+'.txt')).read_text().splitlines():
            match = re.match(r'^<([^,]+),.Cc>\s*(.*)$',line)
            if match and match[1] in axes:
                fields = re.sub(r'<![^>]*>','',match[2]).strip().split('.')
                assert fields and all(fields)
                rows[match[1]]={'zone':axes[match[1]]['zone'],'champs':fields}
        assert set(rows)==set(axes)
        corpus[ed]=rows
    return corpus


def labels_from_starts(size, starts):
    result=[None]*size
    for i,q in enumerate(QUARTS):
        start=starts[q]-1
        stop=starts[QUARTS[(i+1)%4]]-1
        assert 0<=start<size and 0<=stop<size
        for j in range((stop-start)%size):
            pos=(start+j)%size
            assert result[pos] is None
            result[pos]=q
    assert None not in result
    return tuple(result)


def quadrant_views(row,n):
    if 'nominal_par_champ' in row:
        base=tuple(row['nominal_par_champ'])
        variants={base}
        for i, choices in row.get('alternatives_par_champ',{}).items():
            pos=int(i)-1
            variants={v[:pos]+(q,)+v[pos+1:] for v in variants for q in set(choices)|{base[pos]}}
        for v in row.get('autres_scenarios',[]): variants.add(tuple(v))
    else:
        starts=row['premiers']
        base=labels_from_starts(n,starts)
        alternatives=row.get('alternatives',{})
        values=[sorted({starts[q],*alternatives.get(q,[])}) for q in QUARTS]
        variants={labels_from_starts(n,dict(zip(QUARTS,boundaries))) for boundaries in product(*values)}
    assert base in variants and all(len(v)==n and set(v)<=set(QUARTS) for v in variants)
    return base,variants


def counts(values):
    table=Counter(values)
    return {q:table[q] for q in QUARTS}


def analyze(corpus,axes,links,loci,ed,mode):
    total=Counter()
    all_hits={w:Counter() for w in WORD}
    panel_rows={}
    # Keep the numerator and denominator paired for every permissible assignment at each locus.
    feasible={(w,q):{(0,0)} for w in WORD for q in QUARTS}
    for locus in loci:
        fields=corpus[ed][locus]['champs']
        ranks={w:{i for i,value in enumerate(fields,1) if value==w} for w in WORD}
        base,variants=quadrant_views(axes[locus][ed],len(fields))
        for w in WORD:
            sites=[v for v in links if v['locus']==locus and v['forme']==w and v[ed] is not None]
            assert {v[ed] for v in sites}==ranks[w]
            for site in sites:
                assert all(view[site[ed]-1]==site['quart_lu'] for view in variants)
                rank=site[ed]
                assert [fields[(rank-2)%len(fields)],fields[rank%len(fields)]]==site['voisins_'+ed]
            if mode.startswith('commun'):
                ranks[w]={v[ed] for v in sites if all(v[e] is not None for e in EDITIONS)}
        selected=[i for i,f in enumerate(fields,1) if not mode.endswith('simple') or re.fullmatch('[a-z]+',f)]
        sizes=counts(base[i-1] for i in selected)
        total.update(sizes)
        panel_rows[locus]={'champs':sizes}
        for word in WORD:
            positions=ranks[word]
            hits=counts(base[i-1] for i in positions)
            all_hits[word].update(hits)
            panel_rows[locus][word]=hits
            for q in QUARTS:
                choices={(sum(v[i-1]==q for i in positions),sum(v[i-1]==q for i in selected)) for v in variants}
                key=(word,q)
                feasible[key]={(a+c,b+d) for a,b in feasible[key] for c,d in choices}
    result={'champs':dict(total),'n':sum(total.values()),'lignes':panel_rows,'formes':{}}
    for word in WORD:
        stats={}
        for q,n in total.items():
            k=all_hits[word][q]
            pairs=feasible[word,q]
            rates=[100*a/b for a,b in pairs if b]
            stats[q]={'n':n,'k':k,'pour_100':100*k/n if n else None,
                      'n_possible':[min(b for a,b in pairs),max(b for a,b in pairs)],
                      'k_possible':[min(a for a,b in pairs),max(a for a,b in pairs)],
                      'taux_possible':[min(rates),max(rates)] if rates else None}
        result['formes'][word]=stats
    return result


def main():
    pred=read('PREDICTIONS.json')
    assert hashlib.sha256((HERE/'PROTOCOLE.md').read_bytes()).hexdigest()==pred['protocole_sha256']
    axes=read('AXES.json')
    links=read('OCCURRENCES.json')
    corpus=transcriptions(axes)
    save('CERCLES.json',corpus)
    principal=[loc for loc,meta in axes.items() if meta['zone']=='principal']
    secondary=[loc for loc,meta in axes.items() if meta['zone']=='médaillon']
    assert {loc.split('.')[0] for loc in axes}==set(pred['prediction_par_panneau'])
    for site in links:
        if 'champ_ZL_homologue' in site:
            locus=site['locus']
            fields=corpus['ZL'][locus]['champs']
            rank=site['champ_ZL_homologue']
            assert fields[rank-1]==site['lecture_ZL']
            assert [fields[(rank-2)%len(fields)],fields[rank%len(fields)]]==site['voisins_ZL']
            _,variants=quadrant_views(axes[locus]['ZL'],len(fields))
            assert all(view[rank-1]==site['quart_lu'] for view in variants)
    out={}
    for name,loci in [('principal',principal),('medaillons',secondary),('tous_avec_medaillons',principal+secondary)]:
        out[name]={}
        for ed in EDITIONS:
            out[name][ed]={mode:analyze(corpus,axes,links,loci,ed,mode) for mode in ('commun','edition','commun_simple')}
    score={}
    rows=out['principal']['ZL']['commun']['lignes']
    for page,expect in pred['prediction_par_panneau'].items():
        selected=[r for k,r in rows.items() if k.startswith(page+'.')]
        score[page]={w:(sum(r[w][ex['quart']] for r in selected) if selected else None) for w,ex in expect.items()}
    out['score_panneaux']=score
    evaluation={}
    for ed in EDITIONS:
        evaluation[ed]={}
        for mode in ('commun','edition','commun_simple'):
            result=out['principal'][ed][mode]
            comparison={}
            for word in WORD:
                targets={entry[word]['quart'] for entry in pred['prediction_par_panneau'].values()}
                assert len(targets)==1
                target=targets.pop()
                stats=result['formes'][word]
                other_n=sum(v['n'] for q,v in stats.items() if q!=target)
                other_k=sum(v['k'] for q,v in stats.items() if q!=target)
                pages={locus.split('.')[0] for locus,line in result['lignes'].items() if line[word][target]>0}
                comparison[word]={
                    'quart_predit':target,'panneaux_positifs':sorted(pages),
                    'recurrence_atteinte':len(pages)>=pred['recurrence_min_panneaux'],
                    'autres_quarts_reunis':{'k':other_k,'n':other_n,'pour_100':100*other_k/other_n},
                    'depasse_chacun_des_autres_quarts':all(stats[target]['pour_100']>v['pour_100'] for q,v in stats.items() if q!=target),
                    'depasse_les_autres_quarts_reunis':stats[target]['pour_100']>100*other_k/other_n}
            evaluation[ed][mode]=comparison
    out['evaluation']=evaluation
    save('RESULTATS.json',out)
    for ed in EDITIONS:
        r=out['principal'][ed]['commun']
        print(ed,r['champs'],[(w,[v['k'] for v in r['formes'][w].values()]) for w in WORD])


if __name__=='__main__':
    main()
