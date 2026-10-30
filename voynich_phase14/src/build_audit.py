"""Save exact native-pixel crops and a non-blind visual audit ledger."""
from pathlib import Path
import hashlib,json
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
ROWS=[
('f88r.2','1037112',(850,300,1120,550),'Désaccord osal / oral. Le signe médian reste ouvert à deux lectures; aucune résolution imposée.'),
('f88r.6','1037112',(2030,340,2330,560),'otaly est placé près d’un fragment végétal. Le nom de la plante et la relation sémantique restent inconnus.'),
('f88r.15','1037112',(1280,1180,1550,1440),'okol est dans la rangée de fragments végétaux, près d’une feuille et d’une tige courbée. Il n’est pas inscrit sur le récipient de gauche.'),
('f99r.4','1006246',(860,130,1130,360),'oky entre deux fragments de la première rangée; rattachement exact au dessin non démontré.'),
('f99r.24','1006246',(1390,1040,1590,1240),'Deuxième oky sur cette page, près d’une longue racine courbe. Identité graphique compatible avec les deux translittérations.'),
('f99r.11','1006246',(610,440,920,650),'okary entre des fragments végétaux de la première zone. Pas d’identification botanique retenue.'),
('f99r.25','1006246',(1700,1070,1990,1310),'okeoly près de la grande racine courbe; le dessin voisin ne constitue pas une traduction.'),
('f82v.2','1006223',(1160,180,1390,340),'otedy à gauche d’une figure de la zone supérieure. Contexte spatial observé, fonction grammaticale inconnue.'),
('f82v.44','1006223',(1750,2380,2360,3020),'okol à gauche d’une figure située au bord d’un bassin vert. Texte supérieur inclus pour conserver le contexte.'),
('f73v.1','1006207',(900,420,1460,900),'Lecture publiée okol entre des figures du diagramme zodiacal. Traits très pâles: alignement approximatif compatible, lecture autonome non assurée.'),
('f99r.1','1006246',(80,60,780,480),'Inscription effectivement située sur la surface supérieure d’un récipient. ZL okaradag, IT okoramog; désaccord maintenu.'),
('f88r.24','1037112',(690,2290,1000,2480),'ZL otor,am contre IT otor.am. Une séparation graphique est visible; son statut de frontière de mot reste indéterminé.'),
('f99r.2','1006246',(380,110,660,260),'ZL okar,y contre IT okary. Le statut du petit intervalle avant le dernier signe reste indéterminé.'),
('f88r.19','1037112',(380,1810,2540,2300),'Paragraphe f88r.18-22: okol se retrouve dans la deuxième ligne (f88r.19). Cooccurrence locale, sens non établi.'),
('f99r.18','1006246',(250,790,2580,1160),'Paragraphe f99r.15-18: okeoly figure dans la quatrième ligne (f99r.18), avant la rangée contenant l’étiquette f99r.25.'),
('f116v.margin','1006277',(200,50,2500,1000),'Écriture marginale, croix et figures visibles. Aucune nouvelle transcription ni langue assignée; date, main et rapport au texte principal non établis ici.'),
]

def main():
 parsed=json.loads((ROOT/'results/parsed_loci.json').read_text())
 maps={k:{r['locus']:r for r in rows} for k,rows in parsed.items()}
 sources={r['oid']:r for r in json.loads((ROOT/'data/image_sources.json').read_text())}
 (ROOT/'audit').mkdir(exist_ok=True)
 ledger=[]
 for locus,oid,box,note in ROWS:
  im=Image.open(ROOT/'images'/f'{oid}.jpg'); crop=im.crop(box)
  path=ROOT/'audit'/f'{locus.replace(".","_")}.png';crop.save(path)
  # Pixel identity is checked after PNG encoding and decoding.
  assert Image.open(path).tobytes()==crop.tobytes()
  ledger.append(dict(locus=locus,oid=oid,bbox_xyxy=list(box),path=str(path.relative_to(ROOT)),
    sha256=hashlib.sha256(path.read_bytes()).hexdigest(),source_sha256=sources[oid]['sha256'],
    url=sources[oid]['url'],variants={k:{key:maps[k][locus][key] for key in ['kind','raw','clean']}
     for k in maps if locus in maps[k]},note=note,
    status='non-blind visual alignment; not an independent palaeographic adjudication'))
 (ROOT/'results/image_audit.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2))
 print(f'{len(ledger)} exact crops; source-pixel identity verified')

if __name__=='__main__':main()
