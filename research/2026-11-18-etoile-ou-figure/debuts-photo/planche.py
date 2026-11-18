"""Reproduire les deux planches à partir des fichiers originaux indiqués dans le registre."""
from pathlib import Path
from hashlib import sha256
from difflib import SequenceMatcher
import json,re,sys
from PIL import Image, ImageDraw, ImageFont
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite

CASES=[('f84r',12),('f43r',9),('f43v',13),('f105v',3),('f106r',44),('f115r',16),('f116r',35)]
def sha(p):
    return sha256(p.read_bytes()).hexdigest()

def norm(word):
    return re.sub('<[^>]*>|!','',word.replace('<->','.').replace('<~>','.')).replace(',','').strip()

def fonts(n):
    try:return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
    except OSError:return ImageFont.truetype('DejaVuSans.ttf',n)

def place(im,element,xy,maximum):
    factor=min(maximum[0]/element.width,maximum[1]/element.height)
    im.paste(element.resize((round(factor*element.width),round(factor*element.height)),Image.Resampling.LANCZOS),xy)
    return factor

def coords(cache):
    index={v['label']:v for v in json.loads((ROOT/'voynich_resources/yale/image_index.json').read_text())}
    sources={k:(ROOT/'voynich_20261028/data'/name).read_text().splitlines()
             for k,name in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]}
    texts=sources['H']
    out=[]
    for page,n in CASES:
        nat,ref,js=[cache/(page+'-'+s) for s in ('n.jpg','r.jpg','l.json')]
        info=index[page[1:]]
        assert sha(nat)==info['sha256']
        mat,fit=recaler(ref,nat)
        dic,layout=json.loads(js.read_text())
        vs=[dic[v[0]][0] for v in layout]
        ranks=[]; words=[]
        for line in texts:
            m=re.match(r'^<'+page+r'\.(\d+),(.)(..)>\s*(.*)',line)
            if not m or m[2]=='!':continue
            for k,word in enumerate([w for w in norm(m[4]).split('.') if w],1):
                ranks.append((int(m[1]),k));words.append(word)
        mapped={b.a+i:b.b+i for b in SequenceMatcher(None,words,vs,autojunk=False).get_matching_blocks() for i in range(b.size)}
        ids=[i for i,r in enumerate(ranks) if r[0]==n]
        selected=ids[:3]
        assert all(i in mapped and vs[mapped[i]]==words[i] for i in selected)
        boxes=[boite(layout[mapped[i]],mat) for i in selected]
        im=Image.open(nat)
        l,r=boxes[0],boxes[-1]
        if page=='f84r':
            crop=(max(0,l[0]-215),max(0,l[1]-191),min(im.width,l[2]+225),min(im.height,l[3]+267))
        else:
            crop=(0,max(0,min(b[1] for b in boxes)-50),min(im.width,r[2]+66),min(im.height,max(b[3] for b in boxes)+40))
        glyph=(max(0,l[0]-12),max(0,l[1]-15),min(im.width,l[2]+16),min(im.height,l[3]+15))
        lectures={}
        for ed,lines in sources.items():
            exact=next(line for line in lines if line.startswith(f'<{page}.{n},'))
            prev=next(line for line in lines if line.startswith(f'<{page}.{n-1},'))
            head,body=exact.split('>',1)
            first=norm(body).split('.')[:len(selected)]
            assert first==[words[i] for i in selected]
            lectures[ed]={'type':head[-2:],'premiers_mots':first,'ouverture_paragraphe':'<%>' in body,
                          'fin_paragraphe':'<$>' in body,'fin_paragraphe_precedent':'<$>' in prev}
        out.append(dict(lectures=lectures,lieu=f'{page}.{n}',page=page,natif=info['url'],sha256=[sha(q) for q in (nat,ref,js)],
                    urls_reference_carte=[f'https://www.voynichese.com/2/data/folio/image/glance/color/large/{page}.jpg',f'https://www.voynichese.com/2/data/folio/script/{page}.js'],
                    calage=fit,rangs_visualiseur=[mapped[i] for i in selected],mots=[words[i] for i in selected],
                    boites=boxes,cadre_contexte=crop,cadre_mot=glyph))
    return out

def build(cache):
    data=coords(cache)
    (HERE/'COORDONNEES.json').write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
    for label,rows in [('legende',data[:1]),('prose',data[1:])]:
        if label=='legende':
            row=rows[0];p=Image.open(cache/(row['page']+'-n.jpg'))
            p.crop(row['cadre_contexte']).save(HERE/'f84r-legende.jpg',quality=95)
            continue
        img=Image.new('RGB',(1450,207*len(rows)+42),'#f8f7f2'); dr=ImageDraw.Draw(img)
        dr.text((18,9),'Vue depuis le bord gauche du cliché',font=fonts(20),fill='#29342e')
        dr.text((1080,9),'Premier groupe, agrandi',font=fonts(20),fill='#29342e')
        for i,row in enumerate(rows):
            src=Image.open(cache/(row['page']+'-n.jpg'))
            y=43+i*207;title=row['lieu']+'   '+ '  '.join(row['mots'])
            dr.text((20,y),title,font=fonts(25),fill='#19241e')
            bbox=row['cadre_contexte']; off=(20,y+40)
            k=place(img,src.crop(bbox),off,(1030,148))
            a,b,c,d=row['boites'][0]; base=off[1]+round((d-bbox[1])*k)+6
            dr.line((off[0]+round((a-bbox[0])*k),base,off[0]+round((c-bbox[0])*k),base),fill='#9c5539',width=3)
            place(img,src.crop(row['cadre_mot']),(1080,y+29),(345,145))
        img.save(HERE/'six-debuts.jpg',quality=94)

if __name__=='__main__':build(Path(sys.argv[1]))
