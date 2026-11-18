"""Prédictions à distance dans les deux lignes déjà appariées à Celse."""
from pathlib import Path
import sys
from collections import defaultdict
from dictionnaire import HERE,EVA,load,save
from corpus_sources import celsus
from croiser import texts

SITES=("f18v.7","f23r.7")


def manuscript():
    pages=texts("plantes",True)
    out=[]
    for site in SITES:
        line=[r for r in pages[site.split(".")[0]] if r[1]==site]
        assert [r[3][0] for r in line]==list(range(1,1+len(line))) and len({r[2] for r in line})==1
        assert all(len(set(r[3]))==1 for r in line)
        out.append([r[0] for r in line])
    assert out[1][9]=="daiin"
    return out


def locate(historical,paragraphs,place,i):
    if paragraphs is None:return place,i,historical[place]
    prefix=place.rsplit(".",1)[0]+"."
    target=historical[place]
    matches=[]
    for segment,ws in paragraphs.items():
        if not segment.startswith(prefix):continue
        for j in range(len(ws)-len(target)+1):
            if ws[j:j+len(target)]==target:matches.append((segment,i+j,ws))
    if len(matches)==1:return matches[0]
    return None


def compare(lines,r,strict,wide):
    grid=[]
    for site,ws,(where,rank) in zip(SITES,lines,r["lieux"]):
        match=locate(strict,wide,where,rank-1)
        row=[]
        for i,token in enumerate(ws):
            word=None
            if match is not None:
                k=match[1]+i-3
                if 0<=k<len(match[2]):word=match[2][k]
            row.append({"site":site,"rang":i+1,"signe":token,"texte":word})
        grid.append(row)
    seed=dict(zip(EVA,r["mots"]))
    perdir={}
    for order in ((0,1),(1,0)):
        lookup=dict(seed)
        reverse={v:k for k,v in seed.items()}
        exact=[];mismatches=[];duplicates=[];predictions=[];added=[]
        for line_index in order:
            for point in grid[line_index]:
                symbol,plain=point["signe"],point["texte"]
                if plain is None or point["rang"] in (4,5,6):continue
                if symbol in lookup:
                    pred={**point,"annonce":lookup[symbol]}
                    predictions.append(pred)
                    (exact if lookup[symbol]==plain else mismatches).append(pred)
                else:
                    lookup[symbol]=plain;added.append(point)
                if plain in reverse and reverse[plain]!=symbol:
                    duplicates.append({**point,"autre_signe":reverse[plain]})
                else:reverse[plain]=symbol
        perdir[SITES[order[0]]]=dict(exacts=exact,contradictions=mismatches,homophones=duplicates,prevus=predictions,etendus=added)
    return dict(mots=r["mots"],lieux=r["lieux"],alignement=grid,retour_daiin=grid[1][9],directions=perdir)


def main(path):
    lines=manuscript()
    strict=celsus(path,r"[.;:!?]");wide=celsus(path)
    cases=load(HERE/"OUVERTURE-sept.json.gz")["Celse"]["interne"]["paires_retenues"]
    return {name:[compare(lines,r,strict,paras) for r in cases] for name,paras in (("phrase",None),("paragraphe",wide))}


if __name__=="__main__":save(HERE/"LIGNES.json.gz",main(Path(sys.argv[1])))
