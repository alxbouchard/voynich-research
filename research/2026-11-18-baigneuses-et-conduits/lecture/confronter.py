"""Recherche deux mots de f75v dans les vers de Pierre d’Éboli, puis éprouve les clés."""
from collections import Counter, defaultdict
import csv
import gzip
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / "2026-11-18-ordre-des-noms/lecture"))
from comparer import corpus, tokens, units
from essai import tables

SEED = ("olkchy","otoly")
SEMANTIC = {
    "aqua": "aqua aquae aquam aquarum aquas aquis aque",
    "balneum": "balneum balnei balneo balnea balneorum balneis",
    "fons": "fons fontis fonti fontem fonte fontes fontium fontibus",
    "mulier": "mulier mulieris mulieri mulierem muliere mulieres mulierum mulieribus",
    "femina": "femina feminae femine feminam feminarum feminas feminis",
    "canalis": "canalis canali canalem canale canales canalium canalibus",
}
FORMS = {word for forms in SEMANTIC.values() for word in forms.split()}


def read(path):
    data = path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)


def save(filename, result):
    path = HERE / filename
    data = (json.dumps(result,ensure_ascii=False,indent=1)+"\n").encode()
    path.write_bytes(gzip.compress(data,mtime=0) if path.suffix==".gz" else data)


def words(text):
    plain = "".join(c for c in unicodedata.normalize("NFD",text.lower()) if not unicodedata.combining(c))
    return re.findall("[a-z]+", plain)


def repertories(folder):
    source = folder / "vers.json"
    assert sha256(source.read_bytes()).hexdigest() == read(HERE/"SOURCE.json")["sha256"]
    chapters = read(source)
    corpus_lines = [[words(v) for v in src["vers"]] for src in chapters]
    macer = defaultdict(list)
    with (RESEARCH/"2026-11-18-opcheor-paralleles/latin/vers.tsv").open() as stream:
        for row in csv.DictReader(stream,delimiter="\t"):
            macer[row["notice"]].append(words(row["texte_edite"]))
    sets = {}
    for name, batch in [("bains",corpus_lines),("macer",list(macer.values()))]:
        lookup = defaultdict(list)
        joins = defaultdict(list)
        for i,chapter in enumerate(batch):
            for j,line in enumerate(chapter):
                for k,pair in enumerate(zip(line,line[1:])):
                    lookup[pair].append((i,j+1,k+1))
                if j:
                    joins[(chapter[j-1][-1],line[0])].append((i,j,len(chapter[j-1])))
        sets[name] = lookup
        if name=="bains":
            sets["frontiere"] = joins
    headings={}
    for i,row in enumerate(chapters):
        title = words(re.sub(r"^[IVXLCDM]+\s+", "", row["titre"]))
        if len(title)==2:
            headings[tuple(title)]=[(i,0,0)]
    sets["titres"]=headings
    return sets


def transformed(word, mode):
    remaining = units(word)
    if "o" in mode and remaining[:1] == ("o",):
        remaining=remaining[1:]
    if "y" in mode and remaining[-1:] == ("y",):
        remaining=remaining[:-1]
    return remaining


def assignments(segments, clear, width, prior=None):
    if not all(segments) or not all(len(s)<=len(t)<=width*len(s) for s,t in zip(segments,clear,strict=True)):
        return
    signs = (*segments[0]," ",*segments[1])
    for key in tables(signs," ".join(clear),width,prior):
        if width!=1 or len(set(key.values()))==len(key):
            yield key


def encodable(word, key):
    @lru_cache(None)
    def visit(i):
        return i==len(word) or any(word.startswith(v,i) and visit(i+len(v)) for v in set(key.values()))
    return visit(0)


