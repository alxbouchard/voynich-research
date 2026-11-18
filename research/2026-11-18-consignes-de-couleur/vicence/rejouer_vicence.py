from pathlib import Path
from hashlib import sha256
from PIL import Image, ImageOps
import json
import argparse, subprocess, tempfile
parser=argparse.ArgumentParser(description='Reconstruire les neuf cartes à partir du PDF du journal et de la photographie Herba dittimo.')
parser.add_argument('pdf',type=Path)
parser.add_argument('dittimo',type=Path)
parser.add_argument('sortie',type=Path)
a=parser.parse_args()
meta_sources=[(a.pdf,'786225981e2b7555e7de418aa026f0402b6c2db6e8b3d6244b8595d76091a06a'),(a.dittimo,'968ffa7ee0f6b1a2c4c8d23ac0e85d60485ac04a5aa4ea75dabccdce2deca0fa')]
for file,digest in meta_sources:
    if sha256(file.read_bytes()).hexdigest()!=digest: raise SystemExit(f'Empreinte différente pour {file}')
packet=a.sortie;packet.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    prefix=Path(tmp)/'tuile';subprocess.run(['pdfimages','-png',str(a.pdf),str(prefix)],check=True)
    im4=Image.new('RGB',(255,346),'white')
    for idx,pos in [(479,(0,138)),(480,(190,0)),(481,(0,0))]:
        tile=Image.open(f'{prefix}-{idx:03d}.png').convert('RGB').transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        im4.paste(tile,pos)
im39=Image.open(a.dittimo).resize((255,327),Image.Resampling.LANCZOS)
# (id, source, x,y; all crops 80 x 72 in scale of resized page)
areas=[('B17','4',70,0,'sommet de l’illustration, trois fleurs'),('M53','4',42,52,'feuilles, gauche'),('G42','4',117,52,'feuilles, droite'),('R96','4',47,115,'racines'),('D08','4',126,115,'racine, boucle de la queue et corps du dragon'),('L71','4',160,115,'dragon, extrémité droite'),('E34','39',42,137,'contrôle positif gel'),('K21','39',128,78,'contrôle positif de présence de lettres, gr…'),('H69','39',29,18,'contrôle négatif choisi après inspection, feuilles sans inscription distincte')]
records=[]
for id,src,x,y,region in areas:
 im=im4 if src=='4' else im39; bbox=[x,y,x+80,y+72]; cut=ImageOps.grayscale(im.crop(bbox)); fn=packet/f'{id}.png'; cut.resize((400,360),Image.Resampling.NEAREST).save(fn); records.append({'id':id,'folio':f'{src}r','zone':region,'bbox_xyxy_on_equivalent_page':bbox,'native_card_wh':[80,72],'output_wh':[400,360],'sha256':sha256(fn.read_bytes()).hexdigest()})
