#!/usr/bin/env python3
"""Select open-word penalties using phase-20 passages only. CC BY-SA 4.0."""
import json
import random
import time
import common as c
from reference import Reference


def main():
    plan=c.read(c.ROOT/'DEVELOPMENT_PLAN.json')
    c.compile_solver();checks=[]
    for language in ('latin','italian'):
        model=c.build_model(language);c.save(c.DATA/(language+'_models.json'),model)
        reference=Reference(language);rng=random.Random(plan['verification_seed'])
        tests=[''.join(rng.choice('aeirsxz') for _ in range(8)) for _ in range(8)]
        rows=[(b,g,text) for text in tests for b,g in ((.25,0),(1.,6))]
        outputs=c.batch(language,rows,c.TMP/(language+'_unit.txt'))
        for (beta,penalty,text),actual in zip(rows,outputs):
            expected=reference.exhaustive(text,beta,penalty)
            dynamic=reference.exact(text,beta,penalty)
            error=max(abs(actual['score']-expected['score']),abs(dynamic['score']-expected['score']))
            assert error<1e-8
            checks.append({'language':language,'text':text,'beta':beta,'penalty':penalty,
                           'paths':expected['paths'],'maximum_score_error':error})
    c.save(c.OUT/'development/verification.json',{'passed':True,'checks':checks})
    all_rows=[]
    for language in ('latin','italian'):
        sources=[]
        for case in c.read(c.OLD/'data/calibration/cases.json'):
            if case['language']!=language:continue
            truth=c.read(c.OLD/'data/calibration'/case['case']/'truth.json')
            for split in ('fit','transfer'):
                sources.append((case['case'],split,truth['plaintext_'+split]))
        jobs=[(beta,penalty,text.replace(' ','')) for beta in plan['beta_grid']
              for penalty in plan['penalty_grid'] for name,split,text in sources]
        start=time.monotonic()
        print(json.dumps({'development_language':language,'segmentations':len(jobs)}),flush=True)
        outputs=c.batch(language,jobs,c.TMP/(language+'_development.txt'))
        i=0
        for beta in plan['beta_grid']:
            for penalty in plan['penalty_grid']:
                for name,split,text in sources:
                    actual=outputs[i];i+=1
                    metrics=c.previous.metrics(actual['segmentation'],text)
                    all_rows.append({'language':language,'case':name,'split':split,'beta':beta,
                        'penalty':penalty,'metrics':metrics,'output':actual})
        print(json.dumps({'development_completed':language,'seconds':time.monotonic()-start}),flush=True)
    scores=[]
    for beta in plan['beta_grid']:
        for penalty in plan['penalty_grid']:
            rows=[r for r in all_rows if r['beta']==beta and r['penalty']==penalty]
            scores.append({'beta':beta,'penalty':penalty,
                           'macro_boundary_f1':sum(r['metrics']['boundary_f1'] for r in rows)/len(rows)})
    winner=max(scores,key=lambda r:(r['macro_boundary_f1'],r['beta'],r['penalty']))
    c.save(c.OUT/'development/grid.json',{'selection_rule':plan['selection_rule'],'scores':scores,'selected':winner,
           'rows':all_rows,'scope':'Development only; plaintext known and used to select parameters. Not a held-out result.'})
    print(json.dumps({'selected':winner}),flush=True)


if __name__=='__main__':main()
