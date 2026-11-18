"""Émettre les lectures avant de comparer les quatrièmes mots (deux commandes séparées)."""
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import random
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]/"2026-11-18-d-initial-et-formules/vernaculaire"))
from corpus_vern import sources, fingerprint
from essayer import fit

CODES = (tuple("op")+("ch","e","o","r"), tuple("op")+("ch","e","o","l"),
         ("sh","o","d","y"), ("sh","o","l","d","y"))


def write(file, result):
    raw = (json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":"))+"\n").encode()
    (HERE/file).write_bytes(gzip.compress(raw,mtime=0))


def read(file):
    return json.loads(gzip.decompress((HERE/file).read_bytes()))


def suffixes(a,b):
    for i in range(max(1,len(a)-3,len(b)-3),min(len(a),len(b))+1):
        if a[:i]==b[:i] and a[i:]!=b[i:]:
            yield a[:i],a[i:],b[i:]


def blockkeys(a,b,c):
    for stem,r,l in suffixes(a,b):
        for i in range(1,len(c)):
            yield {"opcheo":stem, "r":r, "l":l, "sho":c[:i], "dy":c[i:]}


def projection(codes,key):
    return "".join(key[c] for c in codes)


@lru_cache(maxsize=8192)
def literal_pairs(a,b):
    tables=[]
    for mute in (None, *sorted(set(CODES[0]+CODES[1]+CODES[2]))):
        keys=[{} if mute is None else {mute:""}]
        for codes,word in zip(CODES,(a,b)):
            keys=[extended for base in keys for extended in fit(codes,word,{},base)]
        for key in keys: tables.append((mute,key))
    return tables


def literal_keys(a,b,c):
    # Les doubles fins de la paire imposent au moins trois lettres initiales communes,
    # même si les deux occurrences de o sont muettes.
    if a[:3]!=b[:3]:return
    for mute, key in literal_pairs(a,b):
        for full in fit(CODES[2],c,{},key):
            yield "signes" if mute is None else "un_muet",full


def windows(book,n):
    for j,(ref,words) in enumerate(book):
        for i in range(len(words)-n+1):
            yield j,i,words


def models(a,b,c):
    for key in blockkeys(a,b,c):
        yield "blocs",key,projection(("sho","l","dy"),key)
    for name,key in literal_keys(a,b,c):
        yield name,key,projection(CODES[3],key)


def train(book):
    all_calls=[]
    starts=0
    for j,i,words in windows(book,4):
        starts+=1
        first=words[i:i+3]
        for name,key,w in models(*first):
            all_calls.append([j,i,list(first),name,key,w])
    return {"fenetres":starts, "sha256":fingerprint(book), "annonces":all_calls}


def check(book,fixed):
    assert fingerprint(book)==fixed["sha256"]
    fourth=defaultdict(Counter)
    for j,i,words in windows(book,4):
        w=words[i+3]
        fourth[len(w)][w]+=1
    by_site=defaultdict(list)
    for j,i,first,mode,key,output in fixed["annonces"]:
        by_site[mode,j,i].append((key,output))
    scores=defaultdict(Counter)
    hits=[]
    for (mode,j,i),calls in by_site.items():
        ref,words=book[j]
        truth=words[i+3]
        outs={w for key,w in calls}
        n=scores[mode]
        n["fenetres_avec_sortie"]+=1
        n["sorties_distinctes_cumulees"]+=len(outs)
        n["tables"]+=len(calls)
        dist=fourth[len(truth)]
        n["attendu_4_de_meme_longueur"]+=sum(dist.get(w,0) for w in outs)/sum(dist.values())
        if truth in outs:
            n["fenetres_correctes"]+=1
            valid=[key for key,w in calls if w==truth]
            n["fenetres_correctes_avec_l_prononce"]+=any(key["l"] for key in valid)
            hits.append(dict(regle=mode,segment=j,ref=ref,rang=i+1,clair=words[i:i+4],
                             sorties_distinctes=len(outs),tables_valides=valid))
    return {"scores":scores,"succes":hits}


