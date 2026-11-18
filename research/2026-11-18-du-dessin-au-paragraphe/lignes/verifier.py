"""Ouvrir les seules lignes inférieures préenregistrées et simuler le déplacement de leurs mots."""
from collections import Counter,defaultdict
import numpy as np
from fichiers import HERE,load,save,digest
from masquer import corpus,lectures,units

SEED=991820
REPS=4999
LOTS=('pharmaceutique','f1-16','f103-116')


def summarize_null(draws,expected,hits,fixed,fixed_hits):
    above=int(np.count_nonzero(draws>=hits))
    return dict(attendu_exact=expected,au_moins=above,simulations=len(draws),
                proportion=above/len(draws),p_plus_un=(above+1)/(len(draws)+1),
                min=int(draws.min()),max=int(draws.max()),classes_singleton=fixed,
                succes_inevitables_dans_singletons=fixed_hits)


def shuffle_line(words,guesses,by_length,rng):
    buckets=defaultdict(list)
    for pos,word in enumerate(words):
        if 0<pos<len(words)-1 and word:
            key=len(units(word,False)) if by_length else 0
            buckets[key].append(pos)
    expected=0.0; draws=np.zeros(REPS,dtype=int); fixed=fixed_hits=0
    for positions in buckets.values():
        pinned=[(i,guesses[pos]) for i,pos in enumerate(positions) if pos in guesses]
        if not pinned:continue
        values=[words[pos] for pos in positions]; freq=Counter(values); n=len(values)
        expected+=sum(freq[w]/n for _,w in pinned)
        if n==1:
            fixed+=1; good=int(values[0]==pinned[0][1]);fixed_hits+=good;draws+=good
        elif len(freq)==1:
            draws+=sum(values[0]==w for _,w in pinned)
        else:
            codes={w:i for i,w in enumerate(sorted(freq),1)}
            permuted=rng.permuted(np.broadcast_to([codes[v] for v in values],(REPS,n)),axis=1)
            for i,w in pinned:draws+=permuted[:,i]==codes.get(w,0)
    return draws,expected,fixed,fixed_hits


def observe(sample,editions,rng):
    data={};by_page=defaultdict(Counter); counts=Counter(); arrays={k:np.zeros(REPS,dtype=int) for k in ('libre','longueur')}
    null={k:Counter() for k in arrays};matching=[]
    for page,record in sorted(sample.items()):
        counts['pages']+=1
        for line in record['paires']:
            words=lectures(line['bas'],editions,line['longueur']); guesses={};words_checked=[]
            counts['paires']+=1
            for call in line['annonces']:
                j=call['rang_bas']-1;off=call['decale']-1
                assert 0<j<len(words)-1 and 0<off<len(words)-1 and j not in guesses
                w=call['mot'];actual,shift=words[j],words[off]
                counts['annonces']+=1
                if actual:
                    guesses[j]=w; counts['lisibles']+=1; by_page[page]['lisibles']+=1
                    if w==actual:
                        counts['succes']+=1;by_page[page]['succes']+=1
                        matching.append(dict(haut=line['haut'],rang_haut=call['rang_haut'],bas=line['bas'],rang_bas=call['rang_bas'],mot=w))
                counts['decale_lisible']+=bool(shift);counts['decale_succes']+=w==shift
                if actual and shift:
                    counts['commun_lisible']+=1;counts['commun_vertical']+=w==actual;counts['commun_decale']+=w==shift
                words_checked.append(dict(rang=call['rang_bas'],observe=actual,observe_decale=shift))
            for k in arrays:
                simulations,expect,fixed,hits=shuffle_line(words,guesses,k=='longueur',rng)
                arrays[k]+=simulations;null[k]['attendu']+=expect
                null[k]['singleton']+=fixed;null[k]['singleton_ok']+=hits
            data[line['bas']]=words_checked
    counts.setdefault('succes',0)
    counts['inconnues']=counts['annonces']-counts['lisibles'];counts['echecs']=counts['lisibles']-counts['succes']
    result=dict(comptes=dict(counts),precision=counts['succes']/counts['lisibles'] if counts['lisibles'] else None,
        conditionnels={k:summarize_null(arrays[k],null[k]['attendu'],counts['succes'],null[k]['singleton'],null[k]['singleton_ok']) for k in arrays},
        par_page=dict(by_page),reussites=matching)
    return result,data,arrays


def main():
    snapshot=load('PREDICTIONS.json.gz');assert snapshot['carte']==digest(HERE/'CARTE-MASQUEE.json.gz')
    pages=snapshot['pages'];editions,_=corpus()
    rng=np.random.default_rng(SEED); results={};opened={};reserve={}
    for group in LOTS:
        selected={p:d for p,d in pages.items() if d['lot']==group}
        result,opened[group],arrays=observe(selected,editions,rng)
        results[group]=result
        if group!='pharmaceutique':reserve[group]=arrays
    both=[results[g] for g in LOTS[1:]]
    combined={}
    for k in ('libre','longueur'):
        ds=sum(r[k] for r in reserve.values()); info=[r['conditionnels'][k] for r in both]
        combined[k]=summarize_null(ds,sum(r['attendu_exact'] for r in info),sum(r['comptes']['succes'] for r in both),
            sum(r['classes_singleton'] for r in info),sum(r['succes_inevitables_dans_singletons'] for r in info))
    save('OUVERTURES.json.gz',opened)
    save('RESULTATS.json',dict(annonces_sha256=digest(HERE/'PREDICTIONS.json.gz'),graine=SEED,replications=REPS,
        lots=results,reserves_reunies=combined))


if __name__=='__main__':main()
