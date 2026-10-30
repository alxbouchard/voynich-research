#!/usr/bin/env python3
"""Independent Python scoring/segmentation for the open model. CC BY-SA 4.0."""
import itertools
import math
from functools import lru_cache
import numpy as np
import common as c


class Reference:
    def __init__(self,language):
        folder=c.TMP/'open'/language
        rows=[line.split() for line in (folder/'words.tsv').read_text().splitlines()]
        self.ids={w:i+1 for i,(w,p) in enumerate(rows)}
        self.w1={i+1:float(p) for i,(w,p) in enumerate(rows)}
        self.w2={};self.w3={}
        for n,name,target in ((2,'bigrams.tsv',self.w2),(3,'trigrams.tsv',self.w3)):
            for line in (folder/name).read_text().splitlines():
                fields=line.split();target[tuple(map(int,fields[:n]))]=float(fields[n])
        self.char=[None]+[np.fromfile(folder/f'char{n}.bin').reshape((27,)*n) for n in (1,2,3)]
        self.spell=np.fromfile(folder/'spelling.bin').reshape(28,28,28,27)
        self.length=np.fromfile(folder/'length.bin')

    @lru_cache(maxsize=100000)
    def word_log(self,history,wid):
        context=history+(wid,)
        value=c.WL[0]*self.w1[wid]
        if len(context)>1:value+=c.WL[1]*self.w2.get(context[-2:],0)
        if len(context)>2:value+=c.WL[2]*self.w3.get(context[-3:],0)
        return math.log(value)

    def char_log(self,history,token):
        ctx=tuple(history)+(token,)
        return self.char_context(ctx)

    @lru_cache(maxsize=30000)
    def char_context(self,ctx):
        return math.log(sum(c.CL[n-1]*self.char[n][ctx[-n:]] for n in (1,2,3) if len(ctx)>=n))

    def emission(self,word,beta,penalty):
        if word in self.ids:return 0.
        assert 1<=len(word)<=c.MAX_UNKNOWN
        context=[27,27,27];value=0.
        for nxt in [*[ord(x)-97 for x in word],26]:
            value+=self.spell[tuple(context)+(nxt,)];context=(context+[nxt])[-3:]
        return beta*value+float(self.length[len(word)-1])-penalty

    def full(self,text,beta,penalty):
        words=text.split();history=();lex=0.;emit=0.
        for word in words:
            wid=self.ids.get(word,1);lex+=self.word_log(history,wid)
            emit+=self.emission(word,beta,penalty);history=(history+(wid,))[-2:]
        seq=[26 if x==' ' else ord(x)-97 for x in text]
        chars=sum(self.char_log(seq[max(0,i-2):i],token) for i,token in enumerate(seq))
        return .95*lex+.05*chars+emit

    def exact(self,text,beta,penalty):
        states=[{} for _ in range(len(text)+1)];states[0][((),())]=(0.,())
        for pos in range(len(text)):
            edges=[];char_cache={}
            for end in range(pos+1,min(len(text),pos+c.MAX_UNKNOWN)+1):
                word=text[pos:end];wid=self.ids.get(word,1)
                edges.append((end,word,wid,self.emission(word,beta,penalty)))
            for (words,chars),(score,path) in states[pos].items():
                for end,word,wid,emit in edges:
                    cachekey=(chars,end)
                    if cachekey not in char_cache:
                        hist=chars;add=0.
                        for nxt in ([26] if pos else [])+[ord(x)-97 for x in word]:
                            add+=self.char_log(hist,nxt);hist=(hist+(nxt,))[-2:]
                        char_cache[cachekey]=(add,hist)
                    add,hist=char_cache[cachekey]
                    wh=(words+(wid,))[-2:];value=score+.95*self.word_log(words,wid)+.05*add+emit
                    key=(wh,hist)
                    if key not in states[end] or value>states[end][key][0]:states[end][key]=(value,path+(word,))
        value,path=max(states[-1].values(),key=lambda x:x[0]);result=' '.join(path)
        assert abs(value-self.full(result,beta,penalty))<1e-8*len(text)
        return {'score':value,'segmentation':result}

    def exhaustive(self,text,beta,penalty):
        best=(-math.inf,'');count=0
        for mask in itertools.product((False,True),repeat=len(text)-1):
            parts=[];start=0
            for i,cut in enumerate(mask,1):
                if cut:parts.append(text[start:i]);start=i
            parts.append(text[start:])
            if max(map(len,parts))>c.MAX_UNKNOWN:continue
            s=' '.join(parts);score=self.full(s,beta,penalty);count+=1
            if score>best[0]:best=(score,s)
        return {'score':best[0],'segmentation':best[1],'paths':count}
