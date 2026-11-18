"""Recaler les boîtes Voynichese v2 sur les JPEG de Yale et vérifier les premiers mots."""
import argparse
from collections import defaultdict
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess
from zipfile import ZipFile
from xml.etree import ElementTree

import cv2
import numpy as np

HERE = Path(__file__).resolve().parent
H_PATH = HERE.parents[2] / 'voynich_20261028/data/IT2a-n.txt'
ARCHIVE_URL = 'https://www.voynichese.com/1/data/folio/voynichese_data.zip'
YALE_IDS = dict(f104r=1006256, f104v=1006257, f105v=1006259, f106v=1006261,
                f107r=1006262, f113v=1006271, f116r=1006276)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fetch(path, url):
    if not path.is_file():
        subprocess.run(['curl', '-fLsS', '--retry', '2', url, '-o', str(path)], check=True)


def transformed(pts, m):
    return np.asarray(pts) @ m[:,:2].T + m[:,2]


def register(ref, full):
    scale = 1050 / full.shape[0]
    small = cv2.resize(full, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    detector = cv2.SIFT_create(nfeatures=12000)
    a, da = detector.detectAndCompute(ref, None)
    b, db = detector.detectAndCompute(small, None)
    matches = cv2.BFMatcher(cv2.NORM_L2).knnMatch(da, db, k=2)
    accepted = [p for p, q in matches if p.distance < .73*q.distance]
    uv = np.float64([a[p.queryIdx].pt for p in accepted])
    xy = np.float64([b[p.trainIdx].pt for p in accepted])
    m, inliers = cv2.estimateAffine2D(uv, xy, method=cv2.RANSAC, ransacReprojThreshold=1.8, maxIters=5000)
    keep = inliers.ravel().astype(bool)
    # OpenCV's resize convention maps pixel centres, with each first centre at 0.
    m[:,2] += (1-scale)*.5
    m /= scale
    xy_native = (xy[keep]+.5)/scale-.5
    err = np.linalg.norm(transformed(uv[keep],m) - xy_native, axis=1)
    assert keep.sum() >= 200 and np.percentile(err,95) < 8
    return m, len(accepted), xy_native, err


def align_words(folio, archive, layout, hpath):
    words = []
    for line in hpath.read_text().splitlines():
        match = re.match(r'<'+folio+r'\.(\d+),[^>]*>\s+(.+)', line)
        if match:
            row = re.sub(r'<[^>]*>', '', match[2].replace('<->','.')).replace('!', '').strip().split('.')
            words.extend((int(match[1]),slot,w) for slot,w in enumerate(row,1) if w)
    with ZipFile(archive) as z:
        xml = list(ElementTree.fromstring(z.read('data/'+folio+'.xml')))
    dic, boxes = json.loads(layout.read_text())
    align = difflib.SequenceMatcher(a=[row[2] for row in words], b=[n.text or '' for n in xml], autojunk=False)
    rows = defaultdict(list)
    for a, b, n in align.get_matching_blocks():
        for k in range(n):
            number, slot, word = words[a+k]
            index = int(xml[b+k].attrib['index'])
            entry = boxes[index]
            assert dic[entry[0]][0] == word
            rows[number].append(dict(slot=slot, mot=word, indice=index, boite_v2=entry[1:5]))
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--photos', type=Path, default=HERE/'cache/yale')
    p.add_argument('--cache', type=Path, default=HERE/'cache')
    p.add_argument('--h', type=Path, default=H_PATH)
    p.add_argument('--sortie', type=Path, default=HERE/'calages.json')
    args = p.parse_args()
    args.cache.mkdir(exist_ok=True,parents=True)
    args.photos.mkdir(exist_ok=True,parents=True)
    archive = args.cache / 'voynichese_data.zip'
    fetch(archive, ARCHIVE_URL)
    pred = json.loads((HERE.parent/'PREDICTIONS.json').read_text())['paires_marge']
    wanted = defaultdict(set)
    for pair in pred:
        for locus in (pair['lieu'],pair['temoin']):
            f, n = locus.split('.')
            wanted[f].update([int(n)-1, int(n), int(n)+1])
    records = {}
    for f, wanted_rows in wanted.items():
        cv2.setRNGSeed(0)
        urls = {'yale':f'https://collections.library.yale.edu/iiif/2/{YALE_IDS[f]}/full/full/0/default.jpg',
                'reference':f'https://www.voynichese.com/2/data/folio/image/glance/color/large/{f}.jpg',
                'layout':f'https://www.voynichese.com/2/data/folio/script/{f}.js'}
        paths = {'yale':args.photos/(f+'.jpg'), 'reference':args.cache/(f+'.jpg'), 'layout':args.cache/(f+'.json')}
        for key, path in paths.items():
            fetch(path, urls[key])
        rows = align_words(f, archive, paths['layout'],args.h)
        ref = cv2.imread(str(paths['reference']),cv2.IMREAD_GRAYSCALE)
        full = cv2.imread(str(paths['yale']),cv2.IMREAD_GRAYSCALE)
        m, matches, xy, err = register(ref, full)
        keep_rows = {}
        for n in sorted(wanted_rows - {0}):
            entries = rows[n][:4]
            assert [e['slot'] for e in entries[:2]] == [1,2],(f,n,entries)
            for e in entries:
                x,y,w,h = e['boite_v2']
                q = transformed([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],m)
                e['quadrilatere_yale'] = q.round(2).tolist()
            first = np.mean(entries[0]['quadrilatere_yale'],axis=0)
            closest = np.argsort(np.linalg.norm(xy-first,axis=1))[:30]
            keep_rows[n] = dict(mots=entries, rayon_30_appuis_px=round(float(np.linalg.norm(xy[closest[-1]]-first)),2),
                                erreur_p95_30_appuis_px=round(float(np.percentile(err[closest],95)),2))
        records[f] = dict(urls=urls,sha256={key:sha(v) for key,v in paths.items()},
                          dimensions_yale=list(full.shape[::-1]),dimensions_reference=list(ref.shape[::-1]),
                          affine_v2_vers_yale=m.tolist(),appariements=matches,appuis=len(err),
                          erreur_mediane_px=round(float(np.median(err)),2),
                          erreur_p95_px=round(float(np.percentile(err,95)),2), lignes=keep_rows)
        print(f,len(err),np.percentile(err,95),flush=True)
    out = dict(archive_xml=dict(url=ARCHIVE_URL,sha256=sha(archive)),transcription_sha256=sha(args.h),folios=records)
    args.sortie.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')


if __name__ == '__main__':
    main()
