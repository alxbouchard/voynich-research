"""Prédire la place d’une graphie de légende en admettant une variation médiane."""
from argparse import ArgumentParser
from collections import Counter
from functools import lru_cache
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

HOME_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(HOME_DIR.parent))
from formules import folio, load, scan
from comparer import permutation_distribution

PROTOCOL = "a0b9f86639df26bc3b555cd370bc015dddada07a879613756a1d9923403759ff"


def write(filename, value):
    (HOME_DIR/filename).write_text(json.dumps(value,ensure_ascii=False,indent=1,sort_keys=True)+"\n")


@lru_cache(None)
def units(word):
    return tuple(re.findall(r"c[kptf]h|ch|sh|.",word))


def edits(left, right):
    if left == right:
        return []
    candidates=[]
    for i in range(2,min(len(left),len(right))-1):
        if left[:i] != right[:i]:
            break
        for j in range(max(2,5-i,len(left)-i-2,len(right)-i-2),
                       min(len(left),len(right))-i+1):
            if left[-j:] == right[-j:]:
                candidates.append(dict(debut="".join(left[:i]),fin="".join(left[-j:]),
                    legende="".join(left[i:len(left)-j]),prose="".join(right[i:len(right)-j])))
    return candidates


@lru_cache(None)
def match(label, word, relaxed):
    return word==label or bool(relaxed and edits(units(label),units(word)))


def index(labels, words, relaxed):
    return {p:{w:sorted(a for a in forms if match(a,w,relaxed)) for w in words}
            for p,forms in labels.items()}


def scored(rule, calls, lexicon, old_words=(), old_names=()):
    out=[]
    for r in calls:
        p,w=r["panneau"],r["cible"]
        names=[] if w is None or w==rule[0] else lexicon[p][w]
        new_names=[n for n in names if n not in old_names] if w not in old_words else []
        out.append(dict(r,noms=names,noms_nouveaux=new_names))
    return out


def marked(rows, new=False):
    tag="noms_nouveaux" if new else "noms"
    return [(folio(r["panneau"]),r["cible"],name)
            for r in rows for name in r[tag]]


def distinct(witnesses):
    return any(p!=q and w!=v and a!=b for i,(p,w,a) in enumerate(witnesses)
               for q,v,b in witnesses[i+1:])


def choose(pages,labels,lines,relaxed):
    calls=scan(pages,lines,1)
    words={r["cible"] for rs in calls.values() for r in rs} - {None}
    lex=index(labels,words,relaxed)
    models=[]
    for rule,positions in calls.items():
        rows=scored(rule,positions,lex)
        hits=[r for r in rows if r["noms"]]
        if not hits:
            continue
        marks=marked(hits)
        names=sorted({n for _,_,n in marks})
        leaves=sorted({p for p,_,_ in marks})
        learned_words=sorted({w for _,w,_ in marks})
        models.append(dict(regle=list(rule),appels=len(rows),justes=len(hits),
                    feuillets=leaves,noms=names,mots=learned_words,admis=distinct(marks),
                    exemples=[dict(lieu=r["locus"],mot=r["cible"],legendes={n:labels[r["panneau"]][n]
                                    for n in r["noms"]}) for r in hits]))
    def rank(r):
        return (-len(r["feuillets"]),-len(r["noms"]),-Fraction(r["justes"],r["appels"]),-r["justes"])
    models.sort(key=lambda r:(rank(r),r["regle"]))
    choices={}
    for mode,options in (("strict",[r for r in models if r["admis"]]),("permissif",models)):
        model=options[0] if options else None
        ties=[r["regle"] for r in options if rank(r)==rank(model)] if model else []
        choices[mode]=dict(modele=model,ex_aequo=ties)
    return models,choices


def prepare(q,groups,captions,lines):
    result={}
    for relaxed in (False,True):
        models,choices=choose(groups[q],captions(groups[q]),lines,relaxed)
        eligible={tuple(r["regle"]) for r in models}
        calls=scan(groups[34-q],lines,1,masked=True)
        positions=[dict(regle=list(rule),positions=calls[rule]) for rule in sorted(eligible)]
        result["variation" if relaxed else "exact"]=dict(modeles=models,choix=choices,appels=positions)
    write(f"PREDICTIONS-{q}.json",result)


