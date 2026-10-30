#!/usr/bin/env python3
"""Independent exact/constrained Python calculation. CC BY-SA 4.0."""
import itertools
import math
import numpy as np
import phase22lib as c
from reference import Reference as Phase21Reference


class Reference(Phase21Reference):
    def __init__(self,language):
        super().__init__(language)
        folder=c.TMP/'open'/language
        self.p2=np.fromfile(folder/'boundary2.bin')
        self.p3={}
        for line in (folder/'boundary3.tsv').read_text().splitlines():
            key,p=line.split();self.p3[int(key)]=float(p)

    def probabilities(self,text):
        padded='___'+text+'___';result={}
        for i in range(1,len(text)):
            context=padded[i:i+6];code=0
            for ch in context:code=code*27+(26 if ch=='_' else ord(ch)-97)
            result[i]=self.p3.get(code,float(self.p2[(code//27)%(27**4)]))
        return result

    def corrected_score(self,segmented,baseline,weight,threshold):
        old=c.cuts(baseline);new=c.cuts(segmented);assert old<=new
        assert baseline.replace(' ','')==segmented.replace(' ','')
        probs=self.probabilities(segmented.replace(' ',''));value=self.full(segmented,1.,0.)
        for gap in new-old:
            assert probs[gap]>=threshold
            value+=weight*math.log(probs[gap]/(1-probs[gap]))
        return value

    def constrained(self,text,weight,threshold):
        baseline=self.exact(text,1.,0.);old=c.cuts(baseline['segmentation']);probs=self.probabilities(text)
        states=[{} for _ in range(len(text)+1)];states[0][((),())]=(0.,())
        for pos in range(len(text)):
            edges=[];char_cache={}
            for end in range(pos+1,min(len(text),pos+24)+1):
                if any(pos<cut<end for cut in old):continue
                if end<len(text) and end not in old and probs[end]<threshold:continue
                word=text[pos:end];wid=self.ids.get(word,1);bonus=0.
                if end<len(text) and end not in old:bonus=weight*math.log(probs[end]/(1-probs[end]))
                edges.append((end,word,wid,self.emission(word,1.,0.)+bonus))
            for (words,chars),(score,path) in states[pos].items():
                for end,word,wid,emission in edges:
                    ck=(chars,end)
                    if ck not in char_cache:
                        hist=chars;add=0.
                        for nxt in ([26] if pos else [])+[ord(x)-97 for x in word]:
                            add+=self.char_log(hist,nxt);hist=(hist+(nxt,))[-2:]
                        char_cache[ck]=(add,hist)
                    add,hist=char_cache[ck];wh=(words+(wid,))[-2:]
                    value=score+.95*self.word_log(words,wid)+.05*add+emission;key=(wh,hist)
                    candidate=(value,path+(word,));previous=states[end].get(key)
                    if previous is None or value>previous[0]+1e-12 or (abs(value-previous[0])<=1e-12 and len(candidate[1])<len(previous[1])):
                        states[end][key]=candidate
        value,path=max(states[-1].values(),key=lambda x:(x[0],-len(x[1])))
        if value<=baseline['score']+1e-9:return {'baseline':baseline,'corrected':baseline}
        text_out=' '.join(path)
        assert abs(value-self.corrected_score(text_out,baseline['segmentation'],weight,threshold))<1e-8*len(text)
        return {'baseline':baseline,'corrected':{'score':value,'segmentation':text_out}}

    def exhaustive_constrained(self,text,baseline,weight,threshold):
        old=c.cuts(baseline);probs=self.probabilities(text);best=(self.full(baseline,1.,0.),baseline)
        considered=0;legal=0
        for mask in itertools.product((False,True),repeat=len(text)-1):
            considered+=1;new={i for i,flag in enumerate(mask,1) if flag}
            if not old<=new or any(probs[i]<threshold for i in new-old):continue
            starts=[0]+sorted(new);ends=sorted(new)+[len(text)]
            if any(end-start>24 for start,end in zip(starts,ends)):continue
            legal+=1;text_out=' '.join(text[a:b] for a,b in zip(starts,ends))
            score=self.corrected_score(text_out,baseline,weight,threshold)
            if score>best[0]+1e-9:best=(score,text_out)
        return {'score':best[0],'segmentation':best[1],'considered':considered,'legal':legal}
