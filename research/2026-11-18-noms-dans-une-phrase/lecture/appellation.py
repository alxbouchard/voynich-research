"""Appellation autour du mot d’une étiquette repris en prose."""
from collections import Counter, defaultdict
import csv
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[1]
sys.path.insert(0,str(RESEARCH/"2026-11-18-gestes-des-bains/formule"))
from epreuve import cipher, extend, parse, ref
from transfert import corpus, labels, langage
SIMPLE=re.compile(r"[a-z]+")
NAMES={"Urtica":("urticam",115), "Acidula":("acidulam",711), "Enula":("enula",1489)}
HIST=RESEARCH/"2026-11-18-opcheor-paralleles/latin"


def write(name,obj):
    (HERE/name).write_text(json.dumps(obj,ensure_ascii=False,indent=1)+"\n")


def book():
    with (HIST/"vers.tsv").open() as f:
        rows=list(csv.DictReader(f,delimiter="\t"))
    return [(r["titre"],int(r["rang_du_vers"]),r["texte_edite"],ref.words(r["texte_edite"])) for r in rows]


def calibration(book):
    chapters=defaultdict(list)
    for notice,i,line,w in book:chapters[notice].append((i,w))
    titles=list(chapters)
    ciph=cipher([[w for i,w in rs] for rs in chapters.values()])
    hidden={(title,i):e for title,chapter in zip(titles,ciph) for (i,_),e in zip(chapters[title],chapter)}
    authentic={t:next(r for r in book if r[1]==i) for t,(w,i) in NAMES.items()}
    controls=[]
    for t,(name,i) in NAMES.items():
        teacher=next(q for q in NAMES if q!=t)
        _,idx,_,seq=authentic[teacher]; place=seq.index("quam")
        a,b=hidden[teacher,idx][place:place+2]
        key=extend(a,"quam",1,{})[0]; key=extend(b,"graecus",1,key)[0]
        inv={v:k for k,v in key.items()}; target=tuple(inv[k] for k in "graecus")
        title_cipher=hidden[t,i][authentic[t][3].index(name)]
        hits=[]; baseline=Counter(); nearby=Counter()
        for source,rank,text,w in book:
            if source==teacher:continue
            e=hidden[source,rank]
            for j in range(1,len(e)-1):
                if ref.decode(e[j],key)!="quam":continue
                baseline["annonces"]+=1; baseline["graecus"]+=int(target==e[j+1])
                if e[j-1]!=title_cipher:continue
                nearby["annonces"]+=1; nearby["graecus"]+=int(target==e[j+1])
                hits.append(dict(notice=source,vers=rank,forme_chiffree="".join(target),observe="".join(e[j+1]),exact=e[j+1]==target))
        controls.append(dict(apprentissage=teacher,nom_reserve=t,
             rubrique_flechie_donnee=name,avec_ancre=nearby,sans_ancre=baseline,lieux=hits))
    return dict(source="vers.tsv",sha256=sha256((HIST/"vers.tsv").read_bytes()).hexdigest(),
                vers=[dict(notice=n,vers=i,texte=text) for n,i,text,w in authentic.values()],calibration=controls)