def on_transfer(book,k,mode):
    # N'apprendre qu'un radical pour les blocs, k (un signe) pour la table stricte.
    # Exclure la rubrique/recette entière de l'ajustement.
    r,l=k["r"],k["l"]
    value=k["dy"] if mode=="blocs" else k["d"]+k["y"]
    for j,i,words in windows(book,3):
        a,b=words[i:i+2]
        if len(a)<=len(r) or len(b)<=len(l):continue
        if r and not a.endswith(r) or l and not b.endswith(l):continue
        left=a[:len(a)-len(r)] if r else a
        right=b[:len(b)-len(l)] if l else b
        if left!=right:continue
        if mode!="blocs":
            stem=("o","k","e","o")
            if not any(fit(stem,left,{},k)):continue
        yield j,i,left,value


def section(ref):
    return ref.split(" §")[0]


def transfer(book,validated):
    out=[]
    for trial in validated["succes"]:
        for key in trial["tables_valides"]:
            sites=[]
            for j,i,stem,guess in on_transfer(book,key,trial["regle"]):
                ref,words=book[j]
                if section(ref)==section(trial['ref']):continue
                sites.append({"segment":j,"ref":ref,"rang":i+1,"paire":words[i:i+2],
                              "racine_ajoutee":stem,"annonce_historique_de_dy":guess})
            out.append({"mode":trial["regle"],"lieu_f89":[trial["ref"],trial["rang"]],
                        "cle":key,"lieux_independants":sites})
    return out


def open_transfer(book,rows):
    tests=hits=0
    results=[]
    for row in rows:
        for site in row["lieux_independants"]:
            j,i=site["segment"],site["rang"]-1
            words=book[j][1]
            tests+=1
            actual=words[i+2]
            if site["annonce_historique_de_dy"]==actual:
                hits+=1
                results.append({"source89":row["lieu_f89"],"ref":site["ref"],"rang":i+1,
                                "trois":words[i:i+3], "table":row["cle"]})
    return {"combinaisons_table_lieu":tests,"bonnes":hits,"exemples":results}


def positive():
    key={"opcheo":"san","r":"o","l":"i","sho":"st","dy":"a"}
    plain=("sano","sani","sta","stia")
    # Contrôle structurel synthétique, quatre formes italiennes mises bout à bout.
    found=list(blockkeys(*plain[:3]))
    assert key in found and projection(("sho","l","dy"),key)==plain[3]
    return {"artificiel":True,"suite":plain,"cle_attendue":key,"nombre_tables":len(found)}


def positive_book(book):
    letters=sorted(set("".join(w for _,words in book for w in words)))
    symbols=[f"g{i}" for i in range(len(letters))]
    random.Random(8917).shuffle(symbols)
    cipher=dict(zip(letters,symbols))
    for j,i,words in windows(book,4):
        first=words[i:i+3]; fourth=words[i+3]
        if len(fourth)<3 or fourth in first or not set(fourth)<=set("".join(first)):
            continue
        keys=[{}]
        for w in first:
            code=tuple(cipher[c] for c in w)
            keys=[k for base in keys for k in fit(code,w,{s:(1,) for s in symbols},base)]
        assert len(keys)==1
        expected=projection([cipher[c] for c in fourth],keys[0])
        assert expected==fourth
        return {"quartet_original":words[i:i+4],"ref":book[j][0],"rang":i+1,
                "mot_retrouve":expected}
    raise ValueError("aucun quartet de contrôle")


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode",choices=["annoncer","verifier","transfert","ouvrir_transfert"])
    p.add_argument("viandier",type=Path);p.add_argument("martino",type=Path)
    args=p.parse_args()
    corpus=sources(args.viandier,args.martino)
    if args.mode=="annoncer":
        write("ANNONCES.json.gz",{lang:train(book) for lang,book in corpus.items()})
    elif args.mode=="verifier":
        fr=read("ANNONCES.json.gz")
        result={lang:check(book,fr[lang]) for lang,book in corpus.items()}
        result["controle"]=positive()
        result["controle_textes"]={name:positive_book(b) for name,b in corpus.items()}
        (HERE/"OUVERTURE.json").write_text(json.dumps(result,indent=1,ensure_ascii=False)+"\n")
    elif args.mode=="transfert":
        result=json.loads((HERE/"OUVERTURE.json").read_bytes())
        write("TRANSFERT.json.gz",{lang:transfer(book,result[lang]) for lang,book in corpus.items()})
    else:
        tr=read("TRANSFERT.json.gz")
        result={lang:open_transfer(book,tr[lang]) for lang,book in corpus.items()}
        (HERE/"VERIFICATION-TRANSFERT.json").write_text(json.dumps(result,indent=1,ensure_ascii=False)+"\n")


if __name__=="__main__":main()
