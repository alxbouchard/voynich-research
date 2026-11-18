"""Localiser les inscriptions et relire les éditions. Voir LECTURES.md pour les arguments."""
from hashlib import sha256
import json
from math import dist
from pathlib import Path
import re
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MONTHS = json.loads((HERE.parent / 'releve.json').read_text())['observations']
PRIMARY = ('IT2a-n', 'ZL3b-n')
EDITIONS = (*PRIMARY, 'GC2a-n', 'RF1b-e', 'RF1b-er')
SAMPLES = {
    'f72v2': (14, (4200, 2604, 4401, 2737), 195, (3190, 250, 5930, 3290),
              'Couronne extérieure', 'S1.13', '06:30', '72v2.2nd_ring', 15),
    'f72v1': (31, (1294, 1960, 1482, 2114), 210, (140, 250, 2930, 3290),
              'Couronne intérieure', 'S2.9', '06:30', '72v1.4th_ring', 10),
    'f73r': (4, (1650, 621, 1830, 774), 25, (70, 250, 2800, 3270),
             'Au-dessus du cercle', 'S0.4', '01:00', '73r.top', 4),
    'f73v': (2, (1435, 490, 1596, 602), -12, (120, 160, 2920, 3250),
             'Au-dessus du cercle', 'S0.2', '11:45', '73v.top', 2),
}
STRICT = ('f72v2.14', 'f72v2.15', 'f72v1.31', 'f73r.4', 'f73r.7',
          'f73v.2', 'f73v.6', 'f73v.12', 'f73v.18')
FAMILY = {'GC2a-n': ('co89', 'Co89', 'co79', 'Co79'),
          'RF1b-e': ('eody', 'eo@152;y'), 'RF1b-er': ('eody',)}
TEAL = '#006f83'
RED = '#ba4638'


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def center(box):
    return ((box[0] + box[2]) / 2, (box[1] + box[3]) / 2)


def read_labels(path):
    labels = {}
    for line in path.read_text(encoding='latin1').splitlines():
        row = re.match(r'<(f[^.]+\.\d+),[&@]Lz>\s+(.*)', line)
        if row and row[1].split('.')[0] in SAMPLES:
            labels[row[1]] = re.sub(r'<[^>]*>', '', row[2]).strip()
    return labels


def direct_matches(labels, endings):
    # Les virgules incertaines sont testées comme jonctions et comme coupures.
    # Aucune variante interne ambiguë n'est devinée.
    output = {}
    for line_id, text in labels.items():
        matches = []
        for treatment in ('', '.'):
            tokens = text.replace(',', treatment).split('.')
            matches.append({w for w in tokens if re.fullmatch(r'(?:[A-Za-z0-9]|@[0-9]{3};)+',w)
                            and any(w.endswith(t) and w != t for t in endings)})
        overlap = matches[0] & matches[1]
        if overlap:
            output[line_id] = sorted(overlap)
    return output


