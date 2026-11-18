"""Aligner les mots dans la ligne ; une barrière signalée par l'une des éditions suffit."""
from collections import Counter
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"2026-11-18-dam-en-fin-de-ligne"))
from corpus_dam import MODES, WORD, bords, parse


def local_rows(raw_views,loc):
    words=[]; blocks=[]
    for raw,(_,mode) in zip(raw_views,MODES):
        _,parts=parse(raw,mode)
        words.append(tuple(w for part in parts for w in part))
        blocks.append([i for i,part in enumerate(parts) for w in part])
    ref=words[0]
    alignments=[bords.forced(ref,v) for v in words[1:]]
    previous=None;run=0
    for i,w in enumerate(ref):
        if not WORD.fullmatch(w) or not all(i in m for m in alignments):
            continue
        ids=(i,*(m[i] for m in alignments))
        if any((j==0,j+1==len(v))!=(i==0,i+1==len(ref)) for j,v in zip(ids,words)):
            continue
        if previous is None or any(j!=k+1 or bl[k]!=bl[j] for j,k,bl in zip(ids,previous,blocks)):
            run+=1
        yield w,loc,run,tuple(j+1 for j in ids)
        previous=ids


def control():
    rows=list(local_rows(["aaa.bbb<->ccc.ddd"]*2+["aaa.bbb.ccc.ddd"]*2,"controle"))
    assert [r[0] for r in rows]==["aaa","bbb","ccc","ddd"]
    assert [r[2] for r in rows]==[1,1,2,2]
    # Un seul scribe/transcripteur écrit un groupe entre bbb et ccc.
    gap=list(local_rows(["aaa.bbb.ccc.ddd"]*2+["aaa.bbb.qqq.ccc.ddd"]*2,"lacune"))
    assert [r[2] for r in gap]==[1,1,2,2]
    return rows,gap
