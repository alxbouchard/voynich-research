"""Préparer des cartes aveugles à partir de vues entières, masquant les graphies."""
import argparse
import hashlib
import json
from pathlib import Path
import random
import sys
import cv2
import numpy as np
from PIL import Image, ImageDraw

ICI = Path(__file__).resolve().parent
RECHERCHE = ICI.parents[1]
REGISTRE = RECHERCHE / '2026-11-18-ordre-des-noms/panneaux/RANGEES.json'
YALE = RECHERCHE.parent / 'voynich_resources/yale/image_index.json'
sys.dont_write_bytecode = True
sys.path.insert(0,str(RECHERCHE/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler

# Coordonnées en millièmes de la HAUTEUR des JPEG non recadrés. Les panneaux
# dépliés peuvent avoir une largeur dépassant 1 000 dans ce système.
# L'objet qui franchit le pli conserve la partie observable dans sa vue.
CADRES = {
 'f88r':('1037112',(33,22,708,978),[(605,32,675,75)]),
 'f88v':('1006233',(136,9,751,968),[]),
 'f89r1':('1006233',(752,16,1381,969),[]),
 'f89r2':('1006233',(1382,16,2376,974),[]),
 'f89v1':('1006235',(168,24,798,974),[]),
 'f89v2':('1006234',(55,40,1041,975),[(945,33,1006,72)]),
 'f100r':('1006248',(36,17,700,903),[(620,24,677,66)]),
 'f100v':('1006249',(175,19,785,858),[]),
 'f102r1':('1006251',(745,37,1355,922),[(1241,37,1348,66)]),
 'f102r2':('1006251',(1358,55,2093,963),[]),
 'f102v1':('1006253',(90,30,738,952),[(620,900,708,951)]),
 'f102v2':('1006252',(69,80,746,960),[(601,78,717,116)])}

# Contrôle sur les vues natives : certaines boîtes du visualiseur s'arrêtent
# sur le bord ou glissent sur les portions les plus plissées du parchemin.
BORDS = {
 'f89r2':[(1840,143,1956,177),(2135,142,2234,181),
          (2080,345,2186,385),(1941,562,2019,596),(2034,814,2145,855),
          (2200,276,2308,319),(2088,317,2171,343),(2208,448,2300,525),(2190,641,2272,728)],
 'f89v2':[(147,160,207,189),(146,415,208,447),(246,414,279,443),
          (171,283,239,346),(173,570,239,716),(166,708,246,752),(56,237,81,317)],
 'f102r2':[(1815,302,1860,342),(1858,435,1918,516),(1875,542,1930,656)],
 'f102r1':[(879,641,948,671),(1190,796,1280,830)],
 'f100v':[(717,339,778,366),(687,572,773,607)],
 'f102v1':[(641,336,671,480),(656,667,710,778)],
 'f102v2':[(153,290,185,407),(129,574,174,601),(184,626,218,814),(73,213,101,244)],
}
BLE = (213,203,184)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cartes(yale,ref,cartes,calages):
    materiel = json.loads(REGISTRE.read_text())
    cotes = {r['url'].split('/')[5]:r for r in json.loads(YALE.read_text())}
    geometry = json.loads(calages.read_text()) if calages else {}
    cle={}; provenance={}
    for lot,debut in [('A',('f88','f89')),('B',('f100','f102'))]:
        noms=[nom for nom in CADRES if nom.startswith(debut)]
        rng = random.Random(685274 + ord(lot))
        rng.shuffle(noms)
        dossier=ICI/lot
        dossier.mkdir(exist_ok=True)
        for i, nom in enumerate(noms):
            code=f'{lot}{i+1:02}'
            oid,bords,supplements=CADRES[nom]
            supplements=supplements+BORDS.get(nom,[])
            original=yale/(oid+'.jpg'); imgref=ref/(nom+'.jpg'); texte=cartes/(nom+'.json')
            assert sha(original)==cotes[oid]['sha256']
            if nom in geometry:
                m,qual,_ =geometry[nom]; m=np.asarray(m)
            else:
                m,qual=recaler(imgref,original)
            original_pil=Image.open(original).convert('RGB')
            # Cette hauteur restitue les lignes individuelles dans les racines.
            natif=original_pil.height
            largeur=round(original_pil.width*1500/natif)
            img=original_pil.resize((largeur,1500),Image.Resampling.LANCZOS)
            dess=ImageDraw.Draw(img)
            _,items=json.loads(texte.read_text())
            for item in items:
                x,y,w,h=item[1:5]
                if w<=0 or h<=0:
                    continue
                pad=3.8
                corners=[[xx,yy,1] for xx,yy in [(x-pad,y-pad),(x+w+pad,y-pad),(x+w+pad,y+h+pad),(x-pad,y+h+pad)]]
                pts=np.asarray(corners)@m.T*1500/natif
                dess.polygon([tuple(v) for v in pts.tolist()],fill=BLE)
            for rect in supplements:
                dess.rectangle([round(x*1.5) for x in rect],fill=BLE)
            img=img.crop([round(t*1.5) for t in bords])
            img.save(dossier/(code+'.jpg'),quality=89,optimize=True)
            rangees=[r for r in materiel if r['page']==nom]
            cle[code]={'page':nom,'lot':lot,'rangs':[[p['fragment'] for p in r['positions']] for r in rangees]}
            provenance[code]={'oid':oid,'url':cotes[oid]['url'],'sha256_original':cotes[oid]['sha256'],
                'sha256_reference':sha(imgref),'sha256_boites':sha(texte),'matrix':m.tolist(),**qual,
                'cadre_pour_hauteur_1000':bords,'masques_supplementaires':supplements,'sha256_carte':sha(dossier/(code+'.jpg'))}
        notice=['# Lecture visuelle — lot '+lot,'',
           'Classer chaque dessin de gauche à droite dans chaque rangée, de haut en bas. Les pots marquent le plus souvent le début d’un registre ; ne pas les compter. Les rectangles unis masquent des inscriptions ou un repère de page et peuvent recouvrir des détails du dessin.',
           '',
           '- Y si un axe ou une base se divise en exactement deux bras principaux allongés, chacun sur au moins environ la largeur de l’axe à leur départ. Quelques radicelles accessoires peuvent subsister.',
           '- S si une seule racine principale entière est visible, simple ou avec de petites radicelles.',
           '- M si au moins trois bras principaux sont visibles et qu’aucune paire ne domine.',
           '- X si seules les feuilles sont visibles, si la base est tronquée, si l’on voit deux bulbes distincts sans fourche attribuable ou si l’objet, le rang, la position ou les branches restent ambigus.',
           '',
           'Conserver toutes les positions. Si une rangée contient des dessins imbriqués ou peu lisibles, répondre X aux places que vous ne pouvez pas situer. Utiliser uniquement les JPEG de ce lot. Fournir une seule réponse JSON sous la forme {"code":["chaîne du rang 1","chaîne du rang 2"]}. Chaque chaîne contient une lettre par dessin.','',
           '| Code | Nombres de dessins, rangées successives |','|---|---|']
        for code,c in cle.items():
            if c['lot']==lot:notice.append(f"| {code} | "+', '.join(str(len(x)) for x in c['rangs'])+' |')
        (dossier/'CONSIGNE.md').write_text('\n'.join(notice)+'\n')
    (ICI/'CLE.json').write_text(json.dumps(cle,indent=2,ensure_ascii=False)+'\n')
    (ICI/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2,ensure_ascii=False)+'\n')
    assert sum(len(r) for c in cle.values() for r in c['rangs'])==135


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('yale',type=Path);ap.add_argument('references',type=Path);ap.add_argument('boites',type=Path)
    ap.add_argument('--calages',type=Path)
    a=ap.parse_args()
    cv2.setNumThreads(1)
    cartes(a.yale,a.references,a.boites,a.calages)
