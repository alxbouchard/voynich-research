"""Finite constraint search for a tentative crib; this does not infer plaintext."""
from pathlib import Path
import collections, hashlib, itertools, json, re

ROOT=Path(__file__).resolve().parents[1]
PLAIN_WORDS=['six','marix','morix','vix']
PLAIN=''.join(PLAIN_WORDS)
ATOMS=re.compile(r'cth|ckh|cph|cfh|ch|sh|[a-z]')

def units(word,mode):
    return list(word) if mode=='EVA' else ATOMS.findall(word)

def rows(path):
    out=[]
    for rawline in path.read_text().splitlines():
        m=re.match(r'^<(f\d+[^.>]*)\.(\d+),([^>]+)>\s+(.+)',rawline)
        if m and not m[3].startswith('!') and m[1]!='f116v':
            p,n,k,s=m.groups();out.append(dict(page=p,n=int(n),kind=k,raw=s,locus=p+'.'+n))
    return out

def blocks(rr,spacing):
    allblocks=[];current=[];previous=None
    def flush():
        nonlocal current
        if current:allblocks.append(current);current=[]
    for row in rr:
        join=(previous is not None and row['page']==previous['page'] and row['n']==previous['n']+1
              and row['kind'][1:2]=='P' and previous['kind'][1:2]=='P'
              and row['kind'][0] in '+=' and '<%>' not in row['raw'] and '<$>' not in previous['raw'])
        if not join:flush()
        s=row['raw'].replace('<->','|').replace('<~>','|')
        s=re.sub(r'<[^>]*>','',s)
        s=re.sub(r'\{([a-z]+)\}',r'\1',s)
        s=re.sub(r'\[([^\[\]]+)\]',lambda m:m[1].split(':')[0],s)
        s=s.replace(',', '.' if spacing=='split' else '')
        for j,part in enumerate(s.split('|')):
            if j:flush()
            for w in part.split('.'):
                if re.fullmatch('[a-z]+',w):current.append({'text':w,'locus':row['locus'],'page':row['page'],'kind':row['kind']})
                else:flush()
        previous=row
    flush();return allblocks

def fit(cipher,plain=PLAIN,injective=False):
    if len(cipher)!=len(plain):return None
    key={};rev={}
    for a,b in zip(cipher,plain):
        if a in key and key[a]!=b:return None
        if injective and b in rev and rev[b]!=a:return None
        key[a]=b;rev[b]=a
    return key

def independent_check(cipher,key,injective):
    assert ''.join(key[c] for c in cipher)==PLAIN
    assert all(len({PLAIN[j] for j,x in enumerate(cipher) if x==c})==1 for c in set(cipher))
    if injective:assert len(set(key.values()))==len(key)

def controls():
    key={c:str(i) for i,c in enumerate(sorted(set(PLAIN)))}
    cipher=[key[c] for c in PLAIN]
    assert fit(cipher,injective=True) is not None
    homo=cipher.copy();homo[6]='newglyph'
    assert PLAIN[6]=='i'
    assert fit(homo,injective=False) is not None and fit(homo,injective=True) is None
    bad=cipher.copy();bad[0]=cipher[1]
    assert fit(bad) is None
    for alphabet in ['ab','abc']:
        for p in itertools.product(alphabet,repeat=4):
            for c in itertools.product(alphabet,repeat=4):
                expected=all(p[i]==p[j] for i in range(4) for j in range(4) if c[i]==c[j])
                assert (fit(c,''.join(p)) is not None)==expected
    rr=[dict(page='f1r',n=1,kind='@P0',raw='ab.cd<$>',locus='f1r.1'),
        dict(page='f1r',n=2,kind='+P0',raw='ef.?.gh<->ij',locus='f1r.2')]
    assert [[w['text'] for w in b] for b in blocks(rr,'split')]==[['ab','cd'],['ef'],['gh'],['ij']]
    return 'passed: synthetic bijection, homophony, contradiction, 6,817 exhaustive pairs, and barriers'

def scan(bs,tok,spacing,code):
    output=[];counts=collections.Counter()
    for direction in ['forward','reverse']:
        for block_id,words in enumerate(bs):
            uw=[units(w['text'],tok) for w in words]
            flat=[u for ww in uw for u in ww]
            positions=[(j,k) for j,ww in enumerate(uw) for k in range(len(ww))]
            for search in ['four_words','unspaced']:
                if search=='four_words':
                    windows=[]
                    for j in range(len(words)-3):
                        if [len(x) for x in uw[j:j+4]]==[3,5,5,3]:
                            windows.append(([u for ww in uw[j:j+4] for u in ww],j,0,j+3,len(uw[j+3])-1))
                else:
                    windows=((flat[j:j+len(PLAIN)],*positions[j],*positions[j+len(PLAIN)-1]) for j in range(len(flat)-len(PLAIN)+1))
                for seq,j,k,je,ke in windows:
                    if direction=='reverse':seq=list(reversed(seq))
                    counts[search+'_'+direction+'_windows']+=1
                    key=fit(seq)
                    if key is None:continue
                    bij=fit(seq,injective=True) is not None
                    independent_check(seq,key,bij)
                    row=dict(corpus=code,spacing=spacing,tokenization=tok,direction=direction,search=search,
                             block=block_id,locus_start=words[j]['locus'],locus_end=words[je]['locus'],
                             page=words[j]['page'],start_word=j,start_unit=k,end_word=je,end_unit=ke,
                             eva_words=' '.join(w['text'] for w in words[j:je+1]),cipher_units=seq,
                             key=key,bijection=bij)
                    output.append(row)
                    counts[search+'_'+direction+'_homophonic']+=1
                    if bij:counts[search+'_'+direction+'_bijection']+=1
    return dict(corpus=code,spacing=spacing,tokenization=tok,blocks=len(bs),counts=dict(counts),matches=output)

def main():
    result={'crib_words':PLAIN_WORDS,'controls':controls(),'runs':[],'source_hashes':{}}
    for code,name in [('ZL','ZL3b-n.txt'),('IT','IT2a-n.txt')]:
        path=ROOT/'data'/name;rr=rows(path)
        result['source_hashes'][name]=hashlib.sha256(path.read_bytes()).hexdigest()
        for spacing in ['split','join']:
            bs=blocks(rr,spacing)
            for tok in ['EVA','composed']:
                r=scan(bs,tok,spacing,code);result['runs'].append(r)
                print(code,spacing,tok,r['counts'],flush=True)
    (ROOT/'results/crib_scan.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    summary={k:v for k,v in result.items() if k!='runs'}
    summary['runs']=[{k:v for k,v in r.items() if k!='matches'}|{'matches_f104r':sum(x['page']=='f104r' for x in r['matches'])} for r in result['runs']]
    (ROOT/'results/crib_summary.json').write_text(json.dumps(summary,indent=2))

if __name__=='__main__':main()
