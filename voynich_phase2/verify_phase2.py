#!/usr/bin/env python3
"""Integrity, score and held-out recovery checks; does not claim decipherment."""
import collections, csv, hashlib, json, math, random, re
from pathlib import Path
from search_keys import ROOT, BASE, DATA, OUT, SEED, clean, lm_build, score, parse
from extended_search import build

def read(name):
    return json.loads((OUT/(name+'.json')).read_text())

def main():
    meta=json.loads((ROOT/'SOURCES_AND_LIMITS.json').read_text())
    for src in meta['sources']:
        if 'sha256' in src:
            assert hashlib.sha256((ROOT/src['file']).read_bytes()).hexdigest()==src['sha256']
    corpora={n:parse(n)[0] for n in ('ZL3b-n.txt','IT2a-n.txt')}
    lm,_=lm_build()
    plain=clean((BASE/'controls/input/nathist_book16.txt').read_text())
    a=list('abcdefghijklmnopqrstuvwxyz');random.Random(SEED).shuffle(a)
    cipher=plain.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz',''.join(a)))
    ctl=read('latin_hidden_key_control')
    decoded=cipher[24000:].translate(str.maketrans('abcdefghijklmnopqrstuvwxyz',ctl['key']))
    latin_errors=sum(a!=b for a,b in zip(decoded,plain[24000:]))
    assert len(decoded)==28641 and latin_errors==2
    assert math.isclose(score([cipher[24000:]],ctl['key'],lm),ctl['heldout_cross_entropy_bits'],abs_tol=1e-10)

    raw=(DATA/'dante.txt').read_text();starts=list(re.finditer(r'INFERNO\nInferno\nCanto I\n',raw))
    assert len(starts)==2
    unique=raw[:starts[1].start()]
    assert unique.strip()==raw[starts[1].start():].strip()
    before,after=unique.split('\nPARADISO\n',1)
    def poem(t):
        return clean('\n'.join(l for l in t.splitlines() if l.strip() and not re.match(r'^(INFERNO|PURGATORIO|PARADISO|Inferno|Purgatorio|Paradiso|Canto\b)',l)))
    training=poem(before);plain_it=poem(after)
    assert training==(DATA/'italian_train.txt').read_text()
    lm_it,_=build(training)
    a=list('abcdefghijklmnopqrstuvwxyz');random.Random(SEED+1).shuffle(a)
    cipher_it=plain_it.translate(str.maketrans('abcdefghijklmnopqrstuvwxyz',''.join(a)))
    ctl_it=read('italian_hidden_key_control')
    actual=cipher_it[24000:].translate(str.maketrans('abcdefghijklmnopqrstuvwxyz',ctl_it['key']))
    assert len(actual)==109933 and actual==plain_it[24000:]
    assert math.isclose(score([cipher_it[24000:]],ctl_it['key'],lm_it),ctl_it['heldout_cross_entropy_bits'],abs_tol=1e-10)

    base_names=['eva_ZL_all','eva_ZL_A','eva_ZL_B','eva_IT_all','naibbe_permutation_ZL','naibbe_permutation_IT']
    expanded=json.loads((OUT/'extended_summary.json').read_text())
    real=[read(n) for n in base_names]+[r for r in expanded if r['case'].startswith('extended_')]
    assert len(real)==30 and len({r['case'] for r in real})==30
    # Recompute every saved training score with its key and corresponding model.
    for r in real:
        assert len(r['key'])==26 and set(r['key'])==set('abcdefghijklmnopqrstuvwxyz')
        assert 'candidate_preview_NON_TRANSLATION' in r
        segments=(DATA/(r['case']+'_train.txt')).read_text().splitlines()
        model=lm_it if r['case'].startswith('extended_italian_') else lm
        assert abs(score(segments,r['key'],model)-r['training_cross_entropy_bits'])<0.0001
        assert all(math.isfinite(r[k]) for k in ('training_cross_entropy_bits','heldout_cross_entropy_bits'))
        assert sum(map(len,segments))==r['training_chars']
    leaves={r['leaf'] for r in corpora['ZL3b-n.txt'] if r['type'].startswith('P')}
    test=set(sorted(leaves)[::5]);train=leaves-test
    assert not test.intersection(train)

    rows=list(csv.DictReader((OUT/'illustration_anchors.csv').open()))
    stats=read('anchors_summary')
    assert len(rows)==stats['illustration_labels']==729
    assert sum(r['exact_agreement']=='True' for r in rows)==stats['exact_agreement_all']==497
    assert sum(r['label_type']=='Lz' for r in rows)==299
    assert all(r['meaning']=='UNKNOWN' for r in rows)
    assert sum(r['exact_agreement']=='True' and int(r['paragraph_occurrences'])>0 for r in rows)==258
    lm_build()  # Leave the default model in its documented Latin state.
    result={'status':'PASS','source_hashes':'PASS','real_configurations':30,
            'latin_control_test_letters':28641,'latin_control_errors':latin_errors,
            'italian_control_test_letters':109933,'italian_control_errors':0,
            'saved_training_scores_recomputed':30,'labels':729,'agreeing_labels':497,
            'extended_train_leaves':len(train),'extended_test_leaves':len(test),
            'warning':'Integrity and restricted controls passed. No Voynich plaintext validated.'}
    (OUT/'verification_phase2.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
