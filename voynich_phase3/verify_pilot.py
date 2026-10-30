#!/usr/bin/env python3
"""Validate integrity and scope, not the interpretation of the manuscript."""
from pathlib import Path
import collections,csv,hashlib,json,sys
from PIL import Image
from pypdf import PdfReader
from audit_transcription import possible_tokens
ROOT=Path(__file__).resolve().parent

def read(p):return json.loads((ROOT/p).read_text())
def main():
    sources=read('data/image_sources.json');assert len(sources)==14
    lookup={s['oid']:s for s in sources}
    for s in sources:
        path=ROOT/s['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==s['sha256']
        im=Image.open(path);im.load();assert im.size==(s['width'],s['height'])
    maps=read('data/page_image_map.json');assert len(maps)==12
    for m in maps.values():
        x0,y0,x1,y1=m['page_view_bbox_xyxy'];s=lookup[m['oid']]
        assert 0<=x0<x1<=s['width'] and 0<=y0<y1<=s['height']
    annotations=read('results/image_annotations.json');assert len(annotations)==8
    for a in annotations:
        assert a['status']=='location_reviewed_reading_provisional' and a['meaning']=='UNKNOWN'
        s=lookup[a['oid']]
        for key in ['context_bbox_xyxy','word_bbox_xyxy_approximate']:
            x0,y0,x1,y1=a[key];assert 0<=x0<x1<=s['width'] and 0<=y0<y1<=s['height']
        assert a['oid']==maps[a['locus'].split('.')[0]]['oid']
    rows=read('results/aligned_loci.json');assert len(rows)==384
    assert len(set(r['locus'] for r in rows))==384
    assert collections.Counter(r['status'] for r in rows)=={'accord_diplomatique':164,'accord_apres_normalisation':29,'divergence':188,'absent_ZL':1,'absent_IT':2}
    assert sum(r['image_review']=='anchor_region_only_provisional' for r in rows)==8
    assert sum(any(x in r['flags'] for x in ['illisible','variantes','espace_incertain']) for r in rows)==127
    csvrows=list(csv.DictReader((ROOT/'results/aligned_loci.csv').open()))
    assert csvrows==rows
    pairs=read('results/anchor_robustness.json')
    assert [p['stable_under_tested_segmentations'] for p in pairs]==[False,True,True,True]
    assert 'okols' in possible_tokens('okols,sheey','split')[0]
    assert 'okols' not in possible_tokens('okols,sheey','join')[0]
    assert possible_tokens('o[k:t]ols','split')==[['okols'],['otols']]
    pdf=ROOT/'output/pdf/Voynich_pilote_12_pages_2026-10-28.pdf'
    reader=PdfReader(pdf);assert len(reader.pages)==44
    alltext='\n'.join(p.extract_text() for p in reader.pages)
    assert '127 loci' in alltext and '188' in alltext and 'okolssheey' in alltext
    internal=sum(1 for p in reader.pages for a in p.get('/Annots',[]) if a.get_object().get('/Dest') is not None)
    assert internal>=24
    result={'status':'PASS','source_jpegs_hash_checked':14,'pilot_pages':12,'aligned_loci':384,
        'image_regions_reviewed_provisionally':8,'stable_pairs_under_tested_segmentations':3,
        'conditional_pairs':1,'uncertain_loci':127,'pdf_pages':len(reader.pages),'internal_pdf_links':internal,
        'boundary':'No translation; no independent palaeographic review; other loci imported, not visually certified.'}
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
