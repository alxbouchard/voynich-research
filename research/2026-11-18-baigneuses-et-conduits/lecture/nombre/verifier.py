"""Examiner les voisins de deux mots dans la prose et dans des couples témoins."""
from collections import Counter, defaultdict
from functools import lru_cache
from hashlib import sha256
import re
import sys
from pathlib import Path

from predire import FORMS, HERE, TARGET, entries, line_words, ref, write
from transfert import corpus, langage, spellings, tokens

SIDES = (-1,1)
PROSE = {"P0","P1","Pb","Pc","Pr","Pt"}
BREAK = re.compile(r"<[-~]>|<![^>]*(?:gap|space|jump)[^>]*>",re.I)


def build():
    editions,_ = corpus()
    meta = {}
    for row in (langage.DATA/"ZL3b-n.txt").read_text().splitlines():
        page = re.match(r"^<([^.,>]+)>",row)
        if page:
            attrs=dict(re.findall(r"\$(\w)=(\w+)",row))
            if "Q" in attrs and "B" in attrs:
                meta[page[1]]=attrs["Q"]+"/"+attrs["B"]
    result=[]
    freq=Counter()
    for loc in sorted(set.union(*(set(x) for x in editions.values()))):
        face=loc.split(".")[0]
        if re.fullmatch(r"f(?:75|84)[rv]\d*",face): continue
        lines=[rows.get(loc) for rows in editions.values()]
        kinds={r[1] if r else None for r in lines}
        kind=next(iter(kinds)) if len(kinds)==1 else "disaccord"
        versions=[]
        for row in lines:
            for cut in ("joints","separes"):
                seq=[]
                if row:
                    for i,part in enumerate(BREAK.split(row[3])):
                        if i:seq.append(None)
                        seq.extend(tokens(part,cut))
                versions.append(seq)
        counts=[Counter(seq) for seq in versions]
        common={w:n for w,n in counts[0].items() if w and re.fullmatch("[a-z]+",w)
                and all(c[w]==n for c in counts[1:])}
        if kind in PROSE: freq.update(common)
        result.append((loc,meta.get(face),kind,versions,common))
    return result,freq


def seen(lines, pair):
    counts={w:Counter() for w in pair}
    rows=[]
    for loc,bif,kind,vers,agreed in lines:
        for form,w in zip(FORMS,pair):
            spans=[[i for i,t in enumerate(seq) if t==w] for seq in vers]
            if not any(spans):continue
            prose=kind in PROSE
            prefix="prose" if prose else "autre"
            ct=counts[w]
            ct[prefix+"_loci_au_moins_une_lecture"]+=1
            if not agreed.get(w):
                ct[prefix+"_loci_non_concordants"]+=1
                continue
            for j in range(agreed[w]):
                ct[prefix+"_occurrences"]+=1
                item={"lieu":loc,"rang_occurrence":j+1,"bifeuillet":bif,"type":kind,
                      "mot":w,"forme":form,"voisins":{}}
                for side in SIDES:
                    vals=[]
                    for seq,where in zip(vers,spans):
                        k=where[j]+side
                        vals.append(seq[k] if 0<=k<len(seq) else None)
                    v=vals[0]
                    if v and len(set(vals))==1 and re.fullmatch("[a-z]+",v):
                        item["voisins"][str(side)]=v
                        ct[prefix+"_voisins_lisibles"]+=1
                rows.append(item)
    return counts,rows


def controls(freq):
    true=tuple(TARGET)
    bases=[w for w in freq if w+"y" in freq and w!=true[0]]
    def delta(w):
        return abs(freq[w]-freq[true[0]])+abs(freq[w+"y"]-freq[true[1]])
    return [(w,w+"y") for w in sorted(bases,key=lambda w:(delta(w),w))[:10]]


def lexicon(rows,exclude=None):
    lib=defaultdict(set)
    for v in rows:
        if v["annonce"] and v["notice"]!=exclude:
            lib[v["forme"],v["cote"]].add(v["voisin"])
    return lib


def other(form):
    return FORMS[1-FORMS.index(form)]


