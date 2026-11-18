"""Rechercher les groupes annoncés, sans réordonner les mots dans un passage."""
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent
MONDE = {"wein","weyn"}
MIT = {"mit","mitt"}
CUIT = {"gesoten","gesotten"}
QUALITES = {"VII_RIDGES":{"wild","wilden","wilde","wildem","wilder"},
            "VIII_lecture_photo":{"garten","gartten","gart","gartem"}}


def count(texts, kind):
    hits = []
    cooking = 0
    for place, words in texts:
        cooks = [n for n,w in enumerate(words) if w in CUIT]
        cooking += len(cooks)
        for n,(a,b) in enumerate(zip(words, words[1:])):
            if a not in MIT or b not in MONDE:
                continue
            nearby = [m for m in cooks if n-9 <= m <= n+10]
            qualifying = [i for i,word in enumerate(words) if word in QUALITES.get(kind,set())
                          and any(abs(i-j)<=9 for j in [n,n+1]+nearby)]
            named = [i for i,word in enumerate(words) if ("eppich" in word or "epich" in word)
                     and any(abs(i-j)<=9 for j in [n,n+1]+nearby)]
            hits.append({"lieu":place, "rang_mit":n+1, "cuisson_aux_rangs":[j+1 for j in nearby],
                         "qualificatif":[i+1 for i in qualifying],"eppich_proche":[i+1 for i in named],
                         "extrait":words[max(n-7,0):n+9]})
    return {"cuisson_dans_corps_transcrit":cooking, "mit_wein":len(hits),
            "passages_conformes":sum(bool(hit["cuisson_aux_rangs"]) for hit in hits),
            "occurrences":hits}


if __name__ == "__main__":
    corpus=json.loads((HERE/"PASSAGES.json").read_bytes())
    print(json.dumps({kind:count(texts,kind) for kind,texts in corpus.items()},
                     ensure_ascii=False,indent=1))
