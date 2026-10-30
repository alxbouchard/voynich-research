#!/usr/bin/env python3
"""Post-result explanation only; never tunes or changes the frozen method. CC BY-SA 4.0."""
import math
import phase22lib as c
from boundary_reference import Reference


def main():
    summary=c.read(c.OUT/'summary.json');p=c.read(c.ROOT/'PROTOCOL.json');rows=[]
    for language in p['languages']:
        model=Reference(language)
        for case in summary['cases']:
            if case['language']!=language:continue
            truth=c.read(c.DATA/'controls'/case['case']/'truth.json')
            for mode in ('recovered','oracle'):
                for split in ('fit','transfer'):
                    baseline=case['rows'][mode][split]['baseline'];text=baseline['segmentation'];letters=text.replace(' ','')
                    old=c.cuts(text);gold=c.cuts(truth['plaintext_'+split]);probs=model.probabilities(letters)
                    missing=gold-old;eligible={x for x in probs if x not in old and probs[x]>=p['threshold']}
                    changes=[]
                    for gap in sorted(eligible):
                        positions=[0]+sorted(old|{gap})+[len(letters)]
                        candidate=' '.join(letters[a:b] for a,b in zip(positions,positions[1:]))
                        gain=model.full(candidate,1.,0.)-model.full(text,1.,0.)+p['weight']*math.log(probs[gap]/(1-probs[gap]))
                        changes.append({'gap':gap,'true_boundary':gap in gold,'context_probability':probs[gap],'isolated_cut_score_gain':gain})
                    rows.append({'case':case['case'],'language':language,'mode':mode,'split':split,
                        'missing_boundaries':len(missing),'missing_below_context_threshold':sum(probs[x]<p['threshold'] for x in missing),
                        'missing_eligible':len(missing&eligible),'false_eligible':len(eligible-gold),
                        'eligible_single_cut_diagnostics':changes})
    totals={}
    for mode in ('recovered','oracle'):
        values=[x for x in rows if x['mode']==mode and x['split']=='transfer']
        totals[mode]={k:sum(x[k] for x in values) for k in ('missing_boundaries','missing_below_context_threshold','missing_eligible','false_eligible')}
        gains=[r['isolated_cut_score_gain'] for x in values for r in x['eligible_single_cut_diagnostics'] if r['true_boundary']]
        totals[mode]['best_isolated_missing_cut_gain']=max(gains) if gains else None
    c.save(c.OUT/'posthoc_diagnostic.json',{'scope':'Added after results; descriptive, not preregistered, no parameter selection or new fitting. Single-cut gains do not enumerate joint changes.',
        'transfer_totals':totals,'cases':rows})
    print(totals,flush=True)


if __name__=='__main__':main()
