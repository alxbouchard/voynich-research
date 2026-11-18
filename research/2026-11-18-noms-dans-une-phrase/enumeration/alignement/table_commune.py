"""Compatibilité d'une table de mots entière entre les deux panneaux pharmaceutiques."""
import json
from aligner import HERE, SEED, EDGES, manuscript, write

def main():
    initial=json.loads((HERE/"PREDICTIONS.json").read_text())
    other=next(r for r in json.loads((HERE/"LOCAL-RESULTATS.json").read_text()) if r["dans_panneaux"])
    page=other["lieu"].split(".")[0]
    gallery,_,_=manuscript()
    counts={}; possibilities={}
    for dataset in initial["etudes"]:
        name=dataset["source"]; spans=dataset["expressions"]; keep=[]
        total=0
        for a in spans:
            for b in spans:
                total+=1
                pairs=list(zip(SEED,a["latins"]))+list(zip(other["mots"],b["latins"]))
                table=dict(pairs)
                if any(table[w]!=v for w,v in pairs) or len(set(table.values()))!=len(table):continue
                reverse={v:w for w,v in table.items()}
                expectations={side:reverse.get(b["voisins_latins"][side]) for side in EDGES}
                keep.append(dict(origine=a["lieu"],cible=b["lieu"],latin_origine=a["latins"],
                    latin_cible=b["latins"],table=table,voisins_que_la_table_peut_lire=expectations))
        counts[name]={"combinaisons_de_positions":total,"compatibles":len(keep),
                      "tables_distinctes":len({tuple(sorted(h["table"].items())) for h in keep})}
        possibilities[name]=keep
    write("TABLE-COMMUNE.json",dict(X_est_une_legende_locale=other["mots"][2] in gallery[page],
          fenetre_autre_panneau=other,comptes=counts,lectures_possibles=possibilities))
if __name__=="__main__":main()
