"""Vérifier le troisième mot dans les quatre traitements de l'espace."""
from pathlib import Path
from collections import Counter
import json,sys
from transfert_cle import collect,windows,segment
from lire_doublet import HERE, fit,section,read
from corpus_vern import load_book,martino

def main(path):
    rows=read("ANNONCES.json.gz")["martino"]["annonces"]
    key=next(row[4] for row in rows if row[3]=="un_muet")
    book=load_book(martino(path))
    refs=Counter(w[i+2] for ref,w in book if section(ref)!="recette 59"
                 for i in range(len(w)-2) if w[i:i+2]==("in","l"))
    target=next(row for row in windows() if row["lieu"]=="f19r.2/1/2")
    assert target["ancre"]=="chor" and target["suite"][0]=="y"
    signs=segment(target["suite"][1]) if len(target["suite"])==2 else None
    report={"cible":target,"repertoire":refs,"unites_cible":signs}
    if signs is not None:
        report["projection"]="".join(key.get(x,"["+x+"]") for x in signs)
        report["extensions"]={word:list(fit(signs,word,{},key)) for word in refs}
    (HERE/"F19-RESULTAT.json").write_text(json.dumps(report,indent=1,ensure_ascii=False)+"\n")

if __name__=="__main__":main(Path(sys.argv[1]))