def font(size):
    for choice in ('DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:
            return ImageFont.truetype(choice,size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def mark(im, source_box, boxes):
    draw = ImageDraw.Draw(im)
    for box, color in boxes:
        rect = [v-source_box[i % 2] for i,v in enumerate(box)]
        draw.rectangle(rect,outline='white',width=16)
        draw.rectangle(rect,outline=color,width=10)


def run(images, editions, claston):
    data = {n:read_labels(editions/(n+'.txt')) for n in EDITIONS}
    assert {len(d) for d in data.values()} == {120}
    oldgc = dict(re.findall(r'^<([^>]+)>([^\r\n]+)',claston.read_text('latin1'),re.M))
    assert all(data[PRIMARY[0]][i]==data[PRIMARY[1]][i] and data[PRIMARY[0]][i].endswith('eody')
               for i in STRICT)
    out = {'editions':{n:{'url':f'https://www.voynich.nu/data/{n}.txt',
                          'sha256':digest(editions/(n+'.txt'))} for n in EDITIONS},
           'v101_original':{'url':'https://www.voynich.nu/data/voyn_101.txt','sha256':digest(claston)},
           'neuf_loci_du_test_principal':{i:{n:data[n][i] for n in EDITIONS} for i in STRICT},
           'lecture_directe_sur_120_loci':{n:direct_matches(data[n], ends) for n,ends in FAMILY.items()},
           'photographies':[]}
    panel = Image.new('RGB',(920,1255),'white')
    drawer = ImageDraw.Draw(panel)
    drawer.text((16,12),'Figures et noms des mois dans quatre panneaux du Voynich',font=font(22),fill='black')
    drawer.text((16,45),'Bleu : inscription voynichienne.  Rouge : nom du mois en lettres latines.',font=font(16),fill='#282828')
    for k,m in enumerate(MONTHS):
        f=m['folio']
        n,box,angle,area,place,old,clock,line,index=SAMPLES[f]
        lid=f'{f}.{n}'
        g_word=oldgc[line].rstrip('=-').split('.')[index-1]
        assert g_word == data['GC2a-n'][lid]
        src=images/(m['oid_yale']+'.jpg')
        assert digest(src)==m['sha256_jpeg']
        x,y,x1,y1=box
        namebox=m['boite_mot']
        assert x1<=namebox[0] or x>=namebox[2] or y1<=namebox[1] or y>=namebox[3]
        yoff=76+k*293
        with Image.open(src) as photo:
            assert list(photo.size)==m['dimensions_natives']
            native=photo.crop(box).convert('RGB')
            native.save(HERE/(lid+'.png'))
            overview=photo.crop(area)
            mark(overview,area,[(box,TEAL),(namebox,RED)])
            overview.thumbnail((265,278),Image.Resampling.LANCZOS)
            panel.paste(overview,(10+(265-overview.width)//2,yoff))
            close=native.resize((2*native.width,2*native.height),Image.Resampling.NEAREST)
            close=close.rotate(angle,Image.Resampling.BICUBIC,expand=True,fillcolor='white')
            close.thumbnail((360,265),Image.Resampling.LANCZOS)
            panel.paste(close,(538+(360-close.width)//2,yoff+(273-close.height)//2))
            if f=='f72v1':
                oct_context_box=(1010,1500,2070,2280)
                oct_context=photo.crop(oct_context_box)
                mark(oct_context,oct_context_box,[(box,TEAL),(namebox,RED)])
                oct_context.thumbnail((850,690),Image.Resampling.LANCZOS)
                oct_context.save(HERE/'balance-contexte.jpg',quality=94,subsampling=0)
        drawer.text((288,yoff+37),f"{m['mois_fr']}   {lid}",font=font(19),fill='black')
        drawer.text((288,yoff+79),place,font=font(16),fill='black')
        drawer.text((288,yoff+108),f"Vers {clock.replace(':',' h ')}",font=font(15),fill='black')
        drawer.text((288,yoff+159),data['ZL3b-n'][lid],font=font(23),fill=TEAL)
        drawer.line((12,yoff+282,905,yoff+282),fill='#d0d0d0',width=1)
        out['photographies'].append({'locus':lid,'oid_yale':m['oid_yale'],
              'source':m['source_url'],'sha256_jpeg':m['sha256_jpeg'],
              'locus_historique':old,'position':place,'horloge_ZL':clock,
              'lecture_v101_original':{'ligne':line,'champ_separe_par_points_base_1':index,'forme':g_word},
              'region_native_xyxy_fin_exclue':list(box),'region_annotation_latine':namebox,
              'distance_centres_arrondie_pixels':round(dist(center(box),center(namebox))),
              'sha256_pixels_RVB':sha256(native.tobytes()).hexdigest(), 'sha256_png':digest(HERE/(lid+'.png')),
              'rotation_antihoraire_planche_degres':angle,
              'url_region':f"https://collections.library.yale.edu/iiif/2/{m['oid_yale']}/{x},{y},{x1-x},{y1-y}/full/0/default.jpg"})
    panel.save(HERE/'quatre-figures.jpg',quality=92,subsampling=0)
    (HERE/'releve.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':
    run(*(Path(p) for p in sys.argv[1:]))