@lru_cache(None)
def possible(eva,clear,mapping):
    key=dict(mapping)
    signs=ref.transformed(eva,"o")
    if not signs or not len(signs)<=len(clear)<=2*len(signs):return ()
    return tuple(tuple(sorted((s,v) for s,v in k.items() if s not in key))
                 for k in ref.tables(signs,clear,2,key))


def evaluate(sites,keys,lib,detail=False):
    summary=Counter()
    matches=[]
    for s in sites:
        if s["type"] not in PROSE:continue
        for d,eva in s["voisins"].items():
            d=int(d); f=s["forme"]
            summary["voisins_concordants"]+=1
            signs=ref.transformed(eva,"o")
            flag=Counter()
            if detail:s.setdefault("decodages_par_cote",{})[str(d)]=[]
            for i,key in enumerate(keys):
                spelling=ref.decode(signs,key)
                if spelling:flag["decodable"]+=1
                for name,txt,side in (("direct",f,d),("nombre_echange",other(f),d),("cote_echange",f,-d)):
                    if spelling in lib[txt,side]:
                        flag[name]+=1
                        matches.append(dict(lieu=s["lieu"],bifeuillet=s["bifeuillet"],forme=f,
                                            eva=eva,cote=d,lecture=spelling,cle=i+1,comparaison=name))
                if detail:s["decodages_par_cote"][str(d)].append(spelling)
                for name,txt in (("direct",f),("nombre_echange",other(f))):
                    if any(possible(eva,c,tuple(key.items())) for c in lib[txt,d]):
                        flag["compatible_"+name]+=1
            for name in flag:summary[name]+=1
    for name in ("voisins_concordants","decodable","direct","nombre_echange","cote_echange","compatible_direct","compatible_nombre_echange"):
        summary.setdefault(name,0)
    return {"comptes":summary,"correspondances_completes":matches}


def augmented(rows,keys,lib,swapped=False):
    discovered=defaultdict(list)
    for s in rows:
        if s["type"] not in PROSE or (ord(s["bifeuillet"][0])-64)%2!=1:continue
        for side,w in s["voisins"].items():
            side=int(side)
            f=other(s["forme"]) if swapped else s["forme"]
            units=set(ref.transformed(w,"o"))
            for i,k in enumerate(keys):
                if len(units-k.keys())!=1:continue
                for clear in sorted(lib[f,side]):
                    for mapping in possible(w,clear,tuple(k.items())):
                        assert len(mapping)==1
                        term=(i, *mapping[0])
                        record={"lieu":s["lieu"],"forme":f,"cote":side,"mot":w,"latin":clear}
                        if record not in discovered[term]: discovered[term].append(record)
    return [{"cle":k+1,"signe":s,"valeur":v,"origines":l} for (k,s,v),l in sorted(discovered.items())]


def confirm(rows,keys,lib,calls,swapped=False):
    hits=[]
    for s in rows:
        if s["type"] not in PROSE or (ord(s["bifeuillet"][0])-64)%2!=0:continue
        f=other(s["forme"]) if swapped else s["forme"]
        for d,w in s["voisins"].items():
            d=int(d); signs=ref.transformed(w,"o")
            for call in calls:
                if call["signe"] not in signs:continue
                key=keys[call["cle"]-1]|{call["signe"]:call["valeur"]}
                latin=ref.decode(signs,key)
                if latin not in lib[f,d]:continue
                valid=[a for a in call["origines"] if a["forme"]!=f and a["latin"]!=latin
                       and (latin not in lib[other(f),d] or a["latin"] not in lib[f,a["cote"]])]
                if valid:
                    hits.append(dict(lieu=s["lieu"],bifeuillet=s["bifeuillet"],forme=f,cote=d,
                                     mot=w,latin=latin,cle=call["cle"],signe=call["signe"],
                                     valeur=call["valeur"],origines=valid))
    return hits


