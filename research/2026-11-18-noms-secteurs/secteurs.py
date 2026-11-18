"""Enquiries from four label series against the twelve paragraphs on f67r2."""
import csv
import hashlib
import json
import math
import re
import sys
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
DATA = RESEARCH.parent / "voynich_20261028/data"
sys.path.insert(0, str(RESEARCH / "2026-11-18-sept-astres/transfert"))
from verifier import split_slots

RULES = ("exact","base","debut3")
PARTNERS = {1:29,3:32,5:33,6:27,7:31,8:30,11:28}
ROW = re.compile(r"<(f\w+)\.(\d+),[^>]+>\s*(.*)")
ALG = {"EVA":re.compile("ckh|cth|cph|cfh|ch|sh|."),"ASCII":re.compile(".")}


def data(path):
    tables = {}
    for line in path.read_text().splitlines():
        match = ROW.fullmatch(line)
        if match:
            tables[(match[1],int(match[2]))] = match[3]
    return tables


def slots(table, page, ids, split, variant):
    observations = []
    for n in ids:
        for i,s in enumerate(split_slots(table[(page,n)],split),1):
            alt = re.sub(r"\[([^\]]+)\]", lambda m: "?" if variant=="strict" else m[1].split(":")[0 if variant=="first" else -1],s)
            clean = alt.replace("{","").replace("}","")
            value = clean if re.fullmatch("[a-z]+",clean) else None
            observations.append((f"{page}.{n}:{i}",value))
    return observations


@lru_cache(maxsize=None)
def match_rule(a,b,alphabet,rule):
    if not a or not b:
        return False
    if rule=="exact":
        return a==b
    u,v = ALG[alphabet].findall(a), ALG[alphabet].findall(b)
    if rule=="debut3":
        return len(u)>=3 and u[:3]==v[:3]
    prefix = 0
    for x,y in zip(u,v):
        if x!=y:
            break
        prefix += 1
    return a==b or (prefix>=3 and max(len(u),len(v))-prefix<=2)


@lru_cache(maxsize=None)
def null_hist(n, row_masks):
    """Exact injection null from rook numbers on the hit cells."""
    q = len(row_masks)
    ways = {0:1}
    for row in row_masks:
        new = ways.copy()
        for used,val in ways.items():
            free = row & ~used
            while free:
                bit = free & -free
                new[used|bit] = new.get(used|bit,0)+val
                free -= bit
        ways = new
    rooks = Counter()
    for mask,v in ways.items():
        rooks[mask.bit_count()] += v
    pairs = [rooks[k]*math.perm(n-k,q-k) for k in range(q+1)]
    hist = [sum((-1)**(k-j)*math.comb(k,j)*pairs[k] for k in range(j,q+1)) for j in range(q+1)]
    assert min(hist)>=0 and sum(hist)==math.perm(n,q)
    return hist


def assess(queries, passages, alphabet, rule):
    masks,actual,own_hits = [],[],{}
    n = len(passages)
    for pos,source in queries.items():
        mask=0
        for j,body in passages.items():
            hits = [(i+1,qid,word,bid,other) for qid,word in source for i,(bid,other) in enumerate(body)
                    if match_rule(word,other,alphabet,rule)]
            if hits:
                mask |= 1<<(j-1)
                if j==pos:
                    own_hits[pos]=hits
        masks.append(mask)
        actual.append(pos)
    aligned = len(own_hits)
    hist = null_hist(n,tuple(masks))
    rotations = [sum(bool(mask & (1<<((i-1+s)%n))) for mask,i in zip(masks,actual)) for s in range(n)]
    assert aligned==rotations[0]
    return {"secteurs_requetes":actual,"masques_compatibles":masks,"succes":aligned,
            "succes_destination_unique":sum(mask==(1<<(i-1)) for mask,i in zip(masks,actual)),
            "rencontres_locales":own_hits,"rotations":rotations,"distribution_permutations":hist,
            "permutations_au_moins_aussi_bonnes":str(Fraction(sum(hist[aligned:]),sum(hist))),
            "esperance_succes":str(Fraction(sum(mask.bit_count() for mask in masks),n))}


