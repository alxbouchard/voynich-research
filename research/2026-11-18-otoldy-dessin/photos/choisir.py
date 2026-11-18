"""Associer les témoins à partir des transcriptions et métadonnées IVTFF."""
from pathlib import Path
from hashlib import sha256
import json, re

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[2]/'voynich_20261028/data'
META = re.compile(r'^<(f\d+[rv]\d*)>\s*<!([^>]*)>')
LINE = re.compile(r'^<((f\d+[rv]\d*)\.\d+),.P\w>\s*(.+)')
WORD = 'otoldy'


def folio(page):
    return int(re.match(r'f(\d+)',page)[1])


def parse(path):
    pages, present = {}, {}
    for line in path.read_text().splitlines():
        header = META.match(line)
        if header:
            metadata = dict(re.findall(r'\$(\w)=(\w+)', header[2]))
            if metadata.get('I') == 'H':
                pages[header[1]] = metadata
        record = LINE.match(line)
        if record and record[2] in pages:
            raw = re.sub(r'<![^>]*>|<[%$]>','',record[3]).replace('<->','.').replace('!','')
            for split in ('séparés','joints'):
                words = raw.replace(',', '.' if split=='séparés' else '').split('.')
                if WORD in words:
                    present.setdefault(record[2],{}).setdefault(split,[]).append(record[1])
    return pages, present


def main():
    paths = {'H':DATA/'IT2a-n.txt', 'ZL':DATA/'ZL3b-n.txt'}
    ed = {name:parse(file) for name,file in paths.items()}
    meta, h = ed['H']; other, z = ed['ZL']
    assert meta == other
    targets = sorted((p for p in h.keys() & z.keys()
                      if all(h[p].get(s) and z[p].get(s) for s in ('séparés','joints'))), key=folio)
    assert targets==['f22r','f28r','f44v','f48v','f53v']
    occupied = {folio(p) for p in targets}
    rows = []
    for p in targets:
        m = meta[p]
        eligible = [q for q,n in meta.items() if re.search('[rv]',q)[0]==re.search('[rv]',p)[0] and folio(q) not in occupied
                    and q not in h and q not in z and all(n.get(k)==m.get(k) for k in ('Q','L','H','I'))]
        # Favour a different conjugate sheet if one is available, then nearest leaf.
        # If two are equally near, use the lower folio number.
        ordered = sorted(eligible,key=lambda q:(meta[q]['B']==m['B'],abs(folio(q)-folio(p)),folio(q)))
        q = ordered[0] if ordered else None
        if q: occupied.add(folio(q))
        rows.append({'cible':p, 'lieux':{'H':h[p],'ZL':z[p]},'meta_cible':m,'témoin':q,
                     'meta_témoin':meta[q] if q else None,
                     'admissibles_en_ordre':ordered})
    result = {'fichiers_sha256':{k:sha256(v.read_bytes()).hexdigest() for k,v in paths.items()},
              'faces_avec_forme':{'H':h,'ZL':z},'paires':rows}
    (HERE/'ECHANTILLON.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
