"""Masquer le d initial des deux graphies d'une légende reprise dans la prose."""
from collections import Counter, defaultdict
import argparse
import json
from suffixe import corpus, metadata, strict_rows
from corpus_dam import bords
from combiner import HERE, write


def data():
    ed,_=corpus()
    meta=metadata()
    for loc,(page,kind,_,_) in ed["H"].items():
        info=meta.get(page,{})
        if kind!='P0':
            continue
        if info.get("Q")=="T":
            lot="dernier_cahier"
        elif (info.get("H"),info.get("L"),info.get("I")) in (("2","B","H"),("2","B","B")):
            lot="herbier" if info["I"]=="H" else "bains"
        else:
            continue
        for block,i,word,edges in strict_rows(ed,loc,info.get('I',''),Counter()):
            yield f"{loc}/{block}/{i}",page,lot,word,edges


def announce():
    mask = {k:{"lot":lot,"debut":"debut" in edges,
               "annonce":"dshedy" if "debut" in edges else "shedy"}
            for k,_,lot,w,edges in data() if lot!="bains" and w in ("dshedy","shedy")}
    write("DEBUT-ANNONCES.json",mask)


def verify():
    mask=json.loads((HERE/"DEBUT-ANNONCES.json").read_bytes())
    measures=defaultdict(lambda:defaultdict(Counter))
    totals=defaultdict(Counter)
    strata=defaultdict(lambda:defaultdict(lambda:[0,0,0,0]))
    from_mask={}
    for key,page,lot,w,edges in data():
        if w in ("dshedy","shedy"): name=w
        elif w.endswith('edy'): name="autres_edy"
        else: name="reste"
        totals[lot][name]+=1
        for e in edges:
            measures[lot][e][name]+=1
        if w in ("dshedy","shedy") and lot!="bains":
            assert (mask[key]["annonce"]=="dshedy")==("debut" in edges)
            from_mask[key] = {**mask[key],"lecture":w,"positions":sorted(edges)}
        if ("debut" in edges or "interieur" in edges) and name!="reste":
            for control in ["shedy","autres_edy"]:
                if name=="dshedy" or name==control:
                    idx=(0 if "debut" in edges else 2)+(0 if name=="dshedy" else 1)
                    strata[lot+"/"+control][page][idx]+=1
    assert from_mask.keys()==mask.keys()
    exact={}
    for name,cols in strata.items():
        d=bords.margins(list(cols.values()))
        exact[name]={"groupes_informatifs":d["strates_informatives"],
                     "d_observes":d["courts_bord_observes"],"d_attendus":d["courts_bord_attendus"],
                     "p_unilateral":d["p_superieur_ou_egal"],"par_face":cols}
    write("DEBUT-RESULTATS.json",{"accords":from_mask,"par_position":measures,
                                  "totaux":totals,"controle":exact})


if __name__=="__main__":
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['annoncer','verifier'])
    announce() if p.parse_args().mode=='annoncer' else verify()
