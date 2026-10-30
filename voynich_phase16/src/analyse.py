"""Reproducible limited audit of published marginal anchors, not a decipherment."""
from pathlib import Path
from collections import Counter
import re, json, hashlib

ROOT=Path(__file__).resolve().parent.parent
QUERIES=['oror','aror','sheey','oror sheey','aror sheey','ororsheey','arorsheey',
         'oror tcheey','aror dshey','arorl sheey','aror shedy']
# Manual EVA identification of a conservative subset of the published preliminary table.
BASE={
 'd':('a','b'),'a':('b','c'),'r':('c','d'),'o':('e','f'),
 'in':('f','g'),'n':('g','h'),'e':('h','i'),'ch':('i',None),
 'l':('l','m'),'f':('o','p'),'s':('p','q'),'p':('s','t'),'t':('x','y')}
ATOMS=re.compile(r'cth|ckh|cph|cfh|ch|sh|in|[a-z]')

def rows(path):
    out=[]; meta={}
    for line in path.read_text().splitlines():
        h=re.match(r'^<(f[^.>]+)>\s+<! (.+)>',line)
        if h:meta[h[1]]=dict(re.findall(r'\$(\w)=(\S+)',h[2]))
        m=re.match(r'^<(f\d+[^.>]*)\.(\d+),([^>]+)>\s+(.+)',line)
        if not m:continue
        page,num,kind,raw=m.groups()
        if kind.startswith('!'):continue
        text=re.sub(r'<[^>]*>','',raw.replace('<->','|').replace('<~>','|'))
        out.append(dict(page=page,number=int(num),locus=page+'.'+num,kind=kind,
                        raw=raw,text=text,metadata=meta.get(page,{})))
    return out

def token_segments(row,mode):
    s=row['text']
    if mode!='strict':
        s=re.sub(r'\{([a-z]+)\}',r'\1',s)
        s=re.sub(r'\[([^\[\]]+)\]',lambda m:m[1].split(':')[0],s)
        s=s.replace(',', '.' if mode=='split' else '')
    return [[w if re.fullmatch('[a-z]+',w) else None for w in part.split('.')]
            for part in s.split('|')]

def concordance(rr,mode):
    found={q:[] for q in QUERIES};cross={q:[] for q in QUERIES if ' ' in q}
    previous=None
    for row in rr:
        if row['page']=='f116v':continue
        segments=token_segments(row,mode)
        for segi,seg in enumerate(segments):
            for q in QUERIES:
                words=q.split();n=len(words)
                for j in range(len(seg)-n+1):
                    if seg[j:j+n]==words:
                        found[q].append(dict(locus=row['locus'],segment=segi,index=j,
                                            raw=row['raw'],kind=row['kind'],metadata=row['metadata']))
        # Physical consecutive prose lines, same page and paragraph, no drawing joining.
        if previous is not None:
            a,segs=previous
            if (row['page']==a['page'] and row['number']==a['number']+1
                and row['kind'][1:2]=='P' and a['kind'][1:2]=='P'
                and row['kind'][0] in '+=' and '<%>' not in row['raw'] and '<$>' not in a['raw']):
                pair=[segs[-1][-1],segments[0][0]]
                for q in cross:
                    if pair==q.split():cross[q].append(dict(from_locus=a['locus'],to_locus=row['locus'],raw_before=a['raw'],raw_after=row['raw']))
        previous=(row,segments)
    return dict(counts={q:len(v) for q,v in found.items()},matches=found,
                cross_line_counts={q:len(v) for q,v in cross.items()},cross_line_matches=cross)

def keys():
    out={}
    for side in ['left','right']:
        for uncertain in ['j','k']:
            k={src:pair[side=='right'] for src,pair in BASE.items()}
            k['y']=uncertain if side=='left' else 'l'
            if side=='right':k['ch']=uncertain
            out[side+'_'+uncertain]=k
    return out

