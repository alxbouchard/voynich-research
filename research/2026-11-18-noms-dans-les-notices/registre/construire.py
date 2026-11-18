"""Construire les lignes d'inventaire et la vue éclatée par proposition."""
import argparse
import csv
import hashlib
import itertools
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from extraire_sources import F25, K, N, P, V, write

HERE = Path(__file__).resolve().parent
QURL = 'https://voynich.nu/q{:02}/index.html'
PETERSEN = 'https://www.voynich.nu/extra/herb_oldid.html'
STOLFI = 'https://www.ic.unicamp.br/en/~stolfi/EXPORT/voynich/00-06-07-word-grammar/Notes/064/work/projects/voynich/projects/programs/c/big/big/projects/voynich/Notes/102/work/Notes/091/report/report_091.html'


def build(inputs):
    data = inputs['donnees_documentaires']
    rows = {}
    ambiguous = []
    def entry(fragment, quire):
        if fragment not in rows:
            rows[fragment] = dict(fragment=fragment, quire=quire, source_page=None,
                                  loci=[], targets=[], attachment=None, double_agreement=None,
                                  position={}, evidence=[], cards=[], prior_tests=[], alternatives=[])
        assert rows[fragment]['quire'] == quire
        return rows[fragment]

    def evidence(row, path, **detail):
        row['evidence'].append(dict(path=path, **detail))

    def target(row, page):
        if page not in row['targets']:
            row['targets'].append(page)

    def test(row, kind, path, locus, page, **detail):
        row['prior_tests'].append(dict(kind=kind, path=path, locus=locus, target=page, **detail))

    def attach(row, status, reason, path):
        row['attachment'] = status
        evidence(row, path, attachment=status, reason=reason)

    path = V + '/visuel/INVENTAIRE.json'
    for item in data[path]:
        r = entry(item['fragment'],item['catalogue'])
        r['loci'] = item['loci']
        if item['loci']:
            r['source_page'] = item['loci'][0].split('.')[0]
        for page in item['pages']:
            target(r,page)
        evidence(r, path, source='Zandbergen', targets=item['pages'], qualification=item['qualification'],
                 source_url=QURL.format(r['quire']), initial_exclusion=item['exclusion'])
    path = N + '/sources/Q15.json'
    for item in data[path]:
        r = entry(item['fragment'], 15)
        r.update(source_page=item['source_folio'], loci=[item['locus']],
                 position=dict(row=item['row'], column=item['column'], frame=item['photo_frame'],
                               source_bbox=item['source_bbox']))
        for page in item['target_pages']:
            target(r,page)
        attach(r,'sure' if item['attachment_secure'] else 'faible', item['reason'], path)
    path = N + '/sources/Q19.json'
    for item in data[path]['cas']:
        r = entry(item['fragment'],19)
        r.update(source_page=item['source'],loci=item['loci'],position=dict(row=item['rang'],column=item['colonne']))
        for page in item['pages']:
            target(r,page)
        attach(r,{'nette':'sure','ambigue':'faible','absente':'absente','multiple':'multiple'}[item['attache']],
               item['raison'], path)
    path = N + '/sources/INVENTAIRE_EXTERNE.json'
    for item in data[path]:
        r = rows[item['fragment']]
        assert item['page'] in r['targets']
        for src in item['sources']:
            who = src['source']
            url = STOLFI if 'Stolfi' in who else PETERSEN if 'marginalia' in who else QURL.format(r['quire'])
            evidence(r,path, target=item['page'],source_detail=src,source_url=url)
    path = K + '/ATTACHES_Q19.json'
    for item in data[path]['cas']:
        r = entry(item['fragment'],19)
        r.update(source_page=r['source_page'] or item['source'],loci=item['loci'],position=dict(row=item['rang'],column=item['colonne']))
        target(r,item['page_proposee'])
        attach(r,{'nette':'sure','ambigue':'faible','absente':'absente'}[item['attache']],item['motif'],path)
    path = K + '/CONTRE_LECTURE.json'
    decisions = {x['carte']:x for x in data[K + '/DECISIONS_KNOWLES.json']}
    sources = {x['rank']:x for x in data[N + '/sources/PILOTE_KNOWLES.json']}
    for item in data[path]:
        rank = item['rank']
        name = f'MK{rank:02}'
        image = decisions[name]
        info = dict(rank=rank, montage=name, source_url=sources[rank]['image_link'],
                    thumbnail_url=sources[rank]['thumbnail'], target=item['page_herbier'],
                    source_page=item['page_fragments'], reason=item['raison'], status=item['statut'],
                    source_photo=image['photo_fragment'], target_photo=image['photo_grande_page'])
        if len(item['numeros']) != 1:
            assert len(item['numeros']) == len(item['loci'])
            options = [dict(fragment=f,locus=l) for f,l in zip(item['numeros'],item['loci'])]
            ambiguous.append(dict(**info, quire=15, alternatives=options, path=path))
            for option in options:
                if option['fragment'] in rows:
                    rows[option['fragment']]['alternatives'].append(dict(montage=name, target=info['target'], **option))
            continue
        r = rows[item['numeros'][0]]
        assert info['target'] in r['targets']
        evidence(r,path, **info)
        if r['fragment']==199:
            # L'édition regroupe les deux panneaux en f101v, le montage localise le droit en f101v1.
            r['source_page'] = item['page_fragments']
            r['editorial_page'] = 'f101v'
        if item['attache_sure'] is False:
            attach(r,'faible',item['raison'],path)
    for pilot in data[P]:
        r = rows[pilot['fragment']]
        test(r,'phase45',P,pilot['locus'],pilot['target'])
        if r['attachment'] is None:
            attach(r,'pilote_non_cotee',pilot['visual_note'],P)
        evidence(r,P,source='coordinateur, examen non aveugle',target=pilot['target'],reason=pilot['visual_note'])

    def card(r, card_id, options, expected, readers, path, sha, active=True):
        def unpack(reader):
            c = reader['choice']
            return dict(choice=c,page=options[ord(c)-65] if c else None, confidence=reader['confidence'])
        votes = [unpack(x) for x in readers]
        agree = all(x['choice']==expected and x['confidence'] in ('moyenne','forte') for x in votes)
        if active:
            assert r['double_agreement'] is None and options[ord(expected)-65] in r['targets']
            r['double_agreement'] = agree
        r['cards'].append(dict(id=card_id, options=options, expected=expected, votes=votes, active=active,
                               both_choose_expected=all(x['choice']==expected for x in votes),
                               double_agreement=agree, path=path,sha256=sha))

    path = V + '/visuel/INDEX_CARTES.json'
    old_cards = {x['id']:x for x in data[path]}
    corrected = data[V + '/visuel/CORRECTION.json']
    old = old_cards['V09']
    r = rows[old['fragment']]
    card(r,'V09',old['choices'],old['expected'],[data[V + f'/visuel/lectures/{e}.json']['V09'] for e in 'AB'],
         path,old['sha256'],False)
    old_cards[corrected['id']] = corrected
    path = V + '/visuel/DECISIONS.json'
    for item in data[path]:
        r = rows[item['fragment']]
        attach(r,'sure' if item['attache_sure'] else 'faible',item['motif_attache'],path)
        key = old_cards[item['carte']]
        card(r,item['carte'],key['choices'],key['expected'],item['choix_visuels'],path,key['sha256'])
        assert r['double_agreement'] == item['accord_visuel']
    for base in [N,K]:
        path = base + '/visuel/CLE_CARTES.json'
        for key in data[path]:
            reads = [data[base + f'/lectures/{e}.json'][key['id']] for e in 'AB']
            card(rows[key['fragment']],key['id'],key['candidats'],key['attendu'],reads,path,key['sha256'])
    for base in [N,K]:
        path = base + '/PREDICTIONS.json'
        for pre in data[path]:
            r=rows[pre['fragment']]
            assert set(pre['targets'])<=set(r['targets']) and set(pre['labels'])==set(r['loci'])
            r['prior_destinations'] = pre['destinations']
        path = base + '/RESULTATS.json'
        for v in data[path]:
            test(rows[v['fragment']], 'dessin_dos_ligne1' if v['evaluable'] else 'inscrit_non_evaluable_dessin_dos_ligne1',
                 path,v['locus'],v['page'])
    path = N + '/VARIANTES.json'
    for v in data[path]:
        test(rows[v['fragment']],'variante_edition_dos',path,v['locus'],v['dessin'])
    path = V+'/RESULTATS.json'
    for v in data[path]:
        test(rows[v['fragment']], 'classement_corps' if v['motif_exclusion_texte'] is None else 'classement_ecarte',
             path,v['locus'],v['page'],reason=v['motif_exclusion_texte'])
    path=V+'/verso/audit.json'
    for v in data[path]:
        rs=[r for r in rows.values() if v['locus'] in r['loci']]
        assert len(rs)==1
        test(rs[0],'audit_exact_dessin_dos',path,v['locus'],v['reference'],opposite=v['opposees'])
    if F25 in data:
        v=data[F25]
        test(rows[v['fragment']],'page_entiere_mot_exact_18nov',F25,v['locus'],v['target'])
        evidence(rows[25],F25, source='localisation de la rangée, 18 novembre',
                 reason='L’ordre des légendes et le cadrage de Yale placent le locus auprès du fragment 25. La cote faible du contrôle du 17 novembre reste visible.',
                 source_url='https://collections.library.yale.edu/iiif/2/1006233/2830,105,2410,865/1800,/0/default.jpg')

    by_page=defaultdict(set)
    by_folio=defaultdict(set)
    phy=lambda p: re.match(r'f\d+',p).group()
    for r in rows.values():
        assert r['source_page'] and r['attachment'] and r['targets']
        for p in r['targets']:
            by_page[p].add(r['fragment'])
            by_folio[phy(p)].add(r['fragment'])
    for r in rows.values():
        assert bool(r['loci']) == (r['attachment']!='absente')
        r['target_shared_with']={p:sorted(by_page[p]-{r['fragment']}) for p in r['targets'] if len(by_page[p])>1}
        r['target_folio_shared_with']={p:sorted(by_folio[phy(p)]-{r['fragment']}) for p in r['targets'] if len(by_folio[phy(p)])>1}
        r['ambiguous_montages_sharing_target']={p:[m['montage'] for m in ambiguous if p==m['target']]
                                                for p in r['targets'] if any(p==m['target'] for m in ambiguous)}
        r['source_folio']=phy(r['source_page'])
        r['unique_locus_target']=len(r['loci'])==1 and len(r['targets'])==1
        r['cross_product']=[{'locus':l,'target':p} for l,p in itertools.product(r['loci'],r['targets'])]
    return dict(fragments=[rows[n] for n in sorted(rows)],montages_indetermines=ambiguous)