def forecasts(sets):
    experiments=[]
    for mode, direction, width in product(("-", "o", "y", "oy"), ("haut-bas","bas-haut"), (1,2)):
        seed=SEED if direction=="haut-bas" else SEED[::-1]
        segments=tuple(transformed(w,mode) for w in seed)
        counts={}
        valid=[]
        for name, pairs in sets.items():
            accepted=[]
            for pair, refs in pairs.items():
                for key in assignments(segments,pair,width):
                    hit = pair[seed.index("otoly")] in FORMS
                    accepted.append((pair,key,hit))
                    if name=="bains":
                        lexical={w for q in pairs for w in q}
                        possible={w for w in lexical if encodable(w,key)}
                        predictions=sorted(" ".join(q) for q in pairs if q!=pair and set(q)<=possible)
                        valid.append(dict(expression=pair,lieux=refs,cle=key,sens=hit,annonce=predictions))
            counts[name]=dict(paires=len(pairs),admissibles=len({p for p,k,h in accepted}),
                              tables=len(accepted),sens=sorted({" ".join(p) for p,k,h in accepted if h}))
        experiments.append(dict(mode=mode,ordre=direction,largeur=width,comptes=counts,lectures=valid))
    return experiments


def objects():
    raw = read(HERE.parent/"corpus/INVENTAIRE.json")
    result=[]
    for row in raw["emplacements"]:
        if not row["code"]:
            continue
        editions = [v["editions"] for v in row["lieux"].values()]
        allread=[]
        for ed in ("H","ZL"):
            for cut in ("joints","separes"):
                if any(ed not in views or views[ed] is None for views in editions):
                    break
                allread.append(tuple(w for v in editions for w in tokens(v[ed]["original"],cut)))
        if len(allread)!=4 or len(set(allread))!=1 or not all(re.fullmatch("[a-z]+",w) for w in allread[0]):
            continue
        result.append(dict(lieu=row["id"],bifeuillet=row["bifeuillet"],mots=allread[0]))
    return result


def decode(signs,key):
    return "".join(key[s] for s in signs) if signs and all(s in key for s in signs) else None


def evaluate(sets, records):
    sites=objects()
    seedsite,=[s for s in sites if s["lieu"]=="f75v.36+37"]
    assert tuple(seedsite["mots"])==SEED
    source=seedsite["bifeuillet"]
    pairs=sets["bains"]
    lex={w for q in pairs for w in q}
    rows=[]
    for exp in records:
        mode,width=exp["mode"],exp["largeur"]
        backwards=exp["ordre"]=="bas-haut"
        for r in exp["lectures"]:
            key=r["cle"]
            pair=tuple(r["expression"])
            other_words=set()
            details=[]
            for site in sites:
                if site==seedsite:continue
                seq=site["mots"][::-1] if backwards else site["mots"]
                signs=tuple(transformed(w,mode) for w in seq)
                if len(seq)==1 and site["bifeuillet"]!=source:
                    if signs[0] and all(s in key for s in signs[0]):
                        other_words.add(signs[0])
                if len(seq)!=2:continue
                actual=tuple(decode(s,key) for s in signs)
                allowed=sorted(" ".join(q) for q in pairs
                               if q!=pair and next(assignments(signs,q,width,key),None) is not None)
                match=" ".join(actual) if all(actual) else None
                if match and match!=" ".join(pair):
                    assert (match in allowed)==(match in r["annonce"])
                details.append(dict(lieu=site["lieu"],autre_bifeuillet=site["bifeuillet"]!=source,
                                    eva=seq,dechiffre=actual,correspondances=allowed,
                                    complet=bool(match and match in allowed)))
            singles=sorted({decode(s,key) for s in other_words} & lex & FORMS)
            permuted = Counter()
            # Test all label permutations on the encodable single words, recording distinct hits.
            for vals in set(permutations(key.values())):
                other=dict(zip(key,vals))
                permuted[len({decode(s,other) for s in other_words} & lex & FORMS)]+=1
            passed=[s for s in sites if len(s["mots"])==1 and s["bifeuillet"]!=source
                and decode(transformed(s["mots"][0],mode),key) in singles]
            rows.append(dict(mode=mode,ordre=exp["ordre"],largeur=width,lecture=pair,cle=key,
                   nouveaux_noms=singles,lieux_noms=passed,temoin_permute=dict(sorted(permuted.items())),paires=details))
    return dict(sites=sites,bifeuillet_initial=source,lectures=rows)


if __name__=="__main__":
    data=repertories(Path(sys.argv[2]))
    if sys.argv[1]=="predire":
        save("PREDICTIONS.json.gz",forecasts(data))
    elif sys.argv[1]=="verifier":
        save("RESULTATS.json.gz",evaluate(data,read(HERE/"PREDICTIONS.json.gz")))
    else:
        raise ValueError("predire ou verifier")
