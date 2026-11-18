"""Recréer les cadrages à partir des images Yale exactes de la phase 25."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image,ImageDraw

ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('racine',type=Path,help='racine du dépôt contenant voynich_phase25')
ap.add_argument('sortie',type=Path)
a=ap.parse_args()
data=[
 ('f88r.15','1037112','a1d21ccad0df430b47f3b3df2829bbefb8c4d1644cb70310e6d1de4b01c20013',(850,1180,1850,1840),(1325,1235,1470,1335)),
 ('f89r2.10','1006233','3b553c70d0c068cb39a276d391127165c5d9d868ec08e7f5eb2e73b32bb95d1e',(5250,1230,7390,1780),(6325,1227,6670,1333)),
 ('f101v.10','1006250','1122f1b13afdf1509402334816f95e5e9baa2b6c94aa9e347b04aa2e4e54f36b',(575,690,1430,1450),(850,820,985,955))
]
manifest={}
for locus,photo,sha,box,label in data:
 src=a.racine/'voynich_phase25/sources/images'/(photo+'.jpg')
 assert hashlib.sha256(src.read_bytes()).hexdigest()==sha
 im=Image.open(src).convert('RGB')
 manifest[locus]={'source':'https://collections.library.yale.edu/iiif/2/'+photo+'/full/full/0/default.jpg','sha256':sha,'dimensions':im.size,'detail':box,'cartouche_approximatif':label}
 crop=im.crop(box);crop.thumbnail((1800,850));crop.save(a.sortie/(locus+'-detail.jpg'),quality=96)
 # Montrer le lieu sur le feuillet, sans aucune modification du détail ci-dessus.
 ctx=im.copy()
 draw=ImageDraw.Draw(ctx);draw.rectangle(box,outline='#bb2450',width=10)
 ctx.thumbnail((1650,1110));ctx.save(a.sortie/(locus+'-contexte.jpg'),quality=92)
 im.crop(label).save(a.sortie/(locus+'-signes.jpg'),quality=96)
(a.sortie/'SOURCES.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
