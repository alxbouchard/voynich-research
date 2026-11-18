"""Vérifier les votes en marge et donner la performance à l'échelle des paires."""
from collections import Counter
import json
import re
from predire import HERE, corpus


def read(name):
    return json.loads((HERE/name).read_text())


def confusion(rows,field):
    counts = Counter()
    for r in rows:
        val = r[field]
        if val is None or r['etoile'] is None:
            counts['indetermine'] += 1
        else:
            counts[{(True,True):'VP',(False,True):'FN',(True,False):'FP',(False,False):'VN'}[val,r['etoile']]] += 1
    return {k:counts[k] for k in ('VP','FN','FP','VN','indetermine')}


def main():
    predictions = read('PREDICTIONS.json')
    key = read('marges/cle.json')
    by_locus = {v['lieu']:c for c,v in key.items()}
    votes = [read('vote-marges-'+n+'.json')['votes'] for n in ('I','II')]
    assert all(set(v)==set(key) for v in votes)
    sources,_ = corpus()
    rows = {}
    pairs = []
    for pair in predictions['paires_marge']:
        judged = []
        for loc,guess in ((pair['lieu'],True),(pair['temoin'],False)):
            c = by_locus[loc]
            views = [v[c] for v in votes]
            assert all(v in (False,True,None) for v in views)
            starts = {ed:re.sub(r'<![^>]*>','',lines[loc][3]).lstrip().startswith('<%>')
                      for ed,lines in sources.items()}
            rows[loc] = {'lieu':loc,'code':c,'otor':guess,'votes':views,
                         'etoile':views[0] if views[0]==views[1] else None,
                         'debut_paragraphe_par_edition':starts,
                         'debut_paragraphe':starts['H'] if starts['H']==starts['ZL'] else None}
            judged.append(rows[loc])
        pairs.append({'commune':pair['toutes_conventions'],'cible':judged[0],'temoin':judged[1]})
    scopes = {}
    for tag,selection in [('commun',[p for p in pairs if p['commune']]),('ensemble',pairs)]:
        all_rows = [p[r] for p in selection for r in ('cible','temoin')]
        distinct = {r['lieu']:r for r in all_rows}
        scopes[tag] = {'paires':len(selection),'sites_distincts':len(distinct),
                       'word':confusion(all_rows,'otor'),'word_dedoublonne':confusion(distinct.values(),'otor'),
                       'mise_en_page':confusion(all_rows,'debut_paragraphe')}
        for i,reader in enumerate(('I','II')):
            group=[dict(r,etoile=r['votes'][i]) for r in all_rows]
            scopes[tag]['lecteur_'+reader]=confusion(group,'otor')
    (HERE/'RESULTATS-MARGES.json').write_text(json.dumps({'bilans':scopes,'paires':pairs},indent=1,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
