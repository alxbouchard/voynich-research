"""Recaler les boîtes des annonces de f3v et examiner les trois emplacements déposés."""
from hashlib import sha256
import gzip
import json
from pathlib import Path
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ICI = Path(__file__).resolve().parent
ETUDE = ICI.parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ETUDE / '2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import boite, recaler

PAIRES = [(7, 3), (11, 4), (7, 2)]
YALE = 'https://collections.library.yale.edu/iiif/2/1006081/full/full/0/default.jpg'
VISUALISEUR = 'https://www.voynichese.com/2/data/folio/image/glance/color/large/f3v.jpg'
SHA_YALE = 'b9c19a872d6456fa58f76f15dec1d61bc80cc353fceff33f11abdaae87ce199e'


def charge(f):
    return json.loads(gzip.decompress((ICI.parent / f).read_bytes()))


def centre(b):
    return [(b[0]+b[2])/2, (b[1]+b[3])/2]


def police(taille):
    for name in ('/System/Library/Fonts/Supplemental/Arial.ttf','DejaVuSans.ttf'):
        try: return ImageFont.truetype(name,taille)
        except OSError: pass
    return ImageFont.load_default()


def mesurer(cache):
    photo = cache/'1006081.jpg'
    ref = cache/'reference.jpg'
    assert sha256(photo.read_bytes()).hexdigest() == SHA_YALE
    m, qual = recaler(ref, photo)
    carte = charge('CARTE-MASQUEE.json.gz')['f3v']
    avant = charge('PREDICTIONS.json.gz')['pages']['f3v']['paires']
    apres = charge('OUVERTURES.json.gz')['f1-16']
    normale = np.linalg.solve(m[:,:2].T, np.array([1.,carte['pente']]))
    normale /= np.linalg.norm(normale)
    lignes = []
    for numero, rang in PAIRES:
        h, b = f'f3v.{numero}', f'f3v.{numero+1}'
        paire = next(p for p in carte['paires'] if p['haut'] == h)
        annonces = next(p for p in avant if p['haut'] == h)['annonces']
        annonce = next(a for a in annonces if a['rang_haut'] == rang)
        cible = annonce['rang_bas']
        mot_bas = next(a['observe'] for a in apres[b] if a['rang'] == cible)
        haut = boite([0]+paire['boites_haut'][rang-1],m)
        bas = [boite([0]+bb,m) for bb in paire['boites_bas']]
        p,q = map(lambda t: np.array(centre(t)),[haut,bas[cible-1]])
        classe = sorted([(i,round(float(abs((np.array(centre(bb))-p)@normale)),1))
                         for i,bb in enumerate(bas,1)],key=lambda t: t[1])
        horizontal = max(0,min(haut[2],bas[cible-1][2])-max(haut[0],bas[cible-1][0]))
        lignes.append({'haut':h,'rang_haut':rang,'bas':b,'rang_bas':cible,'annoncé':annonce['mot'],
                       'lu':mot_bas,'boîte_haut':haut,'boîte_bas':bas[cible-1],
                       'centre_haut':p.tolist(),'centre_bas':q.tolist(),
                       'dx_natif':q[0]-p[0],'dy_natif':q[1]-p[1],
                       'largeur_intersection_x':horizontal,'classement_redressé':classe})
    return {'Yale':YALE,'sha_Yale':SHA_YALE,'vue_visualiseur':VISUALISEUR,
            'sha_visualiseur':sha256(ref.read_bytes()).hexdigest(),'dépôt_prédictions':'b47dabb',
            'matrice_vers_native':m.tolist(),'axe_projection_dans_photo':normale.tolist(),
            'pente_déposée_visualiseur':carte['pente'], **qual, 'paires':lignes}


def planche(cache, compte):
    im = Image.open(cache/'1006081.jpg').convert('RGB')
    plan = Image.new('RGB',(1266,532),'#faf9f5')
    d = ImageDraw.Draw(plan)
    d.text((18,12),'Deux reprises prédites et leur témoin voisin sur f3v',fill='#242425',font=police(29))
    d.text((18,55),'Les coins colorés situent les deux mots sur la photographie. Les trois extraits conservent la même échelle.',fill='#404040',font=police(18))
    for i,rec in enumerate(compte['paires']):
        x,y = 17+418*i, 152
        boxes = [rec['boîte_haut'],rec['boîte_bas']]
        centers = [centre(t) for t in boxes]
        cx=sum(a for a,_ in centers)/2;cy=sum(a for _,a in centers)/2
        raw = (round(cx-190),round(cy-148),round(cx+190),round(cy+148))
        a = im.crop(raw)
        plan.paste(a,(x,y))
        for b,c in zip(boxes,['#096687','#9f3829']):
            l,t,r,bt = x+b[0]-raw[0], y+b[1]-raw[1], x+b[2]-raw[0], y+b[3]-raw[1]
            for sx,dx in [(l,1),(r,-1)]:
                for sy,dy in [(t,1),(bt,-1)]:
                    d.line([(sx+9*dx,sy),(sx,sy),(sx,sy+9*dy)],fill=c,width=2)
        d.text((x,99),f"{rec['haut']} → {rec['bas']}   ·   rang {rec['rang_haut']}",fill='#222222',font=police(20))
        d.text((x,459),f"Annoncé   {rec['annoncé']}",fill='#096687',font=police(19))
        d.text((x,492),f"Observé   {rec['lu']}",fill='#9f3829',font=police(19))
    plan.save(ICI/'trois-paires.jpg',quality=95,optimize=True)


if __name__ == '__main__':
    photos = Path(sys.argv[1])
    mesures = mesurer(photos)
    (ICI/'REPERES.json').write_text(json.dumps(mesures,indent=2,ensure_ascii=False)+'\n')
    planche(photos,mesures)
