"""Présence de cth ou de cthy immédiatement avant les interruptions IVTFF."""
from collections import defaultdict
import json
from pathlib import Path
import re
import sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parents[1]/'2026-11-18-opcheor-paralleles/variantes'))
from compter import GAP, corpus, tokens

BORD=re.compile(r'(<[-~]>)')
MODES=[(ed,cut) for ed in ('H','ZL') for cut in ('joints','separes')]

def codes(raw,cut):
    seen=set()
    pieces=BORD.split(re.sub(r'\{[^}]*\}', '?', raw))
    for i in range(0,len(pieces),2):
        spans=GAP.split(pieces[i])
        for rank,span in enumerate(spans):
            ws=tokens(span,cut)
            for pos,w in enumerate(ws):
                if w not in ('cth','cthy'):
                    continue
                names=[w]
                if pos and ws[pos-1]=='daiin':names.append('daiin '+w)
                seen.update(names)
                if pos+1==len(ws) and rank+1==len(spans) and i+1<len(pieces):
                    seen.update(n+' |' for n in names)
    return seen

def main():
    assert 'daiin cth |' in codes('daiin.cth<->dain','joints')
    assert 'daiin cth |' not in codes('daiin.cth.dain<->dy','joints')
    assert 'daiin cth' not in codes('daiin<->cth.dy','joints')
    books,sections=corpus()
    out={}
    for group in ('selection','herbier','autres'):
        result=defaultdict(list)
        coverage=0
        for l in sorted(set(books['ZL'])&set(books['H'])):
            page=books['H'][l][0]
            if group!=('selection' if re.fullmatch(r'f(?:10|11|15)[rv]\d*',page) else
                       'herbier' if sections[page]=='H' else 'autres'):
                continue
            if any(book[l][1]!='P0' for book in books.values()):
                continue
            coverage+=1
            agreed=set.intersection(*(codes(books[ed][l][3],cut) for ed,cut in MODES))
            for k in sorted(agreed):
                result[k].append(l)
        out[group]={'lignes_P0':coverage,'lignes':result}
        print(group,coverage,{k:len(v) for k,v in result.items()})
    (HERE/'bord.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n')
if __name__=='__main__':main()
