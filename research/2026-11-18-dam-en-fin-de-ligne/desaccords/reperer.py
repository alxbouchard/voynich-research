from pathlib import Path
import json
import re
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from corpus_dam import MODES, corpus, metadata, parse, positions, split_word


def parts(word):
    if word.endswith("?") and word.count("?")==1:
        base=word[:-1]
        if re.fullmatch("[a-z]+da",base):
            return base,"?"
    return split_word(word)


def order(row):
    m=re.fullmatch(r"f(\d+)([rv])(\d*)\.(\d+)",row["locus"])
    return (int(m[1]),m[2],int(m[3] or 0),int(m[4]),row["troncon"],row["rang"])


def main():
    editions,_=corpus()
    meta=metadata()
    records=[]
    for loc,(page,kind,_,_) in editions["H"].items():
        if kind!="P0" or loc not in editions["ZL"] or editions["ZL"][loc][1]!=kind:
            continue
        views=[parse(editions[ed][loc][3],cut) for ed,cut in MODES]
        if not all(v[0]==views[0][0] for v in views):
            continue
        for bi,blocks in enumerate(zip(*(v[1] for v in views))):
            if len(set(map(len,blocks)))!=1:
                continue
            for idx,words in enumerate(zip(*blocks)):
                a,b,c,d=words
                if a!=b or c!=d or a==c:
                    continue
                h,z=parts(a),parts(c)
                if not h or not z or h[0]!=z[0] or h[0]=="da" or h[1]==z[1]:
                    continue
                roles=positions(bi,len(views[0][1]),idx,len(blocks[0]))
                records.append(dict(locus=loc,troncon=bi+1,rang=idx+1,base=h[0],
                                    H=a,ZL=c,positions=sorted(roles),
                                    dernier_cahier=meta.get(page,{}).get("Q")=="T",
                                    pred=h[0]+("m" if "fin" in roles else "r"),
                                    incertain="?" in (h[1],z[1])))
    records.sort(key=order)
    selected={}
    for target in ("fin","interieur"):
        available=[x for x in records if target in x["positions"] and not x["incertain"]]
        options=[x for x in available if x["dernier_cahier"]] or available
        selected[target]=next(iter(options),None)
    (HERE/"LIEUX.json").write_text(json.dumps(dict(candidats=records,selection=selected),ensure_ascii=False,indent=1)+"\n")
    print(len(records),selected)


if __name__=="__main__":
    main()
