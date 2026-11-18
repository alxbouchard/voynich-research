"""Créer seize cartes anonymes à partir du choix de feuillets fixé et de l'index Yale."""
import argparse, hashlib, json, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def strip_metadata(jpeg):
    """Supprime les APP/COM facultatifs précédant les coefficients JPEG sans réencodage."""
    assert jpeg[:2] == b'\xff\xd8'
    out = bytearray(jpeg[:2])
    i = 2
    while i < len(jpeg):
        start = i
        assert jpeg[i] == 255
        while jpeg[i] == 255: i += 1
        marker = jpeg[i]
        if marker == 0xda:
            out.extend(jpeg[start:])
            return bytes(out)
        i += 1
        size = int.from_bytes(jpeg[i:i+2],'big')
        assert size >= 2
        end = i + size
        # Les marqueurs standard JFIF et Adobe sans commentaires gardent le modèle colorimétrique.
        if not (0xe0 <= marker <= 0xef or marker == 0xfe) or (marker in (0xe0,0xee) and jpeg[i+2:end].startswith((b'JFIF\x00',b'Adobe'))):
            out.extend(jpeg[start:end])
        i = end
    raise ValueError('Entête JPEG incomplet')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('index',type=Path)
    parser.add_argument('photographies',type=Path)
    parser.add_argument('sortie',type=Path)
    a=parser.parse_args()
    index={'f'+img['label']:img for img in json.loads(a.index.read_text())}
    original_order=[f'f{n}{s}' for n in (75,76,77,78,79,82,83,84) for s in ('r','v')]
    order=original_order.copy()
    seed=202611187516
    random.Random(seed).shuffle(order)
    cards=a.sortie/'cartes'; sheets=a.sortie/'planches'; private=a.sortie/'prive'
    for d in (cards,sheets,private): d.mkdir(exist_ok=True,parents=True)
    manifest={}
    font_files=[Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
    font=next((ImageFont.truetype(str(f),34) for f in font_files if f.exists()),ImageFont.load_default())
    for i,folio in enumerate(order,1):
        code=f'O{i:02d}'; src=a.photographies/(folio+'.jpg'); dst=cards/(code+'.jpg')
        rec=index[folio];assert digest(src)==rec['sha256']
        dst.write_bytes(strip_metadata(src.read_bytes()))
        with Image.open(src) as before, Image.open(dst) as after:
            assert list(after.size)==[rec['width'],rec['height']]
            assert before.convert('RGB').tobytes()==after.convert('RGB').tobytes()
            assert not after.getexif()
        manifest[code]={'face':folio,'source':rec['url'],'sha256_yale':rec['sha256'],'sha256_carte':digest(dst),'dimensions':[rec['width'],rec['height']]}
    inventory={'graine':seed,'faces_admises':original_order,'empreinte_index':digest(a.index),'planches':{}}
    for off in range(0,16,4):
        sheet=Image.new('RGB',(2200,2900),'white')
        drawer=ImageDraw.Draw(sheet);codes=list(manifest)[off:off+4]
        for j,code in enumerate(codes):
            x,y=(j%2)*1100,(j//2)*1450
            with Image.open(cards/(code+'.jpg')) as pic:
                pic.thumbnail((1085,1385),Image.Resampling.LANCZOS)
                sheet.paste(pic,(x+(1100-pic.width)//2,y+55+(1390-pic.height)//2))
            drawer.text((x+550,y+27),code,fill='black',font=font,anchor='mm')
        dest=sheets/f'planche_{1+off//4:02d}.jpg'
        sheet.save(dest,quality=93,subsampling=0)
        inventory['planches'][dest.name]={'codes':codes,'sha256':digest(dest)}
    for name,item in [('correspondance',manifest),('selection',inventory)]:
        (private/(name+'.json')).write_text(json.dumps(item,ensure_ascii=False,indent=2)+'\n')
    print('16 cartes natives, quatre planches, 16 jeux de pixels validés')

if __name__=='__main__': main()
