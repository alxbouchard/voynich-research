"""Comparer la zone claire au niveau du corps des lettres, sur les six jonctions identifiées."""
import json
from pathlib import Path
import sys
from hashlib import sha256
from PIL import Image
from extraire import CASES
HERE=Path(__file__).resolve().parent

def main(paths):
    ref={r['label']:r['sha256'] for r in json.loads((HERE.parents[3]/'voynich_resources/yale/image_index.json').read_bytes())}
    images={}
    for face,path in zip(('f84r','f43v'),paths):
        assert sha256(path.read_bytes()).hexdigest()==ref[face[1:]]
        images[face]=Image.open(path).convert('L')
    result={}
    for code,(face,_,x,y,_,_) in CASES.items():
        img=images[face];widths={}
        for t in (105,125,145):
            inds={j for j in range(-40,41) if all(img.getpixel((x+j,y+dy))>=t for dy in range(0,17))}
            # Le blanc qui touche la verticale indiquée, ou la colonne claire la plus proche à +/- 4 px.
            near=[n for n in inds if abs(n)<=4]
            if not near:widths[t]=0;continue
            k=min(near,key=lambda n:(abs(n),n));a=b=k
            while a-1 in inds:a-=1
            while b+1 in inds:b+=1
            widths[t]=b-a+1
        result[code]=widths
    (HERE/'LARGEURS.json').write_text(json.dumps(result,sort_keys=True,indent=1)+'\n')
    print(result)
if __name__=='__main__': main(list(map(Path,sys.argv[1:])))
