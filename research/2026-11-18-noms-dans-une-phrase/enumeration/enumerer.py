"""Mettre en regard les constructions A X A Y dans trois corpus."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import groupby
import gzip
import json
from pathlib import Path
import random
import re
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(HERE.parent / "contexte"))
from contexte import manuscript


def import_file(name, path):
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def describe(spans, gallery, conjunction, omit=()):
    tables, hits, constructions = {}, [], []
    for page, loc, words, offset in spans:
        if page in omit:
            continue
        lex = gallery[page]
        def named(x, y):
            return y in lex and x != y
        for i in range(len(words)-3):
            a,x,b,y = words[i:i+4]
            if None in (a,x,b,y):
                continue
            kind = "autres_repetes" if a==b else "sans_repetition"
            if a == b == conjunction:
                kind = "conjonction"
            c = tables.setdefault(kind, Counter())
            c["fenetres"] += 1
            if a == b == conjunction:
                constructions.append(dict(page=page, lieu=loc, rang=offset+i+1, x=x, y=y,
                        premier_indexe=x in lex, second_indexe=y in lex, distincts=x!=y))
            if x not in lex:
                continue
            c["x_legende"] += 1
            ok = named(x, y)
            c["deux_legendes_distinctes"] += int(ok)
            # Only shuffling other legible positions leaves the seed A X B intact.
            pool = [w for k,w in enumerate(words) if w and k not in (i,i+1,i+2)]
            c["esperance"] += Fraction(sum(named(x,w) for w in pool),len(pool))
            if kind != "sans_repetition" or ok:
                hits.append(dict(page=page, lieu=loc, rang=offset+i+1, debut=[a,x,b], suite=y, reussi=ok))
    for c in tables.values():
        c["esperance"] = str(c["esperance"])
    return {"comptes":tables, "positions":hits, "expressions":constructions}


def voynich():
    lex, _, records=manuscript()
    spans=[]
    for page, loc, sections in records:
        if page not in lex:
            continue
        offset=0
        for words in sections:
            spans.append((page,loc,words,offset))
            offset+=len(words)
    focal=next(ws for p,loc,ws,offset in spans if loc=="f99r.18" and offset==0)
    assert focal[6:9]==["daiin","okeoly","daiin"]
    actual=focal[9] if len(focal)>9 else None
    prior=focal[5]
    all_labels=set.union(*lex.values())
    focus=dict(gauche=prior, droite=actual, liste=sorted(lex["f99r"]-{"okeoly"}),
        gauche_dans_legendes=sorted(p for p,s in lex.items() if prior in s),
        droite_dans_legendes=sorted(p for p,s in lex.items() if actual in s))
    other={p for p in lex if not p.startswith("f99")}
    return dict(f99r_18=focus, autres_feuillets=describe(spans,lex,"daiin",set(lex)-other),
                feuillet99=describe(spans,lex,"daiin",other),
                sensibilite_toutes_les_legendes=describe(spans,{p:all_labels for p in lex},"daiin"))


def historic():
    base=RESEARCH/"2026-11-18-noms-dans-les-notices/historique"
    m=import_file("edition_macer",base/"extract.py")
    raw=gzip.decompress((base/"source.wiki.gz").read_bytes())
    assert sha256(raw).hexdigest()==m.SOURCE_SHA256
    text=raw.decode()
    headings=list(m.HEADING.finditer(text))
    assert len(headings)==77
    titles={m.tokens(heading[2])[0] for heading in headings}
    macer=[]; verse=0
    for i,h in enumerate(headings):
        end=headings[i+1].start() if i+1<len(headings) else len(text)
        block=re.fullmatch(r"\s*<poem>(.*?)</poem>\s*",text[h.end():end],re.S)
        for line in block[1].strip().splitlines():
            words=m.tokens(re.sub(r"\{\{Versus\|\d+\}\}","",line))
            if words:
                verse+=1
                macer.append(("macer",f"{i+1}.{verse}",words,0))
    lib=RESEARCH/"2026-11-18-legendes-et-paragraphes/temoin"
    b=import_file("edition_cuisine",lib/"verifier.py")
    html=Path(sys.argv[1]).read_bytes()
    assert sha256(html).hexdigest()==b.INPUT_SHA
    parser=b.Edition()
    parser.feed(html.decode()); parser.close()
    assert set(parser.paragraphs)==set(range(1,169))
    meals=[]
    for no, bypage in sorted(parser.paragraphs.items()):
        offset=0
        for face, ww in groupby(bypage,lambda pair:pair[0]):
            words=[w for _,w in ww]
            meals.append(("cuisine",f"{no}.{face}",words,offset))
            offset+=len(words)
    ingredients=set((lib/"ingredients.txt").read_text().split())
    return [(macer,{"macer":titles}), (meals,{"cuisine":ingredients})]


def encrypted_check(spans, lex, name):
    allwords=sorted(set(w for _,_,words,_ in spans for w in words)|lex[name])
    codes=[f"g{i:05d}" for i in range(len(allwords))]
    random.Random(3341).shuffle(codes)
    key=dict(zip(allwords,codes))
    coded=[(p,loc,[key[w] for w in words],offset) for p,loc,words,offset in spans]
    a=describe(spans,lex,"et")
    b=describe(coded,{name:{key[w] for w in lex[name]}},key["et"])
    assert a["comptes"]==b["comptes"]
    for u,v in zip(a["expressions"],b["expressions"],strict=True):
        assert (u["lieu"],u["rang"],key[u["x"]],key[u["y"]])==(v["lieu"],v["rang"],v["x"],v["y"])
    a["renseignements"] = {"mots":sum(len(ws) for _,_,ws,_ in spans),"formes_index":len(lex[name]),"chiffrage_verifie":True}
    return a


if __name__=="__main__":
    out={"voynich":voynich()}
    for spans, lex in historic():
        name=next(iter(lex))
        out[name]=encrypted_check(spans,lex,name)
    compressed=gzip.compress((json.dumps(out,sort_keys=True,ensure_ascii=False,indent=1)+"\n").encode(),mtime=0)
    (HERE/"RESULTATS.json.gz").write_bytes(compressed)
    print(out["voynich"]["f99r_18"])
    for key in ("macer","cuisine"):
        print(key, out[key]["renseignements"],out[key]["comptes"].get("conjonction"))
    for key in ("autres_feuillets","feuillet99","sensibilite_toutes_les_legendes"):
        print(key, out["voynich"][key]["comptes"])