def output(registry, out):
    write(out/'registre.json',registry)
    rows=registry['fragments']
    summaries=[]
    for quire in [15,19]:
        subset=[r for r in rows if r['quire']==quire]
        summaries.append(dict(quire=quire, fragments=len(subset),attaches=dict(Counter(r['attachment'] for r in subset)),
                              unique=sum(r['unique_locus_target'] for r in subset),
                              loci_uniques_et_attache_sure=[r['fragment'] for r in subset if r['unique_locus_target'] and r['attachment']=='sure'],
                              double_accord=[r['fragment'] for r in subset if r['double_agreement']],
                              attache_sure_et_double_accord=[r['fragment'] for r in subset if r['attachment']=='sure' and r['double_agreement']]))
    write(out/'audit.json',{'sha256_registre':hashlib.sha256((out/'registre.json').read_bytes()).hexdigest(),
                             'par_cahier':summaries,'montages_indetermines':len(registry['montages_indetermines'])})
    with (out/'registre.csv').open('w',newline='') as f:
        w=csv.writer(f,lineterminator='\n')
        w.writerow(['quire','source_page','fragment','locus','drawing_target','attachment','double_agreement','other_loci','other_targets','prior_tests_this_pair','other_fragments_same_target','ambiguous_montage'])
        for r in rows:
            for locus,page in itertools.product(r['loci'] or [''],r['targets']):
                other_loci=[l for l in r['loci'] if l!=locus]
                other_targets=[p for p in r['targets'] if p!=page]
                tests=[v['kind'] for v in r['prior_tests'] if v['locus']==locus and v['target']==page]
                w.writerow([r['quire'],r['source_page'],r['fragment'],locus,page,r['attachment'],r['double_agreement'],
                            '|'.join(other_loci),'|'.join(other_targets),'|'.join(tests),
                            '|'.join(map(str,r['target_shared_with'].get(page,[]))),''])
        for m in registry['montages_indetermines']:
            for opt in m['alternatives']:
                w.writerow([m['quire'],m['source_page'],opt['fragment'],opt['locus'],m['target'],'montage_indetermine','','','','','',m['montage']])
    return summaries


if __name__=='__main__':
    cli=argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--inputs',type=Path,default=HERE/'sources.json')
    cli.add_argument('--out',type=Path,default=HERE)
    args=cli.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    print(json.dumps(output(build(json.loads(args.inputs.read_text())),args.out), ensure_ascii=False))
