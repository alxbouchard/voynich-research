"""Vérifie la contraction fixée dans HYPOTHESE.md, sans joindre deux loci."""
import csv
import gzip
import hashlib
import itertools
import json
import re
import sys
from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from secteurs import ALG, DATA, RESEARCH, data, null_hist, slots

MODES = ("deux", "trois", "complet")
SECTOR_FILE = RESEARCH / "2026-11-18-secteurs-rouges/photos/secteurs.csv"


@lru_cache(maxsize=None)
def units(word, collapse):
    if collapse:
        word = re.sub("i{2,}", "i", word)
    return tuple(ALG["EVA"].findall(word))


@lru_cache(maxsize=None)
def cuts(a, b, target, collapse):
    if not a or not b or not target:
        return ()
    a, b, target = (units(w, collapse) for w in (a,b,target))
    splits = []
    for left in range(2,min(len(a),len(target)-1)):
        right = len(target)-left
        if 2 <= right < len(b) and a[:left] == target[:left] and b[-right:] == target[left:]:
            splits.append(("".join(a[:left]), "".join(b[-right:])))
    return tuple(splits)


def occurrence(page, table, split, variant, labels, panels):
    def line(loc):
        return slots(table,page,[loc],split,variant)
    return ({i:line(n) for i,n in labels.items()},
            {i:[line(n) for n in ns] for i,ns in panels.items()})


def primary_loci():
    labels, panels = {}, {}
    with SECTOR_FILE.open() as f:
        for row in csv.DictReader(f):
            i=int(row["secteur"])
            if row["locus_isole"]:
                labels[i]=int(row["locus_isole"])
            a,b=map(int,row["loci_paragraphe"].split("–"))
            panels[i]=list(range(a,b+1))
    return labels, panels


def incidence(labels, panels, collapse, reverse):
    """Evaluate every label position against every two/three-group source window."""
    hits = []
    for src, query in labels.items():
        for dst, lines in panels.items():
            for line in lines:
                for j in range(len(line)-1):
                    pair = line[j:j+2]
                    (a_loc,a), (b_loc,b) = pair[::-1] if reverse else pair
                    third = line[j+2] if j+2 < len(line) else None
                    for pos,(loc,target) in enumerate(query):
                        parts = cuts(a,b,target,collapse)
                        if not parts:
                            continue
                        # Even in the i-normalized variant, the optional third word is copied verbatim.
                        copied = (third and third[1] and pos+1 < len(query)
                                  and third[1] == query[pos+1][1])
                        complete = pos==0 and (len(query)==1 or (len(query)==2 and copied))
                        hits.append({
                            "requete": src, "destination": dst, "source": pair, "cible": (loc,target),
                            "coupes": parts, "troisieme_copie": (third,query[pos+1]) if copied else None,
                            "legende_complete": bool(complete)})
    return hits


def win_key(hit, mode):
    return tuple(loc for loc,_ in hit["source"]) + ((hit["troisieme_copie"][0][0],)
            if mode=="trois" or (mode=="complet" and hit["troisieme_copie"]) else ())


def evaluate(queries, destinations, hits, mode):
    accepted = [h for h in hits if h["requete"] in queries and (
        mode == "deux" or (mode == "trois" and h["troisieme_copie"])
        or (mode == "complet" and h["legende_complete"]))]
    cells = defaultdict(set)
    for h in accepted:
        cells[h["requete"],h["destination"]].add(win_key(h,mode))
    n = len(destinations)
    aligned = 0
    masks, counts, ranks = [], [], []
    for i in queries:
        windows = [len(cells[i,j]) for j in destinations]
        own = windows[destinations.index(i)]
        aligned += own > 0
        counts.append(windows)
        ranks.append((1+sum(v>own for v in windows),sum(v>=own for v in windows)))
        masks.append(sum(1<<j for j,v in enumerate(windows) if v))
    hist = null_hist(n,tuple(masks))
    rotations = [sum((mask >> ((destinations.index(i)+shift)%n)) & 1
                    for i,mask in zip(queries,masks)) for shift in range(n)]
    assert aligned == rotations[0]
    return {"succes":aligned,"fenetres_distinctes_par_destination":counts,
            "rang_local_sur_fenetres_avec_ex_aequo":ranks,"rotations":rotations,
            "rang_rotation_avec_ex_aequo":[1+sum(v>aligned for v in rotations),sum(v>=aligned for v in rotations)],
            "p_rotations":str(Fraction(sum(v>=aligned for v in rotations),n)),
            "effectifs_injections":hist,"p_injections":str(Fraction(sum(hist[aligned:]),sum(hist))),
            "esperance":str(Fraction(sum(mask.bit_count() for mask in masks),n)),
            "fenetres_locales":sum(len(cells[i,i]) for i in queries),
            "fenetres_concurrentes":sum(len(cells[i,j]) for i in queries for j in destinations if j!=i)}


