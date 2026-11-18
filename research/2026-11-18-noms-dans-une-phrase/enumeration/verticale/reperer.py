"""Relier les boîtes du visualiseur aux JPEG de Yale, indépendamment pour les trois vues."""
from pathlib import Path
from hashlib import sha256
from difflib import SequenceMatcher
import json,math,re,sys
import cv2
import numpy as np

ICI=Path(__file__).resolve().parent
DEPOT=ICI.parents[3]
DONNEES=DEPOT/'voynich_20261028/data'
ESSAIS={'f99r':(20,27,25,18,8,'1006246'),
        'f102v1':(2,6,3,21,3,'1006253'),
        'f102v2':(10,16,11,39,2,'1006252')}


def empreinte(p):
    return sha256(p.read_bytes()).hexdigest()


def recaler(reference,yale):
    img=cv2.imread(str(reference),cv2.IMREAD_GRAYSCALE)
    native=cv2.imread(str(yale),cv2.IMREAD_GRAYSCALE)
    rapport=1050/native.shape[0]
    petit=cv2.resize(native,None,fx=rapport,fy=rapport,interpolation=cv2.INTER_AREA)
    sift=cv2.SIFT_create(nfeatures=12000)
    pts0,des0=sift.detectAndCompute(img,None);pts1,des1=sift.detectAndCompute(petit,None)
    matches=cv2.BFMatcher(cv2.NORM_L2).knnMatch(des0,des1,k=2)
    bons=[a for a,b in matches if a.distance<.73*b.distance]
    src=np.asarray([pts0[a.queryIdx].pt for a in bons]);dst=np.asarray([pts1[a.trainIdx].pt for a in bons])
    m,i=cv2.estimateAffine2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=1.8,maxIters=5000)
    utilises=i.ravel().astype(bool)
    assert utilises.sum()>100
    erreurs=np.linalg.norm((src@m[:,:2].T+m[:,2]-dst)[utilises],axis=1)/rapport
    return m/rapport,{'points':int(utilises.sum()),'erreur_p95_pixel':float(np.quantile(erreurs,.95)),
                      'dimensions':[native.shape[1],native.shape[0]]}


def boite(entree,mat):
    x,y,w,h=entree[1:5];pts=np.asarray([[a,b,1] for a in [x,x+w] for b in [y,y+h]])@mat.T
    return [math.floor(pts[:,0].min()),math.floor(pts[:,1].min()),math.ceil(pts[:,0].max()),math.ceil(pts[:,1].max())]


def main(dossier):
    support=json.loads((DEPOT/'voynich_resources/yale/image_index.json').read_text())
    photo={}
    for folio,(lo,hi,vraie,n_prose,slot,oid) in ESSAIS.items():
        jpg=dossier/'yale'/(folio+'.jpg');ref=dossier/'reference'/(folio+'.jpg');js=dossier/'layout'/(folio+'.json')
        officiel=next(v for v in support if '/'+oid+'/' in v['url'])
        assert empreinte(jpg)==officiel['sha256']
        mat,geom=recaler(ref,jpg);dictio,layout=json.loads(js.read_text());mots=[dictio[a[0]][0] for a in layout]
        h=[];indices=[];lignes={}
        for line in (DONNEES/'IT2a-n.txt').read_text().splitlines():
            m=re.match(r'^<'+folio+r'\.(\d+),(.)(..)>\s*(.*)',line)
            if not m or m[2]=='!':continue
            texte=re.sub(r'<[^>]*>|!','',m[4].replace('<->','.').replace('<~>','.')).strip()
            sequence=[j for j in texte.split('.') if j];line_id=int(m[1])
            lignes[line_id]={'type':m[3],'taille':len(sequence),'repere':[]}
            for n,w in enumerate(sequence,1):
                indices.append((line_id,n,w));h.append(w)
        mapp={}
        for b in SequenceMatcher(None,h,mots,autojunk=False).get_matching_blocks():
            for k in range(b.size):mapp[b.a+k]=b.b+k
        # Trois inscriptions dont le dernier signe, ou la lecture, diffère du visualiseur.
        # L'ordre des deux inscriptions encadrantes localise chacune sans inférer son texte.
        lectures_incompletes = {
            9: ('ok??', 10, ['otory', 'ok', 'okody']),
            16: ('tod?', 17, ['olrodar', 'tod', 'podeesho']),
            29: ('e???ddy', 89, ['okockhy', 'eddy', 'pydaeey']),
        }
        for j,(n,r,w) in enumerate(indices):
            k=mapp.get(j)
            if k is None and folio == 'f102v2' and n in lectures_incompletes and r == 1:
                attendu, k, sequence = lectures_incompletes[n]
                assert w == attendu and mots[k-1:k+2] == sequence
            if k is not None:
                lignes[n]['repere'].append({'rang':r,'mot_H':w,'index_carte':k,'boite':boite(layout[k],mat)})
        assert all(len(lignes[n]['repere'])==lignes[n]['taille'] for n in range(lo,hi+1))
        assert any(it['rang']==slot for it in lignes[n_prose]['repere'])
        photo[folio]={'folio':folio,'yale_url':officiel['url'],'yale_sha256':officiel['sha256'],
                      'reference_url':'https://www.voynichese.com/2/data/folio/image/glance/color/large/'+folio+'.jpg',
                      'reference_sha256':empreinte(ref),'carte_url':'https://www.voynichese.com/2/data/folio/script/'+folio+'.js',
                      'carte_sha256':empreinte(js),'matrice_vers_Yale':mat.tolist(),**geom,
                      'rang_prose':slot,'ligne_prose':n_prose,'cible':vraie,'rangee':list(range(lo,hi+1)),
                      'lignes':{n:v for n,v in lignes.items() if v['type'] in ('P0','Lf') or lo<=n<=hi}}
    return photo

if __name__=='__main__':print(json.dumps(main(Path(sys.argv[1])),indent=1,ensure_ascii=False))
