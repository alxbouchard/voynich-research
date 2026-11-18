"""Reproduire les détails du Beinecke MS 408 et les silhouettes masquées."""
from hashlib import sha256
from pathlib import Path
import json
import sys
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
CASES={
 'R':{'locus':'f72v3.17','mot':'okaly','oid':'1006204','rotation':-90,
      'sha256':'2552b2eafb7948d182e52ec49e96a5d92a774917924aea594fb1ac3af3bfcdc5',
      'region_native':(990,1320,1620,2740),'contexte_oriente':(221,63,1220,507),
      'corps_oriente':(563,78,923,501),'horloge_ZL':'08:30','rang_Grove':'S1.17',
      'polygone_sur_corps_x2':[(23,342),(122,294),(170,259),(172,202),(190,145),(248,114),
            (309,109),(369,116),(389,142),(405,184),(406,234),(384,264),(344,294),
            (341,319),(358,350),(386,391),(413,380),(436,324),(446,281),(452,232),
            (468,208),(518,200),(541,211),(526,263),(504,302),(475,347),(456,401),
            (434,450),(399,469),(380,455),(378,534),(369,573),(381,605),(401,633),
            (410,688),(420,723),(409,778),(380,793),(322,759),(300,743),(280,786),
            (259,813),(212,811),(193,768),(181,709),(177,648),(161,592),(151,540),
            (135,551),(120,591),(92,611),(55,606),(30,598),(24,563),(26,470),(38,420)]},
 'X':{'locus':'f73v.27','mot':'okal','oid':'1006207','rotation':90,
      'sha256':'4227e5261bb5986e605ddb4f58fa1526640955d778c06916a1c34734bb431141',
      'region_native':(1645,1215,2380,1960),'contexte_oriente':(22,114,736,482),
      'corps_oriente':(302,115,615,501),'horloge_ZL':'02:30','rang_Grove':'S2.4',
      'polygone_sur_corps_x2':[(148,95),(205,61),(254,47),(310,50),(335,89),(334,168),
            (316,214),(292,264),(304,291),(330,338),(332,366),(351,364),(374,317),
            (401,277),(409,242),(419,205),(444,181),(476,175),(485,196),(454,253),
            (446,275),(422,305),(390,334),(367,385),(348,428),(333,469),(338,496),
            (367,526),(385,556),(386,621),(367,631),(322,598),(277,590),(263,615),
            (252,645),(240,660),(175,663),(151,646),(143,604),(122,569),(113,497),
            (134,465),(134,453),(120,457),(102,498),(99,534),(66,545),(27,547),
            (23,531),(32,486),(41,437),(51,399),(82,364),(112,324),(149,294),
            (165,254),(165,225),(149,198),(145,161)]}
}
def run(directory):
    plate=Image.new('RGB',(675,480),'white')
    draw=ImageDraw.Draw(plate)
    try:
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',23)
    except OSError:
        font=ImageFont.load_default(size=23)
    for i,code in enumerate(('X','R')):
        spec=CASES[code]
        path=directory/(spec['oid']+'.jpg')
        assert sha256(path.read_bytes()).hexdigest()==spec['sha256']
        with Image.open(path) as source:
            region=source.crop(spec['region_native'])
            rot=region.transpose(Image.Transpose.ROTATE_90 if spec['rotation']==90 else Image.Transpose.ROTATE_270)
            entire=rot.crop(spec['contexte_oriente'])
            entire.save(HERE/('contexte-'+spec['locus']+'.jpg'),quality=93,subsampling=0)
            body=rot.crop(spec['corps_oriente'])
            mask=Image.new('L',body.size)
            polygon=[(round(x/2),round(y/2)) for x,y in spec['polygone_sur_corps_x2']]
            ImageDraw.Draw(mask).polygon(polygon,fill=255)
            # Masque extérieur seulement, sans retouche des pixels retenus.
            outline=Image.new('RGB',body.size,'white')
            outline.paste(body,mask=mask)
            outline=outline.crop(mask.getbbox())
            pw,ph=outline.size
            factor=min(275/pw,412/ph)
            seen=outline.resize((round(pw*factor),round(ph*factor)),Image.Resampling.LANCZOS)
            plate.paste(seen,(i*335+(335-seen.width)//2,47+(415-seen.height)//2))
            draw.text((i*335+157,10),code,font=font,fill='#111111')
        x,y,x1,y1=spec['region_native']
        spec['url_region_yale']=f"https://collections.library.yale.edu/iiif/2/{spec['oid']}/{x},{y},{x1-x},{y1-y}/full/0/default.jpg"
    plate.save(HERE/'silhouettes.png')
    (HERE/'coordonnees-et-cle.json').write_text(json.dumps(CASES,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':
    run(Path(sys.argv[1]))