def calibration(chapters,ref_rows):
    # Alphabet de remplacement fixe, charactères opaques séparés du latin par 7 pas.
    alphabet="abcdefghijklmnopqrstuvwxyz"
    shift=lambda w,delta:"".join(alphabet[(alphabet.index(c)+delta)%26] for c in w)
    code=[[[shift(w,7) for w in line] for line in ch] for ch in chapters]
    announced={(a["notice"],a["vers"],a["rang_cible"],a["cote"]) for a in ref_rows if a["annonce"]}
    out=Counter(); details=[]
    for i,chapter in enumerate(code):
        whole=lexicon(ref_rows); apart=lexicon(ref_rows,i)
        for j,line in enumerate(chapter,1):
            for k,t in enumerate(line,1):
                if t not in {shift(f,7) for f in FORMS}: continue
                f=shift(t,-7)
                for d in SIDES:
                    if (i,j,k,d) not in announced:continue
                    clear=shift(line[k-1+d],-7)
                    out["possibles"]+=1
                    for name,family,form,word in [("correct",whole,f,clear),("nombre_echange",whole,other(f),clear),
                        ("mauvaise_cle",whole,f,shift(clear,1)),("notice_retiree",apart,f,clear),
                        ("notice_retiree_nombre_echange",apart,other(f),clear)]:
                        if word in family[form,d]:out[name]+=1
                    if clear in apart[f,d]:details.append({"notice":i,"vers":j,"forme":f,"voisin":clear,"cote":d})
    assert out["correct"]==out["possibles"]==len(announced)
    for name in ("correct","nombre_echange","mauvaise_cle","notice_retiree","notice_retiree_nombre_echange"):
        out.setdefault(name,0)
    return {"scores":out,"recouvrements_hors_notice":details}


def run(mode,folder):
    initial=ref.read(HERE/"ATTENTES.json")
    lib=lexicon(initial["voisins"]); keys=[q["table"] for q in initial["cles"]]
    lines,freq=build()
    pairs=[tuple(TARGET),*controls(freq)]
    plans={}
    inventories={}
    for pair in pairs:
        name="/".join(pair)
        counts,sites=seen(lines,pair)
        assert [counts[w]["prose_occurrences"] for w in pair]==[freq[w] for w in pair]
        inventories[name]=counts,sites
        if mode=="apprendre":
            plans[name]={"frequences":[freq[w] for w in pair],
                         "direct":augmented(sites,keys,lib),"echange":augmented(sites,keys,lib,True)}
    if mode=="apprendre":
        write("PREDICTIONS-EXTENSION.json",plans); return
    assert mode=="verifier"
    plans=ref.read(HERE/"PREDICTIONS-EXTENSION.json")
    assert list(plans)==list(inventories)
    result={}
    for name,(counts,sites) in inventories.items():
        f=plans[name]
        main=name=="/".join(TARGET)
        cases=evaluate(sites,keys,lib,detail=main)
        result[name]={"frequences":f["frequences"],"couverture":counts,"lecture":cases,
                      "apprises":[len(f["direct"]),len(f["echange"])],
                      "confirmation":confirm(sites,keys,lib,f["direct"]),
                      "confirmation_nombre_echange":confirm(sites,keys,lib,f["echange"],True)}
        if main:write("LIEUX.json",sites)
    support=[sorted({w for words in lib.values() for w in words if ref.encodable(w,key)}) for key in keys]
    raw_spellings={}
    for k,usable in zip(keys,support):
        for latin in usable:
            for sig in spellings(latin,k):
                for word in ("".join(sig),"o"+"".join(sig)):
                    if ref.transformed(word,"o")==sig:raw_spellings[word]=dict(latin=latin,occurrences_prose=freq[word])
    discrepancies=[]
    for loc,bif,kind,versions,common in lines:
        for word in TARGET:
            n=[seq.count(word) for seq in versions]
            if any(n) and word not in common:
                discrepancies.append(dict(lieu=loc,bifeuillet=bif,type=kind,forme=word,
                                          H_joint=n[0],H_separe=n[1],ZL_joint=n[2],ZL_separe=n[3]))
    write("ECARTS.json",discrepancies)
    write("RESULTATS.json",dict(portee_par_cle=support,graphies_theoriques=raw_spellings,latin_chiffre=calibration(line_words(folder),initial["voisins"]),
          couples=result,sha_attentes=sha256((HERE/"ATTENTES.json").read_bytes()).hexdigest(),
          sha_augmentations=sha256((HERE/"PREDICTIONS-EXTENSION.json").read_bytes()).hexdigest()))


if __name__=="__main__":
    run(sys.argv[1],Path(sys.argv[2]))
