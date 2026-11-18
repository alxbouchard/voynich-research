"""Extraire les finales à la main sur les originaux, sans tenter de les classer."""
from pathlib import Path
from hashlib import sha256
import json,sys
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent
T=D/'cartes'
# locus, mot des deux éditions, identifiant visible, fenêtre de travail native, cadre de finale relatif.
F={
 'A':('f112r','1006268',[
 ('37/7','keedas','keedar','J4',(1426,2372),(189,37,234,91)),
 ('37/8','otear','otear','r',(1634,2369),(179,38,211,87)),
 ('13','ches','ches','s',(646,948),(123,22,174,68)),
 ('39/9','ogom','ogom','m',(1892,2477),(151,21,193,94)),
 ('39/2','qopal','qopal','l',(571,2583),(192,51,224,94)),
 ('38/1','sar','sar','J2',(283,2500),(134,29,173,82)),
 ('33','shdal','shdal','J6',(1496,2138),(186,31,216,78))]),
 'B':('f67r1','1006194',[
 ('2/9','keeodal','keeoda[l:?]','J1',(1924,468),(195,31,276,99)),
 ('2/4','sar','sar','r',(1050,474),(122,33,158,81)),
 ('3','shees','shees','s',(1600,536),(181,30,229,81)),
 ('3','dam','dam','m',(2037,557),(126,23,182,116)),
 ('6/2','al','al','l',(1285,834),(77,32,116,74)),
 ('4','dair','dair','J5',(1610,619),(151,27,197,83)),
 ('3/2','s','s','J3',(560,566),(45,25,92,78))])}
def font(n):
    try:return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
    except OSError:return ImageFont.truetype('DejaVuSans.ttf',n)

def main(cache):
    sources={};entries={};tiles={}
    dat=json.loads((D.parents[2]/'voynich_resources/yale/image_index.json').read_bytes()) if (D.parents[2]/'voynich_resources/yale/image_index.json').exists() else []
    for setid,(page,oid,rows) in F.items():
        jpg=cache/(page+'-n.jpg');im=Image.open(jpg).convert('RGB')
        digest=sha256(jpg.read_bytes()).hexdigest()
        official=[s['sha256'] for s in dat if '/'+oid+'/' in s['url']]
        if official: assert digest==official[0]
        sources[setid]={'page':page,'oid':oid,'dimensions':im.size,'sha256':digest,
                         'url':f'https://collections.library.yale.edu/iiif/2/{oid}/full/full/0/default.jpg'}
        for loc,h,z,code,origin,rel in rows:
            box=tuple(v+origin[i%2] for i,v in enumerate(rel))
            entries[setid+'-'+code]={'lieu':page+'.'+loc,'H':h,'ZL':z,'cadre_natif':box,'code':code,
                'type':'référence' if len(code)==1 else ('cible' if h!=z else 'témoin')}
            crop=im.crop(box)
            if setid=='B' and code=='J1':
                # Préserver le trait oblique inférieur qui passe sous le signe précédent.
                # Masquer les traits du voisin au-dessus de cette diagonale.
                poly=[(0,0),(36,0),(36,35),(28,44),(16,49),(0,55)]
                mask=Image.new('L',crop.size,0)
                ImageDraw.Draw(mask).polygon(poly,fill=255)
                blank=(2212,498,2212+crop.width,498+crop.height)
                crop.paste(im.crop(blank),mask=mask)
                entries[setid+'-'+code]['fond_parchemin_natif']=blank
                entries[setid+'-'+code]['masque_voisin_relatif']=poly
            tiles[setid,code]=crop.resize(tuple(round(v*1.7) for v in crop.size),Image.Resampling.LANCZOS)
    plate=Image.new('RGB',(1056,930),'#f4f2ea');d=ImageDraw.Draw(plate)
    for j,setid in enumerate(('A','B')):
        y=12+j*455
        d.text((18,y),'Série '+setid,font=font(30),fill='#263c37')
        for k,(title,codes) in enumerate([('Références',['r','s','l','m']),
                    ('À lire',sorted(code for (group,code) in tiles if group==setid and len(code)>1))]):
            ry=y+64+k*198;d.text((18,ry+38),title,font=font(22),fill='#31433c')
            for n,code in enumerate(codes):
                cx=247+n*218
                d.text((cx-11,ry),code,font=font(23),fill='#283b32')
                crop=tiles[setid,code];plate.paste(crop,(cx-crop.width//2,ry+99-crop.height//2))
    plate.save(T/'SIGNES.jpg',quality=96,optimize=True)
    (D/'CLE.json').write_text(json.dumps({'sources':sources,'cartes':entries},ensure_ascii=False,indent=1)+'\n')
if __name__=='__main__':main(Path(sys.argv[1]))