def inventory():
    ed,sections=corpus()
    captions=defaultdict(list)
    forms=[labels(rows,cut) for rows in ed.values() for cut in ("joints","separes")]
    for l in sorted(set.union(*(set(v) for v in forms))):
        v=[f.get(l,()) for f in forms]
        if len(set(v))==1 and len(v[0])==1 and SIMPLE.fullmatch(v[0][0]):captions[v[0][0]].append(l)
    panels={s.split(".")[0] for sites in captions.values() for s in sites}
    meta={}
    for line in (langage.DATA/"ZL3b-n.txt").read_text().splitlines():
        m=re.match(r"^<(f\w+)>",line)
        if m:meta[m[1]]=dict(re.findall(r"\$(\w)=(\w+)",line))
    result=[]; raw={}; counts=Counter()
    for l in sorted(set.intersection(*(set(d) for d in ed.values()))):
        page=l.split(".")[0]
        rs=[b[l] for b in ed.values()]
        if page not in panels or sections[page]!="P" or any(r[1]!="P0" for r in rs):continue
        counts["lignes_P0"]+=1
        vs=[parse(r[3],c) for r in rs for c in ("joints","separes")]
        raw[l]=vs
        for w in sorted(set.intersection(*[set(v) for v in vs],set(captions))):
            places=[[i for i,v in enumerate(line) if v==w] for line in vs]
            if len({len(x) for x in places})!=1:continue
            for j in range(len(places[0])):
                coords=[x[j] for x in places]
                item=dict(lieu=l,occurrence=j+1,positions=coords,ancre=w,face=page,cahier=meta[page]["Q"],
                    bifeuillet=meta[page]["Q"]+"/"+meta[page]["B"],legendes=captions[w],
                    locale=any(x.split(".")[0]==page for x in captions[w]))
                result.append(item)
    assert sum(map(len,captions.values()))==130
    counts["etiquettes_concordantes"]=sum(map(len,captions.values()))
    counts["formes_etiquettes"]=len(captions); counts["panneaux_P0"]=len({l.split('.')[0] for l in raw})
    return result,raw,counts


def neighbor(s,raw,d):
    vals=[]
    for i,seq in zip(s["positions"],raw[s["lieu"]]):
        ix=i+d
        if not(0<=ix<len(seq)):return None
        if None in seq[min(i,ix):max(i,ix)+1]:return None
        vals.append(seq[ix])
    return vals[0] if len(set(vals))==1 and SIMPLE.fullmatch(vals[0]) else None


@lru_cache(None)
def maps(word,clear,width):
    return extend(ref.units(word),clear,width,{}) if word else []


def end(word,clear,width,prior):
    if not word:return []
    return [k for m in prior for k in extend(ref.units(word),clear,width,m)]


def site_id(s):
    return s["lieu"]+"#"+str(s["occurrence"])+":"+s["ancre"]


def forecast(rows,raw):
    out={}
    for width in (1,2):
        teachers=defaultdict(list)
        events=[]
        for s in rows:
            right=neighbor(s,raw,1)
            ks=maps(right,"quam",width)
            if not ks:continue
            events.append(dict(id=site_id(s),cahier=s["cahier"],locale=s["locale"],ancre=s["ancre"],
                     suivant=right,attendu_deuxieme_droite="graecus",attendu_gauche="dicimus",cles_quam=ks))
            if s["locale"] and s["cahier"]=="O":
                for k in end(neighbor(s,raw,2),"graecus",width,ks):
                    teachers[tuple(sorted(k.items()))].append(site_id(s))
        transfer=[]
        for k,orig in sorted(teachers.items()):
            targets=[event["id"] for event in events if event["cahier"]=="S" and
                     ref.decode(ref.units(event["suivant"]),dict(k))=="quam"]
            transfer.append(dict(cle=dict(k),appris=orig,graecus_attendu=targets))
        out[str(width)]=dict(appels=events,cles_de_transfert=transfer)
    return out


