"""Geler les réponses calculables depuis les seuls rangs impairs."""
from collections import Counter
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent

def first(field):
    return field.lower().replace("ſ","s").split()[0] if field.strip() else None

def compute(known):
    baseline=[]
    for lang in (0,1):
        counts=Counter(first(pair[lang])[0] for pairs in known.values() for pair in pairs if first(pair[lang]))
        baseline.append(sorted(counts,key=lambda s:(-counts[s],s))[0])
    result={}
    for key,pairs in known.items():
        rows=[]
        for i,pair in enumerate(pairs):
            prediction=[]
            for lang in (0,1):
                word=first(pair[lang])
                r=first(pairs[i+1][lang]) if i+1<len(pairs) else None
                prediction.append({"word":word,"both":word[0] if word and r and word[0]==r[0] else None,"baseline":baseline[lang]})
            rows.append({"rank":2*i+2,"latin":prediction[0],"german":prediction[1]})
        result[key]=rows
    return result

if __name__=="__main__":
    out=compute(json.loads((HERE/"APPRENTISSAGE.json").read_text()))
    (HERE/"PREDICTIONS.json").write_text(json.dumps(out,ensure_ascii=False,indent=1)+"\n")
