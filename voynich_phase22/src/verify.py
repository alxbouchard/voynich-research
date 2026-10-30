#!/usr/bin/env python3
"""Independent phase-22 provenance, metrics and exact DP audit. CC BY-SA 4.0."""
from collections import defaultdict
import hashlib
import json
import subprocess
import phase22lib as c
import study
from boundary_reference import Reference


def measured(text,truth):
    def parse(s):
        letters=[];boundaries=set()
        for x in s:
            if x==' ':boundaries.add(len(letters))
            else:letters.append(x)
        boundaries.discard(0);boundaries.discard(len(letters));return letters,boundaries
    a,ap=parse(text);b,bp=parse(truth);assert len(a)==len(b)
    return {'character_accuracy':sum(x==y for x,y in zip(a,b))/len(b),
            'boundary_f1':2*len(ap&bp)/(len(ap)+len(bp)) if ap or bp else 1.},ap,bp


def main():
    p=study.check_inputs();summary=c.read(c.OUT/'summary.json');env=c.read(c.DATA/'environment.json');base=env['run_base_commit']
    assert hashlib.sha256(subprocess.check_output(['git','show',base+':voynich_phase22/PROTOCOL.json'],cwd=c.REPO)).hexdigest()==c.sha(study.PFILE)
    for path,digest in p['sha256'].items():
        if '/src/' in path or path.endswith('DEVELOPMENT_PLAN.json') or path.startswith('voynich_phase22/results/development/'):
            assert hashlib.sha256(subprocess.check_output(['git','show',base+':'+path],cwd=c.REPO)).hexdigest()==digest
    raw={x['case']:x for x in c.read(c.REPO/'voynich_phase10/data/source_inputs.json')}
    old_ranges=defaultdict(list);old_keys=set()
    for _,_,lang,_,truth in c.old_cases():
        old_ranges[lang].extend(truth['source_word_ranges'].values());old_keys.add(truth['encryption_key'])
    current=defaultdict(list);new_keys=set();checked=0;optima=0;maximum_error=0.;all_changes=[]
    for language in p['languages']:
        model=Reference(language)
        for case in summary['cases']:
            if case['language']!=language:continue
            name=case['case'];folder=c.DATA/'controls'/name;truth=c.read(folder/'truth.json')
            assert truth['source']==p['languages'][language]
            words=[w for line in raw[truth['source']]['lines'] for w in line['words'] if w]
            assert truth['encryption_key'] not in old_keys|new_keys;new_keys.add(truth['encryption_key'])
            assert len(truth['encryption_key'])==26 and set(truth['encryption_key'])==set(c.ALPHABET)
            for split,(start,end) in truth['source_word_ranges'].items():
                assert ' '.join(words[start:end])==truth['plaintext_'+split];current[language].append((start,end))
                for a,b in old_ranges[language]:assert end<=a-p['old_passage_buffer_words'] or start>=b+p['old_passage_buffer_words']
            for mode in ('initializer','key'):
                command=c.read(c.OUT/'controls'/name/(mode+'.json'))['identity']['command']
                assert command[3]==str(folder/'fit.txt')
                assert all('transfer' not in arg and 'truth' not in arg and 'boundary_solver' not in arg for arg in command)
            for mode,row in case['rows'].items():
                key=row['key'];assert set(key)==set(c.ALPHABET) and len(key)==26
                if mode=='recovered':assert key==c.read(c.OUT/'controls'/name/'key.json')['result']['key']
                else:assert all(key[ord(ch)-97]==c.ALPHABET[i] for i,ch in enumerate(truth['encryption_key']))
                for split in ('fit','transfer'):
                    ciphertext=(folder/(split+'.txt')).read_text().strip();expected=truth['plaintext_'+split]
                    assert ''.join(truth['encryption_key'][ord(x)-97] for x in expected if x!=' ')==ciphertext
                    decoded=''.join(key[ord(x)-97] for x in ciphertext);value=row[split]
                    independent=model.constrained(decoded,p['weight'],p['threshold']);optima+=2
                    boundaries={}
                    for arm in ('baseline','corrected'):
                        text=value[arm]['segmentation'];assert text.replace(' ','')==decoded
                        metrics,boundaries[arm],gold=measured(text,expected)
                        for field,number in metrics.items():assert abs(number-value[arm][field])<1e-12
                        score=model.full(text,1.,0.) if arm=='baseline' else model.corrected_score(text,value['baseline']['segmentation'],p['weight'],p['threshold'])
                        error=max(abs(score-value[arm]['score']),abs(score-independent[arm]['score']))
                        maximum_error=max(maximum_error,error);assert error<1e-8*len(decoded);checked+=1
                    old=boundaries['baseline'];new=boundaries['corrected'];assert old<=new
                    added=new-old;assert sorted(added)==value['added_positions']
                    expected_changes={'added_correct_cuts':len(added&gold),'added_false_cuts':len(added-gold),
                        'baseline_fp':len(old-gold),'corrected_fp':len(new-gold),'baseline_fn':len(gold-old),'corrected_fn':len(gold-new),
                        'baseline_f1':value['baseline']['boundary_f1'],'corrected_f1':value['corrected']['boundary_f1']}
                    for field,number in expected_changes.items():assert abs(value['changes'][field]-number)<1e-12
                    assert len(gold-new)<=len(gold-old) and len(new-gold)-len(old-gold)==len(added-gold)
                    all_changes.append({'case':name,'mode':mode,'split':split,**expected_changes})
            m=case['rows']['recovered']['transfer']['corrected']
            assert case['passes_gate']==(m['character_accuracy']>=p['gate']['character_accuracy'] and m['boundary_f1']>=p['gate']['boundary_f1'])
            print(json.dumps({'verified':name}),flush=True)
    for intervals in current.values():
        ordered=sorted(intervals);assert all(a[1]<=b[0] for a,b in zip(ordered,ordered[1:]))
    assert len(summary['cases'])==12 and len(new_keys)==12
    assert summary==study.aggregate(summary['cases'],p)
    transfer=[x for x in all_changes if x['mode']=='recovered' and x['split']=='transfer']
    strict=all(sum(x['added_correct_cuts'] for x in transfer if x['case'].startswith(lang))>0 for lang in p['languages']) and sum(x['added_false_cuts'] for x in transfer)==0
    assert strict==summary['strict_task_success']
    c.save(c.OUT/'verification.json',{'passed':True,'scored_outputs_checked':checked,'exact_optima_recomputed':optima,
        'maximum_score_difference':maximum_error,'source_excerpts_checked':24,'new_passages_disjoint_and_buffered_from_phases20_21':True,
        'distinct_new_keys':len(new_keys),'frozen_code_and_protocol_unchanged_since':base,'key_search_receives_fit_ciphertext_only':True,
        'same_keys_for_baseline_and_corrected':True,'original_boundaries_preserved_everywhere':True,
        'strict_objective_independently_checked':True,
        'scope':'Internal independent Python calculation using shared source models; not an external replication.'})


if __name__=='__main__':main()
