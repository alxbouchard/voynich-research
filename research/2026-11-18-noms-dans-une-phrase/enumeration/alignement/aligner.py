"""Aligner des codages bijectifs de mots entiers et geler les voisins déductibles."""
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import random
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
from enumerer import historic
from contexte import corpus, manuscript, sections, sequence

SEED=("ckhol","daiin","okeoly","daiin","ckhy")
EDGES={"avant_W":-1,"apres_Y":5,"deux_apres_Y":6}


def write(name,data):
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=1)+"\n")


def outside(words,pos,d):
    j=pos+d
    return words[j] if 0<=j<len(words) else None


def historic_alignments(spans,index):
    name=next(iter(index)); words=set(w for _,_,ws,_ in spans for w in ws)
    opaque=sorted(words);random.Random(879109).shuffle(opaque); hidden={w:f"sym{i}" for i,w in enumerate(opaque)}
    rows=[]; log=Counter()
    for _,loc,line,offset in spans:
        for j in range(len(line)-3):
            et,x,et2,y=line[j:j+4]
            if et!="et" or et2!=et:continue
            log["et_X_et_Y"]+=1
            if j==0:log["debut_sans_W"]+=1;continue
            pos=j-1; physical=line[pos:j+4]
            if len(set(physical))!=4:log["codes_confondus"]+=1;continue
            signature=[physical.index(v) for v in physical]
            assert signature==[0,1,2,1,4]
            encoder=dict(zip(physical,SEED)); relative={}; clear={}; predicted={}
            hseq=[hidden[w] for w in physical]
            for side,d in EDGES.items():
                word=outside(line,pos,d);clear[side]=word
                match=physical.index(word) if word in physical else None
                relative[side]=match
                predicted[side]=encoder.get(word)
                h=hidden.get(word)
                assert match==(hseq.index(h) if h in hseq else None)
            rows.append(dict(lieu=loc,rang_W=offset+pos+1,latins=physical,
                        X_dans_index=x in index[name],Y_dans_index=y in index[name],
                        voisins_latins=clear,positions_prevues=relative,EVA_predits=predicted))
    log["alignements"]=len(rows)
    return {"source":name,"comptes":log,"expressions":rows}


def evidence(rows):
    result={}
    for d in EDGES:
        votes=Counter(r["positions_prevues"][d] for r in rows if r["positions_prevues"][d] is not None)
        ranks=[k for k,n in votes.items() if n==max(votes.values())]
        result[d]=dict(votes=dict(sorted(votes.items())),abstentions=len(rows)-sum(votes.values()),
                       unique_majoritaire=ranks[0] if len(ranks)==1 else None)
    return result


def repository_lines():
    eds,_=corpus()
    result={}
    for loc in sorted(set.intersection(*(set(v) for v in eds.values()))):
        src=[e[loc] for e in eds.values()]
        if any(r[1]!="P0" for r in src):continue
        paths=[sequence(r[3],cut) for r in src for cut in ("joints","separes")]
        result[loc]=sections(paths)
    return result


def slots(record,local):
    output=[]
    for loc,lines in record.items():
        page=loc.split(".")[0]
        offset=0
        for seg,ws in enumerate(lines):
            if not page.startswith("f99"):
                for i in range(len(ws)):
                    for mode,probe in [("cinq",SEED),("quatre",SEED[:4]),("trois",SEED[1:4])]:
                        if tuple(ws[i:i+len(probe)])==probe:
                            output.append(dict(lieu=loc,segment=seg,rang=i+1,rang_ligne=offset+i+1,mode=mode,
                                               dans_panneaux=page in local,cadre=list(probe)))
                    seq=ws[i:i+5]
                    if page in local and len(seq)==5 and all(seq) and seq[1]==seq[3]=="daiin" and len(set(seq))==4:
                        output.append(dict(lieu=loc,segment=seg,rang=i+1,rang_ligne=offset+i+1,mode="structure",
                                dans_panneaux=True,X_legende_locale=seq[2] in local[page],cadre=seq))
            elif loc=="f99r.18":
                for i in range(len(ws)-4):
                    if tuple(ws[i:i+5])==SEED:
                        output.append(dict(lieu=loc,segment=seg,rang=i+1,rang_ligne=offset+i+1,mode="depart",
                            dans_panneaux=True,X_legende_locale=True,cadre=SEED))
                # Un seul segment porte l'amorce.
            offset+=len(ws)
    assert sum(s['mode']=='depart' for s in output)==1
    return output


def predict():
    history=[historic_alignments(spans,index) for spans,index in historic()]
    assert [x["comptes"]["et_X_et_Y"] for x in history]==[5,85]
    for x in history:x["vote"]=evidence(x["expressions"])
    pooled=evidence([r for source in history for r in source["expressions"]])
    lex,_,_=manuscript()
    sites=slots(repository_lines(),lex)
    for s in sites:
        if s["mode"] in ("trois","quatre"):s["suite_attendue"]="ckhy"; continue
        for side,g in pooled.items():
            rank=g["unique_majoritaire"]
            s.setdefault("graphies_par_vote",{})[side]=s["cadre"][rank] if rank is not None else None
            s.setdefault("graphies_au_moins_une_table",{})[side]=sorted({s["cadre"][int(k)] for k in g["votes"]})
    write("PREDICTIONS.json",dict(source_parent=sha256((HERE.parent/"RESULTATS.json.gz").read_bytes()).hexdigest(),
         etudes=history,votes_regroupes=pooled,cibles=sites))


def verify():
    p=json.loads((HERE/"PREDICTIONS.json").read_text())
    lines=repository_lines(); scores={}; details=[]
    for s in p["cibles"]:
        mode=s["mode"];loc=s["lieu"];idx=s["rang"]-1
        words=lines[loc][s["segment"]]
        assert words[idx:idx+len(s["cadre"])]==s["cadre"]
        ctr=scores.setdefault(mode,Counter()); ctr["fenetres"]+=1
        if mode in ("trois","quatre"):
            observed=outside(words,idx,len(s["cadre"]))
            if observed:
                ctr["testables"]+=1;ctr["succes"]+=int(observed==s["suite_attendue"])
            details.append(dict(**s,observe=observed));continue
        observed={side:outside(words,idx,d) for side,d in EDGES.items()}
        details.append(dict(**s,observes=observed))
        for side,w in observed.items():
            if not w:continue
            ctr["voisins_lisibles"]+=1
            if s["graphies_par_vote"][side]:
                ctr["votes_testables"]+=1;ctr["votes_corrects"]+=int(s["graphies_par_vote"][side]==w)
            if s["graphies_au_moins_une_table"][side]:
                ctr["un_ou_plus_testables"]+=1;ctr["au_moins_une_table_correcte"]+=int(w in s["graphies_au_moins_une_table"][side])
    write("RESULTATS.json",dict(comptes=scores,cibles=details))


if __name__=="__main__":
    if sys.argv[2]=="predire":predict()
    elif sys.argv[2]=="verifier":verify()
    else:raise ValueError("predire ou verifier")
