"""Vérifier dans la prose de la même main l'extension de la finale vue près des figures."""
from collections import Counter, defaultdict
import sys
from combiner import HERE, segment, write
sys.path.insert(0,str(HERE.parent/"2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import corpus, metadata, strict_rows


def main():
    editions,_ = corpus()
    meta = metadata()
    faces = defaultdict(lambda:defaultdict(Counter))
    cover = Counter()
    for loc,(page,kind,_,_) in editions["H"].items():
        info = meta.get(page,{})
        category = info.get("I")
        if kind!="P0" or category not in ("H","B"):
            continue
        key = "/".join(info.get(field,"?") for field in ("I","H","L"))
        row = faces[key][page]
        for _,_,word,_ in strict_rows(editions,loc,category,cover):
            u = tuple(segment(word))
            for field,hit in (("total",True),("edy",u[-3:]==("e","d","y")),
                              ("dshedy",word=="dshedy"),("dolchedy",word=="dolchedy"),
                              ("cinq",len(u)==5),("cinq_edy",len(u)==5 and u[-3:]==("e","d","y"))):
                row[field] += int(hit)
    summary = {}
    for group,records in faces.items():
        usable = [r for r in records.values() if r["total"]]
        total = sum(usable,Counter())
        summary[group] = {**total,"faces_avec_edy":sum(bool(r["edy"]) for r in usable),
                          "faces_avec_prose_lisible":len(usable),"faces_sans_prose_lisible":len(records)-len(usable)}
    write("SUFFIXE.json",{"par_face":faces,"comparaison":summary,"couverture":cover})


if __name__=="__main__":
    main()
