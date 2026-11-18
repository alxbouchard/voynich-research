"""Rechercher le début exact o p ch dans les légendes et les paragraphes."""
from collections import Counter
from pathlib import Path
import json
import re
from reprendre import HERE, RESEARCH, MODES, corpus, agreed, inventory
from compter import segment

SINGLE = RESEARCH/"2026-11-18-deux-legendes-botaniques/lecture/tucker/prefixe/resultats.json"
ANCHORS = {"f89", "f100", "f102"}


def prefix(w):
    return bool(re.fullmatch("[a-z]+",w)) and tuple(segment(w)[:3]) == ("o","p","ch")


def scan(objects):
    certain = {loc: sorted({w for w in words if re.fullmatch("[a-z]+",w)})
               for loc,words in objects.items()}
    return {"total":len(objects),"avec_un_mot_lisible":sum(bool(ws) for ws in certain.values()),
            "trouves":{loc:[w for w in words if prefix(w)] for loc,words in certain.items() if any(map(prefix,words))}}


def main():
    inv = json.loads(SINGLE.read_text())
    data = {"un_mot":{}}
    def subset(rows):
        return {k:v for k,v in rows.items() if re.match("f[0-9]+",k)[0] not in ANCHORS}
    for kind in ("Lf","Ls","Lz","Ln","Lc"):
        record = (inv["Ln_un_locus_par_ligne_sans_reunir_les_paires_de_f75v"]
                  if kind=="Ln" else inv["par_code"][kind])
        words = {loc:[w] for loc,w in record["mots_par_locus"].items()}
        data["un_mot"][kind] = {"tous":scan(words), "reserve":scan(subset(words))}
    _,_,ed = inventory()
    variants = {m:subset({k:ws for p,labels in ed[m][0].items() for k,ws in labels.items()}) for m in MODES}
    all_loci = set.union(*(set(v) for v in variants.values()))
    combined = {loc:sorted(set.intersection(*(set(v.get(loc,())) for v in variants.values()))) for loc in sorted(all_loci)}
    data["legendes_entieres_reserve"] = {"accord":scan(combined), **{"/".join(m):scan(v) for m,v in variants.items()}}
    rows = agreed(corpus()[0])
    words = Counter()
    for loc,ngrams in rows.items():
        for (w,),freq in ngrams[0].items():
            if prefix(w):
                words[w] += freq
    data["prose"] = {"mots":sum(sum(r[0].values()) for r in rows.values()),
                     "occurrences_par_graphie":dict(words)}
    (HERE/"PREFIXE.json").write_text(json.dumps(data,sort_keys=True,ensure_ascii=False,indent=2)+"\n")
    print(data["un_mot"]["Lf"],data["legendes_entieres_reserve"],sum(words.values()))
    print({k:v["tous"] for k,v in data["un_mot"].items() if k!="Lf"})


if __name__=="__main__":
    main()
