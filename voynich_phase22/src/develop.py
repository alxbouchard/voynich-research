#!/usr/bin/env python3
"""Choose conservative cuts on old passages; never on new tests. CC BY-SA 4.0."""
from collections import Counter
import json
import random
import shutil
import numpy as np
import phase22lib as c
from boundary_reference import Reference


def verify_classifier(language):
    words=(c.REPO/f'voynich_phase10/data/{language}_train_boundary.txt').read_text().split()
    text=''.join(words);cuts=c.cuts(' '.join(words));padded='___'+text+'___'
    counts=[Counter() for _ in range(3)];positive=[Counter() for _ in range(3)]
    for i in range(1,len(text)):
        for r in (1,2,3):
            ctx=padded[i+3-r:i+3+r];counts[r-1][ctx]+=1
            if i in cuts:positive[r-1][ctx]+=1
    reference=Reference(language);rng=random.Random(220030001);errors=[]
    for i in rng.sample(range(1,len(text)),128):
        prob=len(cuts)/(len(text)-1)
        for r in (1,2,3):
            ctx=padded[i+3-r:i+3+r];prob=(positive[r-1][ctx]+20*prob)/(counts[r-1][ctx]+20)
        code=0
        for char in padded[i:i+6]:code=code*27+(26 if char=='_' else ord(char)-97)
        actual=reference.p3.get(code,float(reference.p2[(code//27)%(27**4)]))
        errors.append(abs(actual-prob))
    assert max(errors)<1e-12
    return {'language':language,'contexts_checked':len(errors),'maximum_error':max(errors)}


def main():
    plan=c.read(c.ROOT/'DEVELOPMENT_PLAN.json');c.compile_solvers();checks=[];classifier=[]
    for language in ('latin','italian'):
        info=c.build_model(language);c.save(c.DATA/(language+'_models.json'),info)
        classifier.append(verify_classifier(language))
        synthetic='unit_'+language
        destination=c.TMP/'open'/synthetic;destination.mkdir(parents=True,exist_ok=True)
        for p in (c.TMP/'open'/language).iterdir():shutil.copyfile(p,destination/p.name)
        np.full(27**4,.95).tofile(destination/'boundary2.bin');(destination/'boundary3.tsv').write_text('')
        rng=random.Random(plan['verification_seed'])
        tests=[''.join(rng.choice('aeirstxz') for _ in range(8)) for _ in range(8)]
        for model,settings in ((language,[(1.,.9)]),(synthetic,[(0.,.9),(4.,.9)])):
            ref=Reference(model);jobs=[(weight,threshold,text) for text in tests for weight,threshold in settings]
            outputs=c.batch(model,jobs,c.TMP/(model+'_checks.txt'))
            for (weight,threshold,text),out in zip(jobs,outputs):
                baseline=ref.exact(text,1.,0.)
                assert abs(out['baseline']['score']-baseline['score'])<1e-8
                exact=ref.exhaustive_constrained(text,baseline['segmentation'],weight,threshold)
                dynamic=ref.constrained(text,weight,threshold)
                error=max(abs(out['corrected']['score']-exact['score']),abs(dynamic['corrected']['score']-exact['score']))
                assert error<1e-8
                checks.append({'model':model,'text':text,'weight':weight,'threshold':threshold,
                    'considered':exact['considered'],'legal':exact['legal'],'maximum_score_error':error,
                    'added_count':len(out['added_positions'])})
    assert any(r['added_count'] for r in checks)
    c.save(c.OUT/'development/verification.json',{'passed':True,'classifier':classifier,'checks':checks})
    all_rows=[]
    for language in ('latin','italian'):
        sources=[(phase,name,split,truth['plaintext_'+split]) for phase,name,lang,path,truth in c.old_cases()
                 if lang==language for split in ('fit','transfer')]
        jobs=[(weight,threshold,text.replace(' ','')) for threshold in plan['threshold_grid']
              for weight in plan['weight_grid'] for phase,name,split,text in sources]
        print(json.dumps({'development':language,'segmentations':len(jobs)}),flush=True)
        outputs=c.batch(language,jobs,c.TMP/(language+'_development.txt'));i=0
        for threshold in plan['threshold_grid']:
            for weight in plan['weight_grid']:
                for phase,name,split,truth in sources:
                    out=outputs[i];i+=1;delta=c.differences(out['baseline']['segmentation'],out['corrected']['segmentation'],truth)
                    all_rows.append({'phase':phase,'case':name,'language':language,'split':split,
                                     'threshold':threshold,'weight':weight,'comparison':delta,'output':out})
    scores=[]
    for threshold in plan['threshold_grid']:
        for weight in plan['weight_grid']:
            rows=[x for x in all_rows if x['threshold']==threshold and x['weight']==weight]
            bylang={lang:sum(r['comparison']['added_correct_cuts'] for r in rows if r['language']==lang) for lang in ('latin','italian')}
            bad=sum(r['comparison']['added_false_cuts'] for r in rows)
            scores.append({'threshold':threshold,'weight':weight,'corrected_fusions':sum(bylang.values()),
                           'introduced_false_cuts':bad,'corrected_by_language':bylang,
                           'strict_eligible':bad==0 and min(bylang.values())>0})
    strict=[r for r in scores if r['strict_eligible']]
    if strict:selected=max(strict,key=lambda r:(r['corrected_fusions'],r['threshold'],-r['weight']))
    else:
        useful=[r for r in scores if min(r['corrected_by_language'].values())>0]
        selected=min(useful,key=lambda r:(r['introduced_false_cuts'],-r['corrected_fusions'],-r['threshold'],r['weight'])) if useful else {'weight':0.,'threshold':1.,'strict_eligible':False}
    c.save(c.OUT/'development/grid.json',{'scores':scores,'selected':selected,'rows':all_rows,
           'scope':'Known letters and boundaries used for development; not held-out performance.'})
    print(json.dumps({'selected':selected}),flush=True)


if __name__=='__main__':main()