def decode(word,key):
    aa=ATOMS.findall(word)
    assert ''.join(aa)==word
    return ''.join(key.get(a) or '['+a+']' for a in aa),all(key.get(a) for a in aa)

def coverage(rr):
    counts=Counter(w for r in rr if r['page']!='f116v'
                   for seg in token_segments(r,'strict') for w in seg if w)
    out={};example_words=['chol','cheol','dain','oror','aror','sheey','daiin','qokeedy']
    for name,key in keys().items():
        complete={w:n for w,n in counts.items() if decode(w,key)[1]}
        lines=[];clean_prose=0
        for r in rr:
            if r['page']=='f116v' or r['kind'][1:2]!='P':continue
            segs=token_segments(r,'strict');ww=[w for s in segs for w in s]
            if not ww or not all(ww):continue
            clean_prose+=1
            if all(decode(w,key)[1] for w in ww):
                lines.append(dict(locus=r['locus'],words=ww,decoded=' '.join(decode(w,key)[0] for w in ww)))
        out[name]=dict(key=key,clean_word_occurrences=sum(counts.values()),clean_word_types=len(counts),
          fully_mapped_occurrences=sum(complete.values()),fully_mapped_types=len(complete),
          clean_prose_lines=clean_prose,fully_mapped_prose_lines=lines,
          top_complete=[dict(eva=w,count=n,mechanical=decode(w,key)[0]) for w,n in sorted(complete.items(),key=lambda a:(-a[1],a[0]))[:30]],
          examples={w:dict(zip(['mechanical','complete'],decode(w,key))) for w in example_words})
    return out

def checks():
    fake=dict(page='f999r',number=1,locus='f999r.1',kind='@P0',raw='oror.sheey',text='oror.sheey',metadata={})
    assert concordance([fake],'strict')['counts']['oror sheey']==1
    for text in ['oror|sheey','oror.?.sheey','oror,sheey']:
        assert concordance([fake|{'text':text}],'strict')['counts']['oror sheey']==0
    assert concordance([fake|{'text':'oror,sheey'}],'split')['counts']['oror sheey']==1
    assert concordance([fake|{'text':'oror,sheey'}],'join')['counts']['oror sheey']==0
    assert concordance([fake|{'page':'f116v'}],'strict')['counts']['oror sheey']==0
    assert decode('chol',keys()['left_j'])==('iel',True)
    assert decode('qokeedy',keys()['left_j'])==('[q]e[k]hhaj',False)
    assert decode('sheey',keys()['left_j'])==('[sh]hhj',False)
    return 'passed'

def main():
    result=dict(protocol=json.loads((ROOT/'PROTOCOL.json').read_text()),software_checks=checks(),corpora={})
    for code,file in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]:
        rr=rows(ROOT/'data'/file)
        result['corpora'][code]=dict(sha256=hashlib.sha256((ROOT/'data'/file).read_bytes()).hexdigest(),
          rows=len(rr),target_rows=[r for r in rr if r['page']=='f116v'],
          concordance={mode:concordance(rr,mode) for mode in ['strict','split','join']},
          coverage=coverage(rr))
    (ROOT/'results/analysis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    summary={code:dict(target_rows=len(x['target_rows']),
        counts={m:v['counts'] for m,v in x['concordance'].items()},
        cross_line={m:v['cross_line_counts'] for m,v in x['concordance'].items()},
        coverage={k:{f:v[f] for f in ['clean_word_occurrences','fully_mapped_occurrences','clean_word_types','fully_mapped_types','clean_prose_lines','fully_mapped_prose_lines']} for k,v in x['coverage'].items()}) for code,x in result['corpora'].items()}
    (ROOT/'results/summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
    for code,a in summary.items():
        print(code,{m:v for m,v in a['counts'].items()})
        k=a['coverage']['left_j']
        print('coverage',k['fully_mapped_occurrences'],k['clean_word_occurrences'],len(k['fully_mapped_prose_lines']),k['clean_prose_lines'])

if __name__=='__main__':main()
