#!/usr/bin/env python3
"""Independent phase-21 decoding, scoring, segmentation and provenance audit. CC BY-SA 4.0."""
from collections import defaultdict
import hashlib
import json
import subprocess
import common as c
import study
from reference import Reference
import verify_calibration as old_verify
import audit_author_segmentation as old_score


def measured(text,truth):
    def parse(s):
        letters=[];boundaries=set()
        for x in s:
            if x==' ':boundaries.add(len(letters))
            else:letters.append(x)
        boundaries.discard(0);boundaries.discard(len(letters))
        return letters,boundaries
    a,ap=parse(text);b,bp=parse(truth);assert len(a)==len(b)
    return {'character_accuracy':sum(x==y for x,y in zip(a,b))/len(b),
            'boundary_f1':2*len(ap&bp)/(len(ap)+len(bp)) if ap or bp else 1.}


def main():
    p=study.check_inputs();summary=c.read(c.OUT/'summary.json');env=c.read(c.DATA/'environment.json')
    base=env['run_base_commit']
    assert hashlib.sha256(subprocess.check_output(['git','show',base+':voynich_phase21/PROTOCOL.json'],cwd=c.REPO)).hexdigest()==c.sha(study.PFILE)
    for path,digest in p['sha256'].items():
        # Hydrated historical data are checked against their fixed hashes by
        # check_inputs; only tracked code has a Git blob at the freeze commit.
        if '/src/' in path or path.endswith('DEVELOPMENT_PLAN.json'):
            content=subprocess.check_output(['git','show',base+':'+path],cwd=c.REPO)
            assert hashlib.sha256(content).hexdigest()==digest
    raw={x['case']:x for x in c.read(c.REPO/'voynich_phase10/data/source_inputs.json')}
    old_ranges=defaultdict(list);old_keys=set()
    for case in c.read(c.OLD/'data/calibration/cases.json'):
        truth=c.read(c.OLD/'data/calibration'/case['case']/'truth.json')
        old_ranges[case['language']].extend(truth['source_word_ranges'].values());old_keys.add(truth['encryption_key'])
    current=defaultdict(list);new_keys=set();checked=0;optima=0;maximum_error=0.
    for language in p['languages']:
        model=Reference(language);closed=old_verify.load_model(c.TMP/'closed'/language)
        for case in summary['cases']:
            if case['language']!=language:continue
            name=case['case'];folder=c.DATA/'controls'/name;truth=c.read(folder/'truth.json')
            assert truth['source']==p['languages'][language]
            words=[w for line in raw[truth['source']]['lines'] for w in line['words'] if w]
            assert truth['encryption_key'] not in old_keys|new_keys;new_keys.add(truth['encryption_key'])
            for split,(start,end) in truth['source_word_ranges'].items():
                assert ' '.join(words[start:end])==truth['plaintext_'+split]
                current[language].append((start,end))
                for a,b in old_ranges[language]:
                    assert end<=a-p['old_passage_buffer_words'] or start>=b+p['old_passage_buffer_words']
            for mode in ('initializer','closed','open'):
                command=c.read(c.OUT/'controls'/name/(mode+'.json'))['identity']['command']
                assert command[3]==str(folder/'fit.txt')
                assert all('transfer' not in arg and 'truth' not in arg for arg in command)
            for mode,row in case['rows'].items():
                key=row['key'];assert set(key)==set(c.ALPHABET) and len(key)==26
                for split in ('fit','transfer'):
                    ciphertext=(folder/(split+'.txt')).read_text().strip()
                    expected=truth['plaintext_'+split]
                    assert ''.join(truth['encryption_key'][ord(x)-97] for x in expected if x!=' ')==ciphertext
                    decoded=''.join(key[ord(x)-97] for x in ciphertext)
                    text=row[split]['segmentation'];assert text.replace(' ','')==decoded
                    for field,value in measured(text,expected).items():assert abs(value-row[split][field])<1e-12
                    if mode in ('closed','oracle_closed'):score=old_score.full_score(text,closed)['combined_score_ln']
                    else:score=model.full(text,p['beta'],p['penalty'])
                    error=abs(score-row[split]['score']);maximum_error=max(maximum_error,error)
                    assert error<1e-8*len(decoded)
                    if mode in ('open','oracle_open'):
                        optimum=model.exact(decoded,p['beta'],p['penalty'])
                        assert abs(optimum['score']-score)<1e-8*len(decoded);optima+=1
                    checked+=1
            m=case['rows']['open']['transfer']
            assert case['passes_gate']==(m['character_accuracy']>=p['gate']['character_accuracy'] and m['boundary_f1']>=p['gate']['boundary_f1'])
            print(json.dumps({'verified':name}),flush=True)
    for intervals in current.values():
        ordered=sorted(intervals);assert all(a[1]<=b[0] for a,b in zip(ordered,ordered[1:]))
    assert len(summary['cases'])==12 and len(new_keys)==12
    assert summary['passed']==sum(x['passes_gate'] for x in summary['cases'])
    assert summary['voynich_gate_open']==all(x['passes_gate'] for x in summary['cases'])
    result={'passed':True,'scored_outputs_checked':checked,'exact_open_optima_recomputed':optima,
            'maximum_score_difference':maximum_error,'source_excerpts_checked':24,
            'new_passages_disjoint_and_buffered_from_phase20':True,'distinct_new_keys':len(new_keys),
            'frozen_code_and_protocol_unchanged_since':base,'key_search_receives_fit_ciphertext_only':True,
            'scope':'Internal independent Python calculation using shared source models; not an external replication.'}
    c.save(c.OUT/'verification.json',result)


if __name__=='__main__':main()
