#!/usr/bin/env python3
"""Compare pinned source readings without replacing uncertainty by certainty."""
from pathlib import Path
import collections,csv,hashlib,json,re,sys
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'voynich_20261028';sys.path.insert(0,str(BASE))
from analyse import parse,normalize

def diplomatic(raw):
    # Remove annotations only. Preserve drawing gaps, ligatures, alternatives,
    # doubtful word separators and rare EVA symbols.
    return re.sub(r'<(?![-~]>)[^>]*>','',raw)

def possible_tokens(raw,commas):
    s=diplomatic(raw);variants=[s]
    while any('[' in v for v in variants):
        new=[]
        for v in variants:
            m=re.search(r'\[([^][]*)\]',v)
            if m:new.extend(v[:m.start()]+x+v[m.end():] for x in m[1].split(':'))
            else:new.append(v)
        variants=new
        assert len(variants)<4096
    return [normalize(v,commas=commas) for v in variants]

def main():
    protocol=json.loads((ROOT/'PROTOCOL.json').read_text())
    image_map=json.loads((ROOT/'data/page_image_map.json').read_text()) if (ROOT/'data/page_image_map.json').exists() else {}
    annotation_file=ROOT/'results/image_annotations.json'
    annotations={a['locus']:a for a in json.loads(annotation_file.read_text())} if annotation_file.exists() else {}
    sources={n:parse(n)[0] for n in ('ZL3b-n.txt','IT2a-n.txt')}
    zl={r['locus'].split(',')[0]:r for r in sources['ZL3b-n.txt']}
    it={r['locus'].split(',')[0]:r for r in sources['IT2a-n.txt']}
    allrows=[];pages=[]
    for page in protocol['pages']:
        keys=sorted({k for k,r in zl.items() if r['page']==page}|{k for k,r in it.items() if r['page']==page},key=lambda k:int(k.split('.')[1]))
        rows=[]
        for key in keys:
            a=zl.get(key);b=it.get(key)
            da=diplomatic(a['raw']) if a else '';db=diplomatic(b['raw']) if b else ''
            flags=[]
            for source,x in [('ZL',da),('IT',db)]:
                if '?' in x:flags.append(source+':illisible')
                if '[' in x:flags.append(source+':variantes')
                if ',' in x:flags.append(source+':espace_incertain')
                if '@' in x:flags.append(source+':signe_rare')
            status='absent_ZL' if a is None else 'absent_IT' if b is None else 'accord_diplomatique' if da==db else 'accord_apres_normalisation' if a['tokens']==b['tokens'] else 'divergence'
            rows.append({'page':page,'locus':key,'type_ZL':a['type'] if a else '', 'type_IT':b['type'] if b else '',
                'raw_ZL':a['raw'] if a else '', 'raw_IT':b['raw'] if b else '',
                'diplomatic_ZL':da,'diplomatic_IT':db,'status':status,'flags':';'.join(flags),
                'image_review':'anchor_region_only_provisional' if key in annotations else 'imported_not_reviewed',
                'image_oid':image_map.get(page,{}).get('oid',''),
                'target_bbox_xyxy':json.dumps(annotations[key]['word_bbox_xyxy_approximate']) if key in annotations else '',
                'meaning':'UNKNOWN'})
        counts=dict(collections.Counter(r['status'] for r in rows))
        pages.append({'page':page,'loci_union':len(rows),'loci_ZL':sum(r['page']==page for r in zl.values()),
            'loci_IT':sum(r['page']==page for r in it.values()),'counts':counts,
            'loci_with_review_flags':sum(bool(r['flags']) for r in rows),
            'loci_with_uncertainty':sum(any(t in r['flags'] for t in ['illisible','variantes','espace_incertain']) for r in rows)})
        allrows.extend(rows)
    pairs=[]
    for pair in protocol['anchor_pairs']:
        tests={}
        for source,recs in [('ZL',zl),('IT',it)]:
            tests[source]={}
            for role in ['label','body']:
                raw=recs[pair[role]]['raw']
                tests[source][role]={
                    'raw':raw,'split_uncertain_spaces_all_variants':all(pair['word'] in t for t in possible_tokens(raw,'split')),
                    'join_uncertain_spaces_all_variants':all(pair['word'] in t for t in possible_tokens(raw,'join'))}
        robust=all(x['split_uncertain_spaces_all_variants'] and x['join_uncertain_spaces_all_variants'] for src in tests.values() for x in src.values())
        pairs.append({**pair,'tests':tests,'stable_under_tested_segmentations':robust,'meaning':'UNKNOWN'})
    summary={'pages':pages,'total_loci_union':len(allrows),
        'counts':dict(collections.Counter(r['status'] for r in allrows)),
        'loci_with_review_flags':sum(bool(r['flags']) for r in allrows),
        'loci_with_uncertainty':sum(any(t in r['flags'] for t in ['illisible','variantes','espace_incertain']) for r in allrows),
        'stable_pairs_under_tested_segmentations':sum(p['stable_under_tested_segmentations'] for p in pairs),
        'limitation':'Computational agreement is not palaeographic certainty. Normalisation selects first alternatives and splits uncertain spaces; diplomatic strings retain them.'}
    for n,x in [('aligned_loci.json',allrows),('pilot_summary.json',summary),('anchor_robustness.json',pairs)]:
        (ROOT/'results'/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
    with (ROOT/'results/aligned_loci.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=allrows[0]);w.writeheader();w.writerows(allrows)
    print(json.dumps(summary,ensure_ascii=False,indent=2))
    print(json.dumps([{k:v for k,v in p.items() if k!='tests'} for p in pairs],ensure_ascii=False))

if __name__=='__main__':main()
