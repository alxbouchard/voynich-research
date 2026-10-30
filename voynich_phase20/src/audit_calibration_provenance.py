#!/usr/bin/env python3
"""Post-run audit of source excerpts, split separation and frozen code.

CC BY-SA 4.0; see phase README for attribution.
"""
from collections import defaultdict
import hashlib
import json
import random
import subprocess
import calibration as study


def main():
    p=study.protocol()
    assert hashlib.sha256(subprocess.check_output([
        'git','show','be58b42:voynich_phase20/CALIBRATION_PROTOCOL.json'],cwd=study.REPO)).hexdigest()==study.sha(study.PFILE)
    for name,digest in p['code_sha256'].items():
        content=subprocess.check_output(['git','show','be58b42:voynich_phase20/'+name],cwd=study.REPO)
        assert hashlib.sha256(content).hexdigest()==digest
    raw={x['case']:x for x in study.read(study.REPO/'voynich_phase10/data/source_inputs.json')}
    ranges=defaultdict(list);seen_keys=set();n=0
    for i,case in enumerate(study.read(study.DATA/'cases.json')):
        truth=study.read(study.DATA/case['case']/'truth.json')
        source=p['languages'][case['language']]
        assert truth['source']==source
        words=[w for line in raw[source]['lines'] for w in line['words'] if w]
        for split in ('fit','transfer'):
            start,end=truth['source_word_ranges'][split]
            assert ' '.join(words[start:end])==truth['plaintext_'+split]
            assert 0<=start<end<=len(words)
            ranges[source].append((start,end))
        assert truth['source_word_ranges']['transfer'][0]-truth['source_word_ranges']['fit'][1]==p['gap_words']
        key=list(study.ALPHABET);random.Random(p['encryption_seed']+(i//6)*100+i%6).shuffle(key)
        assert ''.join(key)==truth['encryption_key']
        assert truth['encryption_key'] not in seen_keys;seen_keys.add(truth['encryption_key'])
        for mode in ('initializer','greedy','exact'):
            result=study.read(study.OUT/case['case']/(mode+'.json'))
            command=result['identity']['command']
            assert command[3]==str(study.DATA/case['case']/'fit.txt')
            assert all('truth' not in str(arg) and 'transfer' not in str(arg) for arg in command)
        n+=1
    for source,intervals in ranges.items():
        ordered=sorted(intervals)
        assert all(a[1]<=b[0] for a,b in zip(ordered,ordered[1:]))
    result={'passed':True,'controls':n,'source_excerpts_checked':2*n,
            'all_source_ranges_disjoint_within_work':True,'gap_words':p['gap_words'],
            'encryption_seeds_reconstructed':True,'distinct_encryption_keys':len(seen_keys),
            'frozen_protocol_and_code_unchanged_since':'be58b42',
            'optimizer_commands_use_fit_ciphertext_only':True,
            'scope':'Post-run provenance audit; not an additional fit or an external preregistration.'}
    study.save(study.OUT/'provenance_verification.json',result)
    print(json.dumps(result),flush=True)


if __name__=='__main__':
    main()
