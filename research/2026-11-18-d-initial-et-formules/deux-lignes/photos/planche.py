"""Repères géométriques et cadrages des six lignes dans les vues natives de Yale."""
from pathlib import Path
import json, re, sys
from hashlib import sha256
from difflib import SequenceMatcher
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[2]
ROOT=RESEARCH.parent
sys.path.insert(0,str(RESEARCH/'2026-11-18-noms-dans-une-phrase/enumeration/verticale'))
from reperer import recaler, boite
CASES={'f108r':20,'f116r':17,'f20r':6,'f31r':2,'f82v':36,'f103v':36}

def sha(p):
    return sha256(p.read_bytes()).hexdigest()

def entries(page,n,cache,index):
    native,ref,layout=[cache/(page+'-'+s) for s in ('n.jpg','r.jpg','l.json')]
    official=index[page[1:]]; assert sha(native)==official['sha256']
    m,reg=recaler(ref,native)
    dic,coords=json.loads(layout.read_bytes());vs=[dic[e[0]][0] for e in coords]
    words=[]; ids=[]; raw={}
    for edition,filename in [('H','IT2a-n.txt'),('ZL','ZL3b-n.txt')]:
        for line in (ROOT/'voynich_20261028/data'/filename).read_text().splitlines():
            a=re.match(r'^<'+page+r'\.(\d+),(.)(..)>\s*(.*)',line)
            if not a or a[2]=='!':continue
            text=a[4].replace('<->','.').replace('<~>','.')
            clean=re.sub(r'<[^>]*>|!','',text).replace(',','').strip('.')
            if int(a[1])==n:raw[edition]=clean
            if edition=='H':
                for j,word in enumerate(clean.split('.')):
                    if not word:continue
                    words.append(word);ids.append((int(a[1]),j+1))
    alignment={b.a+i:b.b+i for b in SequenceMatcher(None,words,vs,autojunk=False).get_matching_blocks() for i in range(b.size)}
    ranks=[i for i,(k,_) in enumerate(ids) if k==n]
    boxed=[]
    for i in ranks:
        if i in alignment:
            j=alignment[i]; boxed.append({'rang':ids[i][1],'mot':words[i],'i_visualiseur':j,'boite':boite(coords[j],m)})
        else:
            boxed.append({'rang':ids[i][1],'mot':words[i],'i_visualiseur':None,'boite':None})
    good=[e['boite'] for e in boxed if e['boite']]
    assert len(good)>=len(ranks)-2
    W,H=Image.open(native).size
    crop=[max(0,min(b[0] for b in good)-90),max(0,min(b[1] for b in good)-20),
          min(W,max(b[2] for b in good)+120),min(H,max(b[3] for b in good)+20)]
    return {'lieu':f'{page}.{n}','transcriptions':raw,'cadre':crop,'groupes':boxed,
            'source':official['url'],'sources_complementaires':[f'https://www.voynichese.com/2/data/folio/image/glance/color/large/{page}.jpg',f'https://www.voynichese.com/2/data/folio/script/{page}.js'],
            'sha256':[sha(x) for x in (native,ref,layout)],'recalage':reg}


def font(n):
    try:return ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc',n)
    except OSError:return ImageFont.truetype('DejaVuSans.ttf',n)

