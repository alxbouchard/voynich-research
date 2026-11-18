"""Deux phrases appariées avec un dictionnaire de mots entiers."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/"2026-11-18-renvois-entre-plantes/phrase"))
from lecture import load, read_books, save

EVA=("qokol","daiin","qokchol","dar")


def inserted(x,u):
    width=len(u)-len(x)
    if width not in (1,2):return None
    offsets=[i for i in range(len(x)+1) if u[:i]+u[i+width:]==x]
    if any(0<i<len(x) for i in offsets):return "interne"
    return "bord" if offsets else None


def catalogue(body):
    frames=defaultdict(list)
    pairs=defaultdict(list)
    for place,ws in body.items():
        for i in range(len(ws)-2):
            a,b,c=ws[i:i+3]
            if a==b:continue
            after=ws[i+3] if i+3<len(ws) else None
            right=(place,i,c,after)
            pairs[a,b].append(right)
            if a==c:
                frames[a].append((place,i,b,ws[i-1] if i else None,after))
    return frames,pairs


def predictions(body):
    frames,pairs=catalogue(body)
    unrestricted=Counter()
    candidates=[]
    for x,left in frames.items():
        for u,right in frames.items():
            if x==u:continue
            kind=inserted(x,u)
            for p,i,y,pr1,nx1 in left:
                for q,j,v,pr2,nx2 in right:
                    if len({x,y,u,v})!=4:continue
                    unrestricted["paires"]+=1
                    if nx1:unrestricted["suivants_lisibles"]+=1
                    if nx1==v:unrestricted["suivant_egale_second_centre"]+=1
                    if not kind:continue
                    lexical=dict(zip((x,y,u,v),EVA))
                    other=[r for r in pairs[u,v] if (r[0],r[1]) not in {(p,i),(q,j)} and r[2]!=u]
                    counts=Counter(r[2] for r in other)
                    tops=sorted(w for w,n in counts.items() if n==max(counts.values())) if counts else []
                    doubles=[r[:3] for r in pairs[x,y] if r[2]==r[3] and r[2] not in lexical]
                    chosen=tops[0] if len(tops)==1 else None
                    candidates.append(dict(lieux=[[p,i+1],[q,j+1]],mots=[x,y,u,v],insertion=kind,
                                           autour=[pr1,nx1,pr2,nx2],
                                           predictions=[lexical.get(w) for w in (pr1,nx1,pr2,nx2)],
                                           troisieme_compte=dict(counts),troisieme_modes=tops,
                                           troisieme_prevu=lexical.get(chosen),
                                           doubles_autres_lieux=[[z,k+1,w] for z,k,w in doubles]))
    return {"sans_contrainte_insertion":dict(unrestricted),"candidats":candidates}


def opened(books):
    data={}
    for name,study in books.items():
        kinds={}
        for name_rule,selected in [
            ("interne",[r for r in study["candidats"] if r["insertion"]=="interne"]),
            ("interne_ou_bord",study["candidats"])]:
            counts=Counter()
            survivors=[]
            hist=Counter()
            for r in selected:
                pred=r["predictions"][1]
                counts["paires"]+=1
                counts["quatrieme_disponible"]+=r["autour"][1] is not None
                counts["quatrieme_annonce_en_eva"]+=bool(pred)
                counts["quatrieme_juste"]+=pred=="dar"
                if pred:hist[pred]+=1
                if pred!="dar":continue
                counts["troisieme_a_f14r_atteste"]+=bool(r["troisieme_modes"])
                counts["troisieme_a_f14r_non_ambigu"]+=len(r["troisieme_modes"])==1
                counts["troisieme_a_f14r_annonce_en_eva"]+=bool(r["troisieme_prevu"])
                counts["troisieme_a_f14r_juste_H"]+=r["troisieme_prevu"]=="dala"
                counts["troisieme_a_f14r_juste_ZL"]+=r["troisieme_prevu"]=="dalo"
                counts["doublet_f102r2"]+=bool(r["doubles_autres_lieux"])
                survivors.append(r)
            kinds[name_rule]=dict(bilan=dict(counts),previsions_quatrieme=dict(hist),paires_retenues=survivors)
        data[name]=kinds
    return data


def challenge():
    # Le moteur ne reçoit ni la table cachée ni les voisins chiffrés.
    book={"feuille1":"sel et sel puis".split(),"feuille2":"seul puis seul et".split(),
          "feuille3":"seul puis et".split(),"leurre":"pain dans pain ensuite".split(),
          "variante":"sain dont sain ensuite".split()}
    table={"sel":"qokol","et":"daiin","seul":"qokchol","puis":"dar"}
    result=predictions(book)
    valid=[r for r in result["candidats"] if r["mots"]==list(table)]
    assert len(valid)==1 and valid[0]["predictions"][1]==table["puis"] and valid[0]["troisieme_prevu"]==table["et"]
    return {"corpus_construit":book,"reponses_attendues":["dar","daiin"],"predictions":valid[0]}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lot",choices=("sept","cambridge"))
    parser.add_argument("mode",choices=("annoncer","ouvrir"))
    parser.add_argument("sources",type=Path,nargs="*")
    args=parser.parse_args()
    pre=HERE/f"ANNONCES-{args.lot}.json.gz"
    if args.mode=="ouvrir":
        save(HERE/f"OUVERTURE-{args.lot}.json.gz",opened(load(pre)["livres"]))
        return
    body=read_books(*args.sources) if args.lot=="sept" else load(args.sources[0])
    save(pre,{"empreintes":{p.name:sha256(p.read_bytes()).hexdigest() for p in args.sources},
              "livres":{n:predictions(b) for n,b in body.items()}})
    save(HERE/"CONTROLE.json",challenge())


if __name__=="__main__":main()
