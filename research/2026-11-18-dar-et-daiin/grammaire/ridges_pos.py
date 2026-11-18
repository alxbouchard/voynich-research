"""Relire, cellule par cellule, les catégories STTS de RIDGES sans réannoter sa langue."""
from collections import Counter,defaultdict
from hashlib import sha256
from io import BytesIO
import json
from pathlib import Path
import re,sys,unicodedata
from xml.etree import ElementTree as ET
from zipfile import ZipFile
from categories_centres import HERE,RESEARCH,save
REF=RESEARCH/'2026-11-18-phrase-et-doublets/lecture'
sys.path.insert(0,str(REF))
from ridges import INNER,INNER_SHA,merged_ranges


def annotated(raw,records):
    with ZipFile(BytesIO(raw)) as wb:
        strs=[''.join(v.text or '' for v in a.findall('.//{*}t')) for a in ET.fromstring(wb.read('xl/sharedStrings.xml'))]
        sheet=ET.fromstring(wb.read('xl/worksheets/sheet1.xml'))
    mat={}
    for row in sheet.findall('./{*}sheetData/{*}row'):
        cells={}
        for c in row.findall('{*}c'):
            v=c.findtext('{*}v','')
            if v:
                cells[re.sub(r'\d+$','',c.get('r'))]=strs[int(v)] if c.get('t')=='s' else v
        mat[int(row.get('r'))]=cells
    header={k:v for v,k in mat[1].items()}
    clean,pos=header['clean'],header['pos']
    spans=merged_ranges(sheet,(clean,pos))
    for loc,words in records.items():
        lo,hi=map(int,loc.split(':')[-1].split('-'))
        tokens=[];tags=[];lines=[]
        for i in range(lo,hi+1):
            a,b=spans[clean].get(i,(i,i))
            if a!=i:continue
            word=unicodedata.normalize('NFC',mat[a].get(clean,'').lower())
            tokens.append(word);lines.append([a,b])
            # Chaque forme clean doit couvrir la même étendue que le mot étiqueté.
            first,last=spans[pos].get(i,(i,i))
            tags.append(mat[first].get(pos) if (first,last)==(a,b) else None)
        assert tokens==words,(loc,tokens,words)
        yield loc,tokens,tags,lines


def run(archive):
    body=json.loads((REF/'RIDGES.json').read_bytes())
    sources=json.loads((REF/'RIDGES-SOURCES.json').read_bytes())
    names=sources['documents']
    with ZipFile(archive) as z:inner=z.read(INNER)
    assert sha256(inner).hexdigest()==INNER_SHA
    events=[];neg=defaultdict(Counter);alltags=Counter();gold=Counter()
    with ZipFile(BytesIO(inner)) as z:
        for name,info in names.items():
            src=z.read('Excel/RIDGES_Herbology/'+name+'.xlsx')
            assert sha256(src).hexdigest()==info['sha256_xlsx']
            pieces={loc:words for loc,words in body.items() if loc.split(':')[0]==name}
            year=re.search(r'148[27]',name)[0]
            for loc,words,tags,lines in annotated(src,pieces):
                for i,(x,b,zword) in enumerate(zip(words,words[1:],words[2:])):
                    if b in (x,zword):continue
                    left,mid,right=tags[i:i+3]
                    key=(year,x,min(2,(3*(i+1))//len(words)),left,right)
                    if x==zword:
                        alltags[mid or 'non_aligne']+=1
                        predicted=left in ('ART','APPR') and right in ('ART','APPR')
                        events.append(dict(lieu=loc,rang=i+2,lignes=lines[i:i+3],fenetre=words[i:i+3],
                            contexte=words[max(0,i-2):i+5],pos=[left,mid,right],cle=key,predit_nom=predicted))
                    elif left and mid and right:
                        neg[key][mid]+=1
    active=set()
    for e in events:
        key=tuple(e['cle']); n=neg[key]; e['temoins']=dict(n)
        if not e['predit_nom'] or not e['pos'][1]:continue
        gold['annonces']+=1;gold['bons']+=e['pos'][1]=='NN'
        if n:
            active.add(key);gold['annonces_appariees']+=1;gold['bons_apparies']+=e['pos'][1]=='NN'
            gold['esperance_appariee']+=n['NN']/sum(n.values())
    gold['temoins_distincts']=sum(neg[k].total() for k in active)
    assert len(events)==115
    save(HERE/'RIDGES-POS.json.gz',dict(source=sources,positions=events,classes=dict(alltags),bilan=dict(gold)))


if __name__=='__main__':run(Path(sys.argv[1]))