def contiguous(query,body):
    words=[w for _,w in query]
    return bool(words and all(words)) and any([w for _,w in body[j:j+len(words)]]==words
                                              for j in range(len(body)-len(words)+1))


def formula_free(passages, sectors, alphabet):
    out={}
    for mode in ("libre","soude_1","soude_2","soude_3"):
        per_sector={}
        uncertain=[]
        for i in sectors:
            words = [w for _,w in passages[i]]
            pool = words[:-1] if mode=="libre" else words
            if None in pool:
                uncertain.append(i)
            observed=set()
            for word in filter(None,pool):
                if mode=="libre":
                    observed.add(word)
                else:
                    width=int(mode[-1])
                    units=ALG[alphabet].findall(word)
                    if len(units)>width:
                        observed.add("".join(units[:width]))
            per_sector[i]=observed
        pool=set.union(*per_sector.values())
        hits={w:[i for i in sectors if w in per_sector[i]] for w in pool}
        mx=max(map(len,hits.values()),default=0)
        upper=max([len(set(v)|set(uncertain)) for v in hits.values()]+[len(uncertain)])
        out[mode]={"maximum":mx,"ex_aequo":{w:hits[w] for w in sorted(hits) if len(hits[w])==mx},
                   "plafond_si_chaque_position_illisible_est_favorable":upper,
                   "secteurs_avec_position_illisible":uncertain}
    return out


def assemble(table,split,variant):
    path=RESEARCH/"2026-11-18-secteurs-rouges/photos/secteurs.csv"
    with path.open() as stream:
        sectors=list(csv.DictReader(stream))
    sources={s:{} for s in ("isole","rouge","visage","cancer")}
    passages={}
    for row in sectors:
        i=int(row["secteur"])
        lo,hi=map(int,row["loci_paragraphe"].split("–"))
        passages[i]=slots(table,"f67r2",range(lo,hi+1),split,variant)
        for key in ("isole","rouge","visage"):
            locus=row["locus_"+key]
            if locus:
                sources[key][i]=slots(table,"f67r2",[int(locus)],split,variant)
        if i in PARTNERS:
            sources["cancer"][i]=slots(table,"f72r3",[PARTNERS[i]],split,variant)
    return sources,passages


def inspect(table,split,variant):
    sources,paragraphs=assemble(table,split,variant)
    evidence={"paragraphes":paragraphs,"legendes":sources,"essais":{}}
    for alphabet in ALG:
        evidence["essais"][alphabet]={}
        for name,queries in sources.items():
            results={}
            for size in (8,0):
                passages={i:(s[:size] if size else s) for i,s in paragraphs.items()}
                results[str(size) if size else "tout"]={rule:assess(queries,passages,alphabet,rule) for rule in RULES}
            evidence["essais"][alphabet][name]=results
        evidence["essais"][alphabet]["preposition_sans_valeur_imposee"]=formula_free(paragraphs,tuple(PARTNERS),alphabet)
    evidence["legendes_completes_reprises"]={k:[i for i,q in queries.items() if contiguous(q,paragraphs[i])]
                                             for k,queries in sources.items()}
    evidence["debuts_publies"]={w:{i:[loc for loc,word in row if word and word.startswith(w)]
                                    for i,row in paragraphs.items() if any(word and word.startswith(w) for _,word in row)}
                                for w in ("ytoa","yfa","op")}
    return evidence


def main():
    out={}
    for ed in ("IT2a-n","ZL3b-n"):
        path=DATA/(ed+".txt")
        table=data(path)
        out[ed]={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"lectures":{}}
        for split in (False,True):
            for variant in ("strict","first","last"):
                run=inspect(table,split,variant)
                out[ed]["lectures"][("separe" if split else "joint")+"_"+variant]=run
    assert null_hist(3,(1,2,4))==[2,3,0,1]
    assert null_hist(3,(7,0))==[0,6,0]
    assert match_rule("ytor","ytoaiin","EVA","debut3") and not match_rule("ytor","ytoaiin","EVA","base")
    (HERE/"secteurs.json").write_text(json.dumps(out,ensure_ascii=False,separators=(",",":"))+"\n")

if __name__=="__main__":
    main()
