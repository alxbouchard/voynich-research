"""Reporter les votes déposés et montrer la vraie rangée en conservant les blancs d'origine."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

D=Path(__file__).resolve().parent
PREV=D.parents[1]/'2026-11-18-racines-fourchues'
def load(path):return json.loads(path.read_bytes())
def font(n):
    try:return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
    except OSError:return ImageFont.truetype('DejaVuSans.ttf',n)

def main(native):
    frozen=load(D/'CIBLES.json')
    assert [(row['lieu'],row['communs']) for row in frozen['cibles']]==[('f88r.4',['oldar'])]
    row=next(r for r in load(D.parents[1]/'2026-11-18-ordre-des-noms/panneaux/RANGEES.json')
             if r['page']=='f88r' and r['rang']==1)
    code=next(k for k,v in load(PREV/'images/CLE.json').items() if v['page']==row['page'])
    votes=[load(PREV/'votes'/f'A-{n}.json')[code][0] for n in (1,2)]
    provenance=load(PREV/'images/PROVENANCE.json')[code]
    assert sha256(native.read_bytes()).hexdigest()==provenance['sha256_original']
    entries=[{**p,'votes':[v[i] for v in votes]} for i,p in enumerate(row['positions'])]
    photo=Image.open(native)
    large=(75,70,2685,923); detail=(881,196,1873,826)
    out={'lieu':'f88r.4','fragment_registre':3,'statut':row['niveau'],'code_carte':code,
         'votes_anciens':entries,'cliche':provenance['url'],'sha256':provenance['sha256_original'],
         'cadre_ensemble':large,'cadre_detail':detail,
         'coordonnees_approximatives_oldar_visualiseur':[1352,415,1523,503]}
    (D/'PHOTO-VOTES.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
    board=Image.new('RGB',(1280,988),'#faf8f2')
    draw=ImageDraw.Draw(board)
    draw.text((20,17),'f88r   Où se trouve oldar dans la première rangée ?',font=font(36),fill='#232d26')
    draw.text((20,72),'Les cinq dessins apparaissent à droite du récipient. Vue de Yale, sans masque.',font=font(22),fill='#445649')
    spread=photo.crop(large);spread.thumbnail((1240,410),Image.Resampling.LANCZOS)
    board.paste(spread,(20,120))
    draw.text((20,549),'Les dessins 2, 3 et 4 et leurs légendes',font=font(27),fill='#232d26')
    crop=photo.crop(detail);crop.thumbnail((570,350),Image.Resampling.LANCZOS)
    board.paste(crop,(20,600))
    labels=[(617,'2  ·  orald','Deux bras dominants (Y, Y).'),(717,'3  ·  oldar','Plusieurs bras (M, M).'),(817,'4  ·  otoky','Dessin indécidable (X, X).')]
    for y,title,sub in labels:
        draw.text((618,y),title,font=font(26),fill='#24352a')
        draw.text((618,y+39),sub,font=font(22),fill='#485347')
    draw.text((20,953),'Attributions par ordre des dessins et inscriptions. Les appréciations proviennent des deux votes sur la carte masquée A04.',font=font(17),fill='#485347')
    board.save(D/'oldar-et-voisins.jpg',quality=93,optimize=True)
if __name__=='__main__':main(Path(sys.argv[1]))
