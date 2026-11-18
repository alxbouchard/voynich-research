"""Contrôle prospectif du patron dans la prose des autres sections."""
import sys
import json
from collections import Counter
from aligner import HERE, EDGES, manuscript, outside, repository_lines, write


def run(mode):
    doc=repository_lines()
    if mode=="predire":
        gallery,_,_=manuscript()
        p=json.loads((HERE/"PREDICTIONS.json").read_text());weights=p["votes_regroupes"]
        sites=[]
        for loc,ss in doc.items():
            page=loc.split(".")[0]
            if page.startswith("f99") or page in gallery:continue
            for seg,words in enumerate(ss):
                for i in range(len(words)-4):
                    a,x,b,y,c=words[i:i+5]
                    if not all((a,x,b,y,c)) or x!=y or x!="daiin" or len({a,x,b,c})!=4:continue
                    group=words[i:i+5]
                    sites.append(dict(lieu=loc,segment=seg,rang=i+1,mots=group,previsions={
                        side:group[g["unique_majoritaire"]] if g["unique_majoritaire"] is not None else None for side,g in weights.items()}))
        write("RESERVE-PREDICTIONS.json",sites)
    else:
        p=json.loads((HERE/"RESERVE-PREDICTIONS.json").read_text()); counts={k:Counter() for k in EDGES}
        for s in p:
            w=doc[s["lieu"]][s["segment"]];i=s["rang"]-1
            assert w[i:i+5]==s["mots"]
            pool=[v for n,v in enumerate(w) if v and n not in range(i,i+5)]
            obs={}
            for k,d in EDGES.items():
                seen=outside(w,i,d);obs[k]=seen
                if seen:
                    c=counts[k];c["essais"]+=1;c["justes"]+=int(seen==s["previsions"][k])
                    c["espere_frequence_dans_ligne"]+=pool.count(s["previsions"][k])/len(pool)
            s["observes"]=obs
        write("RESERVE-RESULTATS.json",{"scores":counts,"lieux":p})


if __name__=="__main__":run(sys.argv[1])
