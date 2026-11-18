"""Énumérer les motifs identiques entre dessins et contrôler l’ordre des lignes."""
from collections import Counter, defaultdict
from random import Random
import re
from chercher import display, herb, save

TARGET=('chol','cthy','daiin')

def motifs(lines):
    output=defaultdict(set)
    for n,pairs in lines.items():
        left=defaultdict(list);right=defaultdict(list)
        for a,m in pairs:
            if a!=m:left[m].append(a)
        for b,m in lines.get(n+2,{}):
            if b!=m:right[m].append(b)
        for m in left.keys() & right.keys():
            output[n].update((a,m,b) for a in left[m] for b in right[m] if a!=b)
    return output

def shared(rows):
    return {w:data for w,data in rows.items() if len({p[0] for p in data})>=2}

def score(pages,randomizer=None):
    all_pos=defaultdict(set);same_line=defaultdict(set)
    for page,ordered in pages.items():
        physical=int(re.match(r'f(\d+)',page)[1])
        if randomizer:
            vals=list(ordered.values());randomizer.shuffle(vals);lines=dict(zip(ordered,vals))
        else:lines=ordered
        for n,words in motifs(lines).items():
            for w in words:
                all_pos[w].add((physical,page,n));same_line[w,n].add((physical,page,n))
    broad=shared(all_pos);fixed=shared(same_line);matches={k[0] for k in fixed}
    return (len(broad),len(matches),TARGET in matches),broad,fixed

def main():
    raw=herb()
    pages={p:{n:{tuple(map(display,pair)) for pair in data} for n,data in lines.items()} for p,lines in raw.items()}
    observed,broad,fixed=score(pages)
    rng=Random(111503)
    samples=[score(pages,rng)[0] for i in range(999)]
    detail=lambda w,places:{'A':w[0],'M':w[1],'B':w[2],'lieux':sorted(places)}
    result={'observation':observed,'tous_motifs_repetes':[detail(w,ps) for w,ps in sorted(broad.items())],
            'motifs_meme_ligne':[detail(w,ps)|{'ligne_A':n} for (w,n),ps in sorted(fixed.items())],
            '999_tirages':[list(k)+[n] for k,n in sorted(Counter(samples).items())],
            'tirages_au_moins_autant_motifs':[sum(row[i]>=observed[i] for row in samples) for i in (0,1)],
            'tirages_avec_cible_meme_ligne':sum(row[2] for row in samples),
            'tirages_avec_motif_quelconque_meme_ligne':sum(row[1]>0 for row in samples)}
    save('positions.json',result)
    print(observed,result['tirages_au_moins_autant_motifs'],result['tirages_avec_cible_meme_ligne'],
          result['tirages_avec_motif_quelconque_meme_ligne'],result['motifs_meme_ligne'])
if __name__=='__main__':main()
