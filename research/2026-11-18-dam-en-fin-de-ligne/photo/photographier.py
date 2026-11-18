"""Caler cinq citations sur la photographie puis extraire les mots et leur voisinage."""
from pathlib import Path
from hashlib import sha256
import json, sys
from PIL import Image, ImageDraw, ImageFont
D=Path(__file__).resolve().parent
sys.path.insert(0,str(D.parents[1]/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite

CASES = [
 ('f43v',1006159,'12',('kedy','dar','chey'),1,False,'Au milieu de la ligne'),
 ('f43r',1006158,'7',('pchdy','kedy','dam'),2,True,'À la fin de la ligne'),
 ('f19r',1006110,'1',('qoky','daiin','dchydy'),1,False,'Modèle intérieur'),
 ('f80v',1006219,'24',('chedy','qoky','daiin'),2,True,'Cible annoncée'),
 ('f55r',1006182,'7',('qotchdy','qokchdy','olkardam'),2,True,'Point de départ'),
]
def font(size):
    try: return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',size)
    except OSError: return ImageFont.truetype('DejaVuSans.ttf',size)

def main(cache):
    plate=Image.new('RGB',(1210, 5*191+100),'#f9f7f0')
    draw=ImageDraw.Draw(plate)
    draw.text((20,17),'Mêmes mots voisins, dernière forme et place dans la ligne',fill='#27332b',font=font(35))
    geom={}
    for j,(page,oid,line,words,idx,end,role) in enumerate(CASES):
        paths=[cache/(page+k) for k in ['-n.jpg','-r.jpg','-l.json']]
        mat,fit=recaler(paths[1],paths[0])
        dic,layout=json.loads(paths[2].read_text());all_words=[dic[e[0]][0] for e in layout]
        starts=[i for i in range(len(all_words)-len(words)+1) if tuple(all_words[i:i+len(words)])==words]
        assert len(starts)==1,(page,starts)
        start=starts[0]; bounds=[boite(layout[start+k],mat) for k in range(len(words))]
        src=Image.open(paths[0]);box=[max(0,min(b[0] for b in bounds)-22),max(0,min(b[1] for b in bounds)-24),
            min(src.width,max(b[2] for b in bounds)+(240 if end else 28)),min(src.height,max(b[3] for b in bounds)+24)]
        # Les boîtes automatiques sont approximatives. La barre extérieure repère exclusivement le mot central.
        piece=src.crop(box);k=min(840/piece.width,129/piece.height)
        piece=piece.resize((round(piece.width*k),round(piece.height*k)),Image.Resampling.LANCZOS)
        y=80+j*191
        draw.text((20,y),f'{page}.{line}   {role}',font=font(24),fill='#23332a')
        draw.text((645,y),'  '.join(words),font=font(24),fill='#323b34')
        plate.paste(piece,(20,y+35)); tar=bounds[idx]
        if page=='f80v':
            # La boîte locale du visualiseur tombe entre les mots. Échelle native du cliché.
            tar=[2424,1912,2530,1948]
        draw.line((20+(tar[0]-box[0])*k,y+37+piece.height,20+(tar[2]-box[0])*k,y+37+piece.height),fill='#9b513a',width=3)
        after=boite(layout[start+len(words)],mat)
        geom[page+'.'+line]={'oid':oid,'yale':f'https://collections.library.yale.edu/iiif/2/{oid}/full/full/0/default.jpg',
          'empreintes_natif_reference_carte':[sha256(p.read_bytes()).hexdigest() for p in paths],
          'reference':f'https://www.voynichese.com/2/data/folio/image/glance/color/large/{page}.jpg',
          'carte':f'https://www.voynichese.com/2/data/folio/script/{page}.js','calage':fit,
          'mots':words,'boites_automatiques':bounds,'cadre_souligne':tar,'cadre':box,'mot_suivant_dans_carte':[all_words[start+len(words)],after]}
    draw.text((20,1033),'Beinecke MS 408  ·  Les barres placées sous les extraits situent le mot comparé.',fill='#49594c',font=font(15))
    plate.save(D/'cinq-passages.jpg',quality=93,optimize=True)
    (D/'COORDONNEES.json').write_text(json.dumps(geom,ensure_ascii=False,indent=1)+'\n')
if __name__=='__main__': main(Path(sys.argv[1]))
