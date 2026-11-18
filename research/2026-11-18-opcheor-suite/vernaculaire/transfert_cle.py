"""Reprendre la seule table de signes donnant trois mots vernaculaires sur f89r2."""
from collections import Counter,defaultdict
from functools import lru_cache
from pathlib import Path
import json, random, re, sys
from lire_doublet import HERE, fit, read, section
from corpus_vern import load_book,martino
sys.path.insert(0,str(HERE.parents[1]/"2026-11-18-d-initial-et-formules"))
from suites import windows,segment


def collect(key):
    types=defaultdict(list)
    for row in windows():
        if re.match(r"f89[rv]",row["page"]):continue
        words=(row["ancre"],*row["suite"])
        for n in range(1,len(words)+1):
            seq=words[:n]
            if not all(set(segment(w))<=key.keys() for w in seq):break
            types[seq].append(row["lieu"])
    return types


def lexicon(book):
    return {n:{tuple(words[i:i+n]) for ref,words in book
               for i in range(len(words)-n+1)} for n in (1,2,3)}


def evaluate(types,mapping,lex,examples=False):
    @lru_cache(maxsize=None)
    def decode(w):
        return "".join(mapping[x] for x in segment(w))
    counts=Counter()
    hits=defaultdict(list)
    for seq,sites in types.items():
        translated=tuple(decode(w) for w in seq)
        if translated in lex[len(seq)]:
            counts[len(seq)]+=len(sites)
            if examples:
                hits[len(seq)].append({"eva":seq,"italien":translated,"effectif":len(sites),
                                      "exemple":sites[0]})
    return {"attestes":dict(counts),"exemples":{n:sorted(items,key=lambda row:-row["effectif"])[:15]
                                                for n,items in hits.items()}}


def targeted(book,mapping):
    matches=[]
    for ref,words in book:
        for i in range(len(words)-1):
            a,b=words[i:i+2]
            candidates=list(fit(segment("okeor"),a,{},mapping))
            for candidate in candidates:
                if "".join(candidate[x] for x in segment("okeol"))!=b:continue
                _,_,*tail=words[i:i+3]
                matches.append({"ref":ref,"rang":i+1,"paire":[a,b],"k":candidate["k"],
                                "troisieme_predit":"ol","mot_suivant":next(iter(tail),None)})
    return matches


def main(path):
    ann=read("ANNONCES.json.gz")
    rows=[row for spec in ann.values() for row in spec["annonces"] if row[3]!="blocs"]
    assert len(rows)==1
    mapping=rows[0][4]
    book=[(ref,words) for ref,words in load_book(martino(path)) if section(ref)!="recette 59"]
    types=collect(mapping);lex=lexicon(book)
    rng=random.Random(891716)
    alphabet=sorted(mapping); vals=[mapping[g] for g in alphabet]
    perm={tuple(vals)}
    sims=[]
    while len(sims)<199:
        rng.shuffle(vals)
        if tuple(vals) in perm:continue
        perm.add(tuple(vals))
        result=evaluate(types,dict(zip(alphabet,vals)),lex)["attestes"]
        sims.append([result.get(n,0) for n in (1,2,3)])
    counts=Counter()
    for seq,sites in types.items():counts[len(seq)]+=len(sites)
    result={"entrees_avec_valeur_pour_chaque_signe":counts,
            "f100v_16":targeted(book,mapping),"prose":evaluate(types,mapping,lex,True),
            "temoins":sims,"mots_italiens_de_reference":sum(len(w) for _,w in book)}
    (HERE/"CLE-TRANSFERT.json").write_text(json.dumps(result,indent=1,ensure_ascii=False)+"\n")
if __name__=="__main__":main(Path(sys.argv[1]))