def verify(rows,raw,registered,book,greek="graecus"):
    lex={w for _,_,_,seq in book for w in seq if len(w)==len(greek)}|{greek}
    vocabulary={w for _,_,_,seq in book for w in seq}
    details=[]
    for s in rows:
        if s["locale"]:details.append(dict(**s,voisins={str(d):neighbor(s,raw,d) for d in (-1,1,2)}))
    out={}
    for width in (1,2):
        p=registered[str(width)]
        transfer=defaultdict(list)
        for rec in p["cles_de_transfert"]:
            for tgt in rec["graecus_attendu"]:transfer[tgt].append(rec["cle"])
        events={e["id"]:e for e in p["appels"]}
        sets={"local":Counter(),"autre_panneau":Counter()}; hits=[]; controls=defaultdict(Counter)
        for s in rows:
            sid=site_id(s); level="local" if s["locale"] else "autre_panneau"; c=sets[level]
            c["reprises"]+=1
            mid=neighbor(s,raw,1); left=neighbor(s,raw,-1); nxt=neighbor(s,raw,2)
            c["premier_voisin_droit_lisible"]+=bool(mid)
            c["deux_voisins_droits_lisibles"]+=bool(mid and nxt)
            c["trois_voisins_lisibles"]+=bool(mid and nxt and left)
            e=events.get(sid)
            if e is None:continue
            ks=e["cles_quam"]
            c["quam_ajustable"]+=1; c["graecus_verifiable"]+=bool(nxt)
            c["dicimus_verifiable"]+=bool(left)
            both=end(nxt,greek,width,ks)
            pre=end(left,"dicimus",width,ks)
            triple=end(left,"dicimus",width,both)
            c["graecus_ajustable"]+=bool(both);c["dicimus_ajustable"]+=bool(pre);c["trois_ajustables"]+=bool(triple)
            clear_names=sorted({name for name,idx in NAMES.values() if end(s["ancre"],name,width,both)})
            strict_names=sorted({name for name in ("urticam","acidulam") if end(s["ancre"],name,width,triple)})
            c["nom_plus_deux_voisins"]+=bool(clear_names);c["nom_plus_trois_voisins"]+=bool(strict_names)
            c["transfert_annonce"]+=bool(transfer[sid])
            c["transfert_lisible"]+=bool(transfer[sid] and nxt)
            full=bool(nxt and any(ref.decode(ref.units(nxt),k)=="graecus" for k in transfer[sid]))
            c["transfert_confirme"]+=full
            if s["locale"] or both or pre or full:
                central={ref.decode(ref.units(s["ancre"]),k) for k in pre}-{None}
                hits.append(dict(id=sid,locale=s["locale"],ancre=s["ancre"],premier_droit=mid,
                    deuxieme_droit=nxt,gauche=left,graecus=bool(both),dicimus=bool(pre),ensemble=bool(triple),
                    legendes=s["legendes"],nombre_cles_dicimus_quam=len(pre),lectures_entieres_du_nom_par_dicimus_quam=sorted(central),
                    lectures_du_nom_attestees=sorted(central & vocabulary),noms_avec_graecus=clear_names,noms_avec_dicimus_graecus=strict_names,transfert=full))
            if nxt:
                for alt in lex:
                    if end(nxt,alt,width,ks):controls[level][alt]+=1
        ctrl={}
        for level in sets:
            score=controls[level][greek]
            ctrl[level]={"autres":len(lex)-1,"au_moins_autant":sum(controls[level][k]>=score for k in lex if k!=greek),
                         "atteignent":{k:v for k,v in sorted(controls[level].items()) if v}}
        out[str(width)]=dict(totaux=sets,lieux=hits,temoins_7_lettres=ctrl)
    return dict(reprises_locales=details,epreuves=out)


if __name__=="__main__":
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument("mode",choices=("predire","verifier","manuscrit")); a=ap.parse_args()
    rows,raw,counts=inventory(); b=book()
    if a.mode=="predire":
        f=forecast(rows,raw)
        write("PREDICTIONS.json",dict(couverture=counts,latin=calibration(b),experiences=f))
        print(counts)
        for w,v in f.items():print(w,Counter((e["cahier"],e["locale"]) for e in v["appels"]),len(v["cles_de_transfert"]))
    elif a.mode=="manuscrit":
        original=json.loads((HERE/"PREDICTIONS.json").read_text())["experiences"]
        assert not any(v["cles_de_transfert"] for v in original.values())
        result=verify(rows,raw,original,b,"grecus")
        normalized=json.dumps(result,ensure_ascii=False).replace("graecus","grecus").replace("temoins_7_lettres","temoins_6_lettres")
        write("LECTURE-1478.json",json.loads(normalized))
    else:
        result=verify(rows,raw,json.loads((HERE/"PREDICTIONS.json").read_text())["experiences"],b)
        write("RESULTATS.json",result)
        for w,exp in result["epreuves"].items():print(w,exp["totaux"])
