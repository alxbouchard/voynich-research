"""Separate the effects of the photo reading and paragraph bounds; test a new prediction."""
import itertools
import json
import re
from collections import defaultdict
from copy import deepcopy

from predire import DATA, EDITIONS, HERE, sha, word_pairs
from tester import PRIMARY, pairs_in, permute, raw_text, slice_local, tokens, word_map

PAIR = tuple(sorted(("opchy","otol")))


def overlap(hblocks,zblocks):
    """Maximal contiguous stretches within one paragraph of both transcriptions."""
    index={loc:(j,idx) for j,block in enumerate(zblocks) for idx,loc in enumerate(block)}
    out=[]
    for block in hblocks:
        run=[]
        previous=None
        for loc in block:
            pos=index.get(loc)
            if pos is None or previous is None or pos!=(previous[0],previous[1]+1):
                if run:
                    out.append(run)
                run=[]
            if pos is not None:
                run.append(loc)
            previous=pos
        if run:
            out.append(run)
    assert sum(map(len,out))==len(set.intersection({l for b in hblocks for l in b},set(index)))
    return out


def evidence(hits,valid):
    return {" ".join(p):hits[p] for p in sorted(valid & hits.keys())}


def reread():
    preds=json.loads((HERE/"predictions_pots_elargis.json").read_text())
    base=preds["conditions"][PRIMARY]
    markup=json.loads((HERE/"notices/paragraphes.json").read_text())
    cuts={ed:[[l.split(",")[0] for l in seq] for seq in entries] for ed,entries in markup.items()}
    cuts["chevauchement"]=overlap(cuts["H"],cuts["ZL"])
    raw=raw_text({p[0].split(".")[0] for p in cuts["H"]})
    out={}
    for reading,method in itertools.product(("editions","otol","okol"),("accord","chevauchement")):
        rows=deepcopy(base)
        row=rows["f102v2/1"]
        assert row["objets"]["f102v2.7"]==[]
        if reading!="editions":
            row["objets"]["f102v2.7"]=[reading]
            row["paires"]=sorted(word_pairs(row["objets"].values()))
        allowed=set().union(*({tuple(p) for p in r["paires"]} for r in rows.values()))
        vocab={w for r in rows.values() for group in r["objets"].values() for w in group}
        hits,available,volume=pairs_in(cuts[method],"accord",raw,False,word_map(vocab,False),8)
        observed=evidence(hits,allowed)
        null=permute(rows,{"notices":hits.keys()},"notices")
        out[reading+"/"+method]={"passages":len(cuts[method]),"positions_par_edition":volume,
                                "avec_deux_mots_attestes":sum(set(p)<=available for p in allowed),
                                "paires":len(allowed),"rencontres":observed,"permutation":null}
        if reading=="otol" and method=="chevauchement":
            # Enumerate the conditional grouping probability for the observed
            # eligible edges within each face, independently of the shuffles.
            for page in sorted({r["page"] for r in rows.values()}):
                parts=[r for r in rows.values() if r["page"]==page]
                flat={k:v for r in parts for k,v in r["objets"].items()}
                edges=[(i,j) for i,j in itertools.combinations(flat,2)
                       if any(tuple(sorted((a,b))) in hits for a in flat[i] for b in flat[j] if a!=b)]
                if edges:
                    desc=out[reading+"/"+method].setdefault('aretes_par_face',{})
                    sizes=[len(r["objets"]) for r in parts]
                    desc[page]={"paires_objets":edges,"tailles":sizes}
                    if len(edges)==1:
                        from fractions import Fraction
                        from math import comb
                        desc[page]["probabilite_meme_rang"]=str(Fraction(sum(comb(n,2) for n in sizes),comb(sum(sizes),2)))
    return out


def new_pages():
    pages=set()
    for ed,file in EDITIONS.items():
        found={m[1] for s in (DATA/file).read_text().splitlines()
               if (m:=re.match(r"^<(f(?:58|100|101)[rv]\d*)>\s",s))}
        pages.update(found)
    raw=raw_text(pages)
    out={}
    for page in sorted(pages):
        blocks={}
        for ed,table in raw.items():
            ids=sorted((loc for loc in table if loc.split('.')[0]==page),key=lambda loc:int(loc.split('.')[1]))
            blocks[ed]=slice_local(ids,table)
        common=overlap(blocks["H"],blocks["ZL"])
        for split in (False,True):
            stats={}
            tags=word_map(set(PAIR),False)
            for ed,table in raw.items():
                singles={w:[] for w in PAIR}
                distances=[]
                n=0
                for seq in blocks[ed]:
                    pos={w:[] for w in PAIR}
                    offset=0
                    for loc in seq:
                        for k,w in enumerate(tokens(table[loc],split),1):
                            offset+=1
                            if w in pos:
                                pos[w].append(offset)
                                singles[w].append([loc,k])
                    n+=offset
                    d=[abs(i-j) for i in pos[PAIR[0]] for j in pos[PAIR[1]]]
                    if d:
                        distances.append((min(d),seq[0]))
                stats[ed]={"paragraphes":len(blocks[ed]),"positions":n,"mots":singles,"distances_minimales":distances}
            hits,available,volume=pairs_in(common,"accord",raw,split,tags,8)
            whole,_,_=pairs_in(common,"accord",raw,split,tags,0)
            stats["accord"]={"troncons":len(common),"presents":sorted(available),"positions":volume,
                             "rencontres_proches":hits.get(PAIR,[]),"rencontres_paragraphe":whole.get(PAIR,[])}
            out[page+("/separe" if split else "/joint")]=stats
    return out


if __name__=="__main__":
    out={"prediction_sha256":sha(HERE/"EPREUVE_F58.md"),"relecture_cahier20":reread(),"nouveaux_passages":new_pages()}
    (HERE/"deux_feuilles.json").write_text(json.dumps(out,indent=1,ensure_ascii=False)+"\n")
