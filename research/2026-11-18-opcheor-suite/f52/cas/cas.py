"""Appliquer cinq mots latins gelés et contrôler les cas de la phrase anatomique."""
from collections import Counter, defaultdict
from pathlib import Path
import argparse,json,re,sys
HERE=Path(__file__).resolve().parent
RESEARCH=HERE.parents[2]
sys.path.insert(0,str(RESEARCH/'2026-11-18-phrase-et-doublets/lecture'))
from corpus_sources import celsus
sys.path.insert(0,str(RESEARCH/'2026-11-18-d-initial-et-formules'))
from suites import windows
LATIN=dict(zip(('ctheor','ctheol','cheeor','cheol','chckheey'),
               ('digiti','digitis','ungues','unguibus','respondent')))
PAIRS={'ctheor':'ctheol','ctheol':'cheeor','cheeor':'cheol','cheol':'chckheey'}
REVERSED={'ctheol':'ctheor','cheol':'cheeor'}

def count_historical(xml):
    source=celsus(xml,r'[.;:!?]')
    loc=[]; rest=[];voc=Counter()
    for k,words in source.items():
        if k.startswith('8.1.'):
            if all(a in words for a in LATIN.values()):
                pos=words.index('digitis')-1
                if words[pos:pos+5]==list(LATIN.values()):
                    loc.append([k,words[max(0,pos-4):pos+7]])
            continue
        voc.update(w for w in words if w in LATIN.values())
        for i in range(len(words)-1):
            for n in (2,3):
                phrase=words[i:i+n]
                if len(phrase)==n and all(w in LATIN.values() for w in phrase):
                    rest.append([k,i+1,phrase])
    return {'source':loc,'attestations_hors_VIII_1':voc,'suites_hors_VIII_1':rest}

def main(mode,xml):
    announced=HERE/'ANNONCES.json'
    if mode=='annoncer':
        research=count_historical(xml)
        research['projections']=[]
        for r in windows():
            if re.match(r'f52[rv]',r['page']) or r['ancre'] not in LATIN:continue
            a=r['ancre']
            research['projections'].append({'lieu':r['lieu'],'mot':a,'direct':PAIRS.get(a),
                                           'inverse':REVERSED.get(a)})
        announced.write_text(json.dumps(research,indent=1,ensure_ascii=False)+'\n');return
    research=json.loads(announced.read_bytes())
    trials={r['lieu']:r for r in research['projections']}
    prev=Counter();same=Counter();flags=Counter()
    out=[]
    for r in windows():
        if re.match(r'f52[rv]',r['page']):continue
        a=r['ancre'];left=LATIN.get(a)
        if r['lieu'] in trials:
            p=trials.pop(r['lieu']);y=r['suite'][0] if r['suite'] else None
            p['observe']=y
            for case in ('direct','inverse'):
                if p[case] is None:continue
                label=f'{a}/{case}'
                prev[label]+=1
                if y is not None:flags[label]+=1;same[label]+=y==p[case]
            out.append(p)
        if left:
            for n in (1,2):
                rest=r['suite'][:n]
                if len(rest)!=n or not all(w in LATIN for w in rest):continue
                key=' '.join(LATIN[w] for w in [a,*rest])
                flags['voynich/'+key]+=1
    assert not trials
    scores={k:[same[k],flags[k],v-flags[k]] for k,v in prev.items()}
    result={'justes_evaluables_inconnues':scores,'suites_en_clair_sur_le_voynich':
            {k:v for k,v in flags.items() if k.startswith('voynich/')},'loci':out}
    (HERE/'RESULTATS.json').write_text(json.dumps(result,indent=1,ensure_ascii=False)+'\n')

if __name__=='__main__':
    par=argparse.ArgumentParser(description=__doc__)
    par.add_argument('mode',choices=['annoncer','ouvrir'])
    par.add_argument('xml',type=Path)
    args=par.parse_args();main(args.mode,args.xml)
