"""Déchiffrer avec les dix valeurs gelées, en conservant les coupures matérielles."""
from collections import Counter,defaultdict
import gzip,json,random,re,sys
from pathlib import Path
from chercher import LATIN,celsus,HERE
sys.path.insert(0,str(HERE.parent))
from suites import aligned,corpus,metadata,segment
CAPPED=4

def sample(signs):
    ed,_=corpus();meta=metadata(); types=defaultdict(list)
    for loc,(page,kind,_,_) in ed["H"].items():
        if kind!="P0" or loc not in ed["ZL"] or ed["ZL"][loc][1]!=kind:continue
        if int(re.match(r'f(\d+)',page)[1]) in (82,103,108,116):continue
        previous=None;run=[]
        for row in aligned(ed,loc,page,meta[page].get('I'),page,Counter()):
            ranks=tuple(map(int,row['rangs_quatre'].split('/')))
            if previous is not None:
                b,rr=previous
                if b!=row['troncon'] or not all(y==x+1 for x,y in zip(rr,ranks)):run=[]
            u=segment(row['mot'])
            if len(u)>1 and u[0]=='d' and 'debut' in row['positions']:u=u[1:]
            if not set(u)<=signs:run=[]
            else:
                run.append((tuple(u),row['mot'],ranks[0]))
                if len(run)>CAPPED:run.pop(0)
                for j in range(len(run)):
                    suffix=run[j:]
                    types[tuple(r[0] for r in suffix)].append((loc,row['troncon'],suffix[0][2],tuple(r[1] for r in suffix)))
            previous=row['troncon'],ranks
    return types

def refs(books,norm):
    index={n:set() for n in range(1,CAPPED+1)}
    for ws in books.values():
        w=[norm(x) for x in ws]
        for n in index:index[n].update(zip(*(w[i:] for i in range(n))))
    return index

def run(path):
    d=json.loads(gzip.decompress((HERE/'RESULTATS.json.gz').read_bytes()))
    key=d['corpus']['Celse']['modeles']['2/muet/d']['0']['lectures_longues'][0][-1]
    cases=sample(set(key));units={w for phrase in cases for w in phrase}
    c={k:v for k,v in celsus(path,r'[.;:!?]').items() if not k.startswith('8.4.')}
    books={'Celse':c,'Macer':json.loads(LATIN.read_bytes())}
    gen=random.Random(108116);order=sorted(key);seq=[key[x] for x in order]
    permutations=[];seen={tuple(seq)}
    while len(permutations)<199:
        gen.shuffle(seq)
        if tuple(seq) not in seen:
            seen.add(tuple(seq));permutations.append(dict(zip(order,seq)))
    out={'table':key,'cibles':{k:sum(len(rs) for s,rs in cases.items() if len(s)==k) for k in range(1,5)},'lectures':{}}
    for name,regularize in [('exact',lambda s:s),('ae_en_e',lambda s:s.replace('ae','e'))]:
        for author,collection in books.items():
            match=refs(collection,regularize);results=[];examples=defaultdict(list)
            for i,m in enumerate([key,*permutations]):
                decoder={w:regularize(''.join(m[g] for g in w)) for w in units}
                counts=[0]*CAPPED
                for phrase,rows in cases.items():
                    latin=tuple(decoder[w] for w in phrase);n=len(latin)
                    if latin in match[n]:
                        counts[n-1]+=len(rows)
                        if i==0 and len(examples[n])<12:examples[n].append([latin,rows[0],len(rows)])
                results.append(counts)
            out['lectures'][author+'/'+name]={'attestes':results[0],'permutations':results[1:],'exemples':dict(examples)}
    (HERE/'TRANSFERT.json').write_text(json.dumps(out,indent=1,ensure_ascii=False,sort_keys=True)+'\n')

if __name__=='__main__':run(Path(sys.argv[1]))
