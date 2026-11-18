"""Comparer les entrées cachées à la prédiction figée et aux autres ordres."""
from collections import Counter
from pathlib import Path
import json
from predire import first

HERE=Path(__file__).resolve().parent
ROOTS={"718-g":42,"718-d":84,"719-g":128,"719-d":171}

def load(name):
    return json.loads((HERE/name).read_text())

def save(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n")

def main():
    odd,even,pred=load("APPRENTISSAGE.json"),load("RESERVE.json"),load("PREDICTIONS.json")
    changes=load("RELECTURE.json")
    inventory=[]
    report={}
    for column, initial_chapter in ROOTS.items():
        for j in range(24):
            latin,german=(even if j%2 else odd)[column][j//2]
            entry=dict(colonne=column,rang=j+1,chapitre=initial_chapter+j,latin=latin,allemand=german)
            for correction in changes:
                if (column,j+1)==(correction["colonne"],correction["rang"]):
                    for field,val in correction["lecture"].items():
                        entry[field]=val
            inventory.append(entry)
    save("NOMS.json",inventory)
    for lang,field in [("latin","latin"),("german","allemand")]:
        scores={m:Counter() for m in ("un","deux","mot","majoritaire","deux_voisins")}
        order=Counter()
        misses=[]
        target_words=Counter()
        for column in ROOTS:
            rows=[r for r in inventory if r["colonne"]==column]
            forms=[first(r[field]) for r in rows]
            for i,row in enumerate(rows):
                form=forms[i]
                if i!=0 and form and forms[i-1]:
                    prev=forms[i-1];order["adjacentes"]+=1
                    order["croissant_ou_egal"]+=int(prev<=form)
                    order["initiale_non_decroissante"]+=int(prev[0]<=form[0])
                    order["initiales_identiques"]+=int(prev[0]==form[0])
                    order["meme_initiale_croissant_ou_egal"]+=int(prev[0]==form[0] and prev<=form)
                if i%2!=1 or not form:
                    continue
                r=pred[column][i//2][lang]
                word=r["word"]
                target_words[form[0]]+=1
                for metric,guess,wanted in (
                    ("un",word[:1] if word else None,form[:1]),
                    ("deux",word[:2] if word else None,form[:2]),
                    ("mot",word,form),
                    ("majoritaire",r["baseline"],form[:1]),
                    ("deux_voisins",r["both"],form[:1]),
                ):
                    if guess is not None:
                        scores[metric]["appels"]+=1
                        scores[metric]["justes"]+=int(guess==wanted)
                        if metric=="un" and guess!=wanted:misses.append(dict(chapitre=row["chapitre"],predit=guess,lu=form))
        report[lang]=dict(scores=scores,ordre=order,erreurs_initiale=misses,initiales_reserve=target_words)
    save("RESULTATS.json",report)
    return report

if __name__=="__main__":
    report=main()
    for lang,data in report.items():print(lang,data["scores"],data["ordre"],data["initiales_reserve"])
