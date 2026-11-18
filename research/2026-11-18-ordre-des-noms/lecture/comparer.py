"""Cherche deux titres contigus à clé inconnue et conserve les prédictions pour le troisième."""
from collections import Counter
import gzip
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0,str(RESEARCH/"2026-11-18-formes-souterraines/nom/second"))
from transfert import corpus, tokens, spellings
sys.path.insert(0,str(RESEARCH/"2026-11-18-carte-sept-etoiles/lecture"))
from essai import tables

def read(path):
    return json.loads(path.read_text())

def save(name,data):
    content=json.dumps(data,ensure_ascii=False,indent=1)+"\n"
    dest=HERE/name
    if dest.suffix==".gz":
        dest.write_bytes(gzip.compress(content.encode(),mtime=0))
    else:
        dest.write_text(content)

def normal(word):
    return "".join(c for c in unicodedata.normalize("NFD",word.lower().strip()) if not unicodedata.combining(c))

def units(word):
    return tuple(re.findall(r"c[ktpf]h|ch|sh|.",word))

def titles():
    macer=read(RESEARCH/"2026-11-18-opcheor-paralleles/latin/corpus.json")
    first=read(RESEARCH/"2026-11-18-bax/etalonnage/TITRES.json")
    register=read(HERE.parent/"temoin/NOMS.json")
    later={r["chapitre"]:r["latin"] for r in register}
    assert len(later)==len(register)
    gart={r["chapitre"]:r["nom_latin"] for r in first}
    for n,title in later.items():
        assert n not in gart or gart[n]==title
        gart[n]=title
    series={
        "Macer":{n:(str(n),word) for n,word in enumerate(macer,1)},
        "Carrara":{n:(r["folio"],r["nom"]) for n,r in enumerate(read(HERE/"CARRARA.json"),1)},
        "Gart":{n:(str(n),t) for n,t in sorted(gart.items())}
    }
    return {s:{n:(ref,normal(w)) for n,(ref,w) in items.items()} for s,items in series.items()}

def blocks():
    for row in read(HERE.parent/"panneaux/RANGEES.json"):
        slots=row["positions"]
        for i in range(0,len(slots)-2,3):
            yield dict(page=row["page"],rank=row["rang"],level=row["niveau"],slots=slots[i:i+3])

def label(editions,page,slot):
    if len(slot["loci"])!=1:
        return None
    locus=page+"."+str(slot["loci"][0])
    forms=[]
    for rows in editions.values():
        record=rows.get(locus)
        if record is None or record[1]!="Lf" or record[2]!="@":
            return None
        for cut in ("joints","separes"):
            ws=tokens(record[3],cut)
            if len(ws)!=1 or not re.fullmatch("[a-z]+",ws[0]):
                return None
            forms.append(ws[0])
    return forms[0] if len(set(forms))==1 else None

def permit(word):
    return bool(re.fullmatch("[a-z]+",word))

def maps(signs,clear,width,prior=None):
    if not permit(clear) or not len(signs)<=len(clear)<=len(signs)*width:
        return
    for key in tables(signs,clear,width,prior):
        if width>1 or len(set(key.values()))==len(key):
            yield key

def predict(first,second,catalog,width):
    output=[]
    for book,entries in catalog.items():
        for idx in entries:
            if idx+1 not in entries or idx+2 not in entries:
                continue
            ref,a=entries[idx]
            _,b=entries[idx+1]
            _,c=entries[idx+2]
            for one in maps(first,a,width):
                for two in maps(second,b,width,one):
                    options=spellings(c,two) if permit(c) else []
                    output.append(dict(book=book,index=idx,ref=ref,seed=[a,b],expected=c,
                       key=two,initials=sorted(k for k,v in two.items() if c.startswith(v)),
                       spellings=[list(enc) for enc in options]))
    return output

def prepare(editions,catalog):
    out=[]
    for block in blocks():
        a,b,_=block["slots"]
        given=[label(editions,block["page"],slot) for slot in (a,b)]
        result=dict(**block,given=given,models={})
        if all(given):
            first,second=map(units,given)
            result["models"]={str(w):predict(first,second,catalog,w) for w in (1,2,3)}
        out.append(result)
    return out

def verify(editions,catalog,pred):
    out=[]
    for block in pred:
        page=block["page"]
        third=label(editions,page,block["slots"][2])
        signs=units(third or "")
        result=dict(page=page,rank=block["rank"],level=block["level"],
            fragments=[s["fragment"] for s in block["slots"]],given=block["given"],third=third,models={})
        for w,records in block["models"].items():
            counts=Counter()
            detail=[]
            for r in records:
                if not third or not permit(r["expected"]):
                    continue
                key=r["key"]
                closed=list(signs) in r["spellings"]
                survives=next(maps(signs,r["expected"],int(w),key),None)
                comp={name for _,name in catalog[r["book"]].values() if
                      name!=r["expected"] and permit(name)}
                competitors=sorted(name for name in comp if next(maps(signs,name,int(w),key),None))
                counts["eligible_tables"]+=1
                counts["initial_hit"]+=bool(signs[0] in r["initials"])
                counts["full_frozen"]+=closed
                counts["full_with_extension"]+=survives is not None
                counts["false_names_tested"]+=len(comp)
                counts["compatible_false_names"]+=len(competitors)
                detail.append(dict(book=r["book"],index=r["index"],expected=r["expected"],seed=r["seed"],
                    initial=signs[0] in r["initials"],frozen=closed,possible=survives,
                    actual_decoded=[key.get(g) for g in signs],alternate_names=competitors,
                    alternatives_tested=len(comp)))
            result["models"][w]=dict(tables=len(records),names=sorted({r["expected"] for r in records}),
                                     relevant=counts,detail=detail)
        out.append(result)
    return out

if __name__=="__main__":
    editions,_=corpus()
    catalog=titles()
    if sys.argv[1]=="predire":
        save("PREDICTIONS.json.gz",prepare(editions,catalog))
    elif sys.argv[1]=="verifier":
        preds=json.loads(gzip.decompress((HERE/"PREDICTIONS.json.gz").read_bytes()))
        save("VERIFICATION.json.gz",verify(editions,catalog,preds))
    else:
        raise ValueError("predire ou verifier")