def main(cache):
    index={d['label']:d for d in json.loads((ROOT/'voynich_resources/yale/image_index.json').read_bytes())}
    data={page:entries(page,n,cache,index) for page,n in CASES.items()}
    (HERE/'COORDONNEES.json').write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n')
    for file,pages in [('deux-lignes.jpg',['f108r','f116r']),('deux-plantes.jpg',['f20r','f31r']),('deux-saiin.jpg',['f82v','f103v'])]:
        board=Image.new('RGB',(1760,570),'#f9f6ef'); draw=ImageDraw.Draw(board)
        for j,page in enumerate(pages):
            row=data[page];native=Image.open(cache/(page+'-n.jpg')).convert('RGB'); part=native.crop(row['cadre'])
            y=282*j;draw.text((14,16+y),row['lieu'],font=font(25),fill='#352c23')
            scale=min(1728/part.width,155/part.height)
            part=part.resize((round(part.width*scale),round(part.height*scale)),Image.Resampling.LANCZOS)
            board.paste(part,(14,y+53))
            draw.text((14,212+y),'H    '+row['transcriptions']['H'].replace('.','  '),font=font(22),fill='#352c23')
            draw.text((14,243+y),'ZL  '+row['transcriptions']['ZL'].replace('.','  '),font=font(22),fill='#352c23')
        board.save(HERE/file,quality=93,subsampling=0)
    extra(cache,index,data)

def extra(cache,index,data):
    import numpy as np
    from itertools import groupby
    intervals=[
        ('dain | chey',438,510,1322,1349),
        ('chey | qokeedy',573,660,1329,1353),
        ('qokeedy | chol',791,930,1362,1380),
        ('chol | cheey (discuté)',972,1070,1364,1385),
        ('cheey | dalkar',1100,1240,1369,1394),
        ('dalkar | okedy',1340,1454,1374,1395),
        ('à l’intérieur de cheey',1099,1125,1369,1394)]
    img=Image.open(cache/'f108r-n.jpg').convert('RGB'); gray=np.array(img.convert('L'))
    widths=[]
    for name,x0,x1,y0,y1 in intervals:
        result={}
        for t in [110,125,140]:
            empty=(gray[y0:y1,x0:x1]<t).sum(0)==0
            candidates=[]
            for blank,seq in groupby(enumerate(empty),lambda pair:pair[1]):
                if blank:
                    xs=[x+x0 for x,_ in seq]
                    candidates.append([len(xs),xs[0],xs[-1]])
            result[t]=max(candidates)
        widths.append({'espace':name,'fenetre':[x0,y0,x1,y1],'resultats':result})
    # Mettre les repères hors du tracé. Le cliché haut reste nu.
    focus=(610,1290,1400,1440); small=img.crop(focus).resize((1580,300),Image.Resampling.LANCZOS)
    board=Image.new('RGB',(1580,370),'#f9f6ef');board.paste(small);dr=ImageDraw.Draw(board)
    for i,text in [(2,'avant chol'),(3,'chol | cheey'),(4,'avant dalkar')]:
        _,a,b=widths[i]['resultats'][125]; l=(a-focus[0])*2;r=(b+1-focus[0])*2
        dr.line((l,313,r,313),fill='#934721',width=4)
        dr.text((l,325),text,font=font(22),fill='#352c23')
    board.save(HERE/'blanc-f108r.jpg',quality=94,subsampling=0)
    (HERE/'BLANCS.json').write_text(json.dumps(widths,ensure_ascii=False,indent=1)+'\n')
    originals=Image.open(cache/'f103v-n.jpg')
    crop=(0,2200,1520,2709)
    bbox=originals.crop(crop);board=Image.new('RGB',(bbox.width+125,bbox.height),'#f9f6ef')
    board.paste(bbox);dr=ImageDraw.Draw(board)
    rowdata={}
    for n in range(34,41):
        row=entries('f103v',n,cache,index)
        head=row['groupes'][0];b=head['boite']; y=round((b[1]+b[3])/2)
        rowdata[n]={'premier_mot_H':head['mot'],'boite_premier_mot':b,'centre_approche':y}
        dr.text((1526,y-crop[1]-12),f'f103v.{n}',font=font(17),fill='#352c23')
    board.save(HERE/'etoiles-f103v.jpg',quality=94,subsampling=0)
    geo={'cadre':crop,'lignes':rowdata,'centres_visuels_approches':[[622,2423],[630,2598]]}
    (HERE/'ETOILES.json').write_text(json.dumps(geo,indent=1)+'\n')

if __name__=='__main__':main(Path(sys.argv[1]))
