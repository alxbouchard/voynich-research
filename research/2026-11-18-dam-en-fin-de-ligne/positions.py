"""Contrôler les marges d’écriture avec les bases, longueurs et faces fixées."""
from collections import Counter, defaultdict
from corpus_dam import bords, corpus, metadata, save, segment, strict_rows


def tabulate():
    editions, _ = corpus()
    meta = metadata()
    coverage = Counter()
    roles = defaultdict(Counter)
    strata = defaultdict(lambda:defaultdict(lambda:[0,0,0,0]))
    for loc,(page,kind,_,_) in editions["H"].items():
        if kind != "P0":
            continue
        for _,_,word,edges in strict_rows(editions,loc,meta.get(page,{}).get("I",""),coverage):
            glyphs = segment(word)
            end = "fin" in edges
            dam = len(glyphs)>3 and glyphs[-3:]==("d","a","m")
            dar = len(glyphs)>3 and glyphs[-3:]==("d","a","r")
            daiin = len(glyphs)>5 and glyphs[-5:]==("d","a","i","i","n")
            am = glyphs[-2:]==("a","m")
            for edge in edges:
                counts = roles[edge]
                counts["positions"] += 1
                for label,test in (("long_dam",dam),("long_dar",dar),("long_daiin",daiin),
                                   ("autres_am",am and not dam),("autres_m",glyphs[-1]=="m" and not am),
                                   ("dam",word=="dam"),("dar",word=="dar"),("daiin",word=="daiin")):
                    counts[label]+=int(test)
            for boundary in ("fin","avant"):
                if boundary not in edges and "interieur" not in edges:
                    continue
                at_edge = boundary in edges
                tests = []
                if dam or dar:
                    tests.append(("dam_contre_dar",(page,tuple(glyphs[:-1])),dam))
                if dam or daiin:
                    base = glyphs[:-1] if dam else glyphs[:-3]
                    tests.append(("dam_contre_daiin",(page,tuple(base)),dam))
                if am:
                    tests.append(("dam_parmi_am",(page,len(glyphs)),dam))
                if word in ("dam","daiin"):
                    tests.append(("mots_dam_daiin",(page,),word=="dam"))
                for name,key,hit in tests:
                    idx = (0 if at_edge else 2)+(0 if hit else 1)
                    strata[name+"/"+boundary][key][idx] += 1
    controls = {}
    for name, group in strata.items():
        # La routine historique nomme « courts » les formes de la première colonne.
        raw = bords.margins(list(group.values()))
        controls[name]={"strates":len(group),"informatives":raw["strates_informatives"],
                        "marges":dict(raw["marges_informatives"]),
                        "dam_observes":raw["courts_bord_observes"],
                        "dam_attendus":raw["courts_bord_attendus"],
                        "p_unilateral":raw["p_superieur_ou_egal"]}
    save("POSITIONS.json",{"positions":roles,"controle":controls,"couverture":coverage})


if __name__=="__main__":
    tabulate()
