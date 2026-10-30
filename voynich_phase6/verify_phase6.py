#!/usr/bin/env python3
"""Recompute metrics from keys; independently check edit distances and saved null summaries."""
import collections, hashlib, json, math, random, re, sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import run_constrained as h
import adjacency_diagnostics as ad
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def lev(a,b):
    prev=list(range(len(b)+1))
    for i,x in enumerate(a,1):
        row=[i]
        for j,y in enumerate(b,1):row.append(min(row[-1]+1,prev[j]+1,prev[j-1]+(x!=y)))
        prev=row
    return prev[-1]
def main():
    h.prepare()
    initial=read(h.OUT/'initial_controls_summary.json'); controls=read(h.OUT/'warm_controls_summary.json'); rows=read(h.OUT/'constrained_real_summary.json')
    assert len(initial)==len(controls)==8 and len(rows)==64
    original={r['case']:r for r in read(h.P5/'results/controls_summary.json')+read(h.P5/'results/real_summary.json')}
    input_hashes={};real=[]
    for r in initial+controls+rows:
        inv=read(h.P5/'data'/f'{r["language"]}_{r["kind"]}_dictionary.json')['inventory']
        for part,label in [('train','train_metrics'),('test','test_metrics')]:
            path=h.P5/'data'/f'{r["case"]}_{part}.txt';input_hashes[str(path.relative_to(ROOT.parent))]=sha(path)
            m,dec,text=h.p5.metrics(h.lines(r['case'],part),r['key'],r['language'],r['kind'])
            for k,v in m.items():assert math.isclose(v,r[label][k],rel_tol=1e-11,abs_tol=1e-11)
            diag=h.join_diagnostics(dec,inv)
            assert diag['noncanonical_segments']==m['segments']-m['canonical_segments']
            if part=='train':
                assert diag['illegal_singleton_joins']==0 and m['canonical_segment_fraction']==1
                obj=-m['quadgrams']*m['bits_per_four_units']-4*m['units']*m['kl_to_model_bits']
                assert abs(obj-r['training_objective'])<1e-6*m['units']
            else: assert diag==r['test_segmentation']
        if r['run_tag']=='warm':
            supplied=list(map(int,(h.DATA/f'{r["case"]}_phase5_learned_key.txt').read_text().split()))
            assert supplied==original[r['case']]['key']
        if r['control']:
            truth=read(h.P5/'data'/f'{r["case"]}_truth.json')['truth_test']
            assert list(map(len,dec))==list(map(len,truth))
            n=sum(map(len,truth));err=sum(a!=b for x,y in zip(dec,truth) for a,b in zip(x,y))
            assert err==r['heldout_unit_errors'] and abs((1-err/n)-r['heldout_unit_accuracy'])<1e-12
            assert (''.join(text)==''.join(inv[x] for s in truth for x in s))==r['full_plaintext_exact']
        else:
            assert not set(r['fit_leaf_pool'])&set(r['test_leaves'])
            if not r['shuffled']:
                null=next(x for x in rows if x['case']==r['case'].replace('voynich_','null_',1))
                assert r['settings']==null['settings']
                for part in ['train','test']:
                    a=h.lines(r['case'],part);b=h.lines(null['case'],part)
                    assert len(a)==len(b) and all(collections.Counter(x)==collections.Counter(y) for x,y in zip(a,b))
                r['null_minus_real_bits']=null['test_metrics']['bits_per_four_units']-r['test_metrics']['bits_per_four_units']
                real.append(r)
    assert len(real)==32 and all(r['heldout_unit_accuracy']>=.95 for r in controls)
    # Rebuild inputs without rerunning randomizations; check observational geometry independently.
    ad.inputs();inputs=read(h.DATA/'adjacency_inputs.json');adj=read(h.OUT/'adjacency_summary.json')
    rng=random.Random(20261032);checks=0;pair_count=0
    for d,r in zip(inputs,adj):
        assert d['case']==r['case']
        words=sorted({w for line in d['lines'] for w in line['words'] if w is not None})
        pairs=[(a,b) for line in d['lines'] for a,b in zip(line['words'],line['words'][1:]) if a is not None and b is not None]
        assert len(pairs)==r['adjacent_pairs'] and d['retained_word_count']==r['words'];pair_count+=len(pairs)
        assert len(words)==r['types']
        for composed in [False,True]:
            matrix=ad.near_matrix(words,composed);units=[tuple(re.findall(h.p5.prev.UNITS,w)) if composed else tuple(w) for w in words]
            mp={w:i for i,w in enumerate(words)}
            # Check all observed distinct word pairs by ordinary dynamic programming.
            testpairs={(mp[a],mp[b]) for a,b in pairs}
            testpairs.update((rng.randrange(len(words)),rng.randrange(len(words))) for _ in range(1000))
            for a,b in testpairs:
                assert bool(matrix[a,b])==(lev(units[a],units[b])==1);checks+=1
            val=sum(matrix[mp[a],mp[b]] for a,b in pairs)/len(pairs)
            key='distinct_edit1_composed' if composed else 'distinct_edit1_EVA'
            assert abs(val-r['observed'][key])<1e-12
        assert abs(sum(a==b for a,b in pairs)/len(pairs)-r['observed']['identical_adjacent'])<1e-12
        joint=collections.Counter((a[-1],b[0]) for a,b in pairs);left=collections.Counter(a[-1] for a,b in pairs);right=collections.Counter(b[0] for a,b in pairs);n=len(pairs)
        mi=sum(c/n*math.log2(c*n/(left[a]*right[b])) for (a,b),c in joint.items())
        assert abs(mi-r['observed']['last_first_mutual_information_bits'])<1e-12
        for mode in ['all_page_slots','line_ends_fixed']:
            draws=np.array(read(h.OUT/f'adjacency_{r["case"]}_{mode}_draws.json'));assert draws.shape==(100,4)
            for i,key in enumerate(r['observed']):
                z=draws[:,i];s=r['nulls'][mode][key]
                vals={'mean':z.mean(),'p025':np.quantile(z,.025),'p975':np.quantile(z,.975),'observed_minus_mean':r['observed'][key]-z.mean(),'exploratory_upper_tail_p':(1+(z>=r['observed'][key]).sum())/101}
                assert all(abs(s[k]-v)<1e-12 for k,v in vals.items())
    group={}
    for lang in ['latin','italian']:
        for kind in ['CV','VC']:
            rr=[r for r in real if r['language']==lang and r['kind']==kind]
            best=min(rr,key=lambda r:r['test_metrics']['bits_per_four_units'])
            group[lang+'_'+kind]={'count':len(rr),'full_canonical_count':sum(r['test_metrics']['canonical_segment_fraction']==1 for r in rr),'test_canonical_min':min(r['test_metrics']['canonical_segment_fraction'] for r in rr),'bits_min':min(r['test_metrics']['bits_per_four_units'] for r in rr),'bits_max':max(r['test_metrics']['bits_per_four_units'] for r in rr),'matched_null_beaten':sum(r['null_minus_real_bits']>0 for r in rr),'best_post_hoc':best['case'],'best_two_letter_fraction':best['test_segmentation']['two_letter_unit_fraction'],'best_distinct_units':best['test_metrics']['output_distinct_units']}
    summary={'verdict':'Aucune traduction validee. Exploratory limited models, no family-wide rejection.','date':'2026-10-28','new_solver_runs':80,'real_count':32,'null_count':32,'all_real_train_canonical':True,'real_full_canonical_count':sum(r['test_metrics']['canonical_segment_fraction']==1 for r in real),'baseline_phase5_full_canonical_count':sum(r['baseline_phase5_test_metrics']['canonical_segment_fraction']==1 for r in real),'groups':group,'controls':[{'case':r['case'],'errors':r['heldout_unit_errors'],'accuracy':r['heldout_unit_accuracy'],'test_canonical':r['test_metrics']['canonical_segment_fraction']} for r in controls],'initial_control_accuracies':{r['case']:r['heldout_unit_accuracy'] for r in initial},'adjacency_randomizations':1600,'adjacency_source_counts':[{k:d[k] for k in ['case','source_word_count_before_template','retained_word_count']} for d in inputs]}
    h.save(h.OUT/'summary.json',summary);h.save(h.OUT/'input_sha256.json',input_hashes)
    h.save(h.OUT/'verification.json',{'status':'PASS','solver_objectives_recomputed':80,'control_accuracies_recomputed':16,'real_null_histogram_pairs':32,'train_test_physical_leaf_disjoint':True,'all_warm_starts_match_learned_phase5_keys':True,'adjacency_pairs_recounted':pair_count,'independent_Levenshtein_comparisons':checks,'null_draws_summary_checked':1600,'not_verified':['semantic interpretation','exhaustive search','historical plausibility of all coding choices','expert blind image reading','independent reproduction of external studies']})
    print(json.dumps(summary,ensure_ascii=False,indent=2));print('VERIFICATION PASS',checks,'edit-distance checks')
if __name__=='__main__':main()
