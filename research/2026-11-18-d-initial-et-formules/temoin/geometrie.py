"""Repérer les lignes de type imprimé sans exposer un seul caractère de la réserve."""
from pathlib import Path
import json
import sys
import hashlib
import numpy as np
from PIL import Image, ImageDraw


HERE = Path(__file__).resolve().parent
PAGES = (383,384)

def measure(path, left_page):
    img=Image.open(path).convert('L')
    w,h=img.size
    left,right=(int(.142*w),int(.944*w)) if left_page else (int(.04*w),int(.805*w))
    top,bottom=int(.072*h),int(.902*h)
    ink=np.asarray(img)[top:bottom,left:right]<117
    # La période du texte est proche de 50 pixels dans ces vues de largeur 1450.
    profile=ink.sum(axis=1)
    peaks=[]
    for y in sorted(range(1,len(profile)-1), key=lambda i:-int(profile[i])):
        if profile[y] < 32: break
        if profile[y]>=profile[y-1] and profile[y]>profile[y+1] and all(abs(y-z)>=36 for z in peaks):
            peaks.append(y)
    peaks.sort()
    rows=[]
    for y in peaks:
        indices=np.where(ink[max(0,y-8):y+8].sum(axis=0)>=3)[0]
        if len(indices):
            x0,x1=np.percentile(indices,[1,99])
            rows.append(dict(y=top+int(y),x0=left+int(x0),x1=left+int(x1)))
    return rows

def main(cache):
    board=Image.new('RGB',(840,870),'white')
    draw=ImageDraw.Draw(board)
    data={}
    for column,view in enumerate(PAGES):
        path=cache/f'mgn-par-{view}.jpg'
        rows=measure(path,view%2==1)
        data[str(view)]={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"lignes":rows}
        base=column*420+25
        draw.text((base,6),f'Vue {view}',fill='black')
        for n,r in enumerate(rows,1):
            y=r['y']*.40
            draw.text((base-22,y-6),str(n),fill='black')
            draw.line((base+.25*r['x0'],y,base+.25*r['x1'],y),width=3,fill='#413a37')
    (HERE/'GEOMETRIE.json').write_text(json.dumps(data,indent=1)+'\n')
    board.save(HERE/'positions-masquees.png')
if __name__=='__main__': main(Path(sys.argv[1]))
