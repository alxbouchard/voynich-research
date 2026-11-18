"""Assembler la vue d’ensemble, les feuilles et les racines sans les cotes ni la prose."""
from pathlib import Path
from hashlib import sha256
import json
import random
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
REG=HERE.parents[2]/'voynich_resources/yale/image_index.json'
INPUT=Path(sys.argv[1])
# Points repérés dans une vue de travail 440 x 570. La silhouette est conservée
# par polygones autour des parties du dessin. Le gris indique un masquage.
parts={
'f93r':{'garde':[[(190,121),(215,103),(239,83),(265,65),(282,80),(303,100),(334,114),(359,126),(375,139),(365,164),(359,169),(379,181),(390,211),(390,388),(375,464),(368,478),(353,468),(357,439),(330,429),(294,421),(281,449),(291,454),(329,459),(352,523),(347,548),(146,550),(150,538),(197,498),(237,479),(261,457),(266,432),(247,421),(219,423),(201,462),(183,432),(180,401),(180,335),(175,243),(180,197),(201,183),(247,173),(193,164),(181,150)]],
'feuille':(179,320,381,448),'base':(139,447,356,551)},
'f93v':{'garde':[[(197,149),(231,149),(242,137),(246,155),(259,159),(273,142),(276,160),(290,147),(291,160),(311,160),(318,155),(325,163),(348,159),(369,136),(373,152),(391,133),(390,152),(405,140),(402,156),(420,172),(405,217),(400,301),(415,344),(414,409),(365,422),(352,452),(400,468),(427,501),(427,555),(111,554),(116,488),(156,460),(218,461),(268,445),(260,401),(196,401),(194,293),(195,228)],[(308,165),(303,128),(304,101),(296,94),(294,69),(300,57),(305,67),(308,94),(314,120),(314,81),(318,62),(316,38),(323,32),(334,33),(337,48),(336,67),(326,80),(320,115),(330,103),(342,80),(348,85),(350,98),(343,108),(331,121),(324,144),(320,170)]],
'feuille':(192,235,309,306),'base':(113,402,429,557)},
'f96r':{'garde':[[(265,170),(260,150),(249,148),(239,132),(242,110),(247,127),(249,98),(265,73),(273,58),(290,47),(329,43),(364,52),(391,68),(399,89),(400,122),(386,143),(349,147),(310,132),(305,111),(292,123),(275,165),(272,243),(299,247),(338,231),(381,248),(405,391),(390,432),(345,422),(292,398),(284,399),(284,430),(300,447),(359,474),(385,499),(404,544),(29,550),(35,512),(62,470),(115,449),(161,447),(224,458),(251,449),(269,430),(269,401),(44,410),(41,328),(55,289),(50,270),(70,244),(92,235),(105,229),(129,237),(140,255),(161,239),(141,233),(139,219),(147,195),(149,211),(163,216),(162,194),(174,198),(167,177),(177,175),(189,195),(189,175),(198,166),(198,191),(215,179),(215,195),(237,180),(234,196),(256,191),(251,217),(231,238),(257,241),(270,244)]],
'feuille':(43,310,148,405),'base':(22,421,412,551)},
'f96v':{'garde':[[(300,466),(287,463),(237,472),(210,495),(184,504),(136,515),(92,527),(64,550),(324,550),(322,481)],[(146,335),(180,316),(179,307),(161,313),(162,296),(180,276),(193,267),(163,271),(154,259),(172,240),(196,226),(205,210),(179,212),(178,196),(194,176),(202,170),(184,165),(180,149),(207,128),(211,139),(221,130),(232,120),(222,148),(213,174),(217,203),(213,222),(215,239),(231,227),(237,232),(232,217),(249,207),(235,203),(232,184),(225,173),(241,167),(238,156),(230,153),(232,133),(244,120),(248,135),(260,147),(258,160),(275,156),(289,162),(281,145),(263,117),(255,103),(233,98),(225,80),(230,66),(256,76),(264,98),(282,123),(280,99),(274,91),(276,64),(284,62),(305,73),(312,91),(302,99),(296,116),(303,124),(313,128),(317,104),(329,101),(327,116),(341,106),(357,106),(372,101),(379,90),(405,85),(402,104),(391,124),(409,126),(429,119),(425,197),(430,338),(429,448),(338,456),(305,437),(311,481),(286,480),(288,401),(149,410)]],
'feuille':(153,222,280,341),'base':(66,450,328,555)}}
originals={r['label']:r for r in json.loads(REG.read_text())}
bg='#d4cebd'
panels=['f93r','f93v','f96r','f96v']
random.Random(11703).shuffle(panels)
dest=HERE/'cartes'
dest.mkdir(exist_ok=True)
key={}
font=ImageFont.load_default(size=22)
for i,face in enumerate(panels,1):
    record=originals[face[1:]]
    path=INPUT/(face+'.jpg')
    assert sha256(path.read_bytes()).hexdigest()==record['sha256']
    im=Image.open(path).convert('RGB')
    w,h=im.size
    def coords(x,y): return round(x*w/440),round(y*h/570)
    def rect(b):return (*coords(*b[:2]),*coords(*b[2:]))
    mask=Image.new('L',im.size)
    for poly in parts[face]['garde']:
        ImageDraw.Draw(mask).polygon([coords(x,y) for x,y in poly],fill=255)
    geom=Image.composite(im,Image.new('RGB',im.size,bg),mask)
    overview=ImageOps.contain(geom.crop(mask.getbbox()),(500,685),Image.Resampling.LANCZOS)
    leaf=ImageOps.contain(im.crop(rect(parts[face]['feuille'])),(465,270),Image.Resampling.LANCZOS)
    base=ImageOps.contain(im.crop(rect(parts[face]['base'])),(465,330),Image.Resampling.LANCZOS)
    board=Image.new('RGB',(1000,735),bg); draw=ImageDraw.Draw(board)
    code=f'J{i}';draw.text((16,8),code,font=font,fill='black')
    board.paste(overview,((510-overview.width)//2,42+(683-overview.height)//2))
    board.paste(leaf,(520+(465-leaf.width)//2,45+(280-leaf.height)//2))
    board.paste(base,(520+(465-base.width)//2,365+(335-base.height)//2))
    board.save(dest/(code+'.jpg'),quality=91)
    key[code]={'face':face,'url':record['url'],'original_sha256':record['sha256']}
    if face=='f93v':
        # Recadrage indépendant du panneau agrandi ; aucune inscription.
        patch=im.crop(rect((211,470,297,547)))
        ImageOps.contain(patch,(450,450),Image.Resampling.LANCZOS).save(dest/'T2.png')
for code,letter in [('T1','B'),('T3','A')]:
    pic=Image.open(HERE.parent/'fragment/cartes'/f'{letter}.png')
    ImageOps.contain(pic,(480,500),Image.Resampling.LANCZOS).save(dest/(code+'.png'))
(HERE/'cle.json').write_text(json.dumps({'plantes':key,'references':{'T3':'A primaire','T1':'B alternative','T2':'f93v même tirage'}},indent=1,ensure_ascii=False)+'\n')
