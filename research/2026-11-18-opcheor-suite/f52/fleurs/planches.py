"""Vérifier les six clichés de Yale et montrer les groupes dans leurs pages."""
from hashlib import sha256
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OBS={"f17v": ("ctheol", (400,0,2140,1150)), "f28r":("ctheol",(1310,190,1810,1140)),
     "f96r": ("ctheor",(1650,250,2630,1220)), "f96v":("ctheor",(700,1900,2830,3040))}
CASES={
    "f99r":("f99r.46","tolsasy",94,(605,2435,920,2620),"f99r.29",(470,1480,2390,1700),
             (1297,1538,1479,1632),(622,2447,872,2599),"dsheol  ckhey  ckheol  okeol  ctheol  qokey  ckhol  okeol  okeey  dald"),
    "f100r":("f100r.2","sochorcfhy",116,(710,95,1000,255),"f100r.25",(323,2500,2310,2725),
             (1087,2589,1263,2679),(729,111,981,234),"sheor  qkeeody  chol  daiin  ctheol  olcheol  cheky  cheol  cheockhy  okeol")}
COLORS=("#236f7e", "#9a431f")
PAPER="#fbfaf5"


def font(n):
    for name in ("DejaVuSans.ttf","/System/Library/Fonts/Helvetica.ttc"):
        try:return ImageFont.truetype(name,n)
        except OSError:continue
    return ImageFont.load_default()


def fit(b,im,xy,wh):
    scale=min(wh[0]/im.width,wh[1]/im.height)
    size=tuple(round(n*scale) for n in im.size)
    b.paste(im.resize(size,Image.Resampling.LANCZOS),xy)
    return scale


def box(d,roi,xy,scale,color):
    coord=[round(x*scale+xy[i%2]) for i,x in enumerate(roi)]
    d.rectangle(coord,outline=color,width=3)


def make(cache):
    index={r["label"]:r for r in json.loads((ROOT/"voynich_resources/yale/image_index.json").read_bytes())}
    src={};ims={}
    for p in list(OBS)+list(CASES):
        r=index[p[1:]];f=cache/(p+"-n.jpg");h=sha256(f.read_bytes()).hexdigest()
        assert h==r["sha256"],p
        ims[p]=Image.open(f).convert("RGB")
        src[p]={"url":r["url"],"sha256":h,"taille":ims[p].size}
    anonymous=Image.new("RGB",(1100,890),"white")
    draw=ImageDraw.Draw(anonymous)
    for i,p in enumerate(("f96r","f17v","f96v","f28r")):
        x=i%2*550;y=i//2*445
        patch=ims[p].crop(OBS[p][1]); patch.thumbnail((530,405))
        anonymous.paste(patch,(x+7,y+25)); draw.text((x+9,y+4),chr(65+i),fill="black")
    anonymous.save(HERE/"organes-anonymes.jpg")
    b=Image.new("RGB",(1700,920),PAPER);d=ImageDraw.Draw(b)
    for i,(p,(w,roi)) in enumerate(OBS.items()):
        x=i*425
        d.text((x+8,8),p+"   "+w,font=font(24),fill="#222")
        fit(b,ims[p],(x+8,53),(405,495))
        fit(b,ims[p].crop(roi),(x+8,572),(405,315))
        src[p]["detail"]=roi
    b.save(HERE/"quatre-plantes.jpg",quality=93,subsampling=0)
    b=Image.new("RGB",(1690,1150),PAPER);d=ImageDraw.Draw(b)
    for i,(p,case) in enumerate(CASES.items()):
        y=570*i
        lab,word,num,labroi,loc,lineroi,placed,labbox,line=case
        xy=(12,y+47)
        scale=fit(b,ims[p],xy,(409,510))
        box(d,labbox,xy,scale,COLORS[0]);box(d,placed,xy,scale,COLORS[1])
        d.text((12,y+5),p,font=font(27),fill="#242424")
        d.text((430,y+12),f"{lab}   Fragment {num}",font=font(23),fill=COLORS[0])
        fit(b,ims[p].crop(labroi),(430,y+54),(510,111))
        d.text((430,y+171),word,font=font(21),fill=COLORS[0])
        d.text((430,y+225),loc+"    Ligne du paragraphe",font=font(23),fill=COLORS[1])
        fit(b,ims[p].crop(lineroi),(430,y+264),(1235,175))
        d.text((430,y+437),line,font=font(20),fill="#262626")
        d.text((430,y+475),"Cinquième groupe",font=font(20),fill=COLORS[1])
        roi=[placed[0]-16,placed[1]-12,placed[2]+22,placed[3]+12]
        fit(b,ims[p].crop(roi),(735,y+461),(257,99))
        src[p].update({"legende":lab,"mot":word,"cadre_legende":labbox,"cadre_detail_legende":labroi,
                       "ligne":loc,"cadre_ligne":lineroi,"cadre_ctheol":placed})
    b.save(HERE/"deux-panneaux.jpg",quality=94,subsampling=0)
    (HERE/"SOURCES.json").write_text(json.dumps(src,indent=1,ensure_ascii=False)+"\n")


if __name__=="__main__":make(Path(sys.argv[1]))
