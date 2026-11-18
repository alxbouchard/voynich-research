"""Calculer les annonces à partir du seul Macer, puis comparer les sept corps de notices."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations
from pathlib import Path
import argparse
import json
import re

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / "2026-11-18-opcheor-paralleles/latin/corpus.json"
PANELS = {"01":"Absinthium", "02":"Abrotanum", "03":"Althaea", "07":"Allium",
          "10":"Anethum", "11":"Apium", "12":"Artemisia"}
ORGANS = {
    "oeil":r"ocul.*", "oreille":r"aur(?:is|em|e|es|ibus|ium|i)",
    "dent":r"den(?:s|t(?:is|em|e|es|ibus|ium|i))", "tête":r"cap(?:ut|it(?:is|i|e|a|ibus|um))",
    "poitrine":r"pect(?:us|or(?:is|i|e|a|ibus|um))", "foie":r"(?:jecor|iecor|jecur|iecur|hepat).*",
    "rate":r"spl(?:en|enis|enem|ene|enibus|eni|e[n]?is)", "rein":r"ren(?:es|um|ibus|is|em|e)",
    "estomac":r"sto[m]+ach.*", "ventre":r"vent(?:er|r(?:is|i|e|em|es|ium|ibus))",
    "peau":r"cut(?:is|i|em|e|es|ibus|ium)", "utérus":r"(?:matri(?:x|c(?:em|e|is|i))|uter(?:us|i|o|um))",
    "menstrues":r"menstru.*", "urine":r"urin.*", "poumon":r"pulmo.*",
    "coeur":r"(?:cor|cord(?:e|is|i|a|ibus))", "sang":r"sangu(?:is|in.*)",
    "intestin":r"intestin.*", "gorge":r"(?:guttur|guttur(?:is|i|e|a)|fauc(?:es|ibus|ium|em|e))",
    "os":r"(?:ossa|ossis|ossibus|ossium)", "nerf":r"nerv.*",
    "cheveu":r"capill.*", "pied":r"(?:pes|ped(?:is|i|em|e|es|ibus|um))"}
ORDS = (r"prim(?:us|a|um|i|o|e)", r"secund(?:us|a|um|i|o|e)",
        r"ter[ct]i(?:us|a|um|i|o|e)", r"quart(?:us|a|um|i|o|e)")


def write(path, data):
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False, sort_keys=True)+"\n")


def family(word):
    return next((lab for lab,pattern in ORGANS.items() if re.fullmatch(pattern,word)), None)


def ordinal(word):
    return next((i for i,pattern in enumerate(ORDS,1) if re.fullmatch(pattern,word)), None)


def degree(words):
    for i,word in enumerate(words):
        n=ordinal(word)
        window=words[max(0,i-8):i+9]
        if n and any(re.match(r"grad|ordin",w) for w in window):
            return {"valeur":n,"graphie":word,"rang":i+1,"contexte":window}


def announce():
    documents = json.loads(SOURCE.read_bytes())
    df = Counter(k for words in documents.values() for k in {family(w) for w in words} if k)
    out = {}
    for panel,title in PANELS.items():
        words = documents[title]
        hits = [(i,w,family(w)) for i,w in enumerate(words,1) if family(w)]
        counts = Counter(k for _,_,k in hits)
        if hits:
            rank = lambda k:(-Fraction(counts[k],df[k]),next(i for i,w,f in hits if f==k),k)
            k=min(counts,key=rank)
            typed=Counter(w for i,w,f in hits if f==k)
            spelling=min(typed,key=lambda w:(-typed[w],next(i for i,s,f in hits if s==w),w))
            selection=dict(famille=k, graphie=spelling, compte=counts[k], notices=df[k],
                           rangs=[i for i,w,f in hits if f==k])
        else: selection=None
        out[panel]={"notice_source":title,"degre":degree(words[:80]),"anatomie":selection}
    return {"source_sha256":sha256(SOURCE.read_bytes()).hexdigest(),"pages":out}


def verify():
    announced=json.loads((HERE/"ANNONCES.json").read_bytes())["pages"]
    trans=json.loads((HERE/"TRANSCRIPTION.json").read_bytes())
    found={}
    matrix={}
    for k,v in trans.items():
        ws=v["mots"].split()
        assert len(ws)<=40
        grades=v["degres_qualites"]
        assert all(w in ws and ordinal(w) for w in grades)
        found[k]={"degre":{"graphie":grades[0],"valeur":ordinal(grades[0])} if grades else None,
                  "tous_degres":grades,"termes":[[i+1,w,family(w)] for i,w in enumerate(ws) if family(w)],
                  "mots":len(ws)}
    for ref,pred in announced.items():
        line={}
        for target,read in found.items():
            d,dd=pred["degre"],read["degre"]
            a=pred["anatomie"]
            line[target]={
                "degre":None if not d else bool(dd and dd["valeur"]==d["valeur"]),
                "ordinal_exact":None if not d else bool(dd and dd["graphie"]==d["graphie"]),
                "valeur_citee":None if not d else any(ordinal(w)==d["valeur"] for w in read["tous_degres"]),
                "organe":None if not a else any(t==a["famille"] for _,w,t in read["termes"]),
                "mot_exact":None if not a else a["graphie"] in trans[target]["mots"].split()}
        matrix[ref]=line
    stats={}
    for criterion in ("degre","ordinal_exact","valeur_citee","organe","mot_exact"):
        panel=list(PANELS)
        def score(order):
            return sum(matrix[k][other][criterion] is True for k,other in zip(panel,order))
        observed=score(panel)
        distrib=Counter(score(order) for order in permutations(panel))
        stats[criterion]={"justes":observed,"annonces":sum(matrix[k][k][criterion] is not None for k in panel),
                          "permutations":sum(distrib.values()),"aussi_bonnes":sum(n for s,n in distrib.items() if s>=observed),
                          "moyenne":sum(s*n for s,n in distrib.items())/sum(distrib.values())}
    return {"lectures":found,"matrice":matrix,"scores":stats}


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("action",choices=["annoncer","verifier"])
    a=p.parse_args().action
    write(HERE/("ANNONCES.json" if a=="annoncer" else "RESULTATS.json"), announce() if a=="annoncer" else verify())
