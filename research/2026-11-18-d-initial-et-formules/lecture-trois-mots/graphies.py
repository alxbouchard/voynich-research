"""Éprouver les trois graphies exactes de Celse avec les mêmes contraintes de lecture."""
from chercher import HERE,PREFIX,SHORT,U,extend
import json

WITNESSES={'florence_1478':['orae','esse','compressae'],
           'clm_69_lecture_proposee':['fore','esse','comprehense'],
           'edition_spencer':['orae','esse','conpressae']}

def solve(plain,shape,cap):
    tables=[{}]
    for word,units in zip(plain,shape):
        tables=[n for m in tables for n in extend(units,word,cap,m)]
    return tables

def main():
    result={}
    for source,words in WITNESSES.items():
        byform={}
        for base,(pre,second) in enumerate(PREFIX):
            for kind,third in [('long',U+('d','y')),('court',SHORT)]:
                for omit in [False,True] if base==0 else [False]:
                    first=pre[1:] if omit else pre
                    for cap in [1,2]:
                        k=f'{base}/{kind}/'+('muet' if omit else 'lu')+f'/{cap}'
                        byform[k]=solve(words,(first,second,third),cap)
        result[source]={'latin':words,'lectures':byform}
    (HERE/'GRAPHIES.json').write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=1)+'\n')
if __name__=='__main__':main()