def compare(labels,lex,rule,rows,model,matrix):
    data=[]
    for r in rows:
        p,w=r["panneau"],r["cible"]
        if w is None or w==rule[0]:
            continue
        if w not in model["mots"]:
            for s in labels:
                matrix[p][s]+=any(n not in model["noms"] for n in lex[s][w])
        if r["noms"]:
            data.append(dict(lieu=r["locus"],rangs=r["rangs"],cible=w,
                noms_nouveaux=r["noms_nouveaux"],correspondances=[dict(nom=n,lieux=labels[p][n],
                decoupages=edits(units(n),units(w))) for n in r["noms"]]))
    return data


def perm(pages,matrix):
    hist=permutation_distribution(pages,matrix)
    actual=sum(matrix[p][p] for p in pages)
    return dict(n=actual,total=hist.total(),egal_ou_plus=sum(c for n,c in hist.items() if n>=actual),
                attendus=str(Fraction(sum(n*c for n,c in hist.items()),hist.total())),
                histogramme=dict(hist))


def verify(q,groups,captions,lines):
    data=json.loads((HOME_DIR/f"PREDICTIONS-{q}.json").read_text())
    out={}
    pages=groups[34-q]
    labels=captions(pages)
    variants=scan(pages,lines,1)
    words={r["cible"] for calls in variants.values() for r in calls} - {None}
    for case,train in data.items():
        lex=index(labels,words,case=="variation")
        summary=[]
        expected={tuple(s["regle"]):s["positions"] for s in train["appels"]}
        pooled={p:dict.fromkeys(pages,0) for p in pages}
        for model in train["modeles"]:
            rule=tuple(model["regle"])
            rows=scored(rule,variants[rule],lex,model["mots"],model["noms"])
            assert [{k:r[k] for k in ("panneau","locus","rangs")} for r in rows]==expected[rule]
            matrix={p:dict.fromkeys(pages,0) for p in pages}
            found=compare(labels,lex,rule,rows,model,matrix)
            for p in pages:
                for s in pages:
                    pooled[p][s]+=matrix[p][s]
            test=perm(pages,matrix)
            yes=distinct(marked(rows,True)) and 20*test["egal_ou_plus"] <= test["total"]
            summary.append(dict(regle=rule,appels=len(rows),lisibles=sum(r["cible"] is not None for r in rows),
                reprises=len(found),reprises_nouvelles=sum(bool(r["noms_nouveaux"]) for r in rows),
                une_inscription=sum(sum(len(v["lieux"]) for v in r["correspondances"])==1 for r in found),
                candidats_ambigus=sum(len(r["correspondances"])>1 for r in found),
                exemples=found,permutations_nouvelles=test,critere_rempli=yes))
        choices={}
        for mode,item in train["choix"].items():
            m=item["modele"]
            if m is None:
                choices[mode]=None
                continue
            chosen=next(s for s in summary if list(s["regle"])==m["regle"])
            rows=scored(tuple(m["regle"]),variants[tuple(m["regle"])],lex,m["mots"],m["noms"])
            choices[mode]=dict(chosen,positions_et_cibles=rows)
        out[case]=dict(choix=choices,tous_modeles=summary,permutation_ensemble=perm(pages,pooled),
                       graphies_eligibles_par_panneau={p:len(v) for p,v in labels.items()})
    write(f"VERIFICATION-{q}.json",out)


if __name__=="__main__":
    assert sha256((HOME_DIR/"PROTOCOLE.md").read_bytes()).hexdigest()==PROTOCOL
    german=edits(tuple("rosenmaryn"),tuple("rosamaryn"))
    assert dict(debut="ros",fin="maryn",legende="en",prose="a") in german
    assert match("chody","chody",False)
    assert not edits(units("chol"),units("chal"))
    parser=ArgumentParser()
    parser.add_argument("operation",choices=["predire","verifier"])
    parser.add_argument("cahier",type=int,choices=[15,19])
    args=parser.parse_args()
    groups,captions,lines=load()
    if args.operation=="predire":
        prepare(args.cahier,groups,captions,lines)
    else:
        verify(args.cahier,groups,captions,lines)