def volume(panels):
    return {sector: {str(k): {
        "toutes":sum(max(0,len(line)-k+1) for line in lines),
        "lisibles":sum(all(w for _,w in line[j:j+k]) for line in lines for j in range(max(0,len(line)-k+1)))
    } for k in (2,3)} for sector, lines in panels.items()}


def page_run(table, split, variant, page, loci):
    labels,panels = occurrence(page,table,split,variant,*loci)
    queries = list(labels)
    partitions = {"tous":queries}
    if page == "f67r2":
        partitions["origine"] = [5,8]
        partitions["cinq_autres"] = [i for i in queries if i not in (5,8)]
    dest = list(panels)
    subsets = {"toutes_lignes":panels}
    if page=="f67r2":
        subsets["derniere_ligne"]={i:lines[-1:] for i,lines in panels.items()}
    res={"cibles":labels,"textes":panels,"ordre_destinations":dest,"ordre_requetes":partitions,"analyses":{}}
    for where,bodies in subsets.items():
        result = {"volume":volume(bodies),"regles":{}}
        for collapse,reverse in itertools.product((False,True),repeat=2):
            name=("i_reduit" if collapse else "exact")+"/"+("inverse" if reverse else "direct")
            hits=incidence(labels,bodies,collapse,reverse)
            result["regles"][name]={"accords":hits,"scores":{
                group:{mode:evaluate(group_queries,dest,hits,mode) for mode in MODES}
                for group,group_queries in partitions.items()}}
        res["analyses"][where]=result
    return res


def self_test():
    assert cuts("ytor","daiin","ytoaiin",False)==(("yto","aiin"),)
    assert cuts("xoab","oyz","xoyz",False)==(("xo","yz"),)
    assert cuts("aaaax","zaaaa","aaaaaa",False)==(("aa","aaaa"),("aaa","aaa"),("aaaa","aa"))
    assert not cuts("okeor","aiin","okain",True)
    assert not cuts("chx","oyz","chyz",False) # ch is one EVA unit
    assert not cuts(None,"daiin","ytoaiin",False)
    assert cuts("ytor","daiin","ytoaiin",True)==(("yto","ain"),)
    assert not cuts("daiin","ytor","ytoaiin",False)
    lab={1:[("c.1:1","ytoaiin"),("c.1:2","am")]}
    src={1:[[("p.1:1","ytor"),("p.1:2","daiin"),("p.1:3","am")]],
         2:[[("p.2:1","ytor")],[("p.3:1","daiin"),("p.3:2","am")]]}
    hits=incidence(lab,src,False,False)
    assert len(hits)==1 and hits[0]["legende_complete"] and hits[0]["troisieme_copie"]
    assert null_hist(3,(1,2,4))==[2,3,0,1]


def dump(path, result):
    payload = (json.dumps(result,ensure_ascii=False,separators=(",",":"))+"\n").encode()
    path.write_bytes(gzip.compress(payload,compresslevel=9,mtime=0))


def run(page, loci, output):
    res={"page":page,"geometrie":{"legendes":loci[0],"destinations":loci[1]},"lectures":{}}
    for ed, file in (("H","IT2a-n"),("ZL","ZL3b-n")):
        path=DATA/(file+".txt")
        table=data(path)
        res.setdefault("sha256",{})[ed]=hashlib.sha256(path.read_bytes()).hexdigest()
        for split, variant in itertools.product((False,True),("strict","first","last")):
            key="/".join((ed,"separe" if split else "joint",variant))
            res["lectures"][key]=page_run(table,split,variant,page,loci)
    dump(HERE/f"{output}.json.gz",res)
    return res


if __name__=="__main__":
    self_test()
    run("f67r2",primary_loci(),"f67r2")
    geom = json.loads((HERE.parent/"geometrie/GEOMETRIE.json").read_text())
    maps = {"f69r":("strict","possible"),
            "f67v1":("axis_inside_visible_frame","possible_including_edge")}
    for page, versions in maps.items():
        for version in versions:
            panels = {int(k):v for k,v in geom[page][version].items()}
            labels = {i:i for i in panels}
            run(page,(labels,panels),f"{page}-{version}")
